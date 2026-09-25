"""lecture 10: pandas_transform-ის ტესტირება და აგრეგაციის დემონსტრაცია."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.ingestion.pandas_transform import compute_daily_currency_stats

def main() -> int:
    csv_path = Path("data/sample/currency_rates_2026-08-27.csv")
    if not csv_path.exists():
        print(f"[FAIL] ფაილი არ მოიძებნა: {csv_path}")
        return 1

    stats = compute_daily_currency_stats(str(csv_path))
    print("ტრანსფორმირებული სტატისტიკა (groupby .agg()):")
    print(stats)
    print("\n[OK] pandas groupby().agg() წარმატებით შესრულდა!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
