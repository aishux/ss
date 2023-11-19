import java.time.LocalDate
import java.time.format.DateTimeFormatter
import java.time.temporal.WeekFields
import java.util.Locale

// Set a specific date (January 1st)
val specificDate = LocalDate.of(2023, 1, 1)

// Extract week number using ISO definition
val weekNumberISO = specificDate.get(WeekFields.ISO.weekOfWeekBasedYear())

// Format week number with leading zeros (e.g., "01", "02", ..., "52")
val formattedWeekNumber = f"$weekNumberISO%02d"

println(s"Formatted Week number (ISO) for January 1st: $formattedWeekNumber")
