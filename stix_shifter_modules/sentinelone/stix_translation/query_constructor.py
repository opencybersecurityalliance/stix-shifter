import re
import json
import logging
from os import path
from datetime import datetime, timedelta
from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import \
    ObservationExpression, ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators


START_STOP_PATTERN = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z)"

logger = logging.getLogger(__name__)
TYPE_MAP_PATH = "json/type_map.json"


class QueryStringPatternTranslator:
    """
       translate stix pattern to native data source query language
    """

    def __init__(self, pattern: Pattern, data_model_mapper, options):
        self.dmm = data_model_mapper
        self.comparator_lookup = self.dmm.map_comparator()
        self.pattern = pattern
        self.options = options
        self.timeframe = []
        self.type_map = self.load_json(TYPE_MAP_PATH)
        self.translated = self.parse_expression(pattern)

    @staticmethod
    def load_json(rel_path_of_file):
        """
        Consumes a json file and returns a dictionary
        :param rel_path_of_file: str
        :return: dict
        """
        _json_path = path.dirname(path.realpath(__file__)) + "/" + rel_path_of_file
        if path.exists(_json_path):
            with open(_json_path, encoding='utf-8') as f_obj:
                return json.load(f_obj)
        raise FileNotFoundError

    @staticmethod
    def _check_boolean_value(final_value):
        """
        returns boolean value of input
        :param final_value:str
        :return bool
        """
        if final_value.lower() == "true" or (final_value.isdigit() and final_value == "1"):
            boolean_value = bool(True)
        elif final_value.lower() == "false" or (final_value.isdigit() and final_value == "0"):
            boolean_value = bool(False)
        else:
            raise NotImplementedError('Invalid boolean type input')
        return boolean_value

    def _check_field_value_support(self, filter_name, value):
        """
        check input value format that matches with the field supported values
        """
        final_value = str(value)
        if filter_name in self.type_map["enum_supported_fields"]:
            if final_value.upper() not in [x.upper() for x in self.type_map["enum_supported_values"][filter_name]]:
                raise NotImplementedError(f'Unsupported ENUM values provided. Possible supported enum values are'
                                          f'{self.type_map["enum_supported_values"][filter_name]}')
            final_value = final_value.upper()
        if filter_name in self.type_map["int_supported_fields"]:
            if not final_value.isdigit():
                raise NotImplementedError(f'string type input - {value} is not supported for int field - {filter_name}')
            final_value = str(value)
        elif filter_name in self.type_map["boolean_supported_fields"]:
            final_value = QueryStringPatternTranslator._check_boolean_value(final_value)
        return final_value

    def _check_value_comparator_support(self, exp_comparator, filter_name):
        """
        check operator format that matches with the field supported values
        """
        filter_type = str(exp_comparator).split(".")[1]
        if filter_name in ["fileFullName"] and filter_type in \
                ["LessThan", "LessThanOrEqual", "GreaterThan", "GreaterThanOrEqual"]:
            raise NotImplementedError(f'{filter_type}'
                                      f' operator is not supported for File Name, Use LIKE or MATCHES operator only')
        if filter_name in self.type_map["string_supported_fields"] and filter_type in\
                ["LessThan", "LessThanOrEqual", "GreaterThan", "GreaterThanOrEqual"]:
            raise NotImplementedError(f'"{filter_type}" operator is not supported for string type input')
        if filter_name in self.type_map["enum_supported_fields"] and filter_type not in ["NotEqual", "Equal"]:
            raise NotImplementedError(f'"{filter_type}" operator is not supported for enum type input')
        if filter_name in self.type_map["timestamp_supported_fields"] and filter_type not in \
                ["LessThan", "LessThanOrEqual", "GreaterThan", "GreaterThanOrEqual"]:
            raise NotImplementedError(f'"{filter_type}" operator is not supported for timestamp type input')

    def _format_set(self, values, filter_name) -> str:
        """
        Formats value in the event of set operation
        :param values
        :return formatted value
        """
        if filter_name in ["fileFullName"]:
            raise NotImplementedError(f'IN operator is not supported for File Name, Use LIKE or MATCHES operator only')
        if filter_name in self.type_map["boolean_supported_fields"]:
            raise NotImplementedError("IN operator is not supported for Boolean fields")
        if filter_name in self.type_map["timestamp_supported_fields"]:
            raise NotImplementedError("IN operator is not supported for Timestamp fields")
        gen = values.element_iterator()

        if filter_name in self.type_map["enum_supported_fields"]:
            val_gen = values.element_iterator()
            for final_value in val_gen:
                if final_value.upper() not in [x.upper() for x in self.type_map["enum_supported_values"][filter_name]]:
                    raise NotImplementedError(f'Unsupported ENUM values provided. Possible supported enum values are'
                                              f'{self.type_map["enum_supported_values"][filter_name]}')
            formatted_value = ','.join([QueryStringPatternTranslator._escape_value(value.upper())
                                        for value in gen])
        else:
            formatted_value = ','.join([QueryStringPatternTranslator._escape_value(value)
                                    for value in gen])
        return f'({formatted_value})'

    def _format_match(self, value, filter_name) -> str:
        """
        Formats value in the event of match operation
        :param value
        :return formatted string type value
        """
        if filter_name not in self.type_map["string_supported_fields"]:
            raise NotImplementedError("only String fields are supported in MATCH operator")
        raw = QueryStringPatternTranslator._escape_value(value)
        return f'{raw}'

    def _format_equality(self, value, filter_name) -> str:
        """
        Formats value in the event of equality operation
        :param value
        :return formatted value
        """
        value = self._check_field_value_support(filter_name, value)
        value_escaped = QueryStringPatternTranslator._escape_value(value)
        return f'{value_escaped}'

    def _format_like(self, value, filter_name) -> str:
        """
        Formats value in the LIKE of equality operation
        :param value
        :return formatted value
        """
        if filter_name not in self.type_map["string_supported_fields"]:
            raise NotImplementedError("only String fields are supported in LIKE operator")
        wildcard = ['%', '$', '+', '*', '^', '?']
        for val in wildcard:
            if val in value:
                logger.error("Wildcard characters is not supported in sentinelone LIKE operator")
                value = re.sub(r'[?|$|%|+|*|^]', '', value)
        return f'("{value}")'

    @staticmethod
    def _escape_value(value) -> str:
        """
        adds escape characters to string type value
        """
        if isinstance(value, str):
            value = f'\"{value}\"'
        return value

    @staticmethod
    def _negate_comparison(comparator):
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
            "in contains anycase": "in contains anycase",
            "IN": "NOT IN",
            "~=": "!~=",
            "regexp": "regexp"
        }
        return negate_comparator[comparator]

    @staticmethod
    def _parse_time_range(qualifier, time_range):
        """
        :param qualifier: str, input time range i.e START t'2019-04-10T08:43:10.003Z'
         STOP t'2019-04-20T10:43:10.003Z'
        :param time_range: int, value available from main.py in options variable
        :return: str, format_string bound with time range provided
        """
        try:
            compile_timestamp_regex = re.compile(START_STOP_PATTERN)
            if qualifier and compile_timestamp_regex.search(qualifier):
                time_range_iterator = compile_timestamp_regex.finditer(qualifier)
                time_range_list = [each.group() for each in time_range_iterator]
            # Default time range Start time = Now - 5 minutes and Stop time = Now
            else:
                stop_time = datetime.utcnow()
                start_time = stop_time - timedelta(minutes=time_range)
                converted_starttime = start_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                converted_stoptime = stop_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                time_range_list = [converted_starttime, converted_stoptime]

        except (KeyError, IndexError, TypeError) as e:
            raise e
        return time_range_list

    def _add_timestamp_to_query(self, query, qualifier):
        """
        adds timestamp to S1QL
        :param query: str
        :param qualifier
        :return str
        """
        converted_timestamp = \
            QueryStringPatternTranslator._parse_time_range(qualifier, self.options["time_range"])
        self.timeframe += converted_timestamp
        query = f'{query} AND EventTime  BETWEEN "{converted_timestamp[0]}"' \
                f' AND "{converted_timestamp[1]}"'
        formatted_query = {"query": query, "fromDate": converted_timestamp[0],
                           "toDate": converted_timestamp[1], "limit": self.options["result_limit"]}
        json_data = json.dumps(formatted_query)
        return json_data

    def _parse_mapped_fields(self, value, comparator, mapped_fields_array,expression):
        """
        parse mapped fields into boolean expression
        :param value: str
        :param comparator: str
        :param mapped_fields_array: list
        :return: str
        """
        comparison_string = ""
        mapped_fields_count = len(mapped_fields_array)
        for mapped_field in mapped_fields_array:
            if expression.negated and str(expression.comparator).split(".")[1] in ['Matches','Like']:
                comparison_string += f'NOT {mapped_field} {comparator} {value}'
            elif mapped_field in self.type_map["boolean_supported_fields"]:
                comparison_string += f'{mapped_field} is {value.lower()}'
            else:
                comparison_string += f'{mapped_field} {comparator} {value}'
            if mapped_fields_count > 1:
                comparison_string += " OR "
                mapped_fields_count -= 1
        return comparison_string

    def _lookup_comparison_operator(self, expression_operator):
        """
        lookup operators support in SentinelOne
        :param expression_operator:enum object
        :return str
        """
        if str(expression_operator) not in self.comparator_lookup:
            raise NotImplementedError(f'Comparison operator {expression_operator.name} '
                                      f'unsupported for SentinelOne connector')
        return self.comparator_lookup[str(expression_operator)]

    def _parse_expression(self, expression, qualifier=None) -> str:
        """
        parse ANTLR pattern to S1QL
        :param expression: expression object, ANTLR parsed expression object
        :param qualifier: str, default in None
        :return str
        """
        if isinstance(expression, ComparisonExpression):  # Base Case
            stix_object, stix_field = expression.object_path.split(':')
            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
            filter_name = mapped_fields_array[0]
            # Converting Equal operator to Like operator for field fileFullName,
            # since it contains full path of file
            if filter_name in ["fileFullName"]:
                if expression.comparator == ComparisonComparators.Equal:
                    expression.comparator = ComparisonComparators.Like
                elif expression.comparator == ComparisonComparators.NotEqual:
                    expression.comparator = ComparisonComparators.Like
                    expression.negated = True

            comparator = self._lookup_comparison_operator(expression.comparator)
            if expression.negated:
                comparator = self._negate_comparison(comparator)

            # Some values are formatted differently based on how they're being compared
            if expression.comparator == ComparisonComparators.Matches:  # needs forward slashes
                value = self._format_match(expression.value, filter_name)
            # should be (x, y, z, ...)
            elif expression.comparator == ComparisonComparators.In:
                value = self._format_set(expression.value, filter_name)
            elif expression.comparator in [ComparisonComparators.GreaterThan, ComparisonComparators.GreaterThanOrEqual,
                                           ComparisonComparators.LessThan,
                                           ComparisonComparators.LessThanOrEqual, ComparisonComparators.Equal,
                                           ComparisonComparators.NotEqual]:

                self._check_value_comparator_support(expression.comparator, filter_name)
                # Should be in double-quotes
                value = self._format_equality(expression.value, filter_name)

            elif expression.comparator == ComparisonComparators.Like:
                value = self._format_like(expression.value, filter_name)
            else:
                value = self._escape_value(expression.value)
            comparison_string = \
                self._parse_mapped_fields(value, comparator, mapped_fields_array, expression)
            if len(mapped_fields_array) > 1:
                grouped_comparison_string = "(" + comparison_string + ")"
                comparison_string = grouped_comparison_string

            if qualifier is not None:
                query_string = self._add_timestamp_to_query(comparison_string, qualifier)
            else:
                query_string = comparison_string
            return query_string

        elif isinstance(expression, CombinedComparisonExpression):
            operator = self._lookup_comparison_operator(expression.operator)
            expression_01 = self._parse_expression(expression.expr1)
            expression_02 = self._parse_expression(expression.expr2)
            if not expression_01 or not expression_02:
                return ''
            if isinstance(expression.expr1, CombinedComparisonExpression):
                expression_01 = f'{expression_01}'
            if isinstance(expression.expr2, CombinedComparisonExpression):
                expression_02 = f'{expression_02}'
            query_string = f'({expression_01} {operator} {expression_02})'
            if qualifier is not None:
                query_string = self._add_timestamp_to_query(query_string, qualifier)
            return f'{query_string}'

        elif isinstance(expression, ObservationExpression):
            query_string = self._parse_expression(expression.comparison_expression)
            query_string = self._add_timestamp_to_query(query_string, qualifier)
            return query_string

        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            if isinstance(expression.observation_expression, CombinedObservationExpression):
                operator = \
                    self._lookup_comparison_operator(expression.observation_expression.operator)
                expression_01 = self._parse_expression(expression.observation_expression.expr1,
                                                       expression.qualifier)
                expression_02 = self._parse_expression(expression.observation_expression.expr2,
                                                       expression.qualifier)
                query_string = \
                    f'{expression_01} {operator} {expression_02}'
            else:
                query_string = self._parse_expression(expression.observation_expression.comparison_expression,
                                                      expression.qualifier)

            if qualifier is not None:
                query_string = self._add_timestamp_to_query(query_string, qualifier)
            return query_string

        elif isinstance(expression, CombinedObservationExpression):
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
        elif isinstance(expression, Pattern):
            return f'{self._parse_expression(expression.expression)}'
        else:
            raise RuntimeError(f'Unknown Recursion Case for expression={expression},'
                               f' type(expression)={type(expression)}')

    def parse_expression(self, pattern: Pattern):
        """
        Conversion of ANTLR pattern to S1QL query
        :param pattern: expression object, ANTLR parsed expression object
        :return: str, S1QL query
        """
        return self._parse_expression(pattern)


