import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "enterprise_open_data")
DB_USER = os.getenv("POSTGRES_USER", "eodp_user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "change_me_locally")

def main():
    print(f"Connecting to PostgreSQL at {DB_HOST}:{DB_PORT} as {DB_USER} (db: {DB_NAME})...")
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()

    # შევქმნათ ცხრილი და ჩავტვირთოთ საწყისი სავალუტო მონაცემები, თუ არ არსებობს
    cur.execute("""
        CREATE TABLE IF NOT EXISTS currency_rates (
            date DATE,
            currency VARCHAR(10),
            rate NUMERIC(10, 4)
        );
    """)
    
    # შევამოწმოთ არის თუ არა მონაცემები
    cur.execute("SELECT COUNT(*) FROM currency_rates;")
    count = cur.fetchone()[0]
    
    if count == 0:
        print("Inserting sample currency data into PostgreSQL...")
        sample_data = [
            ('2026-10-01', 'USD', 2.7000),
            ('2026-10-02', 'USD', 2.7100),
            ('2026-10-03', 'USD', 2.6950),
            ('2026-10-01', 'EUR', 2.9500),
            ('2026-10-02', 'EUR', 2.9600),
            ('2026-10-03', 'EUR', 2.9450),
        ]
        cur.executemany("""
            INSERT INTO currency_rates (date, currency, rate)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, sample_data)
        conn.commit()

    query = "SELECT date, currency, rate FROM currency_rates ORDER BY date, currency;"
    df = pd.read_sql(query, conn)
    cur.close()
    conn.close()

    output_dir = "data/spark_input"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "currency_rates.parquet")
    
    df.to_parquet(output_path, index=False)
    print(f"Successfully saved {len(df)} rows to {output_path}")

if __name__ == "__main__":
    main()
