"""
This module contains the main function for the Cloud Function.
"""
import os
import functions_framework
import pandas as pd
from google.cloud import bigquery, storage
from io import StringIO
from transformations import cleaning, uniformizing, null_handling, outlier

@functions_framework.cloud_event
def gcs_to_bq(cloud_event):
    """
    Triggered by a change to a Cloud Storage bucket.
    This function loads CSV data from GCS, performs data transformations,
    and loads the transformed data into BigQuery.
    """

    # Extract file information from the cloud event
    bucket_name = cloud_event.data["bucket"]
    file_name = cloud_event.data["name"]
    print(f"Detected file: {file_name} in bucket: {bucket_name}.")

    #check if the file is a csv
    if not file_name.endswith('.csv'):
        print("file not a csv, skipping.")
        return

    # Initialize GCS client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Download the CSV file to memory
    csv_data = blob.download_as_text()
    
    # Create a pandas DataFrame from the CSV data
    df = pd.read_csv(StringIO(csv_data))
    print(f"File loaded to dataframe. shape {df.shape}")

    # Data Transformation Pipeline
    df = cleaning.clean_customer_email(df)
    df = cleaning.clean_order_id(df)
    df = uniformizing.uniformize_action_types(df)
    df = null_handling.drop_null_rows(df, ["action", "order_id", "customer_email", "action_time"])
    df = outlier.remove_outliers_zscore(df,"order_id", 3)
    df = null_handling.fill_null_values_with_constant(df,"order_id","unknown")

    print(f"Data Transformation finished. shape {df.shape}")
    
    # Initialize BigQuery client
    bq_client = bigquery.Client()

    # Define the BigQuery table reference
    dataset_id = "ecommerce"
    table_id = "order_events"
    table_ref = bq_client.dataset(dataset_id).table(table_id)

    # Load the DataFrame into BigQuery
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        # Define the schema for the table. If the table was empty, the schema is autodetected.
        schema=[
        bigquery.SchemaField("order_id", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("customer_email", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("action", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("action_time", bigquery.enums.SqlTypeNames.TIMESTAMP),
        ],
    )
    # Convert DataFrame to list of dictionaries for BigQuery
    records = df.to_dict('records')
    job = bq_client.load_table_from_json(records, table_ref, job_config=job_config)
    
    # Wait for the load job to complete
    job.result()

    print(f"Successfully loaded {len(records)} rows to BigQuery table: {table_ref.path}")
