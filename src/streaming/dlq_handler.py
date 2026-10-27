"""lecture 20: Dead Letter Queue — testable envelope-ის აწყობა, confluent_kafka-ისგან დამოუკიდებელი."""
import json
from datetime import datetime, timezone
from typing import Optional

def build_dlq_envelope(
    original_raw: bytes,
    error: Exception,
    source_topic: str,
    original_partition: Optional[int] = None,
    original_offset: Optional[int] = None,
) -> bytes:
    """
    ჩავარდნილ message-ს ახვევს 'envelope'-ში — ორიგინალი payload + error კონტექსტი +
    სად (topic/partition/offset) მოხდა ჩავარდნა. ეს envelope DLQ topic-ში იწერება.
    """
    try:
        original_decoded = original_raw.decode("utf-8")
    except UnicodeDecodeError:
        original_decoded = repr(original_raw)

    envelope = {
        "original_payload": original_decoded,
        "error_type": type(error).__name__,
        "error_message": str(error),
        "source_topic": source_topic,
        "original_partition": original_partition,
        "original_offset": original_offset,
        "failed_at": datetime.now(timezone.utc).isoformat(),
    }
    # ensure_ascii=False აუცილებელია, რომ ქართული ტექსტი escape-ების გარეშე წაკითხვადი დარჩეს
    return json.dumps(envelope, ensure_ascii=False).encode("utf-8")

def parse_dlq_envelope(raw: bytes) -> dict:
    """DLQ-დან წაკითხული envelope-ის დესერიალიზაცია — reprocessing/inspection tooling-ისთვის."""
    return json.loads(raw.decode("utf-8"))
