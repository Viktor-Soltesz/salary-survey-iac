"""
ETL Pipeline for CSV files in Google Cloud Storage
"""

import functions_framework
from cloudevents.http import CloudEvent
import traceback
#import time
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
    """
    Triggered by a change in a storage bucket. Adds detailed logging and error handling.
    """
    print("--- Function execution started ---") # Log entry

    try:
        data = cloud_event.data
        print(f"Received event data: {data}") # Log full event payload

        event_id = cloud_event["id"]
        event_type = cloud_event["type"]

        bucket = data["bucket"]
        name = data["name"]
        metageneration = data["metageneration"]
        timeCreated = data["timeCreated"]
        updated = data["updated"]

        # --- Existing Event Detail Logging ---
        print(f"Event ID: {event_id}")
        print(f"Event type: {event_type}")
        print(f"Bucket: {bucket}")
        print(f"File: {name}")
        print(f"Metageneration: {metageneration}")
        print(f"Created: {timeCreated}")
        print(f"Updated: {updated}")
        # ------------------------------------

        # --- Optional: Test for timing issue ---
        # print("Pausing for 2 seconds before processing...") # <<<  for timing test
        # time.sleep(2)                                      # <<< for timing test
        # ----------------------------------------

        print(f"Checking if file '{name}' is a CSV...") # Log check
        if 'csv' in name.lower(): # Check lower case just in case
            print(f"File '{name}' is a CSV. Starting ETL process.") # Log start ETL

            # --- Extraction ---
            print("Step: Calling extract_csv...")
            df = extract_csv(bucket, name)
            print(f"Step: extract_csv completed. DataFrame shape: {df.shape if df is not None else 'None'}")

            # --- Transformations ---
            print("Step: Calling standardize_format...")
            df = standardize_format(df)
            print(f"Step: standardize_format completed. DataFrame shape: {df.shape}")

            print("Step: Calling drop_nulls...")
            df = drop_nulls(df)
            print(f"Step: drop_nulls completed. DataFrame shape: {df.shape}")

            print("Step: Calling clean_salary...")
            df = clean_salary(df)
            print(f"Step: clean_salary completed. DataFrame shape: {df.shape}")

            print("Step: Calling map_country_codes...")
            df = map_country_codes(df)
            print(f"Step: map_country_codes completed. DataFrame shape: {df.shape}")

            print("Step: Calling map_job_categories...")
            df = map_job_categories(df)
            print(f"Step: map_job_categories completed. DataFrame shape: {df.shape}")

            print("Step: Calling out_of_scope...")
            df = out_of_scope(df)
            print(f"Step: out_of_scope completed. DataFrame shape: {df.shape}")

            # --- Loading into BigQuery ---
            print(f"Step: Calling load_df_to_bq for file '{name}'...")
            load_df_to_bq(df, name)
            print("Step: load_df_to_bq completed.") # This log appears AFTER BQ load

            # --- Archiving ---
            print(f"Step: Calling archive_csv_df for file '{name}'...")
            archive_csv_df(df, name)
            print("Step: archive_csv_df completed.")

            print("--- ETL process completed successfully for CSV file ---")

        else:
            print(f"File '{name}' is not a CSV. Skipping ETL process.") # Log skip

    except Exception as e:
        # --- Catch and log ANY exception during the process ---
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"ERROR encountered during execution: {e}")
        print("Traceback:")
        traceback.print_exc() # Prints the full stack trace
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # Optionally re-raise to mark the function execution as failed
        # raise e

    finally:
        # This will run whether there was an error or not
        print("--- Function execution finished ---") # Log exit
