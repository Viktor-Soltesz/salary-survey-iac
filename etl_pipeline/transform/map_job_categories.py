import pandas as pd
import json
import re
import os

def map_job_categories(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and categorizes job titles into standardized job categories.

    Steps:
    1. Removes 'senior' and 'sr.' from job titles.
    2. Strips leading/trailing whitespace.
    3. Maps job titles to predefined job categories.

    Parameters:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Transformed DataFrame with a new 'job_category' column.
    """

    # Load job category mapping from JSON file
    #mapping_path = os.path.join(os.path.dirname(__file__), 'job_categories.json')
    mapping_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'assets', 'job_categories.json')
    mapping_path = os.path.abspath(mapping_path)

    with open(mapping_path, 'r', encoding='utf-8') as file:
        job_categories = json.load(file)

    # Clean job titles before categorization
    df['job_title'] = df['job_title'].str.replace('senior', '', case=False, regex=False)
    df['job_title'] = df['job_title'].str.replace('sr.', '', case=False, regex=False)
    df['job_title'] = df['job_title'].str.strip()

    # Function to categorize job title
    def categorize_job_title(job_title: str) -> str:
        if pd.isna(job_title):
            return "Uncategorized"

        job_title = job_title.lower()

        for category, keywords in job_categories.items():
            for keyword in keywords:
                if re.search(rf"\b{re.escape(keyword.lower())}\b", job_title):
                    return category

        return "Uncategorized"

    # Apply categorization
    df['job_category'] = df['job_title'].apply(categorize_job_title)

    return df
