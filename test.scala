SELECT TO_CHAR(TO_TIMESTAMP(EXT_TIM_IDENT, 'YYYYMMDD'), 'YYYYMM Mon') AS formatted_date
FROM your_table;
