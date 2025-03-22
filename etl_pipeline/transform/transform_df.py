# transform/transform_df.py
import pandas as pd

def transform_df(df):
    """Transforms the DataFrame by:
       - Stripping whitespace from column names.
       - Removing leading/trailing whitespace from string values.
    """
    # Strip whitespace from column names (ensuring they match the BigQuery schema)
    df.columns = df.columns.str.strip()
    
    # Remove whitespace from string columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()

    return df