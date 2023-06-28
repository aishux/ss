.withColumn("EXT_CC_IDENT",
      when(
        isParentCodePresentUDF(col("COST_CENTER_CODE"), col("PARENT_COST_CENTER_CODE")).equalTo(lit(false)),
        when(hierarchyDf("REP_CC").isNotNull, hierarchyDf("REP_CC"))
          .otherwise(expr("find_rep_cc(COST_CENTER_CODE, PARENT_COST_CENTER_CODE)"))
      )
      .otherwise(col("EXT_CC_IDENT"))
