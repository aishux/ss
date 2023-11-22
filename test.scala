import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.functions._

// Get the current month as an integer (1 to 12)
val currentMonth = LocalDate.now().getMonthValue

// Calculate the quarter based on the current month
val currentQuarter = (currentMonth - 1) / 3 + 1

println(s"The current quarter is: $currentQuarter")

// Create a function to perform the required operations
def calculateSumAmounts(dataFrame: DataFrame, year: String): (Double, Double, Double) = {
  val filteredDF1 = dataFrame
    .filter(col("EXT_MSR_IDENT") === "CA123")
    .filter(col("EXT_TIM_DETAIL").like("%" + year + "%")) // Use the 'year' variable in the filter
    .filter(col("EXT_TVT_IDENT") === "M")
    .filter(col("QQ") < 4)

  val filteredDF2 = dataFrame
    .filter(col("EXT_MSR_IDENT") === "CA123")
    .filter(col("EXT_TIM_DETAIL").like("%" + year + "%")) // Use the 'year' variable in the filter
    .filter(col("EXT_TVT_IDENT") === "W")
    .filter(col("QQ") === 4)
    .filter(col("EXT_TIM_IDENT") <= s"$year-11-14") // Use the 'year' variable in the filter

  // Check if any filtered DataFrame is empty, return (0, 0, 0) for sum amounts
  if (filteredDF1.isEmpty || filteredDF2.isEmpty) {
    return (0.0, 0.0, 0.0)
  }

  // Calculate the sum of AMOUNT_USD, AMOUNT_CHF, AMOUNT_GBP columns for the filtered rows
  val sumAmountUSD = if (filteredDF1.agg(sum("AMOUNT_USD")).head.isNullAt(0)) 0.0 else filteredDF1.agg(sum("AMOUNT_USD")).head.getDouble(0)
  val sumAmountCHF = if (filteredDF1.agg(sum("AMOUNT_CHF")).head.isNullAt(0)) 0.0 else filteredDF1.agg(sum("AMOUNT_CHF")).head.getDouble(0)
  val sumAmountGBP = if (filteredDF1.agg(sum("AMOUNT_GBP")).head.isNullAt(0)) 0.0 else filteredDF1.agg(sum("AMOUNT_GBP")).head.getDouble(0)

  val sumAmountUSD2 = if (filteredDF2.agg(sum("AMOUNT_USD")).head.isNullAt(0)) 0.0 else filteredDF2.agg(sum("AMOUNT_USD")).head.getDouble(0)
  val sumAmountCHF2 = if (filteredDF2.agg(sum("AMOUNT_CHF")).head.isNullAt(0)) 0.0 else filteredDF2.agg(sum("AMOUNT_CHF")).head.getDouble(0)
  val sumAmountGBP2 = if (filteredDF2.agg(sum("AMOUNT_GBP")).head.isNullAt(0)) 0.0 else filteredDF2.agg(sum("AMOUNT_GBP")).head.getDouble(0)

  // Return the sum of amounts for both conditions
  (sumAmountUSD + sumAmountUSD2, sumAmountCHF + sumAmountCHF2, sumAmountGBP + sumAmountGBP2)
}

// Assuming 'spark' is your SparkSession and 'yourDataFrame' is the DataFrame
val spark = SparkSession.builder()
  .appName("CalculateSumAmountsExample")
  .getOrCreate()

// Assuming 'yourDataFrame' is the DataFrame you mentioned
val yourDataFrame = ???

val yearValue = "2023" // Define the year value

// Calculate the sum of AMOUNT_USD, AMOUNT_CHF, AMOUNT_GBP columns based on the specified criteria and year
val (sumUSD, sumCHF, sumGBP) = calculateSumAmounts(yourDataFrame, yearValue)

// Display the calculated sums
println(s"The sum of AMOUNT_USD for the filtered rows is: $sumUSD")
println(s"The sum of AMOUNT_CHF for the filtered rows is: $sumCHF")
println(s"The sum of AMOUNT_GBP for the filtered rows is: $sumGBP")
