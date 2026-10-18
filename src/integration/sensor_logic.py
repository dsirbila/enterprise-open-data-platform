"""lecture 18: Sensor-ის ლოგიკა — testable, Airflow-ის BaseSensorOperator/@task.sensor-ისგან დამოუკიდებელი."""
import logging

logger = logging.getLogger(__name__)

def check_for_new_files(sftp_client, remote_dir: str) -> bool:
    """აბრუნებს True-ს, თუ remote_dir-ში ახალი ფაილია."""
    files = sftp_client.list_new_files(remote_dir)
    if files:
        logger.info("Sensor: ნაპოვნია %d ახალი ფაილი: %s", len(files), files)
        return True

    logger.info("Sensor: ჯერ არცერთი ახალი ფაილი — ველოდებით...")
    return False
