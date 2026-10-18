"""lecture 18: Sensor DAG — ელოდება SFTP-ზე ახალ partner ფაილს, მერე processing-ს იწყებს."""
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.sensors.base import PokeReturnValue
from src.integration.sensor_logic import check_for_new_files
from src.integration.sftp_client import SFTPClient

default_args = {
    "owner": "data-engineering",
    "retries": 1,
}

@dag(
    dag_id="partner_feed_sensor",
    schedule="*/10 * * * *",
    start_date=datetime(2026, 8, 1),
    catchup=False,
    default_args=default_args,
    tags=["sensor", "sftp", "integration"],
)
def partner_feed_sensor_dag():
    @task.sensor(poke_interval=30, timeout=600, mode="reschedule")
    def wait_for_partner_file() -> PokeReturnValue:
        with SFTPClient(host="sftp", port=22, username="partner", password="partnerpass") as client:
            is_ready = check_for_new_files(client, "upload")
            files = client.list_new_files("upload") if is_ready else []
        return PokeReturnValue(is_done=is_ready, xcom_value=files)

    @task
    def process_files(files: list) -> str:
        processed = 0
        with SFTPClient(host="sftp", port=22, username="partner", password="partnerpass") as client:
            for filename in files:
                processed += 1
        return f"დამუშავებულია {processed} ფაილი"

    files = wait_for_partner_file()
    process_files(files)

partner_feed_sensor_dag()
