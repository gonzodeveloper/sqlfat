from antlr4 import *
from antlr_lib.SQLFatParser import SQLFatParser
from antlr_lib.SQLFatLexer import SQLFatLexer
from antlr_lib.SQLFatListener2 import SQLFatListener2




sql = 'CREATE TABLE employee (fname VARCHAR NOT NULL, minit VARCHAR, lname VARCHAR NOT NULL, ssn VARCHAR, bdate DATETIME, address VARCHAR, sex VARCHAR, salary DECIMAL, dno INT) PARTITION BY RANGE(dno, 1, 6) PARTITIONS 3'
input_steam = InputStream(sql)
lexer = SQLFatLexer(input_steam)
token_stream = CommonTokenStream(lexer)
parser = SQLFatParser(token_stream)
tree = parser.sqlStatement()

walker = ParseTreeWalker()
listener = SQLFatListener2()


walker.walk(listener=listener, t=tree)

print(listener.statement)