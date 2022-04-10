"""
Translates ANTLR parsing of STIX pattern into native (Infoblox API) query.

See: https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/adapter-guide/develop-translation-module.md#step-3-edit-the-query-constructor-file
See: OASIS Specification
    Part 1: https://docs.oasis-open.org/cti/stix/v2.0/stix-v2.0-part1-stix-core.html
    Part 2: https://docs.oasis-open.org/cti/stix/v2.0/stix-v2.0-part2-stix-objects.html
    Part 3: https://docs.oasis-open.org/cti/stix/v2.0/stix-v2.0-part3-cyber-observable-core.html
    Part 4: https://docs.oasis-open.org/cti/stix/v2.0/stix-v2.0-part4-cyber-observable-objects.html
    Part 5: https://docs.oasis-open.org/cti/stix/v2.0/stix-v2.0-part5-stix-patterning.html
"""

import datetime
import json
import logging
import re
import time

from stix_shifter_utils.stix_translation.src.json_to_stix import observable
from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import (
    ObservationExpression, ComparisonExpression,
    ComparisonExpressionOperators, ComparisonComparators, Pattern,
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators,
    StartStopQualifier
)
from .transformers import InfobloxToDomainName, TimestampToSeconds

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
TIMESTAMP_MILLISECONDS = r"\.\d+Z$"

THREAT_LEVEL_MAPPING = {
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1
}

logger = logging.getLogger(__name__)

class DuplicateFieldException(Exception):
    """
    Exception thrown when multiple query fields of the same type (ie host or ip) are provided. Infoblox APIs currently
    do not support this type of qerying.
    """
    pass

