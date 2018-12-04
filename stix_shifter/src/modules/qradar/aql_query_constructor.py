import logging
import datetime
import json
import re

logger = logging.getLogger(__name__)

DEFAULT_LIMIT = 10000
DEFAULT_TIMERANGE = 5

from stix_shifter.src.patterns.pattern_objects import ObservationExpression, ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators
from stix_shifter.src.patterns.errors import SearchFeatureNotSupportedError

from stix_shifter.src.transformers import TimestampToMilliseconds, ValueTransformer


def _fetch_network_protocol_mapping():
    try:
        map_file = open(
            'stix_shifter/src/modules/qradar/json/network_protocol_map.json').read()
        map_data = json.loads(map_file)
        return map_data
    except Exception as ex:
        print('exception in reading mapping file:', ex)
        return {}


class AqlQueryStringPatternTranslator:
    comparator_lookup = {
        ComparisonExpressionOperators.And: "AND",
        ComparisonExpressionOperators.Or: "OR",
        ComparisonComparators.GreaterThan: ">",
        ComparisonComparators.GreaterThanOrEqual: ">=",
        ComparisonComparators.LessThan: "<",
        ComparisonComparators.LessThanOrEqual: "<=",
        ComparisonComparators.Equal: "=",
        ComparisonComparators.NotEqual: "!=",
        ComparisonComparators.Like: "LIKE",
        ComparisonComparators.In: "IN",
        ComparisonComparators.Matches: 'MATCHES',
        ComparisonComparators.IsSubSet: 'INCIDR',
        ObservationOperators.Or: 'OR',
        # Treat AND's as OR's -- Unsure how two ObsExps wouldn't cancel each other out.
        ObservationOperators.And: 'OR'
    }

    def __init__(self, pattern: Pattern, data_model_mapper, result_limit):
        self.dmm = data_model_mapper
        self.pattern = pattern
        self.result_limit = result_limit
        self.translated = self.parse_expression(pattern)

        # Split WHERE statements having a START STOP qualifier: AQL only supports one START STOP qualifier per query.
        query_split = self.translated.split("SPLIT")
        if len(query_split) > 1:
            self.queries = _format_split_queries(query_split)
        else:
            self.queries = query_split

    @staticmethod
    def _format_set(values) -> str:
        gen = values.element_iterator()
        return "({})".format(' OR '.join([AqlQueryStringPatternTranslator._escape_value(value) for value in gen]))

    @staticmethod
    def _format_match(value) -> str:
        raw = AqlQueryStringPatternTranslator._escape_value(value)
        if raw[0] == "^":
            raw = raw[1:]
        else:
            raw = ".*" + raw
        if raw[-1] == "$":
            raw = raw[0:-1]
        else:
            raw = raw + ".*"
        return "\'{}\'".format(raw)

    @staticmethod
    def _format_equality(value) -> str:
        return '\'{}\''.format(value)

    @staticmethod
    def _format_like(value) -> str:
        value = "'%{value}%'".format(value=value)
        return AqlQueryStringPatternTranslator._escape_value(value)

    @staticmethod
    def _escape_value(value, comparator=None) -> str:
        if isinstance(value, str):
            return '{}'.format(value.replace('\\', '\\\\').replace('\"', '\\"').replace('(', '\\(').replace(')', '\\)'))
        else:
            return value

    @staticmethod
    def _negate_comparison(comparison_string):
        return "NOT({})".format(comparison_string)

    def _parse_expression(self, expression, qualifier=None) -> str:
        if isinstance(expression, ComparisonExpression):  # Base Case
            # Resolve STIX Object Path to a field in the target Data Model
            stix_object, stix_field = expression.object_path.split(':')
            # Multiple QRadar fields may map to the same STIX Object
            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
            # Resolve the comparison symbol to use in the query string (usually just ':')
            comparator = self.comparator_lookup[expression.comparator]

            if stix_field == 'protocols[*]':
                map_data = _fetch_network_protocol_mapping()
                try:
                    expression.value = map_data[expression.value.lower()]
                except Exception as protocol_key:
                    raise KeyError(
                        "Network protocol {} is not supported.".format(protocol_key))

                except Exception as hash_key:
                    raise KeyError(
                        "File hash {} is not supported.".format(hash_key))
            elif stix_field == 'start' or stix_field == 'end':
                transformer = TimestampToMilliseconds()
                expression.value = transformer.transform(expression.value)

            # Some values are formatted differently based on how they're being compared
            if expression.comparator == ComparisonComparators.Matches:  # needs forward slashes
                value = self._format_match(expression.value)
            # should be (x, y, z, ...)
            elif expression.comparator == ComparisonComparators.In:
                value = self._format_set(expression.value)
            elif expression.comparator == ComparisonComparators.Equal or expression.comparator == ComparisonComparators.NotEqual:
                # Should be in single-quotes
                value = self._format_equality(expression.value)
            # '%' -> '*' wildcard, '_' -> '?' single wildcard
            elif expression.comparator == ComparisonComparators.Like:
                value = self._format_like(expression.value)
            else:
                value = self._escape_value(expression.value)

            comparison_string = ""
            mapped_fields_count = len(mapped_fields_array)
            for mapped_field in mapped_fields_array:
                # if its a set operator() query construction will be different.
                if expression.comparator == ComparisonComparators.IsSubSet:
                    comparison_string += comparator + "(" + "'" + value + "'," + mapped_field + ")"
                else:
                    # There's no aql field for domain-name. using Like operator to find domian name from the url
                    if mapped_field == 'domainname' and comparator != ComparisonComparators.Like:
                        comparator = self.comparator_lookup[ComparisonComparators.Like]
                        value = self._format_like(expression.value)

                    comparison_string += "{mapped_field} {comparator} {value}".format(
                        mapped_field=mapped_field, comparator=comparator, value=value)

                if (mapped_fields_count > 1):
                    comparison_string += " OR "
                    mapped_fields_count -= 1

            if(len(mapped_fields_array) > 1):
                # More than one AQL field maps to the STIX attribute so group the ORs.
                grouped_comparison_string = "(" + comparison_string + ")"
                comparison_string = grouped_comparison_string

            if expression.comparator == ComparisonComparators.NotEqual:
                comparison_string = self._negate_comparison(comparison_string)

            if expression.negated:
                comparison_string = self._negate_comparison(comparison_string)
            if qualifier is not None:
                return "SPLIT{} limit {} {}SPLIT".format(comparison_string, self.result_limit, qualifier)
            else:
                return "{}".format(comparison_string)

        elif isinstance(expression, CombinedComparisonExpression):
            query_string = "{} {} {}".format(self._parse_expression(expression.expr1),
                                             self.comparator_lookup[expression.operator],
                                             self._parse_expression(expression.expr2))
            if qualifier is not None:
                return "SPLIT{} limit {} {}SPLIT".format(query_string, self.result_limit, qualifier)
            else:
                return "{}".format(query_string)
        elif isinstance(expression, ObservationExpression):
            return self._parse_expression(expression.comparison_expression, qualifier)
        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            if isinstance(expression.observation_expression, CombinedObservationExpression):
                operator = self.comparator_lookup[expression.observation_expression.operator]
                # qualifier only needs to be passed into the parse expression once since it will be the same for both expressions
                return "{expr1} {operator} {expr2}".format(expr1=self._parse_expression(expression.observation_expression.expr1),
                                                           operator=operator,
                                                           expr2=self._parse_expression(expression.observation_expression.expr2, expression.qualifier))
            else:
                return self._parse_expression(expression.observation_expression.comparison_expression, expression.qualifier)
        elif isinstance(expression, CombinedObservationExpression):
            operator = self.comparator_lookup[expression.operator]
            return "{expr1} {operator} {expr2}".format(expr1=self._parse_expression(expression.expr1),
                                                       operator=operator,
                                                       expr2=self._parse_expression(expression.expr2))
        elif isinstance(expression, Pattern):
            return "{expr}".format(expr=self._parse_expression(expression.expression))
        else:
            raise RuntimeError("Unknown Recursion Case for expression={}, type(expression)={}".format(
                expression, type(expression)))

    def parse_expression(self, pattern: Pattern):
        return self._parse_expression(pattern)


