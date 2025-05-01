WITH source AS (
    SELECT *
    FROM {{ ref('country_economic_factors') }}
)

SELECT
    country_code,
    median_income_2020_usd,
    mean_income_2020_usd,
    gdp_ppp_usd AS gdp_ppp,
    glassdoor_software_engineer_usd
FROM source