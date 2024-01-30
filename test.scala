import org.apache.spark.sql.{Row, SparkSession}
import org.apache.spark.sql.types._
import java.time.LocalDate
import java.time.DayOfWeek
import java.time.format.DateTimeFormatter

// Create a Spark session
val spark = SparkSession.builder().appName("DatePopulation").getOrCreate()

// Define the schema for your DataFrame
val schema = StructType(Seq(
  StructField("col1", StringType, true),
  StructField("col2", StringType, true),
  // ... (continue defining the schema for your other string columns)
  StructField("col17", StringType, true),
  StructField("col18", StringType, true),
  StructField("col19", StringType, true),
  StructField("col20", StringType, true),
  // ... (continue defining the schema for your other double columns)
  StructField("col37", DoubleType, true),
  StructField("col38", DoubleType, true),
  // ... (continue defining the schema for your other columns)
))

// Function to create a DataFrame with the specified values
def createDataFrame(values: Seq[Any]): org.apache.spark.sql.DataFrame = {
  val row = Row.fromSeq(values)
  spark.createDataFrame(Seq(row)).toDF(schema.fieldNames: _*)
}

// Get the current year
val currentYear = LocalDate.now().getYear

// Get the last date of the current year
val lastDateOfYear = LocalDate.of(currentYear, 12, 31)

// Get the last Friday's date of the current year
val lastFridayOfYear = lastDateOfYear.with(DayOfWeek.FRIDAY)

// Values for 'XXX' records
val valuesRecord1 = Seq.fill(16)("XXX") ++ Seq.fill(20)(0.0)
val valuesRecord2 = Seq(lastFridayOfYear.format(DateTimeFormatter.ofPattern("yyyyMMdd"))) ++ Seq.fill(15)("XXX") ++ Seq.fill(20)(0.0)

// Create DataFrames for the two records
val record1DF = createDataFrame(valuesRecord1)
val record2DF = createDataFrame(valuesRecord2)

// Union the two records to create the final DataFrame
val resultDF = record1DF.union(record2DF)

// Show the resulting DataFrame
resultDF.show(false)


val record2Dataset = spark.createDataset(Seq(Row.fromSeq(valuesRecord2))).toDF(schema: _*)
