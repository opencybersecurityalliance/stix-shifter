from enum import Enum
import typing
import re


class ComparisonComparators(Enum):
    """ Used inside a Comparison Expression to describe a relationship between a field and value. """
    (
        Equal,
        NotEqual,
        GreaterThan,
        LessThan,
        GreaterThanOrEqual,
        LessThanOrEqual,
        In,
        Like,
        Matches,
        IsSuperSet,
        IsSubSet
    ) = range(11)

    def __repr__(self):
        return self._name_


class ComparisonExpressionOperators(Enum):
    """ Used to combine two Comparison Expressions together inside an ObservationExpression"""
    (
        And,
        Or
    ) = range(2)

    def __repr__(self):
        return self._name_


class ObservationOperators(Enum):
    """ Used to combine two or more ObservationExpressions."""
    (
        And,
        Or,
        FollowedBy
    ) = range(3)

    def __repr__(self):
        return self._name_


class STIX2Value:
    pass


class SetValue(STIX2Value):
    def __init__(self):
        self.values = []
        self.is_open = True

    def append(self, value):
        if self.is_open:
            self.values.append(value)
        else:
            raise RuntimeError("Cannot append to closed Set")

    def close(self):
        self.is_open = False

    def element_iterator(self):
        for value in self.values:
            yield str(value)

    def __str__(self):
        return "({})".format(str(self.values).lstrip('[').rstrip(']'))


class BaseComparisonExpression:
    pass


class ComparisonExpression(BaseComparisonExpression):
    def __init__(self, object_path, value, comparator: ComparisonComparators, negated: bool=False):
        if not isinstance(comparator, ComparisonComparators):
            raise RuntimeWarning("{} is not a ComparisonComparator".format(comparator))
        self.object_path = object_path
        self.value = value
        self.comparator = comparator
        self.negated = negated

    def __repr__(self):
        return "ComparisonExpression({field} {comparator} {value})".format(comparator=self.comparator,
                                                                           field=self.object_path,
                                                                           value=self.value)


class CombinedComparisonExpression(BaseComparisonExpression):
    def __init__(self, expr1: BaseComparisonExpression, expr2: BaseComparisonExpression,
                 operator: ComparisonExpressionOperators) -> None:
        if not all((isinstance(expr1, BaseComparisonExpression), isinstance(expr2, BaseComparisonExpression),
                    isinstance(operator, ComparisonExpressionOperators))):
            raise RuntimeWarning("{} constructor called with wrong types".format(__class__)) # noqa: F821
        self.expr1 = expr1
        self.expr2 = expr2
        self.operator = operator

    def __repr__(self) -> str:
        return "CombinedComparisonExpression({expr1} {operator} {expr2})".format(expr1=self.expr1,
                                                                                 operator=self.operator,
                                                                                 expr2=self.expr2)


class BaseObservationExpression:
    pass


class ObservationExpression(BaseObservationExpression):
    def __init__(self, comparison_expression: BaseComparisonExpression) -> None:
        if not isinstance(comparison_expression, BaseComparisonExpression):
            raise RuntimeWarning("{} constructor called with wrong types".format(__class__)) # noqa: F821
        self.comparison_expression = comparison_expression

    def __repr__(self) -> str:
        return "ObservationExpression({expr})".format(expr=self.comparison_expression)


class CombinedObservationExpression(BaseObservationExpression):
    # This method is recursively hit when there are more than two base observation expressions
    # A CombinedObservationExpression will only contain up to two ObservationExpressions, joined by an ObservationOperator
    def __init__(self, expr1: BaseObservationExpression, expr2: BaseObservationExpression,
                 operator: ObservationOperators) -> None:
        self.expr1 = expr1
        self.expr2 = expr2
        self.operator = operator

        self.__check_instances()

    def __check_instances(self):

        if hasattr(self.expr1, 'observation_expression'):
            wrong_type = not isinstance(self.expr1.observation_expression, BaseObservationExpression)
        else:
            wrong_type = not isinstance(self.expr1, BaseObservationExpression)

        if wrong_type:
            raise RuntimeWarning("{} constructor called with wrong types".format(__class__)) # noqa: F821

        if hasattr(self.expr2, 'observation_expression'):
            wrong_type = not isinstance(self.expr2.observation_expression, BaseObservationExpression)
        else:
            wrong_type = not isinstance(self.expr2, BaseObservationExpression)
        if wrong_type:
            raise RuntimeWarning("{} constructor called with wrong types".format(__class__)) # noqa: F821

        if not isinstance(self.operator, ObservationOperators):
            raise RuntimeWarning("{} constructor called with wrong types".format(__class__)) # noqa: F821

    def __repr__(self) -> str:
        return "CombinedObservationExpression({expr1} {operator} {expr2})".format(expr1=self.expr1,
                                                                                  operator=self.operator,
                                                                                  expr2=self.expr2)


class BaseQualifier:
    pass


class Qualifier(BaseQualifier):
    def __init__(self, qualifier, observation_expression: BaseObservationExpression) -> None:
        if not isinstance(observation_expression, BaseObservationExpression):
            raise RuntimeWarning("{} constructor called with wrong types".format(__class__)) # noqa: F821
        self.qualifier = qualifier
        self.observation_expression = observation_expression

    def __repr__(self) -> str:
        return "{observation_expression} Qualifier({qualifier})".format(observation_expression=self.observation_expression, qualifier=self.qualifier)

class StartStopQualifier(Qualifier):
    def __init__(self, qualifier, observation_expression: BaseObservationExpression, start: str, stop: str) -> None:
        if not isinstance(observation_expression, BaseObservationExpression):
            raise RuntimeWarning("{} constructor called with wrong types".format(__class__)) # noqa: F821
        self.qualifier = qualifier
        self.observation_expression = observation_expression
        self.start = start
        self.stop = stop

        pattern = "^t'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z'$"
        match = re.search(pattern, start)
        if not bool(match):
            raise RuntimeError("Invalid STIX timestamp {}".format(start))

        match = re.search(pattern, stop)
        if not bool(match):
            raise RuntimeError("Invalid STIX timestamp {}".format(stop))

    def __repr__(self) -> str:
        return "{observation_expression} StartStopQualifier({qualifier}, start={start}, stop={stop})".format(observation_expression=self.observation_expression, qualifier=self.qualifier, start=self.start, stop=self.stop)

class Pattern:
    def __init__(self, expression: BaseObservationExpression, qualifier=None) -> None:
        self.expression = expression

    def __repr__(self) -> str:
        return "Pattern[{expression}]".format(expression=self.expression)
