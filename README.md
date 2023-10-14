import org.apache.spark.sql.{SparkSession, Row}
import org.apache.spark.sql.types.{StructType, StructField, StringType}

val strFlattenValueWoheader: String = strFlattenValue.substring(strFlattenValue.indexOf(System.getProperty("line.separator")) + 1).toString

// Split the lines into arrays of values
val lines = strFlattenValueWoheader.lines.map(line => line.split(","))

// Determine the number of columns (assuming it's the maximum among all rows)
val numColumns = lines.map(_.length).max

// Create a Spark Session
val spark = SparkSession.builder().appName("DynamicDataFrame").getOrCreate()

// Define a schema with the appropriate number of StringType columns
val schema = StructType((1 to numColumns).map(i => StructField(s"col$i", StringType, true)))

// Create a Row RDD from the lines
val rowRDD = spark.sparkContext.parallelize(lines.map(cols => Row(cols: _*)))

// Create the DataFrame with the specified schema
val tempCSVData = spark.createDataFrame(rowRDD, schema)

// Now, tempCSVData is a DataFrame with columns named col1, col2, col3, etc., without specifying the column names explicitly.
