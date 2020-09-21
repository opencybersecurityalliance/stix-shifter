from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators
from stix_shifter_utils.stix_translation.src.utils.transformers import TimestampToMilliseconds, DateTimeToUnixTimestamp, EpochSecondsToTimestamp
from stix_shifter_utils.stix_translation.src.json_to_stix import observable
import datetime
import logging
import re


logger = logging.getLogger(__name__)


class QueryStringPatternTranslator:
    # Change comparator values to match with supported data source operators
    comparator_lookup = {
        ComparisonExpressionOperators.And: "AND",
        ComparisonExpressionOperators.Or: "OR",
        ComparisonComparators.GreaterThan: ":>",
        ComparisonComparators.GreaterThanOrEqual: ":>=",
        ComparisonComparators.LessThan: ":<",
        ComparisonComparators.LessThanOrEqual: ":<=",
        ComparisonComparators.Equal: ":",
        ComparisonComparators.NotEqual: "NOT",
        ComparisonComparators.Like: ":",
        ComparisonComparators.In: ":",
        ComparisonComparators.Matches: ':',  # Elastic Search does not support PCRE.
        ComparisonComparators.IsSubSet: ':',
        ComparisonComparators.IsSuperSet: ':',
        ObservationOperators.Or: 'OR',
        ObservationOperators.And: 'OR'  # Treat AND's as OR's -- Unsure how two ObsExps wouldn't cancel each other out.
    }

    def __init__(self, pattern: Pattern, data_model_mapper):
        self.dmm = data_model_mapper
        self.pattern = pattern
        # List for any queries that are split due to START STOP qualifier
        self.qualified_queries = []
        # Translated query string without any qualifiers
        self.translated = self.parse_expression(pattern)
        self.qualified_queries.append(self.translated)

        self.qualified_queries = _format_translated_queries(self.qualified_queries)

    @staticmethod
    def _format_set(values) -> str:
        gen = values.element_iterator()
        return "({})".format(' OR '.join(['"{}"'.format(value) for value in gen]))

    @staticmethod
    def _format_equality(value) -> str:
        value_escaped = QueryStringPatternTranslator._escape_value(value)
        return '"{}"'.format(value_escaped)

    @staticmethod
    def _format_like(value) -> str:
        # Replacing value with % to * and _ to ? for to support Like comparator
        if isinstance(value, str):
            return '{}'.format(value.replace('%', '*').replace('_', '?'))
        else:
            return value

    @staticmethod
    def _escape_value(value, comparator=None) -> str:
        if isinstance(value, str):
            return '{}'.format(value.replace('\\', '\\\\').replace('\"', '\\"').replace('(', '\\(').replace(')', '\\)'))
        else:
            return value

    @staticmethod
    def _negate_comparison(comparison_string):
        return "(NOT ({}))".format(comparison_string)

    @staticmethod
    def _parse_mapped_fields(self, expression, value, comparator, stix_field, mapped_fields_array):
        comparison_string = ""
        mapped_fields_count = len(mapped_fields_array)

        for mapped_field in mapped_fields_array:
            if expression.comparator == ComparisonComparators.NotEqual or \
                    expression.comparator == ComparisonComparators.IsSuperSet:
                comparator = ':'
                comparison_string += "(NOT {mapped_field} {comparator} {value} AND {mapped_field}:*)".format(mapped_field=mapped_field, comparator=comparator, value=value)
            elif expression.comparator == ComparisonComparators.GreaterThan or \
                    expression.comparator == ComparisonComparators.LessThan or \
                    expression.comparator == ComparisonComparators.GreaterThanOrEqual or \
                    expression.comparator == ComparisonComparators.LessThanOrEqual:
                # Check whether value is in datetime format, Ex: process.created
                pattern = "^\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z$"
                try:
                    match = bool(re.search(pattern, value))
                except:
                    match = False
                if match:
                    # IF value is in datetime format then do conversion of datetime into
                    # proper Range query of timestamps supported by elastic_ecs for comparators like :<,:>,:<=,:>=
                    comparison_string += _get_timestamp(mapped_field, comparator, value)
                else:
                    comparison_string += "{mapped_field}{comparator}{value}".format(mapped_field=mapped_field,
                                                                                    comparator=comparator,
                                                                                    value=value)
            elif expression.comparator == ComparisonComparators.IsSubSet:
                comparison_string += "({mapped_field} {comparator} {value} AND {mapped_field}:*)".format(
                    mapped_field=mapped_field, comparator=comparator, value=value)
            else:
                comparison_string += "{mapped_field} {comparator} {value}".format(mapped_field=mapped_field,
                                                                                  comparator=comparator,
                                                                                  value=value)
            if (mapped_fields_count > 1):
                comparison_string += " OR "
                mapped_fields_count -= 1

        return comparison_string

    def _parse_expression(self, expression, qualifier=None) -> str:
        if isinstance(expression, ComparisonExpression):  # Base Case
            # Resolve STIX Object Path to a field in the target Data Model
            stix_object, stix_field = expression.object_path.split(':')
            # Multiple data source fields may map to the same STIX Object
            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
            # Resolve the comparison symbol to use in the query string (usually just ':')
            comparator = self.comparator_lookup[expression.comparator]

            if stix_field == 'start' or stix_field == 'end':
                transformer = TimestampToMilliseconds()
                expression.value = transformer.transform(expression.value)

            # Some values are formatted differently based on how they're being compared
            # if expression.comparator == ComparisonComparators.Matches:  # needs forward slashes
            #    value = self._format_match(expression.value)
            # should be (x, y, z, ...)
            elif expression.comparator == ComparisonComparators.In:
                value = self._format_set(expression.value)
            elif expression.comparator == ComparisonComparators.Equal or \
                    expression.comparator == ComparisonComparators.NotEqual or \
                    expression.comparator == ComparisonComparators.IsSubSet or \
                    expression.comparator == ComparisonComparators.IsSuperSet:
                value = self._format_equality(expression.value)
            # '%' -> '*' wildcard, '_' -> '?' single wildcard
            elif expression.comparator == ComparisonComparators.Like:
                value = self._format_like(expression.value)
            else:
                value = self._escape_value(expression.value)

            comparison_string = self._parse_mapped_fields(self, expression, value, comparator, stix_field, mapped_fields_array)
            if(len(mapped_fields_array) > 1):
                # More than one data source field maps to the STIX attribute, so group comparisons together.
                grouped_comparison_string = "(" + comparison_string + ")"
                comparison_string = grouped_comparison_string

            if expression.negated:
                comparison_string = self._negate_comparison(comparison_string)

            if qualifier is not None:
                self.qualified_queries.append("{} {}".format(comparison_string, qualifier))
                return ''
            else:
                return "{}".format(comparison_string)

        elif isinstance(expression, CombinedComparisonExpression):
            operator = self.comparator_lookup[expression.operator]
            expression_01 = self._parse_expression(expression.expr1)
            expression_02 = self._parse_expression(expression.expr2)
            if not expression_01 or not expression_02:
                return ''
            if isinstance(expression.expr1, CombinedComparisonExpression):
                expression_01 = "({})".format(expression_01)
            if isinstance(expression.expr2, CombinedComparisonExpression):
                expression_02 = "({})".format(expression_02)
            query_string = "{} {} {}".format(expression_01, operator, expression_02)
            if qualifier is not None:
                self.qualified_queries.append("{} {}".format(query_string, qualifier))
                return ''
            else:
                return "{}".format(query_string)
        elif isinstance(expression, ObservationExpression):
            return self._parse_expression(expression.comparison_expression, qualifier)
        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            if isinstance(expression.observation_expression, CombinedObservationExpression):
                operator = self.comparator_lookup[expression.observation_expression.operator]
                # qualifier only needs to be passed into the parse expression once since it will be the same for both expressions
                expression_01 = self._parse_expression(expression.observation_expression.expr1)
                expression_02 = self._parse_expression(expression.observation_expression.expr2, expression.qualifier)

                if expression_01:
                    return "{expr1}".format(expr1=expression_01)
            else:
                return self._parse_expression(expression.observation_expression.comparison_expression, expression.qualifier)
        elif isinstance(expression, CombinedObservationExpression):
            operator = self.comparator_lookup[expression.operator]
            expression_01 = self._parse_expression(expression.expr1)
            expression_02 = self._parse_expression(expression.expr2)
            if expression_01 and expression_02:
                return "({}) {} ({})".format(expression_01, operator, expression_02)
            elif expression_01:
                return "{}".format(expression_01)
            elif expression_02:
                return "{}".format(expression_02)
            else:
                return ''
        elif isinstance(expression, Pattern):
            return "{expr}".format(expr=self._parse_expression(expression.expression))
        else:
            raise RuntimeError("Unknown Recursion Case for expression={}, type(expression)={}".format(
                expression, type(expression)))

    def parse_expression(self, pattern: Pattern):
        return self._parse_expression(pattern)


