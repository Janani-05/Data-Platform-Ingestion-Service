# function/main.py

from google.cloud import storage, bigquery
import json
import os

def gcs_to_bq_ingestor(event, context):
    """
    Triggered by a metadata.json upload to GCS.
    Reads metadata, creates BigQuery dataset/table,
    and loads the CSV data into BigQuery.
    """

    print("Cloud Function Triggered!")
    bucket_name = event['bucket']
    file_name = event['name']
    print(f"📂 File uploaded: {file_name} in bucket: {bucket_name}")

    if not file_name.endswith("metadata.json"):
        print(" Not a metadata file — skipping.")
        return "Skipped non-metadata file."

    # Initialize clients
    storage_client = storage.Client()
    bq_client = bigquery.Client()

    # Download metadata.json file
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    metadata_content = blob.download_as_text()
    metadata = json.loads(metadata_content)

    print(" Metadata content:", metadata)

    # Extract fields from metadata.json
    dataset_name = metadata["target_dataset"]
    table_name = metadata["target_table"]
    source_file = metadata["source_file"]
    schema = metadata["schema"]
    description = metadata["table_description"]
    owner_email = metadata["owner_email"]

    # Create dataset if it doesn't exist
    dataset_id = f"{bq_client.project}.{dataset_name}"
    dataset = bigquery.Dataset(dataset_id)
    if not dataset_exists(bq_client, dataset_id):
        dataset.description = f"Dataset for {dataset_name}"
        bq_client.create_dataset(dataset)
        print(f" Created dataset: {dataset_name}")

    # Create table if it doesn't exist
    table_id = f"{dataset_id}.{table_name}"
    if not table_exists(bq_client, table_id):
        schema_fields = [bigquery.SchemaField(s["name"], s["type"], mode=s["mode"]) for s in schema]
        table = bigquery.Table(table_id, schema=schema_fields)
        table.description = description
        table.labels = {"owner_email": owner_email}
        bq_client.create_table(table)
        print(f" Created table: {table_name}")

    # Load data from CSV into BigQuery
    source_uri = f"gs://{bucket_name}/{source_file}"
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1
    )

    load_job = bq_client.load_table_from_uri(source_uri, table_id, job_config=job_config)
    load_job.result()  # Wait for completion

    print(f" Loaded data from {source_file} into {table_id}")
    return "Ingestion completed successfully"


def dataset_exists(client, dataset_id):
    try:
        client.get_dataset(dataset_id)
        return True
    except Exception:
        return False


def table_exists(client, table_id):
    try:
        client.get_table(table_id)
        return True
    except Exception:
        return False

