# Generated from STIXPattern.g4 by ANTLR 4.8
from antlr4 import *

# This class defines a complete generic visitor for a parse tree produced by STIXPatternParser.

class STIXPatternVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by STIXPatternParser#pattern.
    def visitPattern(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#observationExpressions.
    def visitObservationExpressions(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#observationExpressionOr.
    def visitObservationExpressionOr(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#observationExpressionAnd.
    def visitObservationExpressionAnd(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#observationExpressionRepeated.
    def visitObservationExpressionRepeated(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#observationExpressionSimple.
    def visitObservationExpressionSimple(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#observationExpressionCompound.
    def visitObservationExpressionCompound(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#observationExpressionWithin.
    def visitObservationExpressionWithin(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#observationExpressionStartStop.
    def visitObservationExpressionStartStop(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#comparisonExpression.
    def visitComparisonExpression(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#comparisonExpressionAnd.
    def visitComparisonExpressionAnd(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#propTestEqual.
    def visitPropTestEqual(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#propTestOrder.
    def visitPropTestOrder(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#propTestSet.
    def visitPropTestSet(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#propTestLike.
    def visitPropTestLike(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#propTestRegex.
    def visitPropTestRegex(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#propTestIsSubset.
    def visitPropTestIsSubset(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#propTestIsSuperset.
    def visitPropTestIsSuperset(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#propTestParen.
    def visitPropTestParen(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#startStopQualifier.
    def visitStartStopQualifier(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#withinQualifier.
    def visitWithinQualifier(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#repeatedQualifier.
    def visitRepeatedQualifier(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#objectPath.
    def visitObjectPath(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#objectType.
    def visitObjectType(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#firstPathComponent.
    def visitFirstPathComponent(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#indexPathStep.
    def visitIndexPathStep(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#pathStep.
    def visitPathStep(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#keyPathStep.
    def visitKeyPathStep(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#setLiteral.
    def visitSetLiteral(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#primitiveLiteral.
    def visitPrimitiveLiteral(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by STIXPatternParser#orderableLiteral.
    def visitOrderableLiteral(self, ctx):
        return self.visitChildren(ctx)


