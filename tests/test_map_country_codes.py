import pandas as pd
import json
import os
from unittest.mock import mock_open, patch
from etl_pipeline.transform.map_country_codes import map_country_codes

def test_map_country_codes_replaces_names_with_codes():
    # Sample test DataFrame
    df_dirty = pd.DataFrame({
        'country': ['Germany', 'France', 'India', 'Unknown']
    })

    # Define a mock country mapping
    mock_mapping = {
        "germany": "de",
        "france": "fr",
        "india": "in"
    }

    # Patch the open() call inside the function to return our mock JSON
    mock_json = json.dumps(mock_mapping)
    with patch("builtins.open", mock_open(read_data=mock_json)):
        with patch("os.path.join", return_value="mocked_path.json"):
            df_cleaned = map_country_codes(df_dirty)

    # Assert expected output
    expected = pd.Series(["de", "fr", "in", "unknown"], name="country")
    pd.testing.assert_series_equal(df_cleaned['country'], expected)
