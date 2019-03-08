from stix_shifter.stix_translation.src.patterns.pattern_objects import ObservationExpression, ComparisonExpression, \
    ComparisonExpressionOperators, ComparisonComparators, Pattern, \
    CombinedComparisonExpression, CombinedObservationExpression, ObservationOperators
import datetime


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

    def __init__(self, pattern: Pattern, timerange):
        self.parsed_pattern = []
        # Set times based on default timerange or what is in the options
        # START STOP will override this
        self.end_time = datetime.datetime.utcnow()
        go_back_in_minutes = datetime.timedelta(minutes=timerange)
        self.start_time = self.end_time - go_back_in_minutes
        self.parse_expression(pattern)

    def _parse_expression(self, expression, qualifier=None) -> str:
        if isinstance(expression, ComparisonExpression):  # Base Case
            # Resolve STIX Object Path to a field in the target Data Model
            stix_object, stix_field = expression.object_path.split(':')
            comparator = self.comparator_lookup[expression.comparator]
            self.parsed_pattern.append({'attribute': expression.object_path, 'comparison_operator': comparator, 'value': expression.value})
            # todo: if qualifier is not None then update start and end times.
        elif isinstance(expression, CombinedComparisonExpression):
            # todo: if qualifier is not None then update start and end times.
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

    def parse_expression(self, pattern: Pattern):
        return self._parse_expression(pattern)


def parse_stix(pattern: Pattern, timerange):
    x = PatternTranslator(pattern, timerange)
    return {'parsed_stix': x.parsed_pattern, 'start_time': x.start_time, 'end_time': x.end_time}
