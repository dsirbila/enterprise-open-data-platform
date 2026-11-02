"""
lecture 10: xml_validator.py-ის გადამოწმება — lxml XSD ვალიდაციის ტესტი.
"""
import sys
from pathlib import Path

# პროექტის ძირითადი დირექტორიის დამატება sys.path-ში
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR))

from src.ingestion.xml_validator import XMLSchemaValidationError, validate_against_schema

XSD_PATH = str(BASE_DIR / "data/sample/demo_xsd.xsd")
VALID_XML = str(BASE_DIR / "data/sample/demo_xml.xml")
INVALID_XML = str(BASE_DIR / "data/sample/demo_xml_wrong.xml")

def test_valid_xml():
    # 1. სწორი XML-ის ტესტირება
    is_valid = validate_against_schema(VALID_XML, XSD_PATH)
    assert is_valid is True
    print("[OK] სწორი XML გავიდა ვალიდაციას")

def test_invalid_xml():
    # 2. არასრული/არავალიდური XML-ის ტესტირება
    try:
        validate_against_schema(INVALID_XML, XSD_PATH)
        raise AssertionError("უნდა ატყორცნოს XMLSchemaValidationError")
    except XMLSchemaValidationError as exc:
        print(f"[OK] სწორად დაიჭირა არასრული XML: {exc}")

if __name__ == "__main__":
    test_valid_xml()
    test_invalid_xml()