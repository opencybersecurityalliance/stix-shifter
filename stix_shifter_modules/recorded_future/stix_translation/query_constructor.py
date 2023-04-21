from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators
from stix_shifter_utils.stix_translation.src.utils.transformers import TimestampToMilliseconds
from stix_shifter_utils.stix_translation.src.json_to_stix import observable
import logging
import re

# Source and destination reference mapping for ip and mac addresses.
# Change the keys to match the data source fields. The value array indicates the possible data type that can come into from field.
REFERENCE_DATA_TYPES = {"SourceIpV4": ["ipv4", "ipv4_cidr"],
                        "SourceIpV6": ["ipv6"],
                        "DestinationIpV4": ["ipv4", "ipv4_cidr"],
                        "DestinationIpV6": ["ipv6"]}

logger = logging.getLogger(__name__)
data = ""
dataType = ""

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
        ComparisonComparators.Like: "LIKE",
        ComparisonComparators.In: "IN",
        ComparisonComparators.Matches: 'LIKE',
        # ComparisonComparators.IsSubSet: '',
        # ComparisonComparators.IsSuperSet: '',
        ObservationOperators.Or: 'OR',
        # Treat AND's as OR's -- Unsure how two ObsExps wouldn't cancel each other out.
        ObservationOperators.And: 'OR'
    }

    def __init__(self, pattern: Pattern, data_model_mapper):
        self.dmm = data_model_mapper
        self.pattern = pattern
        self.translated = self.parse_expression(pattern)

    @staticmethod
    def _format_equality(value) -> str:
        return '\'{}\''.format(value)

    @staticmethod
    def _parse_mapped_fields(self, expression, value, comparator, stix_field, mapped_fields_array):
        comparison_string = ""
        is_reference_value = self._is_reference_value(stix_field)
        # Need to use expression.value to match against regex since the passed-in value has already been formated.
        # value_type = self._check_value_type(expression.value) if is_reference_value else None
        mapped_fields_count = 1 if is_reference_value else len(mapped_fields_array)

        for mapped_field in mapped_fields_array:
            comparison_string += "{mapped_field} {comparator} {value}".format(mapped_field=mapped_field, comparator=comparator, value=value)

            if (mapped_fields_count > 1):
                comparison_string += " OR "
                mapped_fields_count -= 1
        return comparison_string

    @staticmethod
    def _is_reference_value(stix_field):
        return stix_field == 'src_ref.value' or stix_field == 'dst_ref.value'

    @staticmethod
    def _lookup_comparison_operator(self, expression_operator):
        if expression_operator not in self.comparator_lookup:
            raise NotImplementedError("Comparison operator {} unsupported for Dummy connector".format(expression_operator.name))
        return self.comparator_lookup[expression_operator]

    def _parse_expression(self, expression, qualifier=None) -> str:
        if isinstance(expression, ComparisonExpression):  # Base Case
            # Resolve STIX Object Path to a field in the target Data Model
            stix_object, stix_field = expression.object_path.split(':')

            # Multiple data source fields may map to the same STIX Object
            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
            # Resolve the comparison symbol to use in the query string (usually just ':')
            comparator = self._lookup_comparison_operator(self, expression.comparator)
            if stix_field == 'start' or stix_field == 'end':
                pass

            # Some values are formatted differently based on how they're being compared
            if expression.comparator == ComparisonComparators.Equal or expression.comparator == ComparisonComparators.NotEqual:
                # Should be in single-quotes                
                value = self._format_equality(expression.value)

            #TODO DEBUGGING
            get_data_source_query(stix_field=stix_field, stix_object=stix_object, value=value)

            comparison_string = self._parse_mapped_fields(self, expression, value, comparator, stix_field, mapped_fields_array)
            if(len(mapped_fields_array) > 1 and not self._is_reference_value(stix_field)):
                # More than one data source field maps to the STIX attribute, so group comparisons together.
                grouped_comparison_string = "(" + comparison_string + ")"
                comparison_string = grouped_comparison_string

            return "{}".format(comparison_string)

        elif isinstance(expression, ObservationExpression):
            return self._parse_expression(expression.comparison_expression, qualifier)
        elif isinstance(expression, Pattern):
            return "{expr}".format(expr=self._parse_expression(expression.expression))
        else:
            raise RuntimeError("Unknown Recursion Case for expression={}, type(expression)={}".format(
                expression, type(expression)))

    def parse_expression(self, pattern: Pattern):
        return self._parse_expression(pattern)


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    # Query result limit and time range can be passed into the QueryStringPatternTranslator if supported by the data source.
    # result_limit = options['result_limit']
    # time_range = options['time_range']
    QueryStringPatternTranslator(pattern, data_model_mapping).translated
    # Add space around START STOP qualifiers

    # If supported by the query language, a limit on the number of results should be added to the query as defined by options['result_limit'].
    # Translated patterns must be returned as a list of one or more native query strings.
    # A list is returned because some query languages require the STIX pattern to be split into multiple query strings.
    translated_query = {"data": data, "dataType": dataType}
    return [str(translated_query)]

def get_data_source_query(stix_field, stix_object, value):
    global data, dataType
    dataType = get_data_type(stix_object, stix_field) # can ipv4-addr, ipv6-addr, url, domain, hash
    data = value.replace("'", "")

def get_data_type(stix_object, stix_field):
    if "ipv4" in stix_object or "ipv6" in stix_object:
        return "ip"
    elif "url" in stix_object:
        return "url"
    elif "domain-name" in stix_object:
        return "domain"
    elif "file" in stix_object and "hashes" in stix_field:
        return "hash"
    else:
        return "Unsupported Data Type"