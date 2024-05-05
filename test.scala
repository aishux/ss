import org.apache.spark.sql.{SparkSession, DataFrame}
import org.apache.spark.sql.functions._

// Create SparkSession
val spark = SparkSession.builder()
  .appName("ExchangeRateCalculator")
  .getOrCreate()

// Sample data
val data = Seq(
  ("USD", "CHF", 1.158),
  ("USD", "EUR", 1.08),
  ("USD", "GBP", 1.266),
  ("USD", "USD", 1.0)
)

// Create DataFrame
val df = spark.createDataFrame(data).toDF("FROM", "TO", "EXCHANGE_RATE")

// Create a new DataFrame with exchange rates for CHF
val chfRates = df.filter($"TO" === "CHF").withColumn("EXCHANGE_RATE_CHF", $"EXCHANGE_RATE").select("FROM", "EXCHANGE_RATE_CHF")

// Join the original DataFrame with the CHF rates DataFrame
val result = df.join(chfRates, df("TO") === lit("CHF"), "left")
  .withColumn("EXCHANGE_RATE_CHF", $"EXCHANGE_RATE" / $"EXCHANGE_RATE_CHF")
  .drop("TO", "EXCHANGE_RATE_CHF")

// Show the result
result.show()
