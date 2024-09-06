import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)

from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import (
    ObservationExpression, ComparisonExpression,
    ComparisonExpressionOperators, ComparisonComparators, Pattern,
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators
)

from . import encoders
from . import object_scopers

def stix_strptime(date_string):
    stix_date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    stix_date_format_secs = "%Y-%m-%dT%H:%M:%SZ"
    try:
        return datetime.strptime(date_string, stix_date_format)
    except ValueError:
        return datetime.strptime(date_string, stix_date_format_secs)

class SecuronixSearchTranslator:
    """ The core translator class for Securonix. Instances should not be re-used """

    def __init__(self, pattern: Pattern, data_model_mapper, result_limit, time_range, object_scoper=object_scopers.default_object_scoper):
        self.dmm = data_model_mapper
        self.comparator_lookup = self.dmm.map_comparator()
        self.pattern = pattern
        self.object_scoper = object_scoper
        self.result_limit = result_limit
        self.time_range = time_range

    def translate(self, expression, qualifier=None):
        """ Translate STIX pattern into Securonix query string """
        if isinstance(expression, Pattern):
            expr = self.translate(expression.expression, qualifier=qualifier)
            return expr

        elif isinstance(expression, ObservationExpression):
            translator = _SecuronixObservationExpressionTranslator(
                expression, self.dmm, self.comparator_lookup, self.object_scoper
            )
            translated_query_str = translator.translate(expression.comparison_expression)

            if qualifier:
                # Parsing start and stop times from the qualifier
                stix_date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
                stix_date_format_secs = "%Y-%m-%dT%H:%M:%SZ"
                time_pattern = r"t'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z)'"

                match = re.findall(time_pattern, qualifier)
                if match:
                    start_time_str, end_time_str = match
                    start_time = datetime.strptime(start_time_str, stix_date_format).strftime('%Y-%m-%d %H:%M:%S')
                    end_time = datetime.strptime(end_time_str, stix_date_format).strftime('%Y-%m-%d %H:%M:%S')

                    translated_query_str += f' AND eventtime_from="{start_time}" AND eventtime_to="{end_time}"'

            return translated_query_str

        elif isinstance(expression, CombinedObservationExpression):
            combined_expr_format_string = self.comparator_lookup[str(expression.operator)]
            return combined_expr_format_string.format(
                expr1=self.translate(expression.expr1),
                expr2=self.translate(expression.expr2)
            )

        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            return self.translate(expression.observation_expression, expression.qualifier)
        else:
            raise NotImplementedError("Comparison type not implemented")

class _SecuronixObservationExpressionTranslator:

    def __init__(self, expression: ObservationExpression, dmm, comparator_lookup, object_scoper):
        self.expression = expression
        self.dmm = dmm
        self.comparator_lookup = comparator_lookup
        self.object_scoper = object_scoper

    def _lookup_comparison_operator(self, expression_operator):
        if str(expression_operator) not in self.comparator_lookup:
            raise NotImplementedError(f"Comparison operator {expression_operator.name} unsupported for Securonix connector")
        return self.comparator_lookup[str(expression_operator)]

    def translate(self, expression):
        if isinstance(expression, ComparisonExpression):
            stix_object, stix_path = expression.object_path.split(':')

            object_mapping = self.dmm.map_object(stix_object)
            field_mapping = self.dmm.map_field(stix_object, stix_path)
            object_scoping = self.object_scoper(object_mapping)
            
            if isinstance(field_mapping, list):
                comparisons = [
                    self._build_comparison(expression, object_scoping, mapped_field)
                    for mapped_field in field_mapping
                ]
                return " OR ".join(comparisons)
            else:
                return self._build_comparison(expression, object_scoping, field_mapping)

        elif isinstance(expression, CombinedComparisonExpression):
            return "({} {} {})".format(
                self.translate(expression.expr1),
                self.comparator_lookup[str(expression.operator)],
                self.translate(expression.expr2)
            )

    def _build_comparison(self, expression, object_scoping, field_mapping):
        comparator = self._lookup_comparison_operator(expression.comparator)
        comparison = f'{field_mapping} {comparator} {encoders.simple(expression.value)}'
        securonix_comparison = self._maybe_negate(comparison, expression.negated)
        return f"({object_scoping} AND {securonix_comparison})"

    def _maybe_negate(self, securonix_comparison, negated):
        if negated:
            return f"NOT ({securonix_comparison})"
        else:
            return securonix_comparison

def translate_pattern(pattern: Pattern, data_model_mapping, options):
    result_limit = options.get('result_limit')
    time_range = options.get('time_range')
    index = options.get('index')
    x = SecuronixSearchTranslator(pattern, data_model_mapping, result_limit, time_range)
    translated_query = x.translate(pattern)

    if index:
        indices = [i.strip(' ') for i in index.split(',')]
        index_cmd = ' OR '.join([f'index="{i}"' for i in indices])
        translated_query = f'{index_cmd} {translated_query}'
    return translated_query
