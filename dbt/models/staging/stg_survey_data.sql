{{ config(
    materialized = 'table',
) }}

SELECT *
FROM {{ source('survey_data', 'developer_salaries') }}
LIMIT 10