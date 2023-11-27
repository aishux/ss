import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions._

// Assuming 'mergedDf' is your DataFrame

val windowSpec = Window.partitionBy("EXT_MSR_IDENT").orderBy("EXT_TIM_IDENT")

val updatedDf = mergedDf.withColumn(
  "QTD_USD",
  when(col("EXT_TIM_IDENT") === "20231130",
    last(when(col("EXT_TIM_IDENT") === "20231124", col("YTD_USD")), ignoreNulls = true).over(windowSpec)
  ).otherwise(col("QTD_USD"))
)

updatedDf.show()
