"""lecture 20: Consumer + Dead Letter Queue — ჩავარდნილი message-ები DLQ topic-ში გადადის."""
import logging
from confluent_kafka import Consumer, Producer
from src.streaming.dlq_handler import build_dlq_envelope
from src.streaming.event_transform import MessageValidationError, parse_kafka_message

logger = logging.getLogger(__name__)

TOPIC = "seismic-events"
DLQ_TOPIC = "seismic-events-dlq"

def consume_with_dlq(
    bootstrap_servers: str = "localhost:9092",
    group_id: str = "seismic-consumer-group",
    max_messages: int = 100,
) -> dict:
    consumer = Consumer(
        {
            "bootstrap.servers": bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": "earliest",
        }
    )
    dlq_producer = Producer({"bootstrap.servers": bootstrap_servers})
    consumer.subscribe([TOPIC])

    processed, sent_to_dlq = 0, 0
    try:
        while (processed + sent_to_dlq) < max_messages:
            msg = consumer.poll(timeout=5.0)
            if msg is None:
                break
            if msg.error():
                logger.error("Consumer error: %s", msg.error())
                continue

            try:
                event = parse_kafka_message(msg.value())
                logger.info("მიღებულია: %s", event["event_id"])
                processed += 1
            except MessageValidationError as exc:
                envelope = build_dlq_envelope(
                    msg.value(), exc,
                    source_topic=TOPIC,
                    original_partition=msg.partition(),
                    original_offset=msg.offset(),
                )
                dlq_producer.produce(DLQ_TOPIC, value=envelope)
                dlq_producer.flush()
                logger.warning("გადატანილია DLQ-ში (%s): %s", DLQ_TOPIC, exc)
                sent_to_dlq += 1
    finally:
        consumer.close()

    return {"processed": processed, "sent_to_dlq": sent_to_dlq}

if __name__ == "__main__":
    import logging as _logging
    _logging.basicConfig(level=_logging.INFO)
    result = consume_with_dlq()
    print(f"დამუშავდა: {result['processed']}, DLQ-ში გადავიდა: {result['sent_to_dlq']}")
