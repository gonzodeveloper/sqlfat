grammar SQLFat;

sqlStatement
    : ddlStatement | dmlStatement | utilityStatement // | transactionStatement
;

utilityStatement
    : useStatement
;

ddlStatement
    : createDatabase
    | createTable
    | createIndex
    | dropDatabase
    | dropIndex
    | dropTable
    | truncateTable
;

dmlStatement
    : selectStatement
    | insertStatement
    | deleteStatement
    | loadDataStatement
;

// Implement transactions later
/*
transactionStatement
    : startTransaction
    | beginWork
    | commitWork
    | rollbackWork
    | savepointStatement
    | rollbackStatement
    | releaseStatement
;
*/

// Utility Stuff

useStatement
    : USE DATABASE? fullId
;

// DML Stuff

selectStatement
    : querySpecification                                            #simpleSelect
    | queryExpression                                               #parenthesisSelect
    | querySpecificationNointo unionStatement+
        (
          UNION unionType=(ALL | DISTINCT)?
          (querySpecification | queryExpression)
        )?
        orderByClause? limitClause?                                 #unionSelect
    | queryExpressionNointo unionParenthesis+
        (
          UNION unionType=(ALL | DISTINCT)?
          queryExpression
        )?
        orderByClause? limitClause?                                  #unionParenthesisSelect
;

querySpecification
    : SELECT selectSpec* selectElements
      fromClause? orderByClause? limitClause?
    | SELECT selectSpec* selectElements
    fromClause? orderByClause? limitClause?
;

queryExpression
    : '(' querySpecification ')'
    | '(' queryExpression ')'
;

queryExpressionNointo
    : '(' querySpecificationNointo ')'
    | '(' queryExpressionNointo ')'
;

querySpecificationNointo
    : SELECT selectSpec* selectElements
      fromClause? orderByClause? limitClause?
;


unionStatement
    : UNION unionType=(ALL | DISTINCT)?
      (querySpecificationNointo | queryExpressionNointo)
;

unionParenthesis
    : UNION unionType=(ALL | DISTINCT)? queryExpressionNointo
;

selectSpec
    : (ALL | DISTINCT)
;

selectElements
    : (star='*' | selectElement ) (',' selectElement)*
;

selectElement
    : fullId '.' '*'                                                #selectStarElement
    | fullColumnName (AS? uid)?                                     #selectColumnElement
    | functionCall (AS? uid)?                                       #selectFunctionElement
    | expression (AS? uid)?                                         #selectExpressionElement
;



insertStatement
    : INSERT
      IGNORE? INTO tableName
      (
        ('(' columns=uidList ')')? insertStatementValue
        | SET
            setFirst=updatedElement
            (',' setElements+=updatedElement)*
      )
      (
        ON DUPLICATE KEY UPDATE
        duplicatedFirst=updatedElement
        (',' duplicatedElements+=updatedElement)*
      )?
;

loadDataStatement
    : LOAD DATA
      INFILE filename=stringLiteral
      INTO TABLE tableName
      DELIMITER delimiter=uid
      ENCLOSED BY enclosed_by=uid
;

insertStatementValue
    : selectStatement
    | insertFormat=(VALUES | VALUE)
      '(' expressionsWithDefaults ')'
        (',' '(' expressionsWithDefaults ')')*
;

updatedElement
    : fullColumnName '=' (expression | DEFAULT)
;


deleteStatement
    : singleDeleteStatement | multipleDeleteStatement
;

singleDeleteStatement
    : DELETE FROM tableName
      (PARTITION '(' uidList ')' )?
      (WHERE expression)?
      orderByClause? (LIMIT decimalLiteral)?
    ;

multipleDeleteStatement
    : DELETE
      (
        tableName ('.' '*')? ( ',' tableName ('.' '*')? )*
            FROM tableSources
        | FROM
            tableName ('.' '*')? ( ',' tableName ('.' '*')? )*
            USING tableSources
      )
      (WHERE expression)?
;



selectFieldsInto
    : TERMINATED BY terminationField=STRING_LITERAL
    | ENCLOSED BY enclosion=STRING_LITERAL
    | ESCAPED BY escaping=STRING_LITERAL
;

selectLinesInto
    : STARTING BY starting=STRING_LITERAL
    | TERMINATED BY terminationLine=STRING_LITERAL
;



fromClause
    : FROM tableSources
      (WHERE whereExpr=expression)?
      (
        GROUP BY
        groupByItem (',' groupByItem)*
      )?
      (HAVING havingExpr=expression)?
;

orderByClause
    : ORDER BY orderByExpression (',' orderByExpression)*
;

orderByExpression
    : expression order=(ASC | DESC)?
;