def _get_timestamp(mapped_field, comparator, value):
    converted_value = None

    time_pattern = '%Y-%m-%dT%H:%M:%S.%fZ'
    epoch = datetime.datetime(1970, 1, 1)
    # convert date value from UTC timestamp to epoch seconds
    converted_epoch_seconds = int((datetime.datetime.strptime(value, time_pattern) - epoch).total_seconds())

    if converted_epoch_seconds and comparator == ':>':
        converted_epoch_seconds = converted_epoch_seconds + 1
        # convert epoch seconds to UTC Timestamp format
        value_in_timestamp = EpochSecondsToTimestamp.transform(converted_epoch_seconds)
        # Form RANGE Query [UTC TIMESTAMP TO *]
        converted_value = ':["{}" TO *]'.format(value_in_timestamp)
    elif converted_epoch_seconds and comparator == ':<':
        converted_epoch_seconds = converted_epoch_seconds - 1
        # convert epoch seconds to UTC Timestamp format
        value_in_timestamp = EpochSecondsToTimestamp.transform(converted_epoch_seconds)
        # Form RANGE Query [* TO UTC TIMESTAMP]
        converted_value = ':[* TO "{}"]'.format(value_in_timestamp)
    elif comparator == ':<=':
        # Form RANGE Query [* TO UTC TIMESTAMP]
        converted_value = ':[* TO "{}"]'.format(value)
    elif comparator == ':>=':
        # Form RANGE Query [UTC TIMESTAMP TO *]
        converted_value = ':["{}" TO *]'.format(value)

    if converted_value:
        return "({mapped_field}{value})".format(mapped_field=mapped_field,
                                                value=converted_value)


