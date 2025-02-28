import os
import json
from google.cloud import firestore, storage
from google.api_core.exceptions import GoogleAPICallError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()  # Load .env file

BATCH_SIZE = int(os.getenv("BATCH_SIZE", 2000))  # Number of records per batch, default 2000
CLOUD_STORAGE_BUCKET = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
FIRESTORE_COLLECTION_NAME = os.getenv("GOOGLE_FIRESTORE_COLLECTION_NAME")

# Initialize Firestore and Cloud Storage clients
firestore_client = firestore.Client()
storage_client = storage.Client()
bucket = storage_client.bucket(CLOUD_STORAGE_BUCKET)


def move_data_to_gcs(request):
    try:
        # Query Firestore collection
        collection_ref = firestore_client.collection(FIRESTORE_COLLECTION_NAME)
        docs = collection_ref.limit(BATCH_SIZE).stream()

        # Convert Firestore documents to JSON
        data = [doc.to_dict() for doc in docs]

        # Upload JSON to Cloud Storage
        if data:
            blob = bucket.blob(f"raw/events_batch_{len(data)}.json")
            blob.upload_from_string(json.dumps(data))
            print(f"Uploaded {len(data)} records to Cloud Storage.")
        else:
            print("No more records to process.")

        # Delete processed documents (optional)
        for doc in docs:
            doc.reference.delete()

        return f"Successfully processed {len(data)} records."

    except GoogleAPICallError as e:
        print(f"An error occurred: {e}")
        return f"Failed to process records: {e}"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return f"Failed to process records: {e}"