class QueryStringPatternTranslator:
    """
    Class that handles the translations of the ANTLR parsing to native query.

    :param pattern: ANTRL parsing Pattern
    :param data_model_mapper: Data model mapper used to aid the translation of the ANTRL parsing pattern to native.
                            See: https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/adapter-guide/supported-mappings.md
                            See: https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/adapter-guide/develop-translation-module.md#step-2-edit-the-from_stix_map-json-files
    :type data_model_mapper: QueryTranslator
    :param time_range: Default time range to query over (in minutes).
    :type time_range: int

    Attributes:
        comparator_lookup (map): Mapping, per dialect, of the ANTLR comparison operators and their native equivalent. Used in the tranlation process.
        qualified_queries (list): List of Infoblox translated & formatted queries. Queries are simply the HTTP query parameters for the specific APIs.
    """

    def __init__(self, pattern: Pattern, data_model_mapper, time_range):
        self.dmm = data_model_mapper
        self.comparator_lookup = self.dmm.map_comparator()
        self.pattern = pattern
        self.using_operators = set()
        self.assigned_fields = set()
        self.qualified_queries = []
        self.dialect = data_model_mapper.dialect
        self.translated = self.parse_expression(pattern)

        self.qualified_queries = self.translated
        self.qualified_queries = _format_translated_queries(self.dialect,
                                                            self.qualified_queries,
                                                            time_range)

    @staticmethod
    def _format_equality(value) -> str:
        """
        Given a value taken from ANTLR parsing, formats it in preparation for insertion into an equality expression.
        NOTE: For Infoblox, this simply stringifies the value.

        :param value: query value
        :type value: int/str
        :return: equality equation
        :rtype: str
        """
        return '{}'.format(value)

    @staticmethod
    def _format_like(value) -> str:
        """
        Given a value taken from ANTLR parsing, formats it in preparation for insertion into a like expression.
        NOTE: For Infoblox, this simply stringifies the value.

        :param value: query value
        :type value: int/str
        :return: equality equation
        :rtype: str
        """
        return "{}".format(value)

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

    @staticmethod
    def _parse_reference(value_type, mapped_field, value, comparator):
        """
        Translate reference ANTRL parsing to query (eg src_ref.value => qip).

        :param value_type: type of value (eg ipv4)
        :type value_type: str
        :param mapped_field: native field pointed to by the reference (eg qip for src_ref.value)
        :type mapped_field: str
        :param value: value (127.0.0.1)
        :type value: int/str
        :param comparator: comparison operator (eg =)
        :type comparator: str
        :return: native query segment
        :rtype: str
        """
        if value_type not in REFERENCE_DATA_TYPES["{}".format(mapped_field)]:
            return None
        else:
            return "{mapped_field}{comparator}{value}".format(
                mapped_field=mapped_field, comparator=comparator, value=value)

    def _sanatize_field(self, mapped_field, comparator):
        """
        Special handling/sanitation of fields after translation to yield the desired results for the native query.
        Currently this includes:
        - Special handling for the imported_from_date & imported_to_date query parameters
        - Excluding fields that do not support LIKE. The stix_map specification does not allow the granularity (on a field by field basis) of
            defining which comparison operators are supported by which fields. For some of Infoxblox APIs, some fields support LIKE while others do not.
        - Translate LIKE comparison operations to use the `text_search` query param for the `tideDbData` dialect.

        :param mapped_field: native field pointed to by the reference (eg qip for src_ref.value)
        :type mapped_field: str
        :param comparator: comparison operator (eg Eq)
        :type comparator: ComparisonComparators
        :return: updated field name for native query
        :rtype: str
        """
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
        """
        Special handling/sanitation of values after translation to yield the desired results for the native query.
        Currently this includes:
        - Transforming any values of Domain/Hostname type to match expected Infoblox format (example.com.)
        - Translating threat level (eg HIGH) to its numerical representation (eg 3)
        - Lower-casing values for the `type` field for the `tideDbData` dialect

        :param mapped_field: native field pointed to by the reference (eg qip for src_ref.value)
        :type mapped_field: str
        :param value: value (127.0.0.1)
        :type value: int/str
        :return: updated value for native query
        :rtype: str
        """
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
        """
        Parse ANTLR parsing expression into native query (HTTP API quary params).

        Expression is separated from the field name, comparator operator, and value. Fields and values are sanatized and mapped
        to the native equivalent. Reference expressions are translated into their native equivalent.

        :param expression: STIX ANTLR expression
        :type expression: ObservationExpression or ComparisonExpression
        :param value: value (eg 127.0.0.1)
        :type value: int/str
        :param comparator: comparison operator (eg =)
        :type comparator: str
        :param stix_field: ANTLR STIX field
        :type stix_field: str
        :param mapped_fields_array: list of native fields related to `stix_field`, this is based on the data_model_mapper/dmm
        :type mapped_fields_array: list<str>
        :return: translated native query expression
        :rtype: str
        """
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
        """
        Determine if the provided ANTLR STIX field is a reference (eg src_ref.value)

        :param stix_field: ANTLR STIX field
        :type stix_field: str
        :return: True if the provided field is a reference; False otherwise.
        :rtype: bool
        """
        return stix_field in REFERENCE_FIELDS

    def _lookup_comparison_operator(self, expression_operator):
        """
        Translate STIX expression operator (eg ObservationOperators & ComparisonComparators) to their native query equivalent.

        NOTE: Since all queries are fundamentally HTTP query params (field1 = value1 & field2 = value2). The translated operator
        will always be either one of `&` or `=`.

        :param expression_operator: STIX operator
        :type expression_operator: ObservationOperators & ComparisonComparators
        :return: native conparison operator
        :rtype: str
        :throw: NotImplementedError if expression_operator not found in comparator_lookup
        """
        if str(expression_operator) not in self.comparator_lookup:
            raise NotImplementedError("Comparison operator {} unsupported for Infoblox connector {}".format(expression_operator.name, self.dialect))

        return self.comparator_lookup[str(expression_operator)]

    def _calculate_intersection(self, mapped_fields_array, stix_field, assigned_fields):
        """
        Calculates whether multiple query criteria apply to the same native field.

        NOTE: In some scenarios, like with `tideDbData` dialect `imported` field, duplicates are allowed. In those cases, `assigned_fields`
        is not updated to signify the field was processed.

        :param mapped_fields_array: list of native fields related to `stix_field`, this is based on the data_model_mapper/dmm
        :type mapped_fields_array: list<str>
        :param stix_field: ANTLR STIX field
        :type stix_field: str
        :param assigned_fields: map of currently processed fields. Newly processed field `stix_field` is checked against it to determine if it has previously been processed
        :type assigned_fields: map
        :throw: DuplicateFieldException if multiple criteria found for the same field
        """
        mapped_fields_set = set(mapped_fields_array)
        assigned_fields_set = set(assigned_fields.keys())
        intersection = assigned_fields_set.intersection(mapped_fields_set)
        if intersection:
            raise DuplicateFieldException("Multiple criteria for one field is not support in Infoblox connector, field={}, duplicates={}".format(', '.join(intersection), stix_field))

        if self.dialect == 'tideDbData' and stix_field == 'imported':
            # for TIDE imported date field, allow multiple criteria
            return

        for field in mapped_fields_array:
            assigned_fields[field] = 1

    def _set_threat_type(self, stix_object, stix_field, final_expression, value):
        """
        Determine Infoblox threat type based on stix_object and stix_field.

        NOTE: This is used to select the particular URL path. For example, domainName queries for Dossier will use a path <hostname>/host.
        While ipv4 queries for Dossier will use a path of <hostname>/ip.

        :param stix_object: STIX object
        :type stix_object: str
        :param stix_field: STIX field
        :type stix_field: str
        :param final_expression: native query expression
        :type final_expression: str
        :param value: value (eg 127.0.0.1)
        :type value: int/str
        :return: threat type (host, url, email, ip)
        :rtype: str
        """
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
                    'stix_object': ['domain-name', 'x-infoblox-threat'],
                    'stix_field': ['value', 'host_name', 'domain_ref.value'],
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
            threat_type = None
            if stix_object in mapping['stix_object'] and stix_field in mapping['stix_field']:
                threat_type = mapping['threat_type']

            if stix_object == 'x-infoblox-threat' and stix_field == 'threat_type':
                threat_type = value.lower()

            if threat_type:
                return threat_type
        return

    def _merge_queries_in_expression(self, expression_01, expression_02, operator):
        """
        Merge two query expressions into a single expression.

        NOTE: For complex queries, this parser class recursively traverses the ANTLR expressions until it reaches a simple comparison
        operations. After translating the expression, a list of queries is generated. This method helps stitch the potentially multiple
        lists of queries into a single list of native queries to transmit. During the merge operation, the threat type of the individual
        components are compared. This module currently does not support queries that translate to multiple different threat types (eg ip and host).

        :param expression_01: LH query expression
        :type expression_01: list
        :param expression_02: RH query expression
        :type expression_02: list
        :param operator: comparison operator for the two expressions, determines how they should be joined (AND or OR)
        :type operator: str
        :return: query expression
        :rtype: list
        :throw: RuntimeError if multiple different threat type queries provided
        :throw: assertError if both expressions have more than one query, in that situation the queries are too large.
        """
        assert not (len(expression_01) > 1 and len(expression_02) > 1), "Failed to merge queries, expressions too complex"

        expression_small = expression_01 if len(expression_01) == 1 else expression_02
        expression_large = expression_02 if expression_small == expression_01 else expression_01

        # determine threat_type from individual queries
        threat_type_array = [i['threatType'] for i in (expression_01 + expression_02) if i['threatType']]
        threat_type_set = set(threat_type_array)
        if len(threat_type_set) > 1:
            raise RuntimeError("Conflicting threat_type found, {}".format(sorted(threat_type_set)))

        for query in expression_large:
            merging_expression = expression_small[0]
            query['query'] = operator.join([merging_expression['query'], query['query']])
            query['threatType'] = merging_expression['threatType'] if merging_expression['threatType'] else query['threatType']

        return expression_large

    def _parse_expression(self, expression, qualifier=None, intersection_fields=None) -> str:
        """
        Recursively called method for parsing an ANTLR expression. For complex expressions, like ObservationExpression, LH & RH expressions
        are separated and processed independently before being merged back together.

        Merge two query expressions into a single expression.

        NOTE: For complex queries, this parser class recursively traverses the ANTLR expressions until it reaches a simple comparison
        operations. After translating the expression, a list of queries is generated. This method helps stitch the potentially multiple
        lists of queries into a single list of native queries to transmit. During the merge operation, the threat type of the individual
        components are compared. This module currently does not support queries that translate to multiple different threat types (eg ip and host).

        :param expression: STIX expression to parse
        :type expression: stix_shifter_utils.stix_translation.src.patterns.pattern_object.*
        :param qualifier: STIX qualifier, propagates START/STOP qualifier (on complex expressions) to the necessary basic comparison expression
        :type qualifier: stix_shifter_utils.stix_translation.src.patterns.pattern_objects import StartStopQualifier
        :param intersection_fields: map maintaining already processed field, used by _calculate_intersection to determine multiple criteria
                                    of a single field.
        :type intersection_fields: map
        :return: native query expression
        :rtype: str
        :throw: RuntimeError if unknown expression type provided
        """
        if isinstance(expression, ComparisonExpression):
            # Resolve STIX Object Path to a field in the target Data Model
            stix_object, stix_field = expression.object_path.split(':')

            # Multiple data source fields may map to the same STIX Object
            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)

            if intersection_fields is not None:
                self._calculate_intersection(mapped_fields_array, stix_field, intersection_fields)
            else:
                assigned_fields = dict()
                self._calculate_intersection(mapped_fields_array, stix_field, assigned_fields)

            # Resolve the comparison symbol to use in the query string (usually just ':')
            comparator = self._lookup_comparison_operator(expression.comparator)

            # Some values are formatted differently based on how they're being compared
            if expression.comparator == ComparisonComparators.Like:
                value = self._format_like(expression.value)
            else:
                value = self._format_equality(expression.value)

            final_expression = self._parse_mapped_fields(expression, value, comparator, stix_field, mapped_fields_array)
            threatType = self._set_threat_type(stix_object, stix_field, final_expression, value)
            return [{'query': final_expression, 'threatType': threatType, 'startStopTime': qualifier}]

        elif isinstance(expression, CombinedComparisonExpression):
            operator = self._lookup_comparison_operator(expression.operator)

            # NOTE: APIs do not support duplicate criteria (example domain-name=d1.com AND domain-name=d2.com). As a workaround, the expression
            #   will be split into multiple independent queries.
            exp1_fields = dict()
            use_two_queries = True
            try:
                # Process LHS of expression, intersections here is an invalid query, stop processing.
                expression_01 = self._parse_expression(expression.expr1, qualifier, exp1_fields)
            except DuplicateFieldException as error:
                logger.error("%s", error)
                raise NotImplementedError("{}".format(error))

            try:
                # Process RHS of expression, if intersections are found re-attempt parsing but as two separate queries.
                expression_02 = self._parse_expression(expression.expr2, qualifier, exp1_fields)
            except DuplicateFieldException as error:
                try:
                    exp2_fields = dict()
                    expression_02 = self._parse_expression(expression.expr2, qualifier, exp2_fields)
                    use_two_queries = False
                except DuplicateFieldException as error:
                    logger.error("%s", error)
                    raise NotImplementedError("{}".format(error))

            assert expression_01 and expression_02, "Failed to parse one side of the expression"

            # NOTE: Merging the two list of queries this would be for expressions with `OR` or `AND` (with duplicate criteria). For
            #   expressions with `AND` (but with different criteria), then the list of queries on one side of the expression will be concatenated together.
            result = expression_01 + expression_02
            if expression.operator == ComparisonExpressionOperators.And and use_two_queries:
                result = self._merge_queries_in_expression(expression_01, expression_02, operator)
            return result
        elif isinstance(expression, ObservationExpression):
            result = self._parse_expression(expression.comparison_expression, qualifier, intersection_fields)
            return result
        elif isinstance(expression, StartStopQualifier) and hasattr(expression, 'observation_expression'):
            return self._parse_expression(getattr(expression, 'observation_expression'), expression.qualifier, intersection_fields)
        elif isinstance(expression, CombinedObservationExpression):
            exp1_fields = dict()
            exp2_fields = dict()
            expression_01 = self._parse_expression(expression.expr1, qualifier, exp1_fields)
            expression_02 = self._parse_expression(expression.expr2, qualifier, exp2_fields)

            result = expression_01 + expression_02
            return result
        elif isinstance(expression, Pattern):
            result = self._parse_expression(expression.expression)
            return result
        else:
            raise RuntimeError("Unknown Recursion Case for expression={}, type(expression)={}".format(
                expression, type(expression)))

    def parse_expression(self, pattern: Pattern):
        """
        Entry point for parsing an ANTLR pattern.

        :param pattern: STIX expression to parse
        :type pattern: Pattern
        :return: native query expression
        :rtype: str
        """
        return self._parse_expression(pattern)


