"""lecture 19/20: Seismic Producer — კოორდინატებზე დაფუძნებული custom partitioning (west/east) ინტეგრაციით."""
import json
import random
from confluent_kafka import Producer
from src.streaming.partitioning import get_partition_key

TOPIC = "seismic-events"

def generate_dummy_event():
    # ვანაწილებთ თბილისის, ბათუმის და სხვა არეალის კოორდინატებზე
    locations = [
        ("Tbilisi", 41.7151, 44.8271),
        ("Batumi", 41.6168, 41.6367),
        ("Other", 45.0, 45.0)
    ]
    name, lat, lon = random.choice(locations)
    return {
        "event_id": f"evt-{random.randint(1000, 9999)}",
        "latitude": lat,
        "longitude": lon,
        "magnitude": round(random.uniform(2.0, 6.5), 1),
        "place": name
    }

def run_producer(bootstrap_servers: str = "localhost:9092", num_messages: int = 5):
    producer = Producer({"bootstrap.servers": bootstrap_servers})
    
    for _ in range(num_messages):
        event = generate_dummy_event()
        lat = event["latitude"]
        lon = event["longitude"]
        
        # ვადგენთ რეგიონს კოორდინატებით (west / east / unknown)
        partition_key = get_partition_key(lat, lon)
        
        value_bytes = json.dumps(event, ensure_ascii=False).encode("utf-8")
        key_bytes = partition_key.encode("utf-8")
        
        # ვუგზავნით კაფკას key-სთან ერთად, რომ ერთი რეგიონის მონაცემები ერთ partition-ში დაჯგუფდეს
        producer.produce(TOPIC, key=key_bytes, value=value_bytes)
        print(f"გაგზავნილია: {event['place']} (lat={lat}, lon={lon}) -> key: '{partition_key}'")
        
    producer.flush()
    print("[OK] Producer-მა წარმატებით გაგზავნა შეტყობინებები")

if __name__ == "__main__":
    run_producer()
