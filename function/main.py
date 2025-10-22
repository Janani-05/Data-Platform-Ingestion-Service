# function/main.py
def gcs_to_bq_ingestor(event, context):
    """
    This Cloud Function is triggered by a metadata.json upload to GCS.
    It reads the metadata, creates the BigQuery dataset/table,
    and loads the CSV data into BigQuery.
    """
    print("Function triggered!")
    print("Event data:", event)
    # Placeholder for reading metadata.json
    # Placeholder for creating dataset/table in BigQuery
    # Placeholder for loading CSV into BigQuery
    return "Ingestion function executed successfully"

