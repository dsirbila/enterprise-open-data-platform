"""lecture 22: 3 წყაროს join-ის ლოგიკა — testable, PySpark-ისგან დამოუკიდებელი.
Lab 6-ის Star Schema-ს კონცეფციის გამეორება (dim_date, როგორც conformed key),
ახლა Spark DataFrame join-ის ლოგიკის დონეზე."""

from collections import defaultdict

def join_by_date(weather_rows: list, currency_rows: list, seismic_rows: list) -> list:
    """
    სამივე წყაროს აერთიანებს date_key-ით (Spark-ის df1.join(df2, "date_key", "outer")-ის
    ეკვივალენტი) — თითო თარიღზე ერთი შეჯამებული row.
    """
    by_date = defaultdict(lambda: {"avg_temp": None, "usd_rate": None, "earthquake_count": 0})
    
    for row in weather_rows:
        date_key = row["date_key"]
        temps = [r["temperature_c"] for r in weather_rows if r["date_key"] == date_key]
        by_date[date_key]["avg_temp"] = round(sum(temps) / len(temps), 1)
        
    for row in currency_rows:
        if row["currency_code"] == "USD":
            by_date[row["date_key"]]["usd_rate"] = row["rate"]
            
    for row in seismic_rows:
        by_date[row["date_key"]]["earthquake_count"] += 1
        
    result = []
    for date_key, values in sorted(by_date.items()):
        result.append({"date_key": date_key, **values})
    return result
