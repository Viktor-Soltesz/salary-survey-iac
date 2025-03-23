import numpy as np
import pandas as pd
import pandas.testing as pdt
from etl_pipeline.transform.clean_salary import clean_salary

def test_clean_salary_values_are_cleaned_and_numeric():
    # Define test input as a DataFrame
    df_dirty = pd.DataFrame({
        'salary': [
            '50,000+',    # has comma, plus sign
            '€60000',     # has euro symbol
            ' 75,000-',   # whitespace, comma, minus
            '9000000',    # too high (should remain for now since outlier filtering is not included here)
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
