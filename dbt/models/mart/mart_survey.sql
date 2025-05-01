{{ config(
    materialized = 'table'
) }}

-- mart_survey
-- This model provides the final cleaned and normalized dataset of global developer salaries,
-- ready for consumption by dashboards, reporting, or analysis.
-- It excludes statistical outliers and selects only meaningful fields.

WITH source AS (
    SELECT *
    FROM {{ ref('int_survey_data__outliers_flagged') }}
    WHERE is_outlier = FALSE
)

SELECT
    -- IDs
    survey_entry_id,
    entry_number,

    -- Time
    year,

    -- Key dimensions
    country,
    country_name,
    job_category,
    seniority_level,
    employment_status,
    company_size,

    -- Raw and normalized values
    salary,
    salary_norm2024,
    salary_normgdp,
    salary_norm,

    -- Enrichment fields
    gdp_ppp,
    factor_to_2024,

    -- Outlier score (for reference only)
    z_score_modif

FROM source
