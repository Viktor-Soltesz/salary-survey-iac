{{ config(
    materialized = 'table'
) }}

WITH base AS (
    SELECT *
    FROM {{ ref('stg_survey_data') }}
),

after_cleaning AS (
    SELECT *
    FROM {{ ref('int_survey_data__cleaned') }}
),

after_normalization AS (
    SELECT *
    FROM {{ ref('int_survey_data__outliers_flagged') }}
),

final_mart AS (
    SELECT *
    FROM {{ ref('mart_survey') }}
),

-- Metrics

null_salary AS (
    SELECT 'null_salary' AS metric_name, COUNT(*) AS issue_count
    FROM base
    WHERE salary_raw IS NULL
),

null_country AS (
    SELECT 'null_country' AS metric_name, COUNT(*) AS issue_count
    FROM base
    WHERE country_raw IS NULL
),

null_seniority_level AS (
    SELECT 'null_seniority_level' AS metric_name, COUNT(*) AS issue_count
    FROM base
    WHERE seniority_level_raw IS NULL
),

null_job_category AS (
    SELECT 'null_job_category' AS metric_name, COUNT(*) AS issue_count
    FROM base
    WHERE job_category_raw IS NULL
),

invalid_salary AS (
    SELECT 'invalid_salary' AS metric_name, COUNT(*) AS issue_count
    FROM base
    WHERE salary_raw < 0
),

future_dates AS (
    SELECT 'future_date' AS metric_name, COUNT(*) AS issue_count
    FROM base
    WHERE year_raw > EXTRACT(YEAR FROM CURRENT_DATE())
),

intranslatable_country AS (
    SELECT 'intranslatable_country_code' AS metric_name, COUNT(*) AS issue_count
    FROM after_cleaning
    WHERE country IS NULL
),

miscategorized_seniority AS (
    SELECT 'miscategorized_seniority' AS metric_name, COUNT(*) AS issue_count
    FROM after_cleaning
    WHERE seniority_level = 'other'
),

miscategorized_company_size AS (
    SELECT 'miscategorized_company_size' AS metric_name, COUNT(*) AS issue_count
    FROM after_cleaning
    WHERE company_size = 'other'
),

soft_duplicates AS (
    SELECT 'soft_duplicates' AS metric_name, COUNT(*)
    FROM (
        SELECT country, seniority_level, employment_status, salary, COUNT(*) AS cnt
        FROM final_mart
        GROUP BY country, seniority_level, employment_status, salary
        HAVING COUNT(*) > 1
    )
),

outliers_removed AS (
    SELECT 'outliers_removed' AS metric_name, COUNT(*)
    FROM after_normalization
    WHERE is_outlier = TRUE
),

exact_duplicates AS (
    SELECT 'exact_duplicates' AS metric_name, COUNT(*)
    FROM (
        SELECT year_raw, country_raw, seniority_level_raw, job_category_raw, salary_raw, COUNT(*) AS cnt
        FROM base
        GROUP BY year_raw, country_raw, seniority_level_raw, job_category_raw, salary_raw
        HAVING COUNT(*) > 1
    )
)

-- Final union

SELECT * FROM null_salary
UNION ALL
SELECT * FROM null_country
UNION ALL
SELECT * FROM null_seniority_level
UNION ALL
SELECT * FROM null_job_category
UNION ALL
SELECT * FROM invalid_salary
UNION ALL
SELECT * FROM future_dates
UNION ALL
SELECT * FROM intranslatable_country
UNION ALL
SELECT * FROM miscategorized_seniority
UNION ALL
SELECT * FROM miscategorized_company_size
UNION ALL
SELECT * FROM soft_duplicates
UNION ALL
SELECT * FROM outliers_removed
UNION ALL
SELECT * FROM exact_duplicates