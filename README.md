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
    "ext_tim_ident", "ext_spl_ident", "ext_cc_ident", "ext_ca_ident",
    "ext_sit_ident", "ext_bsg_ident", "ext_prd_ident", "ext_mnd_ident",
    "ext_msr_ident", "ext_ucc_ident", "ext_psg_ident", "ext_nat_ident"
  )

  def getOutputDf(implicit spark: SparkSession): DataFrame =
    List(fnWmbbchMonthlyStandardization(), fnInsightMonthlyStandardization()).reduce(_ unionAll _)

  override def continue(args: Array[String]): Unit = mainFunc

  def fnWmbbchMonthlyStandardization()(implicit spark: SparkSession): DataFrame = {
    val hierarchyTable = "governed.gmis_hierarchy_cema_cost_center_governed"
    val inputTable = "governed_gmis_gpc_wmbbch_data"
    val inputDf = spark.table(inputTable)
    val hierarchyDf = spark.table(hierarchyTable)
    // new
    val joinedDf = inputDf.join(hierarchyDf, inputDf("EXT_CC_IDENT") === hierarchyDf("COST_CENTER_CODE"), "left_outer")

    val modifiedTable = scanLatestLoadDate(inputTable)
      .selectExpr(
        "substr(TIME_STAMP_START, 1, 6) as EXT_TIM_IDENT",
        "EXT_SPL_IDENT as EXT_SPL_IDENT",
        "EXT_ORG_ID as EXT_ORG_IDENT",
        "EXT_SIT_ID as EXT_SIT_IDENT",
        "EXT_BSG_ID as EXT_BSG_IDENT",
        "'EXT_PRD_ID as EXT_PRD_IDENT",
        "EXT_MND_ID as EXT_MND_IDENT",
        "EXT_MS_ID as EXT_MSR_IDENT",
        "EXT_PSG_ID as EXT_PSG_IDENT",
        "EXT_NAT_ID as EXT_NAT_IDENT",
        "AMOUNT_CHF",
        "AMOUNT_USD"
      )
      .withColumn("EXT_SPL_IDENT", expr("substring(EXT_SPL_IDENT, 3, length(EXT_SPL_IDENT)-1)"))
      .standardizeCol(dfDateMap, "EXT_TIM_IDENT", "Cob_Date_with_year_month", col("COB_DATE_STR"), JoinType.INNER)
      .standardizeCol(df_wmbbch_org_hierarchy, "ext_org_ident", "source_code")
      .standardizeCol(df_wmbbch_sit_hierarchy, "ext_sit_ident", "source_code", expr(s"substring($target_code, 3, length($target_code)-1)"))
      .standardizeCol(df_wmbbch_bsg_hierarchy, "ext_bsg_ident", "source_code", expr(s"substring($target_code, 3, length($target_code)-1)"))
      .standardizeCol(df_wmbbch_prd_hierarchy, "ext_prd_ident", "source_code")
      .standardizeCol(df_wmbbch_mnd_hierarchy, "ext_mnd_ident", "source_code")
      .standardizeCol(df_wmbbch_msr_hierarchy, "ext_msr_ident", "source_code", coalesce(col(target_code), col(ext_msr_ident)))
      .standardizeCol(df_wmbbch_psg_hierarchy, "ext_psg_ident", "source_code", expr(s"substring($target_code, 3, length($target_code)-1)"))
      .standardizeCol(df_wmbbch_nat_hierarchy, "ext_nat_ident", "source_code", expr(s"substring($target_code, 3, length($target_code)-1)"))
      .withColumn("ext_cc_ident", expr("case when length(ext_org_ident) = 6 then substring(ext_org_ident, 3, length(ext_org_ident)-1) when length(ext_org_ident) = 15 then substring(ext_org_ident, 3, 4) end"))
    	//write code here
    
    .where(expr("EXT_CC_IDENT IN select distinct level14_code from provision.gwm_wmpc-hier_cema_cost_center_tgt_cema where as_of.dt in (select max(as_of_Dt) from provision.gwm_wmpc-hier-cema_cost_center_tgt_cema where CAST (as_of_dt AS DECIMAL) IS NOT NULL) and Level2-gers_node in ('N14951'))"))

    modifiedTable.withColumn("ext_cc_ident", when(hierarchyDf("REP_CC").isNotNull, hierarchyDf("REP_CC")).otherwise(modifiedTable("ext_cc_ident")))

    modifiedTable
  }
}
