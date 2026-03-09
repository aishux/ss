Then("""^Residual Tenor output should contain:$""") { dataTable: io.cucumber.datatable.DataTable =>
  import scala.jdk.CollectionConverters._
  import org.apache.spark.sql.functions.col

  val expectedRows = dataTable.asMaps().asScala.map(_.asScala.toMap).toList
  
  // 1. Identify exactly which columns the test cares about (e.g., LCR_RESIDUAL_TENOR)
  val targetCols = expectedRows.head.keys.toSeq

  // 2. STRICTLY select only the target columns. 
  // This bypasses NEW_RESIDUAL_TNR_DAYS and prevents Catalyst from crashing.
  val safeDF = outputDF.select(targetCols.map(c => col(c).cast("string")): _*)

  // Optional Debug: This is now safe because the corrupted column is excluded
  safeDF.show(false)

  // 3. Collect and map exactly like before
  val actualRows = safeDF.collect().map { row =>
    targetCols.map { colName =>
      val value = row.getAs[String](colName)
      (colName, Option(value).getOrElse(""))
    }.toMap
  }.toList

  val normalizedExpectedRows = expectedRows.map { row =>
    row.map { case (k, v) => (k, if (v == null || v == "null") "" else v) }
  }

  normalizedExpectedRows.foreach { expectedRow =>
    actualRows should contain (expectedRow)
  }
}
