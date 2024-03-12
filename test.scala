val joinConditions = orgCols.map(orgCol =>
      col("b.access_object") === orgCol ||
        expr(s"CONCAT('CA-', b.access_object)") === orgCol
    )

    // Dynamically construct the join condition
    val joinCondition = joinConditions.reduce(_ || _)
