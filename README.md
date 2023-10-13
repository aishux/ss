import java.util.stream.Collectors
import scala.collection.JavaConverters._

// Assuming `strFlattenValueWoheader` is a Java Stream[String]
val strList = strFlattenValueWoheader.collect(Collectors.toList()).asScala.toList
val tempCSVdata: DataFrame = spark.sparkContext.parallelize(strList).toDF