def _test_or_add_milliseconds(timestamp) -> str:
    """
    Validates and reformats (if necessary) timestamp from the START/STOP qualifier

    :param timestamp: timestamp string (eg 1234-56-78T00:00:00.123Z)
    :type timestamp: str
    :return: sanatized timestamp string
    :rtype: str
    """
    # remove single quotes around timestamp
    timestamp = re.sub("'", "", timestamp)
    # check for 3-decimal milliseconds
    if not bool(re.search(TIMESTAMP_MILLISECONDS, timestamp)):
        timestamp = re.sub('Z$', '.000Z', timestamp)
    return timestamp


def _test_start_stop_format(query_string) -> bool:
    """
    Checks if query_string contains START/STOP qualifier.

    :param query_string: query string
    :type query_string: str
    :return: True if provided query_string contains START/STOP qualifier.
    :rtype: bool
    """
    # Matches STARTt'1234-56-78T00:00:00.123Z'STOPt'1234-56-78T00:00:00.123Z'
    # or START 1234567890123 STOP 1234567890123
    return bool(re.search(START_STOP_STIX_QUALIFIER, query_string))


def _get_parts_start_stop(query):
    """
    Checks if query_string contains START/STOP qualifier.

    :param query_string: query string
    :type query_string: str
    :return: True if provided query_string contains START/STOP qualifier.
    :rtype: bool
    """
    # Remove leading 't' before timestamps
    query = re.sub("(?<=START)t|(?<=STOP)t", "", query)
    # Split individual query to isolate timestamps
    query_parts = re.split("(START)|(STOP)", query)
    # Remove None array entries
    query_parts = list(map(lambda x: x.strip(), list(filter(None, query_parts))))
    return query_parts


