from stix_shifter.stix_translation.src.patterns.pattern_objects import ObservationExpression, ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators
from stix_shifter.stix_translation.src.transformers import TimestampToMilliseconds
from stix_shifter.stix_translation.src.json_to_stix import observable
import logging
import json
import re
import uuid

logger = logging.getLogger(__name__)

REFERENCE_DATA_TYPES = {"sourceip": ["ipv4", "ipv6", "ipv4_cidr"],
                        "sourcemac": ["mac"],
                        "destinationip": ["ipv4", "ipv6", "ipv4_cidr"],
                        "destinationmac": ["mac"]}


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

    def __init__(self, pattern: Pattern, data_model_mapper, options):
        self.result_limit = options['result_limit']
        self.timerange = options['timerange']
        self.dmm = data_model_mapper
        self.select_statement = self.dmm.map_selections()
        self.pattern = pattern
        # Object structure of query attributes in the format of:
        # {observation_group_uuid: {comparision_group_uuid: { query, comparision_operator, qualifier, observation_operator }}}
        self.grouped_queries = {}
        self.translated = self.parse_expression(pattern)
        # Final array of translated query strings
        self.translated_queries = _parse_translated_query_objects(self)

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
        if expression.comparator == ComparisonComparators.Matches:  # needs forward slashes
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

    def _parse_expression(self, expression, qualifier=None, comparision_operator=None, comparision_group=None, observation_group=None, observation_operator=None) -> str:
        if isinstance(expression, ComparisonExpression):  # Base Case
            if not comparision_group:
                comparision_group = str(uuid.uuid4())
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
                grouped_comparison_string = "(" + comparison_string + ")"
                comparison_string = grouped_comparison_string

            if expression.comparator == ComparisonComparators.NotEqual:
                comparison_string = self._negate_comparison(comparison_string)

            if expression.negated:
                comparison_string = self._negate_comparison(comparison_string)

            if qualifier:
                # Transform from human-readable timestamp to 13-digit millisecond time
                # Ex. START t'2014-04-25T15:51:20.000Z' to START 1398441080000
                qualifier = re.sub("(?<=START)t|(?<=STOP)t", "", qualifier)
                start_stop_array = qualifier.split('START')[1].split('STOP')
                qualifier = _convert_timestamps_to_milliseconds(start_stop_array)

            query_attributes = {'query': comparison_string,
                                'qualifier': qualifier,
                                'comparision_operator': comparision_operator,
                                'comparision_group': comparision_group,
                                'observation_group': observation_group,
                                'observation_operator': observation_operator}
            if observation_group not in self.grouped_queries:
                self.grouped_queries[observation_group] = {}
            if comparision_group not in self.grouped_queries[observation_group]:
                self.grouped_queries[observation_group][comparision_group] = [query_attributes]
            else:
                self.grouped_queries[observation_group][comparision_group].append(query_attributes)

        elif isinstance(expression, CombinedComparisonExpression):
            # Record if AND, group
            comparision_operator = self.comparator_lookup[expression.operator]
            comparision_group = str(uuid.uuid4())

            self._parse_expression(expression.expr1, qualifier=qualifier, comparision_operator=comparision_operator,
                                   comparision_group=comparision_group, observation_group=observation_group, observation_operator=observation_operator)
            self._parse_expression(expression.expr2, qualifier=qualifier, comparision_operator=comparision_operator,
                                   comparision_group=comparision_group, observation_group=observation_group, observation_operator=observation_operator)
        elif isinstance(expression, ObservationExpression):
            if not observation_group:
                observation_group = str(uuid.uuid4())
            self._parse_expression(expression.comparison_expression, qualifier=qualifier, comparision_operator=comparision_operator,
                                   comparision_group=comparision_group, observation_group=observation_group, observation_operator=observation_operator)
        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            qualifier = expression.qualifier
            if not observation_group:
                observation_group = str(uuid.uuid4())
            if isinstance(expression.observation_expression, CombinedObservationExpression):
                observation_operator = self.comparator_lookup[expression.observation_expression.operator]

                self._parse_expression(expression.comparison_expression, qualifier=qualifier, comparision_operator=comparision_operator,
                                       comparision_group=comparision_group, observation_group=observation_group, observation_operator=observation_operator)
            else:
                self._parse_expression(expression.observation_expression.comparison_expression, qualifier=qualifier, comparision_operator=comparision_operator,
                                       comparision_group=comparision_group, observation_group=observation_group, observation_operator=observation_operator)
        elif isinstance(expression, CombinedObservationExpression):
            observation_operator = self.comparator_lookup[expression.operator]
            self._parse_expression(expression.expr1, qualifier=qualifier, comparision_operator=comparision_operator,
                                   comparision_group=comparision_group, observation_group=observation_group, observation_operator=observation_operator)

            self._parse_expression(expression.expr2, qualifier=qualifier, comparision_operator=comparision_operator,
                                   comparision_group=comparision_group, observation_group=observation_group, observation_operator=observation_operator)
        elif isinstance(expression, Pattern):
            self._parse_expression(expression.expression)
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
    pattern = "\.\d+Z$"
    if not bool(re.search(pattern, timestamp)):
        timestamp = re.sub('Z$', '.000Z', timestamp)
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
    start_time = _test_or_add_milliseconds(query_parts[0])
    stop_time = _test_or_add_milliseconds(query_parts[1])
    transformer = TimestampToMilliseconds()
    millisecond_start_time = transformer.transform(start_time)
    millisecond_stop_time = transformer.transform(stop_time)
    return "START {} STOP {}".format(str(millisecond_start_time), str(millisecond_stop_time))


