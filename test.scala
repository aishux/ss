import org.apache.spark.sql.functions._
import org.apache.spark.sql.{DataFrame, Row}

protected def fnAbc(): DataFrame = {
  // Your existing code...

  // Assuming UdfDate.fnGenerateR() returns a Seq
  val seqGenerateR: Seq[(String, String, String, String, String, String, String, String)] = UdfDate.fnGenerateR()

  // Convert the Seq to a DataFrame
  val dfGenerateR = spark.createDataFrame(seqGenerateR).toDF(
    "col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8"
  )

  val trendTableWithHierarchy = trendTable
    .withColumn("HIERARCHY_MERGED", getReportingateHier(col(ext_tim_ident), col(ext_tvt_ident)))
    .withColumn("HIERARCHY_MERGED", explode(col("HIERARCHY_MERGED")))
    .select(
      col("HIERARCHY_MERGED.LEVEL1_CODE"),
      col("HIERARCHY_MERGED.LEVEL1_DESC"),
      col("HIERARCHY_MERGED.LEVEL1_WT"),
      col("HIERARCHY_MERGED.LEVEL2_CODE"),
      col("HIERARCHY_MERGED.LEVEL2_DESC"),
      col("HIERARCHY_MERGED.LEVEL2_WT"),
      col("HIERARCHY_MERGED.LEVEL3_CODE"),
      col("HIERARCHY_MERGED.LEVEL3_DESC"),
      col("HIERARCHY_MERGED.LEVEL3_WT"),
      lit("kyvos_gwm").alias("HIERARCHY_TYPE")
    )

  // Union with the output of fnGenerateR
  val resultDF = dfGenerateR.union(trendTableWithHierarchy)

  // Additional operations if needed...

  resultDF
}
