"""
This module contains functions for cleaning data.
"""

import pandas as pd

def clean_customer_email(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the 'customer_email' column in a DataFrame.
    Removes leading/trailing spaces and converts to lowercase.

    Args:
        df: The input DataFrame.

    Returns:
        The DataFrame with the 'customer_email' column cleaned.
    """
    if 'customer_email' in df.columns:
        df['customer_email'] = df['customer_email'].str.strip().str.lower()
    return df

def clean_order_id(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the 'order_id' column in a DataFrame.
    Removes any non-alphanumeric characters.

    Args:
        df: The input DataFrame.

    Returns:
        The DataFrame with the 'order_id' column cleaned.
    """
    if 'order_id' in df.columns:
        df['order_id'] = df['order_id'].str.replace(r'[^a-zA-Z0-9]', '', regex=True)
    return df
