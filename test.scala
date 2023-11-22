import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.functions._

// Create a function to perform the required operations
def calculateSumAmount(dataFrame: DataFrame): Double = {
  val filteredDF = dataFrame
    .filter(col("EXT_MSR_IDENT") === "CA123")
    .filter(col("EXT_TIM_DETAIL").like("%2023%"))
    .filter(col("EXT_TVT_IDENT") === "M")
    .filter(col("QQ") < 4)

  // Calculate the sum of the AMOUNT_USD column for the filtered rows
  val sumAmount = filteredDF.agg(sum("AMOUNT_USD")).collect()(0).getDouble(0)

  sumAmount
}

// Assuming 'spark' is your SparkSession and 'yourDataFrame' is your DataFrame
val spark = SparkSession.builder()
  .appName("CalculateSumAmountExample")
  .getOrCreate()

// Assuming 'yourDataFrame' is the DataFrame you mentioned
val yourDataFrame = ???

// Calculate the sum of AMOUNT_USD column based on the specified criteria
val sumOfAmount = calculateSumAmount(yourDataFrame)

// Display the calculated sum
println(s"The sum of AMOUNT_USD for the filtered rows is: $sumOfAmount")
