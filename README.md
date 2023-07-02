import org.apache.spark.sql.DataFrame
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

class NodeLevel(feedType: String) {
  val inputTable = "governed.input_table"
  val hierarchyTable = "governed.gmis_hierarchy_cema_cost_center_governed"
  val outputTable = "governed.output_table"
  
  def fnNodeLevel()(implicit spark: SparkSession): DataFrame = {
    val inputDf = spark.table(inputTable)
    inputDf.show()  // Print the contents of the input table

    val hierarchyDf = spark.table(hierarchyTable)

    val modifiedTable = inputDf
      .join(hierarchyDf, inputDf("EXT_CC_IDNET") === hierarchyDf("COST_CENTER_CODE"), "left_outer")
      .withColumn("EXT_CC_IDNET",
        when(!col("PARENT_COST_CENTER_CODE").contains(inputDf("EXT_CC_IDNET")),
          when(hierarchyDf("REP_CC").isNotNull, hierarchyDf("REP_CC"))
            .otherwise(
              hierarchyDf.filter(col("COST_CENTER_CODE") === col("PARENT_COST_CENTER_CODE"))
                .select("REP_CC")
                .first()
                .getAs[String]("REP_CC")
            )
        )
        .otherwise(inputDf("EXT_CC_IDNET"))
      )
      .select(inputDf.columns.map(col): _*) // Select only the columns from the inputDf

    modifiedTable.show() // Print the modified table with the join result
    modifiedTable
  }
}

val spark = SparkSession.builder().appName("Example").getOrCreate()
val node = new NodeLevel("show tables")
node.fnNodeLevel()(spark)
