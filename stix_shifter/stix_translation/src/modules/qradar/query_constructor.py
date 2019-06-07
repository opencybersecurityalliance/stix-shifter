from stix_shifter.stix_translation.src.patterns.pattern_objects import ObservationExpression, ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators
from stix_shifter.stix_translation.src.utils.transformers import TimestampToMilliseconds
from stix_shifter.stix_translation.src.json_to_stix import observable
import logging
import json
import re

logger = logging.getLogger(__name__)

REFERENCE_DATA_TYPES = {"sourceip": ["ipv4", "ipv6", "ipv4_cidr"],
                        "sourcemac": ["mac"],
                        "destinationip": ["ipv4", "ipv6", "ipv4_cidr"],
                        "destinationmac": ["mac"]}

START_STOP_STIX_QUALIFIER = "START((t'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z')|(\s\d{13}\s))STOP"
TIMESTAMP = "^'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z'$"
TIMESTAMP_MILLISECONDS = "\.\d+Z$"
TRAILING_COMPARISON_OPERATOR = "\s((OR)|(AND))\s?$"
TRAILING_COMBINED_COMPARISON_OPERATOR = "\sOPERATOR:[a-zA-Z]+$"
LEADING_COMBINED_COMPARISON_OPERATOR = "^OPERATOR:"


