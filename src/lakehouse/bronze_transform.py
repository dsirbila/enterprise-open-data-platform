"""lecture 24: Bronze Layer — ნედლი მონაცემის ჩაწერა, მინიმალური დამუშავებით."""
from datetime import datetime, timezone

def add_bronze_metadata(record: dict, source: str) -> dict:
    """
    ყოველ ნედლ ჩანაწერს ამატებს ingestion metadata-ს — Bronze layer-ის ძირითადი
    პრინციპი: შეინახე ყველაფერი, ისე როგორც მოვიდა, ტრასირების ინფორმაციასთან ერთად.
    """
    return {
        **record,
        "_bronze_source": source,
        "_bronze_ingested_at": datetime.now(timezone.utc).isoformat(),
    }

def bronze_batch(records: list, source: str) -> list:
    return [add_bronze_metadata(r, source) for r in records]