import datetime
import json
import logging
import re
import time

from stix_shifter_utils.stix_translation.src.json_to_stix import observable
from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, SetValue
from stix_shifter_utils.stix_translation.src.utils.transformers import TimestampToMilliseconds
from .visionone_util import remove_enclosed_quote

REFERENCE_DATA_TYPES = {
    "dst": ["ipv4", "ipv6", "ipv4_cidr", "ipv6_cidr"],
    "src": ["ipv4", "ipv6", "ipv4_cidr", "ipv6_cidr"],
    "objectIp": ["ipv4", "ipv6", "ipv4_cidr", "ipv6_cidr"],
    "sender": ["email-address"],
    "source_ip": ["ipv4", "ipv6", "ipv4_cidr", "ipv6_cidr"],
}
START_STOP_STIX_QUALIFIER = r"START((t'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z')|(\s\d{13}\s))STOP"
TIMESTAMP = r"^'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z'$"
TIMESTAMP_MILLISECONDS = r"\.\d+Z$"

logger = logging.getLogger(__name__)


class QueryStringPatternTranslator:

    def __init__(self, pattern: Pattern, data_model_mapper):
        self.dmm = data_model_mapper
        self.comparator_lookup = self.dmm.map_comparator()
        self.pattern = pattern
        self.using_operators = set()
        self.assigned_fields = set()
        self.qualified_queries = []
        self.translated = self.parse_expression(pattern, data_model_mapper.dialect)
        self.qualified_queries.append(self.translated)
        self.qualified_queries = _format_translated_queries(self.qualified_queries)

    @staticmethod
    def _format_equality(value) -> str:
        return '\"{}\"'.format(value)

    @staticmethod
    def _format_like(value) -> str:
        value = "{value}".format(value=value)
        return QueryStringPatternTranslator._escape_value(value)

    @staticmethod
    def _escape_value(value, comparator=None) -> str:
        if isinstance(value, str):
            return '{}'.format(value.replace('\\', '\\\\').replace('\"', '\\"').replace('(', '\\(').replace(')', '\\)').replace(':', '\\:'))
        else:
            return value

    @staticmethod
    def _negate_comparison(comparison_string):
        return "NOT ({})".format(comparison_string)

    @staticmethod
    def _check_value_type(value):
        """
        Determine the type (ipv4, ipv6, mac, date, etc) of the provided value.
        See: https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/stix_shifter_utils/stix_translation/src/json_to_stix/observable.py#L1
        :param value: query value
        :type value: int/str
        :return: type of value
        :rtype: str
        """
        value = str(value)
        for key, pattern in observable.REGEX.items():
            if key != 'date' and bool(re.search(pattern, value)):
                return key
        return None

    def _parse_reference(self, stix_field, value_type, mapped_field, value, comparator):
        if value_type not in REFERENCE_DATA_TYPES["{}".format(mapped_field)]:
            return None
        else:
            return "{mapped_field} {comparator} {value}".format(
                mapped_field=remove_enclosed_quote(mapped_field), comparator=comparator, value=value)

    

    def _parse_mapped_fields(self, value, comparator, mapped_fields_array) -> str:
        """Convert a list of mapped fields into a query string."""
        comparison_strings = []
        value_type = None
        str_ = None

        if isinstance(value, str):
            value = [value]

        for val in value:
            value_type = self._check_value_type(val)

            for mapped_field in mapped_fields_array:
                comparison_strings.append(f'{mapped_field}{comparator}{val}')

        # Only wrap in () if there's more than one comparison string
        if len(comparison_strings) == 1:
            str_ = comparison_strings[0]
        elif len(comparison_strings) > 1:
            str_ = f"{' OR '.join(comparison_strings)}"
        else:
            raise RuntimeError((f'Failed to convert {mapped_fields_array} mapped fields into query string'))

        return str_

    @staticmethod
    def _is_reference_value(stix_field):
        return stix_field in ('src_ref.value', 'dst_ref.value')


    def _lookup_comparison_operator(self, expression_operator, dialect):
        if str(expression_operator) not in self.comparator_lookup:
            raise NotImplementedError("Comparison operator {} unsupported for VisionOne connector".format(expression_operator.name))
        if dialect == 'messageActivityData':
            if expression_operator in (ComparisonExpressionOperators.And, ComparisonExpressionOperators.Or):
                self.using_operators.add(expression_operator)
                if len(self.using_operators) > 1:
                    raise NotImplementedError("Multiple operator is not support in MDL")
            if expression_operator == ComparisonComparators.NotEqual:
                raise NotImplementedError("NOT operator is not support in MDL")
        return self.comparator_lookup[str(expression_operator)]

    def _parse_expression(self, expression, dialect, qualifier=None) -> str:
        group = False
        if isinstance(expression, ComparisonExpression):  # Base Case
            # Resolve STIX Object Path to a field in the target Data Model
            stix_object, stix_field = expression.object_path.split(':')
            # Multiple data source fields may map to the same STIX Object
            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
            if dialect == 'messageActivityData':
                mapped_fields_set = set(mapped_fields_array)
                intersection = self.assigned_fields.intersection(mapped_fields_set)
                if intersection:
                    logger.error(f"[{', '.join(intersection)}] mapped from {stix_field} has multiple criteria")
                    raise NotImplementedError("Multiple criteria for one field is not support in MDL")
                else:
                    self.assigned_fields |= mapped_fields_set
            # Resolve the comparison symbol to use in the query string (usually just ':')
            comparator = self._lookup_comparison_operator(expression.comparator, dialect)

            if stix_field in ('start', 'end'):
                transformer = TimestampToMilliseconds()
                expression.value = transformer.transform(expression.value)

            # Some values are formatted differently based on how they're being compared
            if expression.comparator == ComparisonComparators.Equal:
                # Should be in single-quotes
                value = self._format_equality(expression.value)
            elif expression.comparator == ComparisonComparators.NotEqual:
                value = self._format_equality(expression.value)
                expression.negated = True
            # '%' -> '*' wildcard, '_' -> '?' single wildcard
            elif expression.comparator == ComparisonComparators.Like:
                value = self._format_like(expression.value)
            elif (expression.comparator == ComparisonComparators.In and isinstance(expression.value, SetValue)):
                # apply escape value to remove unwanted char in string.
                value = list(map(self._format_equality, expression.value.element_iterator()))
                group = True
            else:
                value = self._escape_value(expression.value)

            comparison_string = self._parse_mapped_fields(
                value=value,
                comparator=comparator,
                mapped_fields_array=mapped_fields_array
            )
            
            if (len(mapped_fields_array) > 1 and not self._is_reference_value(stix_field)) or group:
                # More than one data source field maps to the STIX attribute, so group comparisons together.
                grouped_comparison_string = "(" + comparison_string + ")"
                comparison_string = grouped_comparison_string

            if expression.negated:
                comparison_string = self._negate_comparison(comparison_string)
            if qualifier is not None:
                return "{} {}".format(comparison_string, qualifier)
            else:
                return "{}".format(comparison_string)

        elif isinstance(expression, CombinedComparisonExpression):
            operator = self._lookup_comparison_operator(expression.operator, dialect)
            expression_01 = self._parse_expression(expression.expr1, dialect)
            expression_02 = self._parse_expression(expression.expr2, dialect)
            if not expression_01 or not expression_02:
                return ''
            if isinstance(expression.expr1, CombinedComparisonExpression):
                expression_01 = "({})".format(expression_01)
            if isinstance(expression.expr2, CombinedComparisonExpression):
                expression_02 = "({})".format(expression_02)
            query_string = "{} {} {}".format(expression_01, operator, expression_02)
            if qualifier is not None:
                return "{} {}".format(query_string, qualifier)
            else:
                return "{}".format(query_string)
        elif isinstance(expression, ObservationExpression):
            return self._parse_expression(expression.comparison_expression, dialect, qualifier)
        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            if isinstance(expression.observation_expression, CombinedObservationExpression):
                operator = self._lookup_comparison_operator(expression.observation_expression.operator, dialect)
                expression_01 = self._parse_expression(expression.observation_expression.expr1, dialect)
                # qualifier only needs to be passed into the parse expression once since it will be the same for both expressions
                expression_02 = self._parse_expression(expression.observation_expression.expr2, dialect, expression.qualifier)
                return "{} {} {}".format(expression_01, operator, expression_02)
            else:
                return self._parse_expression(expression.observation_expression.comparison_expression, dialect, expression.qualifier)
        elif isinstance(expression, CombinedObservationExpression):
            operator = self._lookup_comparison_operator(expression.operator, dialect)
            expression_01 = self._parse_expression(expression.expr1, dialect)
            expression_02 = self._parse_expression(expression.expr2, dialect)
            if expression_01 and expression_02:
                return "({}) {} ({})".format(expression_01, operator, expression_02)
            elif expression_01:
                return "{}".format(expression_01)
            elif expression_02:
                return "{}".format(expression_02)
            else:
                return ''
        elif isinstance(expression, Pattern):
            return "{expr}".format(expr=self._parse_expression(expression.expression, dialect))
        else:
            raise RuntimeError("Unknown Recursion Case for expression={}, type(expression)={}".format(
                expression, type(expression)))

    def parse_expression(self, pattern: Pattern, dialect):
        return self._parse_expression(pattern, dialect)


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


