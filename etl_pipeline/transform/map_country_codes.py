""" 
Module to map country names to standardized country codes.
"""

import json
import os
import pandas as pd

def map_country_codes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Maps country names to standardized country codes based on a JSON file.

    Parameters:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Transformed DataFrame with mapped country codes.
    """

    # Load country mapping from JSON file
    #mapping_path = os.path.join(os.path.dirname(__file__), 'country_mapping.json')
    mapping_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        '.', 
        'assets_etl', 
        'country_mapping.json'
    )
    mapping_path = os.path.abspath(mapping_path)

    with open(mapping_path, 'r', encoding='utf-8') as file:
        country_to_code = json.load(file)

    # Apply mapping
    df['country'] = df['country'].str.lower().replace(country_to_code)

    return df
