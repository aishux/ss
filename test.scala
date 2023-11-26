import org.apache.spark.sql.functions._
import org.apache.spark.sql.DataFrame

// Assuming 'inputDF' is your DataFrame containing the provided data

val quarter = 4
val QQ_MINUS_1 = 3

// Calculate the maximum date when QQ_MINUS_1 matches EXT_TVT_IDENT using when and withColumn
val resultDF = inputDF.withColumn(
  "max_date",
  when(col("QQ") === QQ_MINUS_1 && col("EXT_TVT_IDENT") === quarter, max("EXT_TIM_IDENT").over())
    .otherwise(null) // Set to null if conditions are not met
)

resultDF.show() // Display the DataFrame with the new 'max_date' column
