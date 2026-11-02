"""lecture 23: query აგება, ვალიდაცია და ცხრილის ფორმატირება — clickhouse_connect-ის გარეშე."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.analytics.clickhouse_queries import (
    QueryBuildError,
    build_daily_aggregation_query,
    format_query_result,
)


def main() -> int:
    query = build_daily_aggregation_query(
        "weather_events", "forecast_time", "temperature_c", "avg"
    )
    print(f"Query: {query}")

    try:
        build_daily_aggregation_query(
            "weather_events", "forecast_time", "temperature_c", "median"
        )
        print("[FAIL] median უნდა ჩავარდნილიყო")
        return 1
    except QueryBuildError as exc:
        print(f"[OK] სწორად დაიჭირა: {exc}")

    sample_rows = [
        ("2026-08-25", 21.5),
        ("2026-08-26", 22.0),
        ("2026-08-27", 25.2),
    ]
    table = format_query_result(sample_rows, ["day", "avg_temp"])
    print(table)

    if "(ცარიელი შედეგი)" != format_query_result([], ["day", "avg_temp"]):
        print("[FAIL] ცარიელი შედეგის ფორმატი არასწორია")
        return 1

    print("[OK] ყველა ტესტი გავლილია")
    return 0


if __name__ == "__main__":
    sys.exit(main())
