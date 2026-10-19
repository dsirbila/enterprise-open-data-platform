"""lecture 19: Kafka Producer — USGS მიწისძვრების event stream."""
import logging
from datetime import date, timedelta
from confluent_kafka import Producer
from src.ingestion.seismic_client import SeismicAPIError, SeismicClient
from src.streaming.event_transform import seismic_event_to_kafka_message

logger = logging.getLogger(__name__)
TOPIC = "seismic-events"

def delivery_report(err, msg) -> None:
    if err is not None:
        logger.error("Message delivery ჩავარდა: %s", err)
    else:
        logger.info("Message delivered: %s [partition %d]", msg.topic(), msg.partition())

def produce_recent_events(bootstrap_servers: str = "localhost:9092") -> int:
    producer = Producer({"bootstrap.servers": bootstrap_servers})
    client = SeismicClient()

    end_date = date.today().isoformat()
    start_date = (date.today() - timedelta(days=2)).isoformat()

    try:
        events = client.get_recent_events(start_date, end_date, min_magnitude=1.5)
    except SeismicAPIError as exc:
        logger.error("USGS fetch ჩავარდა: %s", exc)
        return 0

    for event in events:
        message = seismic_event_to_kafka_message(event)
        producer.produce(
            TOPIC,
            key=event["event_id"].encode("utf-8"),
            value=message,
            callback=delivery_report,
        )

    producer.flush()
    logger.info("გაგზავნილია %d event Kafka topic-ში: %s", len(events), TOPIC)
    return len(events)

if __name__ == "__main__":
    import logging as _logging
    _logging.basicConfig(level=_logging.INFO)
    produce_recent_events()