// This is an ANTLR4 grammar for the STIX Patterning Language.
//
// http://docs.oasis-open.org/cti/stix/v2.0/stix-v2.0-part5-stix-patterning.html

grammar STIXPattern;

pattern
  : observationExpressions
  ;

observationExpressions
  : <assoc=left> observationExpressions FOLLOWEDBY observationExpressions
  | observationExpressionOr
  ;

observationExpressionOr
  : <assoc=left> observationExpressionOr OR observationExpressionOr
  | observationExpressionAnd
  ;

observationExpressionAnd
  : <assoc=left> observationExpressionAnd AND observationExpressionAnd
  | observationExpression
  ;

observationExpression
  : LBRACK comparisonExpression RBRACK        # observationExpressionSimple
  | LPAREN observationExpressions RPAREN      # observationExpressionCompound
  | observationExpression startStopQualifier  # observationExpressionStartStop
  | observationExpression withinQualifier     # observationExpressionWithin
  | observationExpression repeatedQualifier   # observationExpressionRepeated
  ;

comparisonExpression
  : <assoc=left> comparisonExpression OR comparisonExpression   # comparisonExpressionOred
  | comparisonExpressionAnd                                     # comparisonExpressionAnd_
  ;

comparisonExpressionAnd
  : <assoc=left> comparisonExpressionAnd AND comparisonExpressionAnd # comparisonExpressionAnded
  | propTest  # comparisonExpressionAndPropTest
  ;

propTest
  : objectPath NOT? (EQ|NEQ) primitiveLiteral           # propTestEqual
  | objectPath NOT? (GT|LT|GE|LE) orderableLiteral      # propTestOrder
  | objectPath NOT? IN setLiteral                       # propTestSet
  | objectPath NOT? LIKE stringLiteral                  # propTestLike
  | objectPath NOT? MATCHES stringLiteral               # propTestRegex
  | objectPath NOT? ISSUBSET stringLiteral              # propTestIsSubset
  | objectPath NOT? ISSUPERSET stringLiteral            # propTestIsSuperset
  | LPAREN comparisonExpression RPAREN                  # propTestParen
  ;

orderingComparator:
  (GT|LT|GE|LE)
  ;

stringLiteral  // Add parse rule to make getting string literals easier
  : StringLiteral
  ;

startStopQualifier
  : START StringLiteral STOP StringLiteral
  ;

withinQualifier
  : WITHIN (IntLiteral|FloatLiteral) SECONDS
  ;

repeatedQualifier
  : REPEATS IntLiteral TIMES
  ;

objectPath
  : objectType COLON firstPathComponent objectPathComponent?
  ;

// The following two simple rules are for programmer convenience: you
// will get "notification" of object path components in order by the
// generated parser, which enables incremental processing during
// parsing.
objectType
  : IdentifierWithoutHyphen
  | IdentifierWithHyphen
  ;

firstPathComponent
  : IdentifierWithoutHyphen
  | StringLiteral
  ;

objectPathComponent
  : <assoc=left> objectPathComponent objectPathComponent  # pathStep
  | '.' (IdentifierWithoutHyphen | StringLiteral)         # keyPathStep
  | LBRACK (IntLiteral|ASTERISK) RBRACK                   # indexPathStep
  ;

setLiteral
  : LPAREN RPAREN
  | LPAREN primitiveLiteral (COMMA primitiveLiteral)* RPAREN
  ;

primitiveLiteral
  : orderableLiteral
  | BoolLiteral
  ;

orderableLiteral
  : IntLiteral
  | FloatLiteral
  | stringLiteral
  | BinaryLiteral
  | HexLiteral
  | TimestampLiteral
  ;

IntLiteral :
  [+-]? ('0' | [1-9] [0-9]*)
  ;

FloatLiteral :
  [+-]? [0-9]* '.' [0-9]+
  ;

HexLiteral :
  'h' QUOTE TwoHexDigits* QUOTE
  ;

BinaryLiteral :
  'b' QUOTE Base64Char* QUOTE
  ;

StringLiteral :
  QUOTE ( ~['\\] | '\\\'' | '\\\\' )* QUOTE
  ;

BoolLiteral :
  TRUE | FALSE
  ;

TimestampLiteral :
  't' QUOTE
  [0-9] [0-9] [0-9] [0-9] HYPHEN [0-9] [0-9] HYPHEN [0-9] [0-9]
  'T'
  [0-9] [0-9] COLON [0-9] [0-9] COLON [0-9] [0-9] (DOT [0-9]+)?
  'Z'
  QUOTE
  ;

//////////////////////////////////////////////
// Keywords

AND:  A N D;
OR:  O R;
NOT:  N O T;
FOLLOWEDBY: F O L L O W E D B Y;
LIKE:  L I K E ;
MATCHES:  M A T C H E S ;
ISSUPERSET:  I S S U P E R S E T ;
ISSUBSET: I S S U B S E T ;
LAST:  L A S T ;
IN:  I N;
START:  S T A R T ;
STOP:  S T O P ;
SECONDS:  S E C O N D S;
TRUE:  T R U E;
FALSE:  F A L S E;
WITHIN:  W I T H I N;
REPEATS:  R E P E A T S;
TIMES:  T I M E S;

// After keywords, so the lexer doesn't tokenize them as identifiers.
// Object types may have unquoted hyphens, but property names
// (in object paths) cannot.
IdentifierWithoutHyphen :
  [a-zA-Z_] [a-zA-Z0-9_]*
  ;

IdentifierWithHyphen :
  [a-zA-Z_] [a-zA-Z0-9_-]*
  ;

EQ        :   '=' | '==';
NEQ       :   '!=' | '<>';
LT        :   '<';
LE        :   '<=';
GT        :   '>';
GE        :   '>=';

QUOTE     : '\'';
COLON     : ':' ;
DOT       : '.' ;
COMMA     : ',' ;
RPAREN    : ')' ;
LPAREN    : '(' ;
RBRACK    : ']' ;
LBRACK    : '[' ;
PLUS      : '+' ;
HYPHEN    : MINUS ;
MINUS     : '-' ;
POWER_OP  : '^' ;
DIVIDE    : '/' ;
ASTERISK  : '*';

fragment A:  [aA];
fragment B:  [bB];
fragment C:  [cC];
fragment D:  [dD];
fragment E:  [eE];
fragment F:  [fF];
fragment G:  [gG];
fragment H:  [hH];
fragment I:  [iI];
fragment J:  [jJ];
fragment K:  [kK];
fragment L:  [lL];
fragment M:  [mM];
fragment N:  [nN];
fragment O:  [oO];
fragment P:  [pP];
fragment Q:  [qQ];
fragment R:  [rR];
fragment S:  [sS];
fragment T:  [tT];
fragment U:  [uU];
fragment V:  [vV];
fragment W:  [wW];
fragment X:  [xX];
fragment Y:  [yY];
fragment Z:  [zZ];

fragment HexDigit: [A-Fa-f0-9];
fragment TwoHexDigits: HexDigit HexDigit;
fragment Base64Char: [A-Za-z0-9+/=];

// Whitespace and comments
//
WS  :  [ \t\r\n\u000B\u000C\u0085\u00a0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u2028\u2029\u202f\u205f\u3000]+ -> skip
    ;

COMMENT
    :   '/*' .*? '*/' -> skip
    ;

LINE_COMMENT
    :   '//' ~[\r\n]* -> skip
    ;
