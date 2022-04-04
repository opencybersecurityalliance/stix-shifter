from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, \
    ComparisonExpression, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, StartStopQualifier
from stix_shifter_utils.stix_translation.src.json_to_stix import observable
import logging
import re

UNIVERSAL_FIELDS = ["filename", "ip", "md5", "path", "sha1", "sha256"]
GREATER_LESS_FIELDS = ["eventdata.regionSize", "eventdata.relevance", "eventdata.size"]

logger = logging.getLogger(__name__)


class QueryStringPatternTranslator:

    def __init__(self, pattern: Pattern, data_model_mapper):
        self.dmm = data_model_mapper
        self.comparator_lookup = self.dmm.map_comparator()
        self.pattern = pattern
        self.is_combined_expression = False
        self.formated_qualifier = None
        self.translated = self.parse_expression(pattern)

    @staticmethod
    def _format_set(values) -> str:
        gen = values.element_iterator()
        return "({})".format(" OR ".join([QueryStringPatternTranslator._escape_value(value) for value in gen]))

    @staticmethod
    def _format_equality(value) -> str:
        return '"{}"'.format(value)
        
    @staticmethod
    def _escape_value(value, comparator=None) -> str:
        if isinstance(value, str):
            return '{}'.format(value.replace('\\', '\\\\').replace('\"', '\\"').replace('(', '\\(').replace(')', '\\)'))
        else:
            return value

    @staticmethod
    def _negate_comparison(comparison_string):
        """
        :param comparison_string: str
        :return: str
        """
        if ' OR ' in comparison_string:
            con_string = re.sub(r'\(', '(NOT ', comparison_string, 1)
            comparison_string = con_string.replace(' OR ', ' OR NOT ')
        else:
            comparison_string = "NOT " + comparison_string
        return comparison_string

    @staticmethod
    def _format_universal_field(field) -> str:
        if field in UNIVERSAL_FIELDS:
            return '${}'.format(field)
        return field

    @staticmethod
    def _check_value_type(value):
        value = str(value)
        for key, pattern in observable.REGEX.items():
            if key != 'date' and bool(re.search(pattern, value)):
                return key
        return None

    @staticmethod
    def _is_reference_value(stix_field):
        return stix_field == 'src_ref.value' or stix_field == 'dst_ref.value'

    @staticmethod
    def _lookup_comparison_operator(self, expression_operator):
        if str(expression_operator) not in self.comparator_lookup:
            raise NotImplementedError("Comparison operator {} unsupported for connector".format(expression_operator.name))
        return self.comparator_lookup[str(expression_operator)]

    def _set_is_combined_expression(self):
        self.is_combined_expression = True

    def _format_qualifier(self, qualifier) -> str:
        if qualifier and isinstance(qualifier, StartStopQualifier):
            self.formated_qualifier = 'AND happenedAfter = "' + qualifier.start_iso + '" AND happenedBefore = "' + qualifier.stop_iso + '"'

    def _parse_mapped_fields(self, value, comparator, mapped_fields_array) -> str:
        """Convert a list of mapped fields into a query string."""
        comparison_strings = []
        str_ = None

        if isinstance(value, str):
            value = [value]

        for val in value:
            for mapped_field in mapped_fields_array:
                mapped_field = self._format_universal_field(mapped_field)
                comparison_strings.append(f'{mapped_field} {comparator} {val}')

        # Only wrap in () if there's more than one comparison string
        if len(comparison_strings) == 1:
            str_ = comparison_strings[0]
        elif len(comparison_strings) > 1:
            str_ = f"{' OR '.join(comparison_strings)}"
        else:
            raise RuntimeError((f'Failed to convert {mapped_fields_array} mapped fields into query string'))

        return str_

    def _parse_expression(self, expression, qualifier=None) -> str:
        if isinstance(expression, ComparisonExpression):  # Base Case
            # Resolve STIX Object Path to a field in the target Data Model
            stix_object, stix_field = expression.object_path.split(':')
            # Multiple data source fields may map to the same STIX Object
            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
            # Resolve the comparison symbol to use in the query string (usually just ':')
            comparator = self._lookup_comparison_operator(self, expression.comparator)

            # Some values are formatted differently based on how they're being compared
            if expression.comparator == ComparisonComparators.In:
                value = self._format_set(expression.value)
                value = list(map(self._format_equality, expression.value.element_iterator()))
            elif expression.comparator == ComparisonComparators.Matches:
                value = self._format_equality(expression.value)
            elif expression.comparator == ComparisonComparators.Like:
                value = self._format_equality(expression.value)
            elif expression.comparator == ComparisonComparators.Equal or expression.comparator == ComparisonComparators.NotEqual:
                # Should be in single-quotes
                value = self._format_equality(expression.value)
            else:
                value = self._escape_value(expression.value)

            comparison_string = self._parse_mapped_fields(
                value=value,
                comparator=comparator,
                mapped_fields_array=mapped_fields_array
            )

            mapped_fields_array_len = len(mapped_fields_array)

            if(mapped_fields_array_len > 1):
                # More than one data source field maps to the STIX attribute, so group comparisons together.
                grouped_comparison_string = "(" + comparison_string + ")"
                comparison_string = grouped_comparison_string

            if expression.negated:
                comparison_string = self._negate_comparison(comparison_string)
            
            self._format_qualifier(qualifier)

            return "{}".format(comparison_string)

        elif isinstance(expression, CombinedComparisonExpression):
            self._set_is_combined_expression()
            operator = self._lookup_comparison_operator(self, expression.operator)
            expression_01 = self._parse_expression(expression.expr1)
            expression_02 = self._parse_expression(expression.expr2)
            if not expression_01 or not expression_02:
                return ''
            if isinstance(expression.expr1, CombinedComparisonExpression):
                expression_01 = "({})".format(expression_01)
            if isinstance(expression.expr2, CombinedComparisonExpression):
                expression_02 = "({})".format(expression_02)

            query_string = "{} {} {}".format(expression_01, operator, expression_02)
            
            self._format_qualifier(qualifier)
            
            return "{}".format(query_string)
        elif isinstance(expression, ObservationExpression):
            return self._parse_expression(expression.comparison_expression, qualifier)
        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            if isinstance(expression.observation_expression, CombinedObservationExpression):
                self._set_is_combined_expression()
                operator = self._lookup_comparison_operator(self, expression.observation_expression.operator)
                expression_01 = self._parse_expression(expression.observation_expression.expr1)
                # qualifier only needs to be passed into the parse expression once since it will be the same for both expressions
                expression_02 = self._parse_expression(expression.observation_expression.expr2, expression)
                return "{} {} {}".format(expression_01, operator, expression_02)
            else:
                return self._parse_expression(expression.observation_expression.comparison_expression, expression)
        elif isinstance(expression, CombinedObservationExpression):
            self._set_is_combined_expression()
            operator = self._lookup_comparison_operator(self, expression.operator)
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


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    query_translator = QueryStringPatternTranslator(pattern, data_model_mapping)
    query = query_translator.translated

    if query_translator.formated_qualifier:
        if query_translator.is_combined_expression:
            query = "({}) {}".format(query, query_translator.formated_qualifier)
        else:
            query = "{} {}".format(query, query_translator.formated_qualifier)

    return query
