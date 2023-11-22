import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.functions._

// Assuming 'spark' is your SparkSession
val spark = SparkSession.builder()
  .appName("JoinAndReplaceExample")
  .getOrCreate()

// Assuming 'timeDf' and 'resultsDF' are your DataFrames
val timeDf: DataFrame = ??? // Replace ??? with your timeDf DataFrame
val resultsDF: DataFrame = ??? // Replace ??? with your resultsDF DataFrame

// Join timeDf and resultsDF based on EXT_MSR_IDENT and EXT_TIM_IDENT columns
val joinedDF = timeDf.join(resultsDF,
  timeDf("EXT_MSR_IDENT") === resultsDF("current_EXT_MSR_IDENT") &&
  timeDf("EXT_TIM_IDENT") === resultsDF("current_EXT_TIM_IDENT"),
  "left_outer"
)

// Replace Amount_USD, Amount_CHF, Amount_GBP columns in timeDf with columns from resultsDF
val updatedTimeDf = joinedDF
  .withColumn("Amount_USD", coalesce(col("AmountUSD"), col("Amount_USD")))
  .withColumn("Amount_CHF", coalesce(col("AmountCHF"), col("Amount_CHF")))
  .withColumn("Amount_GBP", coalesce(col("AmountGBP"), col("Amount_GBP")))
  .drop("AmountUSD", "AmountCHF", "AmountGBP")

// Show the updated timeDf DataFrame
updatedTimeDf.show()
