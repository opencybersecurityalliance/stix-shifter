import datetime
import json
import logging
import re
import time

from stix_shifter_utils.stix_translation.src.json_to_stix import observable
from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import (
    ObservationExpression, ComparisonExpression,
    ComparisonExpressionOperators, ComparisonComparators, Pattern,
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators
)
from .transformers import InfobloxToDomainName, TimestampToSeconds

# TODO: revisit the pattern for references, is this really needed?
REFERENCE_DATA_TYPES = {
    "qip": ["ipv4", "ipv4_cidr"],
    "value": ["ipv4", "ipv4_cidr", "domain_name"],
    "qname": ["domain_name"],
    "ip": ["ipv4", "ipv4_cidr", "ipv6", "ipv6_cidr"]
}
REFERENCE_FIELDS = ('src_ref.value', 'hostname_ref.value',
    'ip_ref.value', 'extensions.dns-ext.question.domain_ref.value'
)

START_STOP_STIX_QUALIFIER = r"START((t'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z')|(\s\d{13}\s))STOP"
TIMESTAMP = r"^'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z'$"
TIMESTAMP_MILLISECONDS = r"\.\d+Z$"

THREAT_LEVEL_MAPPING = {
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1
}

logger = logging.getLogger(__name__)


class QueryStringPatternTranslator:
    comparator_lookup = {
        'tideDbData': {
            ComparisonExpressionOperators.And: "&",
            ObservationOperators.And: '&',
            ComparisonComparators.Equal: "=",
            ComparisonComparators.GreaterThan: "=",
            ComparisonComparators.GreaterThanOrEqual: "=",
            ComparisonComparators.LessThan: "=",
            ComparisonComparators.LessThanOrEqual: "=",
            ComparisonComparators.Like: "="
        },
        'dnsEventData': {
            ComparisonExpressionOperators.And: "&",
            ObservationOperators.And: '&',
            ComparisonComparators.Equal: "="
        },
        'dossierData': {
            ComparisonExpressionOperators.And: "&",
            ObservationOperators.And: '&',
            ComparisonComparators.Equal: "="
        }
    }

    def __init__(self, pattern: Pattern, data_model_mapper, time_range):
        self.dmm = data_model_mapper
        self.pattern = pattern
        self.using_operators = set()
        self.assigned_fields = set()
        self.qualified_queries = []
        self.threat_type_map = {
            'tideDbData': '',
            'dnsEventData': '',
            'dossierData': ''
        }
        self.dialect = data_model_mapper.dialect
        self.translated = self.parse_expression(pattern)

        self.qualified_queries.append(self.translated)
        self.qualified_queries = _format_translated_queries(self.dialect,
                                                            self.qualified_queries,
                                                            self.threat_type_map,
                                                            time_range)

    @staticmethod
    def _format_equality(value) -> str:
        return '{}'.format(value)

    @staticmethod
    def _format_like(value) -> str:
        return "{}".format(value)

    @staticmethod
    def _check_value_type(value):
        value = str(value)
        for key, pattern in observable.REGEX.items():
            if key != 'date' and bool(re.search(pattern, value)):
                return key
        return None

    @staticmethod
    def _parse_reference(value_type, mapped_field, value, comparator):
        if value_type not in REFERENCE_DATA_TYPES["{}".format(mapped_field)]:
            return None
        else:
            return "{mapped_field}{comparator}{value}".format(
                mapped_field=mapped_field, comparator=comparator, value=value)

    def _sanatize_field(self, mapped_field, comparator):
        # NOTE: performs the necessary un-transformation/conversion to Infoblox compatible query.
        comparator_suffix_map = {
            ComparisonComparators.GreaterThan: '_from_date',
            ComparisonComparators.GreaterThanOrEqual: '_from_date',
            ComparisonComparators.LessThan: '_to_date',
            ComparisonComparators.LessThanOrEqual: '_to_date',
        }

        updated_field = mapped_field
        if self.dialect == 'tideDbData':
            if mapped_field == 'imported':
                updated_field = 'imported' + comparator_suffix_map[comparator]
            elif comparator == ComparisonComparators.Like:
                if mapped_field not in ['profile', 'origin', 'host', 'ip', 'url', 'domain', 'property', 'class', 'target']:
                    raise NotImplementedError("Comparison operator {} unsupported for Infoblox connector {} field {}".format(comparator.name, self.dialect, mapped_field))
                updated_field = 'text_search'
        return updated_field

    def _sanatize_value(self, mapped_field, value):
        # NOTE: performs the necessary un-transformation/conversion to Infoblox compatible query.
        updated_value = value
        if self.dialect == 'dnsEventData':
            if mapped_field == 'qname':
                updated_value = InfobloxToDomainName.untransform(value)
            elif mapped_field == 'threat_level':
                updated_value = THREAT_LEVEL_MAPPING[value]
        elif self.dialect == 'tideDbData':
            if mapped_field == 'type':
                updated_value = value.lower()
        return updated_value

    def _parse_mapped_fields(self, expression, value, comparator, stix_field, mapped_fields_array):
        comparison_string = ""
        is_reference_value = self._is_reference_value(stix_field)
        value_type = self._check_value_type(expression.value) if is_reference_value else None
        for mapped_field in mapped_fields_array:
            mapped_field = self._sanatize_field(mapped_field, expression.comparator)
            value = self._sanatize_value(mapped_field, value)
            if is_reference_value:
                parsed_reference = self._parse_reference(value_type, mapped_field, value, comparator)

                if not parsed_reference:
                    continue
                comparison_string += parsed_reference
            else:
                comparison_string += "{mapped_field}{comparator}{value}".format(mapped_field=mapped_field, comparator=comparator, value=value)

        return comparison_string

    @staticmethod
    def _is_reference_value(stix_field):
        return stix_field in REFERENCE_FIELDS

    def _lookup_comparison_operator(self, expression_operator):
        if expression_operator not in self.comparator_lookup[self.dialect]:
            raise NotImplementedError("Comparison operator {} unsupported for Infoblox connector {}".format(expression_operator.name, self.dialect))

        return self.comparator_lookup[self.dialect][expression_operator]

    def _calculate_intersection(self, mapped_fields_array, stix_field):
        mapped_fields_set = set(mapped_fields_array)
        intersection = self.assigned_fields.intersection(mapped_fields_set)
        if intersection:
            logger.error("%s mapped from %s has multiple criteria", ', '.join(intersection), stix_field)
            raise NotImplementedError("Multiple criteria for one field is not support in Infoblox connector")

        if self.dialect == 'tideDbData' and stix_field == 'imported':
            # for TIDE imported date field, allow multiple criteria
            return
        self.assigned_fields |= mapped_fields_set

    def _set_threat_type(self, stix_object, stix_field, final_expression, value):
        # NOTE: for the Dossier and TIDE apis, threat_type must be provided. Using the provided query, determine the appropriate type.
        stix_map = {
            'dossierData': [
                {
                    'stix_object': ['domain-name', 'x-infoblox-dossier-event-result-pdns'],
                    'stix_field': ['value', 'hostname_ref.value'],
                    'threat_type': 'host'
                },
                {
                    'stix_object': ['ipv4-addr', 'ipv6-addr', 'x-infoblox-dossier-event-result-pdns'],
                    'stix_field': ['value', 'ip_ref.value'],
                    'threat_type': 'ip'
                }
            ],
            'tideDbData': [
                {
                    'stix_object': ['x-infoblox-threat'],
                    'stix_field': ['host_name'],
                    'threat_type': 'host'
                },
                {
                    'stix_object': ['ipv4-addr', 'ipv6-addr', 'x-infoblox-threat'],
                    'stix_field': ['value', 'ip_ref.value'],
                    'threat_type': 'ip'
                },
                {
                    'stix_object': ['x-infoblox-threat'],
                    'stix_field': ['url'],
                    'threat_type': 'url'
                },
                {
                    'stix_object': ['email-addr', 'x-infoblox-threat'],
                    'stix_field': ['value', 'email_ref.value'],
                    'threat_type': 'email'
                }
            ]
        }

        if self.dialect not in stix_map:
            return

        for mapping in stix_map[self.dialect]:
            threat_type = ''
            if stix_object in mapping['stix_object'] and stix_field in mapping['stix_field']:
                threat_type = mapping['threat_type']

            if stix_object == 'x-infoblox-threat' and stix_field == 'threat_type':
                threat_type = value.lower()

            if threat_type:
                if self.threat_type_map[self.dialect] and self.threat_type_map[self.dialect] != threat_type:
                    raise RuntimeError("Conflicting threat_type found, old={} new={}".format(self.threat_type_map[self.dialect], threat_type))
                self.threat_type_map[self.dialect] = threat_type


    def _parse_expression(self, expression, qualifier=None) -> str:
        if isinstance(expression, ComparisonExpression):  # Base Case
            # Resolve STIX Object Path to a field in the target Data Model
            stix_object, stix_field = expression.object_path.split(':')

            # Multiple data source fields may map to the same STIX Object
            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
            self._calculate_intersection(mapped_fields_array, stix_field)

            # Resolve the comparison symbol to use in the query string (usually just ':')
            comparator = self._lookup_comparison_operator(expression.comparator)

            # Some values are formatted differently based on how they're being compared
            if expression.comparator == ComparisonComparators.Like:
                value = self._format_like(expression.value)
            else:
                value = self._format_equality(expression.value)

            comparison_string = self._parse_mapped_fields(expression, value, comparator, stix_field, mapped_fields_array)
            if qualifier is not None:
                final_expression = "{}{}".format(comparison_string, qualifier)
            else:
                final_expression = "{}".format(comparison_string)

            self._set_threat_type(stix_object, stix_field, final_expression, value)
            return final_expression

        elif isinstance(expression, CombinedComparisonExpression):
            operator = self._lookup_comparison_operator(expression.operator)
            expression_01 = self._parse_expression(expression.expr1)
            expression_02 = self._parse_expression(expression.expr2)
            if not expression_01 or not expression_02:
                return ''

            # NOTE: for complex expressions, this adds () around them
            if isinstance(expression.expr1, CombinedComparisonExpression):
                expression_01 = "{}".format(expression_01)
            if isinstance(expression.expr2, CombinedComparisonExpression):
                expression_02 = "{}".format(expression_02)
            query_string = "{}{}{}".format(expression_01, operator, expression_02)
            if qualifier is not None:
                return "{} {}".format(query_string, qualifier)
            else:
                return "{}".format(query_string)
        elif isinstance(expression, ObservationExpression):
            return self._parse_expression(expression.comparison_expression, qualifier)
        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            if isinstance(expression.observation_expression, CombinedObservationExpression):
                operator = self._lookup_comparison_operator(expression.observation_expression.operator)
                expression_01 = self._parse_expression(expression.observation_expression.expr1)
                # qualifier only needs to be passed into the parse expression once since it will be the same for both expressions
                expression_02 = self._parse_expression(expression.observation_expression.expr2, expression.qualifier)
                return "{} {} {}".format(expression_01, operator, expression_02)
            else:
                return self._parse_expression(expression.observation_expression.comparison_expression, expression.qualifier)
        elif isinstance(expression, CombinedObservationExpression):
            operator = self._lookup_comparison_operator(expression.operator)
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


