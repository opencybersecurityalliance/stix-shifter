from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators
from stix_shifter_utils.stix_translation.src.utils.transformers import TimestampToMilliseconds
from stix_shifter_utils.stix_translation.src.json_to_stix import observable
from stix_shifter_utils.utils import logger
from stix_shifter_utils.utils.file_helper import read_json
import re

logger = logger.set_logger(__name__)

REFERENCE_DATA_TYPES = {"sourceip": ["ipv4", "ipv6", "ipv4_cidr", "ipv6_cidr"],
                        "sourcemac": ["mac"],
                        "destinationip": ["ipv4", "ipv6", "ipv4_cidr", "ipv6_cidr"],
                        "destinationmac": ["mac"],
                        "sourcev6": ["ipv6", "ipv6_cidr"],
                        "destinationv6": ["ipv6", "ipv6_cidr"]}

FILTERING_DATA_TYPES = {"x-qradar:INOFFENSE": "INOFFENSE"}

START_STOP_STIX_QUALIFIER = "START((t'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z')|(\s\d{13}\s))STOP"
TIMESTAMP = "^'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z'$"
TIMESTAMP_MILLISECONDS = "\.\d+Z$"


class AqlQueryStringPatternTranslator:

    def __init__(self, pattern: Pattern, data_model_mapper, result_limit, options):
        self.options = options
        self.dmm = data_model_mapper
        self.comparator_lookup = self.dmm.map_comparator()
        self.pattern = pattern
        self.result_limit = result_limit
        # List for any queries that are split due to START STOP qualifier
        self.qualified_queries = []
        # Translated query string without any qualifiers
        self.translated = self.parse_expression(pattern)
        self.qualified_queries.append(self.translated)
        self.qualified_queries = _format_translated_queries(self.qualified_queries)

    @staticmethod
    def _format_in(values) -> str:
        gen = values.element_iterator()
        return "({})".format(', '.join("'{}'".format(value) for value in gen))

    @staticmethod
    def _format_match(value) -> str:
        return "\'{}\'".format(value)

    @staticmethod
    def _format_equality(value) -> str:
        return '\'{}\''.format(value)

    @staticmethod
    def _format_like(value) -> str:
        return "'%{value}%'".format(value=value)

    @staticmethod
    def _escape_value(value, comparator=None) -> str:
        if isinstance(value, str):
            return '{}'.format(value.replace('\"', '\\"').replace('(', '\\(').replace(')', '\\)'))
        else:
            return value

    @staticmethod
    def _negate_comparison(comparison_string):
        return "NOT ({})".format(comparison_string)

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
            if (mapped_field == 'sourceip' or mapped_field == 'destinationip') and comparator.upper() == 'LIKE':
                return "str({mapped_field}) {comparator} {value}".format(
                    mapped_field=mapped_field, comparator=comparator, value=value)
            elif (mapped_field == 'sourceip' or mapped_field == 'destinationip') and comparator.upper() == 'IN':
                return "str({mapped_field}) {comparator} {value}".format(
                    mapped_field=mapped_field, comparator=comparator, value=value)
            else:
                return None
        # These next two checks wouldn't be needed if events and flows used their own to-STIX mapping
        # This is here because both events and flows map sourceip and destinationip, but in different ways
        if value_type in REFERENCE_DATA_TYPES['sourcev6'] and (mapped_field == 'sourceip' or mapped_field == 'destinationip') and self.dmm.dialect == 'flows':
            return None
        if value_type not in REFERENCE_DATA_TYPES['sourcev6'] and (mapped_field == 'sourcev6' or mapped_field == 'destinationv6') and self.dmm.dialect == 'flows':
            return None
        if value_type == 'ipv4_cidr' or value_type == 'ipv6_cidr':
            # Comparator originally came in as '=' so it must be changed to INCIDR
            comparator = self.comparator_lookup["ComparisonComparators.IsSubSet"]
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
            if expression.object_path in FILTERING_DATA_TYPES.keys():
                comparison_string += "{}({})".format(FILTERING_DATA_TYPES[expression.object_path], value)
            elif expression.comparator == ComparisonComparators.IsSubSet:
                comparison_string += comparator + "(" + "'" + value + "'," + mapped_field + ")"
            elif is_reference_value:
                parsed_reference = self._parse_reference(self, stix_field, value_type, mapped_field, value, comparator)
                if not parsed_reference:
                    continue
                comparison_string += parsed_reference
            # For [ipv4-addr:value = <CIDR value>]
            elif bool(re.search(observable.REGEX['ipv4_cidr'], str(expression.value))):
                comparison_string += "INCIDR(" + value + "," + mapped_field + ")"
            elif (expression.object_path == 'ipv4-addr:value'
                  or expression.object_path == 'ipv6-addr:value'
                  or expression.object_path == 'network-traffic:dst_ref.value'
                  or expression.object_path == 'network-traffic:src_ref.value') \
                  and expression.comparator == ComparisonComparators.Like:
                      comparison_string += "str({mapped_field}) {comparator} {value}".format(mapped_field=mapped_field,
                                                                                             comparator=comparator,
                                                                                             value=value)
            else:
                # There's no aql field for domain-name. using Like operator to find domian name from the url
                if mapped_field == 'domainname' and comparator != ComparisonComparators.Like:
                    comparator = self.comparator_lookup["ComparisonComparators.Like"]
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
    def _lookup_comparison_operator(self, expression_operator):
        if str(expression_operator) not in self.comparator_lookup:
            raise NotImplementedError("Comparison operator {} unsupported for QRadar connector".format(expression_operator.name))
        return self.comparator_lookup[str(expression_operator)]

    @staticmethod
    def _parse_combined_observation_expression(self, expression):
        operator = self._lookup_comparison_operator(self, expression.operator)
        expression_01 = self._parse_expression(expression.expr1)
        expression_02 = self._parse_expression(expression.expr2)
        if expression_01 and expression_02:
            return "{} {} {}".format(expression_01, operator, expression_02)
        elif expression_01:
            return "{}".format(expression_01)
        elif expression_02:
            return "{}".format(expression_02)
        else:
            return ''

    @staticmethod
    def _parse_observation_expression(self, expression, qualifier=None):
        return "{}".format(self._parse_expression(expression.comparison_expression, qualifier))

    @staticmethod
    def _parse_combined_comparison_expression(self, expression, qualifier=None):
        operator = self._lookup_comparison_operator(self, expression.operator)

        # TEXT SEARCH operator is special case. Parsing combined expression of artifact:payload_bin translated into invalid aql query
        # Two TEXT SEARCH operator cannot be used in a single aql query thats why two expressions are not passed into _parse_expression()
        # Instead we can just construct the query string by adding two values with the oprators
        if isinstance(expression.expr1, ComparisonExpression) and (expression.expr1.object_path == 'artifact:payload_bin' 
            and expression.expr1.comparator == ComparisonComparators.Like 
            and expression.expr2.object_path == 'artifact:payload_bin' 
            and expression.expr2.comparator == ComparisonComparators.Like):
            
            query_string = "TEXT SEARCH '{} {} {}' ".format(expression.expr1.value, operator, expression.expr2.value)
        else:
            expression_01 = self._parse_expression(expression.expr1)
            expression_02 = self._parse_expression(expression.expr2)
            if not expression_01 or not expression_02:
                return ''
            if isinstance(expression.expr1, CombinedComparisonExpression):
                expression_01 = "({})".format(expression_01)
            if isinstance(expression.expr2, CombinedComparisonExpression):
                expression_02 = "({})".format(expression_02)
            query_string = "{} {} {}".format(expression_01, operator, expression_02)

        if qualifier:
            self.qualified_queries.append("{} limit {} {}".format(query_string, self.result_limit, qualifier))
            return ''
        else:
            return "{}".format(query_string)

    @staticmethod
    def _parse_comparison_expression(self, expression, qualifier=None):
        # Resolve STIX Object Path to a field in the target Data Model
        stix_object, stix_field = expression.object_path.split(':')
        # Multiple QRadar fields may map to the same STIX Object
        mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
        # Resolve the comparison symbol to use in the query string (usually just ':')
        comparator = self._lookup_comparison_operator(self, expression.comparator)

        # Special case for artifact:payload_bin object with Like operator where we apply aql TEXT SEARCH
        if expression.comparator == ComparisonComparators.Like and (expression.object_path == 'artifact:payload_bin'):
            return "TEXT SEARCH '{}'".format(expression.value)

        # Special case where we want the risk finding
        if stix_object == 'x-ibm-finding' and stix_field == 'name' and expression.value == "*":
            return "devicetype = 18"
        if stix_field == 'protocols[*]':
            map_data = read_json('network_protocol_map', self.options)
            try:
                expression.value = map_data[expression.value.lower()]
            except Exception as protocol_key:
                raise KeyError(
                    "Network protocol {} is not supported.".format(protocol_key))
        elif stix_field == 'start' or stix_field == 'end':
            transformer = TimestampToMilliseconds()
            expression.value = transformer.transform(expression.value)

        # Some values are formatted differently based on how they're being compared
        if expression.comparator == ComparisonComparators.Matches:  # needs forward slashes
            value = self._format_match(expression.value)
        # should be (x, y, z, ...)
        elif expression.comparator == ComparisonComparators.In:
            value = self._format_in(expression.value)
        elif expression.comparator == ComparisonComparators.Equal or expression.comparator == ComparisonComparators.NotEqual:
            # Should be in single-quotes
            value = self._format_equality(expression.value)
        # '%' -> '*' wildcard, '_' -> '?' single wildcard
        elif expression.comparator == ComparisonComparators.Like and not (expression.object_path == 'artifact:payload_bin'):
            value = self._format_like(expression.value)
        else:
            value = self._escape_value(expression.value)

        comparison_string = self._parse_mapped_fields(self, expression, value, comparator, stix_field, mapped_fields_array)

        if(len(mapped_fields_array) > 1 and not self._is_reference_value(stix_field)):
            # More than one AQL field maps to the STIX attribute so group the ORs.
            comparison_string = "({})".format(comparison_string)
        if expression.negated:
            comparison_string = self._negate_comparison(comparison_string)
        if qualifier:
            self.qualified_queries.append("{} limit {} {}".format(comparison_string, self.result_limit, qualifier))
            return ''
        else:
            return "{}".format(comparison_string)

    def _parse_expression(self, expression, qualifier=None) -> str:
        if isinstance(expression, ComparisonExpression):  # Base Case
            return self._parse_comparison_expression(self, expression, qualifier)
        elif isinstance(expression, CombinedComparisonExpression):
            return self._parse_combined_comparison_expression(self, expression, qualifier)
        elif isinstance(expression, ObservationExpression):
            return self._parse_observation_expression(self, expression, qualifier)
        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            if isinstance(expression.observation_expression, CombinedObservationExpression):
                self._parse_expression(expression.observation_expression.expr1, expression.qualifier)
                self._parse_expression(expression.observation_expression.expr2, expression.qualifier)
                
                return ''
            else:
                return self._parse_expression(expression.observation_expression.comparison_expression, expression.qualifier)
        elif isinstance(expression, CombinedObservationExpression):
            return self._parse_combined_observation_expression(self, expression)
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
    return query_parts[0] + " " + query_parts[1] + " " + str(millisecond_start_time) + " " + query_parts[3] + " " + str(millisecond_stop_time)


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
            formatted_queries.append(query)

    return formatted_queries


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    result_limit = options['result_limit']
    time_range = options['time_range']
    translated_where_statements = AqlQueryStringPatternTranslator(pattern, data_model_mapping, result_limit, options)
    select_statement = translated_where_statements.dmm.map_selections()
    queries = []
    translated_queries = translated_where_statements.qualified_queries
    for where_statement in translated_queries:
        has_start_stop = _test_START_STOP_format(where_statement)
        if(has_start_stop):
            queries.append("SELECT %s FROM %s WHERE %s" % (select_statement, data_model_mapping.dialect, where_statement))
        else:
            queries.append("SELECT %s FROM %s WHERE %s limit %s last %s minutes" % (select_statement, data_model_mapping.dialect, where_statement, result_limit, time_range))
    return queries
