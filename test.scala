// Define group by columns dynamically
val groupByColumns = (1 to 20).map(i => col(s"level$i"))

// Perform group by and aggregation
val groupedResult = finalResult.groupBy(groupByColumns: _*)
                              .agg(collect_set("emails").as("VU1"))
