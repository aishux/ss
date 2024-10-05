import org.apache.spark.sql.functions._
import java.time.{LocalDate, YearMonth}
import java.time.format.DateTimeFormatter
import org.apache.spark.sql.SparkSession

// Create a SparkSession
val spark = SparkSession.builder.appName("DateConversion").getOrCreate()

import spark.implicits._

// Sample data
val data = Seq(
  ("20030401"),
  ("20040101")
).toDF("VALID_FROM")

// UDF to convert date to last day of month
val convertToLastDay = udf((dateStr: String) => {
  val formatter = DateTimeFormatter.ofPattern("yyyyMMdd")
  val parsedDate = LocalDate.parse(dateStr, formatter)
  val year = parsedDate.getYear
  val month = parsedDate.getMonthValue
  val lastDayOfMonth = YearMonth.of(year, month).atEndOfMonth()
  lastDayOfMonth.format(formatter)
})

// Apply the UDF to the DataFrame
val result = data.withColumn("VALID_FROM", convertToLastDay(col("VALID_FROM")))

// Show the result
result.show(false)
