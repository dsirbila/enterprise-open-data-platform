"""lecture 16 lab: Pub/Sub cache invalidation — publisher. გაშვება: python publish_invalidation.py weather:Tbilisi"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.caching.redis_cache import RedisCache

CHANNEL = "cache-invalidation"

def main() -> None:
    if len(sys.argv) != 2:
        print("გამოყენება: python publish_invalidation.py <cache_key>")
        sys.exit(1)

    key = sys.argv[1]
    cache = RedisCache(host="localhost", port=6379)
    cache.publish_invalidation(CHANNEL, key)
    print(f"გამოქვეყნდა invalidation: {key}")

if __name__ == "__main__":
    main()
