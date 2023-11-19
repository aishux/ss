import java.time.LocalDate
import java.time.temporal.WeekFields
import java.util.Locale

object DateExtractor {
  def main(args: Array[String]): Unit = {
    val currentDate = LocalDate.now()

    // Extract current month
    val currentMonth = currentDate.getMonthValue
    println(s"Current month: $currentMonth")

    // Extract week number using ISO definition
    val weekNumberISO = currentDate.get(WeekFields.ISO.weekOfWeekBasedYear())
    println(s"Week number (ISO): $weekNumberISO")

    // Define a Locale for Zurich, Switzerland (German-speaking part)
    val zurichLocale = new Locale("de", "CH") // Language: German, Country: Switzerland

    // Extract week number using custom definition (e.g., Zurich Locale)
    val weekNumberZurich = currentDate.get(WeekFields.of(zurichLocale).weekOfWeekBasedYear())
    println(s"Week number (Custom, Zurich Locale): $weekNumberZurich")
  }
}
