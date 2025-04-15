"""
Unit tests for the clean_salary function in the ETL pipeline.
"""

import numpy as np
import pandas as pd
import pandas.testing as pdt
import pytest
from etl_pipeline.transform.clean_salary import clean_salary

def test_clean_salary_values_are_cleaned_and_numeric():
    """
    Tests that the clean_salary function correctly cleans and converts salary values to numeric.
    """
    # Define test input as a DataFrame
    df_dirty = pd.DataFrame({
        'salary': [
            '50,000+',    # has comma, plus sign
            '€60000',     # has euro symbol
            ' 75,000-',   # whitespace, comma, minus
            '9000000',    # too high (should remain for now since outlier are not handled here)
            'notanumber', # should become None
            None,         # should remain None
            42000         # already clean
        ]
    })

    # Expected cleaned values
    expected_salaries = pd.Series([
        50000.0,
        60000.0,
        75000.0,
        9000000.0,
        np.nan,
        np.nan,
        42000.0
        ],
        name='salary'
    )

    # Apply transformation
    df_cleaned = clean_salary(df_dirty)

    # This comparison handles NaN correctly
    pdt.assert_series_equal(df_cleaned['salary'], expected_salaries, check_names=True)

def test_clean_salary_raises_keyerror_if_column_missing():
    """
    Tests that clean_salary raises a KeyError if the 'salary' column is missing.
    """
    # Create a DataFrame *without* the 'salary' column
    df_invalid = pd.DataFrame({
        'some_other_column': ['a', 'b', 'c'],
        'another_col': [1, 2, 3]
    })

    # Use pytest.raises to assert that a KeyError is raised
    with pytest.raises(KeyError) as excinfo:
        clean_salary(df_invalid)

    # Optionally, assert the specific error message
    assert "Column 'salary' not found in the DataFrame." in str(excinfo.value)
    