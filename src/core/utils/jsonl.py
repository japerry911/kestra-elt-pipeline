import json

from google.cloud import storage


def convert_to_jsonl_and_upload_to_gcs(
    data: list[dict],
    bucket_name: str,
    file_name: str,
):
    """
    Convert a list of dictionaries to JSONL file and uploads to GCS bucket.


    Args:
        data (list[dict]): List of dictionaries (JSON objects)
        bucket_name (str): Name of the GCS bucket
        file_name (str): Name of the file to upload
    """
    jsonl_string = "\n".join(json.dumps(item) for item in data)

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(file_name)

    blob.upload_from_string(jsonl_string)
