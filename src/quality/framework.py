"""lecture 14: Data Quality Framework — ავტომატური ვალიდაცია და Error Report."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

class Severity(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"

@dataclass
class QualityIssue:
    check_name: str
    severity: Severity
    message: str
    row_context: dict = field(default_factory=dict)

@dataclass
class QualityReport:
    source: str
    issues: list = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return any(i.severity == Severity.ERROR for i in self.issues)

    def add(self, check_name, severity, message, row_context=None):
        self.issues.append(QualityIssue(check_name, severity, message, row_context or {}))

    def summary(self) -> str:
        errors = sum(1 for i in self.issues if i.severity == Severity.ERROR)
        warnings = sum(1 for i in self.issues if i.severity == Severity.WARNING)
        return f"{self.source}: {errors} error(s), {warnings} warning(s)"

    def print_report(self) -> None:
        print(f"\n--- Data Quality Report: {self.source} ---")
        if not self.issues:
            print("[OK] ყველა შემოწმება გავლილია, პრობლემა არ აღმოჩენილა.")
            return
        for issue in self.issues:
            icon = "[X]" if issue.severity == Severity.ERROR else "[!]"
            print(f"{icon} [{issue.check_name}] {issue.message}")
        print(self.summary())

# ---------- Generic checks ----------
def check_not_null(rows, field_name, report):
    for row in rows:
        if row.get(field_name) is None:
            report.add("not_null", Severity.ERROR, f"'{field_name}' არის NULL", row)

def check_no_duplicates(rows, key_fields, report):
    seen = set()
    for row in rows:
        key = tuple(row.get(f) for f in key_fields)
        if key in seen:
            report.add("duplicate", Severity.ERROR, f"დუბლიკატი key: {key}", row)
        seen.add(key)

def check_freshness(rows, timestamp_field, max_age_hours, report):
    now = datetime.now(timezone.utc)
    for row in rows:
        ts = row.get(timestamp_field)
        if ts is None:
            continue
        age_hours = (now - ts).total_seconds() / 3600
        if age_hours > max_age_hours:
            report.add(
                "freshness", Severity.WARNING,
                f"{age_hours:.1f}სთ ძველი (ლიმიტი {max_age_hours}სთ)", row,
            )

# ---------- Domain-specific business rules ----------
EXPECTED_QUANTITY = {
    "USD": 1, "EUR": 1, "GBP": 1,
    "TRY": 10,
    "JPY": 100,
}

def check_currency_business_rules(rows, report):
    for row in rows:
        code = row.get("currency_code")
        quantity = row.get("quantity")
        rate = row.get("rate")

        if rate is not None and rate <= 0:
            report.add("business_rule", Severity.ERROR, f"rate <= 0: {rate}", row)

        expected = EXPECTED_QUANTITY.get(code)
        if expected is not None and quantity != expected:
            report.add(
                "business_rule", Severity.ERROR,
                f"{code}-ის quantity მოსალოდნელია {expected}, მიღებულია {quantity}", row,
            )

def check_weather_business_rules(rows, report):
    for row in rows:
        temp = row.get("temperature_c")
        if temp is not None and not (-50 <= temp <= 55):
            report.add("business_rule", Severity.ERROR, f"temperature_c მიღმა რეალურ დიაპაზონს: {temp}", row)
        humidity = row.get("humidity_pct")
        if humidity is not None and not (0 <= humidity <= 100):
            report.add("business_rule", Severity.ERROR, f"humidity_pct არარეალურია: {humidity}", row)

def check_seismic_business_rules(rows, report):
    for row in rows:
        mag = row.get("magnitude")
        if mag is not None and not (0 <= mag <= 10):
            report.add("business_rule", Severity.ERROR, f"magnitude არარეალურია: {mag}", row)
