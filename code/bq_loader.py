"""
Module for loading data into BigQuery.
"""
from google.cloud import bigquery
import pandas as pd

def load_data_to_bq(df: pd.DataFrame, dataset_id: str, table_id: str, schema: list) -> None:
    """
    Loads a pandas DataFrame into a BigQuery table.

    Args:
        df: The pandas DataFrame to load.
        dataset_id: The ID of the BigQuery dataset.
        table_id: The ID of the BigQuery table.
        schema: the schema of the table to be written.

    Raises:
        Exception: If there is an error during the load job.
    """
    print(f"Loading data to BigQuery table: {dataset_id}.{table_id}")

    bq_client = bigquery.Client()
    table_ref = bq_client.dataset(dataset_id).table(table_id)

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        schema=schema
    )
    job = bq_client.load_table_from_dataframe(df, table_ref, job_config=job_config) # this line changed

    try:
        job.result()  # Wait for the job to complete.
        print(f"Successfully loaded data to BigQuery table: {table_ref.path}") # this line changed
    except Exception as e:
        print(f"Error loading data to BigQuery: {e}")
        raise
