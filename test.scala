// Assuming you have a list of monthly amounts (replace this with your data)
val monthlyAmounts: List[Double] = List(100.0, 150.0, 200.0, 180.0, 210.0, 190.0, 220.0, 240.0, 260.0, 280.0, 300.0, 320.0)

// Get the current month (replace with your logic to get the current month)
val currentMonth: Int = java.time.LocalDate.now().getMonthValue

// Calculate YTD amount
val ytdAmount: Double = monthlyAmounts.take(currentMonth).sum

// Display YTD amount
println(s"Year-to-Date (YTD) amount: $ytdAmount")
