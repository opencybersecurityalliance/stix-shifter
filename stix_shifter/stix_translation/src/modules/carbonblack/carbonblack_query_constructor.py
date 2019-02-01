import logging
import datetime
import json
import re

logger = logging.getLogger(__name__)

from stix_shifter.stix_translation.src.patterns.pattern_objects import ObservationExpression, ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, StartStopQualifier, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators
from stix_shifter.stix_translation.src.patterns.errors import SearchFeatureNotSupportedError


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
        ObservationOperators.And: 'or', # This is technically wrong. It should be converted to two separate queries, but
        # current behavior of existing modules treat operator as an OR.
        # observation operator AND - both sides MUST evaluate to true on different observations to be true
    }

    def __init__(self, pattern: Pattern, data_model_mapper, result_limit, dialect):
        self.dmm = data_model_mapper
        self.pattern = pattern
        self.result_limit = result_limit
        self.dialect = dialect
        self.translated = self.parse_expression(pattern)
        self.queries = [self.translated]
        print (self.queries)

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

    def _fomat_start_stop_qualifier(self, expression, qualifier : StartStopQualifier) -> str:
        start = self._to_cb_timestamp(qualifier.start)
        stop = self._to_cb_timestamp(qualifier.stop)

        if self.dialect == "process":
            return "(({}) and start:[{} TO *] and last_update:[* TO {}])".format(expression, start, stop)
        elif self.dialect == "binary":
            return "(({}) and server_added_timestamp:[{} TO {}])".format(expression, start, stop)
        else:
            raise RuntimeError("Invalid CarbonBlack dialect: {}".format(self.dialect))


    def _parse_expression(self, expression, qualifier=None) -> str:
        if isinstance(expression, ComparisonExpression):
            # Base Case
            # Resolve STIX Object Path to a field in the target Data Model
            stix_object, stix_field = expression.object_path.split(':')
            # Multiple QRadar fields may map to the same STIX Object
            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
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

            if len(mapped_fields_array) != 1:
                raise RuntimeError("CarbonBlack invalid multiple fields mapping.")

            mapped_field = mapped_fields_array[0]
            comparison_string = "{mapped_field}{comparator}{value}".format(mapped_field=mapped_field, comparator=comparator, value=value)

            # translate != to NOT equals
            if expression.comparator == ComparisonComparators.NotEqual and not expression.negated:
                expression.negated = True

            if expression.negated:
                comparison_string = self._negate_comparison(comparison_string)

            if qualifier is not None:
                if isinstance(qualifier, StartStopQualifier):
                    return self._fomat_start_stop_qualifier(comparison_string, qualifier)
                else:
                    raise RuntimeError("Unknown Qualifier: {}".format(qualifier))
            else:
                return "{}".format(comparison_string)

        elif isinstance(expression, CombinedComparisonExpression):
            # Note: it seems the ordering of the expressions is reversed at a lower level
            # so we reverse it here so that it is as expected.
            query_string = "{} {} {}".format(self._parse_expression(expression.expr2),
                                             self.comparator_lookup[expression.operator],
                                             self._parse_expression(expression.expr1))
            if qualifier is not None:
                if isinstance(qualifier, StartStopQualifier):
                    return self._fomat_start_stop_qualifier(query_string, qualifier)
                else:
                    raise RuntimeError("Unknown Qualifier: {}".format(qualifier))
            else:
                return "{}".format(query_string)
        elif isinstance(expression, ObservationExpression):
            return self._parse_expression(expression.comparison_expression, qualifier)
        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            if isinstance(expression.observation_expression, CombinedObservationExpression):
                operator = self.comparator_lookup[expression.observation_expression.operator]
                # qualifier only needs to be passed into the parse expression once since it will be the same for both expressions
                return "{expr1} {operator} {expr2}".format(expr1=self._parse_expression(expression.observation_expression.expr1),
                                                           operator=operator,
                                                           expr2=self._parse_expression(expression.observation_expression.expr2, expression))
            else:
                return self._parse_expression(expression.observation_expression.comparison_expression, expression)
        elif isinstance(expression, CombinedObservationExpression):
            operator = self.comparator_lookup[expression.operator]
            return "{expr1} {operator} {expr2}".format(expr1=self._parse_expression(expression.expr1),
                                                       operator=operator,
                                                       expr2=self._parse_expression(expression.expr2))
        elif isinstance(expression, Pattern):
            return "{expr}".format(expr=self._parse_expression(expression.expression))
        else:
            raise RuntimeError("Unknown Recursion Case for expression={}, type(expression)={}".format(
                expression, type(expression)))

    def parse_expression(self, pattern: Pattern):
        return self._parse_expression(pattern)


def translate_pattern(pattern: Pattern, data_model_mapping, result_limit, dialect=None, timerange=None):
    translated_statements = CbQueryStringPatternTranslator(pattern, data_model_mapping, result_limit, dialect)
    return translated_statements.queries
