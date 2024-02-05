import java.time.{LocalDate, DayOfWeek}

def getFridaysInCurrentYear(): Seq[LocalDate] = {
  val currentYear = LocalDate.now().getYear

  val startDate = LocalDate.of(currentYear, 1, 1)
  val endDate = LocalDate.of(currentYear, 12, 31)

  var currentDate = startDate
  var fridays = Seq[LocalDate]()

  while (currentDate.isBefore(endDate) || currentDate.isEqual(endDate)) {
    if (currentDate.getDayOfWeek == DayOfWeek.FRIDAY) {
      fridays = fridays :+ currentDate
    }
    currentDate = currentDate.plusDays(1)
  }

  fridays
}

// Call the function and print the result
val fridaysInCurrentYear = getFridaysInCurrentYear()
fridaysInCurrentYear.foreach(println)
