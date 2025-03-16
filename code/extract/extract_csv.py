from google.cloud import storage
import pandas as pd
from io import StringIO

def extract_csv(bucket, blob_name):
    """Extracts a CSV from GCS and returns a pandas DataFrame."""
    storage_client = storage.Client()
    bucket_obj = storage_client.bucket(bucket)
    blob = bucket_obj.blob(blob_name)
    csv_content = blob.download_as_text()  # Download as text
    df = pd.read_csv(StringIO(csv_content))
    return df