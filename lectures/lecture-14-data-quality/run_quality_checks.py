"""lecture 14 lab: Data Quality Framework-ის გაშვება სამივე წყაროზე."""
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.quality.framework import (
    QualityReport,
    check_currency_business_rules,
    check_freshness,
    check_no_duplicates,
    check_not_null,
    check_seismic_business_rules,
    check_weather_business_rules,
)

NOW = datetime.now(timezone.utc)

def check_weather() -> QualityReport:
    rows = [
        {"city": "Tbilisi", "forecast_time": NOW - timedelta(hours=1), "temperature_c": 24.3, "humidity_pct": 61},
        {"city": "Batumi", "forecast_time": NOW - timedelta(hours=50), "temperature_c": 22.0, "humidity_pct": 70},
        {"city": "Kutaisi", "forecast_time": NOW, "temperature_c": 120.0, "humidity_pct": 55},
        {"city": None, "forecast_time": NOW, "temperature_c": 20.0, "humidity_pct": 60},
    ]
    report = QualityReport(source="weather")
    check_not_null(rows, "city", report)
    check_freshness(rows, "forecast_time", max_age_hours=24, report=report)
    check_weather_business_rules(rows, report)
    return report

def check_currency() -> QualityReport:
    rows = [
        {"currency_code": "USD", "quantity": 1, "rate": 2.6512, "rate_date": "2026-08-27"},
        {"currency_code": "USD", "quantity": 1, "rate": 2.6512, "rate_date": "2026-08-27"},
        {"currency_code": "JPY", "quantity": 1, "rate": 1.7920, "rate_date": "2026-08-27"},
    ]
    report = QualityReport(source="currency")
    check_no_duplicates(rows, ["currency_code", "rate_date"], report)
    check_currency_business_rules(rows, report)
    return report

def check_seismic() -> QualityReport:
    rows = [
        {"event_id": "ge2026aaaa", "magnitude": 2.3},
        {"event_id": "ge2026bbbb", "magnitude": 15.0},
    ]
    report = QualityReport(source="seismic")
    check_not_null(rows, "event_id", report)
    check_seismic_business_rules(rows, report)
    return report

def main() -> int:
    reports = [check_weather(), check_currency(), check_seismic()]
    for report in reports:
        report.print_report()

    any_errors = any(r.has_errors for r in reports)
    return 1 if any_errors else 0

if __name__ == "__main__":
    sys.exit(main())
