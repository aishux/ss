val trendTable = spark.table(outputTable)
  .withColumn("ext_tim_ident", expr("date_format(last_day(to_Date(ext_tim_ident, 'yyyyMMdd')), 'yyyyMMdd')"))

