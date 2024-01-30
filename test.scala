import java.time.{LocalDate, DayOfWeek, DateTimeFormatter}
import java.time.temporal.TemporalAdjusters

// Get the current year
val currentYear = LocalDate.now().getYear

// Get the last day of the current year
val lastDayOfYear = LocalDate.of(currentYear, 12, 31)
val formattedLastDayOfYear = lastDayOfYear.format(DateTimeFormatter.ofPattern("yyyyMMdd"))

// Get the last Friday's date of the current year
val lastFridayOfYear = lastDayOfYear.with(TemporalAdjusters.previous(DayOfWeek.FRIDAY))
val formattedLastFridayOfYear = lastFridayOfYear.format(DateTimeFormatter.ofPattern("yyyyMMdd"))

// Print the results
println(s"Last day of current year: $formattedLastDayOfYear")
println(s"Last Friday of current year: $formattedLastFridayOfYear")
