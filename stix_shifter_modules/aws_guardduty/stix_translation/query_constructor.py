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
        logger.info("AWS GuardDuty Connector")
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
    def _format_value_type(expression, value, mapped_field_type, comparator):
        """
        Converts input value that matches with the mapped field value type
        :param expression
        :param value
        :param mapped_field_type: str
        :param comparator
        :return formatted value
        """
        stix_object, stix_field = expression.object_path.split(':')
        converted_value = str(value)
        if mapped_field_type == "int":
            if not converted_value.isdigit():
                raise NotImplementedError(f'string type input - {converted_value} is not supported for '
                                          f'integer type field {stix_object}:{stix_field}')
            if str(comparator) not in ("ComparisonComparators.Equal", "ComparisonComparators.NotEqual",
                                       "ComparisonComparators.In"):
                converted_value = int(value)
        elif mapped_field_type == "boolean":
            converted_value = QueryStringPatternTranslator._check_boolean_value(converted_value)
        return converted_value

    @staticmethod
    def _check_boolean_value(final_value):
        """
        returns boolean value of input
        :param final_value:str
        :return bool
        """
        if final_value.lower() == "true" or (final_value.isdigit() and final_value == "1"):
            boolean_value = "true"
        elif final_value.lower() == "false" or (final_value.isdigit() and final_value == "0"):
            boolean_value = "false"
        else:
            raise NotImplementedError('Invalid boolean type input')
        return boolean_value

    @staticmethod
    def _format_set(expression, values, mapped_field_type, comparator):
        """
        Formatting value in the event of set operation
        :param expression
        :param values: str or int ,
        :param mapped_field_type: str
        :param comparator
        :return: list of formatted values
        """
        gen = values.element_iterator()
        formatted_values = []
        for value in gen:
            formatted_value = QueryStringPatternTranslator._escape_value(
                QueryStringPatternTranslator._format_value_type(expression, value, mapped_field_type, comparator))
            formatted_values.append(formatted_value)
        return formatted_values

    @staticmethod
    def _format_equality(expression, value, mapped_field_type, comparator):
        """
        Formatting value in the event of equality operation
        :param expression
        :param value: str or int ,
        :param mapped_field_type: str
        :param comparator
        :return: list of formatted values
        """
        value = QueryStringPatternTranslator._escape_value(
            QueryStringPatternTranslator._format_value_type(expression, value, mapped_field_type, comparator))
        if comparator in [ComparisonComparators.GreaterThan, ComparisonComparators.GreaterThanOrEqual,
                          ComparisonComparators.LessThan, ComparisonComparators.LessThanOrEqual]:
            return value
        return [value]

    @staticmethod
    def _escape_value(value):
        """
        Format the value with escape characters
        :param value: str or int
        :return: str or int
        """
        if isinstance(value, str):
            return '{}'.format(value.replace('\\', '\\\\').replace('\"', '\\"').replace('(', '\\(').replace(')', '\\)'))
        return value

    @staticmethod
    def _negate_comparator(comparator):
        """
        returns negation of input operator
        :param comparator:str
        :return str
        """
        negate_comparator = {
            "Equals": "NotEquals",
            "NotEquals": "Equals",
            "LessThan": "GreaterThanOrEqual",
            "LessThanOrEqual": "GreaterThan",
            "GreaterThan": "LessThanOrEqual",
            "GreaterThanOrEqual": "LessThan"
        }
        return negate_comparator[comparator]

    @staticmethod
    def _format_datetime(value):
        """
        Converts timestamp to seconds
        :param value
        :return: int, converted epoch value
        """
        try:
            time_pattern = '%Y-%m-%dT%H:%M:%S.%fZ'
            if re.search(r"\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}Z", str(value)):
                time_pattern = '%Y-%m-%dT%H:%M:%SZ'
            epoch = datetime(1970, 1, 1)
            converted_time = int(((datetime.strptime(value,
                                                     time_pattern) - epoch).total_seconds()) * 1000)
            return converted_time
        except ValueError:
            logger.error("Cannot convert the timestamp %s to seconds", value)
        raise NotImplementedError(f'cannot convert the timestamp {value} to seconds')

    def _check_enum_supported_values(self, value, mapped_fields_array, stix_object, stix_field):
        """
        checks for enum supported values
        :param mapped_fields_array: list
        :param value:str
        :param stix_object: str
        :param stix_field: str
        :return: None
        """
        all_enum_values = []
        if mapped_fields_array[0] in self.config_map["enum_supported_values"]:
            all_enum_values = self.config_map["enum_supported_values"][mapped_fields_array[0]]
        value_not_present = False
        for val in value:
            if val not in all_enum_values:
                value_not_present = True
                break

        if value_not_present:
            raise NotImplementedError(f"The input value provided for the field "
                                      f"{stix_object}:{stix_field} is not among the possible values of the field."
                                      f"Suggested values are {all_enum_values}")

    @staticmethod
    def _or_operator_query(previous_all_queries, current_all_queries):
        """
        Create individual queries for different fields and merge the values incase of similar fields
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
                if previous_query.keys() == current_query.keys():
                    matched_key = [i for i in current_query.keys() if i != 'updatedAt'][0]
                    p_operator = list(previous_query[matched_key].keys())[0]
                    c_operator = list(current_query[matched_key].keys())[0]
                    if c_operator == p_operator and c_operator in ('Equals', 'NotEquals') and p_operator in \
                            ('Equals', 'NotEquals'):
                        # merge values of similar attributes for =,!= operator
                        merged_similar_query = copy.deepcopy(previous_query)
                        merged_similar_query[matched_key][p_operator].extend(current_query[matched_key][c_operator])
                        merged_similar_query[matched_key][p_operator] = list(set(merged_similar_query
                                                                                 [matched_key][p_operator]))
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
                        # create individual queries for similar attributes if operator is not =, !=
                        if previous_query not in individual_query and previous_query not in \
                                already_merged_query:
                            individual_query.append(previous_query)
                        if current_query not in individual_query and current_query not in \
                                already_merged_query:
                            individual_query.append(current_query)

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
                if not current_query.keys() - previous_query.keys():
                    comparison = str(expression).split(" ")
                    raise SimilarExpressionForAndOperatorException(f'The expression [{comparison[0][21:]}] has same '
                                                                   f'data source field mapping with another expression '
                                                                   f'in the pattern which has only AND comparison '
                                                                   f'operator. Recommended to Use OR operator. ')
                # merge multiple queries into a single query
                previous_query.update(current_query)
                if previous_query not in merged_query:
                    merged_query.append(previous_query)
        return merged_query

    def _lookup_comparison_operator(self, expression_operator):
        """
        lookup operators support in AWS GuardDuty
        :param expression_operator:enum object
        :return: str
        """
        if str(expression_operator) not in self.comparator_lookup:
            raise NotImplementedError(
                f'Comparison operator {expression_operator.name} unsupported for AWS GuardDuty connector')

        return self.comparator_lookup[str(expression_operator)]

    def _create_single_comparison_query(self, formatted_value, mapped_fields_array, mapped_field_type, expression,
                                        qualifier):
        """
        Create a query for a comparison expression
        :param formatted_value, str or int or boolean
        :param mapped_fields_array, list
        :param mapped_field_type, str
        :param expression
        :param qualifier, str
        :return: list
        """
        queries = []
        stix_object, stix_field = expression.object_path.split(':')
        comparator = self._lookup_comparison_operator(expression.comparator)
        if mapped_field_type == "enum":
            self._check_enum_supported_values(formatted_value, mapped_fields_array, stix_object, stix_field)
        if expression.negated:
            comparator = QueryStringPatternTranslator._negate_comparator(comparator)
        time_range_list = QueryStringPatternTranslator._parse_time_range(qualifier, self.options["time_range"])
        converted_time_range = QueryStringPatternTranslator._check_time_range_values(time_range_list)
        for field_name in mapped_fields_array:
            query = dict()
            query[field_name] = {comparator: formatted_value}
            query['updatedAt'] = {"GreaterThanOrEqual": converted_time_range[0],
                                  "LessThanOrEqual": converted_time_range[1]}
            queries.append(query)
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
            value = QueryStringPatternTranslator._format_set(expression, expression.value, mapped_field_type,
                                                             expression.comparator)
        elif expression.comparator in [ComparisonComparators.GreaterThan, ComparisonComparators.GreaterThanOrEqual,
                                       ComparisonComparators.LessThan, ComparisonComparators.LessThanOrEqual,
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
            return time_range_list
        except (KeyError, IndexError, TypeError) as e:
            raise e

    @staticmethod
    def _check_time_range_values(time_range_list):
        """
        checks for valid start and stop time
        :param time_range_list: list
        """
        converted_timestamp = []
        for timestamp in time_range_list:
            converted_time = QueryStringPatternTranslator._format_datetime(timestamp)
            converted_timestamp.append(converted_time)
        if converted_timestamp[0] >= converted_timestamp[1]:
            raise StartStopQualifierValueException('Start time should be lesser than Stop time')
        return converted_timestamp

    def _check_value_comparator_support(self, expression, comparator, mapped_field_type):
        """
        checks the comparator and value support
        :param comparator
        :param mapped_field_type: str
        :return: None
        """
        stix_object, stix_field = expression.object_path.split(':')
        comparator_str = str(comparator).split(".")[1]
        if expression.negated:
            comparator_str = f'NOT {comparator_str}'
        if mapped_field_type == "enum" and (comparator not in [ComparisonComparators.Equal,
                                                               ComparisonComparators.NotEqual,
                                                               ComparisonComparators.In]):
            raise NotImplementedError(f'{comparator_str} operator is not supported for Enum type field {stix_object}:'
                                      f'{stix_field}. Possible supported operators are  =, !=, IN, NOT IN ')
        if mapped_field_type == "string" and comparator not in [ComparisonComparators.Equal,
                                                                ComparisonComparators.NotEqual,
                                                                ComparisonComparators.In]:
            raise NotImplementedError(f'{comparator_str} operator is not supported for string type field {stix_object}:'
                                      f'{stix_field}.Possible supported operators are  =, !=, IN, NOT IN')
        if mapped_field_type == "boolean" and comparator not in [ComparisonComparators.Equal,
                                                                 ComparisonComparators.NotEqual]:
            raise NotImplementedError(f'{comparator_str} operator is not supported for Boolean type field '
                                      f'{stix_object}:{stix_field}. Possible supported operators are  =, != ')

    def _get_mapped_field_type(self, mapped_field_array):
        """
        Returns the type of mapped field array
        :param mapped_field_array: list
        :return: str
        """
        mapped_field = mapped_field_array[0]
        mapped_field_type = "string"
        for key, value in self.config_map.items():
            if mapped_field in value and key in ["int_supported_fields",
                                                 "enum_supported_fields",
                                                 "boolean_supported_fields"
                                                 ]:
                mapped_field_type = key.split('_')[0]
                break
        return mapped_field_type

    def _parse_mapped_fields(self, value, mapped_fields_array, mapped_field_type, expression, qualifier, or_operator):
        """
        Creates queries based on combined comparison expression.
        Created queries will be updated in combined_query
        :param value: formatted list
        :param mapped_field_type: string
        :param expression
        :param qualifier
        :param mapped_fields_array : list of mapped fields
        :param or_operator: boolean
        """
        current_query = self._create_single_comparison_query(value, mapped_fields_array, mapped_field_type, expression,
                                                             qualifier)

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
         parse ANTLR pattern to AWS GuardDuty  query format
        :param expression: expression object, ANTLR parsed expression object
        :param qualifier: str, default in None
        :param or_operator: boolean
        """
        if isinstance(expression, ComparisonExpression):  # Base Case
            stix_object, stix_field = expression.object_path.split(':')
            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
            mapped_field_type = self._get_mapped_field_type(mapped_fields_array)
            value = self._eval_comparison_value(expression, mapped_field_type)
            self._parse_mapped_fields(value, mapped_fields_array, mapped_field_type, expression, qualifier,
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
    Conversion of ANTLR pattern to AWS GuardDuty  query
    :param pattern: expression object, ANTLR parsed expression object
    :param data_model_mapping: DataMapper object, mapping object obtained by parsing json
    :param options: dict
    :return: list
    """
    query = QueryStringPatternTranslator(pattern, data_model_mapping, options).qualified_queries
    final_queries = [{'FindingCriteria': {'Criterion': item}} for sublist in query for item in sublist]
    return final_queries
