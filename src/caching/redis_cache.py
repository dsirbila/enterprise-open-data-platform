"""lecture 16: RedisCache — production wrapper redis-py-ს გარშემო."""
import json
import logging
from typing import Any, Optional
import redis

logger = logging.getLogger(__name__)

class RedisCache:
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0) -> None:
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def get(self, key: str) -> Optional[Any]:
        raw = self.client.get(key)
        return json.loads(raw) if raw is not None else None

    def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        self.client.setex(key, ttl_seconds, json.dumps(value))

    def delete(self, key: str) -> None:
        self.client.delete(key)

    # ---------- Pub/Sub invalidation ----------
    def publish_invalidation(self, channel: str, key: str) -> None:
        self.client.publish(channel, key)
        logger.info("INVALIDATION გამოქვეყნდა: channel=%s, key=%s", channel, key)

    def listen_for_invalidations(self, channel: str):
        pubsub = self.client.pubsub()
        pubsub.subscribe(channel)
        for message in pubsub.listen():
            if message["type"] != "message":
                continue
            invalidated_key = message["data"]
            self.delete(invalidated_key)
            logger.info("INVALIDATED (Pub/Sub-იდან): %s", invalidated_key)
