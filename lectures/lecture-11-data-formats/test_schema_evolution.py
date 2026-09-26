"""lecture 11: Avro Schema Evolution ტესტი."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.ingestion.format_writer import write_avro, WEATHER_AVRO_SCHEMA
import fastavro

def main() -> int:
    path = Path("data/format_comparison/evolution_test.avro")
    path.parent.mkdir(parents=True, exist_ok=True)

    # 1. ვწერთ ძველი სქემით
    records = [{"city": "Tbilisi", "latitude": 41.7, "longitude": 44.8, "forecast_time": "2026-08-01T00:00:00", "temperature_c": 25.0, "humidity_pct": 50.0}]
    write_avro(records, path, WEATHER_AVRO_SCHEMA)

    # 2. ვკითხულობთ ახალი სქემით (სადაც დამატებულია wind_speed_kmh default-ით)
    schema_v2 = {
        "type": "record",
        "name": "WeatherForecast",
        "fields": [
            *WEATHER_AVRO_SCHEMA["fields"],
            {"name": "wind_speed_kmh", "type": "double", "default": 0.0},
        ],
    }

    with open(path, "rb") as f:
        reader = fastavro.reader(f, reader_schema=schema_v2)
        migrated_records = list(reader)

    print("[OK] Schema Evolution წარმატებულია:", migrated_records[0])
    path.unlink(missing_ok=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
