import org.apache.spark.sql.functions._

// Assuming `timeDf` is a DataFrame

// Calculate the last date of the current week
val currentDate = java.time.LocalDate.now()
val currentDayOfWeek = currentDate.getDayOfWeek.getValue
val daysUntilEndOfWeek = java.time.DayOfWeek.SUNDAY.getValue - currentDayOfWeek
val lastDateOfCurrentWeek = currentDate.plusDays(daysUntilEndOfWeek)
val formattedDate = lastDateOfCurrentWeek.format(java.time.format.DateTimeFormatter.ofPattern("yyyyMMdd"))

// Filtering based on conditions
val filteredDF = timeDf
  .filter(col("QQ") === 4)
  .filter(to_date(col("ext_tim_ident"), "yyyyMMdd").cast("string") <= formattedDate)

// Displaying the filtered DataFrame
filteredDF.show()
