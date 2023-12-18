import org.apache.spark.sql.{SparkSession, DataFrame}
import org.apache.spark.sql.functions._

// Assuming you already have a SparkSession created
val spark = SparkSession.builder().appName("UpdateValuesExample").getOrCreate()

// Assuming 'df' is your DataFrame
val df: DataFrame = // ... your DataFrame creation or retrieval

// Define a function to update values when CHILD_CODE is 'CA-GEBO'
def updateValues(childCode: String, parentCode: String, derivedPK: String): (String, String) => String = {
  (cc: String, pc: String) =>
    if (cc == childCode) {
      derivedPK // New value for DERIVED_PK when CHILD_CODE is 'CA-GEBO'
    } else {
      pc // Keep the existing value for PARENT_CODE
    }
}

// Define the values to update
val newParentCode = "new_parent_value"
val newDerivedPK = "new_derived_pk_value"

// Update the values based on the condition CHILD_CODE = 'CA-GEBO'
val updatedDF = df.withColumn("PARENT_CODE", when(col("CHILD_CODE") === "CA-GEBO", lit(newParentCode)).otherwise(col("PARENT_CODE")))
  .withColumn("DERIVED_PK", when(col("CHILD_CODE") === "CA-GEBO", lit(newDerivedPK)).otherwise(col("DERIVED_PK")))

// Show the updated DataFrame
updatedDF.show()
