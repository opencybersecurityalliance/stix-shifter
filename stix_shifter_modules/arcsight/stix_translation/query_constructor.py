from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, \
    ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators, StartStopQualifier
from stix_shifter_utils.stix_translation.src.patterns.errors import SearchFeatureNotSupportedError
from datetime import datetime, timedelta
import re
import json

START_STOP_PATTERN = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z)"
# timestamp format check for data source
ISO_8601_PATTERN = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([' \
                   r'0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$ '
MAC = r'(([0-9a-fA-F]{0,2}[:-]){1,5}([0-9a-fA-F]{0,2}))'
IP_ADDRESS = r'((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){1,3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'


# update this lookup for long-int type fields in arcsight logger
INTEGER_LOOKUP_FIELDS = ["sourcePort", "destinationPort", "priority", "startTime", "endTime", "baseEventCount",
                         "eventId", "sourceMacAddress", "destinationMacAddress"]


class QueryStringPatternTranslator:
    # Change comparator values to match with supported data source operators
    comparator_lookup = {
        ComparisonExpressionOperators.And: "AND",
        ComparisonExpressionOperators.Or: "OR",
        ComparisonComparators.GreaterThan: ">",
        ComparisonComparators.GreaterThanOrEqual: ">=",
        ComparisonComparators.LessThan: "<",
        ComparisonComparators.LessThanOrEqual: "<=",
        ComparisonComparators.Equal: "=",
        ComparisonComparators.NotEqual: "!=",
        ComparisonComparators.Like: "=",
        ComparisonComparators.In: "IN",
        # due to limited regex support "Matches" is treated as CONTAINS
        ComparisonComparators.Matches: 'CONTAINS',
        ComparisonComparators.IsSubSet: 'insubnet',
        ObservationOperators.Or: 'OR',
        ObservationOperators.And: 'AND'
    }
    arcsight_operator_lookup = {
        ComparisonComparators.Equal: "IS NULL",
        ComparisonComparators.NotEqual: "IS NOT NULL"
    }

    def __init__(self, pattern: Pattern, data_model_mapper, time_range):
        self.dmm = data_model_mapper
        self._time_range = time_range
        self.qualifier_list = list()
        self.qualified_queries = list()
        self.pattern = pattern
        self.translated = self.parse_expression(pattern)

    @staticmethod
    def _format_set(values) -> str:
        value_list = values.values
        value_list = json.dumps(value_list)

        return value_list

    @staticmethod
    def _format_equality(value) -> str:
        return '\'{}\''.format(value)

    @staticmethod
    def _format_single_quotes(value) -> str:
        return '{}'.format(value.replace('\'', ''))

    @staticmethod
    def _format_double_quotes(value) -> str:
        return '\"{}\"'.format(value)

    @staticmethod
    def _format_like(value) -> str:
        value = "'{}'".format(value.replace('%', '*'))
        return value

    @staticmethod
    def _negate_comparison(comparison_string):
        return "NOT {}".format(comparison_string)

    @staticmethod
    def _escape_value(value) -> str:
        # check for spaces and formatting of path based values to suit arcsight querying support
        if '\\*' in value:
            value = value.replace('\\*', '*')

        if '*' in value:
            value = value.replace('\\', '\\\\\\\\')
        elif isinstance(value, str):
            value = value.replace('\\', '\\\\')

        if bool(re.search(r"\s", value)):
            return '\"{}\"'.format(value)
        else:
            return '{}'.format(value)

    @staticmethod
    def _check_value_type(value, expression, mapped_fields_array):
        """
        Function returning value type 'mac'
        :param value: str
        :return: list
        """
        ref_objects = ['src_ref.value', 'dst_ref.value']
        stix_object, stix_field = expression.object_path.split(':')
        compile_mac_regex = re.compile(MAC)
        compile_ip_regex = re.compile(IP_ADDRESS)
        value = list(map(str, value)) if isinstance(value, list) else [str(value)]
        res = value[0].strip('][').split(', ')
        value_type = []
        if stix_object in ref_objects or stix_field in ref_objects:
            for each in res:
                if compile_mac_regex.search(each):
                    value_type.append('mac')
                if compile_ip_regex.search(each):
                    value_type.append('ip')

            if 'mac' in value_type and 'ip' in value_type:
                raise SearchFeatureNotSupportedError("Search not supported for a combination of ipaddress and "
                                                     "macaddress values")
            elif 'mac' in value_type:
                # condition to remove the IP related fields
                del mapped_fields_array[0]
            elif 'ip' in value_type:
                # condition to remove the Mac related fields
                del mapped_fields_array[1]
            else:
                raise SearchFeatureNotSupportedError("Invalid format not supported for this operation")

    @staticmethod
    def _parse_mapped_fields(self, expression, value, comparator, mapped_fields_array):
        comparison_string = ""
        self._check_value_type(value, expression, mapped_fields_array)
        mapped_fields_count = len(mapped_fields_array)

        # issubnet operator expects string literal in data source
        if expression.comparator in [ComparisonComparators.IsSubSet]:
            value = self._format_double_quotes(value)
        else:
            value = self._format_single_quotes(value)

        for mapped_field in mapped_fields_array:
            # Query formation for fields with full text search support
            if 'fulltextSearch' in mapped_field:
                # check exception condition for non-indexed fields excluding Equals and Matches for query support
                if expression.comparator not in [ComparisonComparators.Equal] or not value:
                    raise SearchFeatureNotSupportedError("Only 'Equals' Operator is supported for non-indexed fields")
                else:
                    comparison_string += "{value}".format(value=value)
            elif not value:
                if expression.comparator in [ComparisonComparators.Equal, ComparisonComparators.NotEqual]:
                    comparator = self.arcsight_operator_lookup.get(expression.comparator)
                    comparison_string += "{mapped_field} {comparator}".format(mapped_field=mapped_field,
                                                                              comparator=comparator)
                else:
                    raise SearchFeatureNotSupportedError("Empty string search is not supported for this operation")

            elif any(mapped_field in match for match in INTEGER_LOOKUP_FIELDS) and expression.comparator \
                    in [ComparisonComparators.Like, ComparisonComparators.Matches]:
                # check for excluding integer type attributes in the LIKE/MATCHES search query
                raise SearchFeatureNotSupportedError("'LIKE / MATCHES' Operator is not supported for integer fields")
            else:
                comparison_string += "{mapped_field} {comparator} {value}".format(mapped_field=mapped_field,
                                                                                  comparator=comparator, value=value)

            if mapped_fields_count > 1:
                comparison_string += " OR "
                mapped_fields_count -= 1
        return comparison_string

    @staticmethod
    def _is_reference_value(stix_field):
        return stix_field == 'src_ref.value' or stix_field == 'dst_ref.value'

    @staticmethod
    def _lookup_comparison_operator(self, expression_operator):
        if expression_operator not in self.comparator_lookup:
            raise NotImplementedError(
                "Comparison operator {} unsupported for ArcSight UDS adapter".format(expression_operator.name))
        return self.comparator_lookup[expression_operator]

    def _parse_time_range(self, qualifier, time_range):
        """
        :param qualifier: str, input time range i.e START t'2019-04-10T08:43:10.003Z' STOP t'2019-04-20T10:43:10.003Z'
        :param time_range: int, value available from main.py in options variable
        :return: str, format_string bound with time range provided
        """
        try:
            compile_timestamp_regex = re.compile(START_STOP_PATTERN)
            if qualifier and compile_timestamp_regex.search(qualifier):
                time_range_iterator = compile_timestamp_regex.finditer(qualifier)
                time_range_list = [each.group() for each in time_range_iterator]
                for index, time in enumerate(time_range_list):
                    match_iso8601 = re.compile(ISO_8601_PATTERN).match
                    if match_iso8601(time) is not None and len(time) > 20:
                        pass
                    else:
                        time_range_list[index] = time.replace('Z', '.000Z')
            # Default time range Start time = Now - 5 minutes and Stop time = Now
            else:
                stop_time = datetime.utcnow()
                start_time = stop_time - timedelta(minutes=time_range)
                converted_starttime = start_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                converted_stoptime = stop_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                time_range_list = [converted_starttime, converted_stoptime]

            self.qualifier_list.append(time_range_list)

        except (KeyError, IndexError, TypeError) as e:
            raise e

    def _parse_expression(self, expression, qualifier=None) -> str:
        if isinstance(expression, ComparisonExpression):  # Base Case
            # Resolve STIX Object Path to a field in the target Data Model
            stix_object, stix_field = expression.object_path.split(':')
            # Multiple data source fields may map to the same STIX Object
            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
            # Resolve the comparison symbol to use in the query string (usually just ':')
            comparator = self._lookup_comparison_operator(self, expression.comparator)

            # Some values are formatted differently based on how they're being compared
            if expression.comparator == ComparisonComparators.Matches:
                value = self._format_equality(expression.value)
            elif expression.comparator == ComparisonComparators.In:
                value = self._format_set(expression.value)
            elif expression.comparator == ComparisonComparators.Equal or \
                    expression.comparator == ComparisonComparators.NotEqual:
                # Should be in single-quotes
                value = self._format_equality(expression.value)
            # '%' -> '*' wildcard
            elif expression.comparator == ComparisonComparators.Like:
                if '_' in expression.value:
                    raise SearchFeatureNotSupportedError(
                        "'LIKE' Operator is not supported for '_' wildcard character")
                else:
                    value = self._format_like(expression.value)
            else:
                value = self._escape_value(expression.value)

            # format path like values to suit arcsight supported formats
            if expression.comparator not in [ComparisonComparators.In]:
                value = self._escape_value(value)

            comparison_string = self._parse_mapped_fields(self, expression, value, comparator,
                                                          mapped_fields_array)

            if len(mapped_fields_array) > 1 and not self._is_reference_value(stix_field):
                # More than one data source field maps to the STIX attribute, so group comparisons together.
                grouped_comparison_string = "(" + comparison_string + ")"
                comparison_string = grouped_comparison_string

            if expression.negated:
                # exclusion conditions for negation operator
                if expression.comparator in [ComparisonComparators.Like]:
                    raise SearchFeatureNotSupportedError("'NOT' Operator is not supported for LIKE")
                if 'fulltextSearch' in mapped_fields_array:
                    raise SearchFeatureNotSupportedError("'NOT' Operator is not supported for non-indexed fields")

                comparison_string = self._negate_comparison(comparison_string)

            return "{}".format(comparison_string)
        elif isinstance(expression, CombinedComparisonExpression):
            operator = self._lookup_comparison_operator(self, expression.operator)
            expression_01 = self._parse_expression(expression.expr1)
            expression_02 = self._parse_expression(expression.expr2)
            if not expression_01 or not expression_02:
                return ''
            query_string = "{} {} {}".format(expression_01, operator, expression_02)
            return "{}".format(query_string)
        elif isinstance(expression, ObservationExpression):
            self._parse_time_range(qualifier, self._time_range)
            return self._parse_expression(expression.comparison_expression, qualifier)
        elif isinstance(expression, CombinedObservationExpression):
            operator = self._lookup_comparison_operator(self, expression.operator)
            expression_01 = self._parse_expression(expression.expr1, qualifier)
            expression_02 = self._parse_expression(expression.expr2, qualifier)
            # condition to pop the duplicate time qualifiers for combined queries
            if self.qualifier_list[-2] == self.qualifier_list[-1]:
                self.qualifier_list.pop(-1)
                if expression_01 and expression_02:
                    return "({}) {} ({})".format(expression_01, operator, expression_02)
                else:
                    return ''
            else:
                if expression_01:
                    self.qualified_queries.append([expression_01])
                if expression_02:
                    self.qualified_queries.append([expression_02])
        elif isinstance(expression, StartStopQualifier):
            if hasattr(expression, 'observation_expression'):
                return self._parse_expression(getattr(expression, 'observation_expression'), expression.qualifier)
        elif isinstance(expression, Pattern):
            return "{expr}".format(expr=self._parse_expression(expression.expression))
        else:
            raise RuntimeError("Unknown Recursion Case for expression={}, type(expression)={}".format(
                expression, type(expression)))

    def parse_expression(self, pattern: Pattern):
        return self._parse_expression(pattern)


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    # Query result limit and time range can be passed into the QueryStringPatternTranslator
    time_range = options['time_range']
    final_queries = []

    query = QueryStringPatternTranslator(pattern, data_model_mapping, time_range)

    # This sample return statement is in an SQL format. This should be changed to the native data source query
    # language. If supported by the query language, a limit on the number of results should be added to the query as
    # defined by options['result_limit']. Translated patterns must be returned as a list of one or more native query
    # strings. A list is returned because some query languages require the STIX pattern to be split into multiple
    # query strings.

    # check for combining the queries for grouped time qualifiers in multiple observations
    if len(query.qualified_queries) == 0 and query.translated is not None:
        translate_query_dict = dict()
        translate_query_dict['query'] = query.translated
        translate_query_dict['start_time'] = query.qualifier_list[0][0]
        translate_query_dict['end_time'] = query.qualifier_list[0][1]
        translate_query_dict = json.dumps(translate_query_dict)
        final_queries.append(translate_query_dict)
    # check for forming multiple queries for individual time qualifiers in multiple observations
    elif query.translated == 'None' and len(query.qualified_queries) > 0:
        query.qualifier_list = list(zip(*query.qualifier_list))
        queries_string = query.qualified_queries
        for index, each_query in enumerate(queries_string, start=0):
            translate_query_dict = dict()
            translate_query_dict['query'] = each_query[0]
            translate_query_dict['start_time'] = query.qualifier_list[0][index]
            translate_query_dict['end_time'] = query.qualifier_list[1][index]
            translate_query_dict = json.dumps(translate_query_dict)
            final_queries.append(translate_query_dict)
    return final_queries