def _format_query_with_timestamp(dialect:str, query: str, time_range, start_stop_time) -> str:
    """
    Based on dialect, format time range for the query.

    NOTE:
    - If START/STOP qualifier not provided, default configuration `time_range` is used.
    - If START/STOP qualifier is provided, the timestamps are parsed out and formatted.
    - Each dialect has a different way to represent a time range in the native query (DnsEvent uses t0/t1 while TideDB uses from_date/to_date)

    :param dialect: dialect for the query (eg dnsEventData, tideDbData, etc)
    :type dialect: str
    :param query: original query string
    :type query: str
    :param time_range: default time range to query over (in minutes).
    :type time_range: int
    :param start_stop_time: qualifier start/stop time (eg STARTt'1234-56-78T00:00:00.123Z'STOPt'1234-56-78T00:00:00.123Z')
    :type start_stop_time: str
    :return: query with start/stop time query parameters added
    :rtype: str
    """
    if dialect == 'dnsEventData':
        if start_stop_time and _test_start_stop_format(start_stop_time):
            query_parts = _get_parts_start_stop(start_stop_time)

            # grab time stamps from array
            start_time = _test_or_add_milliseconds(query_parts[1])
            stop_time = _test_or_add_milliseconds(query_parts[3])

            transformer = TimestampToSeconds()
            second_start_time = transformer.transform(start_time)
            second_stop_time = transformer.transform(stop_time)

            return 't0={}&t1={}&{}'.format(str(second_start_time), str(second_stop_time), query)

        # default to last X minutes
        totime = int(time.time())
        fromtime = int(totime - datetime.timedelta(minutes=time_range).total_seconds())
        return 't0={}&t1={}&{}'.format(str(fromtime), str(totime), query)

    if dialect == 'tideDbData':
        if start_stop_time and _test_start_stop_format(start_stop_time):
            query_parts = _get_parts_start_stop(start_stop_time)

            # grab time stamps from array
            start_time = _test_or_add_milliseconds(query_parts[1])
            stop_time = _test_or_add_milliseconds(query_parts[3])

            transformer = TimestampToSeconds()
            second_start_time = transformer.transform(start_time)
            second_stop_time = transformer.transform(stop_time)

            return 'from_date={}&to_date={}&{}'.format(start_time, stop_time, query)

        if any(substring in query for substring in ['imported', 'expiration']):
            return query
        return 'period={} minutes&{}'.format(time_range, query)

    return query


