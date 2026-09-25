"""lecture 10 (დამატება): lxml-ით XML Schema ვალიდაცია."""
from lxml import etree

class XMLSchemaValidationError(Exception):
    """XML-ის schema-სთან შეუსაბამობისას წარმოქმნილი შეცდომა."""

def validate_against_schema(xml_path: str, xsd_path: str) -> bool:
    schema_doc = etree.parse(xsd_path)
    schema = etree.XMLSchema(schema_doc)

    xml_doc = etree.parse(xml_path)
    if not schema.validate(xml_doc):
        errors = "; ".join(str(e) for e in schema.error_log)
        raise XMLSchemaValidationError(f"XML არ შეესაბამება schema-ს: {errors}")
    return True
