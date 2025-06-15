WITH grouped_series AS (
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
    REPORTING_CURRENCY
),
prompt_ready AS (
  SELECT
    *,
    array_join(
      transform(amount_series, x -> concat(x.REPORTING_DATE, ': ', x.AMOUNT)),
      '\n'
    ) AS prompt_input
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
    'Analyze the time series of AMOUNT across REPORTING_DATE. Identify trends, spikes or drops, and summarize key changes briefly.',
    prompt_input
  ) AS commentary
FROM prompt_ready;
