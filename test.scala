SELECT DATE_FORMAT(STR_TO_DATE(date_column, '%Y%m%d'), '%Y%m %b') AS formatted_date
FROM your_table;
