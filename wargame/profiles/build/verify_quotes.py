#!/usr/bin/env python3
"""Check every evidence quote against its cited source page(s).

Usage: verify_quotes.py <evidence/*.jsonl ...>
Writes <name>.verified.jsonl (items whose quote is found) and <name>.rejected.jsonl,
and prints a per-file pass rate. A quote passes when every "..."-separated segment of
>= 3 words appears (after normalising case, whitespace, quotes and dashes) on the
cited page or the page before/after; short segments are ignored; if exact matching
fails, a segment passes with a fuzzy ratio >= 0.9 against the best window.
"""
import difflib
import os
import json
import re
import sys
import unicodedata

S = os.environ.get("WARGAME_BUILD_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "work"))
_cache = {}


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("­", "")
    s = re.sub(r"-\s*\n\s*", "", s)  # de-hyphenate line breaks
    s = re.sub(r"[^a-z0-9$%.,' ]+", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()


def pages(src):
    if src not in _cache:
        if src == "airbus_fy2025":  # OCR output, one file per page
            import glob, os
            _cache[src] = {int(os.path.basename(f)[:3]): norm(open(f).read())
                           for f in glob.glob(f"{S}/text/airbus_pages/[0-9][0-9][0-9].txt")}
            return _cache[src]
        txt = open(f"{S}/text/{src}.txt").read()
        parts = re.split(r"\n\n=== PAGE (\d+) ===\n", txt)[1:]
        _cache[src] = {int(parts[i]): norm(parts[i + 1]) for i in range(0, len(parts), 2)}
    return _cache[src]


def segment_ok(seg, hay):
    if seg in hay:
        return True
    n = len(seg)
    if n < 15:
        return False
    best = 0.0
    words = hay.split(" ")
    k = len(seg.split(" "))
    for i in range(0, max(1, len(words) - k + 1), 2):
        win = " ".join(words[i:i + k + 2])
        r = difflib.SequenceMatcher(None, seg, win).ratio()
        if r > best:
            best = r
            if best >= 0.9:
                return True
    return False


def check(item):
    src = item.get("source")
    if src not in ("transcripts", "boeing_10k", "airbus_fy2025") and not os.path.exists(f"{S}/text/{src}.txt"):
        return False, "unknown source"
    try:
        p = int(item.get("page"))
    except (TypeError, ValueError):
        return False, "no page"
    pg = pages(src)
    hay = " ".join(pg.get(q, "") for q in (p - 1, p, p + 1))
    if not hay:
        return False, "page not found"
    segs = [norm(x) for x in re.split(r"\.\.\.|…|\[\.\.\.\]", item.get("quote", ""))]
    segs = [x.strip(" .,'") for x in segs if len(x.split(" ")) >= 3]
    if not segs:
        return False, "quote too short"
    if src == "airbus_fy2025":  # OCR text often drops spaces between words: compare space-free
        flat = hay.replace(" ", "")
        for s in segs:
            f = s.replace(" ", "")
            if f in flat:
                continue
            m = difflib.SequenceMatcher(None, f, flat, autojunk=False).find_longest_match(0, len(f), 0, len(flat))
            if m.size < 0.85 * len(f):
                return False, f"segment not found: {s[:60]}"
        return True, ""
    for s in segs:
        if not segment_ok(s, hay):
            return False, f"segment not found: {s[:60]}"
    return True, ""


if __name__ == "__main__":
    total_ok = total = 0
    for path in sys.argv[1:]:
        ok, bad = [], []
        for line in open(path):
            line = line.strip()
            if not line:
                continue
            try:
                it = json.loads(line)
            except json.JSONDecodeError:
                bad.append({"raw": line[:200], "why": "bad json"})
                continue
            good, why = check(it)
            (ok if good else bad).append(it if good else dict(it, why=why))
        base = path[:-6]
        with open(base + ".verified.jsonl", "w") as f:
            f.writelines(json.dumps(x) + "\n" for x in ok)
        with open(base + ".rejected.jsonl", "w") as f:
            f.writelines(json.dumps(x) + "\n" for x in bad)
        n = len(ok) + len(bad)
        total_ok += len(ok)
        total += n
        print(f"{path.split('/')[-1]:24s} {len(ok):4d}/{n:<4d} verified")
    if total:
        print(f"TOTAL {total_ok}/{total} ({100 * total_ok / total:.0f}%)")
