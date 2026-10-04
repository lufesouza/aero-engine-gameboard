#!/usr/bin/env python3
"""Split S&P transcript digests into named executives' own speaking turns.

Usage: exec_turns.py <source key: transcripts|rtx_transcripts|rr_transcripts|ge_transcripts> <out dir>

A turn starts at a line equal to one of an executive's name variants (EXECS)
followed by a title line (or, in pre-2010 digests, a "<strong>Name</strong>" line), and runs until the next speaker line: any line that
looks like a person's name followed by a title or firm line, or "Operator".
Writes <out>/<id>.txt with each turn headed
"##### <date> | <event> | page <n> | <title as printed> | prepared|Q&A" ([page n]
markers inside long turns; pre-2010 digests have no Q&A marker, so all turns read "prepared"), and <out>/roster.json with each executive's events, titles and words.
The pages cited are the digest's own "=== PAGE N ===" numbers, so quotes can be
checked with verify_quotes.py.
"""
import collections
import json
import os
import re
import sys

EXECS = {
    # Boeing
    "mcnerney": ["W. James McNerney", "W. James McNerney, Jr.", "Jim McNerney", "Jim McNerny", "James McNerney"],
    "muilenburg": ["Dennis A. Muilenburg", "Dennis Muilenburg"],
    "calhoun": ["David L. Calhoun", "Dave Calhoun", "David Calhoun"],
    "ortberg": ["Robert K. Ortberg", "Kelly Ortberg", "Kelly R. Ortberg", "Robert Kelly Ortberg"],
    "bell": ["James A. Bell", "James Bell"],
    "smith": ["Gregory D. Smith", "Greg Smith", "Gregory Smith"],
    "west": ["Brian J. West", "Brian West"],
    "malave": ["Jesus Malave", "Jay Malave"],
    "albaugh": ["James F. Albaugh", "Jim Albaugh"],
    "carson": ["Scott E. Carson", "Scott Carson"],
    "conner": ["Raymond L. Conner", "Ray Conner"],
    "mcallister": ["Kevin G. McAllister", "Kevin McAllister"],
    "deal": ["Stanley A. Deal", "Stan Deal"],
    "pope": ["Stephanie F. Pope", "Stephanie Pope"],
    # GE / GE Aerospace, for CFM International (source ge_transcripts); a separate run, so ids do not mix
    "culp": ["H. Lawrence Culp", "Larry Culp", "H. Lawrence Culp, Jr."],
    "immelt": ["Jeffrey R. Immelt", "Jeff Immelt"],
    "flannery": ["John L. Flannery", "John Flannery"],
    "bornstein": ["Jeffrey S. Bornstein", "Jeff Bornstein"],
    "miller": ["Jamie S. Miller", "Jamie Miller"],
    "dybeck_happe": ["Carolina Dybeck Happe", "Carolina Dybeck Happe"],
    "ghai": ["Rahul Ghai"],
    "joyce": ["David Leon Joyce", "David L. Joyce", "David Joyce"],
    "slattery": ["John Stephen Slattery", "John Slattery"],
    "stokes": ["Russell T. Stokes", "Russell Stokes"],
    "ali": ["Mohamed Ali"],
    "fitzgerald": ["William A. Fitzgerald", "Bill Fitzgerald"],
    # Rolls-Royce (source rr_transcripts)
    "erginbilgic": ["M. Tufan Erginbilgic", "Tufan Erginbilgic"],
    "mccabe": ["Helen McCabe"],
    "kakoullis": ["Panos Kakoullis"],
    "cholerton": ["Chris Cholerton"],
    "rwatson": ["Robert Watson"],
    "eschulz": ["Eric Schulz"],
    # RTX / Pratt & Whitney (source rtx_transcripts)
    "calio": ["Christopher T. Calio", "Chris Calio"],
    "mitchill": ["Neil G. Mitchill", "Neil Mitchill"],
    "eddy": ["Shane G. Eddy", "Shane Eddy"],
    "leduc": ["Robert F. Leduc", "Bob Leduc"],
}
VARIANT = {v: k for k, vs in EXECS.items() for v in vs}
S = os.environ.get("WARGAME_BUILD_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "work"))
NAME = re.compile(r"(?:[A-Z][a-zA-Z'\-]*\.?,? ?){2,6}(?:Jr\.|Sr\.|II|III)?")
ROLE = re.compile(r"Research|Division|LLC|Inc\b|Capital|Securities|Bank|Partners|Group|President|Officer|\bVP\b|Vice|CFO|CEO|COO|"
                  r"Analyst|Director|Treasurer|Relations|Chairman|Executive|Former|Senior|Manager|Head of|Chief|Communications")
STRONG = re.compile(r"<strong>\s*(.+?)\s*</strong>")
HEADER = re.compile(r"^(THE BOEING COMPANY|RTX CORPORATION|RAYTHEON TECHNOLOGIES|UNITED TECHNOLOGIES|ROLLS-ROYCE|GENERAL ELECTRIC COMPANY|Copyright ©|COPYRIGHT ©|spglobal\.com)")

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
txt = open(os.path.join(S, "text", f"{src}.txt")).read()
raw = re.split(r"\n\n=== PAGE (\d+) ===\n", txt)[1:]
pages = {int(raw[i]): raw[i + 1] for i in range(0, len(raw), 2)}
events = json.load(open(os.path.join(S, "text", "transcript_index.json" if src == "transcripts" else f"{src}_index.json")))
roster = collections.defaultdict(lambda: {"titles": collections.Counter(), "events": [], "words": 0})
files = {}
for ev in sorted(events, key=lambda e: e["page"]):
    lines = [(p, ln.strip()) for p in range(ev["page"], ev["end_page"] + 1)
             for ln in pages.get(p, "").split("\n") if ln.strip() and not HEADER.match(ln.strip())]
    try:  # skip the participants list
        k = next(i for i, (_, l) in enumerate(lines) if l in ("Presentation", "Question and Answer"))
    except StopIteration:
        k = 0
    cur, buf, title, cur_k = None, [], "", 0
    qa_from = next((i for i, (_, l) in enumerate(lines) if l == "Question and Answer" and i > k), len(lines))

    def flush():
        if cur and buf:
            eid, page = cur
            if eid not in files:
                files[eid] = open(os.path.join(out, f"{eid}.txt"), "w")
            f = files[eid]
            body = "\n".join(buf)
            f.write(f"\n##### {ev['date']} | {ev['event']} | page {page} | {title} | {'Q&A' if cur_k >= qa_from else 'prepared'}\n{body}\n")
            roster[eid]["words"] += len(body.split())

    while k < len(lines):
        p, l = lines[k]
        nxt = lines[k + 1][1] if k + 1 < len(lines) else ""
        m = STRONG.fullmatch(l)  # pre-2010 digests: "<strong>Name - Firm</strong>", text follows directly
        if m:
            name = m.group(1).split(" - ")[0].strip()
            flush()
            cur, buf = None, []
            if name in VARIANT:
                eid = VARIANT[name]
                cur, title, cur_k = (eid, p), "(title not printed)", k
                if ev["date"] not in roster[eid]["events"]:
                    roster[eid]["events"].append(ev["date"])
                roster[eid]["titles"][title] += 1
            k += 1
            continue
        has_role = bool(ROLE.search(nxt)) and len(nxt) < 120
        short_hdr = len(nxt) < 45 and not nxt.rstrip().endswith((".", ",", "?", "!", ":", ";"))
        is_speaker = l == "Operator" or l in VARIANT or (NAME.fullmatch(l) and len(l) < 45 and (has_role or short_hdr))
        if is_speaker:
            flush()
            cur, buf = None, []
            if l in VARIANT:
                eid = VARIANT[l]
                t = nxt if has_role else "(title not printed)"
                cur, title, cur_k = (eid, p), t, k
                if ev["date"] not in roster[eid]["events"]:
                    roster[eid]["events"].append(ev["date"])
                roster[eid]["titles"][t] += 1
            k += 1 if (l == "Operator" or (l in VARIANT and not has_role) or not (has_role or short_hdr)) else 2
            continue
        if cur:
            if buf and p != cur[1] and f"[page {p}]" not in buf:
                buf.append(f"[page {p}]")
            buf.append(l)
        k += 1
    flush()
for f in files.values():
    f.close()
json.dump({n: {"titles": dict(v["titles"]), "events": sorted(v["events"]), "words": v["words"]} for n, v in roster.items()},
          open(os.path.join(out, "roster.json"), "w"), indent=1)
for n, v in sorted(roster.items(), key=lambda kv: -kv[1]["words"]):
    ev = sorted(v["events"])
    print(f"{v['words']:7d} words {len(ev):3d} events {ev[0]}..{ev[-1]}  {n:11s} | {' / '.join(t for t, _ in v['titles'].most_common(3))[:120]}")
