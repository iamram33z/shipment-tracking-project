from airflow import DAG
from airflow.providers.google.cloud.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Airflow Configuration
DAG_BUCKET = os.getenv("DAG_BUCKET")

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 3, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Instantiate the DAG
dag = DAG(
    'firestore_to_bigquery',
    default_args=default_args,
    description='Firestore to GCS and then from GCS to BigQuery',
    schedule_interval=timedelta(minutes=30),  # Run every 30 minutes
    catchup=False,
)

# Task 1: Move data from Firestore to GCS
def run_firestore_to_gcs():
    # Here, you can use the DAG_BUCKET variable in your Firestore to GCS logic
    subprocess.run(['python', 'firestore_to_gcs.py', DAG_BUCKET], check=True)

# Task 2: Transform and load data into BigQuery
def run_transform_and_load():
    subprocess.run(['python', 'transform_and_load.py'], check=True)

# Define tasks using PythonOperator
task_1 = PythonOperator(
    task_id='move_data_to_gcs',
    python_callable=run_firestore_to_gcs,
    dag=dag,
)

task_2 = PythonOperator(
    task_id='transform_and_load_data',
    python_callable=run_transform_and_load,
    dag=dag,
)

# Set task dependencies
task_1 >> task_2  # Ensure task_2 runs only after task_1 completes
