-- Step 1: Create a temporary view with grouped time series
CREATE OR REPLACE TEMP VIEW grouped_series AS
SELECT
  PROJECTION_TYPE,
  REPORTING_PERIOD_TYPE,
  COST_CENTER_CODE,
  CLIENT_ADVSIOR_CODE,
  LEGAL_ENTITY_CODE,
  REPORTING_VIEW_CODE,
  MEASURE,
  BOOK_VIEW_CODE,
  REPORTING_PERIOD,
  ORGANIZATION_CODE,
  REPORTING_CURRENCY,
  array_sort(collect_list(named_struct('REPORTING_DATE', REPORTING_DATE, 'AMOUNT', AMOUNT))) AS amount_series
FROM your_database.your_table
GROUP BY
  PROJECTION_TYPE,
  REPORTING_PERIOD_TYPE,
  COST_CENTER_CODE,
  CLIENT_ADVSIOR_CODE,
  LEGAL_ENTITY_CODE,
  REPORTING_VIEW_CODE,
  MEASURE,
  BOOK_VIEW_CODE,
  REPORTING_PERIOD,
  ORGANIZATION_CODE,
  REPORTING_CURRENCY;

-- Step 2: Convert the array to a prompt string
CREATE OR REPLACE TEMP VIEW prompt_ready AS
SELECT
  *,
  array_join(
    transform(amount_series, x -> concat(x.REPORTING_DATE, ': ', x.AMOUNT)),
    '\n'
  ) AS prompt_input
FROM grouped_series;

-- Step 3: Use ai_query() to generate commentary
SELECT
  PROJECTION_TYPE,
  REPORTING_PERIOD_TYPE,
  COST_CENTER_CODE,
  CLIENT_ADVSIOR_CODE,
  LEGAL_ENTITY_CODE,
  REPORTING_VIEW_CODE,
  MEASURE,
  BOOK_VIEW_CODE,
  REPORTING_PERIOD,
  ORGANIZATION_CODE,
  REPORTING_CURRENCY,
  ai_query(
    'Analyze the time series of amounts over REPORTING_DATE and generate a short commentary on trends or significant changes.',
    prompt_input
  ) AS commentary
FROM prompt_ready;

