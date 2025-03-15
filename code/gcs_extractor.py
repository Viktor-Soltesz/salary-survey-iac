"""
Module for extracting data from Google Cloud Storage.
"""
import pandas as pd
from google.cloud import storage
from io import StringIO

def extract_data_from_gcs(bucket_name: str, file_name: str) -> pd.DataFrame:
    """
    Extracts a CSV file from Google Cloud Storage and returns it as a pandas DataFrame.

    Args:
        bucket_name: The name of the GCS bucket.
        file_name: The name of the file in the bucket.

    Returns:
        A pandas DataFrame containing the data from the CSV file.

    Raises:
        FileNotFoundError: If the file does not exist in the bucket.
        ValueError: If the file is not a CSV.
    """
    print(f"Extracting file: {file_name} from bucket: {bucket_name}.")

    if not file_name.endswith('.csv'):
        raise ValueError("File is not a CSV.")

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    if not blob.exists():
        raise FileNotFoundError(f"File {file_name} not found in bucket {bucket_name}")

    csv_data = blob.download_as_text()
    df = pd.read_csv(StringIO(csv_data))
    print(f"File loaded to dataframe. shape {df.shape}")
    return df
