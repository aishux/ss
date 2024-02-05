import java.time.{LocalDate, DayOfWeek}

def printFridaysInCurrentYear(): Unit = {
  val currentYear = LocalDate.now().getYear

  val startDate = LocalDate.of(currentYear, 1, 1)
  val endDate = LocalDate.of(currentYear, 12, 31)

  var currentDate = startDate

  while (currentDate.isBefore(endDate) || currentDate.isEqual(endDate)) {
    if (currentDate.getDayOfWeek == DayOfWeek.FRIDAY) {
      println(currentDate)
    }
    currentDate = currentDate.plusDays(1)
  }
}

// Call the function
printFridaysInCurrentYear()
