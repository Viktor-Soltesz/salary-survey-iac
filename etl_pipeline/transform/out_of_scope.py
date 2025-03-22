import pandas as pd

def out_of_scope(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filters the dataset to include only full-time (ft) workers.

    Parameters:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Filtered DataFrame with only full-time employees.
    """
    return df[df['employment_status'] == 'ft']
