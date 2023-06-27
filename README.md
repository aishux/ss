import com.ubs.gpc.gmis.transformations.standardization.Standardization
import com.ubs.gpc.gmis.commons.spark.DataframeExtension._
import com.ubs.gpc.gmis.commons.spark.UtilsSpark.JoinType
import org.apache.spark.sql.functions._
import org.apache.spark.sql.{DataFrame, SparkSession}

class GmisFactStandardizationMonthly(feedType: String) extends Standardization {

  override val job_id: String = getJobId(feedType)
  override val feed_type: String = feedType
  override val step: String = "GMIS_FAST_MONTHLY_STANDARDIZATION"
  override val targetTable: String = "governed_gmis_gpc_all_fact"

  override protected val aggregationKeys: List[String] = List(
    "ext_tim_ident", "ext_spl_ident", "ext_cc_ident", "ext_ca_ident", "ext_sit_ident",
    "ext_bsg_ident", "ext_prd_ident", "ext_mnd_ident", "ext_msr_ident",
    "ext_ucc_ident", "ext_psg_ident", "ext_nat_ident"
  )

  def getOutputDf(implicit spark: SparkSession): DataFrame =
    List(fnWmbbchMonthlyStandardization(), fnInsightMonthlyStandardization()).reduce(_ unionAll _)

  override def continue(args: Array[String]): Unit = mainFunc

  def fnWmbbchMonthlyStandardization()(implicit spark: SparkSession): DataFrame = {

    val hierarchyTable = "governed.gmis_hierarchy_cema_cost_center_governed"
    val inputTable = "governed_gmis_gpc_wmbbch_data"

    val inputDf = spark.table(inputTable)
    val hierarchyDf = spark.table(hierarchyTable)

    val modifiedTable = scanLatestLoadDate(inputTable)
      .selectExpr(
        "substr(TIME_STAMP_START, 1, 6) as ext_tim_ident",
        "ext_spl_ident",
        "ext_org_id as ext_cc_ident",
        "ext_sit_id as ext_sit_ident",
        "ext_bsg_id as ext_bsg_ident",
        "ext_prd_id as ext_prd_ident",
        "ext_mnd_id as ext_mnd_ident",
        "ext_ms_id as ext_msr_ident",
        "ext_psg_id as ext_psg_ident",
        "ext_nat_id as ext_nat_ident",
        "AMOUNT_CHF",
        "AMOUNT_USD"
      )
      .withColumn("ext_spl_ident", expr("substring(ext_spl_ident, 3, length(ext_spl_ident)-1)"))
      .standardizeCol(dfDateMap, "ext_tim_ident", "Cob_Date_with_year_month", col("COB_DATE_STR"), JoinType.INNER)
      .standardizeCol(df_wmbbch_org_hierarchy, "ext_cc_ident", "source_code")
      .standardizeCol(df_wmbbch_sit_hierarchy, "ext_sit_ident", "source_code", expr("substring(target_code, 3, length(target_code)-1)"))
      .standardizeCol(df_wmbbch_bsg_hierarchy, "ext_bsg_ident", "source_code", expr("substring(target_code, 3, length(target_code)-1)"))
      .standardizeCol(df_wmbbch_prd_hierarchy, "ext_prd_ident", "source_code")
      .standardizeCol(df_wmbbch_mnd_hierarchy, "ext_mnd_ident", "source_code")
      .standardizeCol(df_wmbbch_msr_hierarchy, "ext_msr_ident", "source_code", coalesce(col("target_code"), col("ext_msr_ident")))
      .standardizeCol(df_wmbbch_psg_hierarchy, "ext_psg_ident", "source_code", expr("substring(target_code, 3, length(target_code)-1)"))
      .standardizeCol(df_wmbbch_nat_hierarchy, "ext_nat_ident", "source_code", expr("substring(target_code, 3, length(target_code)-1)"))
      .withColumn("ext_cc_ident", expr("case when length(ext_org_id) = 6 then substring(ext_org_id, 3, length(ext_org_id)-1) when length(ext_org_id) = 15 then substring(ext_org_id, 3, 4) end"))
      .join(hierarchyDf, scanLatestLoadDate(inputTable)("ext_cc_ident") === hierarchyDf("COST_CENTER_CODE"), "left_outer")
      .withColumn("ext_cc_ident", when(hierarchyDf("REP_CC").isNotNull, hierarchyDf("REP_CC")).otherwise(scanLatestLoadDate(inputTable)("ext_cc_ident")))

    modifiedTable
  }

  def fnInsightMonthlyStandardization()(implicit spark: SparkSession): DataFrame = {
    val inputTable = "governed_gmis_gpc_insight_data"
    scanLatestLoadDate(inputTable)
      .withColumn("ext_cc_ident", lit("EXT_CC_IDENT")) // Placeholder code, replace with actual logic
  }
}
