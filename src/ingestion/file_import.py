"""lecture 10: File Import Engine — CSV/JSON/XML უნიფიცირებული წაკითხვა, ვალიდაციითა და encoding-ის მართვით."""
import csv
import json
import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

class FileImportError(Exception):
    """ფაილის წაკითხვის ან ვალიდაციის შეცდომა."""

def read_csv(path: Path, required_columns: Optional[list] = None) -> list:
    try:
        with open(path, encoding="utf-8-sig") as f:  # utf-8-sig BOM-ს თვითონ ამოიცნობს
            rows = list(csv.DictReader(f))
    except UnicodeDecodeError as exc:
        raise FileImportError(f"CSV encoding შეცდომა {path}: {exc}") from exc

    if not rows:
        raise FileImportError(f"CSV ცარიელია: {path}")

    if required_columns:
        missing = set(required_columns) - set(rows[0].keys())
        if missing:
            raise FileImportError(f"CSV-ს აკლია სვეტები {path}: {missing}")

    logger.info("წაკითხულია %d row CSV-დან: %s", len(rows), path.name)
    return rows

def read_json(path: Path) -> Any:
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        raise FileImportError(f"არასწორი JSON {path}: {exc}") from exc

    logger.info("წაკითხულია JSON: %s", path.name)
    return data

def read_xml(path: Path) -> list:
    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        raise FileImportError(f"არასწორი XML {path}: {exc}") from exc

    root = tree.getroot()
    records = []
    for record_elem in root:
        record = {child.tag: child.text for child in record_elem}
        records.append(record)

    logger.info("წაკითხულია %d ჩანაწერი XML-დან: %s", len(records), path.name)
    return records

def read_file_auto(path: Path, required_columns: Optional[list] = None) -> Any:
    """
    AI Corner მოთხოვნა: ფაილის გაფართოებით ავტომატურად ამორჩეული reader 
    სტანდარტული error handling-ითა და encoding (UTF-8-BOM) მხარდაჭერით.
    """
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return read_csv(path, required_columns=required_columns)
    elif suffix in (".json", ".geojson"):
        return read_json(path)
    elif suffix == ".xml":
        return read_xml(path)
    elif suffix in (".xlsx", ".xls"):
        from .excel_handler import read_excel
        cols_set = set(required_columns) if required_columns else None
        df = read_excel(str(path), required_columns=cols_set)
        return df.to_dict(orient="records")
    else:
        raise FileImportError(f"არასპეციფიცირებული ან უცნობი ფაილის გაფართოება '{suffix}' ფაილისთვის: {path}")
