import pandas as pd
import json
import re
from io import StringIO
from unittest.mock import patch, mock_open
import numpy as np
from etl_pipeline.transform.map_job_categories import map_job_categories

def test_map_job_categories_applies_expected_labels():
    # Define mock job categories mapping
    mock_mapping = {
        "Data": ["data analyst", "data scientist"],
        "DevOps": ["devops", "site reliability"],
        "Product": ["product owner", "product manager"]
    }

    # Simulate dirty job titles in a DataFrame
    csv_data = """job_title
Senior Data Analyst
sr. devops engineer
Product Owner
AI Researcher
  
"""

    df_dirty = pd.read_csv(StringIO(csv_data), skip_blank_lines=False)

    # Prepare mocked JSON mapping
    mock_json = json.dumps(mock_mapping)

    with patch("builtins.open", mock_open(read_data=mock_json)):
        with patch("os.path.join", return_value="mocked_path.json"):
            df_cleaned = map_job_categories(df_dirty)

    # Assertions
    expected_categories = pd.Series(
        ["Data", "DevOps", "Product", "Uncategorized", "Uncategorized"],
        name="job_category"
    )

    # # --- Print statements for debugging ---
    # print(df_dirty)
    # print(len(df_dirty))
    # print("\n--- Debugging Series ---") # Add header for clarity
    # print("Actual Series (df_cleaned['job_category']):")
    # print(df_cleaned["job_category"])

    # print("\nExpected Series (expected_categories):")
    # print(expected_categories)

    pd.testing.assert_series_equal(df_cleaned["job_category"], expected_categories)

def test_map_job_categories_handles_null():
    mock_mapping = {"Test": ["test"]}
    df_dirty = pd.DataFrame({'job_title': [None, pd.NA, np.nan]}) # Different ways to represent null

    mock_json = json.dumps(mock_mapping)
    with patch("builtins.open", mock_open(read_data=mock_json)):
        with patch("os.path.join", return_value="mocked_path.json"):
            df_cleaned = map_job_categories(df_dirty.copy())

    expected_categories = pd.Series(["Uncategorized", "Uncategorized", "Uncategorized"], name="job_category")
    pd.testing.assert_series_equal(df_cleaned["job_category"], expected_categories)