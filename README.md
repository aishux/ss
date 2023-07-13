import org.apache.spark.sql.functions._

val opdf = outputdf
  .withColumn("EXT_MSR_IDENT", col("measure_cd"))
  .union(outputdf.withColumn("EXT_MSR_IDENT", col("group_account_cd")))
  .drop("measure_cd", "group_account_cd")
  .filter(when(col("EXT_MSR_IDENT").startsWith("AEQ"), true)
    .when(col("EXT_MSR_IDENT").startsWith("BS"), true)
    .when(col("EXT_MSR_IDENT").startsWith("FRS"), true)
    .otherwise(false))
