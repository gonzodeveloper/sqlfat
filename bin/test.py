from antlr4 import *
from antlr_lib.SQLFatParser import SQLFatParser
from antlr_lib.SQLFatLexer import SQLFatLexer
from antlr_lib.SQLFatListener2 import SQLFatListener2




sql = 'INSERT INTO dept_locations (dno, dname)  VALUES (1,"Houston"), (2, "Houston"), (2,"Stafford"), (3,"Bellaire"), (4,"Sugarland"), (5,"Houston")'
input_steam = InputStream(sql)
lexer = SQLFatLexer(input_steam)
token_stream = CommonTokenStream(lexer)
parser = SQLFatParser(token_stream)
tree = parser.sqlStatement()

walker = ParseTreeWalker()
listener = SQLFatListener2()


walker.walk(listener=listener, t=tree)

print(listener.statement)