"""
Module Cleans and transforms the 'salary' column in a DataFrame.
"""

import re
import pandas as pd

def clean_salary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and transforms the 'salary_eur' column:
    - Converts salary to string (if necessary).
    - Removes spaces, '+' and '-' characters.
    - Replaces commas with dots for decimal standardization.
    - Removes currency symbols and non-numeric characters.
    - Converts the cleaned string to a numeric format.
    - Filters out extreme outliers (e.g., salaries < 1,000 or > 1,000,000).

    Parameters:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Transformed DataFrame with cleaned salary values.
    """

    # Ensure 'salary' column exists
    if 'salary' not in df.columns:
        raise KeyError("Column 'salary' not found in the DataFrame.")

    # Convert to string and clean salary values
    def clean_salary_value(value):
        if pd.isna(value):
            return None

        # Convert to string and strip whitespaces
        value = str(value).strip()

        # Remove '+' and '-' symbols
        value = value.replace('+', '').replace('-', '')

        # Replace commas with whitespace. Assuming commas are used as thousands separators.
        value = value.replace(',', '')

        # Remove non-numeric characters (except dots for decimal values)
        value = re.sub(r'[^0-9.]', '', value)

        # Convert to float, return None if conversion fails
        try:
            return float(value)
        except ValueError:
            return None

    # Apply transformation
    df['salary'] = df['salary'].apply(clean_salary_value)

    return df
