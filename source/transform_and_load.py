import os
import json
from google.cloud import bigquery, storage

# Load environment variables
CLOUD_STORAGE_BUCKET = os.getenv("CLOUD_STORAGE_BUCKET")
BIGQUERY_DATASET = os.getenv("BIGQUERY_DATASET")
BIGQUERY_TABLE = os.getenv("BIGQUERY_TABLE")

# Initialize BigQuery and Cloud Storage clients
bigquery_client = bigquery.Client()
storage_client = storage.Client()

def transform_and_load(request):
    try:
        # List files in Cloud Storage
        bucket = storage_client.bucket(CLOUD_STORAGE_BUCKET)
        blobs = bucket.list_blobs(prefix="raw/")

        # Process each file
        for blob in blobs:
            # Read the file
            data = json.loads(blob.download_as_text())

            # Transform the data
            transformed_data = []
            for record in data:
                event = record.get("equipmentEvent", {})
                transformed_data.append({
                    "eventID": event.get("eventID"),
                    "equipmentEventTypeCode": event.get("equipmentEventTypeCode"),
                    "equipmentReference": event.get("equipmentReference"),
                    "eventClassifierCode": event.get("eventClassifierCode"),
                    "eventCreatedDateTime": event.get("eventCreatedDateTime"),
                    "eventDateTime": event.get("eventDateTime"),
                    "eventType": event.get("eventType"),
                    "documentReferenceID": event.get("documentReferences", [{}])[0].get("documentReferenceValue"),
                    "eventLocationID": event.get("eventLocation", {}).get("unlocationCode"),
                    "sealID": event.get("seals", [{}])[0].get("sealNumber"),
                    "transportCallID": event.get("transportCall", {}).get("transportCallID"),
                })

            # Load data into BigQuery
            table_ref = bigquery_client.dataset(BIGQUERY_DATASET).table(BIGQUERY_TABLE)
            errors = bigquery_client.insert_rows_json(table_ref, transformed_data)

            if errors:
                print(f"Errors occurred while inserting rows: {errors}")
            else:
                print(f"Successfully loaded {len(transformed_data)} records into BigQuery.")

        return "Data transformation and loading completed successfully."

    except Exception as e:
        print(f"An error occurred: {e}")
        return f"Failed to process data: {e}"