from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, \
    ComparisonExpression, ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators, StartStopQualifier
import re
import json
import os.path as path
from datetime import datetime, timedelta
from collections.abc import Iterable

TIMESTAMP_PATTERN = r"\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z"
PROTOCOL_LOOKUP_JSON_FILE = 'json/network_protocol_map.json'
GUARDDUTY_CONFIG = 'json/guardduty_config.json'

ARRAY_TYPE_COLUMNS = {
    'ocsf': {
        'resources.': {'from': 'UNNEST(resources) as t(resource)', 'where': 'resource.'},
        'src_endpoint.intermediate_ips': {'from': 'UNNEST(src_endpoint.intermediate_ips) as t(src_intermediate_ips)', 'where': 'src_intermediate_ips'},
        'dst_endpoint.intermediate_ips': {'from': 'UNNEST(dst_endpoint.intermediate_ips) as t(dst_intermediate_ips)', 'where': 'dst_intermediate_ips'}
    }
}


class QueryStringPatternTranslator:

    def __init__(self, pattern: Pattern, data_model_mapper, time_range):
        self.dmm = data_model_mapper
        self.comparator_lookup = self.dmm.map_comparator()
        self._time_range = time_range
        self.service_type = self.dmm.dialect
        self._protocol_lookup_needed = True if self.service_type in ['vpcflow', 'ocsf'] else False
        self._epoch_time = True if self.service_type in ['vpcflow', 'ocsf'] else False
        self.qualifier_string = ''
        self.translated = self.parse_expression(pattern)

    @staticmethod
    def _format_set(values) -> tuple:
        """
        Formatting list of values in the event of IN operation
        :param values: str
        :return: list
        """
        if not isinstance(values, tuple):
            values = values.element_iterator()
        return tuple("{}".format(value) for value in values)

    @staticmethod
    def _format_match(value) -> str:
        """
        Formatting value in the event of MATCHES operation
        :param value: str
        :return: str
        """
        return '{}'.format(value)

    @staticmethod
    def _format_equality(value) -> str:
        """
        Formatting value in the event of EQUALS operation
        :param value: str
        :return: str
        """
        return "{}".format(value)

    @staticmethod
    def _format_like(value) -> str:
        """
        Formatting value in the event of LIKE operation
        :param value: str
        :return: str
        """
        value = "{value}".format(value=value)
        return QueryStringPatternTranslator._escape_value(value)

    @staticmethod
    def _escape_value(value) -> str:
        if isinstance(value, str):
            return '{}'.format(value.replace('\"', '\\"').replace('(', '\\(').replace(')', '\\)'))
        else:
            return value

    @staticmethod
    def _negate_comparison(comparison_string):
        """
        Formatting value in the event of LIKE operation
        :param comparison_string: str
        :return: str
        """
        # split_string = re.split(r"\sOR\s|\sAND\s", comparison_string)
        if ' OR ' in comparison_string:
            con_string = re.sub(r'\(', '(NOT ', comparison_string, 1)
            comparison_string = con_string.replace(' OR ', ' OR NOT ')
        else:
            comparison_string = "NOT " + comparison_string
        return comparison_string

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
                converted_time = int(((datetime.strptime(timestamp, time_pattern) - epoch).total_seconds()) * 1000)
                return converted_time
            except ValueError:
                pass
        raise NotImplementedError("cannot convert the timestamp {} to milliseconds".format(timestamp))

    @staticmethod
    def get_time_stamp(timestamp):
        """
        Formatting the valid timestamp
        :param timestamp: str, timestamp
        :return: str, timestamp
        """
        time_patterns = ['%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S.%fZ']
        for fmt in time_patterns:
            try:
                date_time = datetime.strptime(timestamp, fmt)
                return date_time.strftime('%Y-%m-%dT%H:%M:%SZ')
            except ValueError:
                pass
        raise NotImplementedError("no valid timestamp {} provided".format(timestamp))

    @staticmethod
    def load_json(rel_path_of_file):
        """
        Consumes a json file and returns a dictionary
        :param rel_path_of_file: str, path of json file
        :return: dictionary
        """
        _json_path = path.abspath(path.join(path.join(__file__, ".."), rel_path_of_file))
        if path.exists(_json_path):
            with open(_json_path) as f_obj:
                return json.load(f_obj)
        else:
            raise FileNotFoundError

    def _format_datetime(self, value) -> tuple:
        """
        Formating value in the event of value is datetime
        :param value: datetime value
        :return: list, timestamp in milliseconds or timestamp itself
        """
        values = value.values if hasattr(value, 'values') else [value]
        if self._epoch_time:
            milli_secs_lst = list(map(self.get_epoch_time, values))
            values = tuple(map(lambda x: '{}'.format(str(x)[:-3]), milli_secs_lst))
        else:
            time_stamp_chk = list(map(self.get_time_stamp, values))
            values = tuple(map(lambda x: '{}'.format(str(x)), time_stamp_chk))
        return values if len(values) > 1 else values[0]

    def _protocol_lookup(self, value):
        """
        Function for protocol number lookup
        :param value:str or list, protocol
        :return:str or list, protocol
        """
        value = value.values if hasattr(value, 'values') else value
        protocol_json = self.load_json(PROTOCOL_LOOKUP_JSON_FILE)
        if isinstance(value, list):
            protocol_value = tuple(protocol_json.get(each_value.lower()) for each_value in value if each_value.lower(
                             ) in protocol_json)
        else:
            protocol_value = protocol_json.get(value.lower())
        return protocol_value

    def _protocol_check(self, expression):
        """
        Function for protocol check
        :param expression: expression object, ANTLR parsed expression object
        :return: setvalue or str, existing protocol value
        """
        existing_protocol_value = expression.value
        if self._protocol_lookup_needed:
            # Convert protocol name to protocol numbers for vpc logs
            value = self._protocol_lookup(expression.value)
            if (not value) or (isinstance(value, tuple) and None in value):
                raise NotImplementedError(
                    "Un-supported protocol '{}' for operation '{}' for aws athena '{}' logs".format(
                        expression.value, expression.comparator, path.basename(self.service_type)))
            expression.value = value
        else:
            value = expression.value
            value = value.values if hasattr(value, 'values') else value
            if isinstance(value, list):
                protocol_value = tuple(each_value.upper() for each_value in value)
            else:
                protocol_value = str(value).upper()
            expression.value = protocol_value
        return existing_protocol_value

    def _flatten_list(self, nested_list):
        """
        Flattening the list
        :param nested_list: list, json extract scalar mapped fields list
        :return: object
        """
        for item in nested_list:
            if isinstance(item, Iterable) and not isinstance(item, str):
                for x in self._flatten_list(item):
                    yield x
            else:
                yield item

    def _build_json_extract_fields(self, mapped_fields_array):
        """
        Adding json extract scalar function to the json fields
        :param mapped_fields_array: list, attributes in from stix service type json file
        :return: list, mapped fields array with json extract scalar function
        """
        extract_string_list = list()
        extract_string_dict = self.load_json(GUARDDUTY_CONFIG)['guardduty']['extract_fields']
        for value in mapped_fields_array:
            if value in extract_string_dict.keys():
                # json extract scalar function will be added to each mapped fields
                extract_queries = extract_string_dict[value]['json_extract_query']
                if isinstance(extract_queries, list):
                    extract_string_list.append(["json_extract_scalar({})".format(val) for val in
                                                extract_queries])
                else:
                    extract_string_list.append("json_extract_scalar({})".format(extract_queries))
            else:
                extract_string_list.append(value)
        mapped_fields_array = [val for val in self._flatten_list(extract_string_list)]
        return mapped_fields_array

    def _parse_time_range(self, qualifier, time_range):
        """
        Format the input time range UTC timestamp to Unix time
        :param time_range: int, value available from main.py in options variable
        :return: str, format_string
        """
        try:
            compile_timestamp_regex = re.compile(TIMESTAMP_PATTERN)
            if qualifier and compile_timestamp_regex.search(qualifier):
                if self._epoch_time:
                    time_range_iterator = map(lambda x: int(self.get_epoch_time(x.group()) / 1000),
                                              compile_timestamp_regex.finditer(qualifier))
                    time_range_list = [each for each in time_range_iterator]
                else:
                    time_range_iterator = compile_timestamp_regex.finditer(qualifier)
                    time_range_list = ["'{}'".format(each.group()) for each in time_range_iterator]
            # Default time range Start time = Now - 5 minutes and Stop time  = Now
            else:
                if self._epoch_time:
                    stop_time = datetime.now()
                    start_time = int(round((stop_time - timedelta(minutes=time_range)).timestamp()))
                    stop_time = int(round(stop_time.timestamp()))
                    time_range_list = [start_time, stop_time]
                else:
                    stop_time = datetime.utcnow()
                    go_back_in_minutes = timedelta(minutes=time_range)
                    start_time = stop_time - go_back_in_minutes
                    time_range_list = ["'{}'".format(each)for each in
                                       [start_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z', stop_time.strftime(
                                           '%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z']]
            start_stop_list = [each for each in time_range_list]
            
            if self.service_type == 'guardduty':
                startstopattr = 'updatedat'
            elif self.service_type == 'vpcflow':
                startstopattr = 'start'
            elif self.service_type == 'ocsf':
                startstopattr = 'time'
                start_stop_list[0] = int(start_stop_list[0]*1000)
                start_stop_list[1] = int(start_stop_list[1]*1000)

            qualifier_string = "AND {datetime_field} BETWEEN {start} AND " \
                               "{stoptime}".format(datetime_field=startstopattr,
                                                   start=start_stop_list[0],
                                                   stoptime=start_stop_list[1])
            return qualifier_string
        except (KeyError, IndexError, TypeError) as e:
            raise e

    @staticmethod
    def _parse_mapped_fields(expression, value, comparator, mapped_fields_array, service_type):
        """
        Mapping the stix object with their corresponding property, from stix service type json will be used for
        mapping
        :param expression: expression object, ANTLR parsed expression object
        :param value: str
        :param comparator: str
        :param mapped_fields_array: list, attributes in from stix service type json file
        :return: str, filter condition will be constructed
        """
        comparison_string = ""
        mapped_fields_count = len(mapped_fields_array)
        digit_chk = False
        alpha_chk = False
        if isinstance(value, tuple):
            digit_chk = all([True if val.isdigit() else False for val in value])
            alpha_chk = all([True if val.isalpha() else False for val in value])
            if alpha_chk:
                values = tuple(map(lambda x: "lower('{}')".format(x), value))
                value = "({value})".format(value=','.join(values))
        for mapped_field in mapped_fields_array:

            # Format UNNEST columns
            if service_type in ARRAY_TYPE_COLUMNS:
                for column_name, column in ARRAY_TYPE_COLUMNS[service_type].items():
                    if mapped_field.startswith(column_name):
                        mapped_field = '##' + column['from'] + '##' + mapped_field.replace(column_name, column['where'])
                        break
                    
            if (expression.comparator == ComparisonComparators.In and digit_chk) or \
                    (expression.comparator in [ComparisonComparators.Equal, ComparisonComparators.NotEqual,
                                               ComparisonComparators.Like] and str(value).isdigit()) or (
                    expression.comparator == ComparisonComparators.Like and '%' in str(value) or '_' in str(value)):
                comparison_string += "CAST({mapped_field} AS varchar) {comparator} " \
                                     "{value}".format(mapped_field=mapped_field, comparator=comparator,
                                                      value="'{}'".format(value) if not isinstance(value, tuple)
                                                      else "('{}')".format(value[0]) if len(value) == 1 else value)
            elif expression.comparator == ComparisonComparators.Matches:
                comparison_string += "{comparator}(CAST({mapped_field} as varchar), '{value}')".format(
                    comparator=comparator, mapped_field=mapped_field, value=value)
            elif expression.comparator in [ComparisonComparators.GreaterThan, ComparisonComparators.GreaterThanOrEqual,
                                           ComparisonComparators.LessThan,
                                           ComparisonComparators.LessThanOrEqual] and str(value).isdigit():
                comparison_string += "CAST({mapped_field} as REAL) {comparator} {value}".format(
                    mapped_field=mapped_field, comparator=comparator, value=value)
            elif expression.comparator == ComparisonComparators.In:
                comparison_string += "{mapped_field} {comparator} {value}".format(mapped_field="lower({})".format(
                    mapped_field) if alpha_chk else mapped_field, comparator=comparator,
                    value=value if len(value) > 1 else "('{}')".format(value[0]))
            else:
                comparison_string += "lower({mapped_field}) {comparator} lower('{value}')".format(
                                      mapped_field=mapped_field, comparator=comparator,
                                      value=value)
            if mapped_fields_count > 1:
                comparison_string += " OR "
                mapped_fields_count -= 1
        return comparison_string

    @staticmethod
    def _lookup_comparison_operator(self, expression_operator):
        """
        Look up for comparison operators
        :param self: object
        :param expression_operator: operator, ANTLR expression operator
        :return: operator, SQL operator
        """
        if str(expression_operator) not in self.comparator_lookup:
            raise NotImplementedError("Comparison operator {} unsupported for AWS Athena connector".format
                                      (expression_operator.name))
        return self.comparator_lookup[str(expression_operator)]

    def _parse_expression(self, expression, qualifier=None) -> str:
        """
        Constructing SQL by parsing the expression object
        :param expression: expression object, ANTLR parsed expression object
        :param qualifier: str, default in None
        :return:str, SQL where condition
        """
        if isinstance(expression, ComparisonExpression):  # Base Case
            comparison_string = self.__eval_comparison_exp(expression)
            if expression.negated:
                comparison_string = self._negate_comparison(comparison_string)
                return "{}".format(comparison_string)
            return comparison_string
        elif isinstance(expression, CombinedComparisonExpression):
            operator = self._lookup_comparison_operator(self, expression.operator)
            expression_01 = self._parse_expression(expression.expr1)
            expression_02 = self._parse_expression(expression.expr2)
            if not expression_01 or not expression_02:
                query_string = ""
            else:
                query_string = "({} {} {})".format(expression_01, operator, expression_02)
            return query_string
        elif isinstance(expression, ObservationExpression):
            select_query = self.__eval_observation_exp(expression, qualifier)
            return select_query
        elif isinstance(expression, CombinedObservationExpression):
            return self.__eval_comb_observation_exp(expression, qualifier)
        elif isinstance(expression, StartStopQualifier):
            if hasattr(expression, 'observation_expression'):
                return self._parse_expression(getattr(expression, 'observation_expression'), expression.qualifier)
        elif isinstance(expression, Pattern):
            return "{expr}".format(expr=self._parse_expression(expression.expression))
        else:
            raise RuntimeError("Unknown Recursion Case for expression={}, type(expression)={}".format(
                expression, type(expression)))

    def __eval_observation_exp(self, expression, qualifier):
        """
        Parsing observation expression
        :param expression: expression object
        :param qualifier: qualifier
        :return: str
        """
        select_query = ''
        self.qualifier_string = self._parse_time_range(qualifier, self._time_range)
        con_query = self._parse_expression(expression.comparison_expression, qualifier)
        if con_query:
            select_query = "{con_query} {qualifier_string}".format(con_query=con_query,
                                                                   qualifier_string=self.qualifier_string)
        return select_query

    def __eval_comparison_exp(self, expression):
        """
        Parsing comparison expression
        :param expression: expression object
        :return: str, comparison string
        """
        # Resolve STIX Object Path to a field in the target Data Model
        stix_object, stix_field = expression.object_path.split(':')
        # Multiple data source fields may map to the same STIX Object
        existing_protocol_value = None
        if stix_field.lower() == 'protocols[*]':
            existing_protocol_value = self._protocol_check(expression)
        mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
        if self.service_type == 'guardduty':
            mapped_fields_array = self._build_json_extract_fields(mapped_fields_array)
        # Resolve the comparison symbol to use in the query string (usually just ':')
        comparator = self._lookup_comparison_operator(self, expression.comparator)
        comparison_string = self.__eval_comparison_value(comparator, expression, mapped_fields_array, stix_field)
        if stix_field.lower() == 'protocols[*]':
            expression.value = existing_protocol_value
        if len(mapped_fields_array) > 1:
            # More than one data source field maps to the STIX attribute, so group comparisons together.
            grouped_comparison_string = "(" + comparison_string + ")"
            comparison_string = grouped_comparison_string
        return comparison_string

    def __eval_comb_observation_exp(self, expression, qualifier):
        """
        Parsing combined observation expression
        :param expression: expression object
        :param qualifier: qualifier
        :return: str
        """
        operator = self._lookup_comparison_operator(self, expression.operator)
        expression_01 = self._parse_expression(expression.expr1, qualifier)
        expression_02 = self._parse_expression(expression.expr2, qualifier)
        if expression_01 and expression_02:
            return "({}) {} ({})".format(expression_01, operator, expression_02)
        elif expression_01:
            return "{}".format(expression_01)
        elif expression_02:
            return "{}".format(expression_02)
        else:
            return ''

    def __eval_comparison_value(self, comparator, expression, mapped_fields_array, stix_field):
        """
        Parsing comparison expression
        :param comparator:
        :param expression: expression object, ANTLR parsed expression object
        :param mapped_fields_array: list, values available in from stix service type json file
        :param stix_field: str, stix field
        :return: str, comparison string
        """
        # for the datetime value
        if stix_field in ['start', 'end']:
            value = self._format_datetime(expression.value)
            if expression.comparator == ComparisonComparators.In and isinstance(value, str):
                if self._epoch_time:
                    value = "({})".format(value)
                else:
                    value = "('{}')".format(value)
        elif expression.comparator == ComparisonComparators.Matches:
            value = self._format_match(expression.value)
        # should be (x, y, z, ...)
        elif expression.comparator == ComparisonComparators.In:
            value = self._format_set(expression.value)
        elif expression.comparator == ComparisonComparators.Equal or expression.comparator == ComparisonComparators \
                .NotEqual:
            value = self._format_equality(expression.value)
        # '%' , '_' wildcards can be used
        elif expression.comparator == ComparisonComparators.Like:
            value = self._format_like(expression.value)
        else:
            value = expression.value
        comparison_string = self._parse_mapped_fields(expression, value, comparator, mapped_fields_array, self.service_type)
        return comparison_string

    def parse_expression(self, pattern: Pattern):
        return self._parse_expression(pattern)


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    """
    Conversion of expression object to AWS Athena SQL query
    :param pattern: expression object, ANTLR parsed expression object
    :param data_model_mapping: DataMapper object, mapping object obtained by parsing json
    :param options: dict, time_range defaults to 5 and result_limit defaults to 10000
    :return: dict, AWS Athena SQL query
    """
    time_range = options['time_range']
    query = QueryStringPatternTranslator(pattern, data_model_mapping, time_range)
    query_string = "({condition})".format(condition=query.translated)
    return [{query.service_type: query_string}]
