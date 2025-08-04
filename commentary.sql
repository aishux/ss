SELECT ai_generate("Give insights from this data", concat_ws(", ", col1, col2, col3))
FROM sales_data
LIMIT 5;
