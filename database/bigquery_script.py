import os
from google.cloud import bigquery
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# BigQuery Configuration
project_id = os.getenv("GOOGLE_BIGQUERY_PROJECT_ID")
dataset_id = os.getenv("GOOGLE_BIGQUERY_DATASET_NAME")


def run_bigquery_query(project_id, sql_query):
    """
    Connects to BigQuery, runs a SQL query, and returns the results.

    Args:
        project_id (str): Your Google Cloud project ID.
        sql_query (str): The SQL query to execute.

    Returns:
        list: A list of rows from the query result.
        None: If an error occurs.
    """
    try:
        client = bigquery.Client(project=project_id)

        query_job = client.query(sql_query)  # Make an API request.

        results = list(query_job.result())  # Waits for query to finish

        return results

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# If main is run directly, execute the query
if __name__ == "__main__":
    if not all([project_id, dataset_id]):
        print(
            "Error: Missing one or more required environment variables (GOOGLE_BIGQUERY_PROJECT_ID, GOOGLE_BIGQUERY_DATASET_NAME)."
        )
        exit(1)

    # Load SQL query from file
    sql_file_path = "database/create_tables.sql"  # Replace with your SQL file path
    try:
        with open(sql_file_path, "r") as sql_file:
            sql_query = sql_file.read()
    except FileNotFoundError:
        print(f"Error: SQL file not found at {sql_file_path}")
        exit(1)

    results = run_bigquery_query(project_id, sql_query)

    if results is not None:
        print("Tables created/verified successfully.")
        # Optionally, print the results of the query (if any).
        # for row in results:
        #     print(row)
    else:
        print("Table creation failed, check logs for errors")