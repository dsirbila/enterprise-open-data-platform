"""lecture 13 lab: ETL Pipeline-ის გაშვება — NBG → PostgreSQL, incremental."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import psycopg2
from dotenv import load_dotenv

from src.etl.currency_pipeline import CurrencyETLPipeline
from src.ingestion.logging_config import setup_logging

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "enterprise_open_data"),
        user=os.getenv("POSTGRES_USER", "eodp_user"),
        password=os.getenv("POSTGRES_PASSWORD", "change_me_locally"),
    )

def main() -> None:
    setup_logging()
    conn = get_connection()
    pipeline = CurrencyETLPipeline(conn)

    loaded = pipeline.run_incremental(lookback_days=7)
    print(f"[OK] სულ ჩატვირთულია: {loaded} ახალი row")

    conn.close()

if __name__ == "__main__":
    main()
