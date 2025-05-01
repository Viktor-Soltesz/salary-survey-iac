-- stg_seed_inflation_factors.sql
WITH source AS (
    SELECT *
    FROM {{ ref('inflation_factors') }}
)

SELECT
    CAST(year AS NUMERIC) AS year,
    CAST(factor_to_2024 AS NUMERIC) AS factor_to_2024
FROM source