""" This Module will convert Stix Pattern to Sysdig data source supported query """
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
MAC = '^(([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2}))$'
TYPE_MAP_PATH = "json/config_map.json"

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
        logger.info("Sysdig Connector")
        self.dmm = data_model_mapper
        self.options = options
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
        _json_path = path.dirname(path.realpath(__file__)) + "/" + rel_path_of_file
        try:
            if path.exists(_json_path):
                with open(_json_path, encoding='utf-8') as f_obj:
                    return json.load(f_obj)
            raise FileNotFoundException
        except FileNotFoundException as ex:
            raise FileNotFoundError(f'{rel_path_of_file} not found') from ex

    def _format_set(self, values, mapped_field_type):
        """
        Formats value in the event of set operation
        :param values
        :param mapped_field_type: str
        :return formatted value
        """
        gen = values.element_iterator()
        formatted_value = ','.join(QueryStringPatternTranslator._escape_value(
            self._format_value_type(value, mapped_field_type), mapped_field_type)
                                   for value in gen)
        return f'({formatted_value})'

    @staticmethod
    def _format_equality(value, mapped_field_type):
        """
        Formats value in the event of equality operation
        :param value
        :return formatted value
        """
        return QueryStringPatternTranslator._escape_value(value, mapped_field_type)

    @staticmethod
    def _escape_value(value, mapped_field_type):
        """
        adds escape characters to string type value
        :param value
        :return formatted value
        """
        if mapped_field_type == "int":
            return value
        if isinstance(value, str):
            value = f'\"{value}\"'
        return str(value)

    def _format_value_type(self, value, mapped_field_type):
        """
        check input value format that matches with the mapped field value type
        :param value
        :param mapped_field_type: str
        :return formatted value
        """
        converted_value = str(value)
        if mapped_field_type == "mac":
            compile_mac_regex = re.compile(MAC)
            if not compile_mac_regex.search(converted_value):
                raise NotImplementedError(f'Invalid mac address - {converted_value} provided')
        elif mapped_field_type == "int":
            if not converted_value.isdigit():
                raise NotImplementedError(f'string type input - {converted_value} is not supported for '
                                          f'integer type fields')
            converted_value = str(value)
        return converted_value

    def _check_value_comparator_support(self, comparator, mapped_field_type):
        """
        checks the comparator and value support
        :param comparator
        :param mapped_field_type: str
        """
        operator = self.comparator_lookup[str(comparator)]

        if mapped_field_type == 'string' and comparator not in [ComparisonComparators.In,
                                                                ComparisonComparators.Equal,
                                                                ComparisonComparators.NotEqual
                                                                ]:
            raise NotImplementedError(f'{operator} operator is not supported for string type input')
        if mapped_field_type == 'int' and comparator not in [ComparisonComparators.In,
                                                             ComparisonComparators.Equal,
                                                             ComparisonComparators.NotEqual,
                                                             ComparisonComparators.GreaterThan,
                                                             ComparisonComparators.GreaterThanOrEqual,
                                                             ComparisonComparators.LessThanOrEqual,
                                                             ComparisonComparators.LessThan]:
            raise NotImplementedError(f'{operator} operator is not supported for integer type input')

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
            "in": "not in"
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

    @staticmethod
    def get_epoch_time(timestamp):
        """
        Converting timestamp (YYYY-MM-DDThh:mm:ss.000Z) to 13-digit Unix time (epoch + milliseconds)
        :param timestamp: str, timestamp
        :return: int, epoch time
        """
        time_patterns = ['%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S.%fZ']
        epoch = datetime(1970, 1, 1)
        for time_pattern in time_patterns:
            try:
                converted_time = int(
                    ((datetime.strptime(timestamp, time_pattern) - epoch).total_seconds()) * 1000 * 1000000)
                return converted_time
            except ValueError:
                pass
        raise NotImplementedError("cannot convert the timestamp {} to epoch time".format(timestamp))

    def _add_timestamp_to_query(self, query, qualifier):
        """
        adds timestamp filter to Sysdig query
        :param query: str
        :param qualifier
        :return str
        """
        converted_timestamp = \
            QueryStringPatternTranslator._parse_time_range(qualifier, self.options["time_range"])
        QueryStringPatternTranslator._check_time_range_values(converted_timestamp)
        from_epoch = self.get_epoch_time(converted_timestamp[0])
        to_epoch = self.get_epoch_time(converted_timestamp[1])
        final_query = f'from={from_epoch}&to={to_epoch}&filter={query}'
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
                                                 "mac_supported_fields"]:
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
        mapped_fields_count = len(mapped_fields_array)
        for mapped_field in mapped_fields_array:
            if "in" in comparator:
                comparison_string += f'{mapped_field} {comparator} {value}'
            else:
                comparison_string += f'{mapped_field}{comparator}{value}'
            if mapped_fields_count > 1:
                comparison_string += " OR "
                mapped_fields_count -= 1
        return comparison_string

    def _lookup_comparison_operator(self, expression_operator):
        """
        lookup operators support in Sysdig connector
        :param expression_operator:enum object
        :return str
        """
        if str(expression_operator) not in self.comparator_lookup:
            raise NotImplementedError(
                f'Comparison operator {expression_operator.name} unsupported for Sysdig connector')
        operator = self.comparator_lookup[str(expression_operator)]
        return operator

    def _eval_comparison_value(self, expression, mapped_field_type):
        """
        Function for parsing comparison expression value
        :param expression: expression object
        :param mapped_field_type:str
        :return: formatted expression value
        """
        if expression.comparator == ComparisonComparators.In:
            value = self._format_set(expression.value, mapped_field_type)
        elif expression.comparator not in [ComparisonComparators.Like, ComparisonComparators.Matches]:
            value = self._format_value_type(expression.value, mapped_field_type)
            self._check_value_comparator_support(expression.comparator, mapped_field_type)
            value = self._format_equality(value, mapped_field_type)
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

    def _parse_expression(self, expression, qualifier=None):
        """
        parse ANTLR pattern to Sysdig native query
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
            value = self._eval_comparison_value(expression, mapped_field_type)

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
        Conversion of ANTLR pattern to Sysdig query
        :param pattern: expression object, ANTLR parsed expression object
        :return: str, native query
        """
        return self._parse_expression(pattern)

    @staticmethod
    def format_multiple_observations(query):
        """
        timestamp formatting for multiple observations
        """
        split_queries = query.split(' or ')
        query_dict = {}
        for row in split_queries:
            # making single time stamp instead of having multiple same time stamps for multiple queries
            split_query = row.split('filter=')
            query_timestamp = split_query[0]
            if query_dict.get(query_timestamp):
                query_dict[query_timestamp] += " or " + split_query[1]
            else:
                query_dict[query_timestamp] = 'filter=' + split_query[1]
        final_query = [key + value for key, value in query_dict.items()]
        return final_query

    @staticmethod
    def removing_audit_trail_logs(format_queries):
        """
        Displays error message when searched for auditTrail events.
        Adds the condition to filter auditTrail events for other queries.
        """
        query_list = []
        remove_audit = "andsource!=\"auditTrail\""
        if any('auditTrail' in query for query in format_queries):
            raise NotImplementedError('Sysdig connector does not provide auditTrail event')
        else:
            for query in format_queries:
                split_format_query = query.split('filter=')
                query_list.append(f'{split_format_query[0]}filter=({split_format_query[1]}){remove_audit}')
        return query_list


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    """
    Conversion of ANTLR pattern to native data source query
    :param pattern: expression object, ANTLR parsed expression object
    :param data_model_mapping: DataMapper object, mapping object obtained by parsing json
    :param options: dict, time_range defaults to 5
    :return: string, Sysdig  queries
    """
    translated_query_strings = QueryStringPatternTranslator(pattern, data_model_mapping, options)
    final_queries = translated_query_strings.translated_query

    if final_queries.count('from') > 1:
        final_queries = QueryStringPatternTranslator.format_multiple_observations(final_queries)
        return QueryStringPatternTranslator.removing_audit_trail_logs(final_queries)
    else:
        return QueryStringPatternTranslator.removing_audit_trail_logs([final_queries])
