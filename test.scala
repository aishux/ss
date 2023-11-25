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

// Group by 'EXT_MSR_IDENT' and 'EXT_TVT_IDENT' and calculate cumulative sum
val windowSpec = Window.partitionBy("EXT_MSR_IDENT", "EXT_TVT_IDENT").orderBy("EXT_TIM_IDENT")
val cumulativeSumDF = dfFormatted
  .withColumn("TOTAL_USD_CURR_MONTH", sum("AMOUNT_USD").over(windowSpec))

// Display cumulativeSumDF with filters
display(cumulativeSumDF.filter($"EXT_TVT_IDENT" === "M" && $"EXT_MSR_IDENT" === "ABC"))
