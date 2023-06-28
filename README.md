import org.apache.spark.sql.types.StringType

// Rest of your code...

def fnWmbbchMonthlyStandardization()(implicit spark: SparkSession): DataFrame = {
  // Existing code...

  // Function to check if COST_CENTER_CODE is present in PARENT_COST_CENTER_CODE
  def isParentCodePresent(costCenterCode: String, parentCostCenterCode: String): Boolean = {
    val count = hierarchyDf.filter(s"COST_CENTER_CODE = '$parentCostCenterCode' AND PARENT_COST_CENTER_CODE = '$costCenterCode'").count()
    count > 0
  }

  // UDF to apply the check in the when logic
  val isParentCodePresentUDF = udf(isParentCodePresent _)

  val modifiedTable = scanLatestLoadDate(inputTable)
    // other transformations...

    .withColumn("isParentCodePresent", isParentCodePresentUDF(col("COST_CENTER_CODE"), col("PARENT_COST_CENTER_CODE")))
    .withColumn("EXT_CC_IDENT",
      when(col("isParentCodePresent"), col("EXT_CC_IDENT"))
        .otherwise(
          when(hierarchyDf("REP_CC").isNotNull, hierarchyDf("REP_CC"))
            .otherwise(expr("find_rep_cc(COST_CENTER_CODE, PARENT_COST_CENTER_CODE)"))
        )
    )
    .drop("isParentCodePresent")
    // other transformations...

  modifiedTable
}

// Rest of your code...
