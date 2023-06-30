import com.ubs.gpc.gmis.transformations.standardization.Standardization
import com.ubs.gpc.gmis.commons.spark.DataframeExtension._
import com.ubs.gpc.gmis.commons.spark.UtilsSpark.JoinType
import org.apache.spark.sql.functions._
import org.apache.spark.sql.{DataFrame, SparkSession}

class GmisFactStandardizationMonthly(feedType: String) extends Standardization {

  // ... (unchanged code)

  def getOutputDf(implicit spark: SparkSession): DataFrame =
    List(fnWmbbchMonthlyStandardization(), fnInsightMonthlyStandardization()).reduce(_ unionAll _)

  override def continue(args: Array[String]): Unit = mainFunc

  def fnWmbbchMonthlyStandardization()(implicit spark: SparkSession): DataFrame = {
    // ... (unchanged code)

    // Apply the logic to replace EXT_CC_IDENT values recursively
    val outputTable = applyLogicToColumn(modifiedTable, hierarchyDf, "EXT_CC_IDENT")

    outputTable
  }

  // Implement the applyLogicToColumn function here
  def applyLogicToColumn(df: DataFrame, hierarchyDf: DataFrame, columnName: String): DataFrame = {
    val tempTable = df
      .join(hierarchyDf, df(columnName) === hierarchyDf("COST_CENTER_CODE"), "left_outer")
      .filter(df("REP_CC").isNull)
      .select(df(columnName).alias("TEMP_CC_IDENT"), hierarchyDf("REP_CC"), hierarchyDf("PARENT_COST_CENTER_CODE"))

    val replacedTable = df
      .join(tempTable, df(columnName) === tempTable("PARENT_COST_CENTER_CODE"), "left_outer")
      .withColumn(columnName, coalesce(tempTable("REP_CC"), df(columnName)))

    val remainingTable = replacedTable.filter(replacedTable("REP_CC").isNull)

    if (remainingTable.count() > 0) {
      applyLogicToColumn(remainingTable, hierarchyDf, columnName)
    } else {
      replacedTable.drop("TEMP_CC_IDENT", "REP_CC", "PARENT_COST_CENTER_CODE")
    }
  }
}
