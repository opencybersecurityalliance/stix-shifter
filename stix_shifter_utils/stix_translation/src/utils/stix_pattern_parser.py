from stix_shifter_utils.stix_translation.src.patterns.pattern_objects import ObservationExpression, ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators
import datetime
from stix_shifter_utils.stix_translation.src.utils.transformers import DateTimeToUnixTimestamp
import re


class PatternTranslator:
    comparator_lookup = {
        ComparisonExpressionOperators.And: "AND",
        ComparisonExpressionOperators.Or: "OR",
        ComparisonComparators.GreaterThan: ">",
        ComparisonComparators.GreaterThanOrEqual: ">=",
        ComparisonComparators.LessThan: "<",
        ComparisonComparators.LessThanOrEqual: "<=",
        ComparisonComparators.Equal: "=",
        ComparisonComparators.NotEqual: "!=",
        ComparisonComparators.Like: "LIKE",
        ComparisonComparators.In: "IN",
        ComparisonComparators.Matches: 'MATCHES',
        ObservationOperators.Or: 'OR',
        # Treat AND's as OR's -- Unsure how two ObsExps wouldn't cancel each other out.
        ObservationOperators.And: 'OR',
        ObservationOperators.FollowedBy: 'FOLLOWEDBY',
        ComparisonComparators.IsSuperSet: 'ISSUPERSET',
        ComparisonComparators.IsSubSet: 'ISSUBSET'
    }

    def __init__(self, pattern: Pattern, time_range):
        self.parsed_pattern = []
        # Set times based on default time_range or what is in the options
        # START STOP qualifiers will override this
        end_time = datetime.datetime.utcnow()
        self.end_time = DateTimeToUnixTimestamp.transform(end_time)
        go_back_in_minutes = datetime.timedelta(minutes=time_range)
        start_time = end_time - go_back_in_minutes
        self.start_time = DateTimeToUnixTimestamp.transform(start_time)
        self.qualifier_timerange_override = False
        self.parse_expression(pattern)

    def _parse_expression(self, expression, qualifier=None) -> str:
        if isinstance(expression, ComparisonExpression):  # Base Case
            # Resolve STIX Object Path to a field in the target Data Model
            stix_object, stix_field = expression.object_path.split(':')
            comparator = self.comparator_lookup[expression.comparator]
            if expression.negated:
                comparator = 'NOT ' + comparator
            if qualifier is not None:
                self._convert_qualifier_times_to_unix_times(qualifier)
            self.parsed_pattern.append({'attribute': expression.object_path, 'comparison_operator': comparator, 'value': expression.value})
        elif isinstance(expression, CombinedComparisonExpression):
            if qualifier is not None:
                self._convert_qualifier_times_to_unix_times(qualifier)
            self._parse_expression(expression.expr1)
            self._parse_expression(expression.expr2)

        elif isinstance(expression, ObservationExpression):
            self._parse_expression(expression.comparison_expression, qualifier)

        elif hasattr(expression, 'qualifier') and hasattr(expression, 'observation_expression'):
            if isinstance(expression.observation_expression, CombinedObservationExpression):
                self._parse_expression(expression.observation_expression.expr1)
                self._parse_expression(expression.observation_expression.expr2, expression.qualifier)
            else:
                self._parse_expression(expression.observation_expression.comparison_expression, expression.qualifier)
        elif isinstance(expression, CombinedObservationExpression):
            self._parse_expression(expression.expr1)
            self._parse_expression(expression.expr2)
        elif isinstance(expression, Pattern):
            self._parse_expression(expression.expression)
        else:
            raise RuntimeError("Unknown Recursion Case for expression={}, type(expression)={}".format(
                expression, type(expression)))

    def _convert_qualifier_times_to_unix_times(self, qualifier):
        split_object = qualifier.split("'")
        start_time = split_object[1]
        end_time = split_object[3]
        # Add subseconds to timestamp if it's missing
        pattern = "\.\d+Z$"
        if not bool(re.search(pattern, start_time)):
            start_time = re.sub('Z$', '.000Z', start_time)
        if not bool(re.search(pattern, end_time)):
            end_time = re.sub('Z$', '.000Z', end_time)
        # convert from string format '2019-01-18T08:30:16.227Z'
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        start_time = DateTimeToUnixTimestamp.transform(start_time)
        end_time = DateTimeToUnixTimestamp.transform(end_time)
        if not self.qualifier_timerange_override or self.start_time > start_time:
            self.start_time = start_time
        if not self.qualifier_timerange_override or self.end_time < end_time:
            self.end_time = end_time
        self.qualifier_timerange_override = True

    def parse_expression(self, pattern: Pattern):
        return self._parse_expression(pattern)


def parse_stix(pattern: Pattern, time_range):
    x = PatternTranslator(pattern, time_range)
    return {'parsed_stix': x.parsed_pattern, 'start_time': x.start_time, 'end_time': x.end_time}
