"""lecture 17: Airflow DAG-ის 'task ლოგიკა' — plain Python, Airflow-ისგან დამოუკიდებელი."""
import logging
from src.ingestion.currency_client import CurrencyAPIError, CurrencyClient
from src.ingestion.seismic_client import SeismicAPIError, SeismicClient
from src.ingestion.weather_client import WeatherAPIError, WeatherClient

logger = logging.getLogger(__name__)

CITIES = [
    ("Tbilisi", 41.7151, 44.8271),
    ("Batumi", 41.6168, 41.6367),
    ("Kutaisi", 42.2679, 42.7000),
    ("Telavi", 41.9189, 45.4739),
]

def fetch_weather_task() -> dict:
    """ყველა ქალაქის ამინდის fetch — Airflow task-ისთვის დაბრუნებული dict XCom-ში ჩაჯდება."""
    client = WeatherClient()
    results = {}
    errors = []
    for city, lat, lon in CITIES:
        try:
            data = client.fetch(lat, lon, city)
            results[city] = data["current"]["temperature_2m"]
        except WeatherAPIError as exc:
            errors.append(f"{city}: {exc}")

    logger.info("fetch_weather_task: %d/%d ქალაქი წარმატებული", len(results), len(CITIES))
    return {"results": results, "errors": errors}

def fetch_currency_task() -> dict:
    client = CurrencyClient()
    try:
        entry = client.get_rates()
    except CurrencyAPIError as exc:
        logger.error("fetch_currency_task ჩავარდა: %s", exc)
        return {"results": {}, "errors": [str(exc)]}

    rates = {c["code"]: c["rate"] for c in entry["currencies"]}
    logger.info("fetch_currency_task: %d ვალუტა მიღებულია", len(rates))
    return {"results": rates, "errors": []}

def fetch_seismic_task(start_date: str, end_date: str) -> dict:
    client = SeismicClient()
    try:
        events = client.get_recent_events(start_date, end_date, min_magnitude=1.5)
    except SeismicAPIError as exc:
        logger.error("fetch_seismic_task ჩავარდა: %s", exc)
        return {"count": 0, "errors": [str(exc)]}

    logger.info("fetch_seismic_task: %d მოვლენა მიღებულია", len(events))
    return {"count": len(events), "errors": []}

def summarize_run(weather_result: dict, currency_result: dict, seismic_result: dict) -> str:
    """სამივე task-ის შედეგის შეჯამება — Airflow-ის ბოლო task, XCom-ებით იღებს დანარჩენების შედეგებს."""
    total_errors = len(weather_result["errors"]) + len(currency_result["errors"]) + len(seismic_result["errors"])
    summary = (
        f"Weather: {len(weather_result['results'])} ქალაქი, "
        f"Currency: {len(currency_result['results'])} ვალუტა, "
        f"Seismic: {seismic_result['count']} მოვლენა, "
        f"სულ შეცდომა: {total_errors}"
    )
    logger.info("DAG run summary: %s", summary)
    return summary