limitClause
    : LIMIT
    (
        limit=decimalLiteral
    )
;

groupByItem
    : expression order=(ASC | DESC)?
;


tableSources
    : tableSource (',' tableSource)*
    ;

tableSource
    : tableSourceItem joinPart*                                     #tableSourceBase
    | '(' tableSourceItem joinPart* ')'                             #tableSourceNested
;


tableSourceItem
    : tableName
      (PARTITION '(' uidList ')' )? (AS? alias=uid)?                #atomTableItem
    | (
      selectStatement
      | '(' parenthesisSubquery=selectStatement ')'
      )
      AS? alias=uid                                                 #subqueryTableItem
    | '(' tableSources ')'                                          #tableSourcesItem
;

joinPart
    : (INNER | CROSS)? JOIN tableSourceItem
      (
        ON expression
        | USING '(' uidList ')'
      )?                                                            #innerJoin
    | (LEFT | RIGHT) OUTER? JOIN tableSourceItem
        (
          ON expression
          | USING '(' uidList ')'
        )                                                           #outerJoin
    | NATURAL ((LEFT | RIGHT) OUTER?)? JOIN tableSourceItem         #naturalJoin
;
// DDL Stuff

createDatabase
    : CREATE DATABASE ifNotExists? uid
;

dropDatabase
    : DROP DATABASE ifExists? uid
;


ifNotExists
    : IF NOT EXISTS
;

ifExists
    : IF EXISTS
;

createTable
    : CREATE TABLE ifNotExists?
       tableName
       (
         LIKE tableName
       )                                                            #copyCreateTable
    | CREATE TABLE ifNotExists?
       tableName createDefinitions?
       partitionDefinitions?
       AS? selectStatement                                          #queryCreateTable
    | CREATE TABLE ifNotExists?
       tableName createDefinitions
       partitionDefinitions?                                        #columnCreateTable
;

dropTable
    : DROP TABLE ifExists? tables
;

tables
    : tableName (',' tableName)*
;

truncateTable
    : TRUNCATE TABLE? tableName
    ;

createDefinitions
    : '(' createDefinition (',' createDefinition)* ')'
    ;

createDefinition
    : uid columnDefinition                                          #columnDeclaration
    | tableConstraint                                               #constraintDeclaration
    | indexColumnDefinition                                         #indexDeclaration
;

columnDefinition
    : dataType columnConstraint*
;

columnConstraint
    : nullNotnull                                                   #nullColumnConstraint
    | PRIMARY? KEY                                                  #primaryKeyColumnConstraint
    | UNIQUE KEY?                                                   #uniqueKeyColumnConstraint
;

indexColumnDefinition
    : indexFormat=(INDEX | KEY) uid? indexType?
      indexColumnNames indexType*                                 #simpleIndexDeclaration
;

indexType
    : USING (BTREE | HASH)
;

indexColumnNames
    : '(' indexColumnName (',' indexColumnName)* ')'
;

indexColumnName
    : uid ('(' decimalLiteral ')')? sortType=(ASC | DESC)?
;

partitionDefinitions
    : PARTITION BY partitionFunctionDefinition
      (PARTITIONS count=decimalLiteral)?
;

partitionFunctionDefinition
    : HASH '(' expression ',' func=expression  ')'                   #partitionFunctionHash
    | KEY '(' uidList ')'                                            #partitionFunctionKey
    | RANGE '(' expression ',' low=expression',' high=expression ')' #partitionFunctionRange
    | LIST ( '(' expression ')' | COLUMNS '(' uidList ')' )          #partitionFunctionList
;

tableConstraint
    : (CONSTRAINT name=uid?)?
      PRIMARY KEY indexType? indexColumnNames indexType*          #primaryKeyTableConstraint
    | (CONSTRAINT name=uid?)?
      UNIQUE indexFormat=(INDEX | KEY)? index=uid?
      indexType? indexColumnNames indexType*                      #uniqueKeyTableConstraint
;

createIndex
    : CREATE
      indexCategory=(UNIQUE | FULLTEXT )?
      INDEX uid indexType?
      ON tableName indexColumnNames
;

dropIndex
    : DROP INDEX uid ON tableName
;


// Functions

functionCall
    : fullId '(' functionArgs? ')'                                  #udfFunctionCall

;

functionArgs
    : (constant | fullColumnName | functionCall | expression)
    (
      ','
      (constant | fullColumnName | functionCall | expression)
    )*
;

functionArg
    : constant | fullColumnName | functionCall | expression
;

//    Expressions, predicates

// Simplified approach for expression
expression
    : notOperator=(NOT | '!') expression                            #notExpression
    | expression logicalOperator expression                         #logicalExpression
    | predicate IS NOT? testValue=(TRUE | FALSE )                    #isExpression
    | predicate                                                     #predicateExpression
