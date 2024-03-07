-- Update the original table with unique values within each row
UPDATE test
SET columnB = (
    SELECT CONCAT_WS(';', ARRAY_JOIN(ARRAY_DISTINCT(SPLIT(columnB, ';')), ';'))
);

-- Display the updated table
SELECT * FROM test;
