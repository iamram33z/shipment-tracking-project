import os
import json
import re
from google.cloud import bigquery, storage
from dotenv import load_dotenv
from google.cloud.bigquery import DatasetReference

# Load environment variables
load_dotenv()

CLOUD_STORAGE_BUCKET = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
BIGQUERY_DATASET = os.getenv("GOOGLE_BIGQUERY_DATASET_NAME")
SQL_FILE_PATH = "database/create_tables.sql"

# Initialize BigQuery and Cloud Storage clients
bigquery_client = bigquery.Client()
storage_client = storage.Client()

def extract_table_names(sql_file_path):
    """Extracts table names from a SQL file."""
    table_names = []
    try:
        with open(sql_file_path, "r") as sql_file:
            sql_content = sql_file.read()
            pattern = r"CREATE TABLE IF NOT EXISTS\s+`?{}.(\w+)`?".format(BIGQUERY_DATASET)
            matches = re.findall(pattern, sql_content)
            table_names = matches
    except FileNotFoundError:
        print(f"Error: SQL file not found at {sql_file_path}")
    return table_names

def transform_and_load(request):
    try:
        table_names = extract_table_names(SQL_FILE_PATH)
        if not table_names:
            return "Error: Could not extract table names from SQL."

        # List files in Cloud Storage
        bucket = storage_client.bucket(CLOUD_STORAGE_BUCKET)
        blobs = bucket.list_blobs(prefix="raw/")

        # Process each file
        for blob in blobs:
            # Read the file
            data = json.loads(blob.download_as_text())

            # Transform the data
            tables_data = {table_name: [] for table_name in table_names} #create a dictionary of lists.
            for record in data:
                event = record.get("equipmentEvent", {})
                if event:
                    equipment_event = {
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
                    }
                    tables_data["EquipmentEvent"].append(equipment_event)

                    # Add logic for other tables.
                    for doc_ref in event.get("documentReferences", []):
                        tables_data["DocumentReferences"].append({
                            "documentReferenceID": doc_ref.get("documentReferenceValue"),
                            "documentReferenceType": doc_ref.get("documentReferenceType"),
                            "documentReferenceValue": doc_ref.get("documentReferenceValue"),
                        })
                    event_location = event.get("eventLocation", {})
                    tables_data["EventLocation"].append({
                        "eventLocationID": event_location.get("unlocationCode"),
                        "city": event_location.get("address", {}).get("city"),
                        "country": event_location.get("address", {}).get("country"),
                        "floor": event_location.get("address", {}).get("floor"),
                        "name": event_location.get("address", {}).get("name"),
                        "postCode": event_location.get("address", {}).get("postCode"),
                        "stateRegion": event_location.get("address", {}).get("stateRegion"),
                        "street": event_location.get("address", {}).get("street"),
                        "streetNumber": event_location.get("address", {}).get("streetNumber"),
                        "facilityCode": event_location.get("facilityCode"),
                        "facilityCodeListProvider": event_location.get("facilityCodeListProvider"),
                        "latitude": event_location.get("latitude"),
                        "longitude": event_location.get("longitude"),
                        "locationName": event_location.get("locationName"),
                        "unlocationCode": event_location.get("unlocationCode"),
                    })

                    for seal in event.get("seals", []):
                        tables_data["Seals"].append({
                            "sealID": seal.get("sealNumber"),
                            "sealNumber": seal.get("sealNumber"),
                            "sealSource": seal.get("sealSource"),
                            "sealType": seal.get("sealType"),
                        })
                    transport_call = event.get("transportCall", {})
                    tables_data["TransportCall"].append({
                        "transportCallID": transport_call.get("transportCallID"),
                        "carrierServiceCode": transport_call.get("carrierServiceCode"),
                        "exportVoyageNumber": transport_call.get("exportVoyageNumber"),
                        "facilityCode": transport_call.get("facilityCode"),
                        "facilityCodeListProvider": transport_call.get("facilityCodeListProvider"),
                        "facilityTypeCode": transport_call.get("facilityTypeCode"),
                        "importVoyageNumber": transport_call.get("importVoyageNumber"),
                        "modeOfTransport": transport_call.get("modeOfTransport"),
                        "vesselCallSignNumber": transport_call.get("vessel", {}).get("vesselCallSignNumber"),
                        "vesselFlag": transport_call.get("vessel", {}).get("vesselFlag"),
                        "vesselIMONumber": transport_call.get("vessel", {}).get("vesselIMONumber"),
                        "vesselName": transport_call.get("vessel", {}).get("vesselName"),
                        "vesselOperatorCarrierCode": transport_call.get("vessel", {}).get("vesselOperatorCarrierCode"),
                        "vesselOperatorCarrierCodeListProvider": transport_call.get("vessel", {}).get("vesselOperatorCarrierCodeListProvider"),
                    })

            # Load data into BigQuery
            dataset_ref = DatasetReference(bigquery_client.project, BIGQUERY_DATASET)
            for table_name, rows in tables_data.items():
                if rows:
                    table_ref = dataset_ref.table(table_name)
                    errors = bigquery_client.insert_rows_json(table_ref, rows)

                    if errors:
                        print(f"Errors occurred while inserting rows into {table_name}: {errors}")
                    else:
                        print(f"Successfully loaded {len(rows)} records into {table_name}.")

        return "Data transformation and loading completed successfully."

    except Exception as e:
        print(f"An error occurred: {e}")
        return f"Failed to process data: {e}"