;

expressions
    : expression (',' expression)*
;

expressionsWithDefaults
    : expressionOrDefault (',' expressionOrDefault)*
;

expressionOrDefault
    : expression | DEFAULT
;


predicate
    : predicate NOT? IN '(' (selectStatement | expressions) ')'     #inPredicate
    | predicate IS nullNotnull                                      #isNullPredicate
    | left=predicate comparisonOperator right=predicate             #binaryComparasionPredicate
    | predicate NOT? BETWEEN predicate AND predicate                #betweenPredicate
    | (LOCAL_ID VAR_ASSIGN)? expressionAtom                         #expressionAtomPredicate
;


expressionAtom
    : constant                                                      #constantExpressionAtom
    | fullColumnName                                                #fullColumnNameExpressionAtom
    | functionCall                                                  #functionCallExpressionAtom
    | unaryOperator expressionAtom                                  #unaryExpressionAtom
    | BINARY expressionAtom                                         #binaryExpressionAtom
    | '(' expression (',' expression)* ')'                          #nestedExpressionAtom
    | ROW '(' expression (',' expression)+ ')'                      #nestedRowExpressionAtom
    | EXISTS '(' selectStatement ')'                                #existsExpessionAtom
    | '(' selectStatement ')'                                       #subqueryExpessionAtom
    | left=expressionAtom mathOperator right=expressionAtom         #mathExpressionAtom
    ;
unaryOperator
    : '!' | '~' | '+' | '-' | NOT
;

logicalOperator
    : AND | '&' '&' | XOR | OR | '|' '|'
;

comparisonOperator
    : '=' | '>' | '<' | '<' '=' | '>' '='
    | '<' '>' | '!' '=' | '<' '=' '>'
;

mathOperator
    : '*' | '/' | '%' | '+' | '-' | '--'
;

// Common clauses

assignmentField
    : uid | LOCAL_ID
;

constant
    : stringLiteral | decimalLiteral
    | booleanLiteral
    | REAL_LITERAL
    | NOT? nullLiteral=(NULL_LITERAL | NULL_SPEC_LITERAL)
;

nullNotnull
    : NOT? (NULL_LITERAL | NULL_SPEC_LITERAL)
;

decimalLiteral
    : DECIMAL_LITERAL
;

booleanLiteral
: TRUE | FALSE;

fullId
    : uid (DOT_ID | '.' uid)?
;

fullColumnName
    : uid (dottedId dottedId? )?
;

tableName
    : fullId
;

uid
    : ID
    | dataTypeBase
;
uidList
    : uid (',' uid)*
;

dataTypeBase
    : DATE | TIME | TIMESTAMP | DATETIME | YEAR | ENUM | TEXT
;

dottedId
    : DOT_ID
    | '.' uid
;

stringLiteral
    : STRING_LITERAL
;

symbol
    : SYMB
;

dataType
    : typeName=(
        CHAR | VARCHAR | TEXT
        | TINYINT | INT | BIGINT
        | REAL | DOUBLE | FLOAT
        | DECIMAL | NUMERIC
        | DATE | BLOB| BOOL| BOOLEAN
        | BIT| TIME | TIMESTAMP | DATETIME | BINARY | VARBINARY | YEAR )
    | typeName=(ENUM | SET)
      '(' STRING_LITERAL (',' STRING_LITERAL)* ')'
;


