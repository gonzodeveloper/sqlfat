# Generated from SQLFat.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SQLFatParser import SQLFatParser
else:
    from SQLFatParser import SQLFatParser

# This class defines a complete listener for a parse tree produced by SQLFatParser.
class SQLFatListener(ParseTreeListener):

    # Enter a parse tree produced by SQLFatParser#sqlStatement.
    def enterSqlStatement(self, ctx:SQLFatParser.SqlStatementContext):
        pass

    # Exit a parse tree produced by SQLFatParser#sqlStatement.
    def exitSqlStatement(self, ctx:SQLFatParser.SqlStatementContext):
        pass


    # Enter a parse tree produced by SQLFatParser#utilityStatement.
    def enterUtilityStatement(self, ctx:SQLFatParser.UtilityStatementContext):
        pass

    # Exit a parse tree produced by SQLFatParser#utilityStatement.
    def exitUtilityStatement(self, ctx:SQLFatParser.UtilityStatementContext):
        pass


    # Enter a parse tree produced by SQLFatParser#ddlStatement.
    def enterDdlStatement(self, ctx:SQLFatParser.DdlStatementContext):
        pass

    # Exit a parse tree produced by SQLFatParser#ddlStatement.
    def exitDdlStatement(self, ctx:SQLFatParser.DdlStatementContext):
        pass


    # Enter a parse tree produced by SQLFatParser#dmlStatement.
    def enterDmlStatement(self, ctx:SQLFatParser.DmlStatementContext):
        pass

    # Exit a parse tree produced by SQLFatParser#dmlStatement.
    def exitDmlStatement(self, ctx:SQLFatParser.DmlStatementContext):
        pass


    # Enter a parse tree produced by SQLFatParser#useStatement.
    def enterUseStatement(self, ctx:SQLFatParser.UseStatementContext):
        pass

    # Exit a parse tree produced by SQLFatParser#useStatement.
    def exitUseStatement(self, ctx:SQLFatParser.UseStatementContext):
        pass


    # Enter a parse tree produced by SQLFatParser#explainStatement.
    def enterExplainStatement(self, ctx:SQLFatParser.ExplainStatementContext):
        pass

    # Exit a parse tree produced by SQLFatParser#explainStatement.
    def exitExplainStatement(self, ctx:SQLFatParser.ExplainStatementContext):
        pass


    # Enter a parse tree produced by SQLFatParser#simpleSelect.
    def enterSimpleSelect(self, ctx:SQLFatParser.SimpleSelectContext):
        pass

    # Exit a parse tree produced by SQLFatParser#simpleSelect.
    def exitSimpleSelect(self, ctx:SQLFatParser.SimpleSelectContext):
        pass


    # Enter a parse tree produced by SQLFatParser#parenthesisSelect.
    def enterParenthesisSelect(self, ctx:SQLFatParser.ParenthesisSelectContext):
        pass

    # Exit a parse tree produced by SQLFatParser#parenthesisSelect.
    def exitParenthesisSelect(self, ctx:SQLFatParser.ParenthesisSelectContext):
        pass


    # Enter a parse tree produced by SQLFatParser#unionSelect.
    def enterUnionSelect(self, ctx:SQLFatParser.UnionSelectContext):
        pass

    # Exit a parse tree produced by SQLFatParser#unionSelect.
    def exitUnionSelect(self, ctx:SQLFatParser.UnionSelectContext):
        pass


    # Enter a parse tree produced by SQLFatParser#unionParenthesisSelect.
    def enterUnionParenthesisSelect(self, ctx:SQLFatParser.UnionParenthesisSelectContext):
        pass

    # Exit a parse tree produced by SQLFatParser#unionParenthesisSelect.
    def exitUnionParenthesisSelect(self, ctx:SQLFatParser.UnionParenthesisSelectContext):
        pass


    # Enter a parse tree produced by SQLFatParser#querySpecification.
    def enterQuerySpecification(self, ctx:SQLFatParser.QuerySpecificationContext):
        pass

    # Exit a parse tree produced by SQLFatParser#querySpecification.
    def exitQuerySpecification(self, ctx:SQLFatParser.QuerySpecificationContext):
        pass


    # Enter a parse tree produced by SQLFatParser#queryExpression.
    def enterQueryExpression(self, ctx:SQLFatParser.QueryExpressionContext):
        pass

    # Exit a parse tree produced by SQLFatParser#queryExpression.
    def exitQueryExpression(self, ctx:SQLFatParser.QueryExpressionContext):
        pass


    # Enter a parse tree produced by SQLFatParser#queryExpressionNointo.
    def enterQueryExpressionNointo(self, ctx:SQLFatParser.QueryExpressionNointoContext):
        pass

    # Exit a parse tree produced by SQLFatParser#queryExpressionNointo.
    def exitQueryExpressionNointo(self, ctx:SQLFatParser.QueryExpressionNointoContext):
        pass


    # Enter a parse tree produced by SQLFatParser#querySpecificationNointo.
    def enterQuerySpecificationNointo(self, ctx:SQLFatParser.QuerySpecificationNointoContext):
        pass

    # Exit a parse tree produced by SQLFatParser#querySpecificationNointo.
    def exitQuerySpecificationNointo(self, ctx:SQLFatParser.QuerySpecificationNointoContext):
        pass


    # Enter a parse tree produced by SQLFatParser#unionStatement.
    def enterUnionStatement(self, ctx:SQLFatParser.UnionStatementContext):
        pass

    # Exit a parse tree produced by SQLFatParser#unionStatement.
    def exitUnionStatement(self, ctx:SQLFatParser.UnionStatementContext):
        pass


    # Enter a parse tree produced by SQLFatParser#unionParenthesis.
    def enterUnionParenthesis(self, ctx:SQLFatParser.UnionParenthesisContext):
        pass

    # Exit a parse tree produced by SQLFatParser#unionParenthesis.
    def exitUnionParenthesis(self, ctx:SQLFatParser.UnionParenthesisContext):
        pass


    # Enter a parse tree produced by SQLFatParser#selectSpec.
    def enterSelectSpec(self, ctx:SQLFatParser.SelectSpecContext):
        pass

    # Exit a parse tree produced by SQLFatParser#selectSpec.
    def exitSelectSpec(self, ctx:SQLFatParser.SelectSpecContext):
        pass


    # Enter a parse tree produced by SQLFatParser#selectElements.
    def enterSelectElements(self, ctx:SQLFatParser.SelectElementsContext):
        pass

    # Exit a parse tree produced by SQLFatParser#selectElements.
    def exitSelectElements(self, ctx:SQLFatParser.SelectElementsContext):
        pass


    # Enter a parse tree produced by SQLFatParser#selectStarElement.
    def enterSelectStarElement(self, ctx:SQLFatParser.SelectStarElementContext):
        pass

    # Exit a parse tree produced by SQLFatParser#selectStarElement.
    def exitSelectStarElement(self, ctx:SQLFatParser.SelectStarElementContext):
        pass


    # Enter a parse tree produced by SQLFatParser#selectColumnElement.
    def enterSelectColumnElement(self, ctx:SQLFatParser.SelectColumnElementContext):
        pass

    # Exit a parse tree produced by SQLFatParser#selectColumnElement.
    def exitSelectColumnElement(self, ctx:SQLFatParser.SelectColumnElementContext):
        pass


    # Enter a parse tree produced by SQLFatParser#selectFunctionElement.
    def enterSelectFunctionElement(self, ctx:SQLFatParser.SelectFunctionElementContext):
        pass

    # Exit a parse tree produced by SQLFatParser#selectFunctionElement.
    def exitSelectFunctionElement(self, ctx:SQLFatParser.SelectFunctionElementContext):
        pass


    # Enter a parse tree produced by SQLFatParser#selectExpressionElement.
    def enterSelectExpressionElement(self, ctx:SQLFatParser.SelectExpressionElementContext):
        pass

    # Exit a parse tree produced by SQLFatParser#selectExpressionElement.
    def exitSelectExpressionElement(self, ctx:SQLFatParser.SelectExpressionElementContext):
        pass


    # Enter a parse tree produced by SQLFatParser#insertStatement.
    def enterInsertStatement(self, ctx:SQLFatParser.InsertStatementContext):
        pass

    # Exit a parse tree produced by SQLFatParser#insertStatement.
    def exitInsertStatement(self, ctx:SQLFatParser.InsertStatementContext):
        pass


    # Enter a parse tree produced by SQLFatParser#loadDataStatement.
    def enterLoadDataStatement(self, ctx:SQLFatParser.LoadDataStatementContext):
        pass

    # Exit a parse tree produced by SQLFatParser#loadDataStatement.
    def exitLoadDataStatement(self, ctx:SQLFatParser.LoadDataStatementContext):
        pass


    # Enter a parse tree produced by SQLFatParser#insertStatementValue.
    def enterInsertStatementValue(self, ctx:SQLFatParser.InsertStatementValueContext):
        pass

    # Exit a parse tree produced by SQLFatParser#insertStatementValue.
    def exitInsertStatementValue(self, ctx:SQLFatParser.InsertStatementValueContext):
        pass


    # Enter a parse tree produced by SQLFatParser#updatedElement.
    def enterUpdatedElement(self, ctx:SQLFatParser.UpdatedElementContext):
        pass

    # Exit a parse tree produced by SQLFatParser#updatedElement.
    def exitUpdatedElement(self, ctx:SQLFatParser.UpdatedElementContext):
        pass


    # Enter a parse tree produced by SQLFatParser#deleteStatement.
    def enterDeleteStatement(self, ctx:SQLFatParser.DeleteStatementContext):
        pass

    # Exit a parse tree produced by SQLFatParser#deleteStatement.
    def exitDeleteStatement(self, ctx:SQLFatParser.DeleteStatementContext):
        pass


    # Enter a parse tree produced by SQLFatParser#singleDeleteStatement.
    def enterSingleDeleteStatement(self, ctx:SQLFatParser.SingleDeleteStatementContext):
        pass

    # Exit a parse tree produced by SQLFatParser#singleDeleteStatement.
    def exitSingleDeleteStatement(self, ctx:SQLFatParser.SingleDeleteStatementContext):
        pass


    # Enter a parse tree produced by SQLFatParser#multipleDeleteStatement.
    def enterMultipleDeleteStatement(self, ctx:SQLFatParser.MultipleDeleteStatementContext):
        pass

    # Exit a parse tree produced by SQLFatParser#multipleDeleteStatement.
    def exitMultipleDeleteStatement(self, ctx:SQLFatParser.MultipleDeleteStatementContext):
        pass


    # Enter a parse tree produced by SQLFatParser#selectFieldsInto.
    def enterSelectFieldsInto(self, ctx:SQLFatParser.SelectFieldsIntoContext):
        pass

    # Exit a parse tree produced by SQLFatParser#selectFieldsInto.
    def exitSelectFieldsInto(self, ctx:SQLFatParser.SelectFieldsIntoContext):
        pass


    # Enter a parse tree produced by SQLFatParser#selectLinesInto.
    def enterSelectLinesInto(self, ctx:SQLFatParser.SelectLinesIntoContext):
        pass

    # Exit a parse tree produced by SQLFatParser#selectLinesInto.
    def exitSelectLinesInto(self, ctx:SQLFatParser.SelectLinesIntoContext):
        pass


    # Enter a parse tree produced by SQLFatParser#fromClause.
    def enterFromClause(self, ctx:SQLFatParser.FromClauseContext):
        pass

    # Exit a parse tree produced by SQLFatParser#fromClause.
    def exitFromClause(self, ctx:SQLFatParser.FromClauseContext):
        pass


    # Enter a parse tree produced by SQLFatParser#orderByClause.
    def enterOrderByClause(self, ctx:SQLFatParser.OrderByClauseContext):
        pass

    # Exit a parse tree produced by SQLFatParser#orderByClause.
    def exitOrderByClause(self, ctx:SQLFatParser.OrderByClauseContext):
        pass


    # Enter a parse tree produced by SQLFatParser#orderByExpression.
    def enterOrderByExpression(self, ctx:SQLFatParser.OrderByExpressionContext):
        pass

    # Exit a parse tree produced by SQLFatParser#orderByExpression.
    def exitOrderByExpression(self, ctx:SQLFatParser.OrderByExpressionContext):
        pass


    # Enter a parse tree produced by SQLFatParser#limitClause.
    def enterLimitClause(self, ctx:SQLFatParser.LimitClauseContext):
        pass

    # Exit a parse tree produced by SQLFatParser#limitClause.
    def exitLimitClause(self, ctx:SQLFatParser.LimitClauseContext):
        pass


    # Enter a parse tree produced by SQLFatParser#groupByItem.
    def enterGroupByItem(self, ctx:SQLFatParser.GroupByItemContext):
        pass

    # Exit a parse tree produced by SQLFatParser#groupByItem.
    def exitGroupByItem(self, ctx:SQLFatParser.GroupByItemContext):
        pass


    # Enter a parse tree produced by SQLFatParser#tableSources.
    def enterTableSources(self, ctx:SQLFatParser.TableSourcesContext):
        pass

    # Exit a parse tree produced by SQLFatParser#tableSources.
    def exitTableSources(self, ctx:SQLFatParser.TableSourcesContext):
        pass


    # Enter a parse tree produced by SQLFatParser#tableSourceBase.
    def enterTableSourceBase(self, ctx:SQLFatParser.TableSourceBaseContext):
        pass

    # Exit a parse tree produced by SQLFatParser#tableSourceBase.
    def exitTableSourceBase(self, ctx:SQLFatParser.TableSourceBaseContext):
        pass


    # Enter a parse tree produced by SQLFatParser#tableSourceNested.
    def enterTableSourceNested(self, ctx:SQLFatParser.TableSourceNestedContext):
        pass

    # Exit a parse tree produced by SQLFatParser#tableSourceNested.
    def exitTableSourceNested(self, ctx:SQLFatParser.TableSourceNestedContext):
        pass


    # Enter a parse tree produced by SQLFatParser#atomTableItem.
    def enterAtomTableItem(self, ctx:SQLFatParser.AtomTableItemContext):
        pass

    # Exit a parse tree produced by SQLFatParser#atomTableItem.
    def exitAtomTableItem(self, ctx:SQLFatParser.AtomTableItemContext):
        pass


    # Enter a parse tree produced by SQLFatParser#subqueryTableItem.
    def enterSubqueryTableItem(self, ctx:SQLFatParser.SubqueryTableItemContext):
        pass

    # Exit a parse tree produced by SQLFatParser#subqueryTableItem.
    def exitSubqueryTableItem(self, ctx:SQLFatParser.SubqueryTableItemContext):
        pass


    # Enter a parse tree produced by SQLFatParser#tableSourcesItem.
    def enterTableSourcesItem(self, ctx:SQLFatParser.TableSourcesItemContext):
        pass

    # Exit a parse tree produced by SQLFatParser#tableSourcesItem.
    def exitTableSourcesItem(self, ctx:SQLFatParser.TableSourcesItemContext):
        pass


    # Enter a parse tree produced by SQLFatParser#innerJoin.
    def enterInnerJoin(self, ctx:SQLFatParser.InnerJoinContext):
        pass

    # Exit a parse tree produced by SQLFatParser#innerJoin.
    def exitInnerJoin(self, ctx:SQLFatParser.InnerJoinContext):
        pass


    # Enter a parse tree produced by SQLFatParser#outerJoin.
    def enterOuterJoin(self, ctx:SQLFatParser.OuterJoinContext):
        pass

    # Exit a parse tree produced by SQLFatParser#outerJoin.
    def exitOuterJoin(self, ctx:SQLFatParser.OuterJoinContext):
        pass


    # Enter a parse tree produced by SQLFatParser#naturalJoin.
    def enterNaturalJoin(self, ctx:SQLFatParser.NaturalJoinContext):
        pass

    # Exit a parse tree produced by SQLFatParser#naturalJoin.
    def exitNaturalJoin(self, ctx:SQLFatParser.NaturalJoinContext):
        pass


    # Enter a parse tree produced by SQLFatParser#createDatabase.
    def enterCreateDatabase(self, ctx:SQLFatParser.CreateDatabaseContext):
        pass

    # Exit a parse tree produced by SQLFatParser#createDatabase.
    def exitCreateDatabase(self, ctx:SQLFatParser.CreateDatabaseContext):
        pass


    # Enter a parse tree produced by SQLFatParser#dropDatabase.
    def enterDropDatabase(self, ctx:SQLFatParser.DropDatabaseContext):
        pass

    # Exit a parse tree produced by SQLFatParser#dropDatabase.
    def exitDropDatabase(self, ctx:SQLFatParser.DropDatabaseContext):
        pass


    # Enter a parse tree produced by SQLFatParser#ifNotExists.
    def enterIfNotExists(self, ctx:SQLFatParser.IfNotExistsContext):
        pass

    # Exit a parse tree produced by SQLFatParser#ifNotExists.
    def exitIfNotExists(self, ctx:SQLFatParser.IfNotExistsContext):
        pass


    # Enter a parse tree produced by SQLFatParser#ifExists.
    def enterIfExists(self, ctx:SQLFatParser.IfExistsContext):
        pass

    # Exit a parse tree produced by SQLFatParser#ifExists.
    def exitIfExists(self, ctx:SQLFatParser.IfExistsContext):
        pass


    # Enter a parse tree produced by SQLFatParser#copyCreateTable.
    def enterCopyCreateTable(self, ctx:SQLFatParser.CopyCreateTableContext):
        pass

    # Exit a parse tree produced by SQLFatParser#copyCreateTable.
    def exitCopyCreateTable(self, ctx:SQLFatParser.CopyCreateTableContext):
        pass


    # Enter a parse tree produced by SQLFatParser#queryCreateTable.
    def enterQueryCreateTable(self, ctx:SQLFatParser.QueryCreateTableContext):
        pass

    # Exit a parse tree produced by SQLFatParser#queryCreateTable.
    def exitQueryCreateTable(self, ctx:SQLFatParser.QueryCreateTableContext):
        pass


    # Enter a parse tree produced by SQLFatParser#columnCreateTable.
    def enterColumnCreateTable(self, ctx:SQLFatParser.ColumnCreateTableContext):
        pass

    # Exit a parse tree produced by SQLFatParser#columnCreateTable.
    def exitColumnCreateTable(self, ctx:SQLFatParser.ColumnCreateTableContext):
        pass


    # Enter a parse tree produced by SQLFatParser#dropTable.
    def enterDropTable(self, ctx:SQLFatParser.DropTableContext):
        pass

    # Exit a parse tree produced by SQLFatParser#dropTable.
    def exitDropTable(self, ctx:SQLFatParser.DropTableContext):
        pass


    # Enter a parse tree produced by SQLFatParser#tables.
    def enterTables(self, ctx:SQLFatParser.TablesContext):
        pass

    # Exit a parse tree produced by SQLFatParser#tables.
    def exitTables(self, ctx:SQLFatParser.TablesContext):
        pass


    # Enter a parse tree produced by SQLFatParser#truncateTable.
    def enterTruncateTable(self, ctx:SQLFatParser.TruncateTableContext):
        pass

    # Exit a parse tree produced by SQLFatParser#truncateTable.
    def exitTruncateTable(self, ctx:SQLFatParser.TruncateTableContext):
        pass


    # Enter a parse tree produced by SQLFatParser#createDefinitions.
    def enterCreateDefinitions(self, ctx:SQLFatParser.CreateDefinitionsContext):
        pass

    # Exit a parse tree produced by SQLFatParser#createDefinitions.
    def exitCreateDefinitions(self, ctx:SQLFatParser.CreateDefinitionsContext):
        pass


    # Enter a parse tree produced by SQLFatParser#columnDeclaration.
    def enterColumnDeclaration(self, ctx:SQLFatParser.ColumnDeclarationContext):
        pass

    # Exit a parse tree produced by SQLFatParser#columnDeclaration.
    def exitColumnDeclaration(self, ctx:SQLFatParser.ColumnDeclarationContext):
        pass


    # Enter a parse tree produced by SQLFatParser#constraintDeclaration.
    def enterConstraintDeclaration(self, ctx:SQLFatParser.ConstraintDeclarationContext):
        pass

    # Exit a parse tree produced by SQLFatParser#constraintDeclaration.
    def exitConstraintDeclaration(self, ctx:SQLFatParser.ConstraintDeclarationContext):
        pass


    # Enter a parse tree produced by SQLFatParser#indexDeclaration.
    def enterIndexDeclaration(self, ctx:SQLFatParser.IndexDeclarationContext):
        pass

    # Exit a parse tree produced by SQLFatParser#indexDeclaration.
    def exitIndexDeclaration(self, ctx:SQLFatParser.IndexDeclarationContext):
        pass


    # Enter a parse tree produced by SQLFatParser#columnDefinition.
    def enterColumnDefinition(self, ctx:SQLFatParser.ColumnDefinitionContext):
        pass

    # Exit a parse tree produced by SQLFatParser#columnDefinition.
    def exitColumnDefinition(self, ctx:SQLFatParser.ColumnDefinitionContext):
        pass


    # Enter a parse tree produced by SQLFatParser#nullColumnConstraint.
    def enterNullColumnConstraint(self, ctx:SQLFatParser.NullColumnConstraintContext):
        pass

    # Exit a parse tree produced by SQLFatParser#nullColumnConstraint.
    def exitNullColumnConstraint(self, ctx:SQLFatParser.NullColumnConstraintContext):
        pass


    # Enter a parse tree produced by SQLFatParser#primaryKeyColumnConstraint.
    def enterPrimaryKeyColumnConstraint(self, ctx:SQLFatParser.PrimaryKeyColumnConstraintContext):
        pass

    # Exit a parse tree produced by SQLFatParser#primaryKeyColumnConstraint.
    def exitPrimaryKeyColumnConstraint(self, ctx:SQLFatParser.PrimaryKeyColumnConstraintContext):
        pass


    # Enter a parse tree produced by SQLFatParser#uniqueKeyColumnConstraint.
    def enterUniqueKeyColumnConstraint(self, ctx:SQLFatParser.UniqueKeyColumnConstraintContext):
        pass

    # Exit a parse tree produced by SQLFatParser#uniqueKeyColumnConstraint.
    def exitUniqueKeyColumnConstraint(self, ctx:SQLFatParser.UniqueKeyColumnConstraintContext):
        pass


    # Enter a parse tree produced by SQLFatParser#simpleIndexDeclaration.
    def enterSimpleIndexDeclaration(self, ctx:SQLFatParser.SimpleIndexDeclarationContext):
        pass

    # Exit a parse tree produced by SQLFatParser#simpleIndexDeclaration.
    def exitSimpleIndexDeclaration(self, ctx:SQLFatParser.SimpleIndexDeclarationContext):
        pass


    # Enter a parse tree produced by SQLFatParser#indexType.
    def enterIndexType(self, ctx:SQLFatParser.IndexTypeContext):
        pass

    # Exit a parse tree produced by SQLFatParser#indexType.
    def exitIndexType(self, ctx:SQLFatParser.IndexTypeContext):
        pass


    # Enter a parse tree produced by SQLFatParser#indexColumnNames.
    def enterIndexColumnNames(self, ctx:SQLFatParser.IndexColumnNamesContext):
        pass

    # Exit a parse tree produced by SQLFatParser#indexColumnNames.
    def exitIndexColumnNames(self, ctx:SQLFatParser.IndexColumnNamesContext):
        pass


    # Enter a parse tree produced by SQLFatParser#indexColumnName.
    def enterIndexColumnName(self, ctx:SQLFatParser.IndexColumnNameContext):
        pass

    # Exit a parse tree produced by SQLFatParser#indexColumnName.
    def exitIndexColumnName(self, ctx:SQLFatParser.IndexColumnNameContext):
        pass


    # Enter a parse tree produced by SQLFatParser#partitionDefinitions.
    def enterPartitionDefinitions(self, ctx:SQLFatParser.PartitionDefinitionsContext):
        pass

    # Exit a parse tree produced by SQLFatParser#partitionDefinitions.
    def exitPartitionDefinitions(self, ctx:SQLFatParser.PartitionDefinitionsContext):
        pass


    # Enter a parse tree produced by SQLFatParser#partitionFunctionHash.
    def enterPartitionFunctionHash(self, ctx:SQLFatParser.PartitionFunctionHashContext):
        pass

    # Exit a parse tree produced by SQLFatParser#partitionFunctionHash.
    def exitPartitionFunctionHash(self, ctx:SQLFatParser.PartitionFunctionHashContext):
        pass


    # Enter a parse tree produced by SQLFatParser#partitionFunctionKey.
    def enterPartitionFunctionKey(self, ctx:SQLFatParser.PartitionFunctionKeyContext):
        pass

    # Exit a parse tree produced by SQLFatParser#partitionFunctionKey.
    def exitPartitionFunctionKey(self, ctx:SQLFatParser.PartitionFunctionKeyContext):
        pass


    # Enter a parse tree produced by SQLFatParser#partitionFunctionRange.
    def enterPartitionFunctionRange(self, ctx:SQLFatParser.PartitionFunctionRangeContext):
        pass

    # Exit a parse tree produced by SQLFatParser#partitionFunctionRange.
    def exitPartitionFunctionRange(self, ctx:SQLFatParser.PartitionFunctionRangeContext):
        pass


    # Enter a parse tree produced by SQLFatParser#partitionFunctionList.
    def enterPartitionFunctionList(self, ctx:SQLFatParser.PartitionFunctionListContext):
        pass

    # Exit a parse tree produced by SQLFatParser#partitionFunctionList.
    def exitPartitionFunctionList(self, ctx:SQLFatParser.PartitionFunctionListContext):
        pass


    # Enter a parse tree produced by SQLFatParser#primaryKeyTableConstraint.
    def enterPrimaryKeyTableConstraint(self, ctx:SQLFatParser.PrimaryKeyTableConstraintContext):
        pass

    # Exit a parse tree produced by SQLFatParser#primaryKeyTableConstraint.
    def exitPrimaryKeyTableConstraint(self, ctx:SQLFatParser.PrimaryKeyTableConstraintContext):
        pass


    # Enter a parse tree produced by SQLFatParser#uniqueKeyTableConstraint.
    def enterUniqueKeyTableConstraint(self, ctx:SQLFatParser.UniqueKeyTableConstraintContext):
        pass

    # Exit a parse tree produced by SQLFatParser#uniqueKeyTableConstraint.
    def exitUniqueKeyTableConstraint(self, ctx:SQLFatParser.UniqueKeyTableConstraintContext):
        pass


    # Enter a parse tree produced by SQLFatParser#createIndex.
    def enterCreateIndex(self, ctx:SQLFatParser.CreateIndexContext):
        pass

    # Exit a parse tree produced by SQLFatParser#createIndex.
    def exitCreateIndex(self, ctx:SQLFatParser.CreateIndexContext):
        pass


    # Enter a parse tree produced by SQLFatParser#dropIndex.
    def enterDropIndex(self, ctx:SQLFatParser.DropIndexContext):
        pass

    # Exit a parse tree produced by SQLFatParser#dropIndex.
    def exitDropIndex(self, ctx:SQLFatParser.DropIndexContext):
        pass


    # Enter a parse tree produced by SQLFatParser#udfFunctionCall.
    def enterUdfFunctionCall(self, ctx:SQLFatParser.UdfFunctionCallContext):
        pass

    # Exit a parse tree produced by SQLFatParser#udfFunctionCall.
    def exitUdfFunctionCall(self, ctx:SQLFatParser.UdfFunctionCallContext):
        pass


    # Enter a parse tree produced by SQLFatParser#functionArgs.
    def enterFunctionArgs(self, ctx:SQLFatParser.FunctionArgsContext):
        pass

    # Exit a parse tree produced by SQLFatParser#functionArgs.
    def exitFunctionArgs(self, ctx:SQLFatParser.FunctionArgsContext):
        pass


    # Enter a parse tree produced by SQLFatParser#functionArg.
    def enterFunctionArg(self, ctx:SQLFatParser.FunctionArgContext):
        pass

    # Exit a parse tree produced by SQLFatParser#functionArg.
    def exitFunctionArg(self, ctx:SQLFatParser.FunctionArgContext):
        pass


    # Enter a parse tree produced by SQLFatParser#isExpression.
    def enterIsExpression(self, ctx:SQLFatParser.IsExpressionContext):
        pass

    # Exit a parse tree produced by SQLFatParser#isExpression.
    def exitIsExpression(self, ctx:SQLFatParser.IsExpressionContext):
        pass


    # Enter a parse tree produced by SQLFatParser#notExpression.
    def enterNotExpression(self, ctx:SQLFatParser.NotExpressionContext):
        pass

    # Exit a parse tree produced by SQLFatParser#notExpression.
    def exitNotExpression(self, ctx:SQLFatParser.NotExpressionContext):
        pass


    # Enter a parse tree produced by SQLFatParser#logicalExpression.
    def enterLogicalExpression(self, ctx:SQLFatParser.LogicalExpressionContext):
        pass

    # Exit a parse tree produced by SQLFatParser#logicalExpression.
    def exitLogicalExpression(self, ctx:SQLFatParser.LogicalExpressionContext):
        pass


    # Enter a parse tree produced by SQLFatParser#predicateExpression.
    def enterPredicateExpression(self, ctx:SQLFatParser.PredicateExpressionContext):
        pass

    # Exit a parse tree produced by SQLFatParser#predicateExpression.
    def exitPredicateExpression(self, ctx:SQLFatParser.PredicateExpressionContext):
        pass


    # Enter a parse tree produced by SQLFatParser#expressions.
    def enterExpressions(self, ctx:SQLFatParser.ExpressionsContext):
        pass

    # Exit a parse tree produced by SQLFatParser#expressions.
    def exitExpressions(self, ctx:SQLFatParser.ExpressionsContext):
        pass


    # Enter a parse tree produced by SQLFatParser#expressionsWithDefaults.
    def enterExpressionsWithDefaults(self, ctx:SQLFatParser.ExpressionsWithDefaultsContext):
        pass

    # Exit a parse tree produced by SQLFatParser#expressionsWithDefaults.
    def exitExpressionsWithDefaults(self, ctx:SQLFatParser.ExpressionsWithDefaultsContext):
        pass


    # Enter a parse tree produced by SQLFatParser#expressionOrDefault.
    def enterExpressionOrDefault(self, ctx:SQLFatParser.ExpressionOrDefaultContext):
        pass

    # Exit a parse tree produced by SQLFatParser#expressionOrDefault.
    def exitExpressionOrDefault(self, ctx:SQLFatParser.ExpressionOrDefaultContext):
        pass


    # Enter a parse tree produced by SQLFatParser#expressionAtomPredicate.
    def enterExpressionAtomPredicate(self, ctx:SQLFatParser.ExpressionAtomPredicateContext):
        pass

    # Exit a parse tree produced by SQLFatParser#expressionAtomPredicate.
    def exitExpressionAtomPredicate(self, ctx:SQLFatParser.ExpressionAtomPredicateContext):
        pass


    # Enter a parse tree produced by SQLFatParser#inPredicate.
    def enterInPredicate(self, ctx:SQLFatParser.InPredicateContext):
        pass

    # Exit a parse tree produced by SQLFatParser#inPredicate.
    def exitInPredicate(self, ctx:SQLFatParser.InPredicateContext):
        pass


    # Enter a parse tree produced by SQLFatParser#betweenPredicate.
    def enterBetweenPredicate(self, ctx:SQLFatParser.BetweenPredicateContext):
        pass

    # Exit a parse tree produced by SQLFatParser#betweenPredicate.
    def exitBetweenPredicate(self, ctx:SQLFatParser.BetweenPredicateContext):
        pass


    # Enter a parse tree produced by SQLFatParser#binaryComparasionPredicate.
    def enterBinaryComparasionPredicate(self, ctx:SQLFatParser.BinaryComparasionPredicateContext):
        pass

    # Exit a parse tree produced by SQLFatParser#binaryComparasionPredicate.
    def exitBinaryComparasionPredicate(self, ctx:SQLFatParser.BinaryComparasionPredicateContext):
        pass


    # Enter a parse tree produced by SQLFatParser#isNullPredicate.
    def enterIsNullPredicate(self, ctx:SQLFatParser.IsNullPredicateContext):
        pass

    # Exit a parse tree produced by SQLFatParser#isNullPredicate.
    def exitIsNullPredicate(self, ctx:SQLFatParser.IsNullPredicateContext):
        pass


    # Enter a parse tree produced by SQLFatParser#unaryExpressionAtom.
    def enterUnaryExpressionAtom(self, ctx:SQLFatParser.UnaryExpressionAtomContext):
        pass

    # Exit a parse tree produced by SQLFatParser#unaryExpressionAtom.
    def exitUnaryExpressionAtom(self, ctx:SQLFatParser.UnaryExpressionAtomContext):
        pass


    # Enter a parse tree produced by SQLFatParser#subqueryExpessionAtom.
    def enterSubqueryExpessionAtom(self, ctx:SQLFatParser.SubqueryExpessionAtomContext):
        pass

    # Exit a parse tree produced by SQLFatParser#subqueryExpessionAtom.
    def exitSubqueryExpessionAtom(self, ctx:SQLFatParser.SubqueryExpessionAtomContext):
        pass


    # Enter a parse tree produced by SQLFatParser#existsExpessionAtom.
    def enterExistsExpessionAtom(self, ctx:SQLFatParser.ExistsExpessionAtomContext):
        pass

    # Exit a parse tree produced by SQLFatParser#existsExpessionAtom.
    def exitExistsExpessionAtom(self, ctx:SQLFatParser.ExistsExpessionAtomContext):
        pass


    # Enter a parse tree produced by SQLFatParser#constantExpressionAtom.
    def enterConstantExpressionAtom(self, ctx:SQLFatParser.ConstantExpressionAtomContext):
        pass

    # Exit a parse tree produced by SQLFatParser#constantExpressionAtom.
    def exitConstantExpressionAtom(self, ctx:SQLFatParser.ConstantExpressionAtomContext):
        pass


    # Enter a parse tree produced by SQLFatParser#functionCallExpressionAtom.
    def enterFunctionCallExpressionAtom(self, ctx:SQLFatParser.FunctionCallExpressionAtomContext):
        pass

    # Exit a parse tree produced by SQLFatParser#functionCallExpressionAtom.
    def exitFunctionCallExpressionAtom(self, ctx:SQLFatParser.FunctionCallExpressionAtomContext):
        pass


    # Enter a parse tree produced by SQLFatParser#binaryExpressionAtom.
    def enterBinaryExpressionAtom(self, ctx:SQLFatParser.BinaryExpressionAtomContext):
        pass

    # Exit a parse tree produced by SQLFatParser#binaryExpressionAtom.
    def exitBinaryExpressionAtom(self, ctx:SQLFatParser.BinaryExpressionAtomContext):
        pass


    # Enter a parse tree produced by SQLFatParser#fullColumnNameExpressionAtom.
    def enterFullColumnNameExpressionAtom(self, ctx:SQLFatParser.FullColumnNameExpressionAtomContext):
        pass

    # Exit a parse tree produced by SQLFatParser#fullColumnNameExpressionAtom.
    def exitFullColumnNameExpressionAtom(self, ctx:SQLFatParser.FullColumnNameExpressionAtomContext):
        pass


    # Enter a parse tree produced by SQLFatParser#nestedExpressionAtom.
    def enterNestedExpressionAtom(self, ctx:SQLFatParser.NestedExpressionAtomContext):
        pass

    # Exit a parse tree produced by SQLFatParser#nestedExpressionAtom.
    def exitNestedExpressionAtom(self, ctx:SQLFatParser.NestedExpressionAtomContext):
        pass


    # Enter a parse tree produced by SQLFatParser#nestedRowExpressionAtom.
    def enterNestedRowExpressionAtom(self, ctx:SQLFatParser.NestedRowExpressionAtomContext):
        pass

    # Exit a parse tree produced by SQLFatParser#nestedRowExpressionAtom.
    def exitNestedRowExpressionAtom(self, ctx:SQLFatParser.NestedRowExpressionAtomContext):
        pass


    # Enter a parse tree produced by SQLFatParser#mathExpressionAtom.
    def enterMathExpressionAtom(self, ctx:SQLFatParser.MathExpressionAtomContext):
        pass

    # Exit a parse tree produced by SQLFatParser#mathExpressionAtom.
    def exitMathExpressionAtom(self, ctx:SQLFatParser.MathExpressionAtomContext):
        pass


    # Enter a parse tree produced by SQLFatParser#unaryOperator.
    def enterUnaryOperator(self, ctx:SQLFatParser.UnaryOperatorContext):
        pass

    # Exit a parse tree produced by SQLFatParser#unaryOperator.
    def exitUnaryOperator(self, ctx:SQLFatParser.UnaryOperatorContext):
        pass


    # Enter a parse tree produced by SQLFatParser#logicalOperator.
    def enterLogicalOperator(self, ctx:SQLFatParser.LogicalOperatorContext):
        pass

    # Exit a parse tree produced by SQLFatParser#logicalOperator.
    def exitLogicalOperator(self, ctx:SQLFatParser.LogicalOperatorContext):
        pass


    # Enter a parse tree produced by SQLFatParser#comparisonOperator.
    def enterComparisonOperator(self, ctx:SQLFatParser.ComparisonOperatorContext):
        pass

    # Exit a parse tree produced by SQLFatParser#comparisonOperator.
    def exitComparisonOperator(self, ctx:SQLFatParser.ComparisonOperatorContext):
        pass


    # Enter a parse tree produced by SQLFatParser#mathOperator.
    def enterMathOperator(self, ctx:SQLFatParser.MathOperatorContext):
        pass

    # Exit a parse tree produced by SQLFatParser#mathOperator.
    def exitMathOperator(self, ctx:SQLFatParser.MathOperatorContext):
        pass


    # Enter a parse tree produced by SQLFatParser#assignmentField.
    def enterAssignmentField(self, ctx:SQLFatParser.AssignmentFieldContext):
        pass

    # Exit a parse tree produced by SQLFatParser#assignmentField.
    def exitAssignmentField(self, ctx:SQLFatParser.AssignmentFieldContext):
        pass


    # Enter a parse tree produced by SQLFatParser#constant.
    def enterConstant(self, ctx:SQLFatParser.ConstantContext):
        pass

    # Exit a parse tree produced by SQLFatParser#constant.
    def exitConstant(self, ctx:SQLFatParser.ConstantContext):
        pass


    # Enter a parse tree produced by SQLFatParser#nullNotnull.
    def enterNullNotnull(self, ctx:SQLFatParser.NullNotnullContext):
        pass

    # Exit a parse tree produced by SQLFatParser#nullNotnull.
    def exitNullNotnull(self, ctx:SQLFatParser.NullNotnullContext):
        pass


    # Enter a parse tree produced by SQLFatParser#decimalLiteral.
    def enterDecimalLiteral(self, ctx:SQLFatParser.DecimalLiteralContext):
        pass

    # Exit a parse tree produced by SQLFatParser#decimalLiteral.
    def exitDecimalLiteral(self, ctx:SQLFatParser.DecimalLiteralContext):
        pass


    # Enter a parse tree produced by SQLFatParser#booleanLiteral.
    def enterBooleanLiteral(self, ctx:SQLFatParser.BooleanLiteralContext):
        pass

    # Exit a parse tree produced by SQLFatParser#booleanLiteral.
    def exitBooleanLiteral(self, ctx:SQLFatParser.BooleanLiteralContext):
        pass


    # Enter a parse tree produced by SQLFatParser#fullId.
    def enterFullId(self, ctx:SQLFatParser.FullIdContext):
        pass

    # Exit a parse tree produced by SQLFatParser#fullId.
    def exitFullId(self, ctx:SQLFatParser.FullIdContext):
        pass


    # Enter a parse tree produced by SQLFatParser#fullColumnName.
    def enterFullColumnName(self, ctx:SQLFatParser.FullColumnNameContext):
        pass

    # Exit a parse tree produced by SQLFatParser#fullColumnName.
    def exitFullColumnName(self, ctx:SQLFatParser.FullColumnNameContext):
        pass


    # Enter a parse tree produced by SQLFatParser#tableName.
    def enterTableName(self, ctx:SQLFatParser.TableNameContext):
        pass

    # Exit a parse tree produced by SQLFatParser#tableName.
    def exitTableName(self, ctx:SQLFatParser.TableNameContext):
        pass


    # Enter a parse tree produced by SQLFatParser#uid.
    def enterUid(self, ctx:SQLFatParser.UidContext):
        pass

    # Exit a parse tree produced by SQLFatParser#uid.
    def exitUid(self, ctx:SQLFatParser.UidContext):
        pass


    # Enter a parse tree produced by SQLFatParser#uidList.
    def enterUidList(self, ctx:SQLFatParser.UidListContext):
        pass

    # Exit a parse tree produced by SQLFatParser#uidList.
    def exitUidList(self, ctx:SQLFatParser.UidListContext):
        pass


    # Enter a parse tree produced by SQLFatParser#dataTypeBase.
    def enterDataTypeBase(self, ctx:SQLFatParser.DataTypeBaseContext):
        pass

    # Exit a parse tree produced by SQLFatParser#dataTypeBase.
    def exitDataTypeBase(self, ctx:SQLFatParser.DataTypeBaseContext):
        pass


    # Enter a parse tree produced by SQLFatParser#dottedId.
    def enterDottedId(self, ctx:SQLFatParser.DottedIdContext):
        pass

    # Exit a parse tree produced by SQLFatParser#dottedId.
    def exitDottedId(self, ctx:SQLFatParser.DottedIdContext):
        pass


    # Enter a parse tree produced by SQLFatParser#stringLiteral.
    def enterStringLiteral(self, ctx:SQLFatParser.StringLiteralContext):
        pass

    # Exit a parse tree produced by SQLFatParser#stringLiteral.
    def exitStringLiteral(self, ctx:SQLFatParser.StringLiteralContext):
        pass


    # Enter a parse tree produced by SQLFatParser#symbol.
    def enterSymbol(self, ctx:SQLFatParser.SymbolContext):
        pass

    # Exit a parse tree produced by SQLFatParser#symbol.
    def exitSymbol(self, ctx:SQLFatParser.SymbolContext):
        pass


    # Enter a parse tree produced by SQLFatParser#dataType.
    def enterDataType(self, ctx:SQLFatParser.DataTypeContext):
        pass

    # Exit a parse tree produced by SQLFatParser#dataType.
    def exitDataType(self, ctx:SQLFatParser.DataTypeContext):
        pass


