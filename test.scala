import java.time.{LocalDate, DayOfWeek, WeekFields, DateTimeFormatter}
import java.util.Locale

def generateWeeklyData(year: Int, hierarchy_type: String): Seq[(String, String, String, String, String, String, String, String, String, String, String)] = {
  val formatter = DateTimeFormatter.ofPattern("yyyyMMdd")
  val firstDayOfYear = LocalDate.of(year, 1, 1)
  val weekFields = WeekFields.of(Locale.getDefault())

  (1 to firstDayOfYear.range(weekFields.weekOfWeekBasedYear()).getMaximum.toInt).map { week =>
    //val weekStartDate = firstDayOfYear.`with`(weekFields.weekOfWeekBasedYear(), week.toLong).`with`(DayOfWeek.MONDAY)
    val weekStartDate = firstDayOfYear.`with`(weekFields.weekOfWeekBasedYear(), week.toLong).`with`(weekFields.dayOfWeek(), 1)
    val weekEndDate = weekStartDate.plusDays(4)  // Set to Friday
    val weekNumber = f"$week%02d"
    val weekDesc = s"$year $weekNumber"

    ("WEEKLY", "Weekly Periods", "0", s"W_$year", s"$year", weekEndDate.format(formatter), weekDesc, "0", "W", hierarchy_type)
  }
}

val currentYear = LocalDate.now().getYear

val result = generateWeeklyData(currentYear, "kyvos_gwm_pc")
result.foreach(println)
