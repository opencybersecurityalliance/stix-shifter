import re
import json
import copy
from os import path
from datetime import datetime, timedelta
from stix_shifter_utils.utils import logger
from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, \
    ComparisonExpression, ComparisonComparators, Pattern, CombinedComparisonExpression, CombinedObservationExpression, \
    ComparisonExpressionOperators

logger = logger.set_logger(__name__)

START_STOP_PATTERN = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z)"
STOP_TIME = datetime.utcnow()
CONFIG_MAP_PATH = "json/config_map.json"
SYMANTEC_EVENT_RETENTION_PERIOD = 30


class FileNotFoundException(Exception):
    pass


class StartStopQualifierValueException(Exception):
    """ Start Stop qualifier exception """
    pass


QUERY_TEMPLATE = {
    "feature_name": "ALL",
    "product": "SAEP",
    "query": "",
    "start_date": "",
    "end_date": ""
}


class QueryStringPatternTranslator:
    """
    translate stix pattern to native data source query language
    """

    def __init__(self, pattern: Pattern, data_model_mapper, options):

        logger.info("Symantec Endpoint Security Connector")
        self.dmm = data_model_mapper
        self.comparator_lookup = self.dmm.map_comparator()
        self.config_map = self.load_json(CONFIG_MAP_PATH)
        self.pattern = pattern
        self.options = options
        self.qualified_queries = []
        self.logged = False
        self.parse_expression(pattern)

    @staticmethod
    def load_json(rel_path_of_file) -> dict:
        """ Consumes a json file and returns a dictionary
        :param rel_path_of_file: (str) json file path
        :return: json: (dict) loaded json """
        _json_path = path.dirname(path.realpath(__file__)) + "/" + rel_path_of_file
        try:
            if path.exists(_json_path):
                with open(_json_path, encoding='utf-8') as f_obj:
                    return json.load(f_obj)
            raise FileNotFoundException
        except FileNotFoundException as e:
            raise FileNotFoundError(f'{rel_path_of_file} not found') from e

    def _format_set(self, comparator, values, mapped_field_type, expression, mapped_fields_array) -> str:
        """
        Formats value in the event of set operation
        :param comparator: (str) comparison operator
        :param values: (list) list of values
        :param mapped_field_type: (str) type of the field
        :param expression: (object) ANTLR parsed expression object
        :param mapped_fields_array: (list) list of mapped fields
        :return formatted value: (string) formatted value for the IN operator
        """
        gen = values.element_iterator()
        formatted_list = []
        for row in gen:
            row = self._check_value_comparator_support(row, expression.comparator, mapped_field_type,
                                                       mapped_fields_array)
            row = QueryStringPatternTranslator._escape_value(row)
            formatted_list.append(f'\"{row}\"')
        value = ' OR '.join(formatted_list)
        return f'{comparator.replace("value", value)}'

    @staticmethod
    def _format_like(comparator, value) -> str:
        """
        Formats value in the event of like operator
        :param comparator: (str) comparison operator
        :param value: (str) input value
        :return formatted value: (str) formatted value
        """
        # wildcard characters can be applied to single term as per lucene query syntax
        if ' ' in value:
            raise NotImplementedError(f'LIKE does not support on phrases, supports on single term.'
                                      f' {value} contains multiple terms')
        value = QueryStringPatternTranslator._escape_value(value)
        return f'{comparator.replace("value", value)}'

    @staticmethod
    def _format_match(comparator, value) -> str:
        """
        Formats value in the event of matches operator
        :param comparator: (str) comparison operator
        :param value: (str) input value
        :return formatted value: (str) formatted value
        """
        # Escape value as necessary first
        value = value.replace('\\', '\\\\').replace('/', '\\/')
        # Lucene regex anchors are not supported, remove ^ and $
        value = value[1:] if value.startswith('^') else value
        value = value[:-1] if value.endswith('$') else value

        return f'{comparator.replace("value", value)}'

    @staticmethod
    def _format_comparison(comparator, value) -> str:
        """
        Formats value in the event of comparison operators
        :param comparator: (str) comparison operator
        :param value: (str) input value
        :return formatted value: (str) formatted value
        """
        value = QueryStringPatternTranslator._escape_value(value)
        return f'{comparator.replace("value", str(value))}'

    @staticmethod
    def _format_equal(comparator, value, field_type) -> str:
        """
        Formats value in the event of equal operator
        :param comparator: (str) comparison operator
        :param value: (str) input value
        :param field_type: (str) operand type
        :return formatted value: (str) formatted value
        """
        value = QueryStringPatternTranslator._escape_value(value)
        return f'{comparator}{value}' if field_type == "date" else f'{comparator}\"{value}\"'

    @staticmethod
    def _escape_value(value):
        """
        adds escape characters to string type value
        :param value: (str) input value
        :return formatted value: (str) formatted value
        """
        if isinstance(value, str):
            value = value.replace('/', '\\/').replace('\\', '\\\\').replace('\"', '\\"').replace('(', '\\(').replace(')', '\\)').replace(':', '\\:')
            value = value.replace('-', '\\-')
        return value

    @staticmethod
    def _format_datetime(value) -> int:
        """
         Converts timestamp to epoch
        :param value: (str) UTC timestamp
        :return: converted_time: (str) UTC timestamp
        """
        try:
            time_pattern = '%Y-%m-%dT%H:%M:%S.%fZ'
            if re.search(r"\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}Z", str(value)):  # without milliseconds
                time_pattern = '%Y-%m-%dT%H:%M:%SZ'
            epoch = datetime(1970, 1, 1)
            converted_time = int(((datetime.strptime(value, time_pattern) - epoch).total_seconds()) * 1000)
            return converted_time
        except ValueError:
            raise NotImplementedError(f'cannot convert the timestamp {value} to milliseconds')

    @staticmethod
    def _parse_time_range(qualifier, time_range) -> list:
        """
        Converts qualifier timestamp to epoch
        :param qualifier: (str) UTC timestamp
        :param time_range: (int) time range in minutes
        return: converted_timestamp: (str) list of converted UTC timestamp values
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
            for index, timestamp in enumerate(time_range_list):
                time_range_list[index] = timestamp.replace('Z', '+00:00')
            return time_range_list
        except (KeyError, IndexError, TypeError) as e:
            raise e

    @staticmethod
    def _check_time_range_values(time_range):
        """
        checks for valid start time.
        :param time_range: list
        """
        start_date = datetime.strptime(time_range[0].replace('+00:00', 'Z'), '%Y-%m-%dT%H:%M:%S.%fZ')
        end_date = datetime.strptime(time_range[1].replace('+00:00', 'Z'), '%Y-%m-%dT%H:%M:%S.%fZ')

        if start_date > end_date:
            raise StartStopQualifierValueException(f"Start time should be lesser than Stop time")
        if end_date > datetime.utcnow():
            raise StartStopQualifierValueException(f"End time should be lesser than the current time")

        if start_date < (datetime.utcnow() - timedelta(days=SYMANTEC_EVENT_RETENTION_PERIOD)):
            raise StartStopQualifierValueException(f"Start date {start_date} is older than the event retention period of "
                                                   f"{SYMANTEC_EVENT_RETENTION_PERIOD} days")

    def _get_mapped_field_type(self, mapped_field_array) -> str:
        """
        Returns the type of mapped field array
        :param mapped_field_array: (list) list of mapped fields
        :return: mapped_field_type: (str) type of the field
        """
        mapped_field = mapped_field_array[0]
        mapped_field_type = "string"
        for key, value in self.config_map.items():
            if mapped_field in value and key in ["enum_supported_fields", "like_supported_fields",
                                                 "int_supported_fields", "bool_supported_fields",
                                                 "protocol_supported_fields", "date_supported_fields"]:
                mapped_field_type = key.split('_')[0]
                break
        return mapped_field_type

    @staticmethod
    def _convert_severity_value(value, supported_values):
        """
        Returns the type of mapped severity value from supported enum values
        :param value: (int) severity value
        :param supported_values: (list) supported list of severity enum values
        :return: value: matched severity enum value
        """
        if value == 0:
            return 0

        keys = supported_values.keys()
        int_list = [int(x) for x in keys]
        values = [num for num in int_list if num >= value]
        value = min(values)

        return value

    def _check_value_comparator_support(self, value, comparator, mapped_field_type, mapped_fields_array) -> str:
        """
        checks the comparator and value support.
        raise the error for unsupported fields and operators.
        :param value: (str) input value
        :param comparator: (object) comparison operator
        :param mapped_field_type: (str) type of field
        :param mapped_fields_array: (list) list of mapped fields
        :return value: (str) processed/formatted input value
        """

        if comparator in (ComparisonComparators.Like, ComparisonComparators.Matches) and mapped_field_type != "like":
            raise NotImplementedError(f'LIKE/MATCHES operator is not supported for this fields'
                                      f' {",".join(mapped_fields_array)}')

        if mapped_field_type == "enum":
            supported_values = self.config_map['enum_supported_values'].get(mapped_fields_array[0], [])
            enum_value = None
            if 'severity_id' in mapped_fields_array:
                if not str(value).isdigit():
                    raise NotImplementedError(f"String type input {value} is not supported for integer type field")
                if not 0 <= int(value) <= 100:
                    raise NotImplementedError("Severity allowed range from 0 to 100")
                value = self._convert_severity_value(int(value), supported_values)
                enum_value = str(value)
            value = supported_values.get(str(value))
            if not enum_value and not value:
                raise NotImplementedError(f'Unsupported ENUM values provided. {mapped_fields_array[0]} possible '
                                          f"supported enum values are '{','.join(supported_values)}'")

        if mapped_field_type == "protocol":
            supported_values = self.config_map['protocol_supported_values'].get(mapped_fields_array[0], [])
            value = supported_values.get(value)
            if not value:
                raise NotImplementedError(f'Unsupported protocol values provided. {mapped_fields_array[0]} possible '
                                          f"supported protocol values are '{','.join(supported_values)}'")

        if mapped_field_type == "date":
            value = self._format_datetime(value)
            value = f'[ {value} TO {value} ]'
            if not value:
                raise NotImplementedError(f'Unsupported date values provided for {mapped_fields_array[0]}')

        if mapped_field_type != "int":
            if comparator in [ComparisonComparators.GreaterThan, ComparisonComparators.GreaterThanOrEqual,
                              ComparisonComparators.LessThan, ComparisonComparators.LessThanOrEqual]:
                raise NotImplementedError('Comparison operators <, >, <=, >= only supports for integer type fields.')

        if mapped_field_type == "int":
            if not isinstance(value, int):
                raise NotImplementedError(f"String type input {value} is not supported for integer type field")

        if mapped_field_type == "bool":
            if value.lower() in ('true', 'false'):
                value = value.lower()
            else:
                raise NotImplementedError('Boolean field supported values are true/false')

        return value

    def _lookup_comparison_operator(self, expression_operator) -> str:
        """
        lookup operators support in symantec
        :param expression_operator: (object) contains comparison operator
        :return (str) comparator
        """
        if str(expression_operator) not in self.comparator_lookup:
            raise NotImplementedError(
                f'Comparison operator {expression_operator.name} unsupported for symantec connector')
        return self.comparator_lookup[str(expression_operator)]

    def _eval_comparison_value(self, expression, mapped_field_type, mapped_fields_array) -> str:
        """
        Function for parsing comparison expression value
        :param expression: (object) ANTLR parsed expression object
        :param mapped_field_type: (str) type of field
        :param mapped_fields_array: (list) list of mapped fields
        :return value: (str) processed/formatted input value
        """
        comparator = self._lookup_comparison_operator(expression.comparator)
        value = expression.value
        # validating value for all the operators other than IN operator.
        if expression.comparator != ComparisonComparators.In:
            value = self._check_value_comparator_support(value, expression.comparator, mapped_field_type,
                                                         mapped_fields_array)

        # formatting the value based on operators.
        if expression.comparator == ComparisonComparators.Like:
            value = self._format_like(comparator, value)
        elif expression.comparator == ComparisonComparators.Matches:
            value = self._format_match(comparator, value)
        elif expression.comparator == ComparisonComparators.In:
            value = self._format_set(comparator, value, mapped_field_type, expression, mapped_fields_array)
        elif expression.comparator in [ComparisonComparators.Equal, ComparisonComparators.NotEqual]:
            value = self._format_equal(comparator, value, mapped_field_type)
        elif expression.comparator in [ComparisonComparators.GreaterThan, ComparisonComparators.GreaterThanOrEqual,
                                       ComparisonComparators.LessThan, ComparisonComparators.LessThanOrEqual]:
            value = self._format_comparison(comparator, value)
        else:
            raise NotImplementedError('Unknown comparator expression operator')
        return value

    def _add_qualifier(self, query, qualifier) -> list:
        """
        Convert the qualifier into epoch time and append in the query.
        params: query: (list) list of queries
        params: qualifier: (str) start and stop UTC timestamp
        return: query: (list) list of queries attached with timestamp
        """
        time_range = QueryStringPatternTranslator._parse_time_range(qualifier, self.options['time_range'])
        QueryStringPatternTranslator._check_time_range_values(time_range)
        for row in query:
            row['start_date'] = time_range[0]
            row['end_date'] = time_range[1]
        return query

    @staticmethod
    def _parse_mapped_fields(formatted_value, mapped_fields_array, expression) -> list:
        """
        parse mapped fields into boolean expression
        :param formatted_value: (str) input value
        :param mapped_fields_array: (list) list of mapped fields
        :param expression: (object) ANTLR parsed expression object
        :return: (list) formatted query
        """
        comparison_list = []
        comparison_string_new = ''
        query = copy.deepcopy(QUERY_TEMPLATE)
        for index, field_name in enumerate(mapped_fields_array):
            if index > 0:
                comparison_string_new += ' OR '
            if expression.negated or expression.comparator == ComparisonComparators.NotEqual:
                comparison_string = f'-{field_name}{formatted_value}'
            else:
                comparison_string = f'{field_name}{formatted_value}'
            comparison_string_new += comparison_string
        query['query'] = comparison_string_new
        comparison_list.append(query)
        return comparison_list

    @staticmethod
    def check_common_timestamp(query_01, query_02):
        """
        Check the queries contains same timestamp
        :param query_01: (dict) first query
        :param query_02: (dict) second query
        :return True or None
        """
        if query_01['start_date'] == query_02['start_date'] and query_01['end_date'] == query_02['end_date']:
            return True
        return None

    def combine_queries(self, expression_01, expression_02, operator) -> list:
        """
        Combine the queries using OR, AND operator.
        ex: A , B are two queries.
            If A OR B having same timestamp it will combine the queries [A OR B] or [A AND B]
            otherwise it will be a separate queries [ A , B ]
        :param expression_01: (list) first query
        :param expression_02: (list) second query
        :param operator: (str) operator
        :return query: (list) list of combined queries
        """
        query_list = []

        if len(expression_02) == 1:
            expression_01, expression_02 = expression_02, expression_01

        for row_01 in expression_01:
            for row_02 in expression_02:
                common_timestamp = self.check_common_timestamp(row_01, row_02)
                if common_timestamp:
                    combined_query = f'({row_01["query"]}) {operator} ({row_02["query"]})'
                    row_01['query'] = combined_query
                    query_list.append(row_01)
                else:
                    query_list.append(row_02)
                    if row_01 not in query_list:
                        query_list.append(row_01)
        return query_list

    def _eval_combined_comparison_exp(self, expression) -> list:
        """
        Function for parsing combined comparison expression
        :param expression: (object) ANTLR parsed expression object
        """
        query = []
        operator = self._lookup_comparison_operator(expression.operator)
        expression_01 = self._parse_expression(expression.expr1)
        expression_02 = self._parse_expression(expression.expr2)

        if not expression_01 or not expression_02:
            return query

        if expression.operator == ComparisonExpressionOperators.Or:
            query = self.combine_queries(expression_01, expression_02, operator)
        elif expression.operator == ComparisonExpressionOperators.And:
            query = self.combine_queries(expression_01, expression_02, operator)
        return query

    def _eval_combined_observation_exp(self, expression, qualifier=None) -> list:
        """
        Function for parsing combined observation expression
        :param expression: (object) ANTLR parsed expression object
        :param qualifier: (object) timestamp object
        """
        expression_01 = self._parse_expression(expression.expr1, qualifier)
        expression_02 = self._parse_expression(expression.expr2, qualifier)
        operator = self._lookup_comparison_operator(expression.operator)

        query = []
        if expression_01 and expression_02:
            query = self.combine_queries(expression_01, expression_02, operator)
        elif expression_01:
            query = expression_01
        elif expression_02:
            query = expression_02
        return query

    def _parse_expression(self, expression, qualifier=None) -> list:
        """
         Formation of symantec query from ANTLR parsing expression
        :param expression: expression object, ANTLR parsed expression object
        :param qualifier: str, default in None
        :return :None or list
        """
        if isinstance(expression, ComparisonExpression):  # Base Case
            stix_objects = expression.object_path.split(':')
            mapped_fields_array = self.dmm.map_field(stix_objects[0], stix_objects[1])
            mapped_field_type = self._get_mapped_field_type(mapped_fields_array)
            value = self._eval_comparison_value(expression, mapped_field_type, mapped_fields_array)
            query = self._parse_mapped_fields(value, mapped_fields_array, expression)
            return query

        elif isinstance(expression, CombinedComparisonExpression):
            return self._eval_combined_comparison_exp(expression)

        elif isinstance(expression, ObservationExpression):
            query = self._parse_expression(expression.comparison_expression)
            return self._add_qualifier(query, qualifier)

        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            if isinstance(expression.observation_expression, CombinedObservationExpression):
                expression_01 = self._parse_expression(expression.observation_expression.expr1, expression.qualifier)
                expression_02 = self._parse_expression(expression.observation_expression.expr2, expression.qualifier)
                query = []
                if expression_01 and expression_02:
                    operator = self._lookup_comparison_operator(expression.observation_expression.operator)
                    query = self.combine_queries(expression_01, expression_02, operator)
            else:
                query = self._parse_expression(expression.observation_expression, expression.qualifier)
            if qualifier is not None:
                query = self._add_qualifier(query, qualifier)
            return query

        elif isinstance(expression, CombinedObservationExpression):
            return self._eval_combined_observation_exp(expression, qualifier)
        elif isinstance(expression, Pattern):
            return self._parse_expression(expression.expression)
        else:
            raise RuntimeError(f'Unknown Recursion Case for expression={expression}, '
                               f'type(expression)={type(expression)}')

    def parse_expression(self, pattern: Pattern):
        """
         Formation of symantec query from ANTLR parsing expression.
        :param pattern: expression object, ANTLR parsed expression object
        """
        query_list = self._parse_expression(pattern)
        self.qualified_queries = query_list


def translate_pattern(pattern: Pattern, data_model_mapping, options) -> list:
    """
    Conversion of ANTLR pattern to symantec query
    :param pattern: expression object, ANTLR parsed expression object
    :param data_model_mapping: DataMapper object, mapping object obtained by parsing json
    :param options: dict, time_range defaults to 5
    :return: list, symantec queries
    """
    translated_query_strings = QueryStringPatternTranslator(pattern, data_model_mapping, options)
    queries = translated_query_strings.qualified_queries
    return queries
