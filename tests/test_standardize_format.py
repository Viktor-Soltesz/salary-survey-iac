import pandas as pd
from io import StringIO
from etl_pipeline.transform.standardize_format import standardize_format

def test_standardize_format_transforms_headers_and_strings():
    csv_data = """
Work Year,Experience Level , Employment_Type,Employee residence,Salary,Salary in USD,Job Title
2024,Senior,FT,HU,20000,22000,Data Analyst
2023,Mid,PT,DE,18000,20000,Software Engineer
"""

    df_dirty = pd.read_csv(StringIO(csv_data))

    df_cleaned = standardize_format(df_dirty)

    # Check if columns are renamed correctly
    expected_columns = [
        'year',
        'seniority_level',
        'employment_status',
        'country',
        'salary_eur',
        'salary',
        'job_title'
    ]
    assert list(df_cleaned.columns) == expected_columns

    # Check if object columns are lowercased
    assert df_cleaned.loc[0, 'job_title'] == 'data analyst'
    assert df_cleaned.loc[1, 'country'] == 'de'
    assert df_cleaned.loc[0, 'seniority_level'] == 'senior'
