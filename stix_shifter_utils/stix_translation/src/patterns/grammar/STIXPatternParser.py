# Generated from stix_shifter_utils/stix_translation/src/patterns/grammar/STIXPattern.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,53,247,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,1,0,
        1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,5,1,50,8,1,10,1,12,1,53,9,1,1,2,
        1,2,1,2,1,2,1,2,1,2,5,2,61,8,2,10,2,12,2,64,9,2,1,3,1,3,1,3,1,3,
        1,3,1,3,5,3,72,8,3,10,3,12,3,75,9,3,1,4,1,4,1,4,1,4,1,4,1,4,1,4,
        1,4,1,4,3,4,86,8,4,1,4,1,4,1,4,1,4,1,4,1,4,5,4,94,8,4,10,4,12,4,
        97,9,4,1,5,1,5,1,5,1,5,1,5,1,5,5,5,105,8,5,10,5,12,5,108,9,5,1,6,
        1,6,1,6,1,6,1,6,1,6,5,6,116,8,6,10,6,12,6,119,9,6,1,7,1,7,3,7,123,
        8,7,1,7,1,7,1,7,1,7,1,7,3,7,130,8,7,1,7,1,7,1,7,1,7,1,7,3,7,137,
        8,7,1,7,1,7,1,7,1,7,1,7,3,7,144,8,7,1,7,1,7,1,7,1,7,1,7,3,7,151,
        8,7,1,7,1,7,1,7,1,7,1,7,3,7,158,8,7,1,7,1,7,1,7,1,7,1,7,3,7,165,
        8,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,3,7,174,8,7,1,8,1,8,1,9,1,9,1,10,
        1,10,1,10,1,10,1,10,1,11,1,11,1,11,1,11,1,12,1,12,1,12,1,12,1,13,
        1,13,1,13,1,13,3,13,197,8,13,1,14,1,14,1,15,1,15,1,16,1,16,1,16,
        1,16,1,16,1,16,3,16,209,8,16,1,16,1,16,5,16,213,8,16,10,16,12,16,
        216,9,16,1,17,1,17,1,17,1,17,1,17,1,17,5,17,224,8,17,10,17,12,17,
        227,9,17,1,17,1,17,3,17,231,8,17,1,18,1,18,3,18,235,8,18,1,19,1,
        19,1,19,1,19,1,19,1,19,1,19,1,19,3,19,245,8,19,1,19,0,7,2,4,6,8,
        10,12,32,20,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,
        38,0,6,1,0,30,31,1,0,32,35,2,0,2,2,4,4,1,0,28,29,2,0,7,7,28,28,2,
        0,1,2,49,49,262,0,40,1,0,0,0,2,43,1,0,0,0,4,54,1,0,0,0,6,65,1,0,
        0,0,8,85,1,0,0,0,10,98,1,0,0,0,12,109,1,0,0,0,14,173,1,0,0,0,16,
        175,1,0,0,0,18,177,1,0,0,0,20,179,1,0,0,0,22,184,1,0,0,0,24,188,
        1,0,0,0,26,192,1,0,0,0,28,198,1,0,0,0,30,200,1,0,0,0,32,208,1,0,
        0,0,34,230,1,0,0,0,36,234,1,0,0,0,38,244,1,0,0,0,40,41,3,2,1,0,41,
        42,5,0,0,1,42,1,1,0,0,0,43,44,6,1,-1,0,44,45,3,4,2,0,45,51,1,0,0,
        0,46,47,10,2,0,0,47,48,5,13,0,0,48,50,3,2,1,3,49,46,1,0,0,0,50,53,
        1,0,0,0,51,49,1,0,0,0,51,52,1,0,0,0,52,3,1,0,0,0,53,51,1,0,0,0,54,
        55,6,2,-1,0,55,56,3,6,3,0,56,62,1,0,0,0,57,58,10,2,0,0,58,59,5,11,
        0,0,59,61,3,4,2,3,60,57,1,0,0,0,61,64,1,0,0,0,62,60,1,0,0,0,62,63,
        1,0,0,0,63,5,1,0,0,0,64,62,1,0,0,0,65,66,6,3,-1,0,66,67,3,8,4,0,
        67,73,1,0,0,0,68,69,10,2,0,0,69,70,5,10,0,0,70,72,3,6,3,3,71,68,
        1,0,0,0,72,75,1,0,0,0,73,71,1,0,0,0,73,74,1,0,0,0,74,7,1,0,0,0,75,
        73,1,0,0,0,76,77,6,4,-1,0,77,78,5,43,0,0,78,79,3,10,5,0,79,80,5,
        42,0,0,80,86,1,0,0,0,81,82,5,41,0,0,82,83,3,2,1,0,83,84,5,40,0,0,
        84,86,1,0,0,0,85,76,1,0,0,0,85,81,1,0,0,0,86,95,1,0,0,0,87,88,10,
        3,0,0,88,94,3,20,10,0,89,90,10,2,0,0,90,94,3,22,11,0,91,92,10,1,
        0,0,92,94,3,24,12,0,93,87,1,0,0,0,93,89,1,0,0,0,93,91,1,0,0,0,94,
        97,1,0,0,0,95,93,1,0,0,0,95,96,1,0,0,0,96,9,1,0,0,0,97,95,1,0,0,
        0,98,99,6,5,-1,0,99,100,3,12,6,0,100,106,1,0,0,0,101,102,10,2,0,
        0,102,103,5,11,0,0,103,105,3,10,5,3,104,101,1,0,0,0,105,108,1,0,
        0,0,106,104,1,0,0,0,106,107,1,0,0,0,107,11,1,0,0,0,108,106,1,0,0,
        0,109,110,6,6,-1,0,110,111,3,14,7,0,111,117,1,0,0,0,112,113,10,2,
        0,0,113,114,5,10,0,0,114,116,3,12,6,3,115,112,1,0,0,0,116,119,1,
        0,0,0,117,115,1,0,0,0,117,118,1,0,0,0,118,13,1,0,0,0,119,117,1,0,
        0,0,120,122,3,26,13,0,121,123,5,12,0,0,122,121,1,0,0,0,122,123,1,
        0,0,0,123,124,1,0,0,0,124,125,7,0,0,0,125,126,3,36,18,0,126,174,
        1,0,0,0,127,129,3,26,13,0,128,130,5,12,0,0,129,128,1,0,0,0,129,130,
        1,0,0,0,130,131,1,0,0,0,131,132,7,1,0,0,132,133,3,38,19,0,133,174,
        1,0,0,0,134,136,3,26,13,0,135,137,5,12,0,0,136,135,1,0,0,0,136,137,
        1,0,0,0,137,138,1,0,0,0,138,139,5,19,0,0,139,140,3,34,17,0,140,174,
        1,0,0,0,141,143,3,26,13,0,142,144,5,12,0,0,143,142,1,0,0,0,143,144,
        1,0,0,0,144,145,1,0,0,0,145,146,5,14,0,0,146,147,3,18,9,0,147,174,
        1,0,0,0,148,150,3,26,13,0,149,151,5,12,0,0,150,149,1,0,0,0,150,151,
        1,0,0,0,151,152,1,0,0,0,152,153,5,15,0,0,153,154,3,18,9,0,154,174,
        1,0,0,0,155,157,3,26,13,0,156,158,5,12,0,0,157,156,1,0,0,0,157,158,
        1,0,0,0,158,159,1,0,0,0,159,160,5,17,0,0,160,161,3,18,9,0,161,174,
        1,0,0,0,162,164,3,26,13,0,163,165,5,12,0,0,164,163,1,0,0,0,164,165,
        1,0,0,0,165,166,1,0,0,0,166,167,5,16,0,0,167,168,3,18,9,0,168,174,
        1,0,0,0,169,170,5,41,0,0,170,171,3,10,5,0,171,172,5,40,0,0,172,174,
        1,0,0,0,173,120,1,0,0,0,173,127,1,0,0,0,173,134,1,0,0,0,173,141,
        1,0,0,0,173,148,1,0,0,0,173,155,1,0,0,0,173,162,1,0,0,0,173,169,
        1,0,0,0,174,15,1,0,0,0,175,176,7,1,0,0,176,17,1,0,0,0,177,178,5,
        7,0,0,178,19,1,0,0,0,179,180,5,20,0,0,180,181,5,9,0,0,181,182,5,
        21,0,0,182,183,5,9,0,0,183,21,1,0,0,0,184,185,5,25,0,0,185,186,7,
        2,0,0,186,187,5,22,0,0,187,23,1,0,0,0,188,189,5,26,0,0,189,190,5,
        2,0,0,190,191,5,27,0,0,191,25,1,0,0,0,192,193,3,28,14,0,193,194,
        5,37,0,0,194,196,3,30,15,0,195,197,3,32,16,0,196,195,1,0,0,0,196,
        197,1,0,0,0,197,27,1,0,0,0,198,199,7,3,0,0,199,29,1,0,0,0,200,201,
        7,4,0,0,201,31,1,0,0,0,202,203,6,16,-1,0,203,204,5,38,0,0,204,209,
        7,4,0,0,205,206,5,43,0,0,206,207,7,5,0,0,207,209,5,42,0,0,208,202,
        1,0,0,0,208,205,1,0,0,0,209,214,1,0,0,0,210,211,10,3,0,0,211,213,
        3,32,16,4,212,210,1,0,0,0,213,216,1,0,0,0,214,212,1,0,0,0,214,215,
        1,0,0,0,215,33,1,0,0,0,216,214,1,0,0,0,217,218,5,41,0,0,218,231,
        5,40,0,0,219,220,5,41,0,0,220,225,3,36,18,0,221,222,5,39,0,0,222,
        224,3,36,18,0,223,221,1,0,0,0,224,227,1,0,0,0,225,223,1,0,0,0,225,
        226,1,0,0,0,226,228,1,0,0,0,227,225,1,0,0,0,228,229,5,40,0,0,229,
        231,1,0,0,0,230,217,1,0,0,0,230,219,1,0,0,0,231,35,1,0,0,0,232,235,
        3,38,19,0,233,235,5,8,0,0,234,232,1,0,0,0,234,233,1,0,0,0,235,37,
        1,0,0,0,236,245,5,2,0,0,237,245,5,1,0,0,238,245,5,4,0,0,239,245,
        5,3,0,0,240,245,3,18,9,0,241,245,5,6,0,0,242,245,5,5,0,0,243,245,
        5,9,0,0,244,236,1,0,0,0,244,237,1,0,0,0,244,238,1,0,0,0,244,239,
        1,0,0,0,244,240,1,0,0,0,244,241,1,0,0,0,244,242,1,0,0,0,244,243,
        1,0,0,0,245,39,1,0,0,0,23,51,62,73,85,93,95,106,117,122,129,136,
        143,150,157,164,173,196,208,214,225,230,234,244
    ]

