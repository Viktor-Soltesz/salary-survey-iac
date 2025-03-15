"""
This module contains functions for handling null values in data.
"""

import pandas as pd

def drop_null_rows(df: pd.DataFrame, column_names: list[str]) -> pd.DataFrame:
    """
    Drops rows containing null values in the specified columns.

    Args:
        df: The input DataFrame.
        column_names: A list of column names to check for null values.

    Returns:
        The DataFrame with rows containing null values in the specified columns removed.
    """
    return df.dropna(subset=column_names)

def fill_null_values_with_constant(df: pd.DataFrame, column_name: str, constant_value) -> pd.DataFrame:
    """
    Fills null values of the given column with the given constant value.

    Args:
        df: The input DataFrame.
        column_name: The column to transform.
        constant_value: The value to replace the null.

    Returns:
        The DataFrame with rows containing null values in the specified columns filled.
    """
    df[column_name] = df[column_name].fillna(constant_value)
    return df
