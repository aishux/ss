import org.apache.spark.sql.functions._

// Step 1: Renaming and filtering measure_cd column
val step1DF = outputdf
  .withColumn("EXT_MSR_IDENT", col("measure_cd"))
  .filter(col("EXT_MSR_IDENT").startsWith("AEQ") || col("EXT_MSR_IDENT").startsWith("BS") || col("EXT_MSR_IDENT").startsWith("FRS"))
  .drop("measure_cd")

// Step 2: Vertically stack group_account_cd under EXT_MSR_IDENT
val opdf = step1DF
  .union(outputdf.select(col("group_account_cd").alias("EXT_MSR_IDENT")))
  .select("EXT_MSR_IDENT")
