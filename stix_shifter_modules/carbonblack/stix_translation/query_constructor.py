import logging
import datetime
import json
import re
from stix_shifter_utils.utils import logger

from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, StartStopQualifier, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators
from stix_shifter_utils.stix_translation.src.patterns.errors import SearchFeatureNotSupportedError


class CbQueryStringPatternTranslator:
    comparator_lookup = {
        ComparisonExpressionOperators.And: "and",
        ComparisonExpressionOperators.Or: "or",
        ComparisonComparators.Equal: ":",
        ComparisonComparators.NotEqual: ":",

        ComparisonComparators.GreaterThan: ":",
        ComparisonComparators.GreaterThanOrEqual: ":",
        ComparisonComparators.LessThan: ":",
        ComparisonComparators.LessThanOrEqual: ":",

        ObservationOperators.Or: 'or',
        ObservationOperators.And: 'or',  # This is technically wrong. It should be converted to two separate queries, but
        # current behavior of existing modules treat operator as an OR.
        # observation operator AND - both sides MUST evaluate to true on different observations to be true
    }

    def __init__(self, pattern: Pattern, data_model_mapper, result_limit, time_range):
        self.logger = logger.set_logger(__name__)
        self.dmm = data_model_mapper
        self.pattern = pattern
        self.result_limit = result_limit
        self.time_range = time_range # filter results to last x minutes
        self.translated = self.parse_expression(pattern)
        self.queries = []
        self.queries.append(self.translated)

    @staticmethod
    def _format_equality(value) -> str:
        return '{}'.format(CbQueryStringPatternTranslator._escape_value(value))

    @staticmethod
    def _format_lt(value) -> str:
        return '[* TO {}]'.format(CbQueryStringPatternTranslator._escape_value(value))

    @staticmethod
    def _format_gte(value) -> str:
        return '[{} TO *]'.format(CbQueryStringPatternTranslator._escape_value(value))

# Note: target query language doesn't support '<=' or '>' directly so we implement it indirectly for integers
    @staticmethod
    def _format_lte(value) -> str:
        if isinstance(value, int):
            value = value + 1
        return CbQueryStringPatternTranslator._format_lt(value)

    @staticmethod
    def _format_gt(value) -> str:
        if isinstance(value, int):
            value = value + 1
        return CbQueryStringPatternTranslator._format_gte(value)

    @staticmethod
    def _escape_value(value, comparator=None) -> str:
        if isinstance(value, str):
            return '{}'.format(value.replace('\\', '\\\\').replace('\"', '\\"').replace('(', '\\(').replace(')', '\\)').replace(' ', '\\ '))
        else:
            return value

    @staticmethod
    def _negate_comparison(comparison_string) -> str:
        return "-({})".format(comparison_string)

    @staticmethod
    def _to_cb_timestamp(ts: str) -> str:
        stripped = ts[2:-2]
        if '.' in stripped:
            stripped = stripped.split('.', 1)[0]
        return stripped

    def _format_start_stop_qualifier(self, expression, qualifier: StartStopQualifier) -> str:
        start = self._to_cb_timestamp(qualifier.start)
        stop = self._to_cb_timestamp(qualifier.stop)

        return "({}) and last_update:[{} TO {}]".format(expression, start, stop)

    def _parse_expression(self, expression, qualifier=None):
        if isinstance(expression, ComparisonExpression):
            # Base Case
            # Resolve STIX Object Path to a field in the target Data Model
            stix_object, stix_field = expression.object_path.split(':')

            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
            mapped_field = mapped_fields_array[0]

            # Resolve the comparison symbol to use in the query string (usually just ':')
            comparator = self.comparator_lookup[expression.comparator]
            original_stix_value = expression.value

            # Some values are formatted differently based on how they're being compared
            if expression.comparator == ComparisonComparators.Equal or expression.comparator == ComparisonComparators.NotEqual:
                value = self._format_equality(expression.value)
            elif expression.comparator == ComparisonComparators.LessThan:
                value = self._format_lt(expression.value)
            elif expression.comparator == ComparisonComparators.GreaterThanOrEqual:
                value = self._format_gte(expression.value)
            elif expression.comparator == ComparisonComparators.LessThanOrEqual:
                value = self._format_lte(expression.value)
            elif expression.comparator == ComparisonComparators.GreaterThan:
                value = self._format_gt(expression.value)
            else:
                value = self._escape_value(expression.value)

            comparison_string = "{mapped_field}{comparator}{value}".format(mapped_field=mapped_field, comparator=comparator, value=value)

            # translate != to NOT equals
            if expression.comparator == ComparisonComparators.NotEqual and not expression.negated:
                expression.negated = True

            if expression.negated:
                comparison_string = self._negate_comparison(comparison_string)

            if qualifier is not None:
                if isinstance(qualifier, StartStopQualifier):
                    return self._format_start_stop_qualifier(comparison_string, qualifier)
                else:
                    raise RuntimeError("Unknown Qualifier: {}".format(qualifier))
            else:
                return "{}".format(comparison_string)

        elif isinstance(expression, CombinedComparisonExpression):
            # Wrap nested combined comparison expressions in parentheses
            f1 = "({})" if isinstance(expression.expr2, CombinedComparisonExpression) else "{}"
            f2 = "({})" if isinstance(expression.expr1, CombinedComparisonExpression) else "{}"

            # Note: it seems the ordering of the expressions is reversed at a lower level
            # so we reverse it here so that it is as expected.
            query_string = (f1 + " {} " + f2).format(self._parse_expression(expression.expr2),
                                                     self.comparator_lookup[expression.operator],
                                                     self._parse_expression(expression.expr1))
            if qualifier is not None:
                if isinstance(qualifier, StartStopQualifier):
                    return self._format_start_stop_qualifier(query_string, qualifier)
                else:
                    raise RuntimeError("Unknown Qualifier: {}".format(qualifier))
            else:
                return "{}".format(query_string)
        elif isinstance(expression, ObservationExpression):
            query_string = self._parse_expression(expression.comparison_expression, qualifier=qualifier)
            return query_string
        elif isinstance(expression, CombinedObservationExpression):
            operator = self.comparator_lookup[expression.operator]
            expr1 = self._parse_expression(expression.expr1, qualifier=qualifier)
            expr2 = self._parse_expression(expression.expr2, qualifier=qualifier)
            return f'({expr1}) {operator} ({expr2})'
        elif isinstance(expression, Pattern):
            return self._parse_expression(expression.expression)
        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            return self._parse_expression(expression.observation_expression, expression)
        else:
            raise RuntimeError("Unknown Recursion Case for expression={}, type(expression)={}".format(
                expression, type(expression)))

    def _add_default_timerange(self, query):
        if self.time_range and 'last_update' not in query:
            query = "(({}) and last_update:-{}m)".format(query, self.time_range)

        return query

    def parse_expression(self, pattern: Pattern):
        queries = self._parse_expression(pattern)
        return self._add_default_timerange(queries)


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    result_limit = options['result_limit']
    time_range = options['time_range']

    translated_statements = CbQueryStringPatternTranslator(pattern, data_model_mapping, result_limit, time_range)
    return translated_statements.queries
