 val transformedTable = modifiedTable.withColumn("ext_cc_ident", expr("case when length(ext_org_ident) = 6 then substring(ext_org_ident, 3, length(ext_org_ident)-1) when length(ext_org_ident) = 15 then substring(ext_org_ident, 3, 4) end"))

val joinedTable = transformedTable.join(hierarchyDf, transformedTable("ext_cc_ident") === hierarchyDf("COST_CENTER_CODE"), "left_outer")
