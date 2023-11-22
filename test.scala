import org.apache.spark.sql.functions._

// Assuming 'timeDetailDf' and 'resultsDF' are your DataFrames
val timeDetailDf: DataFrame = ??? // Replace ??? with your timeDetailDf DataFrame
val resultsDF: DataFrame = ??? // Replace ??? with your resultsDF DataFrame

val joinedDF = timeDetailDf.join(
  resultsDF,
  timeDetailDf("EXT_MSR_IDENT") === resultsDF("current_EXT_MSR_IDENT") &&
    timeDetailDf("EXT_TIM_IDENT") === resultsDF("current_EXT_TIM_IDENT"),
  "left_outer"
)

val updatedTimeDetailDf = joinedDF
  .withColumn("YTD_USD", when(resultsDF("AmountUSD").isNotNull, resultsDF("AmountUSD")).otherwise(timeDetailDf("YTD_USD")))
  .withColumn("YTD_EUR", when(resultsDF("AmountEUR").isNotNull, resultsDF("AmountEUR")).otherwise(timeDetailDf("YTD_EUR")))
  .withColumn("YTD_GBP", when(resultsDF("AmountGBP").isNotNull, resultsDF("AmountGBP")).otherwise(timeDetailDf("YTD_GBP")))
  .withColumn("YTD_CHF", when(resultsDF("AmountCHF").isNotNull, resultsDF("AmountCHF")).otherwise(timeDetailDf("YTD_CHF")))
  .drop("AmountUSD", "AmountEUR", "AmountGBP", "AmountCHF")

updatedTimeDetailDf.show()
