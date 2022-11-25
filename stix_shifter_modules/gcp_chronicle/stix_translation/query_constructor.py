import copy
from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, \
    ComparisonExpression, ComparisonComparators, Pattern, CombinedComparisonExpression, CombinedObservationExpression
import logging
import re
from datetime import datetime, timedelta
from os import path
import json

logger = logging.getLogger(__name__)

START_STOP_PATTERN = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z)"
MAC = '^(([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2}))$'
EMAIL = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b$'
CONFIG_MAP_PATH = "json/config_map.json"

STOP_TIME = datetime.utcnow()


class StartStopQualifierValueException(Exception):
    pass


class FileNotFoundException(Exception):
    pass


class QueryStringPatternTranslator:
    """
    translate stix pattern to native data source query language
    """

    def __init__(self, pattern: Pattern, data_model_mapper, options):
        logger.info("GCP Chronicle Connector")
        self.dmm = data_model_mapper
        self.options = options
        self.all_queries = []
        self.comparator_lookup = self.dmm.map_comparator()
        self.config_map = self.load_json(CONFIG_MAP_PATH)
        self.parse_expression(pattern)
        self.qualified_query = self._create_formatted_query()

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

    def _create_formatted_query(self):
        """
        Creates formatted native data source query
        Combines similar timestamp observations
        Creates new query for different timestamp observations
        :return: formatted query:list
        """
        final_query = []
        utc_timestamp = STOP_TIME.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        converted_utc_timestamp = QueryStringPatternTranslator._format_datetime(utc_timestamp)
        rule_name = "cp4s_gcp_udi_rule_" + str(converted_utc_timestamp)
        merged_queries = []
        for queries in self.all_queries:
            if not merged_queries:
                merged_queries.append(queries)
            else:
                matched = False
                for query in merged_queries:
                    if queries["timestamp"] == query["timestamp"]:
                        if not query["is_ts_matched"]:
                            query["query"] = f'({query["query"]})'
                            query["is_ts_matched"] = True
                        query["query"] += f' {queries["operator"]} ({queries["query"]})'
                        matched = True
                if not matched:
                    merged_queries.append(queries)
        for queries in merged_queries:
            formatted_query = {
                "ruleText": "rule " + rule_name + " { "
                                                  "meta: author = \"ibm cp4s user\" description = \"Create "
                                                  "event rule that should generate detections\" "
                                                  "events: " + queries['query'] + " condition: $udm}",
                "startTime": queries["timestamp"][0],
                "endTime": queries["timestamp"][1]
            }
            final_query.append(formatted_query)
        return final_query

    @staticmethod
    def _format_set(values, mapped_field_type, is_regex_field) -> list:
        """
        Formats value in the event of set operation
        :param values
        :param mapped_field_type: str
        :param is_regex_field: boolean
        :return formatted value
        """
        gen = values.element_iterator()
        formatted_values = []
        for value in gen:
            formatted_value = QueryStringPatternTranslator._escape_value(
                QueryStringPatternTranslator._format_value_type(value, mapped_field_type), is_regex_field)
            formatted_values.append(formatted_value)
        return formatted_values

    @staticmethod
    def _format_match(value, mapped_field_type) -> str:
        """
        Formats value in the event of Matches operation for regex pattern
        supports only regular expression pattern matching
        :param value
        :param mapped_field_type:str
        """
        if mapped_field_type not in ("string", "email", "mac"):
            raise NotImplementedError(f'MATCHES operator is not supported for {mapped_field_type} type input')
        if not re.search(r'[()}\]\[{*^$+?|]', value):    # replace \\ if regex meta characters are not there
            value = value.replace('\\', '\\\\')
        value = value.replace('/', '\\/')
        return f'/(?s){value}/'  # (?s) to enforce full UDM field matching

    @staticmethod
    def _format_like(value, mapped_field_type) -> str:
        """
        Formats value in the event of like operation for substring matching
        :param value
        :param mapped_field_type:str
        :return formatted string type value
        """
        if mapped_field_type not in ("string", "email", "mac"):
            raise NotImplementedError(f'LIKE operator is not supported for {mapped_field_type} type input')
        value = QueryStringPatternTranslator._escape_value(value, is_regex=True)
        value = value.replace('%', '.*').replace('_', '.')  # replace SQL LIKE characters
        return value

    @staticmethod
    def _format_equality(value, is_regex_field) -> str:
        """
        Formats value in the event of equality operation
        :param value
        :param is_regex_field: boolean
        :return formatted value
        """
        return QueryStringPatternTranslator._escape_value(value, is_regex_field)

    @staticmethod
    def _escape_value(value, is_regex) -> str:
        """
        adds escape characters to string and regex value
        :param value
        :param is_regex: boolean
        :return formatted value
        """
        if is_regex:
            value = re.escape(value).replace('/', "\\/").replace(':', "\\:")
            # (?s) to enforce full UDM field matching
            value = f'/(?s){value}/'
        elif isinstance(value, str):
            value = value.replace('\\', '\\\\').replace('\"', '\\"')
            value = f'\"{value}\"'
        return str(value)

    def _check_enum_supported_values(self, value, mapped_fields_array):
        """
        checks for enum supported values
        :param mapped_fields_array: list
        :param value:str
        :return None
        """
        all_enum_values = []
        for field_name in mapped_fields_array:
            if field_name != "network.dhcp.type":
                field_name = field_name.split('.')[-1]
            if field_name not in self.config_map["enum_supported_values"].keys():
                raise NotImplementedError(f'Enum field - {field_name} is not found in enum_supported_values')
            all_enum_values += list(self.config_map["enum_supported_values"][field_name])
        is_value_present = False
        if not isinstance(value, list):
            value = [value]
        for values in value:
            if values[1:-1] in all_enum_values:
                is_value_present = True
                break  # any one matched input is sufficient to create comparison string
        if not is_value_present:
            raise NotImplementedError(f'Unsupported ENUM values provided. Possible supported'
                                      f' enum values are {all_enum_values}')

    @staticmethod
    def _format_value_type(value, mapped_field_type):
        """
        Converts input value that matches with the mapped field value type
        :param value
        :param mapped_field_type: str
        :return formatted value
        """
        converted_value = str(value)
        if mapped_field_type == "enum":
            converted_value = converted_value.upper()
        elif mapped_field_type == "timestamp":
            converted_value = QueryStringPatternTranslator._format_datetime(converted_value)
        elif mapped_field_type == "mac":
            compile_mac_regex = re.compile(MAC)
            if not compile_mac_regex.search(converted_value):
                raise NotImplementedError(f'Invalid mac address - {converted_value} provided')
        elif mapped_field_type == "int":
            if not converted_value.isdigit():
                raise NotImplementedError(f'string type input - {converted_value} is not supported for '
                                          f'integer type fields')
            converted_value = int(value)
        elif mapped_field_type == "email":
            compile_email_regex = re.compile(EMAIL)
            if not compile_email_regex.search(converted_value):
                raise NotImplementedError(f'Invalid email address - {converted_value} provided')
        return converted_value

    def _check_value_comparator_support(self, value, comparator, mapped_field_type):
        """
        checks the comparator and value support
        :param value
        :param comparator
        :param mapped_field_type: str
        """
        operator = self.comparator_lookup[str(comparator)]
        if mapped_field_type == "enum" and (comparator not in [ComparisonComparators.Equal,
                                                               ComparisonComparators.NotEqual]):
            raise NotImplementedError(f'{operator} operator is not supported for Enum type input. Possible supported '
                                      f'operator are [ =, !=, IN, NOT IN ]')
        if isinstance(value, str) and comparator not in [ComparisonComparators.Equal, ComparisonComparators.NotEqual,
                                                         ComparisonComparators.Like, ComparisonComparators.Matches]:
            raise NotImplementedError(f'{operator} operator is not supported for string type input')

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
                                                     time_pattern) - epoch).total_seconds()))
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

    def _get_mapped_field_type(self, mapped_field_array):
        """
        Returns the type of mapped field array
        :param mapped_field_array: list
        :return: str
        """
        mapped_field = mapped_field_array[0]
        mapped_field_type = "string"
        for key, value in self.config_map.items():
            if mapped_field in value and key in ["int_supported_fields", "email_supported_fields",
                                                 "timestamp_supported_fields", "mac_supported_fields",
                                                 "enum_supported_fields"]:
                mapped_field_type = key.split('_')[0]
                break
        return mapped_field_type

    @staticmethod
    def _security_result_conversion(security_result_conversion_fields, original_field_name, value):
        """
        Conversion of security result field input values
        :param security_result_conversion_fields: dict
        :param original_field_name: str
        :param value: list
        :return: list
        """
        if original_field_name in security_result_conversion_fields:
            values = copy.deepcopy(value)
            value = []
            for val in values:
                formatted_value = val[1:-1]
                if formatted_value in security_result_conversion_fields[original_field_name].keys():
                    category_value = security_result_conversion_fields[original_field_name][formatted_value]
                    if not isinstance(category_value, list):
                        category_value = [category_value]
                    value += ["\"" + i + "\"" for i in category_value]
        return value

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
            "!=": "="
        }
        return negate_comparator[comparator]

    def _add_field_name_condition(self, mapped_field_type, original_field_name, field_name, field_mappings):
        """
        Adds default condition to each field_name
        :param mapped_field_type: str
        :param original_field_name: str
        :param field_name: str
        :param field_mappings: str
        :return str
        """
        split_field_name = original_field_name
        if original_field_name != "network.dhcp.type":
            split_field_name = split_field_name.split('.')[-1]
        unspecified_value = '\"\"'
        if mapped_field_type == 'int':
            unspecified_value = str(0)
        elif mapped_field_type == 'enum':
            if original_field_name == "security_result.category":
                unspecified_value = "UNKNOWN_CATEGORY"
            elif original_field_name == "security_result.severity":
                unspecified_value = "UNKNOWN_SEVERITY"
            else:
                unspecified_value = self.config_map["enum_supported_values"][split_field_name][0]
            unspecified_value = f'\"{unspecified_value}\"'
        add_unspecified_field = f'{field_name} != {unspecified_value}'
        if field_mappings != add_unspecified_field:
            field_mappings = f'( {field_mappings}  and {add_unspecified_field} )'
        return field_mappings

    def _create_parsed_query(self, field_name, value, mapped_field_type, comparator, is_negated):
        """
        Creates comparison string for each field_name in mapped_field_array
        :param field_name: str
        :param value
        :param mapped_field_type: str
        :param comparator: str
        :param is_negated: boolean
        :return: str
        """
        original_field_name = field_name
        field_name = "$udm." + original_field_name
        if original_field_name in self.config_map["list_type_fields"]:
            add_keyword = "any " if comparator == "=" else "all "
            field_name = add_keyword + field_name
        comparison_string = ""
        if not isinstance(value, list):
            value = [value]
        security_result_conversion_fields = self.config_map["security_result_conversion_fields"]
        value = self._security_result_conversion(security_result_conversion_fields, original_field_name, value)
        all_mappings = []
        for values in value:
            split_field_name = original_field_name
            if original_field_name in self.config_map["enum_supported_fields"]:
                if not re.match(r'(?s).*/$', values):
                    values = values.upper()
                mapped_field_type = "enum"
            if mapped_field_type == "enum":
                if split_field_name != "network.dhcp.type":
                    split_field_name = split_field_name.split('.')[-1]
                # value[1:-1] -> removing unwanted double quotes
                if original_field_name not in security_result_conversion_fields and \
                        values[1:-1] not in self.config_map["enum_supported_values"][split_field_name]:
                    continue
            if mapped_field_type not in ("enum", "int", "timestamp"):
                values += " nocase"
            field_mappings = f'{field_name} {comparator} {values}'
            if comparator in ["!=", "<", "<="]:
                field_mappings = self._add_field_name_condition(mapped_field_type, original_field_name, field_name,
                                                                field_mappings)
            all_mappings.append(field_mappings)
        if all_mappings:
            if len(all_mappings) == 1:
                comparison_string += all_mappings[0]
            else:
                condition_string = " and " if is_negated else " or "
                in_comparison_string = f'{condition_string}'.join(all_mappings)
                comparison_string += in_comparison_string
        if len(all_mappings) > 1:
            comparison_string = "(" + comparison_string + ")"
        return comparison_string

    def _parse_mapped_fields(self, formatted_value, mapped_fields_array, mapped_field_type, expression):
        """
        parse mapped fields into boolean expression
        :param formatted_value: str
        :param mapped_fields_array: list
        :param mapped_field_type:str
        :param expression: expression object
        :return: str
        """
        is_negated = expression.negated
        comparator = self._lookup_comparison_operator(expression.comparator)
        if mapped_field_type == "enum":
            self._check_enum_supported_values(formatted_value, mapped_fields_array)
        comparison_string = ""
        comparison_string_new_count = 0
        if is_negated:
            comparator = QueryStringPatternTranslator._format_negate(comparator)
        for field_name in mapped_fields_array:
            comparison_string_new = self._create_parsed_query(field_name, formatted_value, mapped_field_type,
                                                              comparator, is_negated)
            if comparison_string_new:
                comparison_string_new_count += 1
                if comparison_string:
                    comparison_string += " or "
                comparison_string += comparison_string_new

        if len(mapped_fields_array) > 1 and comparison_string and comparison_string_new_count > 1:
            # More than one data source field maps to the STIX attribute, so group comparisons together.
            grouped_comparison_string = "(" + comparison_string + ")"
            comparison_string = grouped_comparison_string
        return comparison_string

    def _lookup_comparison_operator(self, expression_operator):
        """
        lookup operators support in gcp chronicle
        :param expression_operator:enum object
        :return str
        """
        if str(expression_operator) not in self.comparator_lookup:
            raise NotImplementedError(
                f'Comparison operator {expression_operator.name} unsupported for gcp chronicle connector')

        return self.comparator_lookup[str(expression_operator)]

    def _eval_comparison_value(self, expression, mapped_field_type, mapped_fields_array):
        """
        Function for parsing comparison expression value
        :param expression: expression object
        :param mapped_field_type:str
        :return: formatted expression value
        """
        is_regex_field = mapped_fields_array[0] in self.config_map["regex_formatting_fields"]
        if expression.comparator == ComparisonComparators.Like:
            value = self._format_like(expression.value, mapped_field_type)
        elif expression.comparator == ComparisonComparators.Matches:
            value = self._format_match(expression.value, mapped_field_type)
        elif expression.comparator == ComparisonComparators.In:
            value = QueryStringPatternTranslator._format_set(expression.value, mapped_field_type, is_regex_field)
        elif expression.comparator in [ComparisonComparators.GreaterThan, ComparisonComparators.GreaterThanOrEqual,
                                       ComparisonComparators.LessThan, ComparisonComparators.LessThanOrEqual,
                                       ComparisonComparators.Equal, ComparisonComparators.NotEqual]:
            value = QueryStringPatternTranslator._format_value_type(expression.value, mapped_field_type)
            self._check_value_comparator_support(value, expression.comparator, mapped_field_type)
            value = self._format_equality(value, is_regex_field)
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
            expression_01 = f'({expression_01})'
        if isinstance(expression.expr2, CombinedComparisonExpression):
            expression_02 = f'({expression_02})'
        query_string = f'{expression_01} {operator} {expression_02}'
        return f'{query_string}'

    def _eval_combined_observation_exp(self, expression, qualifier=None):
        """
        Function for parsing combined observation expression
        :param expression: expression object
        :param qualifier:  str, default in None
        """
        combined_obs_operator = self._lookup_comparison_operator(expression.operator)
        self._parse_expression(expression.expr1, qualifier)
        self.comparator_lookup["current_observation_operator"] = combined_obs_operator
        self._parse_expression(expression.expr2, qualifier)

    def _parse_expression(self, expression, qualifier=None):
        """
        parse ANTLR pattern to gcp chronicle  yara-l  query
        :param expression: expression object, ANTLR parsed expression object
        :param qualifier: str, default in None
        """
        if isinstance(expression, ComparisonExpression):  # Base Case
            stix_objects = expression.object_path.split(':')
            mapped_fields_array = self.dmm.map_field(stix_objects[0], stix_objects[1])
            mapped_field_type = self._get_mapped_field_type(mapped_fields_array)
            value = self._eval_comparison_value(expression, mapped_field_type, mapped_fields_array)
            comparison_string = self._parse_mapped_fields(value, mapped_fields_array, mapped_field_type, expression)
            return comparison_string
        elif isinstance(expression, CombinedComparisonExpression):
            return self._eval_combined_comparison_exp(expression)
        elif isinstance(expression, ObservationExpression):
            query_data = {}
            query_string = f'{self._parse_expression(expression.comparison_expression)}'
            if isinstance(expression.comparison_expression, ComparisonExpression) and query_string and \
                    query_string[0] == "(" and query_string[-1] == ")":
                query_string = query_string[1:-1]  # removes extra brackets ()
            time_range_list = QueryStringPatternTranslator._parse_time_range(qualifier, self.options["time_range"])
            QueryStringPatternTranslator._check_time_range_values(time_range_list)  # check for valid timestamp values
            obs_operator = self.comparator_lookup["current_observation_operator"] if "current_observation_operator" \
                                                                                     in self.comparator_lookup else "or"
            query_data.update({"query": query_string, "timestamp": time_range_list, "operator": obs_operator,
                               "is_ts_matched": False})
            self.all_queries.append(query_data)
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
        self._parse_expression(pattern)


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    """
        Conversion of ANTLR pattern to gcp chronicle  query
        :param pattern: expression object, ANTLR parsed expression object
        :param data_model_mapping: DataMapper object, mapping object obtained by parsing json
        :param options: dict, time_range defaults to 5
        :return: list
    """
    query = QueryStringPatternTranslator(pattern, data_model_mapping, options).qualified_query
    return query
