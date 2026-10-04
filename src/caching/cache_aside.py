"""lecture 16: Cache-Aside პატერნი — generic, cache-ის იმპლემენტაციისგან დამოუკიდებელი."""
import logging
from typing import Any, Callable

logger = logging.getLogger(__name__)

def get_or_fetch(cache: Any, key: str, ttl_seconds: int, fetch_fn: Callable[[], Any]) -> Any:
    """
    Cache-Aside პატერნი: ჯერ cache-ს ვკითხულობთ, cache miss-ზე fetch_fn()-ს ვიძახებთ
    და შედეგს cache-ში ვინახავთ. cache-ს მხოლოდ .get()/.set() სჭირდება — ეს ფუნქცია
    არ იცის, Redis-ია მიღმა თუ სხვა რამ (testable FakeCache-ითაც).
    """
    cached = cache.get(key)
    if cached is not None:
        logger.info("CACHE HIT: %s", key)
        return cached

    logger.info("CACHE MISS: %s — API-ს ვეკითხებით", key)
    value = fetch_fn()
    cache.set(key, value, ttl_seconds)
    return value
