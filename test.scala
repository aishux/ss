import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions._

// Assuming 'df' is your DataFrame containing the provided data

val windowSpec = Window.partitionBy("EXT_MSR_IDENT").orderBy("EXT_TIM_IDENT")

val resultDF = df
  .withColumn("QQ_minus_1", when(col("EXT_TIM_IDENT") === last_day_of_current_month, col("QQ") - 1))
  .withColumn("max_date_QQ_minus_1",
    when(col("EXT_TIM_IDENT") === last_day_of_current_month && col("QQ_minus_1").isNotNull,
      max(when(col("QQ") === col("QQ_minus_1"), col("EXT_TIM_IDENT"))).over(windowSpec))
  )
  .withColumn("YTD_USD",
    when(col("EXT_TIM_IDENT") === last_day_of_current_week, col("TOTAL_WEEK_AMOUNT_USD"))
      .otherwise(lit(0))
    +
    when(
      col("EXT_TIM_IDENT") === last_day_of_current_month,
      coalesce(
        when(col("EXT_TIM_IDENT") === col("max_date_QQ_minus_1"), col("TOTAL_MONTH_AMOUNT_USD")),
        lit(0)
      )
    )
  )
  .withColumn("YTD_USD", when(col("EXT_TIM_IDENT") === last_day_of_current_month, col("YTD_USD")).otherwise(lit(0)))
  .drop("QQ_minus_1", "max_date_QQ_minus_1")
