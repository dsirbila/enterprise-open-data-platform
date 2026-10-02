"""lecture 14 lab: pandera production alternative for data validation."""
import pandas as pd
import pandera as pa
from pandera import Column, Check

EXPECTED_QUANTITY = {"USD": 1, "EUR": 1, "GBP": 1, "TRY": 10, "JPY": 100}

# განზრახ "ჭუჭყიანი" სემპლი მონაცემები ტესტირებისთვის
data = {
    "currency_code": ["USD", "USD", "JPY"],
    "quantity": [1, 1, 1],  # JPY-ზე intentional შეცდომა (1 100-ის ნაცვლად)
    "rate": [2.6512, 2.6512, 1.7920],
}
df = pd.DataFrame(data)

# Pandera Schema დეკლარაციული აღწერა
currency_schema = pa.DataFrameSchema(
    {
        "currency_code": Column(str),
        "quantity": Column(int),
        "rate": Column(float, Check.gt(0)),
    },
    checks=pa.Check(
        lambda df_arg: df_arg.apply(
            lambda row: EXPECTED_QUANTITY.get(row["currency_code"], row["quantity"]) == row["quantity"],
            axis=1,
        ),
        error="quantity არ ემთხვევა EXPECTED_QUANTITY-ს",
    ),
)

if __name__ == "__main__":
    print("=== Pandera Schema Validation Execution ===")
    try:
        currency_schema.validate(df, lazy=True)  # lazy=True აგროვებს ყველა შეცდომას ერთად
        print("[OK] ყველა შემოწმება გავლილია წარმატებით.")
    except pa.errors.SchemaErrors as exc:
        print("\n[X] აღმოჩენილია Schema Errors:")
        print(exc.failure_cases)
