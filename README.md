import org.apache.spark.sql.DataFrame
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

class NodeLevel(feedType: String) {
  val inputTable = "governed.input_table"
  val hierarchyTable = "governed.gmis_hierarchy_cema_cost_center_governed"
  val outputTable = "governed.output_table"
  val hierarchyDf = spark.table(hierarchyTable)

  def fnNodeLevel()(implicit spark: SparkSession): DataFrame = {
    val inputDf = spark.table(inputTable)
    inputDf.show() // Print the contents of the input table

    val modifiedTable = inputDf
      .withColumn(
        "EXT_CC_IDENT",
        expr(
          s"""
             |WITH COMMON_COST_CENTER AS (
             |  SELECT A.COST_CENTER_CODE FROM governed.gmis_hierarchy_cema_cost_center_governed A, governed.input_table B
             |  WHERE
             |    A.COST_CENTER_CODE = B.EXT_CC_IDENT AND AS_OF_DT = '202012311'
             |),
             |PARENT_CODE_FOUND AS (
             |  SELECT DISTINCT A.PARENT_COST_CENTER_CODE FROM governed.gmis_hierarchy_cema_cost_center_governed A
             |  WHERE
             |    A.PARENT_COST_CENTER_CODE IN (SELECT * FROM COMMON_COST_CENTER) AND AS_OF_DT = '20201231'
             |),
             |PARENT_CODE_NOT_FOUND AS (
             |  SELECT A.COST_CENTER_CODE FROM governed.gmis_hierarchy_cema_cost_center_governed A
             |  WHERE
             |    (A.COST_CENTER_CODE IN (SELECT * FROM COMMON_COST_CENTER) AND AS_OF_DT = '20201231')
             |    AND
             |    (A.COST_CENTER_CODE NOT IN (SELECT * FROM PARENT_CODE_FOUND) AND AS_OF_DT = '20201231')
             |),
             |REP_CC_FIND AS (
             |  SELECT A.REP_CC FROM governed.gmis_hierarchy_cema_cost_center_governed A
             |  WHERE
             |    A.COST_CENTER_CODE IN (SELECT * FROM PARENT_CODE_FOUND) AND AS_OF_DT = '20201231' AND A.REP_CC IS NOT NULL
             |),
             |REP_CC_NULL AS (
             |  SELECT A.PARENT_COST_CENTER_CODE FROM governed.gmis_hierarchy_cema_cost_center_governed A
             |  WHERE
             |    A.COST_CENTER_CODE IN (SELECT * FROM PARENT_CODE_FOUND) AND AS_OF_DT = '20201231' AND A.REP_CC IS NULL
             |),
             |REP_CC_NULL_FIND AS (
             |  SELECT A.REP_CC FROM governed.gmis_hierarchy_cema_cost_center_governed A
             |  WHERE
             |    A.COST_CENTER_CODE IN (SELECT * FROM REP_CC_NULL) AND AS_OF_DT = '20201231'
             |),
             |REP_CC_ALL AS (
             |  SELECT * FROM REP_CC_FIND UNION SELECT * FROM REP_CC_NULL_FIND UNION SELECT * FROM PARENT_CODE_NOT_FOUND
             |)
             |SELECT * FROM REP_CC_ALL
             |""".stripMargin)
      )

    modifiedTable.show() // Print the modified table with the join result
    modifiedTable
  }
}

val spark = SparkSession.builder().appName("Example").getOrCreate()
val node = new NodeLevel("show tables")

node.fnNodeLevel()(spark)