def _test_or_add_milliseconds(timestamp) -> str:
    if not _test_timestamp(timestamp):
        raise ValueError("Invalid timestamp")
    # remove single quotes around timestamp
    timestamp = re.sub("'", "", timestamp)
    # check for 3-decimal milliseconds
    if not bool(re.search(TIMESTAMP_MILLISECONDS, timestamp)):
        timestamp = re.sub('Z$', '.000Z', timestamp)
    return timestamp


def _test_start_stop_format(query_string) -> bool:
    # Matches STARTt'1234-56-78T00:00:00.123Z'STOPt'1234-56-78T00:00:00.123Z'
    # or START 1234567890123 STOP 1234567890123
    return bool(re.search(START_STOP_STIX_QUALIFIER, query_string))


def _get_parts_start_stop(query):
    # Remove leading 't' before timestamps
    query = re.sub("(?<=START)t|(?<=STOP)t", "", query)
    # Split individual query to isolate timestamps
    query_parts = re.split("(START)|(STOP)", query)
    # Remove None array entries
    query_parts = list(map(lambda x: x.strip(), list(filter(None, query_parts))))
    return query_parts


def _test_timestamp(timestamp) -> bool:
    return bool(re.search(TIMESTAMP, timestamp))


def _format_query_with_timestamp(dialect:str, query: str, time_range) -> str:
    if dialect == 'dnsEventData':
        if _test_start_stop_format(query):
            query_parts = _get_parts_start_stop(query)
            if len(query_parts) != 5:
                logger.info("Omitting query due to bad format for START STOP qualifier timestamp")
                return ''

            # grab time stamps from array
            start_time = _test_or_add_milliseconds(query_parts[2])
            stop_time = _test_or_add_milliseconds(query_parts[4])

            transformer = TimestampToSeconds()
            second_start_time = transformer.transform(start_time)
            second_stop_time = transformer.transform(stop_time)

            return 't0={}&t1={}&{}'.format(str(second_start_time), str(second_stop_time), query_parts[0])

        # default to last X minutes
        totime = int(time.time())
        fromtime = int(totime - datetime.timedelta(minutes=time_range).total_seconds())
        return 't0={}&t1={}&{}'.format(str(fromtime), str(totime), query)

    if dialect == 'tideDbData':
        if _test_start_stop_format(query):
            query_parts = _get_parts_start_stop(query)
            if len(query_parts) != 5:
                logger.info("Omitting query due to bad format for START STOP qualifier timestamp")
                return ''

            # grab time stamps from array
            start_time = _test_or_add_milliseconds(query_parts[2])
            stop_time = _test_or_add_milliseconds(query_parts[4])
            return 'from_date={}&to_date={}&{}'.format(start_time, stop_time, query_parts[0])

        if any(substring in query for substring in ['imported', 'expiration']):
            # IMPROVEMENT: Collapse date formatting earilier in the process. Allowing fields that impact date to be filtered out earilier.
            return query
        return 'period={} minutes&{}'.format(time_range, query)

    # remaining dialect (dossierEvent)
    return _get_parts_start_stop(query)[0]


def _format_translated_queries(dialect, query_array, threat_type_map, time_range):
    # remove empty strings in the array
    query_array = list(map(lambda x: x.strip(), list(filter(None, query_array))))

    # Transform from human-readable timestamp to 10-digit second time
    # Ex. START t'2014-04-25T15:51:20.000Z' to START 1398441080
    formatted_queries = []
    for query in query_array:
        unaltered_query = query
        query = _format_query_with_timestamp(dialect, query, time_range)

        if not query:
            continue

        payload = dict()
        payload['offset'] = 0
        payload['query'] = query

        if dialect in threat_type_map and threat_type_map[dialect]:
            payload['threat_type'] = threat_type_map[dialect]
        formatted_queries.append(payload)

    return formatted_queries


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    trans_queries = QueryStringPatternTranslator(pattern, data_model_mapping, options['time_range']).qualified_queries
    queries = []
    for trans_query in trans_queries:
        trans_query['source'] = data_model_mapping.dialect
        queries.append(json.dumps(trans_query))
    return queries
