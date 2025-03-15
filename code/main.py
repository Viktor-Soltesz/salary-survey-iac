"""
Main module for the Cloud Function. Orchestrates data extraction, transformation, and loading.
"""
import functions_framework
import pandas as pd
from transformations import cleaning, uniformizing, null_handling, outlier
from .gcs_extractor import extract_data_from_gcs  # using relative import for modules in same folder
from .bq_loader import load_data_to_bq  # using relative import for modules in same folder

@functions_framework.cloud_event
def gcs_to_bq(cloud_event):
    """
    Cloud Function triggered by a change to a Cloud Storage bucket.
    Orchestrates the data pipeline: extract, transform, load.
    """
    bucket_name = cloud_event.data["bucket"]
    file_name = cloud_event.data["name"]

    try:
        # 1. Extract Data from GCS
        df = extract_data_from_gcs(bucket_name, file_name)

        # 2. Transform Data
        print("Starting Data Transformation...")
        # df = cleaning.clean_customer_email(df)
        # df = cleaning.clean_order_id(df)
        # df = uniformizing.uniformize_action_types(df)
        # df = null_handling.drop_null_rows(df, ["action", "order_id", "customer_email", "action_time"])
        # df = outlier.remove_outliers_zscore(df, "order_id", 3)
        # df = null_handling.fill_null_values_with_constant(df, "order_id", "unknown")
        print(f"Data Transformation finished. shape {df.shape}")

        # 3. Load Data to BigQuery
        dataset_id = "ecommerce"
        table_id = "order_events"
        table_schema = [
            {"name":"order_id", "type":"STRING"},
            {"name":"customer_email", "type":"STRING"},
            {"name":"action", "type":"STRING"},
            {"name":"action_time", "type":"TIMESTAMP"},
        ]
        load_data_to_bq(df, dataset_id, table_id, table_schema)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    except ValueError as e:
        print(f"Error: {e}")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return
