def find_rep_cc(costCenterCode: String, parentCostCenterCode: String): String = {
    val tempVariable = parentCostCenterCode

    val repCc = hierarchyDf.filter(hierarchyDf("COST_CENTER_CODE") === tempVariable)
      .select("REP_CC")
      .first()
      .getAs[String]("REP_CC")

    repCc
  }

  val findRepCcUDF = spark.udf.register("find_rep_cc", find_rep_cc(_: String, _: String))
