#!/usr/bin/env python3
"""Usage: pages.py <transcripts|boeing_10k|airbus_fy2025> <first> [last]  -> prints those pages with their page markers."""
import os, re, sys
S = os.environ.get("WARGAME_BUILD_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "work"))
src, a = sys.argv[1], int(sys.argv[2]); b = int(sys.argv[3]) if len(sys.argv) > 3 else a
if src == "airbus_fy2025":
    import os
    for n in range(a, b + 1):
        f = f"{S}/text/airbus_pages/{n:03d}.txt"
        print(f"\n=== PAGE {n} ===\n" + (open(f).read() if os.path.exists(f) else "[page not OCR'd yet]"))
    sys.exit(0)
txt = open(f"{S}/text/{src}.txt").read()
parts = re.split(r"\n\n=== PAGE (\d+) ===\n", txt)[1:]
for i in range(0, len(parts), 2):
    n = int(parts[i])
    if a <= n <= b:
        print(f"\n=== PAGE {n} ===\n{parts[i+1]}")
