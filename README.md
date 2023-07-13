import org.apache.spark.sql.functions._

val opdf = outputdf
  .filter(col("measure_cd").startsWith("AEQ") || col("measure_cd").startsWith("BS") || col("measure_cd").startsWith("FRS"))
  .withColumn("EXT_MSR_IDENT", col("measure_cd"))
  .union(outputdf.select(col("group_account_cd").alias("EXT_MSR_IDENT")))
