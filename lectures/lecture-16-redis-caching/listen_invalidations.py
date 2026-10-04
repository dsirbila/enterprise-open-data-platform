"""lecture 16 lab: Pub/Sub cache invalidation — subscriber (ცალკე ტერმინალში გასაშვები)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.caching.redis_cache import RedisCache
from src.ingestion.logging_config import setup_logging

CHANNEL = "cache-invalidation"

def main() -> None:
    setup_logging()
    cache = RedisCache(host="localhost", port=6379)
    print(f"ველოდები invalidation შეტყობინებებს არხზე '{CHANNEL}'... (Ctrl+C გაჩერებისთვის)")
    cache.listen_for_invalidations(CHANNEL)

if __name__ == "__main__":
    main()
