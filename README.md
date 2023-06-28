def isParentCodePresent(costCenterCode: String, parentCostCenterCode: String): Boolean = {
    val count = hierarchyDf.filter(s"COST_CENTER_CODE = '$parentCostCenterCode' AND PARENT_COST_CENTER_CODE = '$costCenterCode'").count()
    count > 0
  }
