// 1. We use Regex syntax: ([^"]*)
// 2. We explicitly match the comma AND the space
// 3. I corrected 'headoption' to 'headOption' (Scala is case sensitive)

Then("""^the output should be "([^"]*)", "([^"]*)", "([^"]*)"$""") { (v1: String, v2: String, v3: String) =>
  outputRows.headOption.map(_.toSeq.map(_.toString)) shouldBe Some(Seq(v1, v2, v3))
}
