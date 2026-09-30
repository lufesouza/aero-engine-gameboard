"""Dump every non-empty cell of the three Rolls-Royce workbooks for citation.

Usage: rr_cells_dump.py <folder holding the workbooks, normally the repo root> <output folder>

One file per sheet, <source>__<sheet>.tsv, with lines: ref <TAB> value <TAB> row label
<TAB> nearest period header above. Source ids: ms_model (Morgan Stanley RR model,
28 Jan 2026), ciq_estimates (Capital IQ estimates report), ciq_segments (Capital IQ
segments, FY2015-FY2025). Also writes index.json and cells_cache.json, which
verify_cells.py reads (point RR_CELLS_DIR at the output folder).
Needs openpyxl and xlrd.
"""
import datetime, json, os, re, sys
import openpyxl, xlrd
from openpyxl.utils import get_column_letter
RAW = sys.argv[1]; OUT = sys.argv[2]
FILES = {"ms_model": "Morgan Stanley Rolls-Royce model.xlsm",
         "ciq_estimates": "Rolls-Royce Holdings plc LSE RR Estimates Report.xls",
         "ciq_segments": "Rolls-Royce Holdings plc LSE RR Financials Segments.xls"}
PER = re.compile(r"(^|\D)(19|20)\d\d(\D|$)|^(FY|FH|FQ|1H|2H|CY|H1|H2)|\d{2}e$|12 months|Dec-\d\d")
def fmt(v):
    if v is None: return ""
    if isinstance(v, bool): return str(v)
    if isinstance(v, float):
        if v == int(v) and abs(v) < 1e15: return str(int(v))
        return repr(round(v, 10))
    if isinstance(v, (datetime.datetime, datetime.date)): return v.strftime("%Y-%m-%d")
    return re.sub(r"\s+", " ", str(v)).strip()
def dump(src, sheet, grid):
    # grid: list of rows (lists)
    nrows = len(grid); ncols = max([len(r) for r in grid] + [0])
    def cell(r, c): return grid[r][c] if c < len(grid[r]) else None
    labels = {}
    for r in range(nrows):
        lab = []
        for c in range(min(ncols, 4)):
            v = fmt(cell(r, c))
            if v and not re.fullmatch(r"[-+0-9.eE%]+", v): lab.append(v)
        labels[r] = " | ".join(lab)
    # header rows: rows with >=3 period-looking cells
    hdr_rows = [r for r in range(nrows) if sum(1 for c in range(ncols) if PER.search(fmt(cell(r, c)) or "")) >= 3]
    lines, cache = [], {}
    for r in range(nrows):
        prev_h = [h for h in hdr_rows if h <= r]
        for c in range(ncols):
            v = cell(r, c); s = fmt(v)
            if not s: continue
            ref = f"{get_column_letter(c + 1)}{r + 1}"
            hdr = ""
            for h in reversed(prev_h):
                hv = fmt(cell(h, c))
                if hv: hdr = hv; break
            lines.append(f"{ref}\t{s}\t{labels[r]}\t{hdr}")
            cache[ref] = v if isinstance(v, (int, float, str, bool)) or v is None else s
    fn = f"{src}__{re.sub(r'[^A-Za-z0-9]+', '_', sheet).strip('_')}.tsv"
    with open(os.path.join(OUT, fn), "w") as f:
        f.write(f"# source={src} file={FILES[src]} sheet={sheet}\n# ref\tvalue\trow_label\tcolumn_header\n")
        f.write("\n".join(lines) + "\n")
    return fn, cache
index, allcache = {}, {}
for src, fn in FILES.items():
    path = os.path.join(RAW, fn)
    index[src] = {}; allcache[src] = {}
    if fn.lower().endswith(".xlsm"):
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        for ws in wb.worksheets:
            grid = [list(row) for row in ws.iter_rows(values_only=True, max_col=min(ws.max_column or 1, 200))]
            f, cache = dump(src, ws.title, grid)
            index[src][ws.title] = f; allcache[src][ws.title] = cache
    else:
        wb = xlrd.open_workbook(path, logfile=open(os.devnull, "w"))
        for s in wb.sheets():
            grid = []
            for r in range(s.nrows):
                row = []
                for c in range(s.ncols):
                    ce = s.cell(r, c); v = ce.value
                    if ce.ctype == xlrd.XL_CELL_DATE:
                        try: v = xlrd.xldate.xldate_as_datetime(v, wb.datemode).strftime("%Y-%m-%d")
                        except Exception: pass
                    if ce.ctype == xlrd.XL_CELL_EMPTY: v = None
                    row.append(v)
                grid.append(row)
            f, cache = dump(src, s.name, grid)
            index[src][s.name] = f; allcache[src][s.name] = cache
json.dump(index, open(os.path.join(OUT, "index.json"), "w"), indent=1)
json.dump(allcache, open(os.path.join(OUT, "cells_cache.json"), "w"))
print(json.dumps(index, indent=1))
