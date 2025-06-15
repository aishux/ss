WITH base_data AS (
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
    REPORTING_DATE,
    AMOUNT
  FROM your_database.your_table
),
grouped_series AS (
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
    array_sort(
      collect_list(
        named_struct('REPORTING_DATE', REPORTING_DATE, 'AMOUNT', AMOUNT)
      )
    ) AS time_series
  FROM base_data
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
    REPORTING_CURRENCY
),
prompt_input_ready AS (
  SELECT
    *,
    array_join(
      transform(time_series, x -> concat(x.REPORTING_DATE, ': ', x.AMOUNT)),
      '\n'
    ) AS amount_over_time_text
  FROM grouped_series
)
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
    'Given this time series of AMOUNT over REPORTING_DATE, write a short commentary describing the key trends or changes and suggest any possible reason based on the pattern.',
    amount_over_time_text
  ) AS commentary
FROM prompt_input_ready;
