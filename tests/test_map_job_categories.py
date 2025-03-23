import pandas as pd
import json
import re
from io import StringIO
from unittest.mock import patch, mock_open
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

    df_dirty = pd.read_csv(StringIO(csv_data))

    # Prepare mocked JSON mapping
    mock_json = json.dumps(mock_mapping)

    with patch("builtins.open", mock_open(read_data=mock_json)):
        with patch("os.path.join", return_value="mocked_path.json"):
            df_cleaned = map_job_categories(df_dirty)

    # Assertions
    expected_categories = pd.Series(
        ["Data", "DevOps", "Product", "Uncategorized"],
        name="job_category"
    )

    pd.testing.assert_series_equal(df_cleaned["job_category"], expected_categories)
