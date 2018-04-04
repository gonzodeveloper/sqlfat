from antlr4 import *
from antlr_lib.SQLFatParser import SQLFatParser
from antlr_lib.SQLFatLexer import SQLFatLexer
from antlr_lib.SQLFatListener2 import SQLFatListener2
from utility import DbUtils

utility = utility()


sql = 'SELECT * FROM t1, t2, t3'
input_steam = InputStream(sql)
lexer = SQLFatLexer(input_steam)
token_stream = CommonTokenStream(lexer)
parser = SQLFatParser(token_stream)
tree = parser.sqlStatement()

walker = ParseTreeWalker()
listener = SQLFatListener2()


walker.walk(listener=listener, t=tree)

print(listener.statement)