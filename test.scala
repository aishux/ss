import java.time.LocalDate
import java.time.format.DateTimeFormatter
import java.time.temporal.WeekFields
import java.util.Locale

val currentDate = LocalDate.now()

// Extract week number using ISO definition
val weekNumberISO = currentDate.get(WeekFields.ISO.weekOfWeekBasedYear())

// Format week number with leading zeros (e.g., "01", "02", ..., "52")
val formattedWeekNumber = f"$weekNumberISO%02d"

println(s"Formatted Week number (ISO): $formattedWeekNumber")
