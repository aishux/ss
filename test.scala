import org.apache.spark.sql.functions._

// Assuming `timeDf` is a DataFrame

// Filtering based on conditions
val filteredDF = timeDf
  .filter(col("QQ") === 4)
  .filter(col("ext_tim_ident").isin(timeDf.select(max("ext_tim_ident")).collect(): _*))

// Displaying the filtered DataFrame
filteredDF.show()
