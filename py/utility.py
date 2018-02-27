from antlr4 import *
import json
import sqlite3

if __name__ is not None and "." in __name__:
    from .antlr_lib.SQLFatParser import SQLFatParser
    from .antlr_lib.SQLFatLexer import SQLFatLexer
    from .antlr_lib.SQLFatListener2 import SQLFatListener2
else:
    from antlr_lib.SQLFatParser import SQLFatParser
    from antlr_lib.SQLFatLexer import SQLFatLexer
    from antlr_lib.SQLFatListener2 import SQLFatListener2


class DbUtils():


    def __init__(self, catalog, nodes):
        '''
        Contructor with connection to catalog db
        :param nodes: list of nodes in db
        :param catalog: connection to catalog db
        '''
        self.catalog = catalog
        self.nodes = nodes

    def get_table_meta(self, table_name):

        query = "SELECT tname, partmtd, partcol, partparam1, partparam2, node_count " \
                "FROM tables_meta" \
                "WHERE tname = {} ".format(table_name)
        curs = self.catalog.cursor()
        curs.execute(query)
        row = [x for x in curs.fetchall()]
        return {'tname': row[0], 'partmtd': row[1], 'partcol': row[2],
                'partparam1': row[3], 'partparam2': row[4], 'node_count': row[5]}

    def enter_table_data(self, statement):
        '''

        :param statement:
        :return:
        '''
        tname = statement['clauses']['table']
        partition = statement['clauses']['partition']
        partmtd = partition['function']
        if partmtd == 'range':
            partcol = partition['column']
            partparam1 = partition['values']['low']
            partparam2 = partition['values']['high']
        elif partmtd == 'hash':
            partcol = partition['column']
            partparam1 = partition['values']
            partparam2 = 'NULL'
        else:
            partcol = partparam1 = partparam2 = 'NULL'
        node_count = len(nodes)

        insert = "INSERT INTO table_meta (tname, partmtd, partcol, partparam1, partparam2, node_count)" \
                 "VALUES ({}, {}, {}, {}, {}, {})".format(tname, partmtd, partcol, partparam1, partparam2, node_count)
        curs = self.catalog.cursor()
        curs.execute()

    @staticmethod
    def in_partition(ranges, value, operator):
        '''
        Given a range, operator and value we see if the given partition is used.
        e.g. partition holding ints 10-20 does hold values > 15 but not <= 9, where
        10-20 is the range, 15 and 9 are the values, and > and <= are the values respectively
        :param ranges: tuple with min and max of range, ints
        :param value: int or float of value in question
        :param operator: binary comparison operator  <, >, =, >=, <=, !=, <>, <=>
        :return: True or False depending on evaluation
        '''
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

    @staticmethod
    def get_node_range(n, node_idx, col_min, col_max):
        '''
        For a table partitioned on a column, we want to know the min and max values each node can hold for the
        given column. We assume when a table is partitioned over a list of nodes, each node will have an equally
        large partition and with the column values being arranged in order of node index (lowest partition at node[0],
        highest values at node[n])
        :param n: number of nodes; int
        :param node_idx: index of node in question; int
        :param col_min: ceiling of partition range, int
        :param col_max: floor of partition range, int
        :return: tuple containing the range for the given node
        '''
        if type(col_min) is str:
            col_min = int(col_min)
        if type(col_max) is str:
            col_max = int(col_max)
        if type(n) is str:
            n = int(n)
        idx = node_idx
        node_min = idx * (col_max - col_min) / n
        node_max = (idx + 1) * (col_max - col_min) / n - 1
        return int(node_min), int(node_max)

    @staticmethod
    def condition_to_str(node_idx, table, condition):
        '''
        Given a binary comparison we output a sql string for the given node. If the values being compared are
        outside the given node's partition range, we simply return "NULL" which will keep that datanode from
        needlessly scanning its table
        :param node_idx: index of data node, int
        :param table: required table information (partcol, partmtd, partparams, node_count); dict()
        :param condition: binary comparision (column value on left if present), dict()
        :return: sql string for conditional evaluation by given node
        '''
        left = condition['left']
        right = condition['right']
        op = condition['operator']
        # If we have a range partition and the column is being used, then modify condition for node in question
        if table['partmtd'] == "range" and table['partcol'] == left:
            node_range = DbUtils.get_node_range(table["node_count"], node_idx, table['partparam1'], table['partparam2'])
            if not DbUtils.in_partition(node_range, right, op):
                return "NULL"
            else:
                return left + " " + op + " " + right
        else:
            return left + " " + op + " " + right

    @staticmethod
    def recurse_conditions_to_str(node_idx, table, condition):
        '''
        We can structure any combination of logical conditions as a tree with the binary comparisons as leaves.
        Recurse down the tree, convert everything to sql conditional string, and "trim" any leaves whose comparision
        values are outside of our given nodes range partition (if present)
        :param node_idx: index of data node, int
        :param table: required table information (partcol, partmtd, partparams, node_count); dict()
        :param condition: logical (AND, OR, NOT, XOR, IS) condition derived from our antlr parse tree
        :return: sql string for conditional evaluation by given node
        '''
        log_operator = condition['log_operator']
        if log_operator == "IS":
            return DbUtils.condition_to_str(node_idx, table, condition['condition_0'])
        else:
            return DbUtils.recurse_conditions_to_str(node_idx, table, condition['condition_0']) + " " + log_operator + " " + \
                    DbUtils.recurse_conditions_to_str(node_idx, table, condition['condition_1'])

    @staticmethod
    def proj_tables_to_str(sql_statement):
        '''
        Convert our parse tree back into a sql string with the projected columns and queried table
        :param sql_statement: parse dictionary containing a select statement
        :return: sql string
        '''
        sql_str = "SELECT "
        for keys, vals in sql_statement["clauses"]["projection"].items():
            sql_str += vals + ", "
        # Remove last comma from projection columns
        sql_str = sql_str[:-2] + ' '
        sql_str += "FROM {} ".format(sql_statement['clauses']['table'])
        return sql_str


    def nodes_select(self, statement):
        '''
        For the given select statement we need a list of selects to send to each datanode. However the conditionals
        will have to be modified according to range partition restrictions if present
        :param statement: parse dictionary containing a slect statement
        :return:
        '''
        table = self.get_table_meta(statement['clauses']['table'])
        statements = [DbUtils.proj_tables_to_str(statement)] * int(table['node_count'])
        condition = statement["clauses"]["conditions"]
        if condition is not None:
            for idx, stmnt in enumerate(statements):
                statements[idx] = stmnt + "WHERE " + DbUtils.recurse_conditions_to_str(idx, table, condition)
        return statements

    def nodes_create_table(self, statement):
        '''
        Get a sql string for the given statement. Make sure that
        :param statement:
        :return:
        '''
        table = self.get_table_meta(statement['clauses']['table'])
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
        # Give copy of string for each of nodes
        return [sql_str] * int(table['node_count'])


    def nodes_insert(self, statement, table):
        # Get inset statement prefix
        prefix = "INSERT INTO " + statement['clauses']['table'] + " ("
        cols = [val for key, val in statement['clauses']['columns'].items()]
        prefix += ", ".join(cols) + ") VALUES "

        # Since we might not insert into all nodes, we add prefix strings only after there are values to insert
        insert_flags = [False] * int(table['node_count'])
        statements = [None] * int(table['node_count'])

        # Find index of partitioned colummn if exists
        part_col_idx = None
        if table['partmtd'] is not "None":
            if table['partcol'] in cols:
                for idx, val in enumerate(cols):
                    if table['partcol'] == cols[idx]:
                        part_col_idx = idx
        # For each row we get insert strings for all nodes (will be none if partition restrics)
        rows = [val for key, val in statement['clauses']['values'].items()]
        for row in rows:
            row = [val for key, val in row.items()]
            for idx in range(int(table['node_count'])):
                ins_row = DbUtils.row_for_node(idx, table, row, part_col_idx)
                # Add prefix to statements if this is our first insert-able value
                if insert_flags[idx] is False and ins_row is not None:
                    statements[idx] = prefix
                    # Update flags so we don't add prefix more than once
                    insert_flags[idx] = True
                if ins_row is not None:
                    statements[idx] += ins_row + ","
        # Remove final commas
        for idx, stmnt in enumerate(statements):
            if stmnt is not None:
                statements[idx] = stmnt[:-1]
        return statements

    @staticmethod
    def row_for_node(node_idx, table, row, part_col_idx=None):
        row_str = '(' + ', '.join(row) + ')'
        if part_col_idx is not None:
            value = int(row[part_col_idx])
            if table['partmtd'] == "range":
                node_min, node_max = DbUtils.get_node_range(table['node_count'], node_idx, table['partparam1'], table['partparam2'])
                if value not in range(node_min, node_max):
                    return None
                else:
                    return row_str
            elif table['partmtd'] == "hash":
                if value % table['node_count'] != node_idx:
                    return None
                else:
                    return row_str
        else:
            return row_str

if __name__ == "__main__":
    code = 'CREATE TABLE t1 ( ' \
           'uid INT,' \
           'name VARCHAR NOT NULL,' \
           'PRIMARY KEY (uid) ) ' \
           'PARTITION BY HASH(uid, modulo) ' \
           'PARTITIONS 4'

    node1 = "200.0.0.11"
    node2 = "200.0.0.12"
    node3 = "200.0.0.13"

    nodes = [node1, node2, node3]
    table = {"partcol": "uid", "partmtd": "range", "partparam1": "0", "partparam2": "100", "node_count": "4"}

    input_steam = InputStream(code)
    lexer = SQLFatLexer(input_steam)
    token_stream = CommonTokenStream(lexer)
    parser = SQLFatParser(token_stream)
    walker = ParseTreeWalker()
    listener = SQLFatListener2()

    tree = parser.sqlStatement()

    walker.walk(listener=listener, t=tree)
    sql = listener.statement

    print(json.dumps(sql, indent=4, separators=(',', ': ')))
