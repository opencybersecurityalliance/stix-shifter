import copy
import json
import re
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


class FileNotFoundException(Exception):
    pass


class QueryStringPatternTranslator:
    """
    comparator values to match with supported data source operators
    """

    def __init__(self, pattern: Pattern, data_model_mapper, options):

        logger.info("Cisco Secure Email Connector")
        self.dmm = data_model_mapper
        self.comparator_lookup = self.dmm.map_comparator()
        self.config_map = self.load_json(CONFIG_MAP_PATH)
        self.pattern = pattern
        self.options = options
        self.qualified_queries = []
        self.parse_expression(pattern)

    @staticmethod
    def load_json(rel_path_of_file):
        """ Consumes a json file and returns a dictionary
        :param rel_path_of_file: str
        :return: dict """
        _json_path = path.dirname(path.realpath(__file__)) + "/" + rel_path_of_file
        try:
            if path.exists(_json_path):
                with open(_json_path, encoding='utf-8') as f_obj:
                    return json.load(f_obj)
            raise FileNotFoundException
        except FileNotFoundException as e:
            raise FileNotFoundError(f'{rel_path_of_file} not found') from e

    def _format_set(self, values, mapped_field_type, expression, mapped_fields_array) -> str:
        """
        Formats value in the event of set operation
        :param values: list
        :param mapped_field_type: str
        :param expression: object
        :param mapped_fields_array: object
        :return formatted value
        """
        gen = values.element_iterator()
        formatted_list = []
        for value in gen:
            value = self._check_value_comparator_support(value, expression.comparator, mapped_field_type,
                                                         mapped_fields_array)
            formatted_list.append(value)
        formatted_values = ','.join(formatted_list)
        return formatted_values

    @staticmethod
    def _format_equality(value) -> str:
        """
        Formats value in the event of equality operation
        :param value
        :return formatted value
        """
        return str(value)

    @staticmethod
    def _format_like(value) -> str:
        """
        Formatting value in the event of like operation
        :param value
        :return: list
        """
        return str(value)

    @staticmethod
    def _format_datetime(value) -> str:
        """
         format the date
        :param: value: str
        :return: converted_time: str
        """
        try:
            time_pattern = '%Y-%m-%dT%H:%M:%S.%fZ'
            if re.search(r"\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}Z", str(value)):  # without milli seconds
                time_pattern = '%Y-%m-%dT%H:%M:%SZ'
            converted_time = datetime.strptime(value, time_pattern).strftime('%Y-%m-%dT%H:%M:00.000Z')
            return converted_time
        except ValueError:
            pass
        raise NotImplementedError(f'cannot format the timestamp {value}')

    @staticmethod
    def _parse_time_range(qualifier, time_range):
        """
        Converts qualifier to timestamp format
        :param qualifier: str
        :param time_range: int
        return: list of formatted timestamps
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
            for index, value in enumerate(time_range_list):
                time_range_list[index] = QueryStringPatternTranslator._format_datetime(value)
            return time_range_list
        except (KeyError, IndexError, TypeError) as e:
            raise e

    def _get_mapped_field_type(self, mapped_field_array) -> str:
        """
        Returns the type of mapped field array
        :param mapped_field_array: list
        :return: str
        """
        mapped_field = mapped_field_array[0]
        mapped_field_type = "string"
        for key, value in self.config_map.items():
            if mapped_field in value and key in ["like_supported_fields", "bool_supported_fields",
                                                 "int_supported_fields", "enum_supported_fields"]:
                mapped_field_type = key.split('_')[0]
                break
        return mapped_field_type

    def _check_value_comparator_support(self, value, comparator, mapped_field_type, mapped_fields_array) -> str:
        """
        checks the comparator and value support
        :param value
        :param comparator
        :param mapped_field_type: str
        :param mapped_fields_array: list
        :return value: str
        """
        if mapped_field_type == "int" and not str(value).replace('-', '').isdigit():
            raise NotImplementedError(f"String type input {value} is not supported for integer type field")

        if mapped_field_type == "enum":
            supported_values = self.config_map['enum_supported_values'].get(mapped_fields_array[0], [])
            if value not in supported_values:
                raise NotImplementedError(f'Unsupported ENUM values provided. {mapped_fields_array[0]} possible '
                                          f"supported enum values are '{','.join(supported_values)}'")

        if mapped_field_type == "bool":
            if comparator != ComparisonComparators.Equal:
                raise NotImplementedError('Boolean fields supports only for Equal operator')
            if value.lower() == 'true':
                value = True
            else:
                raise NotImplementedError('Boolean field supported value is only True')

        if comparator == ComparisonComparators.In and \
                mapped_fields_array[0] not in self.config_map['in_supported_fields']:
            raise NotImplementedError("IN operator is not supported for this field")

        if comparator == ComparisonComparators.Like and mapped_field_type != "like":
            raise NotImplementedError("LIKE operator is not supported for this field")

        return value

    def _lookup_comparison_operator(self, expression_operator) -> str:
        """
        lookup operators support in cisco secure email
        :param expression_operator:object
        :return str
        """
        if str(expression_operator) not in self.comparator_lookup:
            raise NotImplementedError(
                f'Comparison operator {expression_operator.name} unsupported for cisco secure email connector')

        return self.comparator_lookup[str(expression_operator)]

    def _eval_comparison_value(self, expression, mapped_field_type, mapped_fields_array) -> str:
        """
        Function for parsing comparison expression value
        :param expression: expression object
        :param mapped_field_type: str
        :param mapped_fields_array: list object
        :return: formatted expression value
        """
        if expression.negated or expression.comparator == ComparisonComparators.NotEqual:
            raise NotImplementedError('Not operator is unsupported for cisco secure email')

        if expression.comparator == ComparisonComparators.Like:
            value = self._check_value_comparator_support(expression.value, expression.comparator, mapped_field_type,
                                                         mapped_fields_array)
            value = self._format_like(value)
        elif expression.comparator == ComparisonComparators.In:
            value = self._format_set(expression.value, mapped_field_type, expression, mapped_fields_array)
        elif expression.comparator == ComparisonComparators.Equal:
            value = self._check_value_comparator_support(expression.value, expression.comparator, mapped_field_type,
                                                         mapped_fields_array)
            value = self._format_equality(value)
        else:
            raise NotImplementedError('Unknown comparator expression operator')
        return value

    def _add_qualifier(self, query, qualifier) -> list:
        """
        Convert the qualifier into epoch time and append in the query.
        params: query : list
        params: qualifier
        return: query : list
        """
        query_qualifier = []
        time_range = QueryStringPatternTranslator._parse_time_range(qualifier, self.options['time_range'])
        for row in query:
            query_qualifier.append(f"{row}&startDate={time_range[0]}&endDate={time_range[1]}")
        return query_qualifier

    def _parse_mapped_fields(self, formatted_value, mapped_fields_array, mapped_field_type, expression) -> list:
        """
        parse mapped fields into boolean expression
        :param formatted_value: str
        :param mapped_fields_array: list
        :param mapped_field_type:str
        :param expression: expression object
        :return: list
        """
        comparator = self._lookup_comparison_operator(expression.comparator)
        comparison_list = []
        for field_name in mapped_fields_array:
            if expression.comparator == ComparisonComparators.Like:
                comparison_string_new = f'{field_name.replace("Value", "Operator")}{comparator}contains&' \
                                        f'{field_name}{comparator}{formatted_value}'
            elif expression.comparator == ComparisonComparators.Equal and mapped_field_type == 'like':
                comparison_string_new = f'{field_name.replace("Value", "Operator")}{comparator}is&' \
                                        f'{field_name}{comparator}{formatted_value}'
            else:
                comparison_string_new = f'{field_name}{comparator}{formatted_value}'
            comparison_list.append(comparison_string_new)
        return comparison_list

    def combine_or_queries(self, expression_01, expression_02) -> list:
        """
        combine the queries using or operator
        :param expression_01: expression object
        :param expression_02: expression object
        :return query list
        """
        query_list = []
        if len(expression_01) == 1 and len(expression_02) == 1:
            field_01, field_02 = None, None
            if len(expression_01[0].split('=')) == 2 or len(expression_02[0].split('=')) == 2:
                field_01 = expression_01[0].split('=')[0]
                field_02 = expression_02[0].split('=')[0]
                if field_01 in self.config_map['or_supported_values'] and \
                        field_02 in self.config_map['or_supported_values']:
                    query_list.append(expression_01[0] + '&' + expression_02[0])
                # combining same date queries
            elif 'startDate' in expression_01[0] and 'startDate' in expression_02[0]:
                splitted_query_01 = expression_01[0].split('&startDate')
                splitted_query_02 = expression_02[0].split('&startDate')
                if splitted_query_01[-1] == splitted_query_02[-1]:
                    field_01 = splitted_query_01[0].split('=')[0]
                    field_02 = splitted_query_02[0].split('=')[0]
                if field_01 in self.config_map['or_supported_values'] and \
                        field_02 in self.config_map['or_supported_values']:
                    query_list.append(expression_01[0] + '&' +
                                      expression_02[0].replace('&startDate'+splitted_query_02[-1], ''))

        # for or operator [query1 , query2]
        if not query_list:
            query_list = expression_01 + expression_02

        return query_list

    def combine_and_queries(self, expression_01, expression_02, operator) -> list:
        """
        combine the queries using and operator
        :param expression_01: expression object
        :param expression_02: expression object
        :param operator: string
        :return query list
        """
        query_list = []

        if len(expression_01) == 1 and len(expression_02) == 1:
            if len(expression_01[0].split('=')) == 2 or len(expression_02[0].split('=')) == 2:
                field_01 = expression_01[0].split('=')[0]
                field_02 = expression_02[0].split('=')[0]
                if field_01 in self.config_map['or_supported_values'] and \
                        field_02 in self.config_map['or_supported_values']:
                    if not (field_01 in self.config_map['grouped_fields'].keys() and
                            field_02 in self.config_map['grouped_fields'].keys()):
                        raise NotImplementedError(f"AND operator is not supported for {field_01, field_02}"
                                                  f" message event fields")

        # for and operator [query1&query2]
        for row_01 in expression_01:
            for row_02 in expression_02:
                query_list.append(f'{row_01}{operator}{row_02}')

        return query_list

    def _eval_combined_comparison_exp(self, expression) -> str:
        """
        Function for parsing combined comparison expression
        :param expression: expression object
        """
        query = []
        operator = self._lookup_comparison_operator(expression.operator)
        expression_01 = self._parse_expression(expression.expr1)
        expression_02 = self._parse_expression(expression.expr2)

        if not expression_01 or not expression_02:
            return query

        if expression.operator == ComparisonExpressionOperators.Or:
            query = self.combine_or_queries(expression_01, expression_02)
        elif expression.operator == ComparisonExpressionOperators.And:
            query = self.combine_and_queries(expression_01, expression_02, operator)
        return query

    def _eval_combined_observation_exp(self, expression, qualifier=None) -> str:
        """
        Function for parsing combined observation expression
        :param expression: expression object
        :param qualifier: qualifier
        """
        expression_01 = self._parse_expression(expression.expr1, qualifier)
        expression_02 = self._parse_expression(expression.expr2, qualifier)
        query = []
        if expression_01 and expression_02:
            query = self.combine_or_queries(expression_01, expression_02)
        elif expression_01:
            query = expression_01
        elif expression_02:
            query = expression_02
        return query

    def _parse_expression(self, expression, qualifier=None) -> list:
        """
         Formation of cisco secure email query from ANTLR parsing expression
        :param expression: expression object, ANTLR parsed expression object
        :param qualifier: str, default in None
        :return :None or list
        """
        if isinstance(expression, ComparisonExpression):  # Base Case
            stix_objects = expression.object_path.split(':')
            mapped_fields_array = self.dmm.map_field(stix_objects[0], stix_objects[1])
            mapped_field_type = self._get_mapped_field_type(mapped_fields_array)
            value = self._eval_comparison_value(expression, mapped_field_type, mapped_fields_array)
            query = self._parse_mapped_fields(value, mapped_fields_array, mapped_field_type, expression)
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
                    query = self.combine_or_queries(expression_01, expression_02)
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

    def combine_in_supported_queries(self, query_list) -> list:
        """
        Combine IN supported fields
        params: query: list
        return: query list
        """
        copy_query_list = copy.deepcopy(query_list)
        for query in copy_query_list:
            for in_field in self.config_map['in_supported_fields']:
                in_field += '='
                if query.count(in_field) > 1:
                    split_query = query.split('&')
                    copy_split_query = copy.deepcopy(split_query)
                    values = []
                    for row in split_query:
                        if in_field in row:
                            values.append(row.replace(in_field, ''))
                            copy_split_query.remove(row)
                    if values:
                        copy_split_query.append(in_field + ','.join(values))
                        query_list.remove(query)
                        query_list.append('&'.join(copy_split_query))
        return query_list

    @staticmethod
    def validate_repeated_fields(query_list) -> list:
        """
        Validate repeated fields in query
        :param query_list: query list
        """
        for row in query_list:
            split_queries = row.split('&')
            for statement in split_queries:
                # get the field name
                if '=' in statement:
                    field = statement.split('=')[0]
                    # duplicate fields cannot be allowed
                    if row.count(field + '=') > 1:
                        raise NotImplementedError(f"{field} cannot be allowed more than once in query")
                else:
                    continue
        return query_list

    def validate_dependant_fields(self, query):
        """
        Validate any dependant fields are required
        params: query : list
        """
        for row in query:
            for key, values in self.config_map['grouped_fields'].items():
                if key in row and [value for value in values if value + '=' not in row]:
                    raise NotImplementedError(f'Add dependant {",".join(values)} fields in pattern')

    def parse_expression(self, pattern: Pattern) -> list:
        """
         Formation of cisco secure email query from ANTLR parsing expression.
        :param pattern: expression object, ANTLR parsed expression object
        """
        query_list = self._parse_expression(pattern)
        query_list = self.combine_in_supported_queries(query_list)
        self.validate_repeated_fields(query_list)
        self.validate_dependant_fields(query_list)

        self.qualified_queries = query_list


def translate_pattern(pattern: Pattern, data_model_mapping, options) -> list:
    """
    Conversion of ANTLR pattern to cisco secure email query
    :param pattern: expression object, ANTLR parsed expression object
    :param data_model_mapping: DataMapper object, mapping object obtained by parsing json
    :param options: dict, time_range defaults to 5
    :return: list, cisco secure email queries
    """
    translated_query_strings = QueryStringPatternTranslator(pattern, data_model_mapping, options)
    queries = translated_query_strings.qualified_queries
    return queries
