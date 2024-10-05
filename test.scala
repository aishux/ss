import org.apache.spark.sql.functions._
import org.apache.spark.sql.SparkSession
import java.time.{LocalDate, YearMonth}
import java.time.format.DateTimeFormatter

// Create a SparkSession
val spark = SparkSession.builder.appName("DateExplode").getOrCreate()
import spark.implicits._

// Sample data
val data = Seq(
  ("20030430", "20031130", 1),
  ("20040131", "20061231", 1)
).toDF("VALID_FROM", "VALID_TO", "ID")

// UDF to generate a sequence of months with the last day between two dates
val generateMonthsLastDay = udf((startDateStr: String, endDateStr: String) => {
  val formatter = DateTimeFormatter.ofPattern("yyyyMMdd")
  val startDate = LocalDate.parse(startDateStr, formatter).withDayOfMonth(1)
  val endDate = LocalDate.parse(endDateStr, formatter).withDayOfMonth(1)

  // Generate a sequence of months between the two dates, but using the last day of each month
  Iterator.iterate(startDate)(_.plusMonths(1))
    .takeWhile(!_.isAfter(endDate))
    .map(date => {
      val yearMonth = YearMonth.of(date.getYear, date.getMonthValue)
      yearMonth.atEndOfMonth().format(formatter) // Get last day of each month
    })
    .toSeq
})

// Apply the UDF and explode the sequence
val result = data
  .withColumn("Month", explode(generateMonthsLastDay(col("VALID_FROM"), col("VALID_TO"))))
  .select("ID", "Month")

// Show the result
result.show(false)
