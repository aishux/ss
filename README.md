 import org.apache.spark.sql.functions._
import org.apache.spark.sql.{DataFrame, SparkSession}

class GmisFactStandardizationMonthly(feedType: String) extends Standardization {

  // Existing code...

  def fnWmbbchMonthlyStandardization()(implicit spark: SparkSession): DataFrame = {
    // Existing code...

    val modifiedTable = // Existing code...

    val modifiedTableWithCC = modifiedTable
      .join(hierarchyDf, modifiedTable("EXT_CC_IDENT") === hierarchyDf("COST_CENTER_CODE"), "left_outer")
      .withColumn("EXT_CC_IDENT",
        when(
          col("PARENT_COST_CENTER_CODE").contains(modifiedTable("EXT_CC_IDENT")),
          modifiedTable("EXT_CC_IDENT")
        ).otherwise(
          when(hierarchyDf("REP_CC").isNotNull, hierarchyDf("REP_CC"))
            .otherwise(
              hierarchyDf.filter(col("COST_CENTER_CODE") === col("PARENT_COST_CENTER_CODE"))
                .select("REP_CC")
                .first()
                .getAs[String]("REP_CC")
            )
        )
      )
      .where(!col("PARENT_COST_CENTER_CODE").contains(col("EXT_CC_IDENT")))

    modifiedTableWithCC
  }
}
