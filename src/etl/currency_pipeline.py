"""lecture 13: პირველი სრულფასოვანი ETL Pipeline — NBG REST API → PostgreSQL.
Extract → Transform → Load, incremental loading + idempotency."""
import logging
from datetime import date, timedelta
from typing import Optional

from src.ingestion.currency_client import CurrencyAPIError, CurrencyClient

logger = logging.getLogger(__name__)

class CurrencyETLPipeline:
    def __init__(self, conn, client: Optional[CurrencyClient] = None) -> None:
        self.conn = conn
        self.client = client or CurrencyClient()

    # ---------- EXTRACT ----------
    def extract(self, on_date: date) -> dict:
        logger.info("EXTRACT: NBG rates თარიღზე %s", on_date)
        return self.client.get_rates(on_date)

    # ---------- TRANSFORM ----------
    def transform(self, raw: dict) -> list:
        rate_date = raw["date"][:10]
        rows = []
        for c in raw["currencies"]:
            rows.append({
                "code": c["code"],
                "name": c["name"],
                "quantity": c["quantity"],
                "rate": c["rate"],
                "rate_date": rate_date,
            })
        logger.info("TRANSFORM: %d row გარდაიქმნა", len(rows))
        return rows

    # ---------- LOAD ----------
    def load(self, rows: list) -> int:
        loaded = 0
        with self.conn, self.conn.cursor() as cur:
            for row in rows:
                cur.execute(
                    "INSERT INTO currency.currencies (code, name) VALUES (%s, %s) ON CONFLICT (code) DO NOTHING",
                    (row["code"], row["name"]),
                )
                cur.execute(
                    """
                    INSERT INTO currency.rates (currency_code, quantity, rate, rate_date)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (currency_code, rate_date) DO NOTHING
                    """,
                    (row["code"], row["quantity"], row["rate"], row["rate_date"]),
                )
                loaded += 1
        logger.info("LOAD: %d row ჩაიტვირთა (idempotent)", loaded)
        return loaded

    def get_loaded_dates(self) -> set:
        with self.conn.cursor() as cur:
            cur.execute("SELECT DISTINCT rate_date FROM currency.rates;")
            return {str(row[0]) for row in cur.fetchall()}

    # ---------- ORCHESTRATION ----------
    def run_incremental(self, lookback_days: int = 7) -> int:
        """
        მხოლოდ ის დღეები ჩატვირთოს, რაც ჯერ არ არის ცხრილში.
        T-1 პრინციპი: today() არ იტვირთება — NBG დღევანდელ კურსს დილით აქვეყნებს.
        """
        already_loaded = self.get_loaded_dates()
        today = date.today()
        total_loaded = 0
        for offset in range(1, lookback_days + 1):
            target_date = today - timedelta(days=offset)
            if str(target_date) in already_loaded:
                logger.info("გამოტოვება %s — უკვე ჩატვირთულია (idempotent skip)", target_date)
                continue
            try:
                raw = self.extract(target_date)
                rows = self.transform(raw)
                total_loaded += self.load(rows)
            except CurrencyAPIError as exc:
                logger.error("ჩავარდა %s: %s", target_date, exc)
        return total_loaded

    def run_full_backfill(self, days: int = 30) -> int:
        """ყველა დღის ხელახლა გავლა — idempotent (ON CONFLICT DO NOTHING) იცავს დუბლიკატისგან."""
        today = date.today()
        total_loaded = 0
        for offset in range(1, days + 1):
            target_date = today - timedelta(days=offset)
            try:
                raw = self.extract(target_date)
                rows = self.transform(raw)
                total_loaded += self.load(rows)
            except CurrencyAPIError as exc:
                logger.error("ჩავარდა %s: %s", target_date, exc)
        return total_loaded
