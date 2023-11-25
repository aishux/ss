import org.apache.spark.sql.{SparkSession, functions}
import org.apache.spark.sql.expressions.Window

// Create a SparkSession
val spark = SparkSession.builder()
  .appName("Calculate Total USD")
  .master("local[*]")
  .getOrCreate()

// Sample data
val data = Seq(
  ("ABC", 20230131, "M", 10),
  // ... (your complete dataset)
  ("XYZ", 20231231, "M", 20)
)

import spark.implicits._

// Create a DataFrame from the provided data
val df = data.toDF("EXT_MSR_IDENT", "EXT_TIM_IDENT", "EXT_TVT_IDENT", "AMOUNT_USD")
  .withColumn("EXT_TIM_IDENT", $"EXT_TIM_IDENT".cast("int"))

// Calculate the total USD for each EXT_MSR_IDENT up to the current month
val windowSpec = Window.partitionBy("EXT_MSR_IDENT").orderBy("EXT_TIM_IDENT").rowsBetween(Window.unboundedPreceding, Window.currentRow)

val result = df
  .withColumn("TOTAL_USD_CURR_MONTH", functions.sum($"AMOUNT_USD").over(windowSpec))
  .orderBy("EXT_MSR_IDENT", "EXT_TIM_IDENT")

result.show()
