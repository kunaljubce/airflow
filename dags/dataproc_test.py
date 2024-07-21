from airflow import models
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocCreateBatchOperator,
    DataprocDeleteBatchOperator,
)

# Assuming the rest of your setup remains the same
PROJECT_ID = "airflow-gc-03072024"  # "{{ var.value.project_id }}"
REGION = "asia-south2"  # Updated to match your region
SUBNET = "airflow-gcp-subnet"
JAR_FILE_URI = "file:///usr/lib/spark/examples/jars/spark-examples.jar"
MAIN_CLASS = "org.apache.spark.examples.SparkPi"
ARGUMENTS = ["1000"]

default_args = {
    "start_date": days_ago(1),
    "project_id": PROJECT_ID,
}

with models.DAG(
    "dataproc_batch_operators_adjusted",
    default_args=default_args,
    schedule_interval=datetime.timedelta(days=1),
) as dag:
    create_batch = DataprocCreateBatchOperator(
        task_id="batch_create_adjusted",
        batch={
            "pyspark_batch": {
                "main_python_file_uri": PYTHON_FILE_LOCATION,  # Keep this if you're running a PySpark job
                "jar_file_uris": [JAR_FILE_URI],
                "args": ARGUMENTS,
            },
            "environment_config": {
                "master_config": {
                    "subnetwork_uri": SUBNET,
                },
                "worker_config": {
                    "num_workers": 2,  # Example number of workers; adjust as needed
                },
            },
        },
        batch_id="batch-create-adjusted",
    )

    # Add other operators as needed

    # Example: List batches operator
    list_batches = DataprocListBatchesOperator(task_id="list-all-batches-adjusted")

    # Connect the tasks as per your workflow
    create_batch >> list_batches
