import java.time.{LocalDate, WeekFields}
import java.util.Locale

val year = 2023
val firstDayOfYear = LocalDate.of(year, 1, 1)
val weekFields = WeekFields.of(Locale.getDefault())

(1 to firstDayOfYear.range(weekFields.weekOfWeekBasedYear()).getMaximum.toInt).foreach { week =>
  val weekStartDate = firstDayOfYear.`with`(weekFields.weekOfWeekBasedYear(), week.toLong).`with`(weekFields.dayOfWeek(), 1)
  val weekEndDate = weekStartDate.plusDays(4) // Set to Friday
  println(s"Week $week: $weekStartDate - $weekEndDate")
}
