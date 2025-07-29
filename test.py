
df = spark.read.option("header", "true") \
               .option("quote", '"') \
               .option("escape", '"') \
               .option("multiLine", "true") \
               .csv("/dbfs/FileStore/your_file.csv")

# Optional: display the DataFrame
display(df)

# Save as a table (choose your table name)
df.write.format("delta").mode("overwrite").saveAsTable("your_table_name")