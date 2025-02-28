import os
from google.cloud import firestore
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Firestore Configuration
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
project_id = os.getenv("GOOGLE_FIRESTORE_PROJECT_ID")
database_name = os.getenv("GOOGLE_FIRESTORE_DATABASE_NAME")

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

# Test Firestore connection
def test_firestore_connection(db):
    try:
        # Write a test document
        test_collection = db.collection("connection_test")
        test_doc = test_collection.document("ping")
        test_doc.set({"status": "connected"})

        # Read the test document
        result = test_doc.get()

        if result.exists:
            print("Firestore connection successful! Data:", result.to_dict())
        else:
            print( "Firestore connection failed!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    db = initialize_firestore()
    test_firestore_connection(db)