class STIXPatternParser ( Parser ):

    grammarFileName = "STIXPattern.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'AND'", "'OR'", "'NOT'", 
                     "'FOLLOWEDBY'", "'LIKE'", "'MATCHES'", "'ISSUPERSET'", 
                     "'ISSUBSET'", "'LAST'", "'IN'", "'START'", "'STOP'", 
                     "'SECONDS'", "'true'", "'false'", "'WITHIN'", "'REPEATS'", 
                     "'TIMES'", "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'<'", "'<='", "'>'", "'>='", "'''", "':'", "'.'", 
                     "','", "')'", "'('", "']'", "'['", "'+'", "<INVALID>", 
                     "'-'", "'^'", "'/'", "'*'" ]

    symbolicNames = [ "<INVALID>", "IntNegLiteral", "IntPosLiteral", "FloatNegLiteral", 
                      "FloatPosLiteral", "HexLiteral", "BinaryLiteral", 
                      "StringLiteral", "BoolLiteral", "TimestampLiteral", 
                      "AND", "OR", "NOT", "FOLLOWEDBY", "LIKE", "MATCHES", 
                      "ISSUPERSET", "ISSUBSET", "LAST", "IN", "START", "STOP", 
                      "SECONDS", "TRUE", "FALSE", "WITHIN", "REPEATS", "TIMES", 
                      "IdentifierWithoutHyphen", "IdentifierWithHyphen", 
                      "EQ", "NEQ", "LT", "LE", "GT", "GE", "QUOTE", "COLON", 
                      "DOT", "COMMA", "RPAREN", "LPAREN", "RBRACK", "LBRACK", 
                      "PLUS", "HYPHEN", "MINUS", "POWER_OP", "DIVIDE", "ASTERISK", 
                      "WS", "COMMENT", "LINE_COMMENT", "InvalidCharacter" ]

    RULE_pattern = 0
    RULE_observationExpressions = 1
    RULE_observationExpressionOr = 2
    RULE_observationExpressionAnd = 3
    RULE_observationExpression = 4
    RULE_comparisonExpression = 5
    RULE_comparisonExpressionAnd = 6
    RULE_propTest = 7
    RULE_orderingComparator = 8
    RULE_stringLiteral = 9
    RULE_startStopQualifier = 10
    RULE_withinQualifier = 11
    RULE_repeatedQualifier = 12
    RULE_objectPath = 13
    RULE_objectType = 14
    RULE_firstPathComponent = 15
    RULE_objectPathComponent = 16
    RULE_setLiteral = 17
    RULE_primitiveLiteral = 18
    RULE_orderableLiteral = 19

    ruleNames =  [ "pattern", "observationExpressions", "observationExpressionOr", 
                   "observationExpressionAnd", "observationExpression", 
                   "comparisonExpression", "comparisonExpressionAnd", "propTest", 
                   "orderingComparator", "stringLiteral", "startStopQualifier", 
                   "withinQualifier", "repeatedQualifier", "objectPath", 
                   "objectType", "firstPathComponent", "objectPathComponent", 
                   "setLiteral", "primitiveLiteral", "orderableLiteral" ]

    EOF = Token.EOF
    IntNegLiteral=1
    IntPosLiteral=2
    FloatNegLiteral=3
    FloatPosLiteral=4
    HexLiteral=5
    BinaryLiteral=6
    StringLiteral=7
    BoolLiteral=8
    TimestampLiteral=9
    AND=10
    OR=11
    NOT=12
    FOLLOWEDBY=13
    LIKE=14
    MATCHES=15
    ISSUPERSET=16
    ISSUBSET=17
    LAST=18
    IN=19
    START=20
    STOP=21
    SECONDS=22
    TRUE=23
    FALSE=24
    WITHIN=25
    REPEATS=26
    TIMES=27
    IdentifierWithoutHyphen=28
    IdentifierWithHyphen=29
    EQ=30
    NEQ=31
    LT=32
    LE=33
    GT=34
    GE=35
    QUOTE=36
    COLON=37
    DOT=38
    COMMA=39
    RPAREN=40
    LPAREN=41
    RBRACK=42
    LBRACK=43
    PLUS=44
    HYPHEN=45
    MINUS=46
    POWER_OP=47
    DIVIDE=48
    ASTERISK=49
    WS=50
    COMMENT=51
    LINE_COMMENT=52
    InvalidCharacter=53

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class PatternContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def observationExpressions(self):
            return self.getTypedRuleContext(STIXPatternParser.ObservationExpressionsContext,0)


        def EOF(self):
            return self.getToken(STIXPatternParser.EOF, 0)

        def getRuleIndex(self):
            return STIXPatternParser.RULE_pattern

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPattern" ):
                listener.enterPattern(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPattern" ):
                listener.exitPattern(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPattern" ):
                return visitor.visitPattern(self)
            else:
                return visitor.visitChildren(self)




    def pattern(self):

        localctx = STIXPatternParser.PatternContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_pattern)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 40
            self.observationExpressions(0)
            self.state = 41
            self.match(STIXPatternParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ObservationExpressionsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def observationExpressionOr(self):
            return self.getTypedRuleContext(STIXPatternParser.ObservationExpressionOrContext,0)


        def observationExpressions(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(STIXPatternParser.ObservationExpressionsContext)
            else:
                return self.getTypedRuleContext(STIXPatternParser.ObservationExpressionsContext,i)


        def FOLLOWEDBY(self):
            return self.getToken(STIXPatternParser.FOLLOWEDBY, 0)

        def getRuleIndex(self):
            return STIXPatternParser.RULE_observationExpressions

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterObservationExpressions" ):
                listener.enterObservationExpressions(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitObservationExpressions" ):
                listener.exitObservationExpressions(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitObservationExpressions" ):
                return visitor.visitObservationExpressions(self)
            else:
                return visitor.visitChildren(self)



    def observationExpressions(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = STIXPatternParser.ObservationExpressionsContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_observationExpressions, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 44
            self.observationExpressionOr(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 51
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,0,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = STIXPatternParser.ObservationExpressionsContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_observationExpressions)
                    self.state = 46
                    if not self.precpred(self._ctx, 2):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                    self.state = 47
                    self.match(STIXPatternParser.FOLLOWEDBY)
                    self.state = 48
                    self.observationExpressions(3) 
                self.state = 53
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,0,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ObservationExpressionOrContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def observationExpressionAnd(self):
            return self.getTypedRuleContext(STIXPatternParser.ObservationExpressionAndContext,0)


        def observationExpressionOr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(STIXPatternParser.ObservationExpressionOrContext)
            else:
                return self.getTypedRuleContext(STIXPatternParser.ObservationExpressionOrContext,i)


        def OR(self):
            return self.getToken(STIXPatternParser.OR, 0)

        def getRuleIndex(self):
            return STIXPatternParser.RULE_observationExpressionOr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterObservationExpressionOr" ):
                listener.enterObservationExpressionOr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitObservationExpressionOr" ):
                listener.exitObservationExpressionOr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitObservationExpressionOr" ):
                return visitor.visitObservationExpressionOr(self)
            else:
                return visitor.visitChildren(self)



    def observationExpressionOr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = STIXPatternParser.ObservationExpressionOrContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 4
        self.enterRecursionRule(localctx, 4, self.RULE_observationExpressionOr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 55
            self.observationExpressionAnd(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 62
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,1,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = STIXPatternParser.ObservationExpressionOrContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_observationExpressionOr)
                    self.state = 57
                    if not self.precpred(self._ctx, 2):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                    self.state = 58
                    self.match(STIXPatternParser.OR)
                    self.state = 59
                    self.observationExpressionOr(3) 
                self.state = 64
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,1,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ObservationExpressionAndContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def observationExpression(self):
            return self.getTypedRuleContext(STIXPatternParser.ObservationExpressionContext,0)


        def observationExpressionAnd(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(STIXPatternParser.ObservationExpressionAndContext)
            else:
                return self.getTypedRuleContext(STIXPatternParser.ObservationExpressionAndContext,i)


        def AND(self):
            return self.getToken(STIXPatternParser.AND, 0)

        def getRuleIndex(self):
            return STIXPatternParser.RULE_observationExpressionAnd

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterObservationExpressionAnd" ):
                listener.enterObservationExpressionAnd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitObservationExpressionAnd" ):
                listener.exitObservationExpressionAnd(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitObservationExpressionAnd" ):
                return visitor.visitObservationExpressionAnd(self)
            else:
                return visitor.visitChildren(self)



    def observationExpressionAnd(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = STIXPatternParser.ObservationExpressionAndContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 6
        self.enterRecursionRule(localctx, 6, self.RULE_observationExpressionAnd, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 66
            self.observationExpression(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 73
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = STIXPatternParser.ObservationExpressionAndContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_observationExpressionAnd)
                    self.state = 68
                    if not self.precpred(self._ctx, 2):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                    self.state = 69
                    self.match(STIXPatternParser.AND)
                    self.state = 70
                    self.observationExpressionAnd(3) 
                self.state = 75
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ObservationExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return STIXPatternParser.RULE_observationExpression

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class ObservationExpressionRepeatedContext(ObservationExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a STIXPatternParser.ObservationExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def observationExpression(self):
            return self.getTypedRuleContext(STIXPatternParser.ObservationExpressionContext,0)

        def repeatedQualifier(self):
            return self.getTypedRuleContext(STIXPatternParser.RepeatedQualifierContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterObservationExpressionRepeated" ):
                listener.enterObservationExpressionRepeated(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitObservationExpressionRepeated" ):
                listener.exitObservationExpressionRepeated(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitObservationExpressionRepeated" ):
                return visitor.visitObservationExpressionRepeated(self)
            else:
                return visitor.visitChildren(self)


    class ObservationExpressionSimpleContext(ObservationExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a STIXPatternParser.ObservationExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LBRACK(self):
            return self.getToken(STIXPatternParser.LBRACK, 0)
        def comparisonExpression(self):
            return self.getTypedRuleContext(STIXPatternParser.ComparisonExpressionContext,0)

        def RBRACK(self):
            return self.getToken(STIXPatternParser.RBRACK, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterObservationExpressionSimple" ):
                listener.enterObservationExpressionSimple(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitObservationExpressionSimple" ):
                listener.exitObservationExpressionSimple(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitObservationExpressionSimple" ):
                return visitor.visitObservationExpressionSimple(self)
            else:
                return visitor.visitChildren(self)


    class ObservationExpressionCompoundContext(ObservationExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a STIXPatternParser.ObservationExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(STIXPatternParser.LPAREN, 0)
        def observationExpressions(self):
            return self.getTypedRuleContext(STIXPatternParser.ObservationExpressionsContext,0)

        def RPAREN(self):
            return self.getToken(STIXPatternParser.RPAREN, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterObservationExpressionCompound" ):
                listener.enterObservationExpressionCompound(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitObservationExpressionCompound" ):
                listener.exitObservationExpressionCompound(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitObservationExpressionCompound" ):
                return visitor.visitObservationExpressionCompound(self)
            else:
                return visitor.visitChildren(self)


    class ObservationExpressionWithinContext(ObservationExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a STIXPatternParser.ObservationExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def observationExpression(self):
            return self.getTypedRuleContext(STIXPatternParser.ObservationExpressionContext,0)

        def withinQualifier(self):
            return self.getTypedRuleContext(STIXPatternParser.WithinQualifierContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterObservationExpressionWithin" ):
                listener.enterObservationExpressionWithin(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitObservationExpressionWithin" ):
                listener.exitObservationExpressionWithin(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitObservationExpressionWithin" ):
                return visitor.visitObservationExpressionWithin(self)
            else:
                return visitor.visitChildren(self)


    class ObservationExpressionStartStopContext(ObservationExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a STIXPatternParser.ObservationExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def observationExpression(self):
            return self.getTypedRuleContext(STIXPatternParser.ObservationExpressionContext,0)

        def startStopQualifier(self):
            return self.getTypedRuleContext(STIXPatternParser.StartStopQualifierContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterObservationExpressionStartStop" ):
                listener.enterObservationExpressionStartStop(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitObservationExpressionStartStop" ):
                listener.exitObservationExpressionStartStop(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitObservationExpressionStartStop" ):
                return visitor.visitObservationExpressionStartStop(self)
            else:
                return visitor.visitChildren(self)



    def observationExpression(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = STIXPatternParser.ObservationExpressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 8
        self.enterRecursionRule(localctx, 8, self.RULE_observationExpression, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 85
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [43]:
                localctx = STIXPatternParser.ObservationExpressionSimpleContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 77
                self.match(STIXPatternParser.LBRACK)
                self.state = 78
                self.comparisonExpression(0)
                self.state = 79
                self.match(STIXPatternParser.RBRACK)
                pass
            elif token in [41]:
                localctx = STIXPatternParser.ObservationExpressionCompoundContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 81
                self.match(STIXPatternParser.LPAREN)
                self.state = 82
                self.observationExpressions(0)
                self.state = 83
                self.match(STIXPatternParser.RPAREN)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 95
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 93
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
                    if la_ == 1:
                        localctx = STIXPatternParser.ObservationExpressionStartStopContext(self, STIXPatternParser.ObservationExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_observationExpression)
                        self.state = 87
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 88
                        self.startStopQualifier()
                        pass

                    elif la_ == 2:
                        localctx = STIXPatternParser.ObservationExpressionWithinContext(self, STIXPatternParser.ObservationExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_observationExpression)
                        self.state = 89
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 90
                        self.withinQualifier()
                        pass

                    elif la_ == 3:
                        localctx = STIXPatternParser.ObservationExpressionRepeatedContext(self, STIXPatternParser.ObservationExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_observationExpression)
                        self.state = 91
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 92
                        self.repeatedQualifier()
                        pass

             
                self.state = 97
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ComparisonExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return STIXPatternParser.RULE_comparisonExpression

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class ComparisonExpressionAnd_Context(ComparisonExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a STIXPatternParser.ComparisonExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def comparisonExpressionAnd(self):
            return self.getTypedRuleContext(STIXPatternParser.ComparisonExpressionAndContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparisonExpressionAnd_" ):
                listener.enterComparisonExpressionAnd_(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparisonExpressionAnd_" ):
                listener.exitComparisonExpressionAnd_(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparisonExpressionAnd_" ):
                return visitor.visitComparisonExpressionAnd_(self)
            else:
                return visitor.visitChildren(self)


    class ComparisonExpressionOredContext(ComparisonExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a STIXPatternParser.ComparisonExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def comparisonExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(STIXPatternParser.ComparisonExpressionContext)
            else:
                return self.getTypedRuleContext(STIXPatternParser.ComparisonExpressionContext,i)

        def OR(self):
            return self.getToken(STIXPatternParser.OR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparisonExpressionOred" ):
                listener.enterComparisonExpressionOred(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparisonExpressionOred" ):
                listener.exitComparisonExpressionOred(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparisonExpressionOred" ):
                return visitor.visitComparisonExpressionOred(self)
            else:
                return visitor.visitChildren(self)



    def comparisonExpression(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = STIXPatternParser.ComparisonExpressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 10
        self.enterRecursionRule(localctx, 10, self.RULE_comparisonExpression, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            localctx = STIXPatternParser.ComparisonExpressionAnd_Context(self, localctx)
            self._ctx = localctx
            _prevctx = localctx

            self.state = 99
            self.comparisonExpressionAnd(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 106
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,6,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = STIXPatternParser.ComparisonExpressionOredContext(self, STIXPatternParser.ComparisonExpressionContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_comparisonExpression)
                    self.state = 101
                    if not self.precpred(self._ctx, 2):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                    self.state = 102
                    self.match(STIXPatternParser.OR)
                    self.state = 103
                    self.comparisonExpression(3) 
                self.state = 108
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,6,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ComparisonExpressionAndContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return STIXPatternParser.RULE_comparisonExpressionAnd

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class ComparisonExpressionAndPropTestContext(ComparisonExpressionAndContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a STIXPatternParser.ComparisonExpressionAndContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def propTest(self):
            return self.getTypedRuleContext(STIXPatternParser.PropTestContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparisonExpressionAndPropTest" ):
                listener.enterComparisonExpressionAndPropTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparisonExpressionAndPropTest" ):
                listener.exitComparisonExpressionAndPropTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparisonExpressionAndPropTest" ):
                return visitor.visitComparisonExpressionAndPropTest(self)
            else:
                return visitor.visitChildren(self)


    class ComparisonExpressionAndedContext(ComparisonExpressionAndContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a STIXPatternParser.ComparisonExpressionAndContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def comparisonExpressionAnd(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(STIXPatternParser.ComparisonExpressionAndContext)
            else:
                return self.getTypedRuleContext(STIXPatternParser.ComparisonExpressionAndContext,i)

        def AND(self):
            return self.getToken(STIXPatternParser.AND, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparisonExpressionAnded" ):
                listener.enterComparisonExpressionAnded(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparisonExpressionAnded" ):
                listener.exitComparisonExpressionAnded(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparisonExpressionAnded" ):
                return visitor.visitComparisonExpressionAnded(self)
            else:
                return visitor.visitChildren(self)



    def comparisonExpressionAnd(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = STIXPatternParser.ComparisonExpressionAndContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 12
        self.enterRecursionRule(localctx, 12, self.RULE_comparisonExpressionAnd, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            localctx = STIXPatternParser.ComparisonExpressionAndPropTestContext(self, localctx)
            self._ctx = localctx
            _prevctx = localctx

            self.state = 110
            self.propTest()
            self._ctx.stop = self._input.LT(-1)
            self.state = 117
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,7,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = STIXPatternParser.ComparisonExpressionAndedContext(self, STIXPatternParser.ComparisonExpressionAndContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_comparisonExpressionAnd)
                    self.state = 112
                    if not self.precpred(self._ctx, 2):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                    self.state = 113
                    self.match(STIXPatternParser.AND)
                    self.state = 114
                    self.comparisonExpressionAnd(3) 
                self.state = 119
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,7,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class PropTestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return STIXPatternParser.RULE_propTest

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class PropTestRegexContext(PropTestContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a STIXPatternParser.PropTestContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def objectPath(self):
            return self.getTypedRuleContext(STIXPatternParser.ObjectPathContext,0)

        def MATCHES(self):
            return self.getToken(STIXPatternParser.MATCHES, 0)
        def stringLiteral(self):
            return self.getTypedRuleContext(STIXPatternParser.StringLiteralContext,0)

        def NOT(self):
            return self.getToken(STIXPatternParser.NOT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPropTestRegex" ):
                listener.enterPropTestRegex(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPropTestRegex" ):
                listener.exitPropTestRegex(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPropTestRegex" ):
                return visitor.visitPropTestRegex(self)
            else:
                return visitor.visitChildren(self)


    class PropTestOrderContext(PropTestContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a STIXPatternParser.PropTestContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def objectPath(self):
            return self.getTypedRuleContext(STIXPatternParser.ObjectPathContext,0)

        def orderableLiteral(self):
            return self.getTypedRuleContext(STIXPatternParser.OrderableLiteralContext,0)

        def GT(self):
            return self.getToken(STIXPatternParser.GT, 0)
        def LT(self):
            return self.getToken(STIXPatternParser.LT, 0)
        def GE(self):
            return self.getToken(STIXPatternParser.GE, 0)
        def LE(self):
            return self.getToken(STIXPatternParser.LE, 0)
        def NOT(self):
            return self.getToken(STIXPatternParser.NOT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPropTestOrder" ):
                listener.enterPropTestOrder(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPropTestOrder" ):
                listener.exitPropTestOrder(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPropTestOrder" ):
                return visitor.visitPropTestOrder(self)
            else:
                return visitor.visitChildren(self)


    class PropTestLikeContext(PropTestContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a STIXPatternParser.PropTestContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def objectPath(self):
            return self.getTypedRuleContext(STIXPatternParser.ObjectPathContext,0)

        def LIKE(self):
            return self.getToken(STIXPatternParser.LIKE, 0)
        def stringLiteral(self):
            return self.getTypedRuleContext(STIXPatternParser.StringLiteralContext,0)

        def NOT(self):
            return self.getToken(STIXPatternParser.NOT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPropTestLike" ):
                listener.enterPropTestLike(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPropTestLike" ):
                listener.exitPropTestLike(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPropTestLike" ):
                return visitor.visitPropTestLike(self)
            else:
                return visitor.visitChildren(self)


    class PropTestEqualContext(PropTestContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a STIXPatternParser.PropTestContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def objectPath(self):
            return self.getTypedRuleContext(STIXPatternParser.ObjectPathContext,0)

        def primitiveLiteral(self):
            return self.getTypedRuleContext(STIXPatternParser.PrimitiveLiteralContext,0)

        def EQ(self):
            return self.getToken(STIXPatternParser.EQ, 0)
        def NEQ(self):
            return self.getToken(STIXPatternParser.NEQ, 0)
        def NOT(self):
            return self.getToken(STIXPatternParser.NOT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPropTestEqual" ):
                listener.enterPropTestEqual(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPropTestEqual" ):
                listener.exitPropTestEqual(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPropTestEqual" ):
                return visitor.visitPropTestEqual(self)
            else:
                return visitor.visitChildren(self)


    class PropTestSetContext(PropTestContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a STIXPatternParser.PropTestContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def objectPath(self):
            return self.getTypedRuleContext(STIXPatternParser.ObjectPathContext,0)

        def IN(self):
            return self.getToken(STIXPatternParser.IN, 0)
        def setLiteral(self):
            return self.getTypedRuleContext(STIXPatternParser.SetLiteralContext,0)

        def NOT(self):
            return self.getToken(STIXPatternParser.NOT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPropTestSet" ):
                listener.enterPropTestSet(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPropTestSet" ):
                listener.exitPropTestSet(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPropTestSet" ):
                return visitor.visitPropTestSet(self)
            else:
                return visitor.visitChildren(self)


    class PropTestIsSubsetContext(PropTestContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a STIXPatternParser.PropTestContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def objectPath(self):
            return self.getTypedRuleContext(STIXPatternParser.ObjectPathContext,0)

        def ISSUBSET(self):
            return self.getToken(STIXPatternParser.ISSUBSET, 0)
        def stringLiteral(self):
            return self.getTypedRuleContext(STIXPatternParser.StringLiteralContext,0)

        def NOT(self):
            return self.getToken(STIXPatternParser.NOT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPropTestIsSubset" ):
                listener.enterPropTestIsSubset(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPropTestIsSubset" ):
                listener.exitPropTestIsSubset(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPropTestIsSubset" ):
                return visitor.visitPropTestIsSubset(self)
            else:
                return visitor.visitChildren(self)


    class PropTestParenContext(PropTestContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a STIXPatternParser.PropTestContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(STIXPatternParser.LPAREN, 0)
        def comparisonExpression(self):
            return self.getTypedRuleContext(STIXPatternParser.ComparisonExpressionContext,0)

        def RPAREN(self):
            return self.getToken(STIXPatternParser.RPAREN, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPropTestParen" ):
                listener.enterPropTestParen(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPropTestParen" ):
                listener.exitPropTestParen(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPropTestParen" ):
                return visitor.visitPropTestParen(self)
            else:
                return visitor.visitChildren(self)


    class PropTestIsSupersetContext(PropTestContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a STIXPatternParser.PropTestContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def objectPath(self):
            return self.getTypedRuleContext(STIXPatternParser.ObjectPathContext,0)

        def ISSUPERSET(self):
            return self.getToken(STIXPatternParser.ISSUPERSET, 0)
        def stringLiteral(self):
            return self.getTypedRuleContext(STIXPatternParser.StringLiteralContext,0)

        def NOT(self):
            return self.getToken(STIXPatternParser.NOT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPropTestIsSuperset" ):
                listener.enterPropTestIsSuperset(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPropTestIsSuperset" ):
                listener.exitPropTestIsSuperset(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPropTestIsSuperset" ):
                return visitor.visitPropTestIsSuperset(self)
            else:
                return visitor.visitChildren(self)



    def propTest(self):

        localctx = STIXPatternParser.PropTestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_propTest)
        self._la = 0 # Token type
        try:
            self.state = 173
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,15,self._ctx)
            if la_ == 1:
                localctx = STIXPatternParser.PropTestEqualContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 120
                self.objectPath()
                self.state = 122
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==12:
                    self.state = 121
                    self.match(STIXPatternParser.NOT)


                self.state = 124
                _la = self._input.LA(1)
                if not(_la==30 or _la==31):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 125
                self.primitiveLiteral()
                pass

            elif la_ == 2:
                localctx = STIXPatternParser.PropTestOrderContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 127
                self.objectPath()
                self.state = 129
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==12:
                    self.state = 128
                    self.match(STIXPatternParser.NOT)


                self.state = 131
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 64424509440) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 132
                self.orderableLiteral()
                pass

            elif la_ == 3:
                localctx = STIXPatternParser.PropTestSetContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 134
                self.objectPath()
                self.state = 136
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==12:
                    self.state = 135
                    self.match(STIXPatternParser.NOT)


                self.state = 138
                self.match(STIXPatternParser.IN)
                self.state = 139
                self.setLiteral()
                pass

            elif la_ == 4:
                localctx = STIXPatternParser.PropTestLikeContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 141
                self.objectPath()
                self.state = 143
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==12:
                    self.state = 142
                    self.match(STIXPatternParser.NOT)


                self.state = 145
                self.match(STIXPatternParser.LIKE)
                self.state = 146
                self.stringLiteral()
                pass

            elif la_ == 5:
                localctx = STIXPatternParser.PropTestRegexContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 148
                self.objectPath()
                self.state = 150
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==12:
                    self.state = 149
                    self.match(STIXPatternParser.NOT)


                self.state = 152
                self.match(STIXPatternParser.MATCHES)
                self.state = 153
                self.stringLiteral()
                pass

            elif la_ == 6:
                localctx = STIXPatternParser.PropTestIsSubsetContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 155
                self.objectPath()
                self.state = 157
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==12:
                    self.state = 156
                    self.match(STIXPatternParser.NOT)


                self.state = 159
                self.match(STIXPatternParser.ISSUBSET)
                self.state = 160
                self.stringLiteral()
                pass

            elif la_ == 7:
                localctx = STIXPatternParser.PropTestIsSupersetContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 162
                self.objectPath()
                self.state = 164
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==12:
                    self.state = 163
                    self.match(STIXPatternParser.NOT)


                self.state = 166
                self.match(STIXPatternParser.ISSUPERSET)
                self.state = 167
                self.stringLiteral()
                pass

            elif la_ == 8:
                localctx = STIXPatternParser.PropTestParenContext(self, localctx)
                self.enterOuterAlt(localctx, 8)
                self.state = 169
                self.match(STIXPatternParser.LPAREN)
                self.state = 170
                self.comparisonExpression(0)
                self.state = 171
                self.match(STIXPatternParser.RPAREN)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OrderingComparatorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def GT(self):
            return self.getToken(STIXPatternParser.GT, 0)

        def LT(self):
            return self.getToken(STIXPatternParser.LT, 0)

        def GE(self):
            return self.getToken(STIXPatternParser.GE, 0)

        def LE(self):
            return self.getToken(STIXPatternParser.LE, 0)

        def getRuleIndex(self):
            return STIXPatternParser.RULE_orderingComparator

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrderingComparator" ):
                listener.enterOrderingComparator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrderingComparator" ):
                listener.exitOrderingComparator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrderingComparator" ):
                return visitor.visitOrderingComparator(self)
            else:
                return visitor.visitChildren(self)




    def orderingComparator(self):

        localctx = STIXPatternParser.OrderingComparatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_orderingComparator)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 175
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 64424509440) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StringLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def StringLiteral(self):
            return self.getToken(STIXPatternParser.StringLiteral, 0)

        def getRuleIndex(self):
            return STIXPatternParser.RULE_stringLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStringLiteral" ):
                listener.enterStringLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStringLiteral" ):
                listener.exitStringLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStringLiteral" ):
                return visitor.visitStringLiteral(self)
            else:
                return visitor.visitChildren(self)




    def stringLiteral(self):

        localctx = STIXPatternParser.StringLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_stringLiteral)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 177
            self.match(STIXPatternParser.StringLiteral)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StartStopQualifierContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def START(self):
            return self.getToken(STIXPatternParser.START, 0)

        def TimestampLiteral(self, i:int=None):
            if i is None:
                return self.getTokens(STIXPatternParser.TimestampLiteral)
            else:
                return self.getToken(STIXPatternParser.TimestampLiteral, i)

        def STOP(self):
            return self.getToken(STIXPatternParser.STOP, 0)

        def getRuleIndex(self):
            return STIXPatternParser.RULE_startStopQualifier

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStartStopQualifier" ):
                listener.enterStartStopQualifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStartStopQualifier" ):
                listener.exitStartStopQualifier(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStartStopQualifier" ):
                return visitor.visitStartStopQualifier(self)
            else:
                return visitor.visitChildren(self)




    def startStopQualifier(self):

        localctx = STIXPatternParser.StartStopQualifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_startStopQualifier)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 179
            self.match(STIXPatternParser.START)
            self.state = 180
            self.match(STIXPatternParser.TimestampLiteral)
            self.state = 181
            self.match(STIXPatternParser.STOP)
            self.state = 182
            self.match(STIXPatternParser.TimestampLiteral)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WithinQualifierContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WITHIN(self):
            return self.getToken(STIXPatternParser.WITHIN, 0)

        def SECONDS(self):
            return self.getToken(STIXPatternParser.SECONDS, 0)

        def IntPosLiteral(self):
            return self.getToken(STIXPatternParser.IntPosLiteral, 0)

        def FloatPosLiteral(self):
            return self.getToken(STIXPatternParser.FloatPosLiteral, 0)

        def getRuleIndex(self):
            return STIXPatternParser.RULE_withinQualifier

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWithinQualifier" ):
                listener.enterWithinQualifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWithinQualifier" ):
                listener.exitWithinQualifier(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWithinQualifier" ):
                return visitor.visitWithinQualifier(self)
            else:
                return visitor.visitChildren(self)




    def withinQualifier(self):

        localctx = STIXPatternParser.WithinQualifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_withinQualifier)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 184
            self.match(STIXPatternParser.WITHIN)
            self.state = 185
            _la = self._input.LA(1)
            if not(_la==2 or _la==4):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 186
            self.match(STIXPatternParser.SECONDS)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RepeatedQualifierContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def REPEATS(self):
            return self.getToken(STIXPatternParser.REPEATS, 0)

        def IntPosLiteral(self):
            return self.getToken(STIXPatternParser.IntPosLiteral, 0)

        def TIMES(self):
            return self.getToken(STIXPatternParser.TIMES, 0)

        def getRuleIndex(self):
            return STIXPatternParser.RULE_repeatedQualifier

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRepeatedQualifier" ):
                listener.enterRepeatedQualifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRepeatedQualifier" ):
                listener.exitRepeatedQualifier(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRepeatedQualifier" ):
                return visitor.visitRepeatedQualifier(self)
            else:
                return visitor.visitChildren(self)




    def repeatedQualifier(self):

        localctx = STIXPatternParser.RepeatedQualifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_repeatedQualifier)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 188
            self.match(STIXPatternParser.REPEATS)
            self.state = 189
            self.match(STIXPatternParser.IntPosLiteral)
            self.state = 190
            self.match(STIXPatternParser.TIMES)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ObjectPathContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def objectType(self):
            return self.getTypedRuleContext(STIXPatternParser.ObjectTypeContext,0)


        def COLON(self):
            return self.getToken(STIXPatternParser.COLON, 0)

        def firstPathComponent(self):
            return self.getTypedRuleContext(STIXPatternParser.FirstPathComponentContext,0)


        def objectPathComponent(self):
            return self.getTypedRuleContext(STIXPatternParser.ObjectPathComponentContext,0)


        def getRuleIndex(self):
            return STIXPatternParser.RULE_objectPath

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterObjectPath" ):
                listener.enterObjectPath(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitObjectPath" ):
                listener.exitObjectPath(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitObjectPath" ):
                return visitor.visitObjectPath(self)
            else:
                return visitor.visitChildren(self)




    def objectPath(self):

        localctx = STIXPatternParser.ObjectPathContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_objectPath)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 192
            self.objectType()
            self.state = 193
            self.match(STIXPatternParser.COLON)
            self.state = 194
            self.firstPathComponent()
            self.state = 196
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==38 or _la==43:
                self.state = 195
                self.objectPathComponent(0)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ObjectTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IdentifierWithoutHyphen(self):
            return self.getToken(STIXPatternParser.IdentifierWithoutHyphen, 0)

        def IdentifierWithHyphen(self):
            return self.getToken(STIXPatternParser.IdentifierWithHyphen, 0)

        def getRuleIndex(self):
            return STIXPatternParser.RULE_objectType

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterObjectType" ):
                listener.enterObjectType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitObjectType" ):
                listener.exitObjectType(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitObjectType" ):
                return visitor.visitObjectType(self)
            else:
                return visitor.visitChildren(self)




    def objectType(self):

        localctx = STIXPatternParser.ObjectTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_objectType)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 198
            _la = self._input.LA(1)
            if not(_la==28 or _la==29):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FirstPathComponentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IdentifierWithoutHyphen(self):
            return self.getToken(STIXPatternParser.IdentifierWithoutHyphen, 0)

        def StringLiteral(self):
            return self.getToken(STIXPatternParser.StringLiteral, 0)

        def getRuleIndex(self):
            return STIXPatternParser.RULE_firstPathComponent

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFirstPathComponent" ):
                listener.enterFirstPathComponent(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFirstPathComponent" ):
                listener.exitFirstPathComponent(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFirstPathComponent" ):
                return visitor.visitFirstPathComponent(self)
            else:
                return visitor.visitChildren(self)




    def firstPathComponent(self):

        localctx = STIXPatternParser.FirstPathComponentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_firstPathComponent)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 200
            _la = self._input.LA(1)
            if not(_la==7 or _la==28):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ObjectPathComponentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return STIXPatternParser.RULE_objectPathComponent

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class IndexPathStepContext(ObjectPathComponentContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a STIXPatternParser.ObjectPathComponentContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LBRACK(self):
            return self.getToken(STIXPatternParser.LBRACK, 0)
        def RBRACK(self):
            return self.getToken(STIXPatternParser.RBRACK, 0)
        def IntPosLiteral(self):
            return self.getToken(STIXPatternParser.IntPosLiteral, 0)
        def IntNegLiteral(self):
            return self.getToken(STIXPatternParser.IntNegLiteral, 0)
        def ASTERISK(self):
            return self.getToken(STIXPatternParser.ASTERISK, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIndexPathStep" ):
                listener.enterIndexPathStep(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIndexPathStep" ):
                listener.exitIndexPathStep(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIndexPathStep" ):
                return visitor.visitIndexPathStep(self)
            else:
                return visitor.visitChildren(self)


    class PathStepContext(ObjectPathComponentContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a STIXPatternParser.ObjectPathComponentContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def objectPathComponent(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(STIXPatternParser.ObjectPathComponentContext)
            else:
                return self.getTypedRuleContext(STIXPatternParser.ObjectPathComponentContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPathStep" ):
                listener.enterPathStep(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPathStep" ):
                listener.exitPathStep(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPathStep" ):
                return visitor.visitPathStep(self)
            else:
                return visitor.visitChildren(self)


    class KeyPathStepContext(ObjectPathComponentContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a STIXPatternParser.ObjectPathComponentContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def DOT(self):
            return self.getToken(STIXPatternParser.DOT, 0)
        def IdentifierWithoutHyphen(self):
            return self.getToken(STIXPatternParser.IdentifierWithoutHyphen, 0)
        def StringLiteral(self):
            return self.getToken(STIXPatternParser.StringLiteral, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterKeyPathStep" ):
                listener.enterKeyPathStep(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitKeyPathStep" ):
                listener.exitKeyPathStep(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitKeyPathStep" ):
                return visitor.visitKeyPathStep(self)
            else:
                return visitor.visitChildren(self)



    def objectPathComponent(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = STIXPatternParser.ObjectPathComponentContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 32
        self.enterRecursionRule(localctx, 32, self.RULE_objectPathComponent, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 208
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [38]:
                localctx = STIXPatternParser.KeyPathStepContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 203
                self.match(STIXPatternParser.DOT)
                self.state = 204
                _la = self._input.LA(1)
                if not(_la==7 or _la==28):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass
            elif token in [43]:
                localctx = STIXPatternParser.IndexPathStepContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 205
                self.match(STIXPatternParser.LBRACK)
                self.state = 206
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 562949953421318) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 207
                self.match(STIXPatternParser.RBRACK)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 214
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,18,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = STIXPatternParser.PathStepContext(self, STIXPatternParser.ObjectPathComponentContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_objectPathComponent)
                    self.state = 210
                    if not self.precpred(self._ctx, 3):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                    self.state = 211
                    self.objectPathComponent(4) 
                self.state = 216
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,18,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class SetLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(STIXPatternParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(STIXPatternParser.RPAREN, 0)

        def primitiveLiteral(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(STIXPatternParser.PrimitiveLiteralContext)
            else:
                return self.getTypedRuleContext(STIXPatternParser.PrimitiveLiteralContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(STIXPatternParser.COMMA)
            else:
                return self.getToken(STIXPatternParser.COMMA, i)

        def getRuleIndex(self):
            return STIXPatternParser.RULE_setLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSetLiteral" ):
                listener.enterSetLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSetLiteral" ):
                listener.exitSetLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSetLiteral" ):
                return visitor.visitSetLiteral(self)
            else:
                return visitor.visitChildren(self)




    def setLiteral(self):

        localctx = STIXPatternParser.SetLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_setLiteral)
        self._la = 0 # Token type
        try:
            self.state = 230
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,20,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 217
                self.match(STIXPatternParser.LPAREN)
                self.state = 218
                self.match(STIXPatternParser.RPAREN)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 219
                self.match(STIXPatternParser.LPAREN)
                self.state = 220
                self.primitiveLiteral()
                self.state = 225
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==39:
                    self.state = 221
                    self.match(STIXPatternParser.COMMA)
                    self.state = 222
                    self.primitiveLiteral()
                    self.state = 227
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 228
                self.match(STIXPatternParser.RPAREN)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrimitiveLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def orderableLiteral(self):
            return self.getTypedRuleContext(STIXPatternParser.OrderableLiteralContext,0)


        def BoolLiteral(self):
            return self.getToken(STIXPatternParser.BoolLiteral, 0)

        def getRuleIndex(self):
            return STIXPatternParser.RULE_primitiveLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrimitiveLiteral" ):
                listener.enterPrimitiveLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrimitiveLiteral" ):
                listener.exitPrimitiveLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrimitiveLiteral" ):
                return visitor.visitPrimitiveLiteral(self)
            else:
                return visitor.visitChildren(self)




    def primitiveLiteral(self):

        localctx = STIXPatternParser.PrimitiveLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_primitiveLiteral)
        try:
            self.state = 234
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 2, 3, 4, 5, 6, 7, 9]:
                self.enterOuterAlt(localctx, 1)
                self.state = 232
                self.orderableLiteral()
                pass
            elif token in [8]:
                self.enterOuterAlt(localctx, 2)
                self.state = 233
                self.match(STIXPatternParser.BoolLiteral)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OrderableLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IntPosLiteral(self):
            return self.getToken(STIXPatternParser.IntPosLiteral, 0)

        def IntNegLiteral(self):
            return self.getToken(STIXPatternParser.IntNegLiteral, 0)

        def FloatPosLiteral(self):
            return self.getToken(STIXPatternParser.FloatPosLiteral, 0)

        def FloatNegLiteral(self):
            return self.getToken(STIXPatternParser.FloatNegLiteral, 0)

        def stringLiteral(self):
            return self.getTypedRuleContext(STIXPatternParser.StringLiteralContext,0)


        def BinaryLiteral(self):
            return self.getToken(STIXPatternParser.BinaryLiteral, 0)

        def HexLiteral(self):
            return self.getToken(STIXPatternParser.HexLiteral, 0)

        def TimestampLiteral(self):
            return self.getToken(STIXPatternParser.TimestampLiteral, 0)

        def getRuleIndex(self):
            return STIXPatternParser.RULE_orderableLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrderableLiteral" ):
                listener.enterOrderableLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrderableLiteral" ):
                listener.exitOrderableLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrderableLiteral" ):
                return visitor.visitOrderableLiteral(self)
            else:
                return visitor.visitChildren(self)




    def orderableLiteral(self):

        localctx = STIXPatternParser.OrderableLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_orderableLiteral)
        try:
            self.state = 244
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [2]:
                self.enterOuterAlt(localctx, 1)
                self.state = 236
                self.match(STIXPatternParser.IntPosLiteral)
                pass
            elif token in [1]:
                self.enterOuterAlt(localctx, 2)
                self.state = 237
                self.match(STIXPatternParser.IntNegLiteral)
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 3)
                self.state = 238
                self.match(STIXPatternParser.FloatPosLiteral)
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 4)
                self.state = 239
                self.match(STIXPatternParser.FloatNegLiteral)
                pass
            elif token in [7]:
                self.enterOuterAlt(localctx, 5)
                self.state = 240
                self.stringLiteral()
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 6)
                self.state = 241
                self.match(STIXPatternParser.BinaryLiteral)
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 7)
                self.state = 242
                self.match(STIXPatternParser.HexLiteral)
                pass
            elif token in [9]:
                self.enterOuterAlt(localctx, 8)
                self.state = 243
                self.match(STIXPatternParser.TimestampLiteral)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[1] = self.observationExpressions_sempred
        self._predicates[2] = self.observationExpressionOr_sempred
        self._predicates[3] = self.observationExpressionAnd_sempred
        self._predicates[4] = self.observationExpression_sempred
        self._predicates[5] = self.comparisonExpression_sempred
        self._predicates[6] = self.comparisonExpressionAnd_sempred
        self._predicates[16] = self.objectPathComponent_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def observationExpressions_sempred(self, localctx:ObservationExpressionsContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 2)
         

    def observationExpressionOr_sempred(self, localctx:ObservationExpressionOrContext, predIndex:int):
            if predIndex == 1:
                return self.precpred(self._ctx, 2)
         

    def observationExpressionAnd_sempred(self, localctx:ObservationExpressionAndContext, predIndex:int):
            if predIndex == 2:
                return self.precpred(self._ctx, 2)
         

    def observationExpression_sempred(self, localctx:ObservationExpressionContext, predIndex:int):
            if predIndex == 3:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 1)
         

    def comparisonExpression_sempred(self, localctx:ComparisonExpressionContext, predIndex:int):
            if predIndex == 6:
                return self.precpred(self._ctx, 2)
         

    def comparisonExpressionAnd_sempred(self, localctx:ComparisonExpressionAndContext, predIndex:int):
            if predIndex == 7:
                return self.precpred(self._ctx, 2)
         

    def objectPathComponent_sempred(self, localctx:ObjectPathComponentContext, predIndex:int):
            if predIndex == 8:
                return self.precpred(self._ctx, 3)
         




