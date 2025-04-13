"""
Module to drop rows with null values in critical columns.
"""

import pandas as pd

def drop_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drops rows with null values in critical columns.
    Parameters:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Transformed DataFrame with nulls removed.
    """

    # Define required columns
    required_columns = [
        'salary', 
        'employment_status', 
        'country', 
        'seniority_level', 
        'job_title', 
        'year']

    # Drop rows where any of the required columns have NaN values
    df = df.dropna(subset=required_columns)

    return df
