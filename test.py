From line 34-68 try replacing with this:


// 1. Define columns and target types (Keep your existing definition)
val allColumnsWithTypes = Seq(
  "REGION_CODE" -> StringType,
  "SAP_FUNCTIONAL_AREA_CODE" -> StringType,
  "GCR_REGULATORY_PRODUCT_TYPE" -> StringType,
  "NEW_RESIDUAL_TNR_DAYS" -> IntegerType
)
val allColumns = allColumnsWithTypes.map(_._1)

// 2. Read rows from Cucumber (Keep your existing definition)
val rows = dataTable.asMaps().asScala.map(_.asScala.toMap).toList

// 3. Build data purely as Strings (REMOVE the manual v.toInt logic)
val data = rows.map { row =>
  allColumns.map(colName => row.getOrElse(colName, null))
}

// 4. Create an ALL-STRING schema for the initial load
val stringSchema = StructType(allColumns.map(name => StructField(name, StringType, nullable = true)))

// 5. Create the raw DataFrame natively as Strings
DataDF = spark.createDataFrame(
  spark.sparkContext.parallelize(data.map(Row.fromSeq)),
  stringSchema
)

// 6. Let Spark natively cast the columns to their target types
allColumnsWithTypes.foreach { case (colName, dataType) =>
  if (dataType != StringType) {
    DataDF = DataDF.withColumn(colName, col(colName).cast(dataType))
  }
}

// Optional Debug: Verify the native casting worked
DataDF.printSchema()
DataDF.show(false)
