import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

val spark = SparkSession.builder.appName("DefaultColumn").getOrCreate()
import spark.implicits._

// Sample DataFrame
val data = Seq(
  (1, "oldA"),
  (2, "oldA")
).toDF("id", "A")

// Perform transformation on column "A" and add column "B" if it doesn't exist
val columns = data.columns

val resultDF = data
  .withColumn("A", lit("A"))
  .withColumn("B", when(lit(columns.contains("B")), col("B")).otherwise(lit("XYZ")))

// Display the result
resultDF.show()