def _format_translated_queries(dialect, entry_array, time_range):
    """
    Performs final formatting for queries. See: https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/adapter-guide/develop-translation-module.md#step-2-edit-the-from_stix_map-json-files


    Operations include:
    - Parsing START/STOP qualifier and adding the appropriate native time fields to the query
    - Format queries into a list of maps with sufficient data (offset, query, threat_type, etc) for transmission to process.

    :param dialect: dialect for the query (eg dnsEventData, tideDbData, etc)
    :type dialect: str
    :param entry_array: list of queries to finalize
    :type entry_array: list
    :param time_range: default time range to query over (in minutes).
    :type time_range: int
    :return: list of queries
    :rtype list
    """
    # Transform from human-readable timestamp to 10-digit second time
    # Ex. START t'2014-04-25T15:51:20.000Z' to START 1398441080
    formatted_queries = []
    for entry in entry_array:
        query = entry['query']
        if not query or not query.strip():
            # ignore empty queries
            continue
        query = _format_query_with_timestamp(dialect, query, time_range, entry['startStopTime'])

        payload = dict()
        payload['offset'] = 0
        payload['query'] = query

        if 'threatType' in entry:
            payload['threat_type'] = entry['threatType']

        formatted_queries.append(payload)

    return formatted_queries


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    """
    Entry point for query_constructor. Initializes QueryStringPatternTranslator, parses the provided pattern, and returns a formatted query.

    :param pattern: STIX pattern to parse
    :type pattern: Pattern
    :param data_model_mapping: data model mapping, see: https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/adapter-guide/develop-translation-module.md
    :type data_model_mapping: QueryTranslator
    :param options: configuration options, see: https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/adapter-guide/develop-configuration-json.md
    :type options: object
    :return: list of queries
    :rtype list
    """
    trans_queries = QueryStringPatternTranslator(pattern, data_model_mapping, options['time_range']).qualified_queries
    queries = []
    for trans_query in trans_queries:
        trans_query['source'] = data_model_mapping.dialect
        queries.append(json.dumps(trans_query))
    return queries
