import org.apache.spark.sql.functions._
import org.apache.spark.sql.expressions.Window

// Assuming 'mergedDf' is your DataFrame and 'week_date_variable' and 'month_date_variable' are your variables

val windowSpec = Window.partitionBy("ID")

val updatedDf = mergedDf.withColumn("QTD_USD",
  when(col("EXT_TVT_IDENT") === "M" && col("EXT_TIM_IDENT") === month_date_variable,
    coalesce(
      first(when(col("EXT_TVT_IDENT") === "W" && col("EXT_TIM_IDENT") === week_date_variable, col("WEEKLY_TOTAL_AMOUNT_USD")))
        .over(windowSpec),
      col("QTD_USD")
    )
  ).otherwise(col("QTD_USD"))
)

updatedDf.where(col("EXT_MSR_IDENT") === "123").show()
