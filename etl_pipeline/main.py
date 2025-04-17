"""ETL Pipeline for CSV files in Google Cloud Storage"""

import functions_framework
from cloudevents.http import CloudEvent
from extract.extract_csv import extract_csv
from transform.standardize_format import standardize_format
from transform.drop_nulls import drop_nulls
from transform.clean_salary import clean_salary
from transform.map_job_categories import map_job_categories
from transform.map_country_codes import map_country_codes
from transform.out_of_scope import out_of_scope
from load.load_csv import archive_csv_df, load_df_to_bq


@functions_framework.cloud_event
def trigger_gcs(cloud_event: CloudEvent) -> None:
    """Triggered by a change in a storage bucket. Adds detailed logging and error handling."""
    print("--- Function execution started ---")

    data = cloud_event.data
    print(f"Received event data: {data}")

    event_id = cloud_event["id"]
    event_type = cloud_event["type"]

    bucket = data["bucket"]
    name = data["name"]
    metageneration = data["metageneration"]
    time_created = data["timeCreated"]
    updated = data["updated"]

    # --- Existing Event Detail Logging ---
    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Bucket: {bucket}")
    print(f"File: {name}")
    print(f"Metageneration: {metageneration}")
    print(f"Created: {time_created}")
    print(f"Updated: {updated}")

    if 'csv' in name.lower():
        print(f"File '{name}' is a CSV. Starting ETL process.") # Log start ETL

        # --- Extraction ---
        df = extract_csv(bucket, name)
        print(f"Step: extract_csv complete. DF Shape: {df.shape if df is not None else 'None'}")

        # --- Transformations ---
        df = standardize_format(df)
        print(f"Step: standardize_format completed. DF shape: {df.shape}")

        df = drop_nulls(df)
        print(f"Step: drop_nulls completed. DF shape: {df.shape}")

        df = clean_salary(df)
        print(f"Step: clean_salary completed. DF shape: {df.shape}")

        df = map_country_codes(df)
        print(f"Step: map_country_codes completed. DF shape: {df.shape}")

        df = map_job_categories(df)
        print(f"Step: map_job_categories completed. DF shape: {df.shape}")

        df = out_of_scope(df)
        print(f"Step: out_of_scope completed. DF shape: {df.shape}")

        # --- Loading into BigQuery ---
        print(f"Step: Calling load_df_to_bq for file '{name}'...")
        load_df_to_bq(df, name)
        print("Step: load_df_to_bq completed.")

        # --- Archiving ---
        archive_csv_df(df, name)
        print("Step: archive_csv_df completed.")

        print("--- ETL process completed successfully for CSV file ---")
    else:
        print(f"File '{name}' is not a CSV. Skipping ETL process.")
