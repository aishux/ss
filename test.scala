import java.time.LocalDate
import java.time.temporal.WeekFields
import java.util.Locale

val currentDate = LocalDate.now()

// Extract current month
val currentMonth = currentDate.getMonthValue
print(s"Current month: $currentMonth\n")

// Extract week number using ISO definition
val weekNumberISO = currentDate.get(WeekFields.ISO.weekOfWeekBasedYear())
print(s"Week number (ISO): $weekNumberISO\n")

// Define a Locale for Zurich, Switzerland (German-speaking part)
val zurichLocale = new Locale("de", "CH") // Language: German, Country: Switzerland

// Extract week number using custom definition (e.g., Zurich Locale)
val weekNumberZurich = currentDate.get(WeekFields.of(zurichLocale).weekOfWeekBasedYear())
print(s"Week number (Custom, Zurich Locale): $weekNumberZurich\n")
