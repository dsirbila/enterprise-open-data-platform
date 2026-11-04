"""lecture 24: Silver Layer — გასუფთავებული, ვალიდირებული, დედუპლიცირებული მონაცემი."""

def clean_weather_batch(bronze_records: list) -> tuple:
    """
    აბრუნებს (clean_records, rejected_records)-ს — Bronze-დან Silver-ში გადასვლისას
    ვშლით დუბლიკატებს და ვფილტრავთ არასწორ (out-of-range) მონაცემებს.
    """
    seen = set()
    clean, rejected = [], []
    for record in bronze_records:
        key = (record["city"], record["forecast_time"])
        if key in seen:
            rejected.append({**record, "_rejection_reason": "duplicate"})
            continue
        seen.add(key)
        
        temp = record.get("temperature_c")
        if temp is None or not (-50 <= temp <= 55):
            rejected.append({**record, "_rejection_reason": f"invalid temperature: {temp}"})
            continue
            
        clean.append(record)
    return clean, rejected