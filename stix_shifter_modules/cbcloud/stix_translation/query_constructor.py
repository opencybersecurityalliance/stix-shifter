import json
import logging
import re

from datetime import datetime, timedelta
from stix_shifter_utils.stix_translation.src.json_to_stix import observable
from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, \
    ComparisonExpression, ComparisonExpressionOperators, ComparisonComparators, Pattern, StartStopQualifier, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators


LOGGER = logging.getLogger(__name__)


class CbCloudQueryStringPatternTranslator:
    # Change comparator values to match with supported data source operators
    comparator_lookup = {
        ComparisonExpressionOperators.And: 'AND',
        ComparisonExpressionOperators.Or: 'OR',
        ComparisonComparators.Equal: ':',
        ComparisonComparators.NotEqual: ':',
        ComparisonComparators.GreaterThan: ':',
        ComparisonComparators.GreaterThanOrEqual: ':',
        ComparisonComparators.LessThan: ':',
        ComparisonComparators.LessThanOrEqual: ':',
        ObservationOperators.Or: 'OR',
        # Treat AND's as OR's -- Unsure how two ObsExps wouldn't cancel each other out.
        ObservationOperators.And: 'OR'
    }

    def __init__(self, pattern: Pattern, data_model_mapper, result_limit, time_range):
        self.dmm = data_model_mapper
        self.pattern = pattern
        self.result_limit = result_limit
        self.time_range = time_range  # filter results to the last x minutes
        self.queries = [json.dumps(translation) for translation in self.parse_expression(pattern)]

    @classmethod
    def _format_equality(cls, value) -> str:
        return f'{cls._escape_value(value)}'

    @classmethod
    def _format_lte(cls, value) -> str:
        return f'[* TO {cls._escape_value(value)}]'

    @classmethod
    def _format_gte(cls, value) -> str:
        return f'[{cls._escape_value(value)} TO *]'

    # Note: documentation appears to be wrong
    @classmethod
    def _format_lt(cls, value) -> str:
        if isinstance(value, int):
            value = value - 1
        return cls._format_lte(value)

    @classmethod
    def _format_gt(cls, value) -> str:
        if isinstance(value, int):
            value = value + 1
        return cls._format_gte(value)

    @staticmethod
    def _escape_value(value) -> str:
        if isinstance(value, str):
            value = value.replace('\\', '\\\\')
            value = value.replace('\"', '\\"')
            value = value.replace('(', '\\(')
            value = value.replace(')', '\\)')
            value = value.replace(' ', '\\ ')
        return value

    @classmethod
    def _format_start_stop_qualifier(cls, expression, qualifier: StartStopQualifier) -> str:
        start = cls._stix_to_cbcloud_timestamp(qualifier.start)
        stop = cls._stix_to_cbcloud_timestamp(qualifier.stop)

        return f'(({expression}) AND process_start_time:[{start} TO *] AND device_timestamp:[* TO {stop}])'

    @staticmethod
    def _negate_comparison(comparison_string: str) -> str:
        return '-{}'.format(comparison_string)

    @staticmethod
    def _datetime_to_cbcloud_timestamp(timestamp: datetime) -> str:
        try:
            str_ = timestamp.strftime('%Y-%m-%dT%H:%M:%S')
        except ValueError:
            str_ = '0000-00-00T00:00:00'

        return f'{str_}Z'

    @staticmethod
    def _stix_to_cbcloud_timestamp(timestamp: str) -> str:
        return timestamp[2:-1]

    @staticmethod
    def _parse_mapped_fields(value, comparator, mapped_fields_array) -> str:
        comparison_strings = []
        value_type = None

        for key, pattern in observable.REGEX.items():
            if bool(re.search(pattern, value)):
                value_type = key

        for mapped_field in mapped_fields_array:
            # Only use the ipv4 fields when the value is an actual ipv4 address or range
            skip = ('ipv4' in mapped_field and value_type not in ['ipv4', 'ipv4_cidr'])
            # Only use the ipv6 fields when the value is an actual ipv6 address or range
            skip = skip or ('ipv6' in mapped_field and value_type not in ['ipv6', 'ipv6_cidr'])

            if not skip:
                comparison_strings.append(f'{mapped_field}{comparator}{value}')

        # Only wrap in () if there's more than one comparison string
        if len(comparison_strings) == 1:
            str_ = comparison_strings[0]
        elif len(comparison_strings) > 1:
            str_ = f"({' OR '.join(comparison_strings)})"

        return str_

    # the return type of this function is a string for expressions types up to CombinedComparionExpression
    # for expressions of ObservableExpression or Higher in the grammar the return type is a list of dictionaries
    # e.g. [{'query': 'foo'}, {'query':'bar'}]
    def _parse_expression(self, expression, qualifier=None):
        if isinstance(expression, ComparisonExpression):
            # Base Case
            # Resolve STIX Object Path to a field in the target Data Model
            stix_object, stix_field = expression.object_path.split(':')

            # Multiple data source fields may map to the same STIX Object
            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)

            # Resolve the comparison symbol to use in the query string (usually just ':')
            comparator = self.comparator_lookup[expression.comparator]

            # Some values are formatted differently based on how they're being compared
            if (expression.comparator == ComparisonComparators.Equal or
                    expression.comparator == ComparisonComparators.NotEqual):
                value = self._format_equality(expression.value)
            elif expression.comparator == ComparisonComparators.LessThan:
                value = self._format_lt(expression.value)
            elif expression.comparator == ComparisonComparators.GreaterThan:
                value = self._format_gt(expression.value)
            elif expression.comparator == ComparisonComparators.LessThanOrEqual:
                value = self._format_lte(expression.value)
            elif expression.comparator == ComparisonComparators.GreaterThanOrEqual:
                value = self._format_gte(expression.value)
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
                    comparison_string = self._format_start_stop_qualifier(comparison_string, qualifier)
                else:
                    raise RuntimeError(f'Unknown Qualifier: {qualifier}')

            return comparison_string

        elif isinstance(expression, CombinedComparisonExpression):
            # Wrap nested combined comparison expressions in parentheses
            fmt1 = "({})" if isinstance(expression.expr2, CombinedComparisonExpression) else "{}"
            fmt2 = "({})" if isinstance(expression.expr1, CombinedComparisonExpression) else "{}"

            # Note: it seems the ordering of the expressions is reversed at a lower level
            # so we reverse it here so that it is as expected.
            query_string = (fmt1 + " {} " + fmt2).format(
                self._parse_expression(expression.expr2),
                self.comparator_lookup[expression.operator],
                self._parse_expression(expression.expr1)
            )

            if qualifier is not None:
                if isinstance(qualifier, StartStopQualifier):
                    query_string = self._format_start_stop_qualifier(query_string, qualifier)
                else:
                    raise RuntimeError(f'Unknown Qualifier: {qualifier}')

            return query_string

        elif isinstance(expression, ObservationExpression):
            query_string = self._parse_expression(expression.comparison_expression, qualifier=qualifier)
            return query_string

        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            return self._parse_expression(expression.observation_expression, expression)

        elif isinstance(expression, CombinedObservationExpression):
            # This code is only correct because we assume AND is OR for observation expressions
            operator = self.comparator_lookup[expression.operator]
            expr1 = self._parse_expression(expression.expr1, qualifier=qualifier)
            expr2 = self._parse_expression(expression.expr2, qualifier=qualifier)
            # OR both ObservationExpressions together
            return f'({expr1}) {operator} ({expr2})'

        elif isinstance(expression, Pattern):
            return self._parse_expression(expression.expression)

        else:
            raise RuntimeError(
                f'Unknown Recursion Case for expression={expression}, type(expression)={type(expression)}'
            )

    def _add_default_timerange(self, query):
        today = datetime.utcnow()
        start = self._datetime_to_cbcloud_timestamp(today - timedelta(minutes=self.time_range))
        stop = self._datetime_to_cbcloud_timestamp(today)
        trange = f'[{start} TO {stop}]'

        # Only add default timerange if there's no existing time constraint on the query
        if self.time_range and 'process_start_time' not in query and 'device_timestamp' not in query:
            query = f'({query}) AND (process_start_time:{trange} OR device_timestamp:{trange})'

        return query

    def _add_no_enriched(self, query):
        """Only retrieve non-enriched events."""
        return query + ' AND -enriched:True'

    def parse_expression(self, pattern: Pattern):
        queries = self._parse_expression(pattern)
        queries = self._add_default_timerange(queries)
        # Return a single-item list
        return [self._add_no_enriched(queries)]


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    result_limit = options['result_limit']
    time_range = options['time_range']
    translated_statements = CbCloudQueryStringPatternTranslator(pattern, data_model_mapping, result_limit, time_range)
    return translated_statements.queries
