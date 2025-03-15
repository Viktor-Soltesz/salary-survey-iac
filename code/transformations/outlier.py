"""
This module contains functions for handling outliers in data.
"""

import pandas as pd
import numpy as np

def remove_outliers_zscore(df: pd.DataFrame, column_name: str, threshold: float = 3) -> pd.DataFrame:
    """
    Removes outliers from a specified column using the Z-score method.

    Args:
        df: The input DataFrame.
        column_name: The name of the column to check for outliers.
        threshold: The Z-score threshold for identifying outliers.

    Returns:
        The DataFrame with outliers removed from the specified column.
    """
    if column_name not in df.columns:
        return df

    # Compute the Z-score for each value in the specified column
    z_scores = np.abs((df[column_name] - df[column_name].mean()) / df[column_name].std())

    # Identify outliers based on the Z-score threshold
    outlier_indices = z_scores > threshold

    # Remove outliers from the DataFrame
    df_filtered = df[~outlier_indices]

    return df_filtered
