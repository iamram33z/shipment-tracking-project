from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from google.cloud import firestore, bigquery
import polars as pl
import hashlib
import logging
import os

# Load environment variables
project_id = os.getenv("GOOGLE_FIRESTORE_PROJECT_ID")
database_name = os.getenv("GOOGLE_FIRESTORE_DATABASE_NAME")
collection_name = os.getenv("GOOGLE_FIRESTORE_COLLECTION_NAME")
bigquery_project_id = os.getenv("GOOGLE_BIGQUERY_PROJECT_ID")
bigquery_dataset_id = os.getenv("GOOGLE_BIGQUERY_DATASET_NAME")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Firestore and BigQuery clients
firestore_client = firestore.Client(project=project_id, database=database_name)
bigquery_client = bigquery.Client(project=bigquery_project_id)

# Function to process Firestore changes
def process_firestore_changes(**kwargs):
    def on_snapshot(doc_snapshot, changes, read_time):
        updated_docs = [doc for doc in changes if doc.type.name == 'MODIFIED']
        if not updated_docs:
            logging.info("No updated documents found.")
            return

        # Convert updated documents to JSON
        json_data = [doc.to_dict() for doc in updated_docs]

        # Create a Polars DataFrame from the JSON data
        df = pl.DataFrame(json_data)

        # Process the DataFrame (use your existing logic here)
        # Example: Flatten the main event fields
        df_events = df.select([
            pl.col("eventID").alias("eventID"),
            pl.col("eventCreatedDateTime").alias("eventCreatedDateTime"),
            pl.col("eventClassifierCode").alias("eventClassifierCode"),
            pl.col("equipmentEventTypeCode").alias("equipmentEventTypeCode"),
            pl.col("equipmentReference").alias("equipmentReference"),
            pl.col("eventDateTime").alias("eventDateTime"),
            pl.col("eventType").alias("eventType")
        ])

        # Parse string columns as datetime (including fractional seconds)
        df_events = df_events.with_columns([
            pl.col("eventCreatedDateTime").str.strptime(pl.Datetime, "%Y-%m-%dT%H:%M:%S%.f").alias("eventCreatedDateTime"),
            pl.col("eventDateTime").str.strptime(pl.Datetime, "%Y-%m-%dT%H:%M:%S%.f").alias("eventDateTime")
        ])

        # Convert datetime columns to ISO 8601 strings (without fractional seconds)
        df_events = df_events.with_columns([
            pl.col("eventCreatedDateTime").dt.strftime("%Y-%m-%dT%H:%M:%S").alias("eventCreatedDateTime"),
            pl.col("eventDateTime").dt.strftime("%Y-%m-%dT%H:%M:%S").alias("eventDateTime")
        ])

        # Upsert into BigQuery (use your existing logic here)
        upsert_to_bigquery(
            client=bigquery_client,
            table_id=f"{bigquery_project_id}.{bigquery_dataset_id}.EquipmentEvent",
            df=df_events,
            unique_key=["eventID"]
        )

    # Listen to Firestore changes
    firestore_client.collection(collection_name).on_snapshot(on_snapshot)

# Function to upsert data into BigQuery
def upsert_to_bigquery(client, table_id, df, unique_key):
    """
    Upserts data into a BigQuery table.

    Args:
        client: BigQuery client.
        table_id: Full table ID in the format 'project_id.dataset_id.table_id'.
        df: Polars DataFrame containing the data to upsert.
        unique_key: The unique key column(s) to match rows for upsert.
    """
    # Convert Polars DataFrame to Pandas DataFrame (BigQuery client works with Pandas)
    pandas_df = df.to_pandas()

    # Create a temporary table ID
    temp_table_id = f"{table_id}_temp"

    # Load the data into a temporary table
    job_config = bigquery.LoadJobConfig(
        autodetect=False,  # Disable autodetect to ensure schema matches
        write_disposition="WRITE_TRUNCATE",  # Overwrite the temporary table
    )

    # Load the DataFrame into the temporary table
    job = client.load_table_from_dataframe(pandas_df, temp_table_id, job_config=job_config)
    job.result()  # Wait for the job to complete

    # Construct the MERGE SQL statement
    columns = pandas_df.columns.tolist()
    set_clause = ", ".join(
        [
            f"{col} = SAFE_CAST(temp.{col} AS TIMESTAMP)"
            if col in ["eventCreatedDateTime", "eventDateTime"]
            else f"{col} = temp.{col}"
            for col in columns
        ]
    )
    insert_columns = ", ".join(columns)
    insert_values = ", ".join(
        [
            f"SAFE_CAST(temp.{col} AS TIMESTAMP)"
            if col in ["eventCreatedDateTime", "eventDateTime"]
            else f"temp.{col}"
            for col in columns
        ]
    )

    merge_sql = f"""
    MERGE `{table_id}` AS target
    USING `{temp_table_id}` AS temp
    ON {' AND '.join([f'target.{key} = temp.{key}' for key in unique_key])}
    WHEN MATCHED THEN
        UPDATE SET {set_clause}
    WHEN NOT MATCHED THEN
        INSERT ({insert_columns}) VALUES ({insert_values})
    """

    # Execute the MERGE statement
    query_job = client.query(merge_sql)
    query_job.result()  # Wait for the job to complete

    # Delete the temporary table
    client.delete_table(temp_table_id, not_found_ok=True)

    logging.info(f"Upserted data into {table_id} successfully!")

# Define the DAG
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
}

dag = DAG(
    'firestore_to_bigquery',
    default_args=default_args,
    description='Listen to Firestore changes and update BigQuery',
    schedule_interval='@once',  # Run once or set a schedule (e.g., '@daily')
    catchup=False,
)

# Define the task
process_firestore_task = PythonOperator(
    task_id='process_firestore_changes',
    python_callable=process_firestore_changes,
    provide_context=True,
    dag=dag,
)

# Set the task in the DAG
process_firestore_task