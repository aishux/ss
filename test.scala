import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

// Create SparkSession
val spark = SparkSession.builder()
  .appName("Currency Conversion")
  .config("spark.master", "local")
  .getOrCreate()

// Create DataFrame for Adj_Mapping
val adjMappingData = Seq(
  (20240131, "M", "USD", 100),
  (20240131, "M", "USD", 200),
  (20240131, "M", "USD", 300),
  (20240131, "W", "USD", 100)
).toDF("EXT_TIM_IDENT", "EXT_TVT_IDENT", "REPORTING_CURRENCY", "AMOUNT")

// Create DataFrame for FX_Rate
val fxRateData = Seq(
  (20240131, "MONTHLY", "USD", "CHF", 1.158),
  (20240131, "MONTHLY", "USD", "EUR", 1.08),
  (20240131, "MONTHLY", "USD", "GBP", 1.266),
  (20240131, "MONTHLY", "USD", "USD", 1.00)
).toDF("COB_DATE", "PERIODICITY", "TO", "FROM", "EXCHANGE_RATE")

// Join the two DataFrames
val joinedDF = adjMappingData.join(
  fxRateData,
  ($"EXT_TIM_IDENT" === $"COB_DATE") &&
  ($"EXT_TVT_IDENT" === lit("M")) &&
  ($"REPORTING_CURRENCY" === $"TO")
)

// Apply currency conversion
val convertedDF = joinedDF.withColumn("AMOUNT_CHF", when($"FROM" === "CHF", $"AMOUNT" / $"EXCHANGE_RATE"))
  .withColumn("AMOUNT_EUR", when($"FROM" === "EUR", $"AMOUNT" / $"EXCHANGE_RATE"))
  .withColumn("AMOUNT_GBP", when($"FROM" === "GBP", $"AMOUNT" / $"EXCHANGE_RATE"))
  .withColumn("AMOUNT_USD", when($"FROM" === "USD", $"AMOUNT" / $"EXCHANGE_RATE"))

// Select relevant columns
val resultDF = convertedDF.select("EXT_TIM_IDENT", "EXT_TVT_IDENT", "REPORTING_CURRENCY", "AMOUNT",
  "AMOUNT_CHF", "AMOUNT_EUR", "AMOUNT_GBP", "AMOUNT_USD")

###############################################################################################################


import org.apache.spark.sql.functions._

// Perform join
val joinedDF = adjMappingData.join(
  fxRateData,
  ($"EXT_TIM_IDENT" === $"COB_DATE") &&
  ($"EXT_TVT_IDENT" === lit("M")) &&
  ($"REPORTING_CURRENCY" === $"TO") &&
  ($"FROM".isin("USD", "EUR", "GBP", "CHF"))
)

// Apply currency conversion and pivot
// Apply currency conversion and pivot
val convertedDF = joinedDF
  .withColumn("CONVERTED_AMOUNT", $"AMOUNT" / $"EXCHANGE_RATE")
  .groupBy(joinedDF.columns.map(col): _*) // Group by all columns
  .pivot("FROM", Seq("USD", "EUR", "GBP", "CHF"))
  .agg(first("CONVERTED_AMOUNT"))

// Select relevant columns
val resultDF = convertedDF.select(
  $"EXT_TIM_IDENT", $"EXT_TVT_IDENT", $"REPORTING_CURRENCY", $"AMOUNT",
  $"USD".alias("AMOUNT_USD"), $"EUR".alias("AMOUNT_EUR"),
  $"GBP".alias("AMOUNT_GBP"), $"CHF".alias("AMOUNT_CHF")
)

// Show the result
resultDF.show()

// Show the result
resultDF.show()