def _test_or_add_milliseconds(timestamp) -> str:
    if not _test_timestamp(timestamp):
        raise ValueError("Invalid timestamp")
    # remove single quotes around timestamp
    timestamp = re.sub("'", "", timestamp)
    # check for 3-decimal milliseconds
    pattern = "\.\d{3}Z$"
    match = re.search(pattern, timestamp)
    if bool(match):
        return timestamp
    else:
        pattern = "(\.\d+Z$)|(Z$)"
        timestamp = re.sub(pattern, ".000Z", timestamp)
        return timestamp


def _test_START_STOP_format(query_string) -> bool:
    # Matches STARTt'1234-56-78T00:00:00.123Z'STOPt'1234-56-78T00:00:00.123Z'
    # or START 1234567890123 STOP 1234567890123
    pattern = "START((t'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z')|(\s\d{13}\s))STOP"
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
    transformer = TimestampToMilliseconds()
    millisecond_start_time = transformer.transform(start_time)
    millisecond_stop_time = transformer.transform(stop_time)
    return query_parts[0] + " " + query_parts[1] + " " + str(millisecond_start_time) + " " + query_parts[3] + " " + str(millisecond_stop_time)


def _format_split_queries(query_array):
    # removing leading AND/OR
    query_array = list(map(lambda x: re.sub("^\s?(OR|AND)\s?", "", x), query_array))
    # removing trailing AND/OR
    query_array = list(map(lambda x: re.sub("\s?(OR|AND)\s?$", "", x), query_array))
    # remove empty strings in the array
    query_array = list(map(lambda x: x.strip(), list(filter(None, query_array))))

    # Transform from human-readable timestamp to 13-digit millisecond time
    # Ex. START t'2014-04-25T15:51:20.000Z' to START 1398441080000
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
    result_limit = options['result_limit'] if 'result_limit' in options else DEFAULT_LIMIT
    timerange = options['timerange'] if 'timerange' in options else DEFAULT_TIMERANGE
    translated_where_statements = AqlQueryStringPatternTranslator(pattern, data_model_mapping, result_limit)
    select_statement = translated_where_statements.dmm.map_selections()
    queries = []
    for where_statement in translated_where_statements.queries:
        has_start_stop = _test_START_STOP_format(where_statement)
        if(has_start_stop):
            queries.append("SELECT {} FROM events WHERE {}".format(select_statement, where_statement))
        else:
            queries.append("SELECT {} FROM events WHERE {} limit {} last {} minutes".format(select_statement, where_statement, result_limit, timerange))

    return queries
