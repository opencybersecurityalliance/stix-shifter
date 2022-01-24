from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, \
    ComparisonExpression, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression
import re
import json
from datetime import datetime, timedelta
from os import path
import copy
from stix_shifter_utils.utils import logger

logger = logger.set_logger(__name__)

START_STOP_PATTERN = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z)"
MAC = '^(([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2}))$'
EMAIL = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b$'
CONFIG_MAP_PATH = "json/config_map.json"

STOP_TIME = datetime.utcnow()


class LinkNotFoundException(Exception):
    pass


class QueryStringPatternTranslator:
    """
    comparator values to match with supported data source operators
    """

    def __init__(self, pattern: Pattern, data_model_mapper, options):

        logger.info("Cybereason Connector")
        self.dmm = data_model_mapper
        self.comparator_lookup = self.dmm.map_comparator()
        self.pattern = pattern
        self.options = options
        self.config_map = self.load_json(CONFIG_MAP_PATH)
        self.qualified_queries = []
        self.parse_expression(pattern)

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
    def _format_negate(comparator):
        """
        returns negation of input operator
        :param comparator:str
        :return str
        """
        negate_comparator = {
            "GreaterThan": "LessOrEqualsTo",
            "GreaterOrEqualsTo": "LessThan",
            "LessThan": "GreaterOrEqualsTo",
            "LessOrEqualsTo": "GreaterThan",
            "Equals": "NotEquals",
            "NotEquals": "Equals",
            "ContainsIgnoreCase": "NotContainsIgnoreCase"
        }
        return negate_comparator[comparator]

    @staticmethod
    def _format_datetime(value):
        """
        Converts timestamp to epoch
        :param value
        :return: int, converted epoch value
        """
        try:
            time_pattern = '%Y-%m-%dT%H:%M:%S.%fZ'

            epoch = datetime(1970, 1, 1)
            converted_time = int(((datetime.strptime(value,
                                                     time_pattern) - epoch).total_seconds()) * 1000)
            return converted_time
        except ValueError:
            pass
        raise NotImplementedError(f'cannot convert the timestamp {value} to milliseconds')

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
        if filter_name in self.config_map["email_filter_names"]:
            compile_email_regex = re.compile(EMAIL)
            if not compile_email_regex.search(final_value):
                raise NotImplementedError(f'Invalid email address - {value} provided')
        elif filter_name in self.config_map["timestamp_filter_names"]:
            final_value = QueryStringPatternTranslator._format_datetime(final_value)
        elif filter_name in self.config_map["mac_address_filter_name"]:
            compile_mac_regex = re.compile(MAC)
            if not compile_mac_regex.search(final_value):
                raise NotImplementedError(f'Invalid mac address - {value} provided')
        elif filter_name in self.config_map["int_supported_element"]:
            if not final_value.isdigit():
                raise NotImplementedError(f'string type input - {value} is not supported for int field - {filter_name}')
            final_value = int(value)
        elif filter_name in self.config_map["boolean_supported_element"]:
            final_value = QueryStringPatternTranslator._check_boolean_value(final_value)
        return final_value

    def _format_equality(self, value, mapped_fields_array):

        """
        Formatting value in the event of equality operation
        :param value: str or int ,
        :param mapped_fields_array: list
        :return: list of formatted values
        """
        filter_name = mapped_fields_array[0].split('.')[1]
        final_value = self._check_field_value_support(filter_name, value)
        return [final_value]

    def _format_set(self, value, mapped_fields_array):
        """
        Formatting value in the event of set operation
        Checking and converting all values in list that is supported by filter_name
        :param value:str
        :param mapped_fields_array:list
        :return: list of converted format
        """
        filter_name = mapped_fields_array[0].split('.')[1]
        if filter_name in self.config_map["boolean_supported_element"]:
            raise NotImplementedError("IN operator is not supported for Boolean fields")
        final_value = []
        for val in value.values:
            final_value.append(self._check_field_value_support(filter_name, val))
        return final_value

    def _format_like(self, value, mapped_fields_array):
        """
        Formatting value in the event of like operation
        :param value,mapped_fields_array
        :return: list
        """
        wildcard = ['%', '$', '+', '*', '^', '?']
        filter_name = mapped_fields_array[0].split('.')[1]
        if filter_name in self.config_map["int_supported_element"] or \
                filter_name in self.config_map["timestamp_filter_names"] or \
                filter_name in self.config_map["boolean_supported_element"]:

            raise NotImplementedError("LIKE OR MATCHES operator is not supported for Integer/Timestamp/Boolean fields")
        for val in wildcard:
            if val in value:
                raise NotImplementedError("Wildcard characters is not supported in Cybereason")
        return [value]

    @staticmethod
    def _parse_time_range(qualifier, time_range):
        """
        Converts qualifier timestamp to epoch
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

    def __eval_comparison_value(self, expression, mapped_fields_array):
        """
        Function for parsing comparison expression value
        :param expression: expression object, mapped_fields_array
        :return: formatted expression value
        """
        value = None
        if expression.comparator == ComparisonComparators.In:

            value = self._format_set(expression.value, mapped_fields_array)

        elif expression.comparator in [ComparisonComparators.GreaterThan, ComparisonComparators.GreaterThanOrEqual,
                                       ComparisonComparators.LessThan,
                                       ComparisonComparators.LessThanOrEqual, ComparisonComparators.Equal,
                                       ComparisonComparators.NotEqual]:
            value = self._format_equality(expression.value, mapped_fields_array)
        elif expression.comparator in [ComparisonComparators.Like, ComparisonComparators.Matches]:
            value = self._format_like(expression.value, mapped_fields_array)
        return value

    @staticmethod
    def _formatted_query(add_query_path, add_custom_fields, options):
        """
        Cybereason native data source format
        """
        query = {
            "queryPath": add_query_path,
            "queryLimits": {
                "groupingFeature": {
                    "elementInstanceType": add_query_path[0]["requestedType"],
                    "featureName": "elementDisplayName"
                }
            },
            "perFeatureLimit": 1,
            "totalResultLimit": options["result_limit"] - 1,  # Cybereason returns 1 more than totalResultLimit records along with
            "perGroupLimit": 1,                               # the options perfeaturelimit=1 and perGroupLimit=1
            "templateContext": "CUSTOM",
            "customFields": add_custom_fields

        }
        return query

    def _update_filter_type(self, comparator, facet_name):
        """
        Updates filter type for specific feature names
        :return :str, updated filter type
        """
        filter_type = str(comparator)
        if facet_name in self.config_map["include_filter_type"]:
            if filter_type in ["Equals", "ContainsIgnoreCase"]:
                filter_type = "Includes"  # equal and not equal operator is not supported in these filters
            elif filter_type in ["NotEquals"]:
                filter_type = "NotIncludes"
            else:
                raise NotImplementedError(f"operator type - {filter_type} is not supported for {facet_name}")
        return filter_type

    def _create_single_comparison_query(self, comparator, value, mapped_fields_array, qualifier):
        """
        creates individual query for every comparison expression
        :param comparator: str
        :param value: list
        :param mapped_fields_array : list
        :return : list
        """
        queries = []
        for mapped_field in mapped_fields_array:
            request_type, facet_name = mapped_field.split('.')
            filter_type = self._update_filter_type(comparator, facet_name)
            if filter_type in ["LessThan", "LessOrEqualsTo", "GreaterThan", "GreaterOrEqualsTo"] \
                    and isinstance(value[0], str):
                raise NotImplementedError(f"{filter_type} operator is not supported for string type input")
            elif filter_type not in ["Equals", "NotEquals"] \
                    and isinstance(value[0], bool):
                raise NotImplementedError(f"{filter_type} operator is not supported for boolean type input")

            add_query_path = [{"requestedType": request_type,
                               "filters": [{"facetName": facet_name, "filterType": filter_type, "values": value}],
                               "isResult": bool(True)}]
            add_custom_fields = self.config_map["custom_fields"][request_type]
            if request_type in self.config_map["timestamp_supported_element"].keys():
                add_timestamp_filter_type = {"facetName": self.config_map["timestamp_supported_element"]
                                                                         [request_type],
                                             "filterType": "Between",
                                             "values": self._parse_time_range(qualifier, self.options["time_range"])}

                add_query_path[0]["filters"].append(add_timestamp_filter_type)

            query = self._formatted_query(add_query_path, add_custom_fields, self.options)
            queries.append(query)
        return queries

    @staticmethod
    def _merge_similar_element(current_query, previous_query, merged_query):
        """
        Merge similar elements
        Merge similar - last feature element of previous query with first feature element of current query
        :param current_query: dict
        :param previous_query: dict
        :param merged_query : list
        """
        current_query_path = current_query["queryPath"][0]
        previous_query_path = previous_query["queryPath"][-1]
        unmatched_filters = []

        for current_filter in current_query_path["filters"]:
            if current_filter not in previous_query_path["filters"]:
                unmatched_filters.append(current_filter)
        current_query_path["filters"] = unmatched_filters + previous_query_path["filters"]
        del previous_query_path["isResult"]
        del previous_query["queryPath"][-1]
        previous_query["queryPath"] += current_query["queryPath"]
        previous_query["customFields"] = current_query["customFields"]
        previous_query["queryLimits"] = current_query["queryLimits"]

        if previous_query not in merged_query:
            merged_query.append(previous_query)

    def _merge_linked_element(self, previous_queries, current_query, merged_query):
        """
        Merge linked feature element between previous query  and current query
        Merge linked - last feature element of previous query with first feature element of current query
        :param previous_queries:dict
        :param current_query:dict
        :param merged_query:list
        """
        previous_requested_type = previous_queries["queryPath"][-1]["requestedType"]
        current_requested_type = current_query["queryPath"][0]["requestedType"]
        for feature_names in self.config_map["linked_fields"][previous_requested_type][current_requested_type]:
            previous_query = copy.deepcopy(previous_queries)
            previous_query_path = previous_query["queryPath"][-1]
            add_connection_feature = {
                "connectionFeature": {
                    "elementInstanceType": feature_names["elementInstanceType"],
                    "featureName": feature_names["feature"],
                }
            }
            if feature_names["isreversed"]:
                add_connection_feature.update({"isReversed": bool(True)})
            del previous_query_path["isResult"]
            previous_query_path.update(add_connection_feature)
            previous_query["queryPath"] += current_query["queryPath"]
            previous_query["customFields"] = current_query["customFields"]
            previous_query["queryLimits"] = current_query["queryLimits"]
            merged_query.append(previous_query)

    def _and_operator_query(self, previous_all_queries, current_all_queries):
        """
        Merge previous query with current query
        :param previous_all_queries:list
        :param current_all_queries:list
        :return : list
        """
        merged_query = []
        for previous_queries in previous_all_queries:
            for current_queries in current_all_queries:
                current_query = copy.deepcopy(current_queries)
                previous_query = copy.deepcopy(previous_queries)
                previous_query_path = previous_query["queryPath"][-1]
                previous_requested_type = previous_query_path["requestedType"]
                current_query_path = current_query["queryPath"][0]
                current_requested_type = current_query_path["requestedType"]
                if current_requested_type == previous_requested_type:
                    QueryStringPatternTranslator._merge_similar_element(current_query, previous_query, merged_query)
                elif current_requested_type in self.config_map["linked_fields"][previous_requested_type].keys():
                    self._merge_linked_element(previous_query,
                                               current_query, merged_query)
        if not merged_query:
            raise LinkNotFoundException('Link is not found between elements')
        return merged_query

    def _parse_mapped_fields(self, comparator, value, mapped_fields_array, qualifier):
        """
        Creates queries based on combined comparison expression.
        Created queries will be updated in combined_query
        :param comparator: str , comparison expression operator type
        :param value: formatted list
        :param mapped_fields_array : list of mapped fields
        """
        current_query = self._create_single_comparison_query(comparator, value, mapped_fields_array, qualifier)
        if not self.qualified_queries[-1]:
            self.qualified_queries[-1] = current_query
        else:
            previous_query = self.qualified_queries.pop()
            merged_query = self._and_operator_query(previous_query, current_query)
            self.qualified_queries.append(merged_query)

    def __eval_observation_expression(self, expression, qualifier):
        """
        Function for parsing observation expression
        :param expression: expression object
        :param qualifier: qualifier
        """
        self.qualified_queries.append([])
        self._parse_expression(expression.comparison_expression, qualifier)
        if len(self.qualified_queries) > 1:
            current_query = self.qualified_queries.pop()
            previous_query = self.qualified_queries.pop()
            merged_query = self._and_operator_query(previous_query, current_query)
            self.qualified_queries.append(merged_query)

    def _parse_expression(self, expression, qualifier=None):
        """
        Formation of Cybereason query from ANTLR parsing expression
        :param expression: expression object, ANTLR parsed expression object
        :param qualifier: str, default in None
        :return :None or str
        """
        if isinstance(expression, ComparisonExpression):  # Base Case
            stix_object, stix_field = expression.object_path.split(':')
            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
            comparator = self.comparator_lookup[str(expression.comparator)]
            if expression.negated:
                comparator = QueryStringPatternTranslator._format_negate(comparator)
            value = self.__eval_comparison_value(expression, mapped_fields_array)
            self._parse_mapped_fields(comparator, value, mapped_fields_array, qualifier)

        elif isinstance(expression, CombinedComparisonExpression):
            self._parse_expression(expression.expr1, qualifier)
            self._parse_expression(expression.expr2, qualifier)
        elif isinstance(expression, ObservationExpression):
            self.__eval_observation_expression(expression, qualifier)

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
            raise RuntimeError(f'Unknown Recursion Case for expression={expression}, '
                               f'type(expression)={type(expression)}')

    def parse_expression(self, pattern: Pattern):
        if "ComparisonExpressionOperators.Or" in str(pattern) or "ObservationOperators.Or" in str(pattern):
            raise NotImplementedError("OR operator is not supported in Cybereason")

        self._parse_expression(pattern)


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    """
    Conversion of ANTLR pattern to Cybereason query
    :param pattern: expression object, ANTLR parsed expression object
    :param data_model_mapping: DataMapper object, mapping object obtained by parsing json
    :param options: dict, time_range defaults to 5
    :return: list, Cybereason queries
    """
    translated_query_strings = QueryStringPatternTranslator(pattern, data_model_mapping, options)
    queries = translated_query_strings.qualified_queries
    final_queries = [item for sublist in queries for item in sublist]
    return final_queries
