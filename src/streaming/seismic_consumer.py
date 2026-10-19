"""lecture 19: Kafka Consumer — მიღებული მოვლენების დამუშავება."""
import logging
from confluent_kafka import Consumer
from src.streaming.event_transform import MessageValidationError, parse_kafka_message

logger = logging.getLogger(__name__)
TOPIC = "seismic-events"

def consume_events(
    bootstrap_servers: str = "localhost:9092",
    group_id: str = "seismic-consumer-group",
    max_messages: int = 100,
) -> int:
    consumer = Consumer(
        {
            "bootstrap.servers": bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": "earliest",
        }
    )
    consumer.subscribe([TOPIC])

    processed = 0
    try:
        while processed < max_messages:
            msg = consumer.poll(timeout=5.0)
            if msg is None:
                break
            if msg.error():
                logger.error("Consumer error: %s", msg.error())
                continue

            try:
                event = parse_kafka_message(msg.value())
            except MessageValidationError as exc:
                logger.error("არასწორი message, გამოტოვება: %s", exc)
                continue

            logger.info(
                "მიღებულია: %s magnitude=%s place=%s",
                event["event_id"], event["magnitude"], event["place"],
            )
            processed += 1
    finally:
        consumer.close()

    return processed

if __name__ == "__main__":
    import logging as _logging
    _logging.basicConfig(level=_logging.INFO)
    consume_events()
