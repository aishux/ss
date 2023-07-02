import org.apache.spark.sql.DataFrame
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

class NodeLevel(feedType: String) {
  val inputTable = "governed.input_table"
  val hierarchyTable = "governed.gmis_hierarchy_cema_cost_center_governed"
  
  def fnNodeLevel()(implicit spark: SparkSession): DataFrame = {
    val inputDf = spark.table(inputTable)
    inputDf.show()  // Print the contents of the input table
    inputDf
  }
}

val spark = SparkSession.builder().appName("Example").getOrCreate()
val node = new NodeLevel("show tables")
node.fnNodeLevel()(spark)
