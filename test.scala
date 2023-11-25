import org.apache.spark.sql.{SparkSession, DataFrame}

// Create SparkSession
val spark = SparkSession.builder().appName("DataFrame Merge").getOrCreate()

// Assuming you have df1 and df2 DataFrames with the given columns

// Perform an outer join without specifying columns
val commonColumns = df1.columns.toSet.intersect(df2.columns.toSet).map(col).toSeq
val mergedDf: DataFrame = df1.select(commonColumns: _*).union(df2.select(commonColumns: _*)).distinct()

// Show the resulting DataFrame
mergedDf.show()
