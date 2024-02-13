import org.apache.spark.sql.functions.{col, expr}

// Assuming df is your DataFrame
val dfWithIntMonth = df.withColumn("month_number_int", col("month_number").cast("int"))

// Remove leading zeros from the integer month column
val dfCleanedMonth = dfWithIntMonth.withColumn("month_number_int", expr("lpad(month_number_int, 2, '0')"))

// If you prefer using regexp_replace:
// val dfCleanedMonth = dfWithIntMonth.withColumn("month_number_int", expr("regexp_replace(month_number_int, '^0+', '')"))

dfCleanedMonth.show()
