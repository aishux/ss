import org.apache.spark.sql.{SparkSession, DataFrame}
import org.apache.spark.sql.functions._

// Create a SparkSession
val spark = SparkSession.builder()
  .appName("AddColumnsToTable")
  .getOrCreate()

// Read your SQL table into a DataFrame
val tableName = "prov.abc"
val existingDF = spark.table(tableName)

// Define the column names
val columnNames = (1 to 15).map(i => s"LEVEL$i_WEIGHT")

// Define the default value
val defaultValue = 1

// Create a new DataFrame by adding the columns with default values
var resultDF: DataFrame = existingDF
for (columnName <- columnNames) {
  resultDF = resultDF.withColumn(columnName, lit(defaultValue))
}

// Show the resulting DataFrame
resultDF.show()

// You can optionally save the result back to a new table
// resultDF.write.save("prov.abc_updated")

// Stop the SparkSession when you're done
spark.stop()

