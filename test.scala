import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.functions._
import java.time.LocalDate
import java.time.format.DateTimeFormatter

// Assuming 'spark' is your SparkSession and 'inputDF' is your DataFrame
val spark: SparkSession = ??? // Replace ??? with your SparkSession
val inputDF: DataFrame = ??? // Replace ??? with your input DataFrame

// Get the current month's last date in the format 'yyyyMMdd'
val currentDate = LocalDate.now()
val lastDayOfMonth = currentDate.withDayOfMonth(currentDate.lengthOfMonth())
val formattedLastDayOfMonth = lastDayOfMonth.format(DateTimeFormatter.ofPattern("yyyyMMdd"))

// Define a new DataFrame by updating 'AMOUNT_USD' column based on the condition
val outputDF = inputDF
  .withColumn("AMOUNT_USD", when(col("EXT_TIM_IDENT") === formattedLastDayOfMonth, col("YTD_USD") - col("AMOUNT_USD")).otherwise(col("AMOUNT_USD"))
  )

outputDF.show()
