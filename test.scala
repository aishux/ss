import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

// Create SparkSession
val spark = SparkSession.builder()
  .appName("AddColumnExample")
  .getOrCreate()

// Sample data
val data = Seq(
  ("USD", "CHF", 1.158),
  ("USD", "EUR", 1.08),
  ("USD", "GBP", 1.266),
  ("USD", "USD", 1.00)
)

// Create DataFrame
val df = spark.createDataFrame(data).toDF("FROM", "TO", "EX_RT")

// Filter rows where TO column is 'CHF'
val chfValue = df.filter(col("TO") === "CHF").select("EX_RT").collect()(0)(0)

// Add new column with constant value
val resultDF = df.withColumn("EX_RT_CHF", lit(chfValue))

// Show result
resultDF.show()


#######

import org.apache.spark.sql.functions._

// Group by ID and get the CHF value for each group
val chfValues = df.groupBy("ID").agg(first(when(col("TO") === "CHF", col("EX_RT"))).alias("EX_RT_CHF"))

// Join the original DataFrame with the calculated CHF values
val resultDF = df.join(chfValues, Seq("ID"), "left")

// Show result
resultDF.show()

#######

SELECT t1.A, t1.B, t1.C, t1.D, t1.E, t1.F, t1.G, t2.F AS J
FROM Temp1 AS t1
LEFT JOIN (
    SELECT A, B, C, G, F
    FROM Temp1
    WHERE D = 'CHF' AND E = 'USD'
) AS t2
ON t1.A = t2.A AND t1.B = t2.B AND t1.C = t2.C AND t1.G = t2.G;
