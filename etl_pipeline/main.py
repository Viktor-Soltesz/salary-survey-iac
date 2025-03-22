# main.py
import functions_framework
from extract.extract_csv import extract_csv
from transform.standardize_format import standardize_format
from transform.drop_nulls import drop_nulls
from transform.clean_salary import clean_salary
from transform.map_job_categories import map_job_categories
from transform.map_country_codes import map_country_codes
from transform.out_of_scope import out_of_scope
from load.load_csv import archive_csv_df, load_df_to_bq

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
        # Extraction: Read CSV into DataFrame
        df = extract_csv(bucket, name)
        # Transformations
        # df = standardize_format(df)
        # df = drop_nulls(df)
        # df = clean_salary(df)
        # df = map_country_codes(df)
        # df = map_job_categories(df)
        # df = out_of_scope(df)
        # Loading into BigQuery: Upload the DataFrame
        load_df_to_bq(df, name)
        # Archiving: Write the transformed CSV to the archive bucket
        archive_csv_df(df, name)