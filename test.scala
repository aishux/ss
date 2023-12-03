import java.time.{DayOfWeek, LocalDate}

// Get today's date
val today = LocalDate.now()

// Find the day of the week (0: Saturday, 1: Sunday, ..., 6: Friday)
val dayOfWeek = today.getDayOfWeek().getValue()

// Calculate the difference to get to the end of the week (Friday: 6)
val daysToAdd = (6 - dayOfWeek + DayOfWeek.SATURDAY.getValue()) % 7

// Calculate the end date of the current week (Friday)
val weekEndDate = today.plusDays(daysToAdd)

// Display the end date of the current week (Friday)
println("End date of the current week (Friday): " + weekEndDate)
