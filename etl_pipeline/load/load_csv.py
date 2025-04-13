"""
Module to archive a DataFrame as CSV in a GCS bucket and load it into BigQuery.
"""

import os
from google.cloud import storage, bigquery

def archive_csv_df(df, blob_name):
    """Archives the DataFrame by writing it as CSV to the archive bucket."""
    archive_bucket_name = os.environ['GCS_ARCHIVE_BUCKET']
    storage_client = storage.Client()
    archive_bucket = storage_client.bucket(archive_bucket_name)
    blob = archive_bucket.blob(blob_name)
    csv_data = df.to_csv(index=False)
    blob.upload_from_string(csv_data, content_type='text/csv')
    print(f"Archived CSV to bucket {archive_bucket_name}/{blob_name}.")

def load_df_to_bq(df, blob_name):
    """Loads the DataFrame into BigQuery."""
    client = bigquery.Client()
    project_id = os.environ['DW_PROJECT_ID']
    # Assuming blob_name is formatted as "dataset/table/..."
    params = blob_name.split("/")
    table_id = f"{project_id}.{params[0]}.{params[1]}"
    print(f"Table ID: {table_id}")

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    load_job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    load_job.result()  # Wait for the job to complete.
    destination_table = client.get_table(table_id)
    print(f"Table has now {destination_table.num_rows} rows.")
