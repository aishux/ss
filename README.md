import org.apache.spark.sql.functions._

// Rest of your code...

def fnWmbbchMonthlyStandardization()(implicit spark: SparkSession): DataFrame = {
  // Existing code...

  // Function to check if COST_CENTER_CODE is present in PARENT_COST_CENTER_CODE
  def isParentCodePresent(costCenterCode: String, parentCostCenterCode: String): Boolean = {
    val count = hierarchyDf.filter(s"COST_CENTER_CODE = '$parentCostCenterCode' AND PARENT_COST_CENTER_CODE = '$costCenterCode'").count()
    count > 0
  }

  // UDF to apply the check in the when logic
  val isParentCodePresentUDF = udf((costCenterCode: String, parentCostCenterCode: String) =>
    isParentCodePresent(costCenterCode, parentCostCenterCode)
  )

  val modifiedTable = scanLatestLoadDate(inputTable)
    // other transformations...

    .withColumn("EXT_CC_IDENT",
      when(
        !isParentCodePresentUDF(col("COST_CENTER_CODE").cast(StringType), col("PARENT_COST_CENTER_CODE").cast(StringType)),
        when(hierarchyDf("REP_CC").isNotNull, hierarchyDf("REP_CC"))
          .otherwise(expr("find_rep_cc(COST_CENTER_CODE, PARENT_COST_CENTER_CODE)"))
      )
      .otherwise(col("EXT_CC_IDENT"))
    )
    // other transformations...

  modifiedTable
}

// Rest of your code...
