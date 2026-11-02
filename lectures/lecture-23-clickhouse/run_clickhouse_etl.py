"""lecture 23 lab: Postgres (operational) → ClickHouse (OLAP) — ETL + აგრეგაციის demo."""

import os
import sys
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import psycopg2
from dotenv import load_dotenv

from src.analytics.clickhouse_client import ClickHouseAnalytics
from src.analytics.clickhouse_queries import (
    build_daily_aggregation_query,
    format_query_result,
)

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")


def get_postgres_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "enterprise_open_data"),
        user=os.getenv("POSTGRES_USER", "eodp_user"),
        password=os.getenv("POSTGRES_PASSWORD", "change_me_locally"),
    )


def _to_naive_datetime(value) -> datetime:
    if isinstance(value, datetime):
        if value.tzinfo is not None:
            return value.astimezone(timezone.utc).replace(tzinfo=None)
        return value
    return datetime.fromisoformat(str(value).replace("Z", "+00:00")).replace(tzinfo=None)


def normalize_weather_rows(rows: list) -> list:
    normalized = []
    for city, forecast_time, temperature_c, humidity_pct in rows:
        normalized.append(
            (
                str(city),
                _to_naive_datetime(forecast_time),
                float(temperature_c) if temperature_c is not None else None,
                float(humidity_pct) if humidity_pct is not None else None,
            )
        )
    return normalized


def normalize_currency_rows(rows: list) -> list:
    normalized = []
    for currency_code, rate_date, rate in rows:
        normalized.append(
            (
                str(currency_code).strip(),
                rate_date,
                float(rate) if isinstance(rate, Decimal) else rate,
            )
        )
    return normalized


def main() -> None:
    ch = ClickHouseAnalytics()
    ch.create_tables()
    ch.truncate_tables()

    pg_conn = get_postgres_connection()
    with pg_conn.cursor() as cur:
        cur.execute(
            "SELECT city, forecast_time, temperature_c, humidity_pct FROM weather.forecasts;"
        )
        weather_rows = normalize_weather_rows(cur.fetchall())
        cur.execute("SELECT currency_code, rate_date, rate FROM currency.rates;")
        currency_rows = normalize_currency_rows(cur.fetchall())

    ch.insert_weather(weather_rows)
    ch.insert_currency(currency_rows)
    print(f"[OK] ჩატვირთულია: {len(weather_rows)} weather row, {len(currency_rows)} currency row")

    query = build_daily_aggregation_query(
        "weather_events", "forecast_time", "temperature_c", "avg"
    )
    rows, columns = ch.run_query(query)
    print()
    print(format_query_result(rows, columns))


if __name__ == "__main__":
    main()
