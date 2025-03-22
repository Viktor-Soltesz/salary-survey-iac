import pandas as pd
import json
import os

def map_country_codes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Maps country names to standardized country codes based on a JSON file.

    Parameters:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Transformed DataFrame with mapped country codes.
    """

    # Load country mapping from JSON file
    mapping_path = os.path.join(os.path.dirname(__file__), 'country_mapping.json')
    
    with open(mapping_path, 'r', encoding='utf-8') as file:
        country_to_code = json.load(file)

    # Apply mapping
    df['country'] = df['country'].str.lower().replace(country_to_code)

    return df
