import pytest
from engine.data import csv_to_xlsx, pdf_to_xlsx, json_to_csv, xml_to_json, yaml_to_json
import json

def test_csv_to_xlsx(sample_csv):
    result = csv_to_xlsx(sample_csv)
    assert result.startswith(b'PK\x03\x04')  # XLSX (ZIP) magic bytes

def test_json_to_csv(sample_json):
    result = json_to_csv(sample_json)
    # Basic check for CSV format (headers and newlines)
    assert b"id,name" in result
    assert b"1,Test" in result

def test_xml_to_json(sample_xml):
    result = xml_to_json(sample_xml)
    parsed = json.loads(result)
    assert "root" in parsed

def test_yaml_to_json(sample_yaml):
    result = yaml_to_json(sample_yaml)
    parsed = json.loads(result)
    assert "key" in parsed
    assert parsed["key"] == "value"

def test_pdf_to_xlsx(sample_pdf):
    result = pdf_to_xlsx(sample_pdf)
    assert result.startswith(b'PK\x03\x04')
