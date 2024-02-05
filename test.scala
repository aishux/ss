import java.time.{LocalDate, DayOfWeek, WeekFields, TemporalAdjusters, DateTimeFormatter}
import java.util.Locale

def generateWeeklyData(year: Int, hierarchy_type: String) = {
    val formatter = DateTimeFormatter.ofPattern("yyyyMMdd")
    val firstFridayOfYear = LocalDate.of(year, 1, 1)
      .with(TemporalAdjusters.nextOrSame(DayOfWeek.FRIDAY))
    val weekFields = WeekFields.of(DayOfWeek.MONDAY, 1)

    Iterator.iterate(firstFridayOfYear)(.plusDays(7)).takeWhile(.getYear == year).map { weekStartDate =>
      val weekEndDate = weekStartDate.with(DayOfWeek.FRIDAY)
      val weekNumber = weekStartDate.get(weekFields.weekOfWeekBasedYear)
      val weekDesc = s"$year ${f"$weekNumber%02d"}"

      ("WEEKLY", "Weekly Periods", "0", s"W_$year", s"$year", weekEndDate.format(formatter), weekDesc, "0", "W", hierarchy_type)
    }
  }
