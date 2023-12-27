import re
import json
import logging
from os import path
from itertools import product
from datetime import datetime, timedelta
from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, \
    ComparisonExpression, ComparisonComparators, Pattern, CombinedComparisonExpression, CombinedObservationExpression

START_STOP_PATTERN = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z)"
logger = logging.getLogger(__name__)
CONFIG_MAP_PATH = "json/config_map.json"
STOP_TIME = datetime.utcnow()


class FileNotFoundException(Exception):
    pass


class StartStopQualifierValueException(Exception):
    pass


class QueryStringPatternTranslator:

    def __init__(self, pattern: Pattern, data_model_mapper, options):
        logger.info("CrowdStrike LogScale Connector")
        self.dmm = data_model_mapper
        self.config_map = QueryStringPatternTranslator.load_json(CONFIG_MAP_PATH)
        self.options = options
        self.all_queries = []
        self.comparator_lookup = self.dmm.map_comparator()
        self.source = self.dmm.dialect
        self.parse_expression(pattern)
        self.translated_query = self._create_formatted_query()

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
    def _format_set(values, list_of_dict_field=False):
        """
        Formats value in the event of IN operation
        :param: values
        :return: formatted values,str
        """
        gen = values.element_iterator()
        if list_of_dict_field:
            formatted_values = [QueryStringPatternTranslator._escape_value(value, list_of_dict_field=list_of_dict_field)
                                for value in gen]
        else:
            formatted_values = \
                [f'\"{QueryStringPatternTranslator._escape_value(value, list_of_dict_field=list_of_dict_field)}\"'
                 for value in gen]
        return formatted_values

    @staticmethod
    def _format_subset(expression, values):
        """
        Formats value in the event of subset operation
        :param expression, values
        :return: formatted values,str
        """
        if expression.negated:
            return f'!cidr(subnet=\"{values}\")'
        return f'cidr(subnet=\"{values}\")'

    @staticmethod
    def _format_match(value, array_fields=None):
        """
        Formats value in the event of match operation
        :param value: str, array_fields: list
        :return: formatted string type value, str
        """
        value = QueryStringPatternTranslator._escape_value(value, is_regex=True, array_fields=array_fields)
        return value

    @staticmethod
    def _format_like(value, array_fields=None):
        """
        Formatting value in the event of like operation
        :param value: str, array_fields: list
        :return: formatted string type value, str
        """
        value = value.replace('%', '.*').replace('_', '.')
        value = QueryStringPatternTranslator._escape_value(value, is_regex=True, array_fields=array_fields)
        return value

    @staticmethod
    def format_equals(value):
        """
        Formats value in the event of equals operation
        :param value: str
        :return: formatted values,str
        """

        if isinstance(value, str):
            value = value.replace('\\', '\\\\').replace('\"', '\\"')
        value = f'\"{value}\"'
        return value

    @staticmethod
    def _escape_value(value, is_regex=False, list_of_dict_field=False, array_fields=None):
        """
        Format the value with escape characters
        :param value: str or int, is_regex: bool, list_of_dict_field: bool, array_fields: list
        :return: value, str or int
        """
        value = str(value)
        if list_of_dict_field:
            value = re.escape(value).replace('/', '\\/').replace('\\\\', '\\\\\\\\').replace('\"', '\\\\\"')

        elif is_regex:
            value = (value.replace('\\', '\\\\').replace('\"', '\\"').replace('(', '\\(').replace(')', '\\)').
                     replace('/', '\\/'))

            value = f'/{value}/i' if not array_fields else value

        return value

    @staticmethod
    def _validate_numerical_value(comparator, value):
        """
        Validate the input value with numerical operators and raise exception in case of invalid type
        :param comparator, value: int
        :return: value,int
        """
        if not isinstance(value, int):
            raise NotImplementedError(f'{comparator} operator is not supported string type value: {value}')
        return value

    def _create_formatted_query(self):
        """
        Creates formatted native data source query
        :return: formatted query: list
        """
        final_query = []
        merged_queries = []
        self.all_queries = [i for n, i in enumerate(self.all_queries) if i not in self.all_queries[:n]]

        for queries in self.all_queries:
            if not merged_queries:
                merged_queries.append(queries)
            else:
                matched = False
                for query in merged_queries:
                    if queries["operator"] != "|" and query["operator"] != "|" and \
                            queries["timestamp"] == query["timestamp"]:
                        if not query["is_ts_matched"]:
                            query["query"] = f'({query["query"]})'
                            query["is_ts_matched"] = True
                        query["query"] += f' {queries["operator"]} ({queries["query"]})'
                        matched = True
                if not matched:
                    merged_queries.append(queries)

        for queries in merged_queries:
            result_query_string = f'{queries["query"]} | tail({self.options["result_limit"]})' \
                if self.options["result_limit"] <= 10000 else queries["query"]
            formatted_query = {
                "source": self.source,
                "queryString": result_query_string,
                "start": queries["timestamp"][0],
                "end": queries["timestamp"][1]
            }
            final_query.append(formatted_query)
        return final_query

    def validate_values(self, field_name, list_of_dict_value, array_not_in_list_of_dict):
        """
        Validate the input values
        :param: field_name: str, list_of_dict_value: list, array_not_in_list_of_dict: bool
        :return: formatted query: str or int
        """
        if field_name in self.config_map.get(self.source, {}).get('integer_fields', []):
            if isinstance(list_of_dict_value, list):
                if len(list_of_dict_value) > 1:
                    return f'({"|".join(list_of_dict_value)})'
                return "|".join(list_of_dict_value)
            return int(list_of_dict_value)

        if isinstance(list_of_dict_value, list):
            if array_not_in_list_of_dict:
                return f'{"|".join(list_of_dict_value)}'
            if len(list_of_dict_value) > 1:
                joined_str = '|'.join([f'\"{val}\"' for val in list_of_dict_value])
                return f'({joined_str})'
            return '|'.join([f'\"{val}\"' for val in list_of_dict_value])
        return f'\"{list_of_dict_value}\"'

    @staticmethod
    def _attribute_processing(field_name):
        """
        Removing the "[*]" from mapped attributes
        :param field_name: str
        :return: list_attribute: list
        """
        list_attribute = []
        split_field = field_name.split(".")
        for field in split_field:
            if "[*]" in field:
                field = field[:-3] + '[]'
            list_attribute.append(field)
        return list_attribute

    def _create_parsed_query_for_list_of_dict(self, field_name, list_of_dict_value, expression_comparator):
        """
        create parsed query for list of dict fields
        :param: field_name: str, list_of_dict_value: list, expression_comparator: object
        :return: formatted query: list
        """
        array_in_list_of_dict = False
        array_not_in_list_of_dict = False

        if field_name.endswith("[*]"):
            if field_name.count("[*]") > 1:
                array_in_list_of_dict = True
            else:
                array_not_in_list_of_dict = True
        list_of_dict_value = self.validate_values(field_name, list_of_dict_value, array_not_in_list_of_dict)

        list_attribute = self._attribute_processing(field_name)

        if array_not_in_list_of_dict:
            new_field_name = ".".join(list_attribute)
        else:
            new_field_name = ""
            for index, value in enumerate(list_attribute):
                if value.endswith('[]'):
                    value = f'\"{value[:-2]}\"' + r"\s*:\s*\[.*"
                elif index < len(list_attribute) - 1:
                    value = f'\"{value}\"' + r"\s*:\s*\{.*"
                else:
                    value = f'\"{value}\"'
                new_field_name += value

        operator = "!=" if expression_comparator == ComparisonComparators.NotEqual else "="

        if array_in_list_of_dict:
            field_mappings = f'@rawstring {operator} /{new_field_name}' + f'{list_of_dict_value}/'
        elif array_not_in_list_of_dict:
            if expression_comparator in [ComparisonComparators.Like, ComparisonComparators.Matches]:
                field_mappings = f'array:regex(array=\"{new_field_name}\",regex = \"{list_of_dict_value}\", flags=i)'
            else:
                if operator == "!=":
                    field_mappings = f'!array:contains(array=\"{new_field_name}\",value = {list_of_dict_value})'
                else:
                    field_mappings = f'array:contains(array=\"{new_field_name}\",value = {list_of_dict_value})'
        else:
            field_mappings = f'@rawstring {operator} /{new_field_name}' + r'\s*:\s*' + f'{list_of_dict_value}/'

        return field_mappings

    def _create_parsed_query(self, field_name, list_of_dict_value, value, comparator, is_negated,
                             expression_comparator):
        """
        Creates comparison string for each field_name in mapped_field_array
        :param field_name: str,
        :param list_of_dict_value: list
        :param value: str
        :param comparator: str
        :param is_negated: boolean
        :param expression_comparator: str
        :return: comparison_string, str
        """
        comparison_string = ""
        if not isinstance(value, list):
            value = [value]

        all_mappings = []
        if "[*]" in field_name:
            list_value = value if field_name.endswith("[*]") and field_name.count("[*]") == 1 else list_of_dict_value

            field_mappings = self._create_parsed_query_for_list_of_dict(field_name, list_value,
                                                                        expression_comparator)
            if is_negated:
                field_mappings = f'not {field_mappings}'
            all_mappings.append(field_mappings)
        else:
            for values in value:
                if expression_comparator == ComparisonComparators.NotEqual and not is_negated:
                    field_mappings = f'({field_name} {comparator} {values} and {field_name} = "*")'
                elif (expression_comparator != ComparisonComparators.IsSubSet) and is_negated:
                    field_mappings = (f'(not {field_name} {comparator} {values} '
                                      f'and {field_name} = "*")')
                else:
                    field_mappings = f'{field_name} {comparator} {values}'
                all_mappings.append(field_mappings)

        if all_mappings:
            if len(all_mappings) == 1:
                comparison_string += all_mappings[0]
            else:
                in_comparison_string = ' and '.join(all_mappings) if is_negated else ' or '.join(all_mappings)
                comparison_string += in_comparison_string

        if len(all_mappings) > 1:
            comparison_string = "(" + comparison_string + ")"

        return comparison_string

    @staticmethod
    def _format_datetime(value):
        """
        Converts timestamp to seconds
        :param value: str
        :return: converted epoch value: int
        """
        try:
            time_pattern = '%Y-%m-%dT%H:%M:%S.%fZ'
            if re.search(r"\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}Z", str(value)):
                time_pattern = '%Y-%m-%dT%H:%M:%SZ'
            epoch = datetime(1970, 1, 1)
            converted_time = int(((datetime.strptime(value, time_pattern) - epoch).total_seconds()) * 1000)
            return converted_time
        except ValueError:
            logger.error("Cannot convert the timestamp %s to seconds", value)
        raise NotImplementedError(f'cannot convert the timestamp {value} to seconds')

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
        :return: converted_timestamp, list
        """
        utc_timestamp = STOP_TIME.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        converted_utc_timestamp = QueryStringPatternTranslator._format_datetime(utc_timestamp)
        converted_timestamp = []
        for timestamp in time_range_list:
            converted_time = QueryStringPatternTranslator._format_datetime(timestamp)
            if converted_time > converted_utc_timestamp:
                raise StartStopQualifierValueException('Start/Stop time should not be in the future UTC timestamp')
            converted_timestamp.append(converted_time)
        if converted_timestamp[0] >= converted_timestamp[1]:
            raise StartStopQualifierValueException('Start time should be lesser than Stop time')
        return converted_timestamp

    def _eval_combined_observation_exp(self, expression, qualifier=None):
        """
        Function for parsing combined observation expression
        :param expression: object
        :param qualifier:  str, default in None
        """
        combined_obs_operator = self._lookup_comparison_operator(expression.operator)
        self._parse_expression(expression.expr1, qualifier, combined_observation=True)
        self.comparator_lookup["current_observation_operator"] = combined_obs_operator
        self._parse_expression(expression.expr2, qualifier, combined_observation=True)

    def _parse_mapped_fields(self, list_of_dict_value, value, expression, mapped_fields_array):
        """
        creates comparison expression for the mapped fields
        :param list_of_dict_value: list
        :param expression: expression
        :param mapped_fields_array: list
        :return comparison_string,str
        """
        subset_expression = []
        is_negated = expression.negated
        comparison_string = ""
        comparison_string_new_count = 0
        for field_name in mapped_fields_array:
            comparator = self._lookup_comparison_operator(expression.comparator)
            comparison_string_new = self._create_parsed_query(field_name, list_of_dict_value,
                                                              value, comparator, is_negated,
                                                              expression.comparator)

            if comparison_string_new:
                if expression.comparator in [ComparisonComparators.IsSubSet] or (
                        field_name.endswith("[*]") and field_name.count("[*]") == 1):
                    subset_expression.append(comparison_string_new)
                else:
                    comparison_string_new_count += 1
                    if comparison_string:
                        comparison_string += " or "
                    comparison_string += comparison_string_new

        if len(mapped_fields_array) > 1 and comparison_string and comparison_string_new_count > 1:
            # More than one data source field maps to the STIX attribute, so group comparisons together.
            comparison_string = "(" + comparison_string + ")"

        return comparison_string, subset_expression

    def _lookup_comparison_operator(self, expression_operator):
        """
        Fetch the comparison operator of the expression
        :param expression_operator:
        return operator,str
        """
        if str(expression_operator) not in self.comparator_lookup:
            raise NotImplementedError(f"Comparison operator {expression_operator.name} unsupported for connector")
        return self.comparator_lookup[str(expression_operator)]

    def _eval_combined_comparison_exp(self, expression):
        """
        Function for parsing combined comparison expression
        :param expression: object
        :return query_string: str
        """
        operator = self._lookup_comparison_operator(expression.operator)
        expression_01 = self._parse_expression(expression.expr1)
        expression_02 = self._parse_expression(expression.expr2)

        if isinstance(expression.expr1, CombinedComparisonExpression) and expression_01:
            expression_01 = f'({expression_01})'
        if isinstance(expression.expr2, CombinedComparisonExpression) and expression_02:
            expression_02 = f'({expression_02})'

        if not expression_01 or not expression_02:
            query_string = f'{expression_01}' if expression_01 else f'{expression_02}'
        else:
            query_string = f'{expression_01} {operator} {expression_02}'
        return query_string

    def _eval_comparison_value(self, expression, list_of_dict_fields, individual_fields, array_fields):
        """
        Function for parsing comparison expression value
        :param expression: expression object
        :param list_of_dict_fields: list
        :param individual_fields: list
        :param array_fields: list
        :return: formatted expression value
        """
        list_of_dict_value, value = None, None
        if list_of_dict_fields and expression.comparator not in [ComparisonComparators.In,
                                                                 ComparisonComparators.NotEqual,
                                                                 ComparisonComparators.Equal]:
            raise NotImplementedError(f'{expression.comparator} is not supported for list of dictionary '
                                      f'fields [{",".join(list_of_dict_fields)}]')
        if array_fields and expression.comparator not in (ComparisonComparators.Like, ComparisonComparators.Matches,
                                                          ComparisonComparators.NotEqual,
                                                          ComparisonComparators.Equal):
            raise NotImplementedError(f'{expression.comparator} is not supported for array attribute '
                                      f' [{",".join(array_fields)}]')

        if expression.comparator == ComparisonComparators.Like and (individual_fields or array_fields):
            value = self._format_like(expression.value, array_fields)
        elif expression.comparator == ComparisonComparators.Matches and (individual_fields or array_fields):
            value = self._format_match(expression.value, array_fields=array_fields)
        elif expression.comparator == ComparisonComparators.In:
            if list_of_dict_fields:
                list_of_dict_value = self._format_set(expression.value, list_of_dict_fields)
            if individual_fields:
                value = self._format_set(expression.value)
        elif expression.comparator == ComparisonComparators.IsSubSet and individual_fields:
            value = self._format_subset(expression, expression.value)
        elif expression.comparator in [ComparisonComparators.GreaterThan, ComparisonComparators.GreaterThanOrEqual,
                                       ComparisonComparators.LessThan, ComparisonComparators.LessThanOrEqual] and \
                individual_fields:
            value = self._validate_numerical_value(expression.comparator, expression.value)
        elif expression.comparator in [ComparisonComparators.Equal, ComparisonComparators.NotEqual]:
            if list_of_dict_fields:
                list_of_dict_value = (QueryStringPatternTranslator._escape_value
                                      (expression.value, list_of_dict_field=list_of_dict_fields))
            if individual_fields or array_fields:
                value = self.format_equals(expression.value)
        else:
            raise NotImplementedError('Unknown comparator expression operator')

        return list_of_dict_value, value

    def _merge_observation_exp(self, expression, query_string, converted_time_range, obs_operator):
        """
        Function for merging observation expression
        :param expression: expression object
        :param query_string: str
        :param converted_time_range: str
        :param obs_operator: str
        """
        query_combinations = list(product(*self.query_list))
        if 'ComparisonExpressionOperators.Or' not in str(expression):
            if query_string:
                for row in query_combinations:
                    joined_query = f'{" | ".join(row)} | {query_string}'
                    self.all_queries.append(
                        {"query": joined_query, "timestamp": converted_time_range, "operator": "|",
                         "is_ts_matched": False})
            else:
                for row in query_combinations:
                    self.all_queries.append(
                        {"query": " | ".join(row), "timestamp": converted_time_range, "operator": "|",
                         "is_ts_matched": False})
        else:
            merged_list = sum(self.query_list, [])
            for row in merged_list:
                self.all_queries.append({"query": row, "timestamp": converted_time_range, "operator": "|",
                                         "is_ts_matched": False})

            if 'ComparisonExpressionOperators.Or' in str(expression) and query_string:
                self.all_queries.append({"query": query_string, "timestamp": converted_time_range,
                                         "operator": obs_operator, "is_ts_matched": False})

    def _eval_observation_exp(self, expression, combined_observation, qualifier):
        """
        Function for parsing observation expression value
        :param expression: expression object
        :param combined_observation: bool
        :param qualifier: expression object
        :return: formatted expression value
        """
        self.query_list = []
        query_string = f'{self._parse_expression(expression.comparison_expression)}'
        if isinstance(expression.comparison_expression, ComparisonExpression) and query_string and \
                query_string[0] == "(" and query_string[-1] == ")":
            query_string = query_string[1:-1]  # removes extra brackets ()

        time_range_list = QueryStringPatternTranslator._parse_time_range(qualifier, self.options["time_range"])
        converted_time_range = QueryStringPatternTranslator._check_time_range_values(time_range_list)
        obs_operator = self.comparator_lookup[
            "current_observation_operator"] if "current_observation_operator" in self.comparator_lookup else "or"

        if combined_observation:
            if self.query_list:
                merged_list = sum(self.query_list, [])
                for row in merged_list:
                    self.all_queries.append({"query": row, "timestamp": converted_time_range, "operator": "|",
                                             "is_ts_matched": False})
            if query_string:
                self.all_queries.append(
                    {"query": query_string, "timestamp": converted_time_range, "operator": obs_operator,
                     "is_ts_matched": False})
        else:
            if self.query_list:
                self._merge_observation_exp(expression, query_string, converted_time_range, obs_operator)
            else:
                self.all_queries.append({"query": query_string, "timestamp": converted_time_range,
                                         "operator": obs_operator, "is_ts_matched": False})

    def _parse_expression(self, expression, qualifier=None, combined_observation=False):
        """
         parse ANTLR pattern to CrowdStrike LogScale query format
        :param expression: expression object, ANTLR parsed expression object
        :param qualifier: str, default in None
        """
        if isinstance(expression, ComparisonExpression):
            stix_object, stix_field = expression.object_path.split(':')
            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
            list_of_dict_fields, individual_fields, array_fields = ([j for j in mapped_fields_array if "[*]" in j
                                                                     and
                                                                     not (j.endswith("[*]") and j.count("[*]") == 1)],
                                                                    [i for i in mapped_fields_array if "[*]" not in i],
                                                                    [k for k in mapped_fields_array if k.endswith("[*]")
                                                                     and k.count("[*]") == 1])
            list_of_dict_value, value = self._eval_comparison_value(expression, list_of_dict_fields,
                                                                    individual_fields, array_fields)
            comparison_string, comparison_list = self._parse_mapped_fields(list_of_dict_value, value, expression,
                                                                           mapped_fields_array)
            if comparison_list:
                self.query_list.append(comparison_list)
            return comparison_string
        elif isinstance(expression, CombinedComparisonExpression):
            return self._eval_combined_comparison_exp(expression)
        elif isinstance(expression, ObservationExpression):
            return self._eval_observation_exp(expression, combined_observation, qualifier)
        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            self._parse_expression(expression.observation_expression, expression.qualifier)
        elif isinstance(expression, CombinedObservationExpression):
            self._eval_combined_observation_exp(expression, qualifier)
        elif isinstance(expression, Pattern):
            self._parse_expression(expression.expression)
        else:
            raise RuntimeError(f'Unknown Recursion Case for expression={expression},'
                               f' type(expression)={type(expression)}')
        return None

    def parse_expression(self, pattern: Pattern):
        return self._parse_expression(pattern)


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    """
        Conversion of ANTLR pattern to Crowdstrike LogScale  query
        :param pattern: expression object, ANTLR parsed expression object
        :param data_model_mapping: DataMapper object, mapping object obtained by parsing json
        :param options: dict
        :return: list
    """
    translator = QueryStringPatternTranslator(pattern, data_model_mapping, options)
    return translator.translated_query
