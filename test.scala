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


###########

from pyspark.sql.functions import col, when

# Assuming 'to' column represents the currency
# Assuming 'ex_rate' column represents the exchange rate

# Define the exchange rate for CHF
chf_exchange_rate = df.select("ex_rate").filter(col("to") == "chf").collect()[0][0]

# Create a new column 'EXC_RATE_CHF'
df = df.withColumn("EXC_RATE_CHF", col("ex_rate") / when(col("to") == "chf", chf_exchange_rate).otherwise(1))
