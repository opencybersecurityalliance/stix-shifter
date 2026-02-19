import re
import json
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

# API query limit is 1350 (MAX_QUERY_LENGTH 1250 +TIMESTAMP_LENGTH 100)
MAX_QUERY_LENGTH = 1250


class FileNotFoundException(Exception):
    pass


class QueryStringPatternTranslator:
    """
    comparator values to match with supported data source operators
    """

    def __init__(self, pattern: Pattern, data_model_mapper, options):

        logger.info("Nozomi Vantage Connector")
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

    def _format_set(self, values, mapped_field_type, expression, mapped_fields_array) -> str:
        """
        Formats value in the event of set operation
        :param values: (list) list of values
        :param mapped_field_type: (str) type of the field
        :param expression: (object) ANTLR parsed expression object
        :param mapped_fields_array: (list) list of mapped fields
        :return formatted value: (string) formatted value for the IN operator
        """
        gen = values.element_iterator()
        formatted_list = []
        formatted_values = []
        result = []
        for value in gen:
            value = self._check_value_comparator_support(value, expression.comparator, mapped_field_type,
                                                         mapped_fields_array, expression)
            formatted_list.append(value)
        # combine the list values based on max query length
        for row in formatted_list:
            if len(str(formatted_values + [row]).replace("'", '\"')) > MAX_QUERY_LENGTH:
                result.append(str(formatted_values).replace("'", '\"'))
                formatted_values = []
            formatted_values.append(row)
        result.append(str(formatted_values).replace("'", '\"'))

        return result

    @staticmethod
    def _format_value(value) -> str:
        """
        Formats value in the event of equality, like, subset operation
        :param value: (str) input value
        :return formatted value: (str) formatted value for other than IN operator
        """
        return f'\"{value}\"'

    @staticmethod
    def _format_datetime(value) -> int:
        """
         Converts timestamp to epoch
        :param value: (str) UTC timestamp
        :return: converted_time: (int) epoch value
        """
        try:
            time_pattern = '%Y-%m-%dT%H:%M:%S.%fZ'
            if re.search(r"\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}Z", str(value)):  # without milli seconds
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
        return: converted_timestamp: (int) list of converted epoch values
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

    def _get_mapped_field_type(self, mapped_field_array) -> str:
        """
        Returns the type of mapped field array
        :param mapped_field_array: (list) list of mapped fields
        :return: mapped_field_type: (str) type of the field
        """
        mapped_field = mapped_field_array[0]
        mapped_field_type = "string"
        for key, value in self.config_map.items():
            if mapped_field in value and key in ["properties_supported_fields", "enum_supported_fields",
                                                 "int_supported_fields", "epoch_supported_fields",
                                                 "bytes_supported_fields", "subset_supported_fields"]:
                mapped_field_type = key.split('_')[0]
                break
        return mapped_field_type

    def _check_value_comparator_support(self, value, comparator, mapped_field_type, mapped_fields_array,
                                        expression) -> str:
        """
        checks the comparator and value support.
        raise the error for unsupported fields and operators.
        :param value: (str) input value
        :param comparator: (object) comparison operator
        :param mapped_field_type: (str) type of field
        :param mapped_fields_array: (list) list of mapped fields
        :param expression: (object) ANTLR parsed expression object
        :return value: (str) processed/formatted input value
        """
        if mapped_field_type == "int":
            if not str(value).isdigit():
                raise NotImplementedError(f"String type input {value} is not supported for integer type field")
            if 'risk' in mapped_fields_array:
                if not 0 <= int(value) <= 100:
                    raise NotImplementedError("Severity allowed range from 0 to 100")
                value = str(int(value) / 10)

        if mapped_field_type == "enum" and \
                'threat_name' in mapped_fields_array and expression.object_path == 'x-ibm-finding:finding_type':
            supported_values = self.config_map['enum_supported_values'].get(mapped_fields_array[0], [])
            if value not in supported_values:
                raise NotImplementedError(f'Unsupported ENUM values provided. {mapped_fields_array[0]} possible '
                                          f"supported enum values are '{', '.join(supported_values)}'")
            if comparator not in (ComparisonComparators.Equal, ComparisonComparators.NotEqual):
                raise NotImplementedError('threat_name fields supports only for Equal/Not Equal operator')

        if mapped_field_type == "properties" and \
                comparator not in (ComparisonComparators.Equal, ComparisonComparators.NotEqual,
                                   ComparisonComparators.Like):
            raise NotImplementedError('Properties field supports only for Equal/Not Equal/Like operator')

        if mapped_field_type == "epoch":
            value = self._format_datetime(value)

        if comparator == ComparisonComparators.IsSubSet and mapped_field_type != 'subset':
            raise NotImplementedError(f'ISSUBSET operator allows only subset supported fields '
                                      f'{self.config_map["subset_supported_fields"]}')

        if expression.negated and comparator in (ComparisonComparators.GreaterThan, ComparisonComparators.LessThan,
                                                 ComparisonComparators.GreaterThanOrEqual,
                                                 ComparisonComparators.LessThanOrEqual,
                                                 ComparisonComparators.IsSubSet):
            raise NotImplementedError('Nozomi Vantage is not supported for NOT <, NOT >, NOT <=, NOT >=, NOT ISSUBSET'
                                      ' operators')

        if mapped_field_type == "bytes" and comparator in (ComparisonComparators.Equal, ComparisonComparators.NotEqual,
                                                           ComparisonComparators.In):
            value = f"{value} bytes"

        return value

    def _lookup_comparison_operator(self, expression_operator) -> str:
        """
        lookup operators support in nozomi
        :param expression_operator: (object) contains comparison operator
        :return (str) comparator
        """
        if str(expression_operator) not in self.comparator_lookup:
            raise NotImplementedError(
                f'Comparison operator {expression_operator.name} unsupported for nozomi connector')

        return self.comparator_lookup[str(expression_operator)]

    def _eval_comparison_value(self, expression, mapped_field_type, mapped_fields_array) -> str:
        """
        Function for parsing comparison expression value
        :param expression: (object) ANTLR parsed expression object
        :param mapped_field_type: (str) type of field
        :param mapped_fields_array: (list) list of mapped fields
        :return value: (str) processed/formatted input value
        """
        if expression.comparator == ComparisonComparators.In:
            value = self._format_set(expression.value, mapped_field_type, expression, mapped_fields_array)
        elif expression.comparator in [ComparisonComparators.Like,
                                       ComparisonComparators.GreaterThan, ComparisonComparators.GreaterThanOrEqual,
                                       ComparisonComparators.LessThan, ComparisonComparators.LessThanOrEqual,
                                       ComparisonComparators.Equal, ComparisonComparators.NotEqual,
                                       ComparisonComparators.IsSubSet]:
            value = self._check_value_comparator_support(expression.value, expression.comparator, mapped_field_type,
                                                         mapped_fields_array, expression)
            value = self._format_value(value)
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
        query_qualifier = []
        time_range = QueryStringPatternTranslator._parse_time_range(qualifier, self.options['time_range'])
        for row in query:
            query_qualifier.append(f"{row} | where record_created_at>={time_range[0]} |"
                                   f" where record_created_at<={time_range[1]}")
        return query_qualifier

    @staticmethod
    def _handle_threat_name(formatted_value, comparator) -> str:
        """
        Handle threat name search
        if threat_name = 'threat' means threat_name != ""
        if threat_name == 'alert' means threat_name == ""
        params: formatted_value: (str) input value
        params: comparator: (str) comparison operator
        return: formatted_value : (str) input value
                comparator: (str) comparison operator
        """
        reverse_comparator = {'==': '!=', '!=': '=='}
        if formatted_value == '"threat"':
            comparator = reverse_comparator.get(comparator, comparator)
        formatted_value = '\"\"'
        return formatted_value, comparator

    def _parse_mapped_fields(self, formatted_value, mapped_fields_array, mapped_field_type, expression) -> list:
        """
        parse mapped fields into boolean expression
        :param formatted_value: (str) input value
        :param mapped_fields_array: (list) list of mapped fields
        :param mapped_field_type: (str) type of field
        :param expression: (object) ANTLR parsed expression object
        :return: (list) formatted query
        """
        comparator = self._lookup_comparison_operator(expression.comparator)

        if expression.negated:
            if expression.comparator == ComparisonComparators.Equal:
                comparator = self._lookup_comparison_operator(ComparisonComparators.NotEqual)
            else:
                comparator = f'!{comparator}'

        if expression.comparator in \
                (ComparisonComparators.Like, ComparisonComparators.In, ComparisonComparators.IsSubSet):
            comparator = f' {comparator} '

        if expression.object_path == 'x-ibm-finding:finding_type':
            formatted_value, comparator = self._handle_threat_name(formatted_value, comparator)

        if mapped_field_type == 'subset':
            mapped_fields_array = self.config_map['subset_supported_fields']

        if isinstance(formatted_value, list):
            formatted_value_list = formatted_value
        else:
            formatted_value_list = [formatted_value]

        comparison_list = []

        for value in formatted_value_list:
            comparison_string_new = 'where '
            for index, field_name in enumerate(mapped_fields_array):
                if index > 0 and comparison_string_new != 'where ':
                    comparison_string_new += ' OR '

                if mapped_field_type == 'properties' and 'properties' in field_name:
                    like_operator = self._lookup_comparison_operator(ComparisonComparators.Like)
                    if '!' in comparator:
                        like_operator = f'!{like_operator}'
                    comparison_string_new += f'{field_name} {like_operator} {value}'
                else:
                    comparison_string = f'{field_name}{comparator}{value}'
                    if len(comparison_string_new + comparison_string) > MAX_QUERY_LENGTH:
                        if comparison_string_new[-4:] == ' OR ':
                            comparison_string_new = comparison_string_new[:-4]
                        comparison_list.append(comparison_string_new)
                        comparison_string_new = 'where '
                    comparison_string_new += comparison_string
            comparison_list.append(comparison_string_new)

        return comparison_list

    @staticmethod
    def check_common_timestamp(query_01, query_02):
        """
        Check the queries contains same timestamp
        :param query_01: (str) first query
        :param query_02: (str) second query
        :return query_01_without_timestamp: (str) first query without timestamp
                query_02_without_timestamp: (str) second query without timestamp
                timestamp: (str) common timestamp from query
        """
        # Find the index where timestamp starts in the query string
        query_01_timestamp_index = query_01.find('| where record_created_at>=')
        query_02_timestamp_index = query_02.find('| where record_created_at>=')

        # Check if the substrings from the index in both query strings are equal.
        if query_01[query_01_timestamp_index:] == query_02[query_02_timestamp_index:]:
            timestamp = query_02[query_02_timestamp_index:]
            query_01_without_timestamp = query_01[:query_01_timestamp_index]
            query_02_without_timestamp = query_02[:query_02_timestamp_index]
            return query_01_without_timestamp, query_02_without_timestamp, timestamp
        # If queries do not have a common timestamp, return None.
        return query_01, query_02, None

    @staticmethod
    def _split_and_query_combine_by_or(query_01, query_02):
        """
        Combine AND constructed query with OR operator
        :param query_01: (str) first query
        :param query_02: (str) second query
        :return query_list: (list) first and second query combined by OR operator
        """
        # split the query using the AND operator
        query_01_split_query = query_01.split(' | ')
        query_02_split_query = query_02.split(' | ')
        query_list = []

        # combine using the OR operator
        # ex:(v1 AND v2) OR v3 -> (v1 or v3) AND (v2 or v3)
        for q1 in query_01_split_query:
            for q2 in query_02_split_query:
                query_list.append(f'{q1.strip()} OR {q2.replace("where ", "").strip()}')
        return query_list

    @staticmethod
    def _check_max_query_length(query_01, query_02, combined_query, query_list):
        """
        Check the combined query its less than max_query_length
        :param query_01: (str) first query
        :param query_02: (str) second query
        :param combined_query: (str) first and second query combined
        :param query_list: (list) query list contains processed queries
        :return query_list: (list) query list contains processed queries
        """
        if len(combined_query) > MAX_QUERY_LENGTH:
            # If the combined query length is greater than the maximum query length,
            # will treat each query as a separate query.
            if query_01 not in query_list:
                query_list.append(query_01)
            if query_02 not in query_list:
                query_list.append(query_02)
        else:
            # If the combined query length is less than the maximum query length,
            # will add it to the processed query list.
            query_list.append(combined_query)
        return query_list

    def combine_or_queries(self, expression_01, expression_02, operator='OR') -> list:
        """
        Combine the queries using OR operator.
        Combined query length should be less than the max query length,
        otherwise will treat each query as separate query.
        ex: A , B are two queries. If A OR B is less than max query length returns A OR B
            If A OR B is more than max query length returns [ A , B ]
        :param expression_01: (list) first query
        :param expression_02: (list) second query
        :param operator: (str) operator
        :return query: (list) list of combined queries
        """
        query_list = []

        if len(expression_02) == 1:
            expression_01, expression_02 = expression_02, expression_01

        for row_01 in expression_01:
            combined_flag = False
            for row_02 in expression_02:
                # combine the query length is less than the max query length
                if len(row_01) + len(row_02) < MAX_QUERY_LENGTH and not combined_flag:
                    combined_flag = True
                    # Queries have a timestamp.
                    if 'record_created_at' in row_01 and 'record_created_at' in row_02:
                        row_01_without_timestamp, row_02_without_timestamp, common_timestamp = \
                            self.check_common_timestamp(row_01, row_02)
                        # Queries have a common timestamp.
                        if common_timestamp:
                            split_query_list = self._split_and_query_combine_by_or(row_01_without_timestamp,
                                                                                   row_02_without_timestamp)
                            combined_query = ' | '.join(split_query_list) + f' {common_timestamp}'
                            query_list = self._check_max_query_length(row_01, row_02, combined_query, query_list)
                        else:
                            if row_01 not in query_list:
                                query_list.append(row_01)
                            query_list.append(row_02)
                    # Query contains the AND operator.
                    elif ' | ' in row_01 or ' | ' in row_02:
                        split_query_list = self._split_and_query_combine_by_or(row_01, row_02)
                        combined_query = ' | '.join(split_query_list)
                        query_list = self._check_max_query_length(row_01, row_02, combined_query, query_list)
                    else:
                        combined_query = f'{row_01} {operator} {row_02.replace("where ", "")}'
                        query_list = self._check_max_query_length(row_01, row_02, combined_query, query_list)
                else:
                    if row_02 not in query_list:
                        query_list.append(row_02)
            if not combined_flag:
                if row_01 not in query_list:
                    query_list.append(row_01)
        return query_list

    def combine_and_queries(self, expression_01, expression_02, operator) -> list:
        """
        combine the queries using and operator
        :param expression_01: (list) first query
        :param expression_02: (list) second query
        :param operator: (str) operator
        :return query: (list) list of combined queries
        """
        query_list = []

        for row_01 in expression_01:
            for row_02 in expression_02:
                # combine the query using the AND operator
                combined_query = f'{row_01} {operator} {row_02}'
                # combined query, if the query length exceeds the maximum query length,
                # will treat each query as a separate query
                if len(combined_query) > MAX_QUERY_LENGTH and not self.logged:
                    self.logged = True
                    logger.info('Unable to split the query. Query length is more than maximum length. '
                                'Use OR operator to split the query.')
                query_list.append(combined_query)
        return query_list

    def _eval_combined_comparison_exp(self, expression) -> str:
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
            query = self.combine_or_queries(expression_01, expression_02, operator)
        elif expression.operator == ComparisonExpressionOperators.And:
            query = self.combine_and_queries(expression_01, expression_02, operator)
        return query

    def _eval_combined_observation_exp(self, expression, qualifier=None) -> str:
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
            query = self.combine_or_queries(expression_01, expression_02, operator)
        elif expression_01:
            query = expression_01
        elif expression_02:
            query = expression_02
        return query

    def _parse_expression(self, expression, qualifier=None) -> list:
        """
         Formation of nozomi query from ANTLR parsing expression
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

    def parse_expression(self, pattern: Pattern) -> list:
        """
         Formation of nozomi query from ANTLR parsing expression.
        :param pattern: expression object, ANTLR parsed expression object
        """
        query_list = self._parse_expression(pattern)
        self.qualified_queries = ['query=alerts | ' + row for row in query_list]


def translate_pattern(pattern: Pattern, data_model_mapping, options) -> list:
    """
    Conversion of ANTLR pattern to nozomi vantage query
    :param pattern: expression object, ANTLR parsed expression object
    :param data_model_mapping: DataMapper object, mapping object obtained by parsing json
    :param options: dict, time_range defaults to 5
    :return: list, nozomi queries
    """
    translated_query_strings = QueryStringPatternTranslator(pattern, data_model_mapping, options)
    queries = translated_query_strings.qualified_queries
    return queries
