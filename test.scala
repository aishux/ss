import org.apache.spark.sql.functions._
import org.apache.spark.sql.expressions.Window

// Define the Window specification
val windowSpec = Window.partitionBy("CC", "MSR")

// Assuming df is your DataFrame
val resultDF = df.withColumn("Z", max(col("A")).over(windowSpec)).filter(col("DATE") === "20241231")

resultDF.show()
