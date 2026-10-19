"""lecture 19: Kafka message serialization/deserialization — testable, confluent_kafka-ისგან დამოუკიდებელი."""
import json

class MessageValidationError(Exception):
    """Kafka message-ის სერიალიზაცია/დესერიალიზაციისას წარმოქმნილი შეცდომა."""

def seismic_event_to_kafka_message(event: dict) -> bytes:
    """მიწისძვრის event dict-ს გარდაქმნის Kafka-ისთვის მზა JSON bytes-ად."""
    # ვამოწმებთ რამდენიმე შესაძლო გასაღებს უსაფრთხოებისთვის
    event_time = event.get("event_time") or event.get("time")
    
    payload = {
        "event_id": event.get("event_id") or event.get("id"),
        "magnitude": event.get("magnitude") if event.get("magnitude") is not None else event.get("mag"),
        "place": event.get("place"),
        "event_time": event_time.isoformat() if hasattr(event_time, "isoformat") else str(event_time),
        "latitude": event.get("latitude"),
        "longitude": event.get("longitude"),
        "depth_km": event.get("depth_km"),
    }
    return json.dumps(payload).encode("utf-8")

def parse_kafka_message(raw: bytes) -> dict:
    """Kafka-დან მიღებული raw bytes-ს parse უკეთებს და საბაზისო ვალიდაციას ატარებს."""
    try:
        data = json.loads(raw.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise MessageValidationError(f"არასწორი JSON message: {exc}") from exc

    required = {"event_id", "magnitude", "place", "event_time"}
    missing = required - set(data.keys())
    if missing:
        raise MessageValidationError(f"message-ს აკლია ველები: {missing}")

    return data