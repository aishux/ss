// Note the added commas between the {string} placeholders
Then("""the output should be "{string}", "{string}", "{string}" """) { (v1: String, v2: String, v3: String) =>
  outputRows.headOption.map(_.toSeq.map(_.toString)) shouldBe Some(Seq(v1, v2, v3))
}
