#!/usr/bin/env python3
"""Check every spreadsheet citation in evidence JSONL against the source workbooks.

Usage: verify_cells.py <evidence/*.jsonl ...>

Items cite cells as "cells": [{"source": "ms_model"|"ciq_estimates"|"ciq_segments",
"sheet": "<sheet name>", "ref": "AS41", "value": <number or text>, "label": "..."}].
A cell passes when the workbook holds the same value at that ref: numbers within 0.5%
relative (or 1e-6 absolute), so rounded figures pass; percentages may be given as
"22.2%" for 0.222; text compares case- and space-insensitively. Items with a "quote"
and no cells are left to verify_quotes.py. Writes <name>.verified.jsonl and
<name>.rejected.jsonl (with "cell_errors") and prints a pass rate per file.

The cell cache is built by rr_cells_dump.py; set RR_CELLS_DIR to its output folder.
"""
import json
import os
import re
import sys

S = os.environ.get("WARGAME_BUILD_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "work"))
CELLS = os.environ.get("RR_CELLS_DIR", os.path.join(S, "rr", "cells"))
_cache = None


def cache():
    global _cache
    if _cache is None:
        with open(os.path.join(CELLS, "cells_cache.json")) as f:
            _cache = json.load(f)
    return _cache


def as_number(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        s = v.strip().replace(",", "").replace("£", "").replace("$", "")
        pct = s.endswith("%")
        s = s.rstrip("%").strip()
        try:
            x = float(s)
        except ValueError:
            return None
        return x / 100.0 if pct else x
    return None


def check_cell(c):
    src, sheet, ref = c.get("source"), c.get("sheet"), str(c.get("ref", "")).upper().replace("$", "")
    book = cache().get(src)
    if book is None:
        return f"unknown source {src!r}"
    if sheet not in book:
        return f"unknown sheet {sheet!r} in {src}"
    if ref not in book[sheet]:
        return f"{src}/{sheet}!{ref} is empty"
    have, want = book[sheet][ref], c.get("value")
    hn, wn = as_number(have), as_number(want)
    if hn is not None and wn is not None:
        if abs(hn - wn) <= max(1e-6, 0.005 * abs(hn)):
            return None
        # a percentage written as 22.2 for a cell holding 0.222
        if abs(hn * 100 - wn) <= max(1e-6, 0.005 * abs(hn * 100)):
            return None
        return f"{src}/{sheet}!{ref} holds {have!r}, cited {want!r}"
    norm = lambda s: re.sub(r"\s+", " ", str(s)).strip().lower()
    if norm(have) == norm(want):
        return None
    return f"{src}/{sheet}!{ref} holds {have!r}, cited {want!r}"


def main(paths):
    for path in paths:
        ok, bad = [], []
        for line in open(path):
            if not line.strip():
                continue
            it = json.loads(line)
            cells = it.get("cells") or []
            if not cells:
                (ok if it.get("quote") else bad).append(it if it.get("quote") else dict(it, cell_errors=["no cells and no quote"]))
                continue
            errs = [e for e in (check_cell(c) for c in cells) if e]
            (bad if errs else ok).append(dict(it, cell_errors=errs) if errs else it)
        base = path[:-6] if path.endswith(".jsonl") else path
        with open(base + ".verified.jsonl", "w") as f:
            f.writelines(json.dumps(x) + "\n" for x in ok)
        with open(base + ".rejected.jsonl", "w") as f:
            f.writelines(json.dumps(x) + "\n" for x in bad)
        n = len(ok) + len(bad)
        print(f"{os.path.basename(path)}: {len(ok)}/{n} pass" + (f" ({100 * len(ok) / n:.0f}%)" if n else ""))
        for x in bad[:20]:
            print("  REJECT", x.get("finding", "")[:80], "|", "; ".join(x.get("cell_errors", [])))


if __name__ == "__main__":
    main(sys.argv[1:])
