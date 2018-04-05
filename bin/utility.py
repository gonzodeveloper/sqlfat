from antlr4 import *
import sqlite3
from .antlr_lib.SQLFatParser import SQLFatParser
from .antlr_lib.SQLFatLexer import SQLFatLexer
from .antlr_lib.SQLFatListener2 import SQLFatListener2


class DbUtils:

    def __init__(self, nodes):
        """
        Constructor with connection to catalog db
        :param nodes: list of nodes in db
        """
        self.nodes = nodes
        self.node_count = len(nodes)
        self.catalog = sqlite3.connect('sqlfat/bin/catalog/catalog.db')
        self.statement = None
        self.current_db = None

    def parse(self, sql):
        """
        Parse a given string of sql into a nested dictionary representation for the antlr parse tree.
        Store in class data.
        :param sql: sql string
        :return: N/A
        """
        # If we receive a quit order immediately set type and don't bother with parse
        if sql == "_quit":
            self.statement = {'type': 'QUIT'}
            return self.statement

        # Get all the tools to create an antlr parse tree
        input_steam = InputStream(sql)
        lexer = SQLFatLexer(input_steam)
        token_stream = CommonTokenStream(lexer)
        parser = SQLFatParser(token_stream)
        tree = parser.sqlStatement()

        # Get a tree walker and listener
        walker = ParseTreeWalker()
        listener = SQLFatListener2()

        # Walking the tree will create a json-like nested dictionary in our listener. We will use this for processing.
        try:
            walker.walk(listener=listener, t=tree)
        # If our parse tree walker throws an error, or if the listener has a null object then the SQL was incorrect
        except AttributeError:
            raise SyntaxError
        if listener.statement is None:
            raise SyntaxError

        self.statement = listener.statement
        return self.statement

    def get_node_strings(self):
        """
        Return a list of sql strings corresponding to the existing parsed statement and the nodes in the database.
        The individual strings will obey the partition restrictions of the given table. For example, an insert statement
        will return a list of null values with one insert statement which will place the given row into the
        correct node partition.
        :return: List of SQL strings to be sent to datanodes
        """
        sql_type = self.statement_type()
        if sql_type == "SELECT":
            return self._nodes_select()
        elif sql_type == "INSERT":
            return self._nodes_insert()
        elif sql_type == "CREATE TABLE":
            return self._nodes_create_table()
        elif sql_type == "USE":
            pass
        elif sql_type == "JOINED":
            return self.get_join_statements()
        else:
            return None

    def set_db(self):
        self.current_db = self.statement['name']

    def get_db(self):
        return self.current_db

    def statement_type(self):
        """
        Determine whether the last statement parsed was a CREATE TABLE statement or not
        :return:
        """
        if self.statement['type'] == "SELECT":
            if self.statement['clauses']['source']['joined'] is True:
                return "JOINED"
        return self.statement['type']

    def enter_table_data(self):
        """
        Only call if parsed statement was CREATE TABLE. Inserts the table's meta data into the catalog db.
        :return: N/A
        """
        db = self.current_db
        tname = self.statement['clauses']['table']
        partition = self.statement['clauses']['partition']
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

        cols = "["
        for keys, defs in self.statement['clauses']['definitions'].items():
            if defs['type'] == 'col':
                cols += " " + defs['name']
        cols += "]"

        vals = [db, tname, partmtd, partcol, partparam1, partparam2, cols]
        row = '"{0}"'.format('", "'.join(vals))

        insert = "INSERT INTO table_meta (db, tname, partmtd, partcol, partparam1, partparam2, cols) " \
                 "VALUES ({})".format(row)
        curs = self.catalog.cursor()
        curs.execute(insert)
        self.catalog.commit()

        return row

    def enter_table_meta_str(self, rowstr):
        """
        Enter meta data for a newly created table into the local catalog db
        :param rowstr: list of meta data values
        :return: NA
        """
        insert = "INSERT INTO table_meta (db, tname, partmtd, partcol, partparam1, partparam2, cols) " \
                 "VALUES ({})".format(rowstr)
        curs = self.catalog.cursor()
        curs.execute(insert)
        self.catalog.commit()

    def _nodes_select(self):
        """
        For the last select statement we need a list of selects to send to each datanode. However the conditionals
        will have to be modified according to range partition restrictions if present
        :return:
        """
        # Get tables' meta_dictionary (this is for simple select so we simply take the first table
        table = self.get_table_meta(self.statement['clauses']['source']['tables'][0])
        statements = [self._proj_tables_to_str()] * self.node_count
        condition = self.statement["clauses"]["conditions"]
        if condition is not None:
            for idx, stmnt in enumerate(statements):
                statements[idx] = stmnt + \
                                  "WHERE " + DbUtils._recurse_conditions_to_str(idx, table, self.node_count, condition)
        return statements

    def _nodes_create_table(self):
        """
        Get create tables strings for the latest statement
        :return:
        """
        sql_str = "CREATE TABLE " + self.statement['clauses']['table'] + " ("
        for keys, vals in self.statement['clauses']['definitions'].items():
            if vals['type'] == 'col':
                sql_str += vals['name'] + " " + vals['datatype']
                if vals['constraint'] is not None:
                    sql_str += " " + vals['constraint']
            else:
                sql_str += vals['type'] + " " + vals['col']
            sql_str += ", "
        # Remove last coma
        sql_str = sql_str[:-2] + ")"
        # Give copy of string for each of nodes
        return [sql_str] * self.node_count

    def _nodes_insert(self):
        '''
        Get insert strings for the latest statement
        :return:
        '''
        # Get table's meta_dictionary
        table = self.get_table_meta(self.statement['clauses']['table'])

        # Get inset statement prefix
        prefix = "INSERT INTO " + self.statement['clauses']['table'] + " ("
        cols = [val for key, val in self.statement['clauses']['columns'].items()]
        prefix += ", ".join(cols) + ") VALUES "

        # Since we might not insert into all nodes, we add prefix strings only after there are values to insert
        insert_flags = [False] * self.node_count
        statements = [None] * self.node_count

        # Find index of partitioned colummn if exists
        part_col_idx = None
        if table['partmtd'] is not "None" and table['partcol'] in cols:
            for idx, val in enumerate(cols):
                if table['partcol'] == cols[idx]:
                    part_col_idx = idx

        # For each row we get insert strings for all nodes (will be none if partition restricts)
        rows = [val for key, val in self.statement['clauses']['values'].items()]
        for row in rows:
            row = [val for key, val in row.items()]
            for idx in range(self.node_count):
                ins_row = DbUtils.row_for_node(idx, self.node_count, table, row, part_col_idx)
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

    def get_table_meta(self, table_name):
        """
        Get a dictionary of the meta data for a given table. Including table name, partition method, partition column,
        and the partition parameters
        :param table_name: name of table, string
        :return: dictionary contianing metadata
        """
        query = "SELECT tname, partmtd, partcol, partparam1, partparam2, cols " \
                "FROM table_meta " \
                "WHERE tname = \"{}\" ".format(table_name)
        print(query)
        curs = self.catalog.cursor()
        curs.execute(query)
        row = curs.fetchall()[0]
        return {'tname': row[0], 'partmtd': row[1], 'partcol': row[2],
                'partparam1': row[3], 'partparam2': row[4], 'cols': row[5]}

    @staticmethod
    def _in_partition(ranges, value, operator):
        """
        Given a range, operator and value we see if the given partition is used.
        e.g. partition holding ints 10-20 does hold values > 15 but not <= 9, where
        10-20 is the range, 15 and 9 are the values, and > and <= are the values respectively
        :param ranges: tuple with min and max of range, ints
        :param value: int or float of value in question
        :param operator: binary comparison operator  <, >, =, >=, <=, !=, <>, <=>
        :return: True or False depending on evaluation
        """
        (low, high) = ranges
        if type(value) is str:
            value = int(value)
        if operator == "!=" or operator == "<>":
            return True
        elif operator == "=" or operator == "<=>":
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
    def _get_node_range(n, node_idx, col_min, col_max):
        """
        For a table partitioned on a column, we want to know the min and max values each node can hold for the
        given column. We assume when a table is partitioned over a list of nodes, each node will have an equally
        large partition and with the column values being arranged in order of node index (lowest partition at node[0],
        highest values at node[n])
        :param n: number of nodes; int
        :param node_idx: index of node in question; int
        :param col_min: ceiling of partition range, int
        :param col_max: floor of partition range, int
        :return: tuple containing the range for the given node
        """
        if type(col_min) is str:
            col_min = int(col_min)
        if type(col_max) is str:
            col_max = int(col_max)
        idx = node_idx
        node_min = idx * (col_max - col_min) / n
        node_max = (idx + 1) * (col_max - col_min) / n - 1
        return int(node_min), int(node_max)

    @staticmethod
    def _condition_to_str(node_idx, node_count, table, condition):
        """
        Given a binary comparison we output a sql string for the given node. If the values being compared are
        outside the given node's partition range, we simply return "NULL" which will keep that datanode from
        needlessly scanning its table
        :param node_idx: index of data node, int
        :param table: required table information (partcol, partmtd, partparams); dict()
        :param node_count: number of nodes being used
        :param condition: binary comparision (column value on left if present), dict()
        :return: sql string for conditional evaluation by given node
        """
        left = condition['left']
        right = condition['right']
        op = condition['operator']

        if left not in table['cols']:
            return "1=1"

        # If we have a range partition and the column is being used, then modify condition for node in question
        if table['partmtd'] == "range" and table['partcol'] == left:
            node_range = DbUtils._get_node_range(node_count, node_idx, table['partparam1'], table['partparam2'])
            if not DbUtils._in_partition(node_range, right, op):
                return "NULL"
            else:
                return left + " " + op + " " + right
        # If this column is not range partitioned for any of the tables then return to all
        return left + " " + op + " " + right

    @staticmethod
    def _recurse_conditions_to_str(node_idx, node_count, meta,  condition):
        """
        We can structure any combination of logical conditions as a tree with the binary comparisons as leaves.
        Recurse down the tree, convert everything to sql conditional string, and "trim" any leaves whose comparision
        values are outside of our given nodes range partition (if present)
        :param node_idx: index of data node, int
        :param node_count: number of nodes being used
        :param table: required table information (partcol, partmtd, partparams); dict()
        :param condition: logical (AND, OR, NOT, XOR, IS) condition derived from our antlr parse tree
        :return: sql string for conditional evaluation by given node
        """
        log_operator = condition['log_operator']
        if log_operator == "IS":
            return DbUtils._condition_to_str(node_idx, node_count, meta, condition['condition_0'])
        else:
            return DbUtils._recurse_conditions_to_str(node_idx, node_count, meta, condition['condition_0']) + " " + log_operator + " " + \
                    DbUtils._recurse_conditions_to_str(node_idx, node_count, meta, condition['condition_1'])

    def _proj_tables_to_str(self):
        """
        Convert our parse tree back into a sql string with the projected columns and queried table
        :return: sql string
        """
        sql_str = "SELECT "
        for keys, vals in self.statement["clauses"]["projection"].items():
            sql_str += vals + ", "
        # Remove last comma from projection columns
        sql_str = sql_str[:-2] + ' '
        sql_str += "FROM " + self.statement['clauses']['source']['tables'][0] + " "
        return sql_str


    @staticmethod
    def row_for_node(node_idx, node_count, table, row, part_col_idx=None):
        """
        Decides if row of data belongs to a given node. Outputs sql string fragment accordingly
        :param node_idx: index of the node in question, int
        :param node_count: total number of nodes in db, int
        :param table: table metadata to include th partition method and parameters, dictionary
        :param row: row of data in dictionary format
        :param part_col_idx: index of partitioned column in row
        :return: row string "(col0, col1,..., coln)" if the row belongs in the node. otherwise None.
        """
        row_str = '(' + ', '.join(row) + ')'
        if part_col_idx is not None:
            value = int(row[part_col_idx])
            if table['partmtd'] == "range":
                node_min, node_max = DbUtils._get_node_range(node_count, node_idx, table['partparam1'], table['partparam2'])
                if value not in range(node_min, node_max + 1):
                    return None
            elif table['partmtd'] == "hash":
                if value % node_count != node_idx:
                    return None

        return row_str

    def partition_col(self, headers, meta):
        """
        Given a list of column headers for a table, find which one (if any) the table uses as a partition index
        :param headers: list of column names
        :param meta: dict formatted meta data for the table
        :return: index corresponding to column in list that table is partitioned on
        """
        part_col_idx = None
        for idx, cols in enumerate(headers):
            if cols == meta['partcol']:
                part_col_idx = idx
        return part_col_idx

    def target_node(self, row, meta, partition_column):
        """
        Given a row of data determine which datanode it should be entered into.
        :param row: row data, list
        :param meta: dict formatted meta data for the table
        :param partition_column: index of partition column in the row
        :return:
        """
        node_count = self.node_count
        target_idx = None
        if meta['partmtd'] == "range":
            if partition_column is not None:
                partmin = int(meta['partparam1'])
                partmax = int(meta['partparam2'])
                val = int(row[partition_column])
                target_idx = int(val / ((partmax - partmin) / node_count))

        elif meta['partmtd'] == "hash":
            if partition_column is not None:
                val = int(row[partition_column])
                target_idx = val % node_count

        return target_idx

    def get_join_statements(self):
        statement_list = []
        for tables in self.statement['clauses']['source']['tables']:
            meta = self.get_table_meta(tables)
            t_row = []
            for idx in range(self.node_count):
                statement = "SELECT * FROM {} ".format(tables)
                condition = self.statement["clauses"]["conditions"]
                if condition is not None:
                    statement += "WHERE " + DbUtils._recurse_conditions_to_str(idx, self.node_count, meta, condition)
                t_row.append(statement)
            statement_list.append(t_row)
        print(statement_list)
        return statement_list
