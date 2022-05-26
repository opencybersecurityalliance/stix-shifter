import datetime
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

    def __init__(self, pattern: Pattern, data_model_mapper, options:dict):
        self.dmm = data_model_mapper
        self.comparator_lookup = self.dmm.map_comparator()
        self.pattern = pattern
        self.options = options
        self.is_combined_expression = False
        self.translated = self.parse_expression(pattern)

    @staticmethod
    def _format_set(values) -> str:
        gen = values.element_iterator()
        return "({})".format(" OR ".join([QueryStringPatternTranslator._escape_value(value) for value in gen]))

    @staticmethod
    def _format_equality(value) -> str:
        return '"{}"'.format(value)
        
    @staticmethod
    def _escape_value(value) -> str:
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
    def _format_range_field(field, comparator) -> str:
        if field in GREATER_LESS_FIELDS:
            if comparator == ComparisonComparators.LessThanOrEqual:
                return '{}.lte'.format(field)
            else:
                return '{}.gte'.format(field)
        return field

    @staticmethod
    def _check_value_type(value):
        value = str(value)
        for key, pattern in observable.REGEX.items():
            if key != 'date' and bool(re.search(pattern, value)):
                return key
        return None

    @staticmethod
    def _lookup_comparison_operator(self, expression_operator):
        if str(expression_operator) not in self.comparator_lookup:
            raise NotImplementedError("Comparison operator {} unsupported for connector".format(expression_operator.name))
        return self.comparator_lookup[str(expression_operator)]

    def _format_qualifier(self, qualifier, time_range) -> str:
        str_qualifier_pattern = 'AND happenedAfter = "{start_iso}" AND happenedBefore = "{stop_iso}"'
        if qualifier and isinstance(qualifier, StartStopQualifier):
            start_iso = qualifier.start.replace("t'","").replace("'", "")
            stop_iso = qualifier.stop.replace("t'","").replace("'", "")
            formated_qualifier = str_qualifier_pattern.format(start_iso=start_iso, stop_iso=stop_iso)
        else:
            stop_time = datetime.datetime.utcnow()
            start_time = stop_time - datetime.timedelta(minutes=time_range)
            converted_starttime = start_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            converted_stoptime = stop_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            formated_qualifier = str_qualifier_pattern.format(start_iso=converted_starttime, stop_iso=converted_stoptime)

        return formated_qualifier

    def _parse_mapped_fields(self, value, comparator, expression_comparator, mapped_fields_array) -> str:
        """Convert a list of mapped fields into a query string."""
        comparison_strings = []
        str_ = None

        if isinstance(value, str):
            value = [value]

        for val in value:
            for mapped_field in mapped_fields_array:
                mapped_field = self._format_universal_field(mapped_field)
                mapped_field = self._format_range_field(mapped_field, expression_comparator)
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
                expression_comparator=expression.comparator,
                mapped_fields_array=mapped_fields_array
            )

            mapped_fields_array_len = len(mapped_fields_array)

            if(mapped_fields_array_len > 1):
                # More than one data source field maps to the STIX attribute, so group comparisons together.
                comparison_string = "({})".format(comparison_string)

            if expression.negated:
                comparison_string = self._negate_comparison(comparison_string)
            
            return "{}".format(comparison_string)

        elif isinstance(expression, CombinedComparisonExpression):
            operator = self._lookup_comparison_operator(self, expression.operator)
            expression_01 = self._parse_expression(expression.expr1)
            expression_02 = self._parse_expression(expression.expr2)
            if not expression_01 or not expression_02:
                return ''

            expression_string = "{} {} {}".format(expression_01, operator, expression_02)
            
            return "{}".format(expression_string)
        elif isinstance(expression, ObservationExpression):
            formated_qualifier = self._format_qualifier(qualifier, self.options['time_range'])
            expression_string = self._parse_expression(expression.comparison_expression)
            expression_string = "({}) {}".format(expression_string, formated_qualifier)

            return expression_string
        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            formated_qualifier = self._format_qualifier(expression, self.options['time_range'])

            if isinstance(expression.observation_expression, CombinedObservationExpression):
                expression_string = self._parse_expression(expression.observation_expression, expression)
                return "{}".format(expression_string)
            else:
                expression_string = self._parse_expression(expression.observation_expression.comparison_expression, expression)
                return "({}) {}".format(expression_string, formated_qualifier)

        elif isinstance(expression, CombinedObservationExpression):
            operator = self._lookup_comparison_operator(self, expression.operator)
            expression_01 = self._parse_expression(expression.expr1, qualifier)
            expression_02 = self._parse_expression(expression.expr2, qualifier)
            if expression_01 and expression_02:
                return "{} {} {}".format(expression_01, operator, expression_02)
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
    query_translator = QueryStringPatternTranslator(pattern, data_model_mapping, options)
    query = query_translator.translated
    return query
