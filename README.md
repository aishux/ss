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
      .join(hierarchyDf, inputDf("EXT_CC_IDENT") === hierarchyDf("COST_CENTER_CODE"), "left_outer")
      .withColumn(
        "EXT_CC_IDENT",
        expr(
          s"CASE WHEN EXT_CC_IDENT IN (SELECT DISTINCT PARENT_COST_CENTER_CODE FROM governed.gmis_hierarchy_cema_cost_center_governed WHERE REP_CC IS NOT NULL) THEN REP_CC ELSE (SELECT REP_CC FROM governed.gmis_hierarchy_cema_cost_center_governed WHERE EXT_CC_IDENT = PARENT_COST_CENTER_CODE LIMIT 1) END"
        )
      )

    modifiedTable.show() // Print the modified table with the join result
    modifiedTable
  }
}

val spark = SparkSession.builder().appName("Example").getOrCreate()
val node = new NodeLevel("show tables")

node.fnNodeLevel()(spark)
