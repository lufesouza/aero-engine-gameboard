#!/usr/bin/env python3
"""Step 1: turn the uploaded sources into per-page text under $WARGAME_BUILD_DIR/text.

    python3 extract_text.py            # needs pypdf, xlrd (pip install pypdf xlrd)
    python3 ocr_airbus.py 3            # the Airbus report has no text layer: OCR it
                                       # (needs pymupdf, rapidocr-onnxruntime)

Sources are read from the repository root (the files uploaded to main).
"""
import csv
import json
import logging
import os
import re
import zipfile

import pypdf
import xlrd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
S = os.environ.get("WARGAME_BUILD_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "work"))
TEXT = os.path.join(S, "text")
SRC = os.path.join(S, "src")
logging.disable(logging.WARNING)


def unzip(name, sub):
    with zipfile.ZipFile(os.path.join(ROOT, name)) as z:
        z.extractall(os.path.join(SRC, sub))


def pdf_to_pages(path, key):
    r = pypdf.PdfReader(path)
    with open(os.path.join(TEXT, f"{key}.txt"), "w") as f:
        for i, pg in enumerate(r.pages):
            try:
                t = pg.extract_text() or ""
            except Exception as e:  # noqa: BLE001
                t = f"[extract error {e}]"
            f.write(f"\n\n=== PAGE {i + 1} ===\n{t}")
    print(key, len(r.pages), "pages")


def capiq_to_csv(name, out):
    s = xlrd.open_workbook(os.path.join(ROOT, name)).sheets()[0]
    hdr = next(i for i in range(s.nrows) if str(s.cell_value(i, 0)).startswith("For the Fiscal Period Ending"))
    cols = []
    for v in s.row_values(hdr)[1:]:
        m = re.findall(r"\w{3}-\d\d-(\d{4})", str(v))
        cols.append(f"FY{m[0]}" if m else "")
    with open(os.path.join(TEXT, out), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["line_item"] + cols)
        for i in range(hdr + 1, s.nrows):
            lab = str(s.cell_value(i, 0)).strip()
            if lab:
                w.writerow([lab] + [v if v not in ("", "-") else "" for v in s.row_values(i)[1:]])


def index_transcripts():
    import datetime
    txt = open(os.path.join(TEXT, "transcripts.txt")).read()
    raw = re.split(r"\n\n=== PAGE (\d+) ===\n", txt)[1:]
    pages = [(int(raw[i]), raw[i + 1]) for i in range(0, len(raw), 2)]
    docs, cur = [], None
    for n, t in pages:
        head = t[:500]
        a = re.search(r"The Boeing Company NYSE:BA\s*\n\s*([^\n]+?)\s*\n\s*\w+day, (\w+ \d{1,2}, \d{4})", head)
        b = re.search(r"THE BOEING COMPANY ([A-Z0-9 /&\-\.]+?)\s*\|\s*([A-Z]{3} \d{1,2}, \d{4})", head)
        key = None
        if a:
            key = (a.group(1).strip(), datetime.datetime.strptime(a.group(2), "%B %d, %Y").date())
        elif b:
            key = (b.group(1).strip().title(), datetime.datetime.strptime(b.group(2).title(), "%b %d, %Y").date())
        if key and (cur is None or key[1] != cur["date"]):
            cur = {"event": key[0], "date": key[1], "page": n}
            docs.append(cur)
    for i, d in enumerate(docs):
        d["end_page"] = docs[i + 1]["page"] - 1 if i + 1 < len(docs) else pages[-1][0]
        d["date"] = d["date"].isoformat()
    json.dump(docs, open(os.path.join(TEXT, "transcript_index.json"), "w"), indent=0)
    print("transcripts:", len(docs), "documents indexed")


if __name__ == "__main__":
    os.makedirs(TEXT, exist_ok=True)
    unzip("Boeing 10ks.zip", "boeing10k")
    unzip("airbus_se_report_of_the_board_of_directors_fy_2025.zip", "airbus")
    pdf_to_pages(os.path.join(ROOT, "Transcripts from 2006-2025_Compressed.pdf"), "transcripts")
    pdf_to_pages(os.path.join(SRC, "boeing10k", "Boeing 10ks.pdf"), "boeing_10k")
    capiq_to_csv("The Boeing Company NYSE BA Financials Income Statement.xls", "boeing_capiq_income_statement.csv")
    capiq_to_csv("The Boeing Company NYSE BA Financials Segments.xls", "boeing_capiq_segments.csv")
    index_transcripts()
