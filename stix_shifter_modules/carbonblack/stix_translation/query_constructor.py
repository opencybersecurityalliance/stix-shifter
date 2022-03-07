import logging
import datetime
import json
import re
from stix_shifter_utils.utils import logger
from stix_shifter_utils.stix_translation.src.json_to_stix import observable

from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, StartStopQualifier, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators, SetValue
from stix_shifter_utils.stix_translation.src.patterns.errors import SearchFeatureNotSupportedError


class CbQueryStringPatternTranslator:

    def __init__(self, pattern: Pattern, data_model_mapper, result_limit, time_range):
        self.logger = logger.set_logger(__name__)
        self.dmm = data_model_mapper
        self.comparator_lookup = self.dmm.map_comparator()
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
        return "-{}".format(comparison_string)

    @staticmethod
    def _to_cb_timestamp(ts: str) -> str:
        stripped = ts[2:-2]
        if '.' in stripped:
            stripped = stripped.split('.', 1)[0]
        return stripped

    def _format_start_stop_qualifier(self, expression, qualifier: StartStopQualifier) -> str:
        start = self._to_cb_timestamp(qualifier.start)
        stop = self._to_cb_timestamp(qualifier.stop)

        return "{} and last_update:[{} TO {}]".format(expression, start, stop)

    @staticmethod
    def _check_value_type(value):
        """
        Determine the type (ipv4, ipv6, mac, date, etc) of the provided value.
        See: https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/stix_shifter_utils/stix_translation/src/json_to_stix/observable.py#L1

        :param value: query value
        :type value: int/str
        :return: type of value
        :rtype: str
        """
        value = str(value)
        for key, pattern in observable.REGEX.items():
            if bool(re.search(pattern, value)):
                return key
        return None

    def _parse_mapped_fields(self, value, comparator, mapped_fields_array) -> str:
        """Convert a list of mapped fields into a query string."""
        comparison_strings = []
        value_type = None
        str_ = None

        if isinstance(value, str):
            value = [value]

        for val in value:
            value_type = self._check_value_type(val)

            for mapped_field in mapped_fields_array:
                # Only use the ipv4 fields when the value is an actual ipv4 address or range
                skip = ('ipv4' in mapped_field and value_type not in ['ipv4', 'ipv4_cidr'])
                # Only use the ipv6 fields when the value is an actual ipv6 address or range
                skip = skip or ('ipv6' in mapped_field and value_type not in ['ipv6', 'ipv6_cidr'])

                if not skip:
                    comparison_strings.append(f'{mapped_field}{comparator}{val}')

        # Only wrap in () if there's more than one comparison string
        if len(comparison_strings) == 1:
            str_ = comparison_strings[0]
        elif len(comparison_strings) > 1:
            str_ = f"({' or '.join(comparison_strings)})"
        else:
            raise RuntimeError((f'Failed to convert {mapped_fields_array} mapped fields into query string'))

        return str_
    
    def _parse_expression(self, expression, qualifier=None):
        if isinstance(expression, ComparisonExpression):
            comparison_string = ""
            # Base Case
            # Resolve STIX Object Path to a field in the target Data Model
            stix_object, stix_field = expression.object_path.split(':')

            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)
            mapped_field = mapped_fields_array[0]

            # Resolve the comparison symbol to use in the query string (usually just ':')
            comparator = self.comparator_lookup[str(expression.comparator)]
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
            elif (expression.comparator == ComparisonComparators.In and
                    isinstance(expression.value, SetValue)):
                value = list(map(self._escape_value, expression.value.element_iterator()))
            else:
                value = self._escape_value(expression.value)

            comparison_string = self._parse_mapped_fields(
                value=value,
                comparator=comparator,
                mapped_fields_array=mapped_fields_array
            )

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
            query_string = "({} {} {})".format(self._parse_expression(expression.expr2),
                                                     self.comparator_lookup[str(expression.operator)],
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
            operator = self.comparator_lookup[str(expression.operator)]
            expr1 = self._parse_expression(expression.expr1, qualifier=qualifier)
            expr2 = self._parse_expression(expression.expr2, qualifier=qualifier)
            return f'{expr1} {operator} {expr2}'
        elif isinstance(expression, Pattern):
            return self._parse_expression(expression.expression)
        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            return self._parse_expression(expression.observation_expression, expression)
        else:
            raise RuntimeError("Unknown Recursion Case for expression={}, type(expression)={}".format(
                expression, type(expression)))

    def _add_default_timerange(self, query):
        if self.time_range and 'last_update' not in query:
            query = "{} and last_update:-{}m".format(query, self.time_range)

        return query

    def parse_expression(self, pattern: Pattern):
        queries = self._parse_expression(pattern)
        return self._add_default_timerange(queries)


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    result_limit = options['result_limit']
    time_range = options['time_range']

    translated_statements = CbQueryStringPatternTranslator(pattern, data_model_mapping, result_limit, time_range)
    return translated_statements.queries
