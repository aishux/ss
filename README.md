import org.apache.spark.sql.DataFrame
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

class NodeLevel(feedType: String) {
  val inputTable = "governed.input_table"
  val hierarchyTable = "governed.gmis_hierarchy_cema_cost_center_governed"
  val outputTable = "governed.output_table"

  def fnNodeLevel(hierarchyDf: DataFrame)(implicit spark: SparkSession): DataFrame = {
    val inputDf = spark.table(inputTable)
    inputDf.show() // Print the contents of the input table

    val modifiedTable = inputDf
      .join(hierarchyDf, inputDf("EXT_CC_IDNET") === hierarchyDf("COST_CENTER_CODE"), "left_outer")
      .withColumn(
        "EXT_CC_IDNET",
        expr(
          s"""
             |CASE
             |  WHEN !PARENT_COST_CENTER_CODE LIKE CONCAT('%', EXT_CC_IDNET, '%')
             |    THEN CASE
             |           WHEN REP_CC IS NOT NULL THEN REP_CC
             |           ELSE (SELECT REP_CC FROM hierarchyDf WHERE COST_CENTER_CODE = PARENT_COST_CENTER_CODE LIMIT 1)
             |         END
             |  ELSE EXT_CC_IDNET
             |END
             |""".stripMargin)
      )
      .drop(hierarchyDf.columns: _*) // Drop columns from the hierarchyDf

    modifiedTable.show() // Print the modified table with the join result
    modifiedTable
  }
}

val spark = SparkSession.builder().appName("Example").getOrCreate()
val node = new NodeLevel("show tables")

// Retrieve the hierarchyDf DataFrame
val hierarchyDf = spark.table("governed.gmis_hierarchy_cema_cost_center_governed")

node.fnNodeLevel(hierarchyDf)(spark)
