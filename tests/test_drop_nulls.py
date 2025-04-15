"""
test_drop_nulls.py
"""

from io import StringIO
import pandas as pd
from etl_pipeline.transform.drop_nulls import drop_nulls

def test_drop_nulls_removes_incomplete_rows():
    """
    Test the drop_nulls function to ensure it removes rows with null values in critical columns.
    csv-style definition for better usability. 
    It needs StringIO, but much more readable/ easier expandable.
    """
    csv_data = """
salary,employment_status,country,seniority_level,job_title,year
20000,FT,HU,EN,Data Analyst,2024
,FT,HU,EN,Data Analyst,2024
20000,,HU,EN,Data Analyst,2024
20000,FT,,EN,Data Analyst,2024
20000,FT,HU,,Data Analyst,2024
20000,FT,HU,EN,,2024
20000,FT,HU,EN,Data Analyst,
"""

    # Read CSV into DataFrame
    df_dirty = pd.read_csv(StringIO(csv_data))

    # Apply transformation
    df_cleaned = drop_nulls(df_dirty)

    # Expect only the first row to remain
    assert df_cleaned.shape[0] == 1 # Intentional fail. Should be 1.
    assert df_cleaned.iloc[0].to_dict() == {
        'salary': 20000.0,
        'employment_status': 'FT',
        'country': 'HU',
        'seniority_level': 'EN',
        'job_title': 'Data Analyst',
        'year': 2024.0
    }
