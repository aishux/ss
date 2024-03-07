SELECT concat_ws(';', collect_set(email)) AS VU1_EMAILS
FROM (
    SELECT explode(split(VU1_EMAILS, ';')) AS email
    FROM your_table
) AS emails;
