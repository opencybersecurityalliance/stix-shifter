import logging
import re

from datetime import datetime, timedelta
from stix_shifter_utils.stix_translation.src.json_to_stix import observable
from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, \
    ComparisonExpression, ComparisonExpressionOperators, ComparisonComparators, Pattern, StartStopQualifier, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators, SetValue


logger = logging.getLogger(__name__)


class CbCloudQueryStringPatternTranslator:
    """Carbon Black Cloud STIX to query string pattern translator."""

    def __init__(self, pattern: Pattern, data_model_mapper, time_range):
        """CbCloudQueryStringPatternTranslator constructor."""
        self.dmm = data_model_mapper
        self.comparator_lookup = self.dmm.map_comparator()
        self.pattern = pattern
        self.time_range = time_range  # filter results to the last x minutes
        self.queries = self.parse_expression(pattern)

    @classmethod
    def _format_equality(cls, value) -> str:
        """Format a value that's part of an equality comparison."""
        return f'{cls._escape_value(value)}'

    @classmethod
    def _format_lte(cls, value) -> str:
        """Format a value that's part of a LessThanOrEqual comparison."""
        return f'[* TO {cls._escape_value(value)}]'

    @classmethod
    def _format_gte(cls, value) -> str:
        """Format a value that's part of a GreaterThanOrEqual comparison."""
        return f'[{cls._escape_value(value)} TO *]'

    @classmethod
    def _format_lt(cls, value) -> str:
        """Format a value that's part of a LessThan comparison."""
        if isinstance(value, int):
            value = value - 1
        return cls._format_lte(value)

    @classmethod
    def _format_gt(cls, value) -> str:
        """Format a value that's part of a GreaterThan comparison."""
        if isinstance(value, int):
            value = value + 1
        return cls._format_gte(value)

    @classmethod
    def _format_start_stop_qualifier(cls, expression, qualifier: StartStopQualifier) -> str:
        """Convert a STIX start stop qualifier into a query string.

        Carbon Black Cloud defines a timerange with a start and stop value
        based on the device_timestamp field. The timerange can either be
        specified as part of the process search query using the device_timestamp
        field directly or via a separate field in the API JSON request:

        "time_range": {
          "end": "2020-01-27T18:34:04Z",
          "start": "2020-01-18T18:34:04Z,
        }
        """
        start = cls._stix_to_cbcloud_timestamp(qualifier.start)
        stop = cls._stix_to_cbcloud_timestamp(qualifier.stop)
        return f'({expression}) AND device_timestamp:[{start} TO {stop}]'

    @staticmethod
    def _escape_value(value) -> str:
        """Trim whitespace and escape specific characters in a value."""
        if isinstance(value, str):
            value = value.strip()
        if isinstance(value, str) and not re.match(r'^\[[\*\sa-z0-9.:-]*to[\*\sa-z0-9.:-]*\]$', value.lower()):
            value = value.replace('\\', '\\\\')
            value = value.replace('\"', '\\"')
            value = value.replace('(', '\\(')
            value = value.replace(')', '\\)')
            value = value.replace(' ', '\\ ')
        return value

    @staticmethod
    def _negate_comparison(comparison_string: str) -> str:
        return '-{}'.format(comparison_string)

    @staticmethod
    def _datetime_to_cbcloud_timestamp(timestamp: datetime) -> str:
        """Convert a datetime object to a Carbon Black Cloud timestamp."""
        try:
            str_ = timestamp.strftime('%Y-%m-%dT%H:%M:%S')
        except ValueError:
            str_ = '0000-00-00T00:00:00'

        return f'{str_}Z'

    @staticmethod
    def _stix_to_cbcloud_timestamp(timestamp: str) -> str:
        """Convert a STIX timestamp to a Carbon Black Cloud timestamp."""
        return timestamp[2:-1]

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
            str_ = f"({' OR '.join(comparison_strings)})"
        else:
            raise RuntimeError((f'Failed to convert {mapped_fields_array} mapped fields into query string'))

        return str_

    def _parse_expression(self, expression, qualifier=None):
        """Parse a STIX expression into a query string."""
        if isinstance(expression, ComparisonExpression):
            # Resolve STIX Object Path to a field in the target Data Model
            stix_object, stix_field = expression.object_path.split(':')

            # Multiple data source fields may map to the same STIX Object
            mapped_fields_array = self.dmm.map_field(stix_object, stix_field)

            # Resolve the comparison symbol to use in the query string (usually just ':')
            comparator = self.comparator_lookup[str(expression.comparator)]

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
                    comparison_string = self._format_start_stop_qualifier(comparison_string, qualifier)
                else:
                    raise RuntimeError(f'Unknown Qualifier: {qualifier}')

            return comparison_string

        elif isinstance(expression, CombinedComparisonExpression):
            # Wrap nested combined comparison expressions in parentheses
            fmt1 = "({})" if isinstance(expression.expr2, CombinedComparisonExpression) else "{}"
            fmt2 = "({})" if isinstance(expression.expr1, CombinedComparisonExpression) else "{}"
            operator = self.comparator_lookup[str(expression.operator)]

            # Note: it seems the ordering of the expressions is reversed at a lower level
            # so we reverse it here so that it is as expected.
            query_string = (fmt1 + " {} " + fmt2).format(
                self._parse_expression(expression.expr2),
                self.comparator_lookup[str(expression.operator)],
                self._parse_expression(expression.expr1)
            )

            if qualifier is not None:
                if isinstance(qualifier, StartStopQualifier):
                    query_string = self._format_start_stop_qualifier(query_string, qualifier)
                else:
                    raise RuntimeError(f'Unknown Qualifier: {qualifier}')

            return query_string

        elif isinstance(expression, ObservationExpression):
            # An observation can contain a qualifier
            query_string = self._parse_expression(expression.comparison_expression, qualifier=qualifier)
            return query_string

        elif isinstance(expression, CombinedObservationExpression):
            # A combined observation can consist of observations containing a qualifier
            operator = self.comparator_lookup[str(expression.operator)]
            expr1 = self._parse_expression(expression.expr1, qualifier=qualifier)
            expr2 = self._parse_expression(expression.expr2, qualifier=qualifier)
            return f'({expr1}) {operator} ({expr2})'

        elif isinstance(expression, Pattern):
            return self._parse_expression(expression.expression)

        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            # When there's a startstop qualifier the object type is StartStopQualifier
            return self._parse_expression(expression.observation_expression, qualifier=expression)

        else:
            raise RuntimeError(
                f'Unknown Recursion Case for expression={expression}, type(expression)={type(expression)}'
            )

    def _add_default_timerange(self, query):
        """Add a default timerange to a query string."""
        today = datetime.utcnow()
        if self.time_range:
            start = self._datetime_to_cbcloud_timestamp(today - timedelta(minutes=self.time_range))
        stop = self._datetime_to_cbcloud_timestamp(today)

        # Add a default timerange when there's no time constraint in the query.
        # Carbon Black Cloud defines a timerange with a start and stop value
        # based on the device_timestamp field. The timerange can either be
        # specified as part of the process search query using the device_timestamp
        # field directly or via a separate field in the API JSON request:
        #
        # "time_range": {
        #   "end": "2020-01-27T18:34:04Z",
        #   "start": "2020-01-18T18:34:04Z,
        # }
        if self.time_range and 'device_timestamp' not in query:
            query = f'({query}) AND device_timestamp:[{start} TO {stop}]'

        return query

    def _add_no_enriched(self, query):
        """Append exclusion for enriched events to the query string."""
        return f'({query}) AND -enriched:True'

    def parse_expression(self, pattern: Pattern):
        """Translation entry point."""
        query = self._parse_expression(pattern)
        query = self._add_default_timerange(query)
        return self._add_no_enriched(query)


def translate_pattern(pattern: Pattern, data_model_mapping, options):
    time_range = options['time_range']
    translated_statements = CbCloudQueryStringPatternTranslator(pattern, data_model_mapping, time_range)
    return translated_statements.queries
