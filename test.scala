import java.time.LocalDate
import java.time.format.DateTimeFormatter

// Get the current date
val currentDate = LocalDate.now()

// Get the last day of the current month
val lastDayOfMonth = currentDate.withDayOfMonth(currentDate.lengthOfMonth())

// Format the last day of the current month to yyyymmdd format
val formatter = DateTimeFormatter.ofPattern("yyyyMMdd")
val formattedLastDay = lastDayOfMonth.format(formatter)

// Print the formatted last day of the current month
println(s"The last day of the current month in yyyymmdd format is: $formattedLastDay")
