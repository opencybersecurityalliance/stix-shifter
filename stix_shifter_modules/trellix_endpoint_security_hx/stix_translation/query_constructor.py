from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, \
    ComparisonExpression, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression
import logging
import re
import json
from datetime import datetime, timedelta
from os import path
import copy

logger = logging.getLogger(__name__)

START_STOP_PATTERN = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z)"
STOP_TIME = datetime.utcnow()
CONFIG_MAP_PATH = "json/config_map.json"


class FileNotFoundException(Exception):
    pass


class StartStopQualifierValueException(Exception):
    pass


class SimilarExpressionForAndOperatorException(Exception):
    pass


class QueryStringPatternTranslator:

    def __init__(self, pattern: Pattern, data_model_mapper, options):
        logger.info("Trellix Endpoint Security HX Connector")
        self.dmm = data_model_mapper
        self.options = options
        self.qualified_queries = []
        self.config_map = self.load_json(CONFIG_MAP_PATH)
        self.comparator_lookup = self.dmm.map_comparator()
        self.parse_expression(pattern)

    @staticmethod
    def load_json(rel_path_of_file):
        """
        Consumes a json file and returns a dictionary
        :param rel_path_of_file: str
        :return: dict
        """
        _json_path = path.dirname(path.abspath(__file__)) + "/" + rel_path_of_file
        try:
            if path.exists(_json_path):
                with open(_json_path, encoding='utf-8') as f_obj:
                    return json.load(f_obj)
            raise FileNotFoundException
        except FileNotFoundException as e:
            raise FileNotFoundError(f'{rel_path_of_file} not found') from e

    @staticmethod
    def _format_value_type(expression, value, mapped_field_type):
        """
        Converts input value that matches with the mapped field value type
        :param expression
        :param value
        :param mapped_field_type: str
        :return formatted value
        """
        stix_object, stix_field = expression.object_path.split(':')
        converted_value = str(value)
        if mapped_field_type == "int":
            if not converted_value.isdigit():
                raise NotImplementedError(f'string type input - {converted_value} is not supported for '
                                          f'integer type field {stix_object}:{stix_field}')
            converted_value = int(value)
        return converted_value

    @staticmethod
    def _format_in(expression, values, mapped_field_type):
        """
        Formatting value in the event of IN operation
        :param expression
        :param values: str or int
        :param mapped_field_type: str
        :return: list of formatted values
        """
        gen = values.element_iterator()
        formatted_values = []
        for value in gen:
            formatted_value = QueryStringPatternTranslator._escape_value(
                QueryStringPatternTranslator._format_value_type(expression, value, mapped_field_type))
            formatted_values.append(formatted_value)
        return formatted_values

    @staticmethod
    def _format_equality(expression, value, mapped_field_type, comparator):
        """
        Formatting value in the event of equality operation
        :param expression
        :param value: str or int
        :param mapped_field_type: str
        :return: list of formatted values
        """
        value = QueryStringPatternTranslator._escape_value(
            QueryStringPatternTranslator._format_value_type(expression, value, mapped_field_type))
        if comparator in [ComparisonComparators.GreaterThan, ComparisonComparators.LessThan]:
            return value
        return value

    @staticmethod
    def _escape_value(value):
        """
        Format the value with escape characters
        :param value: str or int
        :return: str or int
        """
        if isinstance(value, str):
            return '{}'.format(value.replace('"', '\"'))
        return value

    @staticmethod
    def _negate_comparator(comparator):
        """
        returns negation of input operator
        :param comparator:str
        :return str
        """
        negate_comparator = {
            "equals": "not equals",
            "not equals": "equals",
            "less than": "greater than",
            "contains": "not contains",
            "greater than": "less than",
        }
        return negate_comparator[comparator]

    def _lookup_comparison_operator(self, expression_operator):
        """
        lookup operators support in trellix_endpoint_security_hx
        :return: str
        """
        if str(expression_operator) not in self.comparator_lookup:
            raise NotImplementedError(
                f'Comparison operator {expression_operator.name} unsupported for trellix_endpoint_security_hx')

        return self.comparator_lookup[str(expression_operator)]

    @staticmethod
    def _or_operator_query(previous_all_queries, current_all_queries):
        """
        Create individual queries for different fields and merge the values in case of similar fields
        :param previous_all_queries:list
        :param current_all_queries:list
        :return: list
        """
        merged_query = []
        similar_query = []
        individual_query = []
        already_merged_query = []
        for previous_queries in previous_all_queries:
            for current_queries in current_all_queries:
                current_query = copy.deepcopy(current_queries)
                previous_query = copy.deepcopy(previous_queries)
                previous_key = [i['field'] for i in previous_query['query'] if i['field'] != 'Timestamp - Event']
                current_key = [j['field'] for j in current_query['query'] if j['field'] != 'Timestamp - Event']
                if current_key == previous_key or current_key[0] in previous_key:
                    # merge queries in case of same attribute combined by OR operator
                    merged_similar_query = copy.deepcopy(previous_query)
                    c_query = [j for j in current_query['query'] if j['field'] == current_key[0]]
                    merged_similar_query['query'].extend(c_query)
                    if previous_query in individual_query:
                        individual_query.remove(previous_query)
                    if current_query in individual_query:
                        individual_query.remove(current_query)
                    if previous_query not in already_merged_query:
                        already_merged_query.append(previous_query)
                    if current_query not in already_merged_query:
                        already_merged_query.append(current_query)
                    if merged_similar_query not in similar_query:
                        similar_query.append(merged_similar_query)

                else:
                    # create individual queries in case of different attributes
                    if previous_query not in individual_query and previous_query not in already_merged_query:
                        individual_query.append(previous_query)
                    if current_query not in individual_query and current_query not in already_merged_query:
                        individual_query.append(current_query)

        merged_query.extend(individual_query)
        merged_query.extend(similar_query)
        return merged_query

    @staticmethod
    def _and_operator_query(previous_all_queries, current_all_queries, expression):
        """
        Merge previous query with current query, and log the error in case of similar fields
        :param expression
        :param previous_all_queries:list
        :param current_all_queries:list
        :return: list
        """
        merged_query = []
        for previous_queries in previous_all_queries:
            for current_queries in current_all_queries:
                current_query = copy.deepcopy(current_queries)
                previous_query = copy.deepcopy(previous_queries)
                previous_key = [i['field'] for i in previous_query['query'] if i['field'] != 'Timestamp - Event']
                current_key = [j['field'] for j in current_query['query'] if j['field'] != 'Timestamp - Event']
                if current_key == previous_key or current_key[0] in previous_key:
                    comparison = str(expression).split(" ")
                    raise SimilarExpressionForAndOperatorException(f'The expression [{comparison[0][21:]}] has same '
                                                                   f'data source field mapping with another expression '
                                                                   f'in the pattern which has only AND comparison '
                                                                   f'operator. Recommended to Use OR operator. ')
                # merge multiple queries into a single query
                c_query = [j for j in current_query['query'] if j['field'] != 'Timestamp - Event']
                for new in c_query:
                    previous_query['query'].append(new)
                if previous_query not in merged_query:
                    merged_query.append(previous_query)
        return merged_query

    def _create_single_comparison_query(self, formatted_value, mapped_fields_array, expression,
                                        qualifier):
        """
        Create a query for a comparison expression
        :param formatted_value, str or int or boolean
        :param mapped_fields_array, list
        :param expression
        :param qualifier, str
        :return: list
        """
        comparator = self._lookup_comparison_operator(expression.comparator)
        if expression.negated:
            comparator = QueryStringPatternTranslator._negate_comparator(comparator)
        time_range_list = QueryStringPatternTranslator._parse_time_range(qualifier, self.options["time_range"])
        stix_object, stix_field = expression.object_path.split(':')
        queries = []
        for field_name in mapped_fields_array:
            if field_name == "HTTP Header" and comparator not in ["contains", "not contains"]:
                raise NotImplementedError(
                    f'{str(expression.comparator).split(".")[1]} operator is not supported for '
                    f'{stix_object}:{stix_field}.'
                    f'Possible supported operators are LIKE, NOT LIKE, MATCHES, NOT MATCHES')
            if expression.comparator == ComparisonComparators.In:
                format_query = []
                for val in formatted_value:
                    query = {"field": field_name, "value": val, "operator": comparator}
                    format_query.append(query)
                time_format = {
                    "field": "Timestamp - Event",
                    "operator": "between",
                    "value": time_range_list
                }
                format_query.append(time_format)
                queries.append({"query": format_query})
            else:
                query = {"field": field_name, "value": formatted_value, "operator": comparator}
                time_format = {"field": "Timestamp - Event",
                               "operator": "between",
                               "value": time_range_list
                               }
                format_query = {"query": [query, time_format]}

                queries.append(format_query)
        return queries

    def _eval_comparison_value(self, expression, mapped_field_type):
        """
        Function for parsing comparison expression value
        :param expression, expression object
        :param mapped_field_type, str
        :return: formatted value
        """
        self._check_value_comparator_support(expression, expression.comparator, mapped_field_type)
        if expression.comparator == ComparisonComparators.In:
            value = QueryStringPatternTranslator._format_in(expression, expression.value, mapped_field_type)

        elif expression.comparator in [ComparisonComparators.GreaterThan, ComparisonComparators.Like,
                                       ComparisonComparators.LessThan, ComparisonComparators.Matches,
                                       ComparisonComparators.Equal, ComparisonComparators.NotEqual]:
            value = QueryStringPatternTranslator._format_equality(expression, expression.value, mapped_field_type,
                                                                  expression.comparator)

        else:
            raise NotImplementedError('Unknown comparator expression operator')
        return value

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
            utc_timestamp = STOP_TIME.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            for timestamp in time_range_list:
                if timestamp > utc_timestamp:
                    raise StartStopQualifierValueException('Start/Stop time should not be in the future UTC timestamp')
            if time_range_list[0] >= time_range_list[1]:
                raise StartStopQualifierValueException('Start time should be lesser than Stop time')
            return time_range_list
        except (KeyError, IndexError, TypeError) as e:
            raise e

    def _check_value_comparator_support(self, expression, comparator, mapped_field_type):
        """
        checks the comparator and value support
        :param comparator
        :param mapped_field_type: str
        :return: None
        """
        stix_object, stix_field = expression.object_path.split(':')
        comparator_str = str(comparator).split(".")[1]
        if (((stix_object == "file" and stix_field == "parent_directory_ref.path") or
             (stix_object == "directory" and stix_field == "path") or
             (stix_object == "process" and stix_field == "parent_ref.cwd")) and comparator not in
                [ComparisonComparators.Like, ComparisonComparators.Matches]):
            raise NotImplementedError(
                f'{comparator_str} operator is not supported for {stix_object}:'
                f'{stix_field}.Possible supported operators are  LIKE, MATCHES, NOT LIKE, NOT MATCHES')
        elif mapped_field_type == "string" and comparator in [ComparisonComparators.GreaterThan,
                                                              ComparisonComparators.LessThan]:
            raise NotImplementedError(f'{comparator_str} operator is not supported for string type field {stix_object}:'
                                      f'{stix_field}. Possible supported operators are  =, !=, IN, NOT IN, LIKE, '
                                      f'NOT LIKE,MATCHES,NOT MATCHES')
        elif mapped_field_type == "int" and comparator in [ComparisonComparators.Like, ComparisonComparators.Matches]:
            raise NotImplementedError(f'{comparator_str} operator is not supported for integer '
                                      f'type field {stix_object}:'
                                      f'{stix_field}.Possible supported operators are  =, !=, IN, NOT IN, <, >')
        elif mapped_field_type in ["hash", "ip"] and comparator in [ComparisonComparators.GreaterThan,
                                                                    ComparisonComparators.LessThan,
                                                                    ComparisonComparators.Like,
                                                                    ComparisonComparators.Matches]:
            m_type = "IP Address" if mapped_field_type == "ip" else "File Hash"
            raise NotImplementedError(
                f'{comparator_str} operator is not supported for {m_type} type field {stix_object}:'
                f'{stix_field}.Possible supported operators are  =, !=, IN, NOT IN')

    def _get_mapped_field_type(self, mapped_field_array):
        """
        Returns the type of mapped field array
        :param mapped_field_array: list
        :return: str
        """
        mapped_field = mapped_field_array[0]
        mapped_field_type = "string"
        for key, value in self.config_map.items():
            if mapped_field in value and key in ["int_supported_fields"]:
                mapped_field_type = key.split('_')[0]
                break
            elif mapped_field in value and key in ["hash_supported_fields", "ip_supported_fields"]:
                mapped_field_type = key.split('_')[0]
                break
        return mapped_field_type

    def _parse_mapped_fields(self, value, mapped_fields_array, expression, qualifier, or_operator):
        """
        Creates queries based on combined comparison expression.
        """
        current_query = self._create_single_comparison_query(value, mapped_fields_array, expression, qualifier)
        if not self.qualified_queries[-1]:
            self.qualified_queries[-1] = current_query
        else:
            previous_query = self.qualified_queries.pop()
            if or_operator:
                merged_query = QueryStringPatternTranslator._or_operator_query(previous_query, current_query)
            else:
                merged_query = QueryStringPatternTranslator._and_operator_query(previous_query, current_query,
                                                                                expression)
            self.qualified_queries.append(merged_query)

    @staticmethod
    def verify_common_stix_attributes(comparison_expression):
        """
        Raise Exception if similar six attributes are used in a pattern which has only AND operator
        :param comparison_expression
        """
        comparison_expression_str = str(comparison_expression)
        comparison_pattern_1 = re.finditer(pattern=r'\(ComparisonExpression\(', string=comparison_expression_str)
        comparison_pattern_2 = re.finditer(pattern=r' ComparisonExpression\(', string=comparison_expression_str)
        indices = [index.start() for index in comparison_pattern_1] + [index.start() for index in comparison_pattern_2]
        indices.sort()
        for i in indices:
            end_index = comparison_expression_str.find(')', i)
            exp = comparison_expression_str[i:end_index + 1]
            comparison = exp.split(" ")
            if comparison[0] != "" and comparison_expression_str.find(comparison[0][1:], end_index) != -1:
                raise SimilarExpressionForAndOperatorException(
                    f'Multiple [{comparison[0][22:]}] expression is used in the pattern which has only AND comparison '
                    f'operator. Recommended to Use OR operator for similar STIX attributes.')

    def _parse_expression(self, expression, qualifier=None, or_operator=None):
        """
         parse ANTLR pattern to TRELLIX ENDPOINT SECURITY HX  query format
        :param expression: expression object, ANTLR parsed expression object
        :param qualifier: str, default is None
        :param or_operator: boolean
        """
        if isinstance(expression, ComparisonExpression):  # Base Case
            stix_object, stix_field = expression.object_path.split(':')
            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
            mapped_field_type = self._get_mapped_field_type(mapped_fields_array)
            value = self._eval_comparison_value(expression, mapped_field_type)

            self._parse_mapped_fields(value, mapped_fields_array, expression, qualifier,
                                      or_operator)

        elif isinstance(expression, CombinedComparisonExpression):
            if self.or_operator_enabled:
                self._parse_expression(expression.expr1, qualifier, True)
                self._parse_expression(expression.expr2, qualifier, True)
            else:
                self._parse_expression(expression.expr1, qualifier)
                self._parse_expression(expression.expr2, qualifier)

        elif isinstance(expression, ObservationExpression):
            self.or_operator_enabled = False
            self.qualified_queries.append([])
            if 'ComparisonExpressionOperators.Or' in str(expression.comparison_expression):
                self.or_operator_enabled = True
            else:
                QueryStringPatternTranslator.verify_common_stix_attributes(expression.comparison_expression)
            self._parse_expression(expression.comparison_expression, qualifier)
        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            if isinstance(expression.observation_expression, CombinedObservationExpression):
                self._parse_expression(expression.observation_expression.expr1, expression.qualifier)
                self._parse_expression(expression.observation_expression.expr2, expression.qualifier)
            else:
                self._parse_expression(expression.observation_expression, expression.qualifier)

        elif isinstance(expression, CombinedObservationExpression):
            self._parse_expression(expression.expr1, qualifier)
            self._parse_expression(expression.expr2, qualifier)

        elif isinstance(expression, Pattern):
            self._parse_expression(expression.expression)
        else:
            raise RuntimeError(f"Unknown Recursion Case for expression={expression}, "
                               f"type(expression)={type(expression)}")

    def parse_expression(self, pattern: Pattern):
        self._parse_expression(pattern)


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    """
    Conversion of ANTLR pattern to TRELLIX ENDPOINT SECURITY HX  query
    :param pattern: expression object, ANTLR parsed expression object
    :param data_model_mapping: DataMapper object, mapping object obtained by parsing json
    :param options: dict
    :return: list
    """
    query = QueryStringPatternTranslator(pattern, data_model_mapping, options).qualified_queries
    final_queries = [item for sublist in query for item in sublist]
    updated_queries = [{"host_set": {"_id": host}, "query": item['query']} for item in final_queries
                       for host in options['host_sets'].split(",") if host]
    return updated_queries
