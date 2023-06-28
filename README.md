def fnWmbbchMonthlyStandardization()(implicit spark: SparkSession): DataFrame = {
  val hierarchyTable = "governed.gmis_hierarchy_cema_cost_center_governed"
  val inputTable = "governed_gmis_gpc_wmbbch_data"
  val inputDf = spark.table(inputTable)
  val hierarchyDf = spark.table(hierarchyTable)

  def find_rep_cc(costCenterCode: String, parentCostCenterCode: String): String = {
    val tempVariable = parentCostCenterCode

    val repCc = hierarchyDf.filter(hierarchyDf("COST_CENTER_CODE") === tempVariable)
      .select("REP_CC")
      .first()
      .getAs[String]("REP_CC")

    repCc
  }

  val findRepCcUDF = udf(find_rep_cc(_: String, _: String))

  val modifiedTable = scanLatestLoadDate(inputTable)
    .selectExpr(
      // Column selection code
    )
    .withColumn("EXT_CC_IDENT", when(hierarchyDf("REP_CC").isNotNull, hierarchyDf("REP_CC"))
      .otherwise(when(hierarchyDf("REP_CC").isNull, findRepCcUDF(col("EXT_CC_IDENT"), col("PARENT_COST_CENTER_CODE")))
      .otherwise(col("EXT_CC_IDENT"))))

  // Rest of your modifications to the modifiedTable DataFrame

  modifiedTable
}
