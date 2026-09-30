#!/usr/bin/env python3
"""Step 1 for the engine-maker profiles (Rolls-Royce, Pratt & Whitney).

    python3 extract_text_engines.py        # needs pymupdf

Turns the engine-maker PDFs uploaded to the repository root into per-page text
under $WARGAME_BUILD_DIR/text/<key>.txt (with "=== PAGE N ===" markers, the same
format verify_quotes.py reads) and writes an event index for each transcript
digest and each 10-K bundle: text/<key>_index.json = [{event, date, page, end_page}].
"""
import datetime
import json
import os
import re

import pymupdf

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
S = os.environ.get("WARGAME_BUILD_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "work"))
TEXT = os.path.join(S, "text")

SOURCES = {
    "rr_transcripts": "Transcript Digest 2010-26.pdf",      # Rolls-Royce earnings calls (S&P)
    "rtx_transcripts": "Transcript Digest 15-25.pdf",       # RTX / UTC earnings calls (S&P)
    "rtx_10k": "Filings.pdf",                               # UTC / RTX 10-Ks FY2016-FY2024
    "rr_sec": "SEC Fillings.pdf",                           # Rolls-Royce ADR deposit agreement (Form F-6)
    "gtf_news": "Durability news 11-19-25.pdf",             # FlightGlobal on GTF durability, Nov 2025
    "engine_brief_2019": "Global Strategy Brief-2019-Global Commercial Aircraft Engine Manufacturers.pdf",
}
COMPANY = {"rr_transcripts": r"Rolls-Royce Holdings plc LSE:RR\.?|ROLLS-ROYCE HOLDINGS PLC",
           "rtx_transcripts": r"RTX Corporation NYSE:RTX|Raytheon Technologies Corporation NYSE:RTX|United Technologies Corporation NYSE:UTX|"
                              r"RTX CORPORATION|RAYTHEON TECHNOLOGIES CORPORATION|UNITED TECHNOLOGIES CORPORATION"}


def extract(key, name):
    doc = pymupdf.open(os.path.join(ROOT, name))
    with open(os.path.join(TEXT, f"{key}.txt"), "w") as f:
        for i, pg in enumerate(doc):
            f.write(f"\n\n=== PAGE {i + 1} ===\n{pg.get_text()}")
    print(key, doc.page_count, "pages")


def pages(key):
    txt = open(os.path.join(TEXT, f"{key}.txt")).read()
    raw = re.split(r"\n\n=== PAGE (\d+) ===\n", txt)[1:]
    return [(int(raw[i]), raw[i + 1]) for i in range(0, len(raw), 2)]


def index_transcripts(key):
    co = COMPANY[key]
    pg = pages(key)
    docs, cur = [], None
    for n, t in pg:
        head = re.sub(r"[ \t]+", " ", t[:700])
        a = re.search(rf"(?:{co})\s*\n?\s*([^\n]+?)\s*\n\s*\w+day, (\w+ \d{{1,2}}, \d{{4}})", head)
        b = re.search(rf"(?:{co}) ([A-Z0-9 /&\-\.']+?)\s*\|\s*([A-Z]{{3}} \d{{1,2}}, \d{{4}})", head)
        k = None
        try:
            if a:
                k = (a.group(1).strip(), datetime.datetime.strptime(a.group(2), "%B %d, %Y").date())
            elif b:
                k = (b.group(1).strip().title(), datetime.datetime.strptime(b.group(2).title(), "%b %d, %Y").date())
        except ValueError:
            k = None
        if k and (cur is None or k[1] != cur["date"]):
            cur = {"event": k[0], "date": k[1], "page": n}
            docs.append(cur)
    for i, d in enumerate(docs):
        d["end_page"] = docs[i + 1]["page"] - 1 if i + 1 < len(docs) else pg[-1][0]
        d["date"] = d["date"].isoformat()
    json.dump(docs, open(os.path.join(TEXT, f"{key}_index.json"), "w"), indent=0)
    print(key, len(docs), "events", docs[-1]["date"] if docs else "", "..", docs[0]["date"] if docs else "")


def index_10k(key):
    docs = []
    for n, t in pages(key):
        head = t[:600]
        m = re.search(r"For the (?:fiscal )?year ended ([A-Za-z]+ \d{1,2}, \d{4})", head)
        if m and "FORM 10-K" in head.upper():
            co = "United Technologies" if "UNITED TECHNOLOGIES" in head.upper() else "RTX / Raytheon Technologies"
            docs.append({"event": f"{co} Form 10-K{'/A' if '10-K/A' in head else ''} FY{m.group(1)[-4:]}",
                         "date": datetime.datetime.strptime(m.group(1), "%B %d, %Y").date().isoformat(), "page": n})
    last = pages(key)[-1][0]
    for i, d in enumerate(docs):
        d["end_page"] = docs[i + 1]["page"] - 1 if i + 1 < len(docs) else last
    json.dump(docs, open(os.path.join(TEXT, f"{key}_index.json"), "w"), indent=0)
    print(key, [(d["event"], d["page"]) for d in docs])


if __name__ == "__main__":
    os.makedirs(TEXT, exist_ok=True)
    for k, name in SOURCES.items():
        extract(k, name)
    for k in ("rr_transcripts", "rtx_transcripts"):
        index_transcripts(k)
    index_10k("rtx_10k")