def _test_or_add_milliseconds(timestamp) -> str:
    if not _test_timestamp(timestamp):
        raise ValueError("Invalid timestamp")
    # remove single quotes around timestamp
    timestamp = re.sub("'", "", timestamp)
    # check for 3-decimal milliseconds
    pattern = "\.\d+Z$"
    if not bool(re.search(pattern, timestamp)):
        timestamp = re.sub('Z$', '.000Z', timestamp)
    return timestamp


def _test_START_STOP_format(query_string) -> bool:
    # Matches STARTt'1234-56-78T00:00:00.123Z'STOPt'1234-56-78T00:00:00.123Z'
    pattern = "START((t'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z')|(\s\d{13}\s))STOP"
    match = re.search(pattern, query_string)
    return bool(match)


def _test_timerange_format(query_string) -> bool:
    # Matches @timestamp:["2019-01-28T12:24:01.009Z" TO "2019-01-28T12:54:01.009Z]"
    pattern = r'\@timestamp:\["\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z"\s*TO'
    match = re.search(pattern, query_string)
    return bool(match)


def _test_timestamp(timestamp) -> bool:
    pattern = "^'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z'$"
    match = re.search(pattern, timestamp)
    return bool(match)


def _convert_timestamps_to_milliseconds(query_parts):
    # grab time stamps from array
    start_time = _test_or_add_milliseconds(query_parts[2])
    stop_time = _test_or_add_milliseconds(query_parts[4])
    return query_parts[0] + ' AND (@timestamp:["' + str(start_time) + '" TO "' + str(stop_time) + '"])'


def _format_translated_queries(query_array):
    # remove empty strings in the array
    query_array = list(map(lambda x: x.strip(), list(filter(None, query_array))))

    formatted_queries = []
    for query in query_array:
        if _test_START_STOP_format(query):
            # Remove leading 't' before timestamps
            query = re.sub("(?<=START)t|(?<=STOP)t", "", query)
            # Split individual query to isolate timestamps
            query_parts = re.split("(START)|(STOP)", query)
            # Remove None array entries
            query_parts = list(map(lambda x: x.strip(), list(filter(None, query_parts))))
            if len(query_parts) == 5:
                formatted_queries.append(_convert_timestamps_to_milliseconds(query_parts))
            else:
                logger.info("Omitting query due to bad format for START STOP qualifier timestamp")
                continue
        else:
            formatted_queries.append(query)

    return formatted_queries


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    # Added size parameter in tranmission module
    #result_limit = options['result_limit']
    time_range = options['time_range']
    translated_query_strings = QueryStringPatternTranslator(pattern, data_model_mapping)
    queries = []
    translated_queries = translated_query_strings.qualified_queries
    for query_string in translated_queries:
        has_start_stop = _test_timerange_format(query_string)

        if(has_start_stop):
            queries.append("{}".format(query_string))
        else:
            # Set times based on default time_range or what is in the options
            stop_time = datetime.datetime.utcnow()
            go_back_in_minutes = datetime.timedelta(minutes=time_range)
            start_time = stop_time - go_back_in_minutes
            # converting from UTC timestamp 2019-04-13 23:13:06.130401 to
            # string format 2019-04-13 23:13:06.130Z
            converted_starttime = start_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            converted_stoptime = stop_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            time_range_str = 'AND (@timestamp:["' + str(converted_starttime) + '" TO "' + str(
                converted_stoptime) + '"])'
            queries.append("{} {}".format(query_string, time_range_str))

    return queries
