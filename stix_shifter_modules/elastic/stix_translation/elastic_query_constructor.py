import logging
import datetime

logger = logging.getLogger(__name__)

from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators
from stix_shifter_utils.stix_translation.src.patterns.errors import SearchFeatureNotSupportedError

class ElasticQueryStringPatternTranslator:
    comparator_lookup = {
        ComparisonExpressionOperators.And: "AND",
        ComparisonExpressionOperators.Or: "OR",
        ComparisonComparators.GreaterThan: ":>",
        ComparisonComparators.GreaterThanOrEqual: ":>=",
        ComparisonComparators.LessThan: ":<",
        ComparisonComparators.LessThanOrEqual: ":<=",
        ComparisonComparators.Equal: ":",
        ComparisonComparators.NotEqual: ":",
        ComparisonComparators.Like: ":",
        ComparisonComparators.In: ":",
        ComparisonComparators.Matches: ':',
        ObservationOperators.Or: 'OR',
        ObservationOperators.And: 'OR'  # Treat AND's as OR's -- Unsure how two ObsExps wouldn't cancel each other out.
    }

    def __init__(self, pattern: Pattern, data_model_mapper, base_prefix: str='data_model.', action_prefix: str='action.',
                 fields_prefix: str='fields.', object_prefix: str='object'):
        self.dmm = data_model_mapper
        self.pattern = pattern
        self.action_prefix = base_prefix + action_prefix
        self.fields_prefix = base_prefix + fields_prefix
        self.object_prefix = base_prefix + object_prefix
        self.translated = self.parse_expression(pattern)

    @staticmethod
    def _format_set(values) -> str:
        gen = values.element_iterator()
        return "({})".format(' OR '.join([ElasticQueryStringPatternTranslator._escape_value(value) for value in gen]))

    @staticmethod
    def _format_match(value) -> str:
        raw = ElasticQueryStringPatternTranslator._escape_value(value)
        if raw[0] == "^":
            raw = raw[1:]
        else:
            raw = ".*" + raw
        if raw[-1] == "$":
            raw = raw[0:-1]
        else:
            raw = raw + ".*"
        return "/{}/".format(raw)

    @staticmethod
    def _format_equality(value) -> str:
        # if object is of type datetime, remove quotes
        if (type(value) is datetime.datetime):
          return '{}'.format(value)

        return '"{}"'.format(value)

    @staticmethod
    def _format_like(value) -> str:
        value = value.replace('%', '*')
        value = value.replace('_', '?')
        return ElasticQueryStringPatternTranslator._escape_value(value)

    @staticmethod
    def _escape_value(value, comparator=None) -> str:
        if isinstance(value, str):
            return '{}'.format(value.replace('\\', '\\\\').replace('\"', '\\"').replace('(', '\\(').replace(')', '\\)'))
        else:
            return value

    @staticmethod
    def _negate_comparison(comparison_string):
        return "NOT({})".format(comparison_string)

    def _parse_expression(self, expression) -> str:
        if isinstance(expression, ComparisonExpression):  # Base Case
            # Resolve STIX Object Path to a field in the target Data Model
            stix_object, stix_field = expression.object_path.split(':')
            mapped_object = self.dmm.map_object(stix_object)
            mapped_field = "{}{}".format(self.fields_prefix, self.dmm.map_field(stix_object, stix_field))
            scope_to_object = "{}:{}".format(self.object_prefix, mapped_object)

            # Resolve the comparison symbol to use in the query string (usually just ':')
            comparator = self.comparator_lookup[expression.comparator]

            # Some values are formatted differently based on how they're being compared
            if expression.comparator == ComparisonComparators.Matches:  # needs forward slashes
                value = self._format_match(expression.value)
            elif expression.comparator == ComparisonComparators.In:  # should be (x, y, z, ...)
                value = self._format_set(expression.value)
            elif expression.comparator == ComparisonComparators.Equal or expression.comparator == ComparisonComparators.NotEqual:
                value = self._format_equality(expression.value)  # Should be in double-quotes
            elif expression.comparator == ComparisonComparators.Like:  # '%' -> '*' wildcard, '_' -> '?' single wildcard
                value = self._format_like(expression.value)
            else:
                value = self._escape_value(expression.value)

            comparison_string = "{mapped_field}{comparator}{value}".format(mapped_field=mapped_field,
                                                                           comparator=comparator,
                                                                           value=value)

            if expression.comparator == ComparisonComparators.NotEqual:
                comparison_string = self._negate_comparison(comparison_string)

            if expression.negated:
                comparison_string = self._negate_comparison(comparison_string)

            return "{scope_to_object} AND {comparison}".format(scope_to_object=scope_to_object,
                                                               comparison=comparison_string)

        elif isinstance(expression, CombinedComparisonExpression):
            query_string = "({}) {} ({})".format(self._parse_expression(expression.expr1),
                                                 self.comparator_lookup[expression.operator],
                                                 self._parse_expression(expression.expr2))
            return query_string
        elif isinstance(expression, ObservationExpression):
            return self._parse_expression(expression.comparison_expression)
        elif isinstance(expression, CombinedObservationExpression):
            if expression.operator == ObservationOperators.FollowedBy:
                raise SearchFeatureNotSupportedError("{feature} on {platform}".format(feature=expression.operator,
                                                                                      platform="Elasticsearch"))
            else:
                operator = self.comparator_lookup[expression.operator]
            return "({expr1}) {operator} ({expr2})".format(expr1=self._parse_expression(expression.expr1),
                                                           operator=operator,
                                                           expr2=self._parse_expression(expression.expr2))
        elif isinstance(expression, Pattern):
            return self._parse_expression(expression.expression)
        else:
            raise RuntimeError("Unknown Recursion Case for expression={}, type(expression)={}".format(expression,
                                                                                                      type(expression)))

    def parse_expression(self, pattern: Pattern):
        return self._parse_expression(pattern)


def translate_pattern(pattern: Pattern, data_model_mapping):
    x = ElasticQueryStringPatternTranslator(pattern, data_model_mapping)
    return x.translated
