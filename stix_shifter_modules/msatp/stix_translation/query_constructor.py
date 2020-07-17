from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators, StartStopQualifier
from datetime import datetime, timedelta
import re

START_STOP_PATTERN = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z)"
DS_INT_FIELDS = ["InitiatingProcessParentId", "InitiatingProcessId", "ProcessId", "LocalPort", "RemotePort"]
DS_DATETIME_FIELD = ["InitiatingProcessCreationTime", "InitiatingProcessParentCreationTime", "ProcessCreationTime"]
MAC = '(([0-9a-fA-F]{0,2}[:-]){1,5}([0-9a-fA-F]{0,2}))'
FLOOR_TIME = '| extend FormattedTimeKey = bin(EventTime, 1m)'


class QueryStringPatternTranslator:
    """
    Stix to kusto query translation
    """
    comparator_lookup = {
        ComparisonExpressionOperators.And: "and",
        ComparisonExpressionOperators.Or: "or",
        ComparisonComparators.Equal: "==",
        ComparisonComparators.NotEqual: "!=",
        ComparisonComparators.Like: "contains",
        ComparisonComparators.Matches: "matches",
        ComparisonComparators.GreaterThan: ">",
        ComparisonComparators.GreaterThanOrEqual: ">=",
        ComparisonComparators.LessThan: "<",
        ComparisonComparators.LessThanOrEqual: "<=",
        ComparisonComparators.In: "in~",
        ObservationOperators.Or: 'OR',
        ObservationOperators.And: 'OR'
    }
    # STIX attribute to MSATP table mapping
    msatp_lookup_table = {"file": "FileCreationEvents",
                          "process": "ProcessCreationEvents",
                          "user-account": "ProcessCreationEvents",
                          "ipv4-addr": "NetworkCommunicationEvents",
                          "ipv6-addr": "NetworkCommunicationEvents",
                          "network-traffic": "NetworkCommunicationEvents",
                          "url": "NetworkCommunicationEvents",
                          "windows-registry-key": "RegistryEvents",
                          "x-msatp": "FileCreationEvents",
                          "directory": "FileCreationEvents"
                          }
    # Join query to get MAC address value from MachineNetworkInfo
    join_query = ' | join kind= inner (MachineNetworkInfo {qualifier_string}{floor_time}| mvexpand parse_json(' \
                 'IPAddresses) | extend IP = IPAddresses.IPAddress | project EventTime ,MachineId , MacAddress, IP, ' \
                 'FormattedTimeKey) on MachineId, $left.FormattedTimeKey ' \
                 '== $right.FormattedTimeKey | where LocalIP == IP | where {mac_query} | order by EventTime desc'

    def __init__(self, pattern: Pattern, data_model_mapper, time_range):
        self.dmm = data_model_mapper
        self._time_range = time_range
        self.qualified_queries = []
        self.qualifier_string = ''
        self.lookup_table_object = None
        self.lookup_table = None
        self._is_mac = None
        self.parse_expression(pattern)

    @staticmethod
    def _format_equality(value, comparator) -> str:
        """
        Formatting value in the event of equality operation
        :param value: str
        :return: str
        """
        if isinstance(value, str):
            if comparator == '==':
                comparator = '=~'
            elif comparator == '!=':
                comparator = '!~'
        return '"{}"'.format(value), comparator

    @staticmethod
    def _format_set(value) -> str:
        """
        Formatting list of values in the event of IN operation
        :param values: str
        :return: list
        """
        final_value = []
        for val in value.values:
            final_value.append('"{}"'.format(val))
        return '{}'.format(str(final_value).replace('[', '(').replace(']', ')').replace("'", ""))

    @staticmethod
    def _format_like(value, comparator) -> str:
        """
        Formatting value in the event of LIKE operation
        :param value: str
        :return: str
        """
        # Replacing value with % to .* and _ to . for supporting Like comparator
        compile_regex = re.compile(r'.*(\%|\_).*')
        if compile_regex.match(value):
            if comparator == 'contains':
                comparator = 'matches'
            return 'regex"({}$)"'.format(value.replace('%', '.*').replace('_', '.')), comparator
        return '"{}"'.format(value), comparator

    @staticmethod
    def _format_matches(value) -> str:
        """
        Formatting value in the event of MATCHES operation
        :param value: str
        :return: str
        """
        return 'regex"({})"'.format(value)

    @staticmethod
    def _format_datetime(value, expression) -> str:
        """
        Formating value in the event of value is datetime
        :param value:
        :return:
        """
        if expression.comparator == ComparisonComparators.In:
            final_value = []
            for val in value.values:
                final_value.append('{}'.format('datetime({})'.format(val)))
            return '{}'.format(str(final_value).replace('[', '(').replace(']', ')').replace("'", ""))
        elif expression.comparator == ComparisonComparators.Matches:
            return 'regex"({})"'.format(value)
        return 'datetime({})'.format(value)

    @staticmethod
    def _negate_comparison(comparison_string):
        return "(not ({}))".format(comparison_string)

    @staticmethod
    def _check_value_type(value, expression):
        """
        Function returning value type 'mac'
        :param value: str
        :return: list
        """
        mac_objects = ['src_ref.value', 'mac-addr']
        stix_object, stix_field = expression.object_path.split(':')
        compile_mac_regex = re.compile(MAC)
        value = list(map(str, value)) if isinstance(value, list) else [str(value)]
        value_type = []
        if stix_object in mac_objects or stix_field in mac_objects:
            for each in value:
                if compile_mac_regex.search(each):
                    value_type.append('mac')
        return value_type

    @staticmethod
    def _parse_time_range(qualifier, time_range):
        """
        :param qualifier: str, input time range i.e START t'2019-04-10T08:43:10.003Z' STOP t'2019-04-20T10:43:10.003Z'
        :param time_range: int, value available from main.py in options variable
        :return: str, format_string bound with time range provided
        """
        try:
            compile_timestamp_regex = re.compile(START_STOP_PATTERN)
            mapped_field = "EventTime"
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

            value = ('{mapped_field} >= datetime({start_time}) and {mapped_field} < datetime({stop_time}) '
                     ).format(mapped_field=mapped_field, start_time=time_range_list[0], stop_time=time_range_list[1])
            format_string = ' where {value}'.format(value=value)

        except (KeyError, IndexError, TypeError) as e:
            raise e
        return format_string

    @staticmethod
    def _parse_mapped_fields(expression, value, comparator, mapped_fields_array):
        """
        Mapping the stix object property with their corresponding property, from_stix_map.json will be used for mapping
        :param expression: expression object, ANTLR parsed expression object
        :param value: str
        :param comparator: str
        :param mapped_fields_array: list, Mapping available in from_stix_map.json
        :return: str, where condition will be constructed for value
        """
        comparison_string = ""
        is_int_field = False
        is_date_field = False
        for index_of_field, map_field in enumerate(mapped_fields_array):
            mapped_field = map_field.split('.')[1]
            if mapped_field == 'MacAddress':
                mapped_field = '{}'.format(mapped_field)
                value = '{}'.format(value).replace(':', '').replace('-', '')
            if mapped_field in DS_DATETIME_FIELD:
                is_date_field = True
            if mapped_field in DS_INT_FIELDS:
                is_int_field = True
            # changing mapped field to 'tostring(mapped_field)' for datetime values
            if expression.comparator in [ComparisonComparators.Like, ComparisonComparators.Matches,
                                         ComparisonComparators.Equal, ComparisonComparators.NotEqual]:
                if is_int_field or is_date_field:
                    mapped_field = 'tostring({mapped_field})'.format(mapped_field=mapped_field)
            elif expression.comparator in [ComparisonComparators.GreaterThan, ComparisonComparators.GreaterThanOrEqual,
                                           ComparisonComparators.LessThan,
                                           ComparisonComparators.LessThanOrEqual]:
                if not is_int_field and not is_date_field:
                    raise NotImplementedError(
                        "Comparison operator {} unsupported for MSATP attribute {}".format(comparator, mapped_field))

            comparison_string += '{mapped_field} {comparator} {value}'.format(mapped_field=mapped_field,
                                                                              comparator=comparator, value=value)
            if index_of_field < len(mapped_fields_array) - 1:
                comparison_string += " or "
        return comparison_string

    @staticmethod
    def clean_format_string(format_string):
        """
        Formats and replaces carriage return(\r), newline character(\n), spaces > 2, tab with 1 space
        :param format_string: str
        :return: str
        """
        return re.sub(r'\r|\n|\s{2,}|\t', ' ', format_string)

    def get_lookup_table_of_obs_exp(self, expression, lookup_table, objects_dict):
        """
        Function to parse observation expression and return the object(i.e FileCreationEvents
        , ProcessCreationEvents, NetworkCommunicationEvents, RegistryEvents) involved
        :param expression: expression object, ANTLR parsed expression object
        :param lookup_table: list, empty list
        :param objects_dict: dict, dictionary of objects as keys and respective fields as values
        :return: None
        """

        if hasattr(expression, 'object_path'):
            stix_object = expression.object_path.split(':')[0]
            value = expression.value.values if hasattr(expression.value, 'values') else expression.value
            value_type = self._check_value_type(value, expression)
            if 'mac' in value_type:
                self._is_mac = True
            lookup_table.append(objects_dict.get(stix_object))
            final_lookup = list(set(lookup_table))
            if self._is_mac:
                self.lookup_table_object = 'NetworkCommunicationEvents'
            else:
                if len(final_lookup) == 1:
                    self.lookup_table_object = final_lookup[0]
                elif 'NetworkCommunicationEvents' in final_lookup:
                    self.lookup_table_object = 'NetworkCommunicationEvents'
                elif 'RegistryEvents' in final_lookup:
                    self.lookup_table_object = 'RegistryEvents'
                elif 'ProcessCreationEvents' in final_lookup:
                    self.lookup_table_object = 'ProcessCreationEvents'

        else:
            self.get_lookup_table_of_obs_exp(expression.expr1, lookup_table, objects_dict)
            self.get_lookup_table_of_obs_exp(expression.expr2, lookup_table, objects_dict)

    def _lookup_comparison_operator(self, expression_operator):
        """
        Comparison operator lookup with error handling for un-supported operators
        :param expression_operator: str
        :return: str
        """
        if expression_operator not in self.comparator_lookup:
            raise NotImplementedError(
                "Comparison operator {} unsupported for MSATP connector".format(expression_operator.name))
        return self.comparator_lookup.get(expression_operator)

    def _parse_expression(self, expression, qualifier=None):
        """
        Complete formation of Kusto query from ANTLR expression object
        :param expression: expression object, ANTLR parsed expression object
        :param qualifier: str, default in None
        :return: None or kusto query as the method call is recursive
        """
        if isinstance(expression, ComparisonExpression):  # Base Case
            return self.__eval_comparison_exp(expression)
        elif isinstance(expression, CombinedComparisonExpression):
            operator = self._lookup_comparison_operator(expression.operator)
            expression_01 = self._parse_expression(expression.expr1)
            expression_02 = self._parse_expression(expression.expr2)
            if not expression_01:
                kusto_query = "{}".format(expression_02)
            elif not expression_02:
                kusto_query = "{}".format(expression_01)
            else:
                return "({}) {} ({})".format(expression_01, operator, expression_02)
            return kusto_query
        elif isinstance(expression, ObservationExpression):
            kusto_query = self.__eval_observation_exp(expression, qualifier)
            final_comparison_exp = '({})'.format(kusto_query)
            self.qualified_queries.append(final_comparison_exp)
            return None
        elif isinstance(expression, CombinedObservationExpression):
            self._parse_expression(expression.expr1, qualifier)
            self._parse_expression(expression.expr2, qualifier)
            return None
        elif isinstance(expression, StartStopQualifier):
            if hasattr(expression, 'observation_expression'):
                return self._parse_expression(getattr(expression, 'observation_expression'), expression.qualifier)
        elif isinstance(expression, Pattern):
            return self._parse_expression(expression.expression)
        else:
            raise RuntimeError("Unknown Recursion Case for expression={}, type(expression)={}".format(
                expression, type(expression)))

    def __eval_observation_exp(self, expression, qualifier):
        """
        Function for parsing observation expression value
        :param expression: expression object
        :param qualifier: qualifier
        :return:
        """
        self._is_mac = False
        self.lookup_table = []
        self.get_lookup_table_of_obs_exp(expression.comparison_expression, self.lookup_table,
                                         self.msatp_lookup_table)
        kusto_query = self._parse_expression(expression.comparison_expression)
        self.qualifier_string = self._parse_time_range(qualifier, self._time_range)
        self.qualifier_string = self.clean_format_string(self.qualifier_string)
        self.lookup_table_object = 'find withsource = TableName in ({})'.format(self.lookup_table_object)
        if self._is_mac:
            kusto_query = self.lookup_table_object + self.qualifier_string + FLOOR_TIME + \
                self.join_query.format(mac_query=kusto_query, qualifier_string='|' + self.qualifier_string,
                                       floor_time=FLOOR_TIME)
        else:
            kusto_query = self.lookup_table_object + self.qualifier_string + '| order by EventTime desc | ' \
                                                                             'where ' + kusto_query
        return kusto_query

    def parse_expression(self, pattern: Pattern):
        """
        parse_expression --> Kusto query
        :param pattern: expression object, ANTLR parsed expression object
        :return:str, Kusto query(native query)
        """
        return self._parse_expression(pattern)

    def __eval_comparison_value(self, expression, comparator):
        """
        Function for parsing comparison expression value
        :param expression: expression object, stix_object, stix_field, comparator
        :return: formatted expression value and comparator
        """
        if expression.comparator == ComparisonComparators.In:
            value = self._format_set(expression.value)
        elif expression.comparator in [ComparisonComparators.Equal, ComparisonComparators.NotEqual]:
            value, comparator = self._format_equality(expression.value, comparator)
        elif expression.comparator in [ComparisonComparators.GreaterThan, ComparisonComparators.GreaterThanOrEqual,
                                       ComparisonComparators.LessThan,
                                       ComparisonComparators.LessThanOrEqual]:
            value = expression.value
        elif expression.comparator == ComparisonComparators.Like:
            value, comparator = self._format_like(expression.value, comparator)
        else:
            if expression.comparator == ComparisonComparators.Matches:
                value = self._format_matches(expression.value)
        return value, comparator

    def __eval_comparison_exp(self, expression):
        """
        Function for parsing comparsion expression and returning query
        :param expression: expression object, ANTLR parsed expression object
        :return: str, query string for the comparison expression
        """
        stix_object, stix_field = expression.object_path.split(':')
        value = expression.value.values if hasattr(expression.value, 'values') else expression.value
        value_type = self._check_value_type(value, expression)
        mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
        mapped_list = [fields for fields in mapped_fields_array if fields.split('.')[0] == self.lookup_table_object]
        mapped_mac_list = [fields for fields in mapped_fields_array if fields.split('.')[0] == 'MachineNetworkInfo'
                           and 'mac' in value_type]
        # raise ValueError as the Stix object are not matching in the observation
        if not mapped_list and not mapped_mac_list:
            raise ValueError("STIX_objects is not mapping with lookup table attributes")
        comparator = self._lookup_comparison_operator(expression.comparator)
        mapped_from_stix_list = mapped_mac_list if mapped_mac_list else mapped_list
        if stix_field == 'created':
            value = self._format_datetime(expression.value, expression)
        elif 'path' in stix_field:
            if comparator == self.comparator_lookup.get(ComparisonComparators.Like):
                value, comparator = self._format_like(expression.value, comparator)
            else:
                raise TypeError("Comparator {comparator} unsupported for Directory Path, use only LIKE operator"
                                .format(comparator=comparator))
        else:
            value, comparator = self.__eval_comparison_value(expression, comparator)
        comparison_string = self._parse_mapped_fields(expression, value, comparator,
                                                      mapped_from_stix_list)
        if expression.negated:
            comparison_string = self._negate_comparison(comparison_string)
        comparison_string = self.clean_format_string(comparison_string)
        return "{}".format(comparison_string)


def translate_pattern(pattern: Pattern, data_model_mapper, options):
    """
    Conversion of expression object to kusto query
    :param pattern: expression object, ANTLR parsed expression object
    :param data_model_mapper: DataMapper object, mapping object obtained by parsing from_stix_map.json
    :param options: dict,time_range defaults to 5
    :return: str, kusto query
    """
    time_range = options['time_range']
    translated_dictionary = QueryStringPatternTranslator(pattern, data_model_mapper, time_range)
    translated_query = translated_dictionary.qualified_queries
    if len(translated_query) > 1:
        # Query formation for multiple observation expression
        final_query = ['union {}'.format(','.join(translated_query))]
    else:
        # Query formation for single observation expression
        final_query = translated_query
    return final_query
