from antlr4 import *
import json


if __name__ is not None and "." in __name__:
    from .antlr_lib.SQLFatParser import SQLFatParser
    from .antlr_lib.SQLFatLexer import SQLFatLexer
    from .antlr_lib.SQLFatListener2 import SQLFatListener2
else:
    from antlr_lib.SQLFatParser import SQLFatParser
    from antlr_lib.SQLFatLexer import SQLFatLexer
    from antlr_lib.SQLFatListener2 import SQLFatListener2




def in_partition(ranges, value, operator):
    (low, high) = ranges
    if type(value) is str:
        value = int(value)
    if operator == "!=" or operator == "<>":
        return True
    elif operator == "=" or operator =="<=>":
        return low <= value <= high
    elif operator == ">":
        return low > value or high > value
    elif operator == "<":
        return low < value or high < value
    elif operator == ">=":
        return low >= value or high >= value
    elif operator == "<=":
        return low <= value or high <= value

def get_node_range(n, node_idx, col_min, col_max):
    if type(col_min) is str:
        col_min = int(col_min)
    if type(col_max) is str:
        col_max = int(col_max)
    if type(n) is str:
        n = int(n)
    idx = node_idx
    node_min = idx * (col_max - col_min) / n
    node_max = (idx + 1) * (col_max - col_min) / n - 1
    return node_min, node_max

def condition_to_str(node_idx, table, condition):
    left = condition['left']
    right = condition['right']
    op = condition['operator']
    # If we have a range partition and the column is being used, then modify condition for node in question
    if table['partmd'] == "range" and table['partcol'] == left:
        node_range = get_node_range(table["node_count"], node_idx, table['partparam1'], table['partparam2'])
        if not in_partition(node_range, right, op):
            return "NULL"
        else:
            return left + " " + op + " " + right
    else:
        return left + " " + op + " " + right

def recurse_conditions_to_str(node_idx, table, condition):
    log_operator = condition['log_operator']
    if log_operator == "IS":
        return condition_to_str(node_idx, table, condition['condition_0'])
    else:
        return recurse_conditions_to_str(node_idx, table, condition['condition_0']) + " " + log_operator + " " + \
                recurse_conditions_to_str(node_idx, table, condition['condition_1'])

def proj_tables_to_str(sql_statement):
    sql_str = "SELECT "
    for keys, vals in sql_statement["clauses"]["projection"].items():
        sql_str += vals + ", "
    # Remove last comma from projection columns
    sql_str = sql_str[:-2] + ' '
    sql_str += "FROM {} ".format(sql_statement['clauses']['table'])
    return sql_str


def nodes_select(statement, table):
    statements = [proj_tables_to_str(statement)] * int(table['node_count'])
    condition = statement["clauses"]["conditions"]
    if condition is not None:
        for idx, stmnt in enumerate(statements):
            statements[idx] = stmnt + "WHERE " + recurse_conditions_to_str(idx, table, condition)
    return statements

def nodes_create_table(statement, table):
    sql_str = "CREATE TABLE " + statement['clauses']['table'] + " ("
    for keys, vals in statement['clauses']['definitions'].items():
        if vals['type'] == 'col':
            sql_str += vals['name'] + " " + vals['datatype']
            if vals['constraint'] is not None:
                sql_str += " " + vals['constraint']
        else:
            sql_str += vals['type'] + " " + vals['col']
        sql_str += ", "
    # Remove last comment
    sql_str = sql_str[:-2] + ")"

    statements = [sql_str] * int(table['node_count'])

    return statements

def nodes_insert(statement, table):
    sql_str = "INSERT INTO " + statement['clause']['table'] + " VALUES("
    cols = [val for key, val in statement['clause']['columns'].items()]
    sql_str += ", ".join(cols) + ")"
    node_strings = [None] * table['node_count']
    if table['partmd'] is not "None":
        if table['partcol'] in cols:
            for idx in enumerate(cols):
                if table['partcol'] == cols[idx]:
                    part_col_idx = idx
    for key, val in statement['clauses']['values'].items():
        

def row_for_node(node_idx, table, row, part_col_idx=None):
    if part_col_idx is not None:
        value = row[part_col_idx]
        if table['partmd'] == "range":
            node_min, node_max = get_node_range(table['node_count'], node_idx, table['partparam1'], table['partparam2'])
            if value not in range(node_min, node_max):
                return None
        elif table['partmd'] == "hash":
            if value % table['node_count'] != node_idx:
                return None
        else:
            return '(' + ', '.join(row) + ')'


if __name__ == "__main__":
    code = 'INSERT INTO t1 (uid, name, address) VALUES (11, "bob hope", "123 easy st. ")'

    node1 = "200.0.0.11"
    node2 = "200.0.0.12"
    node3 = "200.0.0.13"

    nodes = [node1, node2, node3]
    table = {"partcol": "uid", "partmd": "range", "partparam1": "0", "partparam2": "100", "node_count": "4"}

    input_steam = InputStream(code)
    lexer = SQLFatLexer(input_steam)
    token_stream = CommonTokenStream(lexer)
    parser = SQLFatParser(token_stream)
    walker = ParseTreeWalker()
    listener = SQLFatListener2()

    tree = parser.sqlStatement()

    walker.walk(listener=listener, t=tree)
    sql = listener.statement

    print(json.dumps(sql, indent = 4, separators=(',', ': ')))
