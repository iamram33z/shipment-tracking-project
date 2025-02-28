import os
import json
from google.cloud import firestore
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Firestore Configuration
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
project_id = os.getenv("GOOGLE_FIRESTORE_PROJECT_ID")
database_name = os.getenv("GOOGLE_FIRESTORE_DATABASE_NAME")
collection_name = os.getenv("GOOGLE_FIRESTORE_COLLECTION_NAME")

# Initialize Firestore client
def initialize_firestore():
    try:
        # Set the environment variable for the credentials
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path

        # Initialize Firestore client
        db = firestore.Client(project=project_id, database=database_name)
        print("Firestore client initialized successfully!")
        return db
    except Exception as e:
        print(f"Failed to initialize Firestore: {e}")
        exit(1)

# Upsert data into Firestore
def upsert_data_to_firestore(db, collection_name, data):
    try:
        collection_ref = db.collection(collection_name)

        for idx, record in enumerate(data, start=1):
            event_data = record.get("equipmentEvent", {})
            document_id = event_data.get("eventID")  # Extract eventID as the unique identifier

            if not document_id:
                print(f"Skipping record {idx}: Missing 'eventID' field.")
                continue  # Skip if no eventID is found

            # Upsert logic: If document with eventID exists, update it; otherwise, insert a new one
            doc_ref = collection_ref.document(document_id)
            doc_ref.set(event_data, merge=True)  # 'merge=True' ensures upsert behavior

            print(f"{idx}: Data upserted successfully (eventID: {document_id})")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Initialize Firestore
    db = initialize_firestore()

    # Load data from events.json
    with open("pre_project/events.json", "r") as file:
        data = json.load(file)
        print("Data loaded successfully!")

    # Upsert data into Firestore
    upsert_data_to_firestore(db, collection_name, data)