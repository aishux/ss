import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

// Create a SparkSession
val spark = SparkSession.builder()
  .appName("Calculate Cumulative Sum")
  .master("local[*]")
  .getOrCreate()

import spark.implicits._

// Sample DataFrame
val data = Seq(
  ("ABC", "20230131", "M", 10),
  ("ABC", "20230228", "M", 10),
  // Add other rows here
  ("XYZ", "20231130", "M", 20),
  ("XYZ", "20231231", "M", 20)
)

val df = data.toDF("EXT_MSR_IDENT", "EXT_TIM_IDENT", "EXT_TVT_IDENT", "AMOUNT_USD")

// Convert 'EXT_TIM_IDENT' column to date type
val dateFormat = "yyyyMMdd"
val dfFormatted = df.withColumn("EXT_TIM_IDENT", to_date($"EXT_TIM_IDENT", dateFormat))

// Self-join to calculate cumulative sum
val cumulativeSumDF = dfFormatted.as("df1")
  .join(
    dfFormatted.as("df2"),
    ($"df1.EXT_MSR_IDENT" === $"df2.EXT_MSR_IDENT") && ($"df1.EXT_TIM_IDENT" >= $"df2.EXT_TIM_IDENT"),
    "left_outer"
  )
  .groupBy($"df1.EXT_MSR_IDENT", $"df1.EXT_TIM_IDENT", $"df1.EXT_TVT_IDENT", $"df1.AMOUNT_USD")
  .agg(sum($"df2.AMOUNT_USD").alias("TOTAL_USD_CURR_MONTH"))
  .orderBy($"df1.EXT_MSR_IDENT", $"df1.EXT_TIM_IDENT")

cumulativeSumDF.show()
