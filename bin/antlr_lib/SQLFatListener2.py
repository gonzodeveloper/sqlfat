if __name__ is not None and "." in __name__:
    from .SQLFatParser import SQLFatParser
    from .SQLFatListener import SQLFatListener
else:
    from SQLFatListener import SQLFatListener
    from SQLFatParser import SQLFatParser


class SQLFatListener2(SQLFatListener):
    """
    This is our custom listener that overloads methods defined by ANTLR's automatically generated listener class.
    This listener is simple. It merely builds a JSON-like dictionary of our parsed SQL statements such that our utility
    class will have easy access to the various fields. Each SQL statement will be defined by a type, either SELECT,
    CREATE TABLE, INSERT, LOAD, USE or QUIT (for now). Once this listener has been walked along a parse tree this
    dictionary can be readily accessed via the statement variable.

    Rather than writing full comments here, it would benefit the user to test this listener on their own. Write a SQL
    statement, get a parse tree, walk the tree with this listener then look at the listener.statement.
    """

    def __init__(self):
        self.statement = None

    def enterSimpleSelect(self, ctx:SQLFatParser.SimpleSelectContext):
        self.statement = {"type": "SELECT",
                          "clauses": self.enterQuerySpecification(ctx.querySpecification())}

    def enterQuerySpecification(self, ctx:SQLFatParser.QuerySpecificationContext):
        return {"projection": self.enterSelectElements(ctx.selectElements()),
                "source": self.enterFromClause(ctx.fromClause(), "source"),
                "conditions": self.enterFromClause(ctx.fromClause(), "conditions")}

    def enterSelectElements(self, ctx:SQLFatParser.SelectElementsContext):
        elements = dict()
        for i in range(0, ctx.getChildCount(), 2):
            d = {"col_{}".format(int(i/2)) : self.enterSelectColumnElement(ctx.getChild(i))}
            elements = {**elements, **d}
        return elements

    def enterSelectColumnElement(self, ctx:SQLFatParser.SelectColumnElementContext):
        return ctx.getText()

    def enterFromClause(self, ctx:SQLFatParser.FromClauseContext, clause=None):
        if clause is "source":
            if isinstance(ctx.source, SQLFatParser.SingleTableContext):
                return self.enterSingleTable(ctx.source)
            elif isinstance(ctx.source, SQLFatParser.JoinedTableContext):
                return self.enterJoinedTable(ctx.source)
            elif isinstance(ctx.source, SQLFatParser.ListTablesContext):
                return self.enterListTables(ctx.source)
            else:
                print('balls')

        elif clause is "conditions":
            if isinstance(ctx.whereExpr, SQLFatParser.LogicalExpressionContext):
                return  self.enterLogicalExpression(ctx.whereExpr)
            elif isinstance(ctx.whereExpr, SQLFatParser.NotExpressionContext):
                return self.enterNotExpression(ctx.whereExpr)
            elif isinstance(ctx.whereExpr, SQLFatParser.IsExpressionContext):
                return self.enterIsExpression(ctx.whereExpr)
            elif isinstance(ctx.whereExpr, SQLFatParser.PredicateExpressionContext):
                return self.enterPredicateExpression(ctx.whereExpr)
            else:
                return None

    def enterSingleTable(self, ctx:SQLFatParser.SingleTableContext):
        return {"tables": [ctx.tableName().getText()],
                "joined": False}

    def enterJoinedTable(self, ctx:SQLFatParser.JoinedTableContext):
        print(ctx.tableName())
        return {"tables": [names.getText() for names in ctx.tableName()],
                "joined": True}

    def enterListTables(self, ctx:SQLFatParser.ListTablesContext):
        return {"tables": [names.getText() for names in ctx.tableName()],
                "joined": True}

    def enterLogicalExpression(self, ctx:SQLFatParser.LogicalExpressionContext):

        if isinstance(ctx.expression(0), SQLFatParser.LogicalExpressionContext):
            c_0 = self.enterLogicalExpression(ctx.expression(0))
        else:
            c_0 = self.enterPredicateExpression(ctx.expression(0))

        if isinstance(ctx.expression(1), SQLFatParser.LogicalExpressionContext):
            c_1 = self.enterLogicalExpression(ctx.expression(1))
        else:
            c_1 = self.enterPredicateExpression(ctx.expression(1))
        return {"log_operator": ctx.logicalOperator().getText(),
                'condition_0': c_0,
                'condition_1': c_1}

    def enterPredicateExpression(self, ctx: SQLFatParser.PredicateExpressionContext):
        if isinstance(ctx.predicate(), SQLFatParser.BinaryComparasionPredicateContext):
            return self.enterBinaryComparasionPredicate(ctx.predicate())
        elif isinstance(ctx.predicate(), SQLFatParser.ExpressionAtomPredicateContext):
            return ctx.getText()

    def enterBinaryComparasionPredicate(self, ctx:SQLFatParser.BinaryComparasionPredicateContext):
        return {"log_operator": "IS",
                'condition_0': {'left': ctx.left.getText(), 'operator': ctx.comparisonOperator().getText(), 'right': ctx.right.getText()}}

    def enterColumnCreateTable(self, ctx:SQLFatParser.ColumnCreateTableContext):
        self.statement = {"type": "CREATE TABLE",
                          "clauses": {
                              "table": self.enterTableName(ctx.tableName()),
                              "definitions":  self.enterCreateDefinitions(ctx.createDefinitions()),
                              "partition": {"column": self.enterPartitionDefinitions(ctx.partitionDefinitions(), "column"),
                                            "function": self.enterPartitionDefinitions(ctx.partitionDefinitions(), "function"),
                                            "values": self.enterPartitionDefinitions(ctx.partitionDefinitions(), "values"),
                                            "number": self.enterPartitionDefinitions(ctx.partitionDefinitions(), "number")
                                           }
                                    }
                          }

    def enterTableName(self, ctx:SQLFatParser.TableNameContext):
        return ctx.getText()

    def enterCreateDefinitions(self, ctx:SQLFatParser.CreateDefinitionsContext):
        elements = dict()
        for i in range(1, ctx.getChildCount(), 2):
            child = ctx.getChild(i)
            if isinstance(child, SQLFatParser.ColumnDeclarationContext):
                defn = self.enterColumnDeclaration(child)
            elif isinstance(child, SQLFatParser.ConstraintDeclarationContext):
                defn = self.enterConstraintDeclaration(child)
            d = {"def_{}".format(int(i / 2)): defn}
            elements = {**elements, **d}
        return elements

    def enterColumnDeclaration(self, ctx:SQLFatParser.ColumnDeclarationContext):
        declaration = {"type": "col", "name": ctx.uid().getText()}
        return {**declaration, **self.enterColumnDefinition(ctx.columnDefinition())}

    def enterColumnDefinition(self, ctx:SQLFatParser.ColumnDefinitionContext):
        if isinstance(ctx.columnConstraint(0), SQLFatParser.NullColumnConstraintContext):
            constraint_txt = "NOT NULL"
        elif isinstance(ctx.columnConstraint(0), SQLFatParser.PrimaryKeyColumnConstraintContext):
            constraint_txt = "PRIMARY KEY"
        elif isinstance(ctx.columnConstraint(0), SQLFatParser.UniqueKeyColumnConstraintContext):
            constraint_txt = "UNIQUE"
        else:
            constraint_txt = None
        return {"datatype": ctx.dataType().getText(), "constraint": constraint_txt}

    def enterConstraintDeclaration(self, ctx:SQLFatParser.ConstraintDeclarationContext):
        constraint = {"type": "constraint"}
        if isinstance(ctx.tableConstraint(), SQLFatParser.PrimaryKeyTableConstraintContext):
            constraint = {**constraint, **self.enterPrimaryKeyTableConstraint(ctx.tableConstraint())}
        return constraint

    def enterPrimaryKeyTableConstraint(self, ctx:SQLFatParser.PrimaryKeyTableConstraintContext):
        return {"type": "PRIMARY KEY", "col": self.enterIndexColumnNames(ctx.indexColumnNames())}

    def enterIndexColumnNames(self, ctx:SQLFatParser.IndexColumnNamesContext):
        return ctx.indexColumnName(0).getText()

    def enterPartitionDefinitions(self, ctx:SQLFatParser.PartitionDefinitionsContext, clause=None):
        if clause is "function":
            if isinstance(ctx.partitionFunctionDefinition(), SQLFatParser.PartitionFunctionHashContext):
                return "hash"
            elif isinstance(ctx.partitionFunctionDefinition(), SQLFatParser.PartitionFunctionRangeContext):
                return "range"
            else:
                return "None"
        elif clause is "values":
            if isinstance(ctx.partitionFunctionDefinition(), SQLFatParser.PartitionFunctionHashContext):
                return self.enterPartitionFunctionHash(ctx.partitionFunctionDefinition(), "values")
            elif isinstance(ctx.partitionFunctionDefinition(), SQLFatParser.PartitionFunctionRangeContext):
                return self.enterPartitionFunctionRange(ctx.partitionFunctionDefinition(), "values")
            else:
                return "None"
        elif clause is "number":
            return ctx.count.getText()
        elif clause is "column":
            if isinstance(ctx.partitionFunctionDefinition(), SQLFatParser.PartitionFunctionHashContext):
                return self.enterPartitionFunctionHash(ctx.partitionFunctionDefinition(), "column")
            elif isinstance(ctx.partitionFunctionDefinition(), SQLFatParser.PartitionFunctionRangeContext):
                return self.enterPartitionFunctionRange(ctx.partitionFunctionDefinition(), "column")

    def enterPartitionFunctionHash(self, ctx:SQLFatParser.PartitionFunctionHashContext, clause=None):
        if clause is "values":
            return ctx.func.getText()
        if clause is "column":
            return ctx.expression(0).getText()

    def enterPartitionFunctionRange(self, ctx:SQLFatParser.PartitionFunctionRangeContext, clause= None):
        if clause is "values":
            return {"low": ctx.low.getText(), "high": ctx.high.getText()}
        if clause is "column":
            return ctx.expression(0).getText()

    def enterInsertStatement(self, ctx:SQLFatParser.InsertStatementContext):
        print(ctx.columns.getText())
        self.statement = {"type": "INSERT",
                          "clauses": {
                              "table": self.enterTableName(ctx.tableName()),
                              "columns": self.enterUidList(ctx.columns, cols=True),
                              "values": self.enterInsertStatementValue(ctx.insertStatementValue())
                          }}

    def enterInsertStatementValue(self, ctx:SQLFatParser.InsertStatementValueContext):
        if ctx.selectStatement():
            return {"subquery" : ctx.selectStatement().getText()}
        else:
            rows = dict()
            for idx, expr in enumerate(ctx.expressionsWithDefaults()):
                d = {"row_{}".format(idx): self.enterExpressionsWithDefaults(expr, cols=True)}
                rows = {**rows, **d}
            return rows

    def enterExpressionsWithDefaults(self, ctx:SQLFatParser.ExpressionsWithDefaultsContext, cols=False):
        if cols is True:
            elements = dict()
            for idx, expr in enumerate(ctx.expressionOrDefault()):
                d = {"col_{}".format(idx): expr.getText()}
                elements = {**elements, **d}
            return elements
        else:
            pass

    def enterUidList(self, ctx:SQLFatParser.UidListContext, cols=False):
        if cols is True:
            elements = dict()
            for idx, uid in enumerate(ctx.uid()):
                d = {"col_{}".format(idx): uid.getText()}
                elements = {**elements, **d}
            return elements
        else:
            pass

    def enterExplainStatement(self, ctx:SQLFatParser.ExplainStatementContext):
        self.statement = {'type': 'EXPLAIN',
                          'table': ctx.fullId().getText()
                          }

    def enterLoadDataStatement(self, ctx:SQLFatParser.LoadDataStatementContext):
        self.statement = {'type': 'LOAD',
                          'file': ctx.filename.getText(),
                          'table': ctx.tableName().getText(),
                          'quotechar': ctx.enclosed_by.getText(),
                          'delimiter': ctx.delimiter.getText()}

    def enterUseStatement(self, ctx:SQLFatParser.UseStatementContext):
        self.statement = {"type": "USE",
                          "name": ctx.fullId().getText()}

    def enterCreateDatabase(self, ctx:SQLFatParser.CreateDatabaseContext):
        self.statement = {"type": "CREATE DATABASE",
                          "name": ctx.uid().getText()}

    def enterDropDatabase(self, ctx:SQLFatParser.DropDatabaseContext):
        self.statement = {"type": "DROP DATABASE",
                          "name": ctx.uid().getText()}

    def enterDropTable(self, ctx:SQLFatParser.DropTableContext):
        self.statement = {"type": "DROP TABLE",
                          "name": ctx.tables().getText()}

    def enterTruncateTable(self, ctx:SQLFatParser.TruncateTableContext):
        self.statement = {"type": "TRUNCATE",
                          "table": ctx.tableName().getText()}