def merge_query(queries, timeframe, limit):
    """
    merge query for multiple observation
    :param queries: str
    :param timeframe : qualifier list of all observations
    :param limit: default 10000
    :return: str, merged query
    """
    query_set = []
    val = queries.split('} OR {')
    for i in val:
        i = re.search(r'query":[\s+]"(.+?)",[\s+]"fromDate"', i).group(1)
        query_set.append('(' + i + ')')
    final_query = ' OR '.join(query_set)
    final_query = final_query.replace('\\', '')
    formatted_query = {"query": final_query, "fromDate": min(timeframe), "toDate": max(timeframe),
                       "limit": limit}
    return json.dumps(formatted_query)


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    """
    Conversion of ANTLR pattern to S1QL query
    :param pattern: expression object, ANTLR parsed expression object
    :param data_model_mapping: DataMapper object, mapping object obtained by parsing json
    :param options: dict, time_range defaults to 5
    :return: str, S1QL query
    """
    translated_query_strings = QueryStringPatternTranslator(pattern, data_model_mapping, options)
    limit = options['result_limit']
    queries = translated_query_strings.translated
    timeframe = translated_query_strings.timeframe
    match = re.search(r'}\ OR \{"', queries)
    if match:
        final_queries = merge_query(queries, timeframe, limit)
    else:
        final_queries = queries
    return final_queries
