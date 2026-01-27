Feature: NSFR Rules Validation

  Scenario: Validate Covid Flag Rules using Rule Expression
    Given I have the rules file at "src/test/resources/nsfr_rules.csv" with delimiter ","
    When I validate the "Covid Flag" rules
    Then the calculation results should match the expected output defined in the rules


package com.ubs.mplifi.stepdefinitions

import io.cucumber.scala.{EN, ScalaDsl}
import org.apache.spark.sql.{DataFrame, Row, SparkSession, functions => F}
import org.apache.spark.sql.types._
import com.ubs.mplifi.calculate.CalcRules
import org.scalatest.matchers.should.Matchers
import scala.collection.mutable.ArrayBuffer

class NsfrRulesSteps extends ScalaDsl with EN with Matchers {

  // Initialize Spark Session (assuming local for testing)
  val spark: SparkSession = SparkSession.builder()
    .appName("NSFR Rules Test")
    .master("local[*]")
    .getOrCreate()

  import spark.implicits._

  var rulesDf: DataFrame = _
  var rulesFilePath: String = _
  var fileDelimiter: String = _
  var validationErrors: ArrayBuffer[String] = ArrayBuffer()

  Given("""I have the rules file at {string} with delimiter {string}""") { (path: String, delimiter: String) =>
    rulesFilePath = path
    fileDelimiter = delimiter
    
    // Load the rules CSV
    rulesDf = spark.read
      .option("header", "true")
      .option("delimiter", delimiter)
      .option("inferSchema", "true")
      .csv(path)
  }

  When("""I validate the {string} rules""") { (ruleSetDesc: String) =>
    // 1. Filter the rules for the specific set
    val targetRules = rulesDf.filter(F.col("ruleSetDesc") === ruleSetDesc).collect()
    
    // 2. Instantiate the Calculator
    val calcRules = new CalcRules()

    // 3. Iterate through each rule to verify it
    targetRules.foreach { ruleRow =>
      val ruleId = ruleRow.getAs[Int]("ruleId")
      val ruleExpr = ruleRow.getAs[String]("ruleExpr")
      val outputExpr = ruleRow.getAs[String]("outputExpression")
      val outputColNamesRaw = ruleRow.getAs[String]("outputColumnNames")
      val outputDataTypesRaw = ruleRow.getAs[String]("outputDatatype")

      // --- Prepare Configuration for calculate_transform ---
      val outCols = outputColNamesRaw.split("~")
      val outTypes = outputDataTypesRaw.split("~")
      
      // Construct outputStructColumns like Seq("COVID_FLAG:STRING", ...)
      val outputStructColumns = outCols.zip(outTypes).map { case (name, dtype) => s"$name:$dtype" }.toSeq
      // outputNewColumns are the final columns we expect in the DF
      val outputNewColumns = outCols.toSeq
      
      // --- Generate Input Data based on ruleExpr ---
      val inputMap = parseRuleExpr(ruleExpr)
      
      // Create a schema and row for the source DataFrame
      // We explicitly add columns found in the rule expression. 
      // In a real scenario, you might need a full schema definition.
      // Here we dynamically build it based on what the rule checks.
      val schemaFields = inputMap.keys.map(k => StructField(k, StringType, true)).toSeq
      val schema = StructType(schemaFields)
      val rowData = Row.fromSeq(inputMap.values.toSeq)
      
      val sourceDf = spark.createDataFrame(
        spark.sparkContext.parallelize(Seq(rowData)),
        schema
      )
      
      // Pass the FULL rules dataframe (filtered) to the engine, 
      // so we also test that the engine picks the correct rule (salience/priority).
      val filteredRulesDf = rulesDf.filter(F.col("ruleSetDesc") === ruleSetDesc)

      // --- Execute the Function ---
      // We pass an empty list for sourceDropColumns as not specified
      val resultDf = calcRules.calculate_transform(
        sourceDf, 
        filteredRulesDf, 
        outputStructColumns, 
        outputNewColumns, 
        Seq.empty[String]
      )

      // --- Verify Output ---
      val resultRow = resultDf.head()
      val expectedValues = parseOutputExpr(outputExpr)

      // Check each expected column
      outCols.zipWithIndex.foreach { case (colName, index) =>
        val actual = Option(resultRow.getAs[String](colName)).getOrElse("")
        val expected = expectedValues.lift(index).getOrElse("").trim
        
        if (actual != expected) {
          validationErrors += s"Rule $ruleId Failed: Column '$colName' -> Expected '$expected', but got '$actual'. (Input: $ruleExpr)"
        }
      }
    }
  }

  Then("""the calculation results should match the expected output defined in the rules""") { () =>
    if (validationErrors.nonEmpty) {
      fail(s"Validation failed with ${validationErrors.length} errors:\n" + validationErrors.mkString("\n"))
    }
  }

  // --- Helper Methods ---

  /**
   * Parses SQL-like rule expressions to extract column-value pairs.
   * Handles:
   * - COL = 'VAL'
   * - COL IN ('V1', 'V2') (Takes V1)
   * - 1=1 (Returns dummy data to avoid matching specific rules if necessary)
   */
  def parseRuleExpr(expr: String): Map[String, String] = {
    if (expr.contains("1=1")) {
      // Return a dummy map or minimal required columns ensuring it DOESN'T match previous specific rules
      // For this specific dataset, specific rules check for 'W011'. 
      // We provide a different value to ensure we hit the default/fallback logic if that's what 1=1 implies.
      return Map("GCR_COMPANY_ID" -> "DUMMY_VAL") 
    }

    val conditions = scala.collection.mutable.Map[String, String]()
    val parts = expr.split(" AND ")

    parts.foreach { part =>
      if (part.contains(" IN ")) {
        // Parse: COL IN ('V1', 'V2')
        val pattern = """(\w+)\s+IN\s+\((.+)\)""".r
        pattern.findFirstMatchIn(part) match {
          case Some(m) => 
            val col = m.group(1)
            val values = m.group(2).split(",").map(_.trim.stripPrefix("'").stripSuffix("'"))
            conditions += (col -> values.head) // Use first value for testing
          case None => // Handle error or ignore
        }
      } else if (part.contains("=")) {
        // Parse: COL = 'VAL'
        val pattern = """(\w+)\s*=\s*'([^']*)'""".r
        pattern.findFirstMatchIn(part) match {
          case Some(m) =>
            conditions += (m.group(1) -> m.group(2))
          case None => 
            // Handle numeric or non-quoted equals if necessary
            val numPattern = """(\w+)\s*=\s*([0-9]+)""".r
            numPattern.findFirstMatchIn(part) match {
              case Some(m) => conditions += (m.group(1) -> m.group(2))
              case None =>
            }
        }
      }
    }
    conditions.toMap
  }

  /**
   * Parses output expression like: Val1', '', 'Val3'
   */
  def parseOutputExpr(expr: String): Seq[String] = {
    // Basic split by comma, then clean up quotes
    // Note: This regex split handles commas inside quotes if needed, 
    // but for the provided simple format, splitting by comma is likely sufficient.
    expr.split(",").map(_.trim.stripPrefix("'").stripSuffix("'"))
  }
}
