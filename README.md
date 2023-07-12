import org.apache.spark.sql.functions._

val updatedDF = originalDF
  .withColumn("EXT_MSR_IDENT", $"measure_cd")
  .union(originalDF.filter($"group_account_cd".startsWith("AEQ") || $"group_account_cd".startsWith("BS") || $"group_account_cd".startsWith("FRS"))
    .withColumn("EXT_MSR_IDENT", $"group_account_cd"))
  .select("EXT_MSR_IDENT")
