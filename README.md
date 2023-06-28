def fnWmbbchMonthlyStandardization()(implicit spark: SparkSession): DataFrame = {
  val hierarchyTable = "governed.gmis_hierarchy_cema_cost_center_governed"
  val inputTable = "governed_gmis_gpc_wmbbch_data"
  val inputDf = spark.table(inputTable)
  val hierarchyDf = spark.table(hierarchyTable)

  // Function to check if COST_CENTER_CODE is present in PARENT_COST_CENTER_CODE
  def isParentCodePresent(costCenterCode: String, parentCostCenterCode: String): Boolean = {
    hierarchyDf.filter(hierarchyDf("COST_CENTER_CODE") === parentCostCenterCode && hierarchyDf("PARENT_COST_CENTER_CODE") === costCenterCode).count() > 0
  }

  // UDF to apply the check in the withColumn logic
  val isParentCodePresentUDF = udf(isParentCodePresent _)

  val modifiedTable = scanLatestLoadDate(inputTable)
    // other transformations...

    .withColumn("EXT_CC_IDENT",
      when(
        col("PARENT_COST_CENTER_CODE").isNull || isParentCodePresentUDF(col("COST_CENTER_CODE"), col("PARENT_COST_CENTER_CODE")),
        when(hierarchyDf("REP_CC").isNotNull, hierarchyDf("REP_CC"))
          .otherwise(expr("find_rep_cc(COST_CENTER_CODE, PARENT_COST_CENTER_CODE)"))
      )
      .otherwise(col("EXT_CC_IDENT"))
    )

    // remaining transformations...

    modifiedTable
}
