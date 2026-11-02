"""lecture 23: ClickHouse client — production wrapper clickhouse_connect-ს გარშემო."""

import logging

import clickhouse_connect

logger = logging.getLogger(__name__)

WEATHER_DDL = """
CREATE TABLE IF NOT EXISTS weather_events (
    city String,
    forecast_time DateTime,
    temperature_c Float32,
    humidity_pct Float32
) ENGINE = MergeTree()
ORDER BY (city, forecast_time)
"""

CURRENCY_DDL = """
CREATE TABLE IF NOT EXISTS currency_rates (
    currency_code String,
    rate_date Date,
    rate Float64
) ENGINE = MergeTree()
ORDER BY (currency_code, rate_date)
"""


class ClickHouseAnalytics:
    def __init__(self, host: str = "localhost", port: int = 8123) -> None:
        self.client = clickhouse_connect.get_client(host=host, port=port)

    def create_tables(self) -> None:
        self.client.command(WEATHER_DDL)
        self.client.command(CURRENCY_DDL)
        logger.info("ClickHouse ცხრილები შექმნილია (ან უკვე არსებობდა)")

    def truncate_tables(self) -> None:
        self.client.command("TRUNCATE TABLE IF EXISTS weather_events")
        self.client.command("TRUNCATE TABLE IF EXISTS currency_rates")

    def insert_weather(self, rows: list) -> None:
        self.client.insert(
            "weather_events",
            rows,
            column_names=["city", "forecast_time", "temperature_c", "humidity_pct"],
        )

    def insert_currency(self, rows: list) -> None:
        self.client.insert(
            "currency_rates",
            rows,
            column_names=["currency_code", "rate_date", "rate"],
        )

    def run_query(self, sql: str):
        result = self.client.query(sql)
        return result.result_rows, result.column_names
