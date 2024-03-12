val resultDF = your_table_name
  .groupBy(
    col("ACCESS_OBJECT"),
    col("LEVEL1"),
    col("LEVEL2"),
    col("LEVEL3"),
    col("SYSTEM_CODE")
  )
  .agg(
    max(when(col("SYSTEM_CODE") === "VU1", concat_ws(";", collect_set("EMAIL")))).alias("VU1_EMAILS"),
    max(when(col("SYSTEM_CODE") === "VW3", concat_ws(";", collect_set("EMAIL")))).alias("VW3_EMAILS")
  )

// Show the result
resultDF.show()
