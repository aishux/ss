import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.functions._

// Create a function to perform the required operations
def calculateSumAmounts(dataFrame: DataFrame): (Double, Double, Double) = {
  val filteredDF = dataFrame
    .filter(col("EXT_MSR_IDENT") === "CA123")
    .filter(col("EXT_TIM_DETAIL").like("%2023%"))
    .filter(col("EXT_TVT_IDENT") === "M")
    .filter(col("QQ") < 4)

  // Calculate the sum of AMOUNT_USD, AMOUNT_CHF, AMOUNT_GBP columns for the filtered rows
  val sumAmountUSD = filteredDF.agg(sum("AMOUNT_USD")).collect()(0).getDouble(0)
  val sumAmountCHF = filteredDF.agg(sum("AMOUNT_CHF")).collect()(0).getDouble(0)
  val sumAmountGBP = filteredDF.agg(sum("AMOUNT_GBP")).collect()(0).getDouble(0)

  (sumAmountUSD, sumAmountCHF, sumAmountGBP)
}

// Assuming 'spark' is your SparkSession and 'yourDataFrame' is your DataFrame
val spark = SparkSession.builder()
  .appName("CalculateSumAmountsExample")
  .getOrCreate()

// Assuming 'yourDataFrame' is the DataFrame you mentioned
val yourDataFrame = ???

// Calculate the sum of AMOUNT_USD, AMOUNT_CHF, AMOUNT_GBP columns based on the specified criteria
val (sumUSD, sumCHF, sumGBP) = calculateSumAmounts(yourDataFrame)

// Display the calculated sums
println(s"The sum of AMOUNT_USD for the filtered rows is: $sumUSD")
println(s"The sum of AMOUNT_CHF for the filtered rows is: $sumCHF")
println(s"The sum of AMOUNT_GBP for the filtered rows is: $sumGBP")