def _convert_timestamps_to_milliseconds(query_parts):
    # grab time stamps from array
    start_time = _test_or_add_milliseconds(query_parts[2])
    stop_time = _test_or_add_milliseconds(query_parts[4])
    transformer = TimestampToMilliseconds()
    millisecond_start_time = transformer.transform(start_time)
    millisecond_stop_time = transformer.transform(stop_time)
    payload = dict()
    payload['offset'] = 0
    payload['from'] = millisecond_start_time
    payload['to'] = millisecond_stop_time
    payload['query'] = query_parts[0]
    return payload


def _format_translated_queries(query_array):
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
            payload = dict()
            payload['offset'] = 0
            payload['query'] = query
            formatted_queries.append(payload)

    return formatted_queries


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    # Query result limit and time range can be passed into the QueryStringPatternTranslator if supported by the data source.
    # result_limit = options['result_limit']
    # time_range = options['time_range']
    trans_queries = QueryStringPatternTranslator(pattern, data_model_mapping).qualified_queries
    # Add space around START STOP qualifiers
    # query = re.sub("START", "START ", query)
    # query = re.sub("STOP", " STOP ", query)

    # This sample return statement is in an SQL format. This should be changed to the native data source query language.
    # If supported by the query language, a limit on the number of results should be added to the query as defined by options['result_limit'].
    # Translated patterns must be returned as a list of one or more native query strings.
    # A list is returned because some query languages require the STIX pattern to be split into multiple query strings.
    queries = []
    for q in trans_queries:
        q['source'] = data_model_mapping.dialect
        if 'to' not in q:
            q['to'] = int(time.time())
            q['from'] = int(q['to'] - datetime.timedelta(minutes=options['time_range']).total_seconds())
        else:
            q['to'] = int(q['to'] / 1000)
            q['from'] = int(q['from'] / 1000)
        queries.append(json.dumps(q))
    return queries
