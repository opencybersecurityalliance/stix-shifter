""" This Module will convert Stix Pattern to RHACS data source supported query """
import re
import json
import logging
from os import path
from datetime import datetime, timedelta
from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, \
    ComparisonExpression, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression

logger = logging.getLogger(__name__)

START_STOP_PATTERN = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z)"
TYPE_MAP_PATH = "json/type_map.json"

STOP_TIME = datetime.utcnow()


class StartStopQualifierValueException(Exception):
    """ Start Stop qualifier exception """
    pass


class FileNotFoundException(Exception):
    """ file not found exception """
    pass


class QueryStringPatternTranslator:
    """
    translate stix pattern to native data source query language
    """

    def __init__(self, pattern: Pattern, data_model_mapper, options):
        logger.info("RHACS Connector")
        self.dmm = data_model_mapper
        self.options = options
        self.timeframe = []
        self.comparator_lookup = self.dmm.map_comparator()
        self.type_map = self.load_json(TYPE_MAP_PATH)
        self.translated_query = self.parse_expression(pattern)

    @staticmethod
    def load_json(rel_path_of_file):
        """
        Consumes a json file and returns a dictionary
        :param rel_path_of_file: str
        :return: dict
        """
        _json_path = path.abspath(path.join(path.join(__file__, ".."), rel_path_of_file))
        try:
            if path.exists(_json_path):
                with open(_json_path, encoding='utf-8') as f_obj:
                    return json.load(f_obj)
            raise FileNotFoundException
        except FileNotFoundException as ex:
            raise FileNotFoundError(f'{rel_path_of_file} not found') from ex

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
        return f'{value}'

    @staticmethod
    def _format_equality(value) -> str:
        """
        Formats value in the event of equality operation
        :param value
        :return formatted value
        """
        return QueryStringPatternTranslator._escape_value(value)

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
        return f'{value}.*'

    @staticmethod
    def _escape_value(value) -> str:
        """
        adds escape characters to string type value
        :param value
        :return formatted value
        """
        if isinstance(value, str):
            value = f'"{value}"'
        return value

    @staticmethod
    def _format_datetime(value):
        """
        Converts timestamp to month/date/year format
        :param value
        :return: str, converted month/date/year format
        """
        match = re.findall(r'\d{4}-\d{2}-\d{2}', value)
        filter_value = match[0]
        filter_value = filter_value.split('-')
        value = f'{filter_value[1]}/{filter_value[2]}/{filter_value[0]}'
        return value

    def _field_severity(self, comparator, value):
        """
        check for severity and convert input value to
        LOW_SEVERITY,MEDIUM_SEVERITY,HIGH_SEVERITY
        param comparator
        param value
        return value(str)
        """
        if comparator not in [":", ":!"]:
            raise NotImplementedError(f'{comparator} comparator is not supported with this field')

        value = int(value)
        if 1 <= int(value) <= 25:
            value = str("LOW_SEVERITY")
        elif 26 <= int(value) <= 50:
            value = str("MEDIUM_SEVERITY")
        elif 51 <= int(value) <= 75:
            value = str("HIGH_SEVERITY")
        elif 76 <= int(value) <= 100:
            value = str("CRITICAL_SEVERITY")
        else:
            raise NotImplementedError('only 1-100 integer values are supported with this field')
        return f'"{value}"'

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
        elif mapped_field_type == "int":
            if not converted_value.isdigit():
                raise NotImplementedError(f'string type input - {converted_value} is '
                                          f'not supported for integer type fields')

            converted_value = int(value)

        elif mapped_field_type == "boolean":
            converted_value = QueryStringPatternTranslator._check_boolean_value(converted_value)

        elif mapped_field_type == "timestamp":
            converted_value = QueryStringPatternTranslator._format_datetime(converted_value)

        return converted_value

    def _check_enum_supported_values(self, converted_value, mapped_fields_array):
        """
        checks for enum supported values
        :param mapped_fields_array: list
        :param converted_value:str
        :return enum formatted value :str
        """
        try:
            formatted_values = converted_value.upper()
            if formatted_values not in self.type_map["enum_supported_values"][mapped_fields_array[0]]:
                raise NotImplementedError(f'Unsupported ENUM values provided. '
                                          f'Possible supported enum values are'
                                          f'{self.type_map["enum_supported_values"][mapped_fields_array[0]]}')
            return f'{formatted_values}'
        except (KeyError, IndexError, TypeError) as ex:
            raise KeyError(f'{mapped_fields_array[0]} is not found in enum_supported_values') from ex

    def _check_value_comparator_support(self, comparator, mapped_field_type):
        """
        checks the comparator and value support
        :param comparator
        :param mapped_field_type: str
        """
        operator = self.comparator_lookup[str(comparator)]

        if mapped_field_type == 'string' and comparator not in [ComparisonComparators.Equal,
                                                                ComparisonComparators.NotEqual,
                                                                ComparisonComparators.Like,
                                                                ComparisonComparators.Matches]:
            raise NotImplementedError(f'{operator} operator is not supported for string type input')

        if mapped_field_type == 'int' and comparator not in [ComparisonComparators.Equal,
                                                             ComparisonComparators.NotEqual,
                                                             ComparisonComparators.GreaterThan,
                                                             ComparisonComparators.GreaterThanOrEqual,
                                                             ComparisonComparators.LessThanOrEqual,
                                                             ComparisonComparators.LessThan]:
            raise NotImplementedError(f'{operator} operator is not supported for integer type input')

        if mapped_field_type == 'enum' and comparator not in [ComparisonComparators.Equal,
                                                              ComparisonComparators.NotEqual
                                                              ]:
            raise NotImplementedError(f'{operator} operator is not supported for enum type input')

        if mapped_field_type == 'boolean' and comparator not in [ComparisonComparators.Equal]:
            raise NotImplementedError(f'{operator} operator is not supported for boolean type input')

        if mapped_field_type == 'timestamp' and comparator not in [ComparisonComparators.Equal,
                                                                   ComparisonComparators.GreaterThan,
                                                                   ComparisonComparators.GreaterThanOrEqual,
                                                                   ComparisonComparators.LessThanOrEqual,
                                                                   ComparisonComparators.LessThan
                                                                   ]:
            raise NotImplementedError(f'{operator} operator is not supported for timestamp input')

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
            ":>": ":<=",
            ":>=": ":<",
            ":<": ":>=",
            ":<=": ":>",
            ":": ":!",
            ":!": ":",
            ":r/": ":!r/"
        }
        return negate_comparator[comparator]

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
            if qualifier and compile_timestamp_regex.search(qualifier):
                time_range_iterator = compile_timestamp_regex.finditer(qualifier)
                time_range_list = [each.group() for each in time_range_iterator]
            else:
                start_time = STOP_TIME - timedelta(minutes=time_range)
                converted_start_time = start_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                # limit 3 digit value for millisecond
                converted_stop_time = STOP_TIME.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                time_range_list = [converted_start_time, converted_stop_time]
        except (KeyError, IndexError, TypeError) as ex:
            raise ex
        return time_range_list

    def _add_timestamp_to_query(self, query, qualifier):
        """
        adds timestamp filter to rhacs query
        :param query: str
        :param qualifier
        :return str
        """
        match = re.search(r'Violation\s*Time:', query)
        if match:
            final_query = query
        else:
            converted_timestamp = \
                QueryStringPatternTranslator._parse_time_range(qualifier, self.options["time_range"])
            QueryStringPatternTranslator._check_time_range_values(converted_timestamp)
            self.timeframe += converted_timestamp
            final_query = f'{query}+Violation Time:>=' \
                          f'{QueryStringPatternTranslator._format_datetime(converted_timestamp[0])}'
        return final_query

    def _check_mapped_field_type(self, mapped_field_array):
        """
        Returns the type of mapped field array
        :param mapped_field_array: list
        :return: str
        """
        mapped_field = mapped_field_array[0]
        mapped_field_type = "string"
        for key, value in self.type_map.items():
            if mapped_field in value and key in ["int_supported_fields", "string_supported_fields",
                                                 "enum_supported_fields", "boolean_supported_fields",
                                                 "timestamp_supported_fields"]:
                mapped_field_type = key.split('_')[0]
                break
        return mapped_field_type

    @staticmethod
    def _parse_mapped_fields(value, comparator, mapped_fields_array):
        """
        parse mapped fields into query expression
        :param value: str
        :param comparator: str
        :param mapped_fields_array: list
        :return: str
        """
        comparison_string = ""
        for mapped_field in mapped_fields_array:
            comparison_string += f'{mapped_field}{comparator}{value}'

        return comparison_string

    def _lookup_comparison_operator(self, expression_operator):
        """
        lookup operators support in rhacs connector
        :param expression_operator:enum object
        :return str
        """
        if str(expression_operator) not in self.comparator_lookup:
            raise NotImplementedError(
                f'Comparison operator {expression_operator.name} unsupported for rhacs connector')

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

        elif expression.comparator in [ComparisonComparators.GreaterThan,
                                       ComparisonComparators.GreaterThanOrEqual,
                                       ComparisonComparators.LessThan,
                                       ComparisonComparators.LessThanOrEqual,
                                       ComparisonComparators.Equal,
                                       ComparisonComparators.NotEqual]:
            value = self._format_value_type(expression.value, mapped_field_type, mapped_fields_array)
            self._check_value_comparator_support(expression.comparator, mapped_field_type)
            if mapped_fields_array[0] == "Violation Time":
                value = f'{value}'
            else:
                value = self._format_equality(value)

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

        query_string = f'{expression_01}{operator}{expression_02}'
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
        parse ANTLR pattern to rhacs native query
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
            if mapped_fields_array[0] == "Severity":
                value = self._field_severity(comparator, value)

            comparison_string = self._parse_mapped_fields(value, comparator, mapped_fields_array)
            return comparison_string

        elif isinstance(expression, CombinedComparisonExpression):
            return self._eval_combined_comparison_exp(expression)

        elif isinstance(expression, ObservationExpression):
            query_string = self._parse_expression(expression.comparison_expression)
            query_string = self._add_timestamp_to_query(query_string, qualifier)
            return query_string

        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            if isinstance(expression.observation_expression, CombinedObservationExpression):
                operator = self._lookup_comparison_operator(expression.observation_expression.operator)
                expression_01 = self._parse_expression(expression.observation_expression.expr1,
                                                       expression.qualifier)
                expression_02 = self._parse_expression(expression.observation_expression.expr2,
                                                       expression.qualifier)
                query_string = f'{expression_01} {operator} {expression_02}'
            else:
                query_string = self._parse_expression(expression.observation_expression,
                                                      expression.qualifier)
            if qualifier is not None:
                query_string = self._add_timestamp_to_query(query_string, qualifier)
            return query_string

        elif isinstance(expression, CombinedObservationExpression):
            return self._eval_combined_observation_exp(expression, qualifier)

        elif isinstance(expression, Pattern):
            return self._parse_expression(expression.expression)
        else:
            raise RuntimeError(f'Unknown Recursion Case for expression={expression},'
                               f' type(expression)={type(expression)}')

    def parse_expression(self, pattern: Pattern):
        """
        Conversion of ANTLR pattern to rhacs query
        :param pattern: expression object, ANTLR parsed expression object
        :return: str, native query
        """
        if "ComparisonExpressionOperators.Or" in str(pattern):
            raise NotImplementedError("comparison expression OR operator is not supported in rhacs")

        return self._parse_expression(pattern)


def multiple_observation(query):
    """
    converts multiple observation query into separate queries
    param:query
    return list
    """
    query = query.split(' OR')
    return [query[i].strip() for i in range(len(query))]


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    """
        Conversion of ANTLR pattern to native data source query
        :param pattern: expression object, ANTLR parsed expression object
        :param data_model_mapping: DataMapper object, mapping object obtained by parsing json
        :param options: dict, time_range defaults to 5
        :return: string, rhacs  queries
    """
    query = QueryStringPatternTranslator(pattern, data_model_mapping, options).translated_query
    match = re.search(r'\s*OR\s*', query)
    if match:
        query = multiple_observation(query)
    return query
