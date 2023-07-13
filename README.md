import org.apache.spark.sql.functions._

val opdf = outputdf
  .withColumn("EXT_MSR_IDENT_CODE", col("measure_cd"))
  .filter(col("EXT_MSR_IDENT_CODE").startsWith("AEQ") || col("EXT_MSR_IDENT_CODE").startsWith("BS") || col("EXT_MSR_IDENT_CODE").startsWith("FRS"))
  .withColumn("EXT_GROUP_ACCOUNT_IDENT", col("group_account_cd"))
  .select("EXT_MSR_IDENT_CODE", "EXT_GROUP_ACCOUNT_IDENT")
  .withColumnRenamed("EXT_MSR_IDENT_CODE", "EXT_MSR_IDENT")
  .union(outputdf.select(col("group_account_cd").alias("EXT_MSR_IDENT")))
