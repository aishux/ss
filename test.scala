import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

object YearlyToMonthly {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .appName("YearlyToMonthly")
      .getOrCreate()

    import spark.implicits._

    // Sample data
    val data = Seq(
      ("202301", 23456),
      ("2024", 6000),
      ("2021", 12000)
    )

    val df = data.toDF("REPORTING_DATE", "AMOUNT")

    // Create a UDF to split yearly data into monthly data
    val splitYearlyToMonthly = udf((year: String, amount: Int) => {
      if (year.length == 4) {
        val yearInt = year.toInt
        (1 to 12).map { month =>
          f"$yearInt%04d$month%02d" -> amount / 12
        }
      } else {
        Seq(year -> amount)
      }
    })

    // Apply the UDF and explode the array of tuples
    val result = df.withColumn("monthly_data", explode(splitYearlyToMonthly($"REPORTING_DATE", $"AMOUNT")))

    // Select and rename columns
    val finalResult = result.select($"monthly_data._1".as("REPORTING_DATE"), $"monthly_data._2".as("AMOUNT"))

    // Show the resulting DataFrame
    finalResult.show()
  }
}