def _fetch_network_protocol_mapping():
    try:
        map_file = open(
            'stix_shifter/stix_translation/src/modules/qradar/json/network_protocol_map.json').read()
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

    def __init__(self, pattern: Pattern, data_model_mapper, result_limit, timerange):
        self.dmm = data_model_mapper
        self.pattern = pattern
        self.result_limit = result_limit
        self.timerange = timerange
        self.qualified_queries = []  # Queries with START STOP qualifiers
        self.unqualified_queries = []  # Queries without START STOP qualifiers
        self.parse_expression(pattern)
        self.qualified_queries = self._format_qualified_queries()
        if self.unqualified_queries:
            combined_unqualified_queries_string = self._format_unqualified_queries()
            self.qualified_queries.append(combined_unqualified_queries_string)

    @staticmethod
    def _format_set(values) -> str:
        gen = values.element_iterator()
        return "({})".format(' OR '.join([AqlQueryStringPatternTranslator._escape_value(value) for value in gen]))

    @staticmethod
    def _format_match(value) -> str:
        return "\'{}\'".format(value)

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

    @staticmethod
    def _check_value_type(value):
        value = str(value)
        for key, pattern in observable.REGEX.items():
            if key != 'date' and bool(re.search(pattern, value)):
                return key
        return None

    @staticmethod
    def _parse_reference(self, stix_field, value_type, mapped_field, value, comparator):
        if value_type not in REFERENCE_DATA_TYPES["{}".format(mapped_field)]:
            return None
        if value_type == 'ipv4_cidr':
            # Comparator originally came in as '=' so it must be changed to INCIDR
            comparator = self.comparator_lookup[ComparisonComparators.IsSubSet]
            return comparator + "(" + value + "," + mapped_field + ")"
        else:
            return "{mapped_field} {comparator} {value}".format(
                mapped_field=mapped_field, comparator=comparator, value=value)

    @staticmethod
    def _parse_mapped_fields(self, expression, value, comparator, stix_field, mapped_fields_array):
        comparison_string = ""
        is_reference_value = self._is_reference_value(stix_field)
        # Need to use expression.value to match against regex since the passed-in value has already been formated.
        value_type = self._check_value_type(expression.value) if is_reference_value else None
        mapped_fields_count = 1 if is_reference_value else len(mapped_fields_array)

        for mapped_field in mapped_fields_array:
            # if its a set operator() query construction will be different.
            if expression.comparator == ComparisonComparators.IsSubSet:
                comparison_string += comparator + "(" + "'" + value + "'," + mapped_field + ")"
            elif is_reference_value:
                parsed_reference = self._parse_reference(self, stix_field, value_type, mapped_field, value, comparator)
                if not parsed_reference:
                    continue
                comparison_string += parsed_reference
            # For [ipv4-addr:value = <CIDR value>]
            elif bool(re.search(observable.REGEX['ipv4_cidr'], str(expression.value))):
                comparison_string += "INCIDR(" + value + "," + mapped_field + ")"
            elif expression.object_path == 'x-readable-payload:value' and expression.comparator == ComparisonComparators.Like:
                comparison_string += "TEXT SEARCH '{}'".format(value)
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
        return comparison_string

    @staticmethod
    def _is_reference_value(stix_field):
        return stix_field == 'src_ref.value' or stix_field == 'dst_ref.value'

    @staticmethod
    def _format_value(self, expression):
        if expression.comparator == ComparisonComparators.Matches:
            # needs forward slashes
            return self._format_match(expression.value)
        # should be (x, y, z, ...)
        elif expression.comparator == ComparisonComparators.In:
            return self._format_set(expression.value)
        elif expression.comparator == ComparisonComparators.Equal or expression.comparator == ComparisonComparators.NotEqual:
            # Should be in single-quotes
            return self._format_equality(expression.value)
        # '%' -> '*' wildcard, '_' -> '?' single wildcard
        elif expression.comparator == ComparisonComparators.Like and not (expression.object_path == 'x-readable-payload:value'):
            return self._format_like(expression.value)
        else:
            return self._escape_value(expression.value)

    @staticmethod
    def _parse_pattern_expression(self, expression):
        return self._parse_expression(expression.expression)

    @staticmethod
    def _parse_combined_observation_expression(self, expression, qualifier=None, calling_object_type=None, operator_override=None):
        operator = self.comparator_lookup[expression.operator]
        expression_01 = self._parse_expression(expression.expr1, qualifier, 'CombinedObservationExpression')
        expression_02 = self._parse_expression(expression.expr2, qualifier, 'CombinedObservationExpression')
        if expression_01 and expression_02:
            query_string = "({}) {} ({})".format(expression_01, operator, expression_02)
        elif expression_01:
            query_string = expression_01
        elif expression_02:
            query_string = expression_02
        else:
            query_string = ''
        if qualifier is not None and query_string:
            self.qualified_queries.append("{} limit {} {}".format(query_string, self.result_limit, qualifier))
            # return ''
        elif calling_object_type == 'CombinedObservationExpression' or not query_string:
            return query_string
        else:
            self.unqualified_queries.append(query_string)

    @staticmethod
    def _parse_observation_expression(self, expression, qualifier=None, calling_object_type=None):
        query_string = self._parse_expression(expression.comparison_expression, qualifier, calling_object_type)
        if qualifier is not None and query_string:
            self.qualified_queries.append("{} limit {} {}".format(query_string, self.result_limit, qualifier))
        elif calling_object_type == 'CombinedObservationExpression' or not query_string:
            return query_string
        else:
            self.unqualified_queries.append(query_string)

    @staticmethod
    def _parse_combined_comparison_expression(self, expression, qualifier=None, calling_object_type=None):
        operator = self.comparator_lookup[expression.operator]
        expression_01 = self._parse_expression(expression.expr1, qualifier, 'CombinedComparisonExpression')
        expression_02 = self._parse_expression(expression.expr2, qualifier, 'CombinedComparisonExpression')

        if expression_01 and expression_02:
            query_string = "({} {} {})".format(expression_01, operator, expression_02)
        elif expression_01:
            query_string = "OPERATOR:{} {} OPERATOR:{}".format(operator, expression_01, operator)
        elif expression_02:
            query_string = "OPERATOR:{} {} OPERATOR:{}".format(operator, expression_02, operator)
        else:
            query_string = ''

        if qualifier is not None and query_string:
            self.qualified_queries.append("{} limit {} {}".format(query_string, self.result_limit, qualifier))
        elif calling_object_type in ['CombinedObservationExpression', 'ObservationExpression', 'CombinedComparisonExpression'] or not query_string:
            return query_string
        else:
            self.unqualified_queries.append(query_string)

    @staticmethod
    def _parse_expression_with_start_stop(self, expression):
        qualifier = expression.qualifier
        if isinstance(expression.observation_expression, CombinedObservationExpression):
            operator = self.comparator_lookup[expression.observation_expression.operator]
            expression_01 = self._parse_expression(expression.observation_expression.expr1, qualifier)
            expression_02 = self._parse_expression(expression.observation_expression.expr2, qualifier)
            if expression_01 and expression_02:
                query_string = "({} {} {})".format(expression_01, operator, expression_02)
            elif expression_01:
                query_string = "OPERATOR:{} {} OPERATOR:{}".format(operator, expression_01, operator)
            elif expression_02:
                query_string = "OPERATOR:{} {} OPERATOR:{}".format(operator, expression_02, operator)
            else:
                query_string = ''
            return query_string
        else:
            return self._parse_expression(expression.observation_expression.comparison_expression, qualifier)

    @staticmethod
    def _parse_comparison_expression(self, expression, qualifier=None, calling_object_type=None):
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
        elif stix_field == 'start' or stix_field == 'end':
            transformer = TimestampToMilliseconds()
            expression.value = transformer.transform(expression.value)

        # Some values are formatted differently based on how they're being compared
        value = self._format_value(self, expression)
        comparison_string = self._parse_mapped_fields(self, expression, value, comparator, stix_field, mapped_fields_array)

        if(len(mapped_fields_array) > 1 and not self._is_reference_value(stix_field)):
            # More than one AQL field maps to the STIX attribute so group the ORs.
            comparison_string = "({})".format(comparison_string)
        if expression.comparator == ComparisonComparators.NotEqual:
            comparison_string = self._negate_comparison(comparison_string)
        if expression.negated:
            comparison_string = self._negate_comparison(comparison_string)
        if calling_object_type in ['CombinedObservationExpression', 'ObservationExpression', 'CombinedComparisonExpression']:
            return comparison_string
        elif qualifier is not None:
            self.qualified_queries.append("{} limit {} {}".format(comparison_string, self.result_limit, qualifier))
        else:
            self.unqualified_queries.append(comparison_string)
            return comparison_string

    def _parse_expression(self, expression, qualifier=None, calling_object_type=None) -> str:
        if isinstance(expression, ComparisonExpression):  # Base Case
            return self._parse_comparison_expression(self, expression, qualifier, calling_object_type)
        elif isinstance(expression, CombinedComparisonExpression):
            if not calling_object_type:
                calling_object_type = 'CombinedComparisonExpression'
            return self._parse_combined_comparison_expression(self, expression, qualifier, calling_object_type)
        elif isinstance(expression, ObservationExpression):
            if not calling_object_type:
                calling_object_type = 'ObservationExpression'
            return self._parse_observation_expression(self, expression, qualifier, calling_object_type)
        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            return self._parse_expression_with_start_stop(self, expression)
        elif isinstance(expression, CombinedObservationExpression):
            return self._parse_combined_observation_expression(self, expression)
        elif isinstance(expression, Pattern):
            return self._parse_pattern_expression(self, expression)
        else:
            raise RuntimeError("Unknown Recursion Case for expression={}, type(expression)={}".format(
                expression, type(expression)))

    def _format_qualified_queries(self):
        # remove empty strings in the array
        query_array = list(map(lambda x: x.strip(), list(filter(None, self.qualified_queries))))

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

    def _format_unqualified_queries(self):
        # remove empty strings in the array
        query_array = list(map(lambda x: x.strip(), list(filter(None, self.unqualified_queries))))
        combined_query_string = ''
        # combine all queries into one query joined by OR
        for index, query in enumerate(query_array):
            if index == 0:
                combined_query_string += query
            else:
                if _test_leading_combined_comparison_operator(query):
                    combined_query_string = re.sub(TRAILING_COMPARISON_OPERATOR, '', combined_query_string)
                combined_query_string += " {}".format(query)
            if (index < (len(query_array) - 1)) and (not _test_trailing_combined_comparison_operator(query)):
                combined_query_string += " OR"
        # Remove trailing combined comparison operator
        combined_query_string = re.sub(TRAILING_COMBINED_COMPARISON_OPERATOR, '', combined_query_string)
        # Remove any remaining combined comparison tags
        combined_query_string = re.sub("OPERATOR:", '', combined_query_string)
        # append time and result limit to last query
        combined_query_string += " limit {} last {} minutes".format(self.result_limit, self.timerange)
        return combined_query_string

    def parse_expression(self, pattern: Pattern):
        return self._parse_expression(pattern)


