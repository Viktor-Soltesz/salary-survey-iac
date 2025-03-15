import functions_framework
from google.cloud import bigquery, storage
import os
import pandas as pd
from io import StringIO

def extract_csv(bucket, blob_name):
    """Extracts a CSV from GCS and returns a pandas DataFrame."""
    storage_client = storage.Client()
    bucket_obj = storage_client.bucket(bucket)
    blob = bucket_obj.blob(blob_name)
    csv_content = blob.download_as_text()  # Download as text into the python runtime environment
    df = pd.read_csv(StringIO(csv_content))
    return df

def transform_df(df):
    """Transforms the DataFrame by stripping whitespace from string columns."""
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()
    return df

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
    table_id = "{}.{}.{}".format(project_id, params[0], params[1])
    print(f"Table ID: {table_id}")

    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        # Optionally, use WRITE_TRUNCATE or other dispositions based on your needs
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        source_format=bigquery.SourceFormat.CSV,
    )
    
    load_job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    load_job.result()  # Wait for the job to complete.
    destination_table = client.get_table(table_id)
    print("Table has now {} rows.".format(destination_table.num_rows))

# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def trigger_gcs(cloud_event):
    data = cloud_event.data

    event_id = cloud_event["id"]
    event_type = cloud_event["type"]

    bucket = data["bucket"]
    name = data["name"]
    metageneration = data["metageneration"]
    timeCreated = data["timeCreated"]
    updated = data["updated"]

    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Bucket: {bucket}")
    print(f"File: {name}")
    print(f"Metageneration: {metageneration}")
    print(f"Created: {timeCreated}")
    print(f"Updated: {updated}")

    if 'csv' in name:
        # Extraction
        df = extract_csv(bucket, name)
        # Transformation
        df = transform_df(df)
        # Loading into BigQuery
        load_df_to_bq(df, name)
        # Archiving the transformed CSV
        archive_csv_df(df, name)
