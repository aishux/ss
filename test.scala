import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions._
import org.apache.spark.sql.DataFrame

// Sample DataFrame creation (replace this with your actual DataFrame)
val data = Seq(
  ("ABC", 20230131, "M", 1, 10),
  // ... (insert the rest of your data)
  ("XYZ", 20231124, "W", 4, 5)
)

val columns = Seq("EXT_MSR_IDENT", "EXT_TIM_IDENT", "EXT_TVT_IDENT", "QQ", "AMOUNT_USD")

val df = data.toDF(columns: _*)

// Convert 'EXT_TIM_IDENT' to DateType
val formattedDF = df.withColumn("EXT_TIM_IDENT", to_date($"EXT_TIM_IDENT".cast("string"), "yyyyMMdd"))

// Filter data where 'EXT_TVT_IDENT' = 'M' and 'EXT_TIM_IDENT' like '%2023%'
val filteredDF = formattedDF.filter($"EXT_TVT_IDENT" === "M" && $"EXT_TIM_IDENT".like("%2023%"))

// Define Window specification partitioned by 'EXT_MSR_IDENT' and 'QQ'
val windowSpec = Window.partitionBy("EXT_MSR_IDENT", "QQ").orderBy("EXT_TIM_IDENT")

// Create a new column with the running total for each 'QQ' partition
val resultDF = filteredDF.withColumn("TOTAL_WEEK_AMOUNT_USD", sum("AMOUNT_USD").over(windowSpec))

// Show the resulting DataFrame
resultDF.show()