def _test_or_add_milliseconds(timestamp) -> str:
    if not _test_timestamp(timestamp):
        raise ValueError("Invalid timestamp")
    # remove single quotes around timestamp
    timestamp = re.sub("'", "", timestamp)
    # check for 3-decimal milliseconds
    if not bool(re.search(TIMESTAMP_MILLISECONDS, timestamp)):
        timestamp = re.sub('Z$', '.000Z', timestamp)
    return timestamp


def _test_START_STOP_format(query_string) -> bool:
    # Matches STARTt'1234-56-78T00:00:00.123Z'STOPt'1234-56-78T00:00:00.123Z'
    # or START 1234567890123 STOP 1234567890123
    return bool(re.search(START_STOP_STIX_QUALIFIER, query_string))


def _test_timestamp(timestamp) -> bool:
    return bool(re.search(TIMESTAMP, timestamp))


def _test_trailing_combined_comparison_operator(query_string) -> bool:
    return bool(re.search(TRAILING_COMBINED_COMPARISON_OPERATOR, query_string))


def _test_leading_combined_comparison_operator(query_string) -> bool:
    return bool(re.search(LEADING_COMBINED_COMPARISON_OPERATOR, query_string))


def _convert_timestamps_to_milliseconds(query_parts):
    # grab time stamps from array
    start_time = _test_or_add_milliseconds(query_parts[2])
    stop_time = _test_or_add_milliseconds(query_parts[4])
    transformer = TimestampToMilliseconds()
    millisecond_start_time = transformer.transform(start_time)
    millisecond_stop_time = transformer.transform(stop_time)
    return query_parts[0] + " " + query_parts[1] + " " + str(millisecond_start_time) + " " + query_parts[3] + " " + str(millisecond_stop_time)


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    result_limit = options['result_limit']
    timerange = options['timerange']
    translated_where_statements = AqlQueryStringPatternTranslator(pattern, data_model_mapping, result_limit, timerange)
    select_statement = translated_where_statements.dmm.map_selections()
    queries = []
    translated_queries = translated_where_statements.qualified_queries
    for where_statement in translated_queries:
        queries.append("SELECT {} FROM events WHERE {}".format(select_statement, where_statement))
    return queries
