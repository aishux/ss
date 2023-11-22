import org.apache.spark.sql.functions._

// Assuming `timeDf` is a DataFrame

// Filtering based on conditions
val filteredDF = timeDf
  .filter(col("QQ") === 4)
  .filter(to_date(col("ext_tim_ident"), "yyyyMMdd").cast("string") <= "2023-11-24")

// Displaying the filtered DataFrame
filteredDF.show()
