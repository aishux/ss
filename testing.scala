// 1. We use Regex syntax: ([^"]*)
// 2. We explicitly match the comma AND the space
// 3. I corrected 'headoption' to 'headOption' (Scala is case sensitive)

Then("""^the output should be "([^"]*)", "([^"]*)", "([^"]*)"$""") { (v1: String, v2: String, v3: String) =>
  outputRows.headOption.map(_.toSeq.map(_.toString)) shouldBe Some(Seq(v1, v2, v3))
}


Then("""^the output should be "([^"]*)", "([^"]*)", "([^"]*)"$""") { (v1: String, v2: String, v3: String) =>
  val actualOpt = Option(outputRows).flatMap(_.headOption).map { row =>
    row.toSeq.map(e => java.lang.String.valueOf(e))
  }
  actualOpt shouldBe Some(Seq(v1, v2, v3))
}


Then("""^the output should be "([^"]*)", "([^"]*)", "([^"]*)"$""") {
  (v1: String, v2: String, v3: String) =>

    val row = outputRows.headOption.getOrElse(fail("No output rows produced"))

    val actual = outputRows.headOption.map(_.toSeq.take(3).map(e => Option(e).map(_.toString).getOrElse("")))

    actual shouldBe Some(Seq(v1, v2, v3))
}


System.err.println(s"DEBUG: DataFrame Schema: ${df.schema.treeString}")



Then("""^the output should be "([^"]*)", "([^"]*)", "([^"]*)"$""") {
  (v1: String, v2: String, v3: String) =>

    val row = outputRows.headOption.getOrElse(fail("No output rows produced"))

    val actual = Seq(
      row.getAs[String]("COVID_FLAG"),
      row.getAs[String]("AdjTenorDate"),
      row.getAs[String]("NSFRR_REASON_CODE")
    )

    actual shouldBe Seq(v1, v2, v3)
}



Then("""^the output should be "([^"]*)", "([^"]*)", "([^"]*)"$""") {
  (v1: String, v2: String, v3: String) =>

    val actual = outputRows.headOption.map { row => row.toSeq.takeRight(3).map(e => Option(e).map(_.toString).getOrElse("")) }

    actual shouldBe Some(Seq(v1, v2, v3))
}


Then("""^the output should be "([^"]*)", "([^"]*)", "([^"]*)"$""") {
  (v1: String, v2: String, v3: String) =>

    val row = outputRows.headOption.getOrElse(fail("No output rows produced"))

    // 1. Get the Main Struct (COVID_FLAG) as a ROW, not a String
    val covidFlagStruct = row.getAs[Row]("COVID_FLAG")

    // 2. Get the Nested 'result' Struct as a ROW
    // We use Option() to handle cases where 'result' might be null
    val actualValues = Option(covidFlagStruct.getAs[Row]("result")) match {
      case Some(res) => 
        Seq(
          String.valueOf(res.getAs[Any]("COVID_FLAG")),        // Extract nested COVID_FLAG
          String.valueOf(res.getAs[Any]("AdjTenorDate")),      // Extract nested AdjTenorDate
          String.valueOf(res.getAs[Any]("NSFRR_REASON_CODE"))  // Extract nested NSFRR_REASON_CODE
        )
      case None => 
        // Handle case where result struct itself is null
        Seq("null", "null", "null") 
    }

    // 3. Compare
    actualValues shouldBe Seq(v1, v2, v3)
}
