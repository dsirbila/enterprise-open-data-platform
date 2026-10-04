"""lecture 16 lab: Cache-Aside real Redis-ით — Open-Meteo API + TTL cache."""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.caching.cache_aside import get_or_fetch
from src.caching.redis_cache import RedisCache
from src.ingestion.logging_config import setup_logging
from src.ingestion.weather_client import WeatherClient

CACHE_TTL_SECONDS = 60

def main() -> None:
    setup_logging()
    cache = RedisCache(host="localhost", port=6379)
    client = WeatherClient()

    print("--- პირველი მოთხოვნა ---")
    start = time.perf_counter()
    result1 = get_or_fetch(
        cache, "weather:Tbilisi", CACHE_TTL_SECONDS,
        lambda: client.get_current_weather(),
    )
    print(f"დრო: {time.perf_counter() - start:.3f}s | {result1}")

    print("\n--- მეორე მოთხოვნა (იგივე წუთში — cache HIT მოსალოდნელია) ---")
    start = time.perf_counter()
    result2 = get_or_fetch(
        cache, "weather:Tbilisi", CACHE_TTL_SECONDS,
        lambda: client.get_current_weather(),
    )
    print(f"დრო: {time.perf_counter() - start:.3f}s | {result2}")

if __name__ == "__main__":
    main()
