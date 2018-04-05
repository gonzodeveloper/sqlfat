from antlr4 import *
from antlr_lib.SQLFatParser import SQLFatParser
from antlr_lib.SQLFatLexer import SQLFatLexer
from antlr_lib.SQLFatListener2 import SQLFatListener2




sql = 'CREATE TABLE department ( dname VARCHAR NOT NULL, dnumber INT NOT NULL, mgrssn VARCHAR ) PARTITION BY RANGE(dnumber, 0, 6) PARTITIONS 3'
input_steam = InputStream(sql)
lexer = SQLFatLexer(input_steam)
token_stream = CommonTokenStream(lexer)
parser = SQLFatParser(token_stream)
tree = parser.sqlStatement()

walker = ParseTreeWalker()
listener = SQLFatListener2()


walker.walk(listener=listener, t=tree)

print(listener.statement)