import logging

import dateutil.parser
from antlr4 import CommonTokenStream, ParseTreeWalker, InputStream
from .grammar import STIXPatternListener, STIXPatternParser, STIXPatternLexer
from .pattern_objects import ObservationExpression, CombinedComparisonExpression, ObservationOperators, \
    ComparisonExpressionOperators, ComparisonComparators, SetValue, ComparisonExpression, CombinedObservationExpression, Pattern, Qualifier, StartStopQualifier

logger = logging.getLogger(__name__)


class STIXQueryBuilder(STIXPatternListener):

    query_comparators = {
        'and': ComparisonExpressionOperators.And,
        # 'not': ComparisonExpressionOperators.Not,
        'or': ComparisonExpressionOperators.Or,
    }

    def __init__(self) -> None:
        self._stack = []
        # self._saved_stack is used to save the main stack, when a second stack is used to parse a sequence
        # of indterminate length (e.g. a STIX Patterning Set).
        self._saved_stack = self._stack

    def push(self, x) -> None:
        self._stack.append(x)

    def pop(self):
        return self._stack.pop()

    def exitObjectPath(self, ctx) -> None:
        logger.debug("{} {} {}".format("ObjectPath", ctx, ctx.getText()))
        # Single quotes are valid for any path but required for those with dashes.
        # They're not really relevant once they're parsed out, so just remove them
        self.push(ctx.getText().replace("'", ""))

    def exitPropTestLike(self, ctx: STIXPatternParser.PropTestLikeContext) -> None:
        logger.debug("{} {} {}".format("PropTestLike", ctx, ctx.getText()))
        value = self.pop()
        object_path = self.pop()
        negated = ctx.NOT()
        self.push(ComparisonExpression(object_path, value, ComparisonComparators.Like, negated=negated))

    def exitPrimitiveLiteral(self, ctx) -> None:
        logger.debug("{} {} {}".format("PrimitiveLiteral", ctx, ctx.getText()))
        # This can be TimestampLiteral or BoolLiteral.  These should be handed with more specific targets, e.g.
        #   exitTimestampLiteral and exitBoolLiteral.
        # self.push(ctx.getText().strip("'"))

    def exitPropTestRegex(self, ctx: STIXPatternParser.PropTestRegexContext) -> None:
        logger.debug("{} {} {}".format("PropTestRegex", ctx, ctx.getText()))
        logger.debug("stack={}".format(self._stack))
        value = self.pop()
        object_path = self.pop()
        negated = ctx.NOT()
        self.push(ComparisonExpression(object_path, value, ComparisonComparators.Matches, negated=negated))

    def exitPropTestEqual(self, ctx: STIXPatternParser.PropTestEqualContext) -> None:
        logger.debug("{} {} {} | stack={}".format("PropTestEqual", ctx, ctx.getText(), self._stack))
        value = self.pop()
        object_path = self.pop()
        negated = ctx.NOT()

        if ctx.EQ():
            comparator = ComparisonComparators.Equal
        elif ctx.NEQ():
            comparator = ComparisonComparators.NotEqual
        else:
            raise RuntimeWarning("Unrecognized Equality Comparator")
        self.push(ComparisonExpression(object_path, value, comparator, negated=negated))

    def exitPropTestOrder(self, ctx: STIXPatternParser.PropTestOrderContext) -> None:
        logger.debug("{} {} {} | stack={}".format("PropTestOrder", ctx, ctx.getText(), self._stack))
        value = self.pop()
        object_path = self.pop()
        negated = str(ctx.NOT()) == "NOT"

        if ctx.GT():
            comparator = ComparisonComparators.GreaterThan
        elif ctx.LT():
            comparator = ComparisonComparators.LessThan
        elif ctx.GE():
            comparator = ComparisonComparators.GreaterThanOrEqual
        elif ctx.LE():
            comparator = ComparisonComparators.LessThanOrEqual
        else:
            raise RuntimeWarning("Unrecognized Ordering Comparator")

        self.push(ComparisonExpression(object_path, value, comparator=comparator, negated=negated))

    def exitPropTestSet(self, ctx: STIXPatternParser.PropTestSetContext) -> None:
        logger.debug("{} {} {} | stack={}".format("PropTestSet", ctx, ctx.getText(), self._stack))
        vals = self.pop()
        object_path = self.pop()
        negated = str(ctx.NOT()) == "NOT"

        self.push(ComparisonExpression(object_path, vals, ComparisonComparators.In, negated=negated))

    def enterSetLiteral(self, ctx: STIXPatternParser.SetLiteralContext) -> None:
        """ Called when Set Literals begin being parsed.  Since the length is unpredictable, replace the stack
        with a SetValue object. SetValue is also a stack (implements .pop() and .push()).  When the SetLiteral is
        done being parsed, the original stack will be restored, and the SetValue pushed onto it."""
        self._saved_stack = self._stack
        self._stack = SetValue()

    def exitSetLiteral(self, ctx: STIXPatternParser.SetLiteralContext):
        """Called when SetLiterals are done being parsed. Restore the stack and push the built SetValue object onto
        the top of the stack so it can be used in a comparison expression."""
        if not isinstance(self._stack, SetValue):
            raise RuntimeError("Exiting Set Literal but current stack isn't Set Object")
        else:
            set_value = self._stack
            set_value.close()
            self._stack = self._saved_stack
            self.push(set_value)

    def exitOrderableLiteral(self, ctx: STIXPatternParser.OrderableLiteralContext):
        """  Can be IntPosLiteral, IntNegLiteral, FloatPosLiteral, FloatNegLiteral, stringLiteral, BinaryLiteral, HexLiteral, TimestampLiteral """
        logger.debug("{} {} {}".format("OrderableLiteral", ctx, ctx.getText()))
        if ctx.stringLiteral():
            pass  # Strings should have already been pushed onto the stack
        elif ctx.IntPosLiteral() or ctx.IntNegLiteral():
            self.push(int(ctx.getText()))
        elif ctx.FloatPosLiteral() or ctx.FloatNegLiteral():
            self.push(float(ctx.getText()))
        elif ctx.BinaryLiteral():
            # Leave these as strings for now
            self.push(ctx.getText())
        elif ctx.HexLiteral():
            # Leave these as strings for now
            self.push(ctx.getText())
        elif ctx.TimestampLiteral():  # TODO: is this the right way?
            ts = dateutil.parser.parse(ctx.getText().strip("'").strip("t"))
            self.push(ts)

    def exitComparisonExpressionAnded(self, ctx):
        logger.debug("{} {} {}".format("ComparisonExpressionAnded", ctx, ctx.getText()))
        exp1 = self.pop()
        exp2 = self.pop()
        self.push(CombinedComparisonExpression(exp1, exp2, ComparisonExpressionOperators.And))

    def exitComparisonExpressionOred(self, ctx) -> None:
        logger.debug("{} {} {}".format("ComparisonExpressionOred", ctx, ctx.getText()))
        exp1 = self.pop()
        exp2 = self.pop()
        self.push(CombinedComparisonExpression(exp1, exp2, ComparisonExpressionOperators.Or))

    def exitStringLiteral(self, ctx: STIXPatternParser.StringLiteralContext) -> None:
        logger.debug("{} {} {}".format("String", ctx, ctx.getText()))
        self.push(ctx.getText().strip("'").replace("\\\\", "\\"))

    def exitObservationExpressionSimple(self, ctx):
        # Roughly analogous to CQL DataModelQuery
        logger.debug("{} {} {}".format("ObservationExpressionSimple", ctx, ctx.getText()))
        comparison_expression = self.pop()

        # Done with this observation expression, the next one might have a different object type
        # object_name = self._current_object_type
        # self._current_object_type = None

        logger.debug("Current Parser Stack: {}".format(self._stack))
        # logger.debug("Building DMQ with object_name={}, action={}, query={}".format(object_name, self.action, query))
        # self.push(DataModelQuery(object_name=object_name, action=self.action, query=query))
        self.push(ObservationExpression(comparison_expression))

    def exitObservationExpressionAnd(self, ctx: STIXPatternParser.ObservationExpressionAndContext):
        logger.debug("{} {} {}".format("ObservationExpressionAnd", ctx, ctx.getText()))
        if ctx.AND():
            expr2 = self.pop()
            expr1 = self.pop()
            operator = ObservationOperators.And
            self.push(CombinedObservationExpression(expr1, expr2, operator))

    def exitObservationExpressionOr(self, ctx: STIXPatternParser.ObservationExpressionOrContext):
        logger.debug("{} {} {}".format("ObservationExpressionOr", ctx, ctx.getText()))
        if ctx.OR():  # Check if there's OR'd Observation Expressions
            expr2 = self.pop()
            expr1 = self.pop()
            operator = ObservationOperators.Or
            self.push(CombinedObservationExpression(expr1, expr2, operator))

    def exitObservationExpressionStartStop(self, ctx: STIXPatternParser.ObservationExpressionStartStopContext):
        logger.debug("{} {} {}".format("ObservationExpressionStartStop", ctx, ctx.getText()))
        qualifier = ctx.startStopQualifier()
        qualifier_text = qualifier.getText()  # Ex: "START'2016-06-01T00:00:00Z'STOP'2016-06-01T01:11:11Z'"
        observation = ctx.observationExpression()
        expression = self.pop()
        start_time = str(qualifier.TimestampLiteral(i=0))
        stop_time = str(qualifier.TimestampLiteral(i=1))
        observation_expression_with_qualifier = StartStopQualifier(qualifier_text, expression, start_time, stop_time)
        self.push(observation_expression_with_qualifier)

    def exitObservationExpressions(self, ctx: STIXPatternParser.ObservationExpressionsContext):
        logger.debug("{} {} {}".format("ObservationExpressions", ctx, ctx.getText()))
        if ctx.FOLLOWEDBY():
            expr2 = self.pop()
            expr1 = self.pop()
            operator = ObservationOperators.FollowedBy
            self.push(CombinedObservationExpression(expr1, expr2, operator))

    def exitPattern(self, ctx):
        logger.debug("{} {} {}".format("Pattern", ctx, ctx.getText()))
        observation_expression = self.pop()
        self.push(Pattern(observation_expression))

    def exitPropTestIsSuperset(self, ctx: STIXPatternParser.PropTestIsSupersetContext) -> None:
        logger.debug("{} {} {}".format("exitPropTestIsSuperset", ctx, ctx.getText()))
        value = self.pop()
        object_path = self.pop()
        self.push(ComparisonExpression(object_path, value, ComparisonComparators.IsSuperSet))

    def exitPropTestIsSubset(self, ctx: STIXPatternParser.PropTestIsSubsetContext) -> None:
        logger.debug("{} {} {}".format("propTestIsSubset", ctx, ctx.getText()))
        value = self.pop()
        object_path = self.pop()
        negated = ctx.NOT()
        self.push(ComparisonExpression(object_path, value, ComparisonComparators.IsSubSet, negated=negated))

# copied from CASCADE data_model (defined twice)


class InvalidFieldError(KeyError):
    pass


class InvalidActionError(ValueError):
    pass


class InvalidObjectError(ValueError):
    pass


class ParserError(ValueError):
    pass


def generate_query(query_string):
    try:
        lexer = STIXPatternLexer(InputStream(query_string))
        stream = CommonTokenStream(lexer)
        parser = STIXPatternParser(stream)
        builder = STIXQueryBuilder()
        tree = parser.pattern()
        walker = ParseTreeWalker()
        walker.walk(builder, tree)
        query = builder.pop()
        logger.debug(query)
    except Exception as e:
        raise ParserError(e)

    return query
