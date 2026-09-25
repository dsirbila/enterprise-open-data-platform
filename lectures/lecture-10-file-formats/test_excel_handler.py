"""lecture 10: Excel ჰენდლერის round-trip და failure სცენარების ტესტირება."""
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.ingestion.excel_handler import read_excel, write_excel, ExcelImportError

def main() -> int:
    test_path = Path("/tmp/test_currency.xlsx")
    
    try:
        # 1. ტესტი: Round-trip (ჩაწერა და წაკითხვა)
        df_original = pd.DataFrame([
            {"currency_code": "USD", "rate": 2.65},
            {"currency_code": "EUR", "rate": 2.92}
        ])
        write_excel(df_original, str(test_path))
        df_read = read_excel(str(test_path))
        
        # შევამოწმოთ იდენტურობა
        pd.testing.assert_frame_equal(df_original, df_read)
        print("[OK] round-trip სწორია — ჩაწერილი და წაკითხული მონაცემი იდენტურია")

        # 2. ტესტი: აკლია სვეტები
        try:
            read_excel(str(test_path), required_columns={"currency_code", "nonexistent_column"})
        except ExcelImportError as exc:
            print(f"[OK] სწორად დაიჭირა: {exc}")

        # 3. ტესტი: ფაილი ვერ მოიძებნა
        try:
            read_excel("/tmp/does_not_exist.xlsx")
        except ExcelImportError as exc:
            print(f"[OK] სწორად დაიჭირა: {exc}")

    finally:
        if test_path.exists():
            test_path.unlink()

    return 0

if __name__ == "__main__":
    sys.exit(main())
