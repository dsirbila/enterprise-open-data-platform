"""lecture 15: Batch file processing + ACK/NACK generation — B2B partner feed simulation."""
import csv
import io
from datetime import datetime, timezone

class BatchProcessingError(Exception):
    """batch ფაილის დამუშავებისას წარმოქმნილი ნებისმიერი შეცდომა."""

REQUIRED_COLUMNS = {"event_id", "magnitude", "place", "event_time"}

def parse_batch_csv(content: str) -> list:
    reader = csv.DictReader(io.StringIO(content))
    rows = list(reader)
    if not rows:
        raise BatchProcessingError("ფაილი ცარიელია — 0 row")

    missing = REQUIRED_COLUMNS - set(rows[0].keys())
    if missing:
        raise BatchProcessingError(f"აკლია სავალდებულო სვეტები: {missing}")

    for i, row in enumerate(rows, start=1):
        try:
            float(row["magnitude"])
        except ValueError:
            raise BatchProcessingError(f"row {i}: არასწორი magnitude მნიშვნელობა: {row['magnitude']!r}")

    return rows

def generate_ack(filename: str, row_count: int) -> str:
    now = datetime.now(timezone.utc).isoformat()
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        "<ack>\n"
        f"  <file>{filename}</file>\n"
        "  <status>SUCCESS</status>\n"
        f"  <rows_processed>{row_count}</rows_processed>\n"
        f"  <timestamp>{now}</timestamp>\n"
        "</ack>\n"
    )

def generate_nack(filename: str, error_message: str) -> str:
    now = datetime.now(timezone.utc).isoformat()
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        "<nack>\n"
        f"  <file>{filename}</file>\n"
        "  <status>FAILED</status>\n"
        f"  <error>{error_message}</error>\n"
        f"  <timestamp>{now}</timestamp>\n"
        "</nack>\n"
    )

def process_batch_file(filename: str, content: str) -> tuple:
    """
    დაბრუნებს (ack_or_nack_xml, is_success)-ს — orchestrator-ისთვის მოსახერხებელი ინტერფეისი.
    """
    try:
        rows = parse_batch_csv(content)
    except BatchProcessingError as exc:
        return generate_nack(filename, str(exc)), False
    return generate_ack(filename, len(rows)), True
