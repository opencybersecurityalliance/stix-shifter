from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, \
    ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators, StartStopQualifier
from datetime import datetime, timedelta
import re

START_STOP_PATTERN = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z)"
DS_INT_FIELDS = ["InitiatingProcessParentId", "InitiatingProcessId", "ProcessId", "LocalPort", "RemotePort"]
DS_DATETIME_FIELD = ["InitiatingProcessCreationTime", "InitiatingProcessParentCreationTime", "ProcessCreationTime"]
MAC = '(([0-9a-fA-F]{0,2}[:-]){1,5}([0-9a-fA-F]{0,2}))'
FLOOR_TIME = '| extend FormattedTimeKey = bin(Timestamp, 1m)'


class QueryStringPatternTranslator:
    """
    Stix to kusto query translation
    """
    # Join query to get MAC address value from DeviceNetworkInfo
    join_query = ' | join kind= inner (DeviceNetworkInfo {qualifier_string}{floor_time}| mvexpand parse_json(' \
                 'IPAddresses) | extend IP = IPAddresses.IPAddress | project Timestamp ,DeviceId , MacAddress, IP, ' \
                 'FormattedTimeKey) on DeviceId, $left.FormattedTimeKey ' \
                 '== $right.FormattedTimeKey | where LocalIP == IP | where {mac_query} | order by Timestamp desc'

    def __init__(self, pattern: Pattern, data_model_mapper, time_range):
        self.dmm = data_model_mapper
        self.comparator_lookup = self.dmm.map_comparator()
        self._time_range = time_range
        self.qualified_queries = []
        self.qualifier_string = ''
        self.lookup_table_object = None
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
        return "not ({})".format(comparison_string)

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
            mapped_field = "Timestamp"
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
        add_parenthesis = False
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

            curr_comparison_string = '{mapped_field} {comparator} {value}'.format(mapped_field=mapped_field,
                                                                                  comparator=comparator, value=value)
            if index_of_field < len(mapped_fields_array) - 1:
                curr_comparison_string = '({}) or '.format(curr_comparison_string)
                add_parenthesis = True

            elif add_parenthesis:
                curr_comparison_string = '({})'.format(curr_comparison_string)

            comparison_string += curr_comparison_string

        return comparison_string

    @staticmethod
    def clean_format_string(format_string):
        """
        Formats and replaces carriage return(\r), newline character(\n), spaces > 2, tab with 1 space
        :param format_string: str
        :return: str
        """
        return re.sub(r'\r|\n|\s{2,}|\t', ' ', format_string)

    def _lookup_comparison_operator(self, expression_operator):
        """
        Comparison operator lookup with error handling for un-supported operators
        :param expression_operator: str
        :return: str
        """
        if str(expression_operator) not in self.comparator_lookup:
            raise NotImplementedError(
                "Comparison operator {} unsupported for MSATP connector".format(expression_operator.name))
        return self.comparator_lookup.get(str(expression_operator))

    # get atomicQuery, map the query to tables
    def __eval_comparison_exp_map(self, expression):
        stix_object, stix_field = expression.object_path.split(':')
        comparator = self._lookup_comparison_operator(expression.comparator)
        if stix_field == 'created':
            value = self._format_datetime(expression.value, expression)
        elif 'path' in stix_field:
            if comparator == self.comparator_lookup.get("ComparisonComparators.Like"):
                value, comparator = self._format_like(expression.value, comparator)
            else:
                raise TypeError("Comparator {comparator} unsupported for Directory Path, use only LIKE operator"
                                .format(comparator=comparator))
        else:
            value, comparator = self.__eval_comparison_value(expression, comparator)
        mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
        map_tables_to_fields = {}
        for field in mapped_fields_array:
            curr_table = field.split('.')[0]
            if map_tables_to_fields.get(curr_table):
                map_tables_to_fields[curr_table].append(field)
            else:
                map_tables_to_fields[curr_table] = [field]

        map_tables_to_queries = {}
        for table in map_tables_to_fields:
            map_tables_to_queries[table] = self._parse_mapped_fields(expression, value,
                                                                     comparator, map_tables_to_fields[table])
            if expression.negated:
                comparison_string = self._negate_comparison(map_tables_to_queries[table])
                comparison_string = self.clean_format_string(comparison_string)
                map_tables_to_queries[table] = comparison_string

        return map_tables_to_queries

    @staticmethod
    def mergeDict(dict1, dict2):
        """ Merge dictionaries and keep values of common keys in list"""
        dict3 = {**dict1, **dict2}
        for key, value in dict3.items():
            if key in dict1 and key in dict2:
                dict3[key] = [value, dict1[key]]
        return dict3

    def _parse_expression(self, expression, qualifier=None):
        """
        Complete formation of Kusto query from ANTLR expression object
        :param expression: expression object, ANTLR parsed expression object
        :param qualifier: str, default in None
        :return: None or kusto query as the method call is recursive
        """
        if isinstance(expression, ComparisonExpression):  # Base Case
            return self.__eval_comparison_exp_map(expression)
        elif isinstance(expression, CombinedComparisonExpression) or \
                isinstance(expression, CombinedObservationExpression):
            operator = self._lookup_comparison_operator(expression.operator)
            exp_map_01 = self._parse_expression(expression.expr1)
            exp_map_02 = self._parse_expression(expression.expr2)
            if not exp_map_01:
                kusto_query_map = exp_map_02
            elif not exp_map_02:
                kusto_query_map = exp_map_01
            else:
                if (operator == 'and'):
                    kusto_query_map = QueryStringPatternTranslator.construct_and_op_map(exp_map_01, exp_map_02)

                else:
                    kusto_query_map = QueryStringPatternTranslator.construct_op_map(exp_map_01, exp_map_02, operator)

            return kusto_query_map

        elif isinstance(expression, ObservationExpression):
            self.qualifier_string = self._parse_time_range(qualifier, self._time_range)
            self.qualifier_string = self.clean_format_string(self.qualifier_string)
            return self._parse_expression(expression.comparison_expression, qualifier)

        elif isinstance(expression, StartStopQualifier):
            if hasattr(expression, 'observation_expression'):
                return self._parse_expression(getattr(expression, 'observation_expression'), expression.qualifier)

        elif isinstance(expression, Pattern):
            return self._parse_expression(expression.expression)
        else:
            raise RuntimeError("Unknown Recursion Case for expression={}, type(expression)={}".format(
                expression, type(expression)))

    @staticmethod
    def construct_op_map(exp_map_01, exp_map_02, operator):
        merged_map = QueryStringPatternTranslator.mergeDict(exp_map_01, exp_map_02)

        for table in merged_map:
            if (isinstance(merged_map[table], list) and len(merged_map[table])) > 1:
                merged_query = '{}'.format(list(merged_map[table])[0])
                for query in merged_map[table][1:]:
                    merged_query = '({}) {} ({})'.format(merged_query, operator, query)
                merged_map[table] = merged_query

            else:
                merged_map[table] = '({})'.format(merged_map[table])

        return merged_map

    @staticmethod
    def construct_and_op_map(exp_map_01, exp_map_02):
        merged_map = QueryStringPatternTranslator.construct_intesec_map(exp_map_01, exp_map_02)
        for table in merged_map:
            if (len(merged_map[table])) > 1:
                merged_query = '({})'.format(list(merged_map[table])[0])
                for query in merged_map[table][1:]:
                    merged_map[table] = merged_query + ' and ({})'.format(query)

        return merged_map

    @staticmethod
    def construct_intesec_map(exp_map_01, exp_map_02):
        intesec_tables = [table for table in exp_map_01.keys() if table in exp_map_02.keys()]
        dict_01 = {table: exp_map_01[table] for table in intesec_tables}
        dict_02 = {table: exp_map_02[table] for table in intesec_tables}
        return QueryStringPatternTranslator.mergeDict(dict_01, dict_02)

    def construct_query_from_map(self, map_kusto_query):
        for table in map_kusto_query:
            curr_query = '(find withsource = TableName in ({}) {} | order by Timestamp desc | where {})' \
                .format(table, self.qualifier_string, map_kusto_query[table])
            self.qualified_queries.append(curr_query)

    def parse_expression(self, pattern: Pattern):
        """
        parse_expression --> Kusto query
        :param pattern: expression object, ANTLR parsed expression object
        :return:str, Kusto query(native query)
        """
        map_kusto_query = self._parse_expression(pattern)
        self.construct_query_from_map(map_kusto_query)

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
