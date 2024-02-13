import org.apache.spark.sql.functions.{col, expr}

// Assuming df is your DataFrame
val dfWithTempA = df.withColumn("month_number_int", col("month_number").cast("int"))
                     .withColumn("temp_a", expr("annual_ytd / 12 * (3 + month_number_int)"))

dfWithTempA.show()
