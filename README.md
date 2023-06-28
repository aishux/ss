.withColumn("EXT_CC_IDENT", when(
      !isParentCodePresentUDF(col("COST_CENTER_CODE").cast(StringType), col("PARENT_COST_CENTER_CODE").cast(StringType)),
      when(hierarchyDf("REP_CC").isNotNull, hierarchyDf("REP_CC"))
        .otherwise(expr("find_rep_cc(COST_CENTER_CODE, PARENT_COST_CENTER_CODE)"))
    ).otherwise(col("EXT_CC_IDENT")))
