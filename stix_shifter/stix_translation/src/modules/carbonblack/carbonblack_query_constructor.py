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
        ObservationOperators.And: 'or', # TODO this is technically wrong. It should be converted to two separate queries
        # observation operator AND - both sides MUST evaluate to true on different observations to be true
    }

    def __init__(self, pattern: Pattern, data_model_mapper, result_limit):
        self.dmm = data_model_mapper
        self.pattern = pattern
        self.result_limit = result_limit
        self.translated = self.parse_expression(pattern)
        self.queries = [self.translated]
        print (self.queries)

    @staticmethod
    def _format_equality(value) -> str:
        return '{}'.format(value)

    @staticmethod
    def _format_lt(value) -> str:
        return '[* TO {}]'.format(value)

    @staticmethod
    def _format_gte(value) -> str:
        return '[{} TO *]'.format(value)

    @staticmethod
    def _escape_value(value, comparator=None) -> str:
        if isinstance(value, str): # TODO this escape is incorrect for carbonblack
            return '{}'.format(value.replace('\\', '\\\\').replace('\"', '\\"').replace('(', '\\(').replace(')', '\\)'))
        else:
            return value

    @staticmethod
    def _negate_comparison(comparison_string):
        return "-({})".format(comparison_string)

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
            elif expression.comparator == ComparisonComparators.LessThanOrEqual: # TODO fix target query language doesn't support this so will require some work
                value = self._format_lt(expression.value)
            elif expression.comparator == ComparisonComparators.GreaterThan: # TODO fix target query language doesn't support this so will require some work
                value = self._format_gte(expression.value)
            else:
                value = self._escape_value(expression.value)

            comparison_string = ""
            mapped_fields_count = len(mapped_fields_array)
            for mapped_field in mapped_fields_array:
                comparison_string += "{mapped_field}{comparator}{value}".format(
                    mapped_field=mapped_field, comparator=comparator, value=value)

                if (mapped_fields_count > 1):
                    comparison_string += " OR "
                    mapped_fields_count -= 1

            if(len(mapped_fields_array) > 1):
                # More than one Cb field maps to the STIX attribute so group the ORs.
                grouped_comparison_string = "(" + comparison_string + ")"
                comparison_string = grouped_comparison_string

            # translate != to NOT equals
            if expression.comparator == ComparisonComparators.NotEqual and not expression.negated:
                expression.negated = True

            if expression.negated:
                comparison_string = self._negate_comparison(comparison_string)

            if qualifier is not None:
                if isinstance(qualifier, StartStopQualifier):
                    start = to_cb_timestamp(qualifier.start)
                    stop = to_cb_timestamp(qualifier.stop)
                    return "(({}) and start:[{} TO *] and last_update:[* TO {}])".format(comparison_string, start, stop)
                else:
                    raise RuntimeError("Unknown Qualifier")
            else:
                return "{}".format(comparison_string)

        elif isinstance(expression, CombinedComparisonExpression):
            query_string = "{} {} {}".format(self._parse_expression(expression.expr1),
                                             self.comparator_lookup[expression.operator],
                                             self._parse_expression(expression.expr2))
            if qualifier is not None:
                if isinstance(qualifier, StartStopQualifier):
                    start = to_cb_timestamp(qualifier.start)
                    stop = to_cb_timestamp(qualifier.stop)
                    return "(({}) and start:[{} TO *] and last_update:[* TO {}])".format(comparison_string, start, stop)
                else:
                    raise RuntimeError("Unknown Qualifier")
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

def to_cb_timestamp(ts: str) -> str:
    stripped = ts[2:-2]
    if '.' in stripped:
        stripped = stripped.split('.', 1)[0]
    return stripped

def translate_pattern(pattern: Pattern, data_model_mapping, result_limit, timerange=None):
    translated_statements = CbQueryStringPatternTranslator(pattern, data_model_mapping, result_limit)
    return translated_statements.queries
