import java.util.stream.Collectors
import java.util.stream.StreamSupport
import scala.collection.JavaConverters._

// Assuming `strFlattenValueWoheader` is a Java Stream[String]
val strList = StreamSupport.stream(strFlattenValueWoheader.spliterator(), false)
  .collect(Collectors.toList[String]())
  .asScala
  .toList

val tempCSVdata: DataFrame = spark.sparkContext.parallelize(strList).toDF
