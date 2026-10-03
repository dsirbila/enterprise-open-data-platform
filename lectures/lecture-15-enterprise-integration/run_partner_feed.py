"""lecture 15 lab: Partner Feed ორკესტრაცია — SFTP-დან ჩამოტვირთვა,
დამუშავება, ACK/NACK-ის უკან ატვირთვა, ფაილის არქივში გადატანა."""
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from dotenv import load_dotenv
from src.integration.batch_processor import process_batch_file
from src.integration.sftp_client import SFTPClient, SFTPIntegrationError
from src.ingestion.logging_config import setup_logging

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

UPLOAD_DIR = "upload"
PROCESSED_DIR = "processed"
ACK_DIR = "ack"

def main() -> int:
    setup_logging()
    client = SFTPClient(
        host=os.getenv("SFTP_HOST", "localhost"),
        port=int(os.getenv("SFTP_PORT", "2222")),
        username=os.getenv("SFTP_USER", "partner"),
        password=os.getenv("SFTP_PASSWORD", "partnerpass"),
    )

    processed_count = 0
    failed_count = 0

    try:
        with client:
            files = client.list_new_files(UPLOAD_DIR)
            print(f"ნაპოვნია {len(files)} ახალი ფაილი: {files}")

            for filename in files:
                with tempfile.TemporaryDirectory() as tmp:
                    local_path = os.path.join(tmp, filename)
                    client.download(f"{UPLOAD_DIR}/{filename}", local_path)

                    with open(local_path, encoding="utf-8") as f:
                        content = f.read()

                    response_xml, success = process_batch_file(filename, content)

                    ack_filename = f"{filename}.ack.xml" if success else f"{filename}.nack.xml"
                    ack_local_path = os.path.join(tmp, ack_filename)
                    with open(ack_local_path, "w", encoding="utf-8") as f:
                        f.write(response_xml)

                    client.upload(ack_local_path, f"{ACK_DIR}/{ack_filename}")
                    client.move_remote(f"{UPLOAD_DIR}/{filename}", f"{PROCESSED_DIR}/{filename}")

                    if success:
                        processed_count += 1
                        print(f"[OK] {filename} — დამუშავდა, ACK ატვირთულია")
                    else:
                        failed_count += 1
                        print(f"[FAIL] {filename} — ჩავარდა, NACK ატვირთულია")

    except SFTPIntegrationError as exc:
        print(f"[FAIL] SFTP შეცდომა: {exc}")
        return 1

    print(f"\nსულ: {processed_count} წარმატებული, {failed_count} ჩავარდნილი")
    return 0

if __name__ == "__main__":
    sys.exit(main())
