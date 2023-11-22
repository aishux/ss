import org.apache.spark.sql.functions._

val timeDetailDf: DataFrame = ??? // Replace ??? with your timeDetailDf DataFrame
val resultsDF: DataFrame = ??? // Replace ??? with your resultsDF DataFrame

val joinedDF = timeDetailDf.join(
  resultsDF
    .withColumn("formatted_EXT_TIM_IDENT", date_format(col("current_EXT_TIM_IDENT"), "yyyyMMdd")),
  timeDetailDf("EXT_MSR_IDENT") === resultsDF("current_EXT_MSR_IDENT") &&
    timeDetailDf("EXT_TIM_IDENT") === col("formatted_EXT_TIM_IDENT"),
  "left_outer"
)

val updatedTimeDetailDf = joinedDF
  .withColumn("YTD_USD", coalesce(resultsDF("AmountUSD"), timeDetailDf("YTD_USD")))
  .withColumn("YTD_EUR", coalesce(resultsDF("AmountEUR"), timeDetailDf("YTD_EUR")))
  .withColumn("YTD_GBP", coalesce(resultsDF("AmountGBP"), timeDetailDf("YTD_GBP")))
  .withColumn("YTD_CHF", coalesce(resultsDF("AmountCHF"), timeDetailDf("YTD_CHF")))
  .drop("AmountUSD", "AmountEUR", "AmountGBP", "AmountCHF", "formatted_EXT_TIM_IDENT")

updatedTimeDetailDf.show()