// Lexer vocabulary
ALL         :       'ALL';
AND         :       'AND';
AS          :       'AS';
ASC         :       'ASC';
BETWEEN     :       'BETWEEN';
BIGINT      :       'BIGINT';
BINARY      :       'BINARY';
BIT         :       'BIT';
BLOB        :       'BLOB';
BOOL        :       'BOOL';
BOOLEAN     :       'BOOLEAN';
BTREE       :       'BTREE';
BY          :       'BY';
CHAR        :       'CHAR';
COLUMNS     :       'COLUMNS';
CONSTRAINT  :       'CONSTRAINT';
CREATE      :       'CREATE';
CROSS       :       'CROSS';
DATA        :       'DATA';
DATABASE    : 	    'DATABASE';
DATE        :       'DATE';
DATETIME    :       'DATETIME';
DECIMAL     :       'DECIMAL';
DEFAULT     :       'DEAFAULT';
DELETE      :       'DELETE';
DELIMITER   :       'DELIMITER';
DESC        :       'DESC';
DISTINCT    :       'DISTINCT';
DOUBLE      :       'DOUBLE';
DROP        :       'DROP';
DUPLICATE   :       'DUPLICATE';
ENCLOSED    :       'ENCLOSED';
ENUM        :       'ENUM';
ESCAPED     :       'ESCAPED';
EXISTS      :       'EXISTS';
FALSE       :       'FALSE';
FIELDS      :       'FIELDS';
FLOAT       :       'FLOAT';
FROM        :       'FROM';
FULLTEXT    :       'FULLTEXT';
GROUP       :       'GROUP';
HAVING      :       'HAVING';
HASH        :       'HASH';
INDEX       :       'INDEX';
INFILE      :       'INFILE';
IF          :       'IF';
IGNORE      :       'IGNORE';
IN          :       'IN';
INNER       :       'INNER';
INSERT      :       'INSERT';
INT         :       'INT';
INTO        :       'INTO';
IS          :       'IS';
JOIN        :       'JOIN';
KEY         :       'KEY';
KEYS        :       'KEYS';
LINE        :       'LINE';
LINES       :       'LINES';
LEFT        :       'LEFT';
LIKE        :       'LIKE';
LIMIT       :       'LIMIT';
LIST        :       'LIST';
LOAD        :       'LOAD';
LOCAL       :       'LOCAL';
NATURAL     :       'NATURAL';
NUMERIC     :       'NUMERIC';
NOT         :       'NOT';
ON          :       'ON';
OR          :       'OR';
ORDER       :       'ORDER';
OUTER       :       'OUTER';
PARTITION   :       'PARTITION';
PARTITIONS  :       'PARTITIONS';
PRIMARY     :       'PRIMARY';
RANGE       :       'RANGE';
REAL        :       'REAL';
REPLACE     :       'REPLACE';
RIGHT       :       'RIGHT';
ROW         :       'ROW';
ROWS        :       'ROWS';
SELECT      :       'SELECT';
SET         :       'SET';
STARTING    :       'STARTING';
TABLE       :       'TABLE';
TERMINATED  :       'TERMINATED';
TEXT        :       'TEXT';
TIME        :       'TIME';
TIMESTAMP   :       'TIMESTAMP';
TINYINT     :       'TINYINT';
TRUNCATE    :       'TRUNCATE';
TRUE        :       'TRUE';
UNION       :       'UNION';
UNIQUE      :       'UNIQUE';
UPDATE      :       'UPDATE';
USE         :       'USE';
USING       :       'USING';
VALUE       :       'VALUE';
VALUES      :       'VALUES';
VARCHAR     :       'VARCHAR';
VARBINARY   :       'VARBINARY';
WHERE       :       'WHERE';
XOR         :       'XOR';
YEAR        :       'YEAR';


NULL_LITERAL        :   'NULL';
ID                  :   ID_LITERAL;
DOT_ID              :   '.' ID_LITERAL;
DECIMAL_LITERAL     :   DEC_DIGIT+;
REAL_LITERAL        :   (DEC_DIGIT+)? '.' DEC_DIGIT+;
STRING_LITERAL      :   DQUOTA_STRING | SQUOTA_STRING;
NULL_SPEC_LITERAL   :   '\\' 'N';
LOCAL_ID            :   '@'     (
                                  [A-Z0-9._$]+
                                  | SQUOTA_STRING
                                  | DQUOTA_STRING
                                );
VAR_ASSIGN          :   ':=';

SPACE               :   [ \t\r\n]+ -> skip;

EQUAL_SYMBOL        :   '=';
GREATER_SYMBOL      :   '>';
LESS_SYMBOL         :   '<';
EXCLAMATION_SYMBOL  :   '!';

DOT                 :   '.';
LR_BRACKET          :   '(';
RR_BRACKET          :   ')';
COMMA               :   ',';
SEMI                :   ';';
AT_SIGN             :   '@';
ZERO_DECIMAL        :   '0';
ONE_DECIMAL         :   '1';
TWO_DECIMAL         :   '2';
SINGLE_QUOTE_SYMB   :   '\'';
DOUBLE_QUOTE_SYMB   :   '"';
REVERSE_QUOTE_SYMB  :   '`';
COLON_SYMB          :   ':';
PIPE                :   '|';
SYMB                :  DOT | COMMA | SEMI | LR_BRACKET | RR_BRACKET | SINGLE_QUOTE_SYMB | DOUBLE_QUOTE_SYMB
                    | REVERSE_QUOTE_SYMB | SPACE | PIPE;

fragment DQUOTA_STRING:              '"' ( '\\'. | '""' | ~('"'| '\\') )* '"';
fragment SQUOTA_STRING: '\'' ('\\'. | '\'\'' | ~('\'' | '\\'))* '\'';
fragment DEC_DIGIT  :   [0-9];
fragment ID_LITERAL :   [a-zA-Z_$0-9]*?[a-zA-Z_$]+?[a-zA-Z_$0-9]*;



