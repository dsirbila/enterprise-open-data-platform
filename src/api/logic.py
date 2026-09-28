"""lecture 12: FastAPI-ის უკან მდგარი ბიზნეს-ლოგიკა — testable, framework-ისგან დამოუკიდებელი."""
from typing import Any
from datetime import date, timedelta

CITY_COORDS = {
    "Tbilisi": (41.7151, 44.8271),
    "Batumi": (41.6168, 41.6367),
    "Kutaisi": (42.2679, 42.7000),
    "Telavi": (41.9189, 45.4739),
}

class UnknownCityError(Exception):
    """მოთხოვნილი ქალაქი CITY_COORDS-ში არ არსებობს."""

class UnknownEventError(Exception):
    """მოთხოვნილი მიწისძვრა მითითებული ID-ით ვერ მოიძებნა."""

def get_weather_for_city(client: Any, city: str) -> dict:
    if city not in CITY_COORDS:
        raise UnknownCityError(f"უცნობი ქალაქი: {city}")
    lat, lon = CITY_COORDS[city]
    data = client.fetch(lat, lon, city)
    current = data["current"]
    return {
        "city": city,
        "temperature_c": current["temperature_2m"],
        "wind_speed_kmh": current["wind_speed_10m"],
    }

def get_currency_rates(client: Any) -> dict:
    entry = client.get_rates()
    return {
        "date": entry["date"],
        "rates": [
            {"code": c["code"], "name": c["name"], "quantity": c["quantity"], "rate": c["rate"]}
            for c in entry["currencies"]
        ],
    }

def get_seismic_events(client: Any, start_date: str, end_date: str, min_magnitude: float = 1.5) -> list:
    return client.get_recent_events(start_date, end_date, min_magnitude)

def get_seismic_event_by_id(client: Any, event_id: str) -> dict:
    # ვიყენებთ რეალურ დინამიკურ თარიღებს (ბოლო 30 დღე), რომ მომავალ დროში არ გადავიდეთ
    end_date = str(date.today())
    start_date = str(date.today() - timedelta(days=30))
    
    events = client.get_recent_events(start_date, end_date, 0.0)
    event = next((e for e in events if e.get("event_id") == event_id), None)
    
    if not event:
        raise UnknownEventError(f"მიწისძვრა ID-ით '{event_id}' ვერ მოიძებნა.")
    return event
