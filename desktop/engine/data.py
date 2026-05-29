"""Data conversion module.

Handles: csv→xlsx, pdf→xlsx, json→csv, xml→json, yaml→json
"""

import io
import json
import csv
from .validator import validate


def csv_to_xlsx(data: bytes, is_web: bool = False) -> bytes:
    validate(data, "csv", is_web=is_web)
    import openpyxl
    reader = csv.reader(io.StringIO(data.decode("utf-8-sig")))
    wb = openpyxl.Workbook()
    ws = wb.active
    for row in reader:
        ws.append(row)
    out = io.BytesIO()
    wb.save(out)
    return out.getvalue()


def pdf_to_xlsx(data: bytes, is_web: bool = False) -> bytes:
    validate(data, "pdf", is_web=is_web)
    import pdfplumber
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    with pdfplumber.open(io.BytesIO(data)) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    ws.append([cell or "" for cell in row])
    out = io.BytesIO()
    wb.save(out)
    return out.getvalue()


def json_to_csv(data: bytes, is_web: bool = False) -> bytes:
    validate(data, "json", is_web=is_web)
    rows = json.loads(data.decode("utf-8"))
    if not isinstance(rows, list):
        raise ValueError("JSON must be a top-level array of objects")
    out = io.StringIO()
    if rows:
        writer = csv.DictWriter(out, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return out.getvalue().encode("utf-8")


def xml_to_json(data: bytes, is_web: bool = False) -> bytes:
    validate(data, "xml", is_web=is_web)
    import xmltodict
    parsed = xmltodict.parse(data.decode("utf-8"))
    return json.dumps(parsed, indent=2, ensure_ascii=False).encode("utf-8")


def yaml_to_json(data: bytes, is_web: bool = False) -> bytes:
    validate(data, "yaml", is_web=is_web)
    import yaml
    parsed = yaml.safe_load(data.decode("utf-8"))
    return json.dumps(parsed, indent=2, ensure_ascii=False).encode("utf-8")
