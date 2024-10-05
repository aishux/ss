import org.apache.spark.sql.functions._
import org.apache.spark.sql.SparkSession
import java.time.LocalDate
import java.time.format.DateTimeFormatter
import org.apache.spark.sql.expressions.Window

// Create a SparkSession
val spark = SparkSession.builder.appName("DateExplode").getOrCreate()
import spark.implicits._

// Sample data
val data = Seq(
  ("20030430", "20031130", 1),
  ("20040131", "20061231", 1)
).toDF("VALID_FROM", "VALID_TO", "ID")

// UDF to generate a sequence of months between two dates
val generateMonths = udf((startDateStr: String, endDateStr: String) => {
  val formatter = DateTimeFormatter.ofPattern("yyyyMMdd")
  val startDate = LocalDate.parse(startDateStr, formatter).withDayOfMonth(1)
  val endDate = LocalDate.parse(endDateStr, formatter).withDayOfMonth(1)

  // Generate a sequence of months between the two dates
  Iterator.iterate(startDate)(_.plusMonths(1))
    .takeWhile(!_.isAfter(endDate))
    .map(_.format(formatter))
    .toSeq
})

// Apply the UDF and explode the sequence
val result = data
  .withColumn("Month", explode(generateMonths(col("VALID_FROM"), col("VALID_TO"))))
  .select("ID", "Month")

// Show the result
result.show(false)
