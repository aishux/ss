import org.apache.spark.sql.functions._

// Assuming 'mergedDf' is your DataFrame

val variable_name = "20233010" // Your variable containing the date string

val updatedDf = mergedDf.withColumn(
  "YTD_USD",
  when(col("EXT_TVT_IDENT") === "M" && col("EXT_TIM_IDENT") === variable_name,
    col("FINAL_AMOUNT_USD")
  ).otherwise(col("YTD_USD"))
)

updatedDf.show() // Show the updated DataFrame
