from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, \
    ComparisonExpression, ComparisonComparators, Pattern, CombinedComparisonExpression, CombinedObservationExpression
import logging
import re
from datetime import datetime, timedelta
from os import path
import json

logger = logging.getLogger(__name__)

START_STOP_PATTERN = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z)"
MAC = '^(([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2}))$'
CONFIG_MAP_PATH = "json/config_map.json"
FIELDS_MAP_PATH = "json/fields_map.json"

STOP_TIME = datetime.utcnow()


class StartStopQualifierValueException(Exception):
    pass


class FileNotFoundException(Exception):
    pass


class QueryStringPatternTranslator:
    """
    translate stix pattern to native data source query language
    """

    def __init__(self, pattern: Pattern, data_model_mapper, options):
        logger.info("Palo Alto Cortex XDR Connector")
        self.dmm = data_model_mapper
        self.options = options
        self.timeframe = []
        self.comparator_lookup = self.dmm.map_comparator()
        self.config_map = self.load_json(CONFIG_MAP_PATH)
        self.all_fields_map = self.load_json(FIELDS_MAP_PATH)
        self.translated_query = self.parse_expression(pattern)
        self.qualified_query = self._create_formatted_query(self.dmm, self.translated_query,
                                                            self.timeframe, self.all_fields_map, options)

    @staticmethod
    def load_json(rel_path_of_file):
        """
        Consumes a json file and returns a dictionary
        :param rel_path_of_file: str
        :return: dict
        """

        _json_path = path.dirname(path.realpath(__file__)) + "/" + rel_path_of_file
        try:
            if path.exists(_json_path):
                with open(_json_path, encoding='utf-8') as f_obj:
                    return json.load(f_obj)
            raise FileNotFoundException
        except FileNotFoundException as e:
            raise FileNotFoundError(f'{rel_path_of_file} not found') from e

    @staticmethod
    def _create_formatted_query(dmm, translated_query, timeframe, all_fields_map, options):
        """
        Formation of Palo Alto - native query language structure
        :param dmm
        :param translated_query:str
        :param timeframe:list
        :param all_fields_map:dict
        :param options:dict
        :return: formatted_query :list
        """
        limit = options["result_limit"]
        dataset_name = dmm.dialect
        all_fields = all_fields_map["all_fields"]  # all_fields included in to_stix_mapping
        fields = ','.join(all_fields)
        query = f'dataset = {dataset_name} | filter {translated_query} | alter dataset_name = \"{dataset_name}\" ' \
                f'| fields dataset_name,{fields} | limit {limit} '  # adding custom field 'dataset_name' to query,
        # since this 'dataset_name' field will be used in translate results
        formatted_query = {
            dataset_name: {"query": query, "timeframe": {"from": min(timeframe), "to": max(timeframe)}}}
        return [formatted_query]

    def _format_set(self, values, mapped_field_type, mapped_fields_array) -> str:
        """
        Formats value in the event of set operation
        :param values
        :param mapped_field_type: str
        :param mapped_fields_array: list
        :return formatted value
        """
        gen = values.element_iterator()
        formatted_value = ','.join(QueryStringPatternTranslator._escape_value(
            self._format_value_type(value, mapped_field_type, mapped_fields_array), mapped_field_type)
                                   for value in gen)
        return f'({formatted_value})'

    @staticmethod
    def _format_match(value, mapped_field_type) -> str:
        """
        Formats value in the event of match operation
        :param value
        :param mapped_field_type:str
        :return formatted string type value
        """
        if mapped_field_type != "string":
            raise NotImplementedError('MATCHES operators is supported only for string type input')
        if '^' in value and value.index('^') != 0:
            raise NotImplementedError('^ symbol should be at the starting position of the expression')
        if '$' in value and value.index('$') != len(value) - 1:
            raise NotImplementedError('$ symbol should be at the ending position of the expression')
        value = '{}'.format(value.replace('\\', '\\\\').replace('\"', '\\"').replace('(', '\\(').replace(')', '\\)'))
        return f'\"{value}\"'

    @staticmethod
    def _format_equality(value, mapped_field_type) -> str:
        """
        Formats value in the event of equality operation
        :param value
        :param mapped_field_type: str
        :return formatted value
        """
        return QueryStringPatternTranslator._escape_value(value, mapped_field_type)

    @staticmethod
    def _format_like(value, mapped_field_type) -> str:
        """
        Formats value in the event of LIKE operation
        :param value
        :param mapped_field_type: str
        :return formatted value
        """
        if mapped_field_type != "string":
            raise NotImplementedError("LIKE operator is supported only for string type input")
        return QueryStringPatternTranslator._escape_value(value, mapped_field_type)

    @staticmethod
    def _escape_value(value, mapped_field_type) -> str:
        """
        adds escape characters to string type value
        :param value
        :param mapped_field_type: str
        :return formatted value
        """
        if isinstance(value, str) and mapped_field_type != "enum":
            value = f'\"{value}\"'
        return str(value)

    def _check_enum_supported_values(self, converted_value, mapped_fields_array):
        """
        checks for enum supported values
        :param mapped_fields_array: list
        :param converted_value:str
        :return enum formatted value :str
        """
        try:
            formatted_values = converted_value.upper()
            if formatted_values not in self.config_map["enum_supported_values"][mapped_fields_array[0]]:
                raise NotImplementedError(f'Unsupported ENUM values provided. Possible supported enum values are'
                                          f'{self.config_map["enum_supported_values"][mapped_fields_array[0]]}')
            return f'ENUM.{formatted_values}'
        except (KeyError, IndexError, TypeError) as e:
            raise KeyError(f'{mapped_fields_array[0]} is not found in enum_supported_values') from e

    def _format_value_type(self, value, mapped_field_type, mapped_fields_array):
        """
        check input value format that matches with the mapped field value type
        :param value
        :param mapped_field_type: str
        :param mapped_fields_array: list
        :return formatted value
        """
        converted_value = str(value)
        if mapped_field_type == "enum":
            converted_value = self._check_enum_supported_values(converted_value, mapped_fields_array)
        elif mapped_field_type == "timestamp":
            converted_value = QueryStringPatternTranslator._format_datetime(converted_value)
        elif mapped_field_type == "mac":
            compile_mac_regex = re.compile(MAC)
            if not compile_mac_regex.search(converted_value):
                raise NotImplementedError(f'Invalid mac address - {converted_value} provided')
        elif mapped_field_type == "int":
            if not converted_value.isdigit():
                raise NotImplementedError(f'string type input - {converted_value} is not supported for '
                                          f'integer type fields')
            converted_value = int(value)
        elif mapped_field_type == "boolean":
            converted_value = QueryStringPatternTranslator._check_boolean_value(converted_value)
        return converted_value

    def _check_value_comparator_support(self, value, comparator, mapped_field_type):
        """
        checks the comparator and value support
        :param value
        :param comparator
        :param mapped_field_type: str
        """
        operator = self.comparator_lookup[str(comparator)]
        if mapped_field_type == "enum" and (comparator not in [ComparisonComparators.Equal, ComparisonComparators.In,
                                                               ComparisonComparators.NotEqual]):
            raise NotImplementedError(f'{operator} operator is not supported for Enum type input. Possible supported '
                                      f'operator are [=,!=,in,not in]')
        if isinstance(value, str) and comparator not in [ComparisonComparators.Equal, ComparisonComparators.NotEqual,
                                                         ComparisonComparators.Like, ComparisonComparators.Matches]:
            raise NotImplementedError(f'{operator} operator is not supported for string type input')
        if isinstance(value, bool) and comparator not in [ComparisonComparators.Equal, ComparisonComparators.NotEqual]:
            raise NotImplementedError(f'{operator} operator is not supported for Boolean type input')

    @staticmethod
    def _check_boolean_value(converted_value):
        """
        returns boolean value of input
        :param converted_value:str
        :return bool
        """
        if converted_value.lower() == "true" or (converted_value.isdigit() and converted_value == "1"):
            boolean_value = bool(True)
        elif converted_value.lower() == "false" or (converted_value.isdigit() and converted_value == "0"):
            boolean_value = bool(False)
        else:
            raise NotImplementedError('Invalid boolean type input')
        return boolean_value

    @staticmethod
    def _format_negate(comparator):
        """
        returns negation of input operator
        :param comparator:str
        :return str
        """
        negate_comparator = {
            ">": "<=",
            ">=": "<",
            "<": ">=",
            "<=": ">",
            "=": "!=",
            "!=": "=",
            "contains": "not contains",
            "in": "not in",
            "~=": "!~="
        }
        return negate_comparator[comparator]

    @staticmethod
    def _format_datetime(value):
        """
        Converts timestamp to milliseconds
        :param value
        :return: int, converted epoch value
        """
        try:
            time_pattern = '%Y-%m-%dT%H:%M:%S.%fZ'
            if re.search(r"\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}Z", str(value)):  # without milli seconds
                time_pattern = '%Y-%m-%dT%H:%M:%SZ'
            epoch = datetime(1970, 1, 1)
            converted_time = int(((datetime.strptime(value,
                                                     time_pattern) - epoch).total_seconds()) * 1000)
            return converted_time
        except ValueError:
            pass
        raise NotImplementedError(f'cannot convert the timestamp {value} to milliseconds')

    @staticmethod
    def _check_time_range_values(converted_timestamp):
        """
        checks for valid start and stop time
        :param converted_timestamp: list
        """
        if converted_timestamp[0] > converted_timestamp[1]:
            raise StartStopQualifierValueException('Start time should be lesser than Stop time')

    @staticmethod
    def _parse_time_range(qualifier, time_range):
        """
        Converts qualifier timestamp to epoch
        :param qualifier: str
        :param time_range: int
        return: list of converted epoch values
        """
        try:
            compile_timestamp_regex = re.compile(START_STOP_PATTERN)
            converted_timestamp = []
            if qualifier and compile_timestamp_regex.search(qualifier):
                time_range_iterator = compile_timestamp_regex.finditer(qualifier)
                time_range_list = [each.group() for each in time_range_iterator]
            else:
                start_time = STOP_TIME - timedelta(minutes=time_range)
                converted_start_time = start_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                # limit 3 digit value for millisecond
                converted_stop_time = STOP_TIME.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                time_range_list = [converted_start_time, converted_stop_time]
            for timestamp in time_range_list:
                converted_time = QueryStringPatternTranslator._format_datetime(timestamp)
                converted_timestamp.append(converted_time)
            return converted_timestamp
        except (KeyError, IndexError, TypeError) as e:
            raise e

    def _add_timestamp_to_query(self, query, qualifier):
        """
        adds timestamp filter to Palo Alto Cortex XDR query
        :param query: str
        :param qualifier
        :return str
        """
        converted_timestamp = QueryStringPatternTranslator._parse_time_range(qualifier, self.options["time_range"])
        QueryStringPatternTranslator._check_time_range_values(converted_timestamp)  # check timestamp value range
        self.timeframe += converted_timestamp
        if self.dmm.dialect in self.config_map["timestamp_supported_dataset"].keys():
            timestamp_field_name = self.config_map["timestamp_supported_dataset"][self.dmm.dialect]
            timestamp_field = f' and (to_epoch({timestamp_field_name},\"millis\") >= {converted_timestamp[0]} and ' \
                              f'to_epoch({timestamp_field_name},\"millis\") <= {converted_timestamp[1]})'
            if timestamp_field not in query:
                query = f'({query} {timestamp_field})'
        else:
            query = f'({query})'
        return query

    def _check_mapped_field_type(self, mapped_field_array):
        """
        Returns the type of mapped field array
        :param mapped_field_array: list
        :return: str
        """
        mapped_field = mapped_field_array[0]
        mapped_field_type = "string"
        for key, value in self.config_map.items():
            if mapped_field in value and key in ["int_supported_fields", "enum_supported_fields",
                                                 "boolean_supported_fields", "timestamp_supported_fields",
                                                 "mac_supported_fields"]:
                mapped_field_type = key.split('_')[0]
                break
        return mapped_field_type

    @staticmethod
    def _parse_mapped_fields(value, comparator, mapped_fields_array):
        """
        parse mapped fields into boolean expression
        :param value: str
        :param comparator: str
        :param mapped_fields_array: list
        :return: str
        """
        comparison_string = ""
        mapped_fields_count = len(mapped_fields_array)
        for field_name in mapped_fields_array:
            comparison_string += f'{field_name} {comparator} {value}'
            if mapped_fields_count > 1:
                comparison_string += " or "
                mapped_fields_count -= 1
        if len(mapped_fields_array) > 1:
            # More than one data source field maps to the STIX attribute, so group comparisons together.
            grouped_comparison_string = "(" + comparison_string + ")"
            comparison_string = grouped_comparison_string
        return comparison_string

    def _lookup_comparison_operator(self, expression_operator):
        """
        lookup operators support in Palo Alto Cortex XDR
        :param expression_operator:enum object
        :return str
        """
        if str(expression_operator) not in self.comparator_lookup:
            raise NotImplementedError(
                f'Comparison operator {expression_operator.name} unsupported for Palo Alto Cortex XDR connector')

        return self.comparator_lookup[str(expression_operator)]

    def _eval_comparison_value(self, expression, mapped_field_type, mapped_fields_array):
        """
        Function for parsing comparison expression value
        :param expression: expression object
        :param mapped_field_type:str
        :param mapped_fields_array:list
        :return: formatted expression value
        """
        if expression.comparator == ComparisonComparators.Matches:
            value = QueryStringPatternTranslator._format_match(expression.value, mapped_field_type)
        elif expression.comparator == ComparisonComparators.In:
            value = self._format_set(expression.value, mapped_field_type, mapped_fields_array)
        elif expression.comparator in [ComparisonComparators.GreaterThan, ComparisonComparators.GreaterThanOrEqual,
                                       ComparisonComparators.LessThan, ComparisonComparators.LessThanOrEqual,
                                       ComparisonComparators.Equal, ComparisonComparators.NotEqual]:
            value = self._format_value_type(expression.value, mapped_field_type, mapped_fields_array)
            self._check_value_comparator_support(value, expression.comparator, mapped_field_type)
            value = self._format_equality(value, mapped_field_type)
        elif expression.comparator == ComparisonComparators.Like:
            value = self._format_value_type(expression.value, mapped_field_type, mapped_fields_array)
            value = self._format_like(value, mapped_field_type)
        else:
            raise NotImplementedError('Unknown comparator expression operator')
        return value

    def _eval_combined_comparison_exp(self, expression):
        """
        Function for parsing combined comparison expression
        :param expression: expression object
        """
        operator = self._lookup_comparison_operator(expression.operator)
        expression_01 = self._parse_expression(expression.expr1)
        expression_02 = self._parse_expression(expression.expr2)
        if not expression_01 or not expression_02:
            return ''
        if isinstance(expression.expr1, CombinedComparisonExpression):
            expression_01 = f'{expression_01}'
        if isinstance(expression.expr2, CombinedComparisonExpression):
            expression_02 = f'{expression_02}'

        query_string = f'{expression_01} {operator} {expression_02}'
        return f'{query_string}'

    def _eval_combined_observation_exp(self, expression, qualifier=None):
        """
        Function for parsing combined observation expression
        :param expression: expression object
        :param qualifier: qualifier
        """
        operator = self._lookup_comparison_operator(expression.operator)
        expression_01 = self._parse_expression(expression.expr1, qualifier)
        expression_02 = self._parse_expression(expression.expr2, qualifier)
        query = ''
        if expression_01 and expression_02:
            query = f'{expression_01} {operator} {expression_02}'
        elif expression_01:
            query = f'{expression_01}'
        elif expression_02:
            query = f'{expression_02}'
        return query

    def _parse_expression(self, expression, qualifier=None) -> str:
        """
        parse ANTLR pattern to Palo Alto Cortex XDR query
        :param expression: expression object, ANTLR parsed expression object
        :param qualifier: str, default in None
        :return str
        """
        if isinstance(expression, ComparisonExpression):  # Base Case
            stix_objects = expression.object_path.split(':')
            mapped_fields_array = self.dmm.map_field(stix_objects[0], stix_objects[1])
            comparator = self._lookup_comparison_operator(expression.comparator)
            if expression.negated:
                comparator = QueryStringPatternTranslator._format_negate(comparator)
            mapped_field_type = self._check_mapped_field_type(mapped_fields_array)
            value = self._eval_comparison_value(expression, mapped_field_type, mapped_fields_array)

            comparison_string = self._parse_mapped_fields(value, comparator, mapped_fields_array)
            return comparison_string

        elif isinstance(expression, CombinedComparisonExpression):
            return self._eval_combined_comparison_exp(expression)
        elif isinstance(expression, ObservationExpression):
            query_string = self._parse_expression(expression.comparison_expression)
            return self._add_timestamp_to_query(query_string, qualifier)

        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            if isinstance(expression.observation_expression, CombinedObservationExpression):
                operator = self._lookup_comparison_operator(expression.observation_expression.operator)
                expression_01 = self._parse_expression(expression.observation_expression.expr1, expression.qualifier)
                expression_02 = self._parse_expression(expression.observation_expression.expr2, expression.qualifier)
                query_string = f'{expression_01} {operator} {expression_02}'
            else:
                query_string = self._parse_expression(expression.observation_expression, expression.qualifier)
            if qualifier is not None:
                query_string = self._add_timestamp_to_query(query_string, qualifier)
            return query_string
        elif isinstance(expression, CombinedObservationExpression):
            return self._eval_combined_observation_exp(expression, qualifier)
        elif isinstance(expression, Pattern):
            return f'{self._parse_expression(expression.expression)}'
        else:
            raise RuntimeError(f'Unknown Recursion Case for expression={expression},'
                               f' type(expression)={type(expression)}')

    def parse_expression(self, pattern: Pattern):
        return self._parse_expression(pattern)


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    """
        Conversion of ANTLR pattern to Palo ALTO CORTEX XDR query
        :param pattern: expression object, ANTLR parsed expression object
        :param data_model_mapping: DataMapper object, mapping object obtained by parsing json
        :param options: dict, time_range defaults to 5
        :return: list, PALO ALTO  queries
        """

    query = QueryStringPatternTranslator(pattern, data_model_mapping, options).qualified_query
    return query
