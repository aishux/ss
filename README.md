import org.apache.spark.sql.functions._
import spark.implicits._

// Step 1: Filter measure_cd column and rename it to EXT_MSR_IDENT_CODE
val step1DF = outputdf
  .filter(col("measure_cd").startsWith("AEQ") || col("measure_cd").startsWith("BS") || col("measure_cd").startsWith("FRS"))
  .withColumn("EXT_MSR_IDENT_CODE", col("measure_cd"))
  .drop("measure_cd", "group_account_cd")

// Step 2: Create DataFrame with EXT_MSR_IDENT column from group_account_cd
val step2DF = outputdf
  .select(col("group_account_cd").alias("EXT_MSR_IDENT"))

// Step 3: Union step1DF and step2DF
val opdf = step1DF.union(step2DF)
