// UDF to apply the check in the when logic
  val isParentCodePresentUDF = udf((costCenterCode: String, parentCostCenterCode: String) =>
    isParentCodePresent(costCenterCode, parentCostCenterCode)
  )


  
