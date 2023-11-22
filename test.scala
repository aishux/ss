import java.time.LocalDate
import java.time.DayOfWeek
import java.time.format.DateTimeFormatter

// Get the current date
val currentDate = LocalDate.now()

// Get the day of the week (e.g., Monday to Sunday -> 1 to 7)
val currentDayOfWeek = currentDate.getDayOfWeek().getValue()

// Calculate the number of days until the end of the week (Sunday)
val daysUntilEndOfWeek = DayOfWeek.SUNDAY.getValue() - currentDayOfWeek

// Calculate the last date of the current week
val lastDateOfCurrentWeek = currentDate.plusDays(daysUntilEndOfWeek)

// Format the last date of the current week to YYYYMMDD
val formattedDate = lastDateOfCurrentWeek.format(DateTimeFormatter.ofPattern("yyyyMMdd"))

println(formattedDate) // Output: YYYYMMDD format of the last date of the current week
