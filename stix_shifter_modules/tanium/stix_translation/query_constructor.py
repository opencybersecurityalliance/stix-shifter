from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, StartStopQualifier,\
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators
from stix_shifter_utils.stix_translation.src.utils.transformers import TimestampToMilliseconds
from stix_shifter_utils.stix_translation.src.json_to_stix import observable
import logging
import re

# Source and destination reference mapping for ip and mac addresses.
# Change the keys to match the data source fields. The value array indicates the possible data type that can come into from field.
REFERENCE_DATA_TYPES = {"source_ipaddr": ["ipv4", "ipv4_cidr", "ipv6", "ipv6_cidr"],
                        "dest_ipaddr": ["ipv4", "ipv4_cidr"],
                        }

TIMESTAMP_STIX_PROPERTIES = ["created", "modified", "accessed", "ctime", "mtime", "atime", "created_time", "modifed_time"]

logger = logging.getLogger(__name__)


class QueryStringPatternTranslator:

    def __init__(self, pattern: Pattern, data_model_mapper):
        self.dmm = data_model_mapper
        self.comparator_lookup = self.dmm.map_comparator()
        self.pattern = pattern
        self.translated = self.parse_expression(pattern)

    @staticmethod
    def _format_equality(value) -> str:
        return '{}'.format(value)

    @classmethod
    def _format_start_stop_qualifier(self, expression, qualifier) -> str:
        """Convert a STIX start stop qualifier into a query string.

        The sample MySQL schema included in this connector defines a timerange with a start and stop value
        based on the entry_time field. 
        """
        qualifier_split = qualifier.split("'")
        start = qualifier_split[1]
        stop = qualifier_split[3]
        qualified_query = "%s&alertedAtFrom=%s&alertedAtUntil=%s" % (expression, start, stop)
        return qualified_query

    @staticmethod
    def _escape_value(value, comparator=None) -> str:
        if isinstance(value, str):
            return '{}'.format(value.replace('\\', '\\\\').replace('\"', '\\"').replace('(', '\\(').replace(')', '\\)'))
        else:
            return value

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
        else:
            return "{mapped_field} {comparator} {value}".format(
                mapped_field=mapped_field, comparator=comparator, value=value)

    @staticmethod
    def _parse_mapped_fields(self, expression, value, comparator, stix_field, mapped_fields_array):
        if stix_field in TIMESTAMP_STIX_PROPERTIES:
            value = self._format_timestamp(value)
        comparison_string = ""
        is_reference_value = self._is_reference_value(stix_field)
        # Need to use expression.value to match against regex since the passed-in value has already been formated.
        value_type = self._check_value_type(expression.value) if is_reference_value else None
        mapped_fields_count = 1 if is_reference_value else len(mapped_fields_array)

        for mapped_field in mapped_fields_array:
            if is_reference_value:
                parsed_reference = self._parse_reference(self, stix_field, value_type, mapped_field, value, comparator)
                if not parsed_reference:
                    continue
                comparison_string += parsed_reference
            else:
                comparison_string += "{mapped_field}{comparator}{value}".format(mapped_field=mapped_field, comparator=comparator, value=value)

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
            raise NotImplementedError("Comparison operator {} unsupported for MySQL connector".format(expression_operator.name))
        return self.comparator_lookup[str(expression_operator)]

    def _parse_expression(self, expression, qualifier=None) -> str:
        if isinstance(expression, ComparisonExpression):  # Base Case
            logger.info("expression is " + expression.value)
            # Resolve STIX Object Path to a field in the target Data Model
            stix_object, stix_field = expression.object_path.split(':')
            # Multiple data source fields may map to the same STIX Object
            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
            # Resolve the comparison symbol to use in the query string (usually just ':')
            comparator = self._lookup_comparison_operator(self, expression.comparator)

            if stix_field == 'start' or stix_field == 'end':
                transformer = TimestampToMilliseconds()
                expression.value = transformer.transform(expression.value)

            if expression.comparator == ComparisonComparators.Equal:
                # Should be in single-quotes
                value = self._format_equality(expression.value)
            else:
                value = self._escape_value(expression.value)

            comparison_string = self._parse_mapped_fields(self, expression, value, comparator, stix_field, mapped_fields_array)
            if(len(mapped_fields_array) > 1 and not self._is_reference_value(stix_field)):
                # More than one data source field maps to the STIX attribute, so group comparisons together.
                grouped_comparison_string = "(" + comparison_string + ")"
                comparison_string = grouped_comparison_string

            if qualifier:
                comparison_string = self._format_start_stop_qualifier(comparison_string, qualifier)
                return comparison_string
            else:
                return "{}".format(comparison_string)
        elif isinstance(expression, CombinedComparisonExpression):
            operator = self._lookup_comparison_operator(self, expression.operator)
            expression_01 = self._parse_expression(expression.expr1)
            expression_02 = self._parse_expression(expression.expr2)
            if not expression_01 or not expression_02:
                return ''
            if isinstance(expression.expr1, CombinedComparisonExpression):
                expression_01 = "{}".format(expression_01)
            if isinstance(expression.expr2, CombinedComparisonExpression):
                expression_02 = "{}".format(expression_02)
            if operator == 'AND':
                query_string = "({}{}{})".format(expression_01, operator, expression_02)
            else:
                query_string = "{}{}{}".format(expression_01, operator, expression_02)
            if qualifier:
                query_string = self._format_start_stop_qualifier(query_string, qualifier)
                return query_string
            else:
                return "{}".format(query_string)
        elif isinstance(expression, ObservationExpression):
            return self._parse_expression(expression.comparison_expression, qualifier)
        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            if isinstance(expression.observation_expression, CombinedObservationExpression):
                operator = self._lookup_comparison_operator(self, expression.observation_expression.operator)
                expression_01 = self._parse_expression(expression.observation_expression.expr1)
                # qualifier only needs to be passed into the parse expression once since it will be the same for both expressions
                expression_02 = self._parse_expression(expression.observation_expression.expr2, expression.qualifier)
                return "{}{}{}".format(expression_01, operator, expression_02)
            else:
                return self._parse_expression(expression.observation_expression.comparison_expression, expression.qualifier)
        elif isinstance(expression, CombinedObservationExpression):
            operator = self._lookup_comparison_operator(self, expression.operator)
            expression_01 = self._parse_expression(expression.expr1)
            expression_02 = self._parse_expression(expression.expr2)
            if expression_01 and expression_02:
                return "{}{}{}".format(expression_01, operator, expression_02)
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


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    query = QueryStringPatternTranslator(pattern, data_model_mapping).translated

    # This sample return statement is in an SQL format. This should be changed to the native data source query language.
    # If supported by the query language, a limit on the number of results should be added to the query as defined by options['result_limit'].
    # Translated patterns must be returned as a list of one or more native query strings.
    # A list is returned because some query languages require the STIX pattern to be split into multiple query strings.
        
    logger.info("The Query is " + query)
    return ["%s" % (query)]
