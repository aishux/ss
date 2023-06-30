import org.apache.spark.sql.functions.expr

def fnWmbbchMonthlyStandardization()(implicit spark: SparkSession): DataFrame = {
  // Existing code...

  val modifiedTable = // Existing code...

  modifiedTable
    .join(hierarchyDf, modifiedTable("EXT_CC_IDENT") === hierarchyDf("COST_CENTER_CODE"), "left_outer")
    .withColumn("EXT_CC_IDENT",
      when(!col("PARENT_COST_CENTER_CODE").contains(modifiedTable("EXT_CC_IDENT")),
        when(hierarchyDf("REP_CC").isNotNull, hierarchyDf("REP_CC"))
          .otherwise(expr("find_rep_cc(COST_CENTER_CODE, PARENT_COST_CENTER_CODE)"))
      )
      .otherwise(modifiedTable("EXT_CC_IDENT"))
    )
    .where(!col("PARENT_COST_CENTER_CODE").contains(modifiedTable("EXT_CC_IDENT")))
}
