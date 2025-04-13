"""
Extract CSV from Google Cloud Storage (GCS) and load into a pandas DataFrame.
"""

from io import StringIO
from google.cloud import storage
import pandas as pd

def extract_csv(bucket: str, blob_name: str) -> pd.DataFrame:
    """Extracts a CSV from GCS and returns a pandas DataFrame."""
    storage_client = storage.Client()
    bucket_obj = storage_client.bucket(bucket)
    blob = bucket_obj.blob(blob_name)
    csv_content = blob.download_as_text()  # Download as text
    df = pd.read_csv(StringIO(csv_content))
    return df
