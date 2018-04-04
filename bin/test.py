from antlr4 import *
from antlr_lib.SQLFatParser import SQLFatParser
from antlr_lib.SQLFatLexer import SQLFatLexer
from antlr_lib.SQLFatListener2 import SQLFatListener2




sql = 'INSERT INTO employee (fname, minit, lname, ssn, bdate, address, sex, salary, dno) VALUES ("James","E","Borg","888665555","1927/11/10","450 Stone, Houston, TX","M",55000, 5)'
input_steam = InputStream(sql)
lexer = SQLFatLexer(input_steam)
token_stream = CommonTokenStream(lexer)
parser = SQLFatParser(token_stream)
tree = parser.sqlStatement()

walker = ParseTreeWalker()
listener = SQLFatListener2()


walker.walk(listener=listener, t=tree)

print(listener.statement)