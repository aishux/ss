-- Update the original table with unique values
UPDATE test
SET A = (
    SELECT CONCAT_WS(';', COLLECT_SET(UniqueValue))
    FROM TempUniqueValues
);
