val modifiedTable = scanLatestLoadDate(inputTable)
  .selectExpr(
    "substr(TIME_STAMP_START, 1, 6) AS ext_tim_ident",
    "EXT_SPL_IDENT AS ext_spl_ident",
    "EXT_ORG_ID AS ext_org_ident",
    "EXT_SIT_ID AS ext_sit_ident",
    "EXT_BSG_ID AS ext_bsg_ident",
    "'EXT_PRD_ID AS ext_prd_ident",
    "EXT_MND_ID AS ext_mnd_ident",
    "EXT_MS_ID AS ext_msr_ident",
    "EXT_PSG_ID AS ext_psg_ident",
    "EXT_NAT_ID AS ext_nat_ident",
    "AMOUNT_CHF",
    "AMOUNT_USD"
  )
  .withColumn("ext_spl_ident", expr("substring(ext_spl_ident, 3, length(ext_spl_ident) - 1)"))
  .standardizeCol(dfDateMap, "ext_tim_ident", "Cob_Date_with_year_month", col("COB_DATE_STR"), JoinType.INNER)
  .standardizeCol(df_wmbbch_org_hierarchy, "ext_org_ident", "source_code")
  .standardizeCol(df_wmbbch_sit_hierarchy, "ext_sit_ident", "source_code", expr(s"substring($target_code, 3, length($target_code) - 1)"))
  .standardizeCol(df_wmbbch_bsg_hierarchy, "ext_bsg_ident", "source_code", expr(s"substring($target_code, 3, length($target_code) - 1)"))
  .standardizeCol(df_wmbbch_prd_hierarchy, "ext_prd_ident", "source_code")
  .standardizeCol(df_wmbbch_mnd_hierarchy, "ext_mnd_ident", "source_code")
  .standardizeCol(df_wmbbch_msr_hierarchy, "ext_msr_ident", "source_code", coalesce(col("target_code"), col("ext_msr_ident")))
  .standardizeCol(df_wmbbch_psg_hierarchy, "ext_psg_ident", "source_code", expr(s"substring(target_code, 3, length(target_code) - 1)"))
  .standardizeCol(df_wmbbch_nat_hierarchy, "ext_nat_ident", "source_code", expr(s"substring(target_code, 3, length(target_code) - 1)"))
  .withColumn(
    "ext_cc_ident",
    expr("case when length(ext_org_ident) = 6 then substring(ext_org_ident, 3, length(ext_org_ident) - 1) when length(ext_org_ident) = 15 then substring(ext_org_ident, 3, 4) end")
  )
  .join(hierarchyDf, modifiedTable("ext_cc_ident") === hierarchyDf("COST_CENTER_CODE"), "left_outer")
  .withColumn("ext_cc_ident", when(hierarchyDf("REP_CC").isNotNull, hierarchyDf("REP_CC")).otherwise(modifiedTable("ext_cc_ident")))
  .withColumn("EXT_ORG_ID", when(hierarchyDf("REP_CC").isNotNull, hierarchyDf("REP_CC")).otherwise(modifiedTable("EXT_ORG_ID")))

modifiedTable