def _parse_translated_query_objects(self):
    grouped_queries = self.grouped_queries
    selections_string = "SELECT {} FROM events WHERE".format(self.select_statement)
    limit_string = "limit {}".format(self.result_limit)
    default_time_string = "last {} minutes".format(self.timerange)
    formatted_queries = []
    unqualified_queries = []
    unqualified_query = ''

    for observation_key, observation_object in grouped_queries.items():  # A single [ ]
        query_string = ''
        observation_element_count = len(observation_object.items())
        qualifier = None
        observation_operator = None
        for comparison_key, comparison_object_array in observation_object.items():
            break_to_outer_loop = False  # Array of one or more comparision statements joined by AND/OR
            comparison_string = "(" if len(comparison_object_array) > 1 else ""
            for obj in comparison_object_array:  # Single comparision statement
                pattern = "NOMAP\:([a-zA-Z\d]){8}-(([a-zA-Z\d]){4}-){3}([a-zA-Z\d]){12}"
                match = re.search(pattern, obj['query'])

                single_observation_single_comparison = (len(grouped_queries.items()) == 1 and len(comparison_object_array) == 1)
                single_observation_multi_and_comparisons = (obj['comparision_operator'] == 'AND' and len(grouped_queries.items()) == 1)

                if match:
                    # Skip unmapped comparison but include comparison joined by the OR
                    if (obj['comparision_operator'] == 'OR'):
                        continue
                    # TODO: Property handle case where there may be other ORed comparisons in the observation.
                    # This is the single_observation_multi_and_comparisons condition
                    # May need to build up the comparison string differently to handle this

                    elif (single_observation_single_comparison or single_observation_multi_and_comparisons):
                        error_id = match[0].split(":")[1]
                        raise self.dmm.mapping_errors[error_id]
                    elif (obj['comparision_operator'] == 'AND'):
                        comparison_string = ''
                        break_to_outer_loop = True
                        break
                    else:
                        continue

                comparison_string += obj['query']
                if obj['comparision_operator']:
                    comparison_string += " {} ".format(obj['comparision_operator'])
            if break_to_outer_loop:
                break
            if len(comparison_object_array) > 1:
                comparison_string = re.sub("\s(OR|AND)\s?$", ")", comparison_string)
            query_string += comparison_string
        qualifier = comparison_object_array[0]['qualifier']

        if qualifier and query_string:
            formatted_queries.append("{} {} {} {}".format(selections_string, query_string, limit_string, qualifier))
        elif query_string:
            unqualified_queries.append(query_string)

    if unqualified_queries:
        if len(unqualified_queries) == 1:
            formatted_queries.append("{} {} {} {}".format(selections_string, unqualified_queries[0], limit_string, default_time_string))
        else:
            unqualified_query_string = ''
            for index, value in enumerate(unqualified_queries):
                unqualified_query_string += "({})".format(value)
                if index < len(unqualified_queries) - 1:
                    unqualified_query_string += ' OR '
            formatted_queries.append("{} {} {} {}".format(selections_string, unqualified_query_string, limit_string, default_time_string))

    return formatted_queries


def translate_pattern(pattern: Pattern, data_model_mapping, options):

    return AqlQueryStringPatternTranslator(pattern, data_model_mapping, options).translated_queries
