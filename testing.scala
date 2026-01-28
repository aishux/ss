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
