"""
Integration test for the entire transformation pipeline from dirty to clean data.
"""

import os
import pandas as pd
from etl_pipeline.transform.standardize_format import standardize_format
from etl_pipeline.transform.clean_salary import clean_salary
from etl_pipeline.transform.out_of_scope import out_of_scope
from etl_pipeline.transform.drop_nulls import drop_nulls
from etl_pipeline.transform.map_country_codes import map_country_codes
from etl_pipeline.transform.map_job_categories import map_job_categories

def test_transformation_pipeline_from_dirty_to_clean():
    """
    Test the entire transformation pipeline from dirty to clean data.
    """
    # Define paths
    base_dir = os.path.dirname(__file__)  
    assets_tests_dir = os.path.join(base_dir, 'assets_tests')
    dirty_csv_path = os.path.join(assets_tests_dir, 'test_data_dirty.csv')
    clean_csv_path = os.path.join(assets_tests_dir, 'test_data_clean.csv')

    # Load dirty input and expected clean output
    df_dirty = pd.read_csv(dirty_csv_path)
    df_expected = pd.read_csv(clean_csv_path)

    # Run full transformation pipeline
    df = standardize_format(df_dirty)
    df = drop_nulls(df)
    df = clean_salary(df) # test fails
    df = map_country_codes(df)
    df = map_job_categories(df) # error
    df = out_of_scope(df)

    # Convert columns in df_expected to float64. As float64 can handle NaNs.
    df_expected[['salary','year']] = df_expected[['salary','year']].astype('float64')

    # Reset index before comparison (optional but helps)
    df = df.reset_index(drop=True)
    df_expected = df_expected.reset_index(drop=True)

    # Compare results
    pd.testing.assert_frame_equal(df, df_expected)
