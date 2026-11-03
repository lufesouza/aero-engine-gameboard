"""Build fps_franchise.html: what staying in, or leaving, the narrowbody market is worth beyond what Boeing's brief
counts, from Boeing's history and how analysts, Airbus and companies that left their markets value it, and whether it
changes Boeing's fps decision in the MAX phase-out game.

Reads data/franchise.json (franchise.py: the six terms, every plan and column of every round, and Boeing's decision
re-run with them), data/thresholds.json (thresholds.py) and data/franchise_research.json (the sourced findings behind
the parameters). Every figure on the page comes from those files; the claims in the copy are asserted below.

  python3 make_franchise_html.py
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050-obj"))
import page_kit as K  # noqa: E402

esc = K.esc
FR = json.load(open(os.path.join(HERE, "data", "franchise.json")))
TH = json.load(open(os.path.join(HERE, "data", "thresholds.json")))
RS = json.load(open(os.path.join(HERE, "data", "franchise_research.json")))
M0 = FR["constants"]["M0"]
RND = FR["rounds"]
YEAR = {int(n): r["year"] for n, r in RND.items()}
MODES = ("rule", "pairwise", "worst_first", "premium")
R10, R8 = "10.5%", "8.1%"
TEN, SEVEN, TEN_NEW = "10-year at Renton", "7-year at Renton", "10-year, new sites"
TERMS = [("C1", "Continuing value"), ("C2", "Services"), ("C3_loaded", "Stranded overhead"), ("C4", "Widebody erosion"), ("C6", "Closing costs")]
VIEWS = [("game", "The brief"), ("core", "+ continuing value, services, closing costs"), ("core+overhead", "+ stranded overhead"),
         ("full", "+ widebody erosion")]
VSHORT = {"game": "The brief", "core": "+ Core terms", "core+overhead": "+ Overhead", "full": "+ Widebody", "high": "High case, all terms"}
IN_VIEW = {"game": (), "core": ("C1", "C2", "C6"), "core+overhead": ("C1", "C2", "C6", "C3_loaded"), "full": ("C1", "C2", "C6", "C3_loaded", "C4")}
for v, cs in IN_VIEW.items():
    assert tuple(FR["scenarios"][v]) == cs
assert abs(FR["rates"][R8] - (1.105 / 1.022 - 1)) < 1e-12 and FR["rates"][R10] == 0.105


def b(v, dp=2, sign=True):
    return K.usd(v, dp, sign and K.rnd(v, dp) != 0)


def bp(v, dp=2, sign=True):
    return re.sub(r"<[^>]+>", "", b(v, dp, sign))


def pct(x, dp=1):
    return f"{K.rnd(100 * x, dp):.{dp}f}%"


def nw(s):
    return f'<span class="nw">{s}</span>'


# ─────────────────────────────── the numbers ───────────────────────────────
def item(n, key, name, c, src="terms"):
    """A term (or the game's value) for `name` against Do Nothing in the CEO's expected columns of round n."""
    r = RND[str(n)]
    t = r[src][key]
    return sum((t[name][int(i)][c] - t["Do Nothing"][int(i)][c]) * wt for i, wt in r["weights"].items())


def terms_sum(n, key, name, view):
    return sum(item(n, key, name, c) for c in IN_VIEW[view])


def rng(n, key, what="margin"):
    """Low and high of a threshold across the four readings of the CEO's rule (None: not reached)."""
    t = RND[str(n)]["thresholds"][key]
    xs = [t[md][what] for md in MODES]
    lo = min((x for x in xs if x is not None), default=None)
    hi = None if any(x is None for x in xs) else max(xs)
    return lo, hi


def rtxt(lo, hi, f=pct, none="not reached"):
    if lo is None:
        return none
    if hi is None:
        return f"{f(lo)} or more"
    a, z = f(lo), f(hi)
    return a if a == z else f"{a[:-1]}–{z}" if a.endswith("%") and z.endswith("%") else f"{a}–{z}"


def cut_txt(lo, hi):
    if lo is None:
        return "no cut is enough"
    return rtxt(lo, hi, lambda x: pct(x, 0))


def launched(n, key):
    t = RND[str(n)]["thresholds"][key]["base"]
    return [t[md] for md in MODES if t[md]]


# the game-only thresholds are thresholds.json's, and the brief's items are cashflows.json's
for n in (1, 2, 3, 4):
    g = rng(n, "base|game|10.5%")
    th = TH["rounds"][str(n)]["range"]["margin"]
    assert abs(g[0] - th["low"]) < 1e-5 and ((g[1] is None and th["high"] is None) or abs(g[1] - th["high"]) < 1e-5)
CF = json.load(open(os.path.join(HERE, "data", "cashflows.json")))
assert abs(item(1, "base|10.5%", TEN, "game") - CF["plans"][TEN]["item_vs_dn"]) < 1e-9
assert abs(item(1, "base|10.5%", SEVEN, "game") - CF["plans"][SEVEN]["item_vs_dn"]) < 1e-9

G10, G7 = item(1, "base|10.5%", TEN, "game"), item(1, "base|10.5%", SEVEN, "game")
F10, F7 = terms_sum(1, "base|10.5%", TEN, "full"), terms_sum(1, "base|10.5%", SEVEN, "full")
G10_8, G7_8 = item(1, "base|8.1%", TEN, "game"), item(1, "base|8.1%", SEVEN, "game")
F10_8, F7_8 = terms_sum(1, "base|8.1%", TEN, "full"), terms_sum(1, "base|8.1%", SEVEN, "full")
RE_8 = item(1, "base|8.1%", "Re-engine", "game")
GM30, FM30, FM30_8, HM30, HM30_8 = (rng(1, k) for k in ("base|game|10.5%", "base|full|10.5%", "base|full|8.1%", "high|full|10.5%", "high|full|8.1%"))
GM30_8 = rng(1, "base|game|8.1%")
FC30_8 = rng(1, "base|full|8.1%", "cut")
SHARE_CLOSED = F10 / -G10
# the claims in the copy
assert G10 < 0 and G7 < 0 and G10 + F10 < 0 and G7 + F7 < 0                  # behind Do Nothing with the terms on
assert 0.3 < SHARE_CLOSED < 0.4
for n in (1, 2, 3, 4):                                                           # no launch at 10.5%, any case, any view
    for lv in ("low", "base", "high"):
        for v in IN_VIEW:
            assert not launched(n, "%s|%s|10.5%%" % (lv, v)), (n, lv, v)
            lo, hi = rng(n, "%s|%s|10.5%%" % (lv, v))
            assert lo > M0
assert FM30[0] < GM30[0] and FM30[1] < GM30[1]
assert not launched(1, "base|full|8.1%") and FM30_8[0] > M0                       # 8.1%: close, no launch
assert G10_8 + F10_8 > 0 and G7_8 + F7_8 > 0 and RE_8 > G7_8 + F7_8 + 1.0        # beats Do Nothing, not the Re-engine alone
assert launched(1, "high|full|8.1%") == [TEN_NEW] * 4 and HM30_8[1] < M0         # the high case launches in 2030
assert launched(2, "high|full|8.1%") == [SEVEN] * 4 and all(not launched(n, "high|full|8.1%") for n in (3, 4))
assert launched(1, "tail rising|full|8.1%") == [TEN_NEW] * 4 and not launched(1, "tail as run|full|8.1%")
# how far the franchise moves the 2030 threshold (points of margin), at each end of the range and each rate
DROP = [100 * (a - z) for a, z in ((GM30[0], FM30[0]), (GM30[1], FM30[1]), (GM30_8[0], FM30_8[0]), (GM30_8[1], FM30_8[1]))]
assert 4.0 <= min(DROP) and max(DROP) <= 6.1
# the franchise is worth less the later the launch, and at 8.1% only 2030 beats never launching
FV = {n: terms_sum(n, "base|10.5%", TEN, "full") for n in (1, 2, 3, 4)}
assert FV[1] > FV[2] > FV[3] > FV[4] > 0
LW8 = {n: RND[str(n)]["launch_when"]["base|full|8.1%"][TEN] for n in (1, 2, 3, 4)}
assert LW8[1] > 0 and all(LW8[n] < 0 for n in (2, 3, 4))
for n in (1, 2, 3, 4):
    assert abs(RND[str(n)]["launch_when"]["base|full|10.5%"][TEN] - (item(n, "base|10.5%", TEN, "game") + FV[n])) < 1e-9
# most of the continuing value is earned after 2060
CAL = FR["calibration"]
DF60 = 1.105 ** -(2060 - 2026)
assert 0.03 < DF60 < 0.035
# the other overhead reading works against the fps; the price concession works for it
C3P = item(1, "base|10.5%", TEN, "C3_programme")
C5 = item(1, "base|10.5%", TEN, "C5")
assert C3P < 0 < item(1, "base|10.5%", TEN, "C3_loaded") and C5 > 0
PRG30, PRC30 = rng(1, "base|core+programme|10.5%"), rng(1, "base|full+price|10.5%")
PRC30_8 = rng(1, "base|full+price|8.1%")
assert PRG30[0] > M0 and PRC30[0] > M0 and not launched(1, "base|full+price|10.5%")
TL = {t: rng(1, "tail %s|full|10.5%%" % t) for t in ("as run", "held", "rising")}
TL8 = {t: rng(1, "tail %s|full|8.1%%" % t) for t in ("as run", "held", "rising")}
assert TL["held"] == FM30 and TL8["held"] == FM30_8
assert TL["rising"][1] < TL["held"][1] < TL["as run"][1]


# demand after 2060 on each tail (the 737/A320 class, after the class share), for the copy
DG = os.path.join(HERE, "..", "..", "dashgame")
CLASS = json.load(open(os.path.join(DG, "supply_demand.json")))["demand"]["class_share"]


def curve(path):
    c = json.load(open(path))
    return {y: (r + g) * CLASS for y, r, g in zip(c["years"], c["replacements"], c["growth"])}


DEM = {"as run": curve(os.path.join(DG, "demand_page_n0.json")),
       "held": curve(os.path.join(HERE, "data", "curves", "franchise_held.json")),
       "rising": curve(os.path.join(HERE, "data", "curves", "franchise_rising.json"))}
assert abs(DEM["as run"][2060] - DEM["held"][2075]) < 1e-9 and DEM["as run"][2075] < 200 < 1700 < DEM["rising"][2070]


# ─────────────────────────────── charts ───────────────────────────────
def waterfall(narrow=False):
    """The 2030 bridge for the 10-year at Renton against Do Nothing, at 10.5%: the brief, each term, the total."""
    rows = [("The brief", 0.0, G10, "total")]
    cum = G10
    for c, label in TERMS:
        v = item(1, "base|10.5%", TEN, c)
        rows.append((label, cum, cum + v, "pos" if v >= 0 else "neg"))
        cum += v
    rows.append(("With the franchise", 0.0, cum, "total"))
    assert abs(cum - (G10 + F10)) < 1e-9
    lo, hi = -7.0, 0.5
    if narrow:
        w, left, right, rh, top = 400, 12, 12, 50, 10
    else:
        w, left, right, rh, top = 760, 196, 70, 36, 10
    h = top + rh * len(rows) + 30
    sx = lambda v: left + (v - lo) / (hi - lo) * (w - left - right)
    out = [K.svg_open(w, h, "Bridge from the brief's value of the 10-year fps at Renton against Do Nothing to its value with the franchise terms, 2030", "chart narrow" if narrow else "chart")]
    for v in range(int(lo), 1):
        x = sx(v)
        out.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{top}" y2="{h - 26}" class="{"zero" if v == 0 else "grid"}"/>')
        if not narrow or v % 2 == 0:
            out.append(f'<text x="{x:.1f}" y="{h - 10}" text-anchor="middle" class="tick">{bp(v, 0, False)}</text>')
    for i, (label, x0, x1, kind) in enumerate(rows):
        y = top + i * rh
        val = bp(x1 - x0 if kind != "total" else x1)
        col = {"total": "var(--pos)", "pos": "var(--s1)", "neg": "var(--s2)"}[kind]
        if narrow:
            out.append(f'<text x="{left}" y="{y + 15}" class="rowlab sm">{esc(label)}</text>'
                       f'<text x="{w - right}" y="{y + 15}" text-anchor="end" class="val">{val}</text>')
            by, bh = y + 22, 16
        else:
            out.append(f'<text x="{left - 10}" y="{y + rh / 2 + 5:.1f}" text-anchor="end" class="rowlab sm{" strong" if kind == "total" else ""}">{esc(label)}</text>')
            by, bh = y + 8, rh - 16
        a, z = sx(min(x0, x1)), sx(max(x0, x1))
        out.append(f'<rect x="{a:.1f}" y="{by:.1f}" width="{max(2.0, z - a):.1f}" height="{bh}" rx="3" fill="{col}"/>')
        if not narrow:
            tx = sx(max(x0, x1, 0.0) if kind == "total" else max(x0, x1)) + 6
            out.append(f'<text x="{tx:.1f}" y="{y + rh / 2 + 5:.1f}" class="val">{val}</text>')
        if i + 1 < len(rows):                     # connector to the next bar
            nxt = top + (i + 1) * rh + (22 if narrow else 8)
            out.append(f'<line x1="{sx(x1):.1f}" x2="{sx(x1):.1f}" y1="{by + bh:.1f}" y2="{nxt:.1f}" class="leader" stroke-dasharray="3 3"/>')
        out.append(f'<rect x="0" y="{y}" width="{w}" height="{rh}" class="hit" {K.mark_attrs((label, "", None), (val, "change" if kind != "total" else "against Do Nothing", col), (bp(x1), "running total", None))}/>')
    out.append("</svg>")
    return "".join(out)


def margin_chart(n, narrow=False):
    """Margin the fps needs for Boeing to launch in round n, by view, at 10.5% and 8.1% (low-high across readings)."""
    rows = [(VSHORT[v], "base|%s" % v) for v, _ in VIEWS] + [(VSHORT["high"], "high|full")]
    lo_x, hi_x = 0.20, 0.46
    if narrow:
        w, left, right, rh, top = 400, 12, 12, 62, 28
    else:
        w, left, right, rh, top = 760, 190, 96, 44, 28
    h = top + rh * len(rows) + 28
    sx = lambda v: left + (min(max(v, lo_x), hi_x) - lo_x) / (hi_x - lo_x) * (w - left - right)
    out = [K.svg_open(w, h, "fps margin needed for Boeing to launch in %d, by view, at 10.5%% and 8.1%%" % YEAR[n], "chart narrow" if narrow else "chart")]
    for k in range(20, 47, 5 if not narrow else 5):
        x = sx(k / 100)
        out.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{top}" y2="{h - 24}" class="grid"/><text x="{x:.1f}" y="{h - 8}" text-anchor="middle" class="tick">{k}%</text>')
    xr = sx(M0)
    out.append(f'<line x1="{xr:.1f}" x2="{xr:.1f}" y1="{top - 6}" y2="{h - 24}" class="ref" stroke-dasharray="4 3"/>'
               f'<text x="{xr + 5:.1f}" y="{top - 10}" class="reflab">fps margin in the game, {pct(M0, 2)}</text>')
    for i, (label, key) in enumerate(rows):
        y = top + i * rh
        txt = []
        for j, (rate, col) in enumerate(((R10, "var(--s1)"), (R8, "var(--s2)"))):
            lo, hi = rng(n, "%s|%s" % (key, rate))
            t = rtxt(lo, hi)
            txt.append((rate, t))
            if narrow:
                by = y + 24 + j * 15
            else:
                by = y + 8 + j * 15
            a, z = sx(lo), sx(hi if hi is not None else lo)
            if z - a < 6:
                a, z = (a + z) / 2 - 3, (a + z) / 2 + 3
            out.append(f'<rect x="{a:.1f}" y="{by:.1f}" width="{z - a:.1f}" height="10" rx="5" fill="{col}"/>')
            if not narrow:
                out.append(f'<text x="{z + 6:.1f}" y="{by + 9:.1f}" class="val sm">{esc(t)}</text>')
        if narrow:
            out.append(f'<text x="{left}" y="{y + 14}" class="rowlab sm">{esc(label)}</text>')
            out.append(f'<text x="{w - right}" y="{y + 14}" text-anchor="end" class="val sm">{esc(txt[0][1])} · {esc(txt[1][1])}</text>')
        else:
            out.append(f'<text x="{left - 10}" y="{y + 22}" text-anchor="end" class="rowlab sm">{esc(label)}</text>')
        out.append(f'<rect x="0" y="{y}" width="{w}" height="{rh}" class="hit" {K.mark_attrs((label, "", None), (txt[0][1], "at 10.5%", "var(--s1)"), (txt[1][1], "at 8.1%", "var(--s2)"))}/>')
    out.append("</svg>")
    return "".join(out)


# ─────────────────────────────── tables ───────────────────────────────
def ctable(head, rows, num_cols=(), cls="cards", txt_cols=()):
    """A table that becomes labelled cards on a phone (each cell carries its column's label)."""
    th = "".join(f'<th scope="col"{" class=n" if i in num_cols else ""}>{h}</th>' for i, h in enumerate(head))
    body = []
    for r in rows:
        if isinstance(r, str):            # a group header row
            body.append(f'<tr class="grp"><th scope="rowgroup" colspan="{len(head)}">{r}</th></tr>')
            continue
        cells = []
        for j, c in enumerate(r):
            if j == 0:
                cells.append(f'<th scope="row">{c}</th>')
            else:
                k = "n" if j in num_cols else ("txt" if j in txt_cols else "")
                lab = re.sub(r"<[^>]+>", "", head[j])
                cells.append(f'<td{f" class={k}" if k else ""} data-label="{esc(lab, quote=True)}">{c}</td>')
        body.append("<tr>" + "".join(cells) + "</tr>")
    return f'<div class="scroll"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'


def bridge_table():
    head = ["", "10-year at Renton, 10.5%", "7-year at Renton, 10.5%", "10-year at Renton, 8.1%", "7-year at Renton, 8.1%"]
    rows = [["<b>The brief</b>"] + [b(item(1, k, p, "game")) for k, p in (("base|10.5%", TEN), ("base|10.5%", SEVEN), ("base|8.1%", TEN), ("base|8.1%", SEVEN))]]
    for c, label in TERMS:
        rows.append([label] + [b(item(1, k, p, c)) for k, p in (("base|10.5%", TEN), ("base|10.5%", SEVEN), ("base|8.1%", TEN), ("base|8.1%", SEVEN))])
    tot = lambda k, p, lv="base": item(1, "%s|%s" % (lv, k), p, "game") + terms_sum(1, "%s|%s" % (lv, k), p, "full")
    rows.append(["<b>With the franchise</b>"] + [f"<b>{b(tot(k, p))}</b>" for k, p in ((R10, TEN), (R10, SEVEN), (R8, TEN), (R8, SEVEN))])
    rows.append(["Low case, all terms"] + [b(tot(k, p, "low")) for k, p in ((R10, TEN), (R10, SEVEN), (R8, TEN), (R8, SEVEN))])
    rows.append(["High case, all terms"] + [b(tot(k, p, "high")) for k, p in ((R10, TEN), (R10, SEVEN), (R8, TEN), (R8, SEVEN))])
    rows.append(["<i>The 787 Re-engine alone, for comparison</i>"] + [b(item(1, "base|%s" % k, "Re-engine", "game")) for k in (R10, R10, R8, R8)])
    return ctable(head, rows, num_cols=(1, 2, 3, 4))


def threshold_table():
    head = ["", "Margin needed, 10.5%", "Bill cut needed, 10.5%", "Margin needed, 8.1%", "Bill cut needed, 8.1%"]
    rows = []
    for n in (1, 2, 3, 4):
        rows.append(f"{YEAR[n]} brief")
        for v, label in VIEWS + [("high", "High case, all terms")]:
            key = "high|full" if v == "high" else "base|%s" % v
            cells = [esc(VSHORT[v])]
            for rate in (R10, R8):
                cells.append(rtxt(*rng(n, "%s|%s" % (key, rate))))
                cells.append(cut_txt(*rng(n, "%s|%s" % (key, rate), "cut")))
            if launched(n, "%s|%s" % (key, R8)):
                cells[3] = cells[3] + " (launches)"
            rows.append(cells)
    return ctable(head, rows, num_cols=(1, 2, 3, 4))


def launch_table():
    head = ["", "The brief, 10.5%", "Franchise terms, 10.5%", "With the franchise, 10.5%", "The brief, 8.1%", "With the franchise, 8.1%"]
    rows = []
    for plan in (TEN, SEVEN):
        rows.append(f"{plan}, against Do Nothing")
        for n in (1, 2, 3, 4):
            g = item(n, "base|10.5%", plan, "game")
            f = terms_sum(n, "base|10.5%", plan, "full")
            g8 = item(n, "base|8.1%", plan, "game")
            f8 = terms_sum(n, "base|8.1%", plan, "full")
            assert abs(RND[str(n)]["launch_when"]["base|full|8.1%"][plan] - (g8 + f8)) < 1e-9
            rows.append([f"Launch in {YEAR[n]}", b(g), b(f), f"<b>{b(g + f)}</b>", b(g8), f"<b>{b(g8 + f8)}</b>"])
    return ctable(head, rows, num_cols=(1, 2, 3, 4, 5))


def tail_table():
    head = ["Demand after 2061", "Margin needed, 10.5%", "Margin needed, 8.1%"]
    f0 = lambda v: f"{K.rnd(v, 0):,.0f}"
    lab = {"as run": f"As run: the run's own curve, from {f0(DEM['as run'][2060])} a year in 2060 to {f0(DEM['as run'][2075])} in 2075; COMAC's protected sales take what is left",
           "held": f"Held at the 2060 market, {f0(DEM['held'][2075])} a year (base)",
           "rising": f"Rising: the conservative game's curve shape from 2060, {f0(DEM['rising'][2070])} a year by 2070"}
    rows = [[esc(lab[t]), rtxt(*TL[t]), rtxt(*TL8[t]) + (" (launches)" if launched(1, "tail %s|full|8.1%%" % t) else "")] for t in ("as run", "held", "rising")]
    return ctable(head, rows, num_cols=(1, 2))


PARAM_ROWS = [
    ("Continuing value",
     "fps profit after its 20 counted years, to its 50th year in service (\"a product that's going to be out there for 50 years\", Boeing's CFO, 2025, B-2278). The margin fades from 25.64% toward the game's A320neo margin of 13.14% by year 50 (Mauboussin's fade of excess returns; Morningstar gives wide-moat firms at least 20 years). Less a sustaining derivative at year 27, with the game's debt penalty. Deliveries come from the game's own supply-and-demand engine run on past 2061.",
     "Derivative 12.5% of the bill (25% / 10%); fade by year 50 (in 10 years / none); demand held at 2060 (as run / rising)",
     "Moderate: the horizon and fade are standard analyst practice (Morningstar, McKinsey, Mauboussin); the derivative share rests on Boeing's own 10-15% re-engine figure (B-0432)"),
    ("Services",
     "Boeing's services profit on every narrowbody it delivers, by the aircraft's age, over a 25-year average life. Boeing's own business cases added this lifecycle value to the airplane's NPV (Muilenburg, 2018, B-1457).",
     "$0.084M per aircraft-year ($0.045M / $0.135M): $0.38M of fleet-tied revenue at 22% ($0.30M at 15% / $0.45M at 30%)",
     "Moderate: from Boeing Global Services' 2024 revenue and margin over the 14,000-aircraft fleet (10-K FY2024; Goldman Sachs split, an analyst estimate); cross-checked against the price Mitsubishi paid for CRJ support"),
    ("Stranded overhead",
     "Shared Boeing Commercial Airplanes overhead carried by narrowbody volume. When volume falls it can be cut only 15% a year, and 35% of it never goes. The game's margins are read as fully loaded, so only the unabsorbed part counts.",
     "$1.91B a year ($1.51B / $2.40B): depreciation $0.74B plus 45% of $5.0B G&A, times a 64% narrowbody share; never-cut share 35% (20% / 50%); cut 15% a year (25% / 10%)",
     "Moderate: FY2024 10-K cost pools and Goldman Sachs's narrowbody shares (analyst estimates); Boeing booked $1.1-3.7B a year of unabsorbed cost in 2019-23 (Goldman Sachs; research file)"),
    ("Widebody erosion",
     "Widebody share Boeing loses while it has no new narrowbody in service, phased in as the MAX runs off (package and single-supplier campaigns lost).",
     "5 points of the 170-a-year widebody market (0 / 15)",
     "Weak, judgement: no source sizes it. The 15-point case is McDonnell Douglas, whose MD-11 ended once Douglas stopped launching narrowbodies (FTC 1997)"),
    ("Closing costs",
     "Half when the MAX ends (every plan; earlier with Renton, where the fps takes over its lines), half when Boeing leaves narrowbodies (Do Nothing by 2060). The option to come back is valued at zero.",
     "$3.0B ($1.5B / $4.5B)",
     "Moderate: Douglas $1.4B in 1997 (about $2.8B today), Saab SKr4bn, BAE £400M; none of eight airframers that left came back (research file)"),
]


def param_table():
    return ctable(["Term", "What it counts", "Base (low / high)", "Evidence"], [[f"<b>{esc(a)}</b>", esc(b_), esc(c), esc(d)] for a, b_, c, d in PARAM_ROWS],
                  cls="cards wide", txt_cols=(1, 2, 3))


HISTORY = [
    ("2003-06", "Leaves niches on a plain business case",
     "Ended the 757 (2004) and the 717 (2005, about $380M of charges: \"the overall market for the airplane does not support continuing 717 production\"). The A321neo later took 71% of the upper narrowbody against 29% for the MAX 9/10 (Avolon, 2017); the NMA that was meant to win it back was shelved in 2020.",
     "Boeing releases 2003-10-16, 8-K Jan 2005; AIN 2017-08-31; B-1436, B-1613"),
    ("2011", "Defends the core with the cheapest adequate product",
     "\"If it looked like we are putting meaningful market share at risk by waiting to do a new airplane, we would re-engine instead\" (McNerney). The MAX cost about 10-15% of a clean sheet. It came after American put 260 of 460 aircraft with Airbus, three months after the CEO said a three-to-four-year gap would not lose customers.",
     "B-0422, B-0432, B-0338; AMR 8-K 2011-07-20"),
    ("2012-22", "Sets a share floor of about 40%",
     "\"We do not want them to get to 60% and us, 40%... they come down the learning curve faster than we do, they have pricing power\" (Albaugh, 2012). Calhoun in 2022: \"If stable is at 40 without China, then that's what we want to do.\" Boeing now holds about 34% of the single-aisle backlog.",
     "B-0638, B-1936; AIN 2026-01-07"),
    ("2016", "Says share is not the test",
     "\"It will not be based on market share. We are not in business just to chase market share\" (Muilenburg). The business case decides.",
     "B-1131"),
    ("2016-18", "Values programmes as franchises",
     "Tanker: \"a 50-, 60-year widebody franchise. And that's the way we think about it\" (Muilenburg). T-X and MQ-25 bids were made \"to create long-term, valuable products and services franchises\". The NMA case added services and lifecycle value to the airplane's own NPV.",
     "BX-1033, BX-1545, B-1457"),
    ("2019-21", "Pays to keep the capability",
     "Kept the 737 workforce and supply chain through the grounding: about $5B of abnormal production costs, a revealed price for not losing the line.",
     "B-1618, FY2020 10-K"),
    ("2025-26", "Today: a successor is coming, on three conditions",
     "Market, technology and Boeing's own financial and capacity readiness, \"not now on all 3\" (Ortberg, 2025). \"There will be a day where we have to enter into a new program. That day is not today\" (Malave, 2026). The CFO before him called it a 50-year product.",
     "BX-1296, B-2278; Transcript Digest (4) p.100"),
]

OTHERS = [
    ("Analysts never stop at a programme's horizon",
     ["Morningstar runs an explicit forecast, a fade and a perpetuity, and gives wide-moat firms such as Boeing at least 20 years of excess returns. It estimates that \"half of Boeing's enterprise value is derived from its 737 product line\" (analyst estimate).",
      "Barclays (2019) put the whole narrowbody industry at $238B of present value, about $2.4B per share point (analyst estimate).",
      "McKinsey's value-driver formula and Mauboussin's competitive-advantage period are the standard tools: excess returns fade toward the cost of capital rather than stopping."]),
    ("Airbus pays to stay in",
     ["The A320neo cost just over EUR 1bn and, in Leahy's words, left the CSeries \"virtually no business case\"; it has 11,529 orders.",
      "When customers rejected the first A350, Airbus spent about EUR 11.6bn on the A350 XWB rather than cede the segment (EADS, 2006).",
      "Faury on the next single-aisle: \"If we move first, the supply chain will come to us.\""]),
    ("Leaving is close to permanent",
     ["McDonnell Douglas took 3-4% of 1996 orders against a 12% ten-year average once it stopped launching products; the FTC found it \"no longer ... a meaningful competitive force\".",
      "None of eight airframers that left large commercial aircraft since 1962 came back (Convair to Bombardier).",
      "Exits cost one to three years of the segment's losses (Douglas $1.4B, Saab SKr4bn, BAE £400M), and the installed base outlives the exit: Rolls-Royce sold its IAE stake for $1.5bn plus flight-hour payments, and says its installed base \"is where the majority of the value of the business lies\"."]),
    ("Other industries say the same",
     ["Christensen and colleagues (HBR, 2008): the do-nothing case wrongly assumes \"the present health of the company will persist\".",
      "Dixit (1989): exit and re-entry are hysteretic, so an exit is close to irreversible.",
      "Intel left DRAM and GE applied \"number one or two\" only once the position was already lost and the capital had a better use; Boeing's narrowbody meets neither condition (inference)."]),
]


def calib_table():
    dn = CAL["dn_max_profit_pv"]["Airbus launches NGSA"]
    head = ["", "The brief", "Analysts and practice"]
    rows = [["Do Nothing's 737 MAX profit, 2026-2060", f"{b(dn, 1, False)} today", "Morningstar: about half of Boeing's enterprise value comes from the 737 line, about $65B on the board's $130B (analyst estimate)"],
            ["One narrowbody share point", f"{b(CAL['share_point_pv_10yr'], 2, False)} today (20 fps a year, {CAL['eis_10yr']}-{CAL['eis_10yr'] + 19})", "Barclays: about $2.4B (the industry's $238B, 2019 dollars; analyst estimate)"],
            ["Discount rate", "10.5% on constant 2026 dollars, about 12.9% nominal", "8-10% nominal: Morningstar Boeing 8.6%, Goldman Sachs Airbus 9%, Rolls-Royce 8.46%"],
            ["Horizon", "20 years from entry into service; Do Nothing to 2060; nothing after", "Explicit forecast, then a fade, then a perpetuity"]]
    assert 19.5 < dn < 20.5 and 0.6 < CAL["share_point_pv_10yr"] < 0.66
    return ctable(head, rows, txt_cols=(1, 2))


CSS_EXTRA = """
table.cards tr.grp th { background: var(--sunk); font: 600 .78rem/1.3 var(--font-mono); letter-spacing: .06em; text-transform: uppercase; color: var(--muted); }
table.cards.wide td.txt, table.cards td.txt { font-size: .88rem; }
table.cards td.txt { min-width: 14rem; }
.legend i.sw { width: 14px; height: 10px; border-radius: 5px; }
.ev { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 12px; }
.ev h3 { font: 600 1.02rem/1.3 var(--font-body); margin: 0 0 6px; }
.ev ul { margin: 0; padding-left: 18px; font-size: .9rem; } .ev li { margin-bottom: 6px; text-wrap: pretty; }
.chart .rowlab.sm.strong { font-weight: 700; }
ul.cav li, footer, td.txt { overflow-wrap: anywhere; }
@media (max-width: 640px) {
  table.cards { min-width: 0 !important; }
  table.cards thead { display: none; }
  table.cards, table.cards tbody, table.cards tr, table.cards th, table.cards td { display: block; width: auto; }
  table.cards tr { border-bottom: 1px solid var(--line); padding: 8px 10px; }
  table.cards tr.grp { padding: 0; }
  table.cards tr.grp th { padding: 7px 10px; }
  table.cards tbody th { min-width: 0; border: 0; padding: 0 0 4px; font-weight: 600; }
  table.cards td { border: 0; padding: 3px 0; display: flex; justify-content: space-between; align-items: baseline; gap: 12px; text-align: right; white-space: normal; min-width: 0; }
  table.cards td::before { content: attr(data-label); flex: 1 1 0; min-width: 0; font: 600 11px var(--font-mono); color: var(--muted); text-transform: uppercase; letter-spacing: .03em; text-align: left; }
  table.cards td.txt { display: block; text-align: left; }
  table.cards td.txt::before { display: block; margin-bottom: 2px; }
}
"""


def build(out_path):
    tiles = [
        ("2030 margin needed, the brief", rtxt(*GM30), f"the fps margin at which Boeing launches in 2030, across the four readings of the CEO's rule. The game's fps earns {pct(M0, 2)}."),
        ("With the franchise, 10.5%", rtxt(*FM30), f"all five terms at their base values: about {K.rnd(100 * (GM30[0] - FM30[0]), 0):.0f} points lower, still {K.rnd(100 * (FM30[0] - M0), 0):.0f}-{K.rnd(100 * (FM30[1] - M0), 0):.0f} points short. No launch."),
        ("With the franchise, 8.1%", rtxt(*FM30_8), f"the fps now beats Do Nothing ({bp(G10_8 + F10_8, 1)} to {bp(G7_8 + F7_8, 1)}) but not the 787 Re-engine alone ({bp(RE_8, 1)}). A {pct(FC30_8[0], 0)} cut in Boeing's share of the bill would launch it."),
        ("What waiting costs", f"{bp(FV[1], 1)} → {bp(FV[2], 1)} → {bp(FV[3], 1)}", "what the franchise terms add to the 10-year fps at Renton if it is launched in 2030, 2035 or 2045, in today's money at 10.5%."),
    ]
    tiles_html = '<div class="tiles">' + "".join(f'<div class="panel tile"><div class="k">{esc(k)}</div><div class="v">{esc(v)}</div><div class="d">{esc(d)}</div></div>' for k, v, d in tiles) + "</div>"
    hist = ctable(["When", "What Boeing did", "What it shows", "Evidence"], [[esc(a), f"<b>{esc(b_)}</b>", esc(c), esc(d)] for a, b_, c, d in HISTORY],
                  txt_cols=(1, 2, 3))
    others = '<div class="ev">' + "".join(f'<div class="panel"><h3>{esc(t)}</h3><ul>{"".join(f"<li>{esc(x)}</li>" for x in xs)}</ul></div>' for t, xs in OTHERS) + "</div>"
    lo_case10 = item(1, "low|10.5%", TEN, "game") + terms_sum(1, "low|10.5%", TEN, "full")
    hi_case10 = item(1, "high|10.5%", TEN, "game") + terms_sum(1, "high|10.5%", TEN, "full")
    m2 = rng(2, "base|full|10.5%")
    m3, m4 = rng(3, "base|full|10.5%"), rng(4, "base|full|10.5%")
    c1_10 = item(1, "base|10.5%", TEN, "C1")
    n_find = sum(len(r["findings"]) for r in RS["research"])
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Narrowbody Franchise Value</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{K.CSS + CSS_EXTRA}</style></head><body><div class="wrap">
<header class="top"><p class="eyebrow">Boeing Product Development · war game rerun · MAX phase-out world · BOEING PROPRIETARY</p>
<h1>What staying in the narrowbody market is worth, and whether it changes the fps decision</h1>
<p class="lede">Boeing's brief counts an fps for 20 years from entry into service and Do Nothing to 2060. It counts nothing after that, and it never prices what leaving the narrowbody market costs.
This page builds that missing piece from how Boeing has valued its franchises since 2003 and from how analysts, Airbus and companies that left their markets value them.
It adds five terms to the brief, re-runs Boeing's decision rule with them, and reports the result at the game's 10.5% and at 8.1% (10.5% read as a nominal rate, less 2.2% inflation).</p>
<p class="gloss"><b>Basis.</b> Constant 2026 $B, pre-tax, discounted to 2026, against Do Nothing, in the columns the CEO expected each round (2030: Airbus launches NGSA).
Rivals' moves are held as the game played them: this is an overlay on Boeing's valuation, not a replay of the game. With the terms switched off, the model gives back the brief's value of every plan in every column
to the cent, and every decision threshold on the main report.</p></header>
<section style="margin-top:18px">{tiles_html}</section>

<section><h2>The answer</h2><div class="bl">
<div class="panel"><div><b>The franchise is worth about a third of the fps's gap to Do Nothing</b>
In 2030 the terms add {b(F10)} to the 10-year fps at Renton and {b(F7)} to the 7-year. The brief has them {b(-G10, 2, False)} and {b(-G7, 2, False)} behind Do Nothing; with the franchise they are
still {b(-(G10 + F10), 2, False)} and {b(-(G7 + F7), 2, False)} behind. Continuing value is the biggest term ({b(c1_10)} for the 10-year).</div></div>
<div class="panel"><div><b>At the game's 10.5%, no case changes any decision</b>
The margin Boeing needs falls in every round: 2030 from {rtxt(*GM30)} to {rtxt(*FM30)} (high case {rtxt(*HM30)}), 2035 to {rtxt(*m2)}. It never reaches {pct(M0, 2)}.
2045 and 2050 stay out of reach ({rtxt(*m3)} and {rtxt(*m4)}).</div></div>
<div class="panel"><div><b>The discount rate decides it</b>
Most of the franchise is earned after 2060, when a dollar is worth {K.rnd(DF60 * 100, 0):.0f} cents today at 10.5%. At 8.1% the brief's own 2030 threshold drops to {rtxt(*GM30_8)} and the franchise
takes it to {rtxt(*FM30_8)}. The fps then beats Do Nothing, but the 787 Re-engine alone is worth more, so the CEO's rule still picks the Re-engine.
In the high case at 8.1%, Boeing launches: the 10-year fps on new sites in 2030 (and the 7-year at Renton in the 2035 brief). So does the base case if demand rises after 2061.</div></div>
<div class="panel"><div><b>Waiting is where the franchise is lost</b>
At 8.1%, launching in 2030 is the only date that beats never launching ({b(LW8[1])} for the 10-year at Renton); from 2035 every launch is behind ({b(LW8[2])} in 2035, {b(LW8[3])} in 2045).
At 10.5% the franchise terms shrink from {b(FV[1])} for a 2030 launch to {b(FV[3])} for 2045. Do Nothing in 2030 is a deferral, and the deferral is what costs the franchise.</div></div>
</div></section>

<section><h2>How Boeing has valued staying in</h2><div class="stack">
<div class="panel"><p>Boeing has never left its core narrowbody market. It has left niches on a forward-looking business case, defended the core with the cheapest adequate product when share was at risk,
and, in its own programme decisions, counted franchise value that the war game's brief leaves out.</p></div>
<div class="panel">{hist}
<p class="cap">Evidence ids are the repo's Boeing evidence files (profiles/boeing/evidence.jsonl and executives/evidence.jsonl), each a quote from a call, filing or conference with its page.</p></div>
</div></section>

<section><h2>How others value it</h2>{others}</section>

<section><h2>The model: five terms added to the brief</h2><div class="stack">
<div class="panel"><p>Each term is a yearly flow for every plan in every column of every round, discounted like the brief and counted to the same end year within a round
(the latest fps entry into service plus 50 years). After 2061, the game's own supply-and-demand engine is run on, with Boeing's preference held where the game left it.
In this world the 737 MAX is gone from 2060 in every plan and in the status quo, so Do Nothing earns no narrowbody profit after 2060.</p>
<p class="cap">Views used below: <b>core</b> is continuing value, services and closing costs; then <b>+ overhead</b> adds stranded overhead; then <b>+ widebody</b> adds widebody erosion (judgement). The high and low cases move every parameter together toward or against the fps.</p></div>
<div class="panel">{param_table()}</div>
</div></section>

<section><h2>2030: what the franchise adds</h2><div class="stack">
<div class="panel"><p class="ctitle">The franchise terms close about a third of the 10-year fps's gap to Do Nothing; continuing value is most of it</p>
<div class="legend"><span><i class="sq" style="background:var(--pos)"></i>Value against Do Nothing</span><span><i class="sq" style="background:var(--s1)"></i>Adds to the fps</span><span><i class="sq" style="background:var(--s2)"></i>Takes from it</span></div>
<div class="cw only-wide">{waterfall()}</div><div class="cw only-narrow">{waterfall(True)}</div>
<p class="cap">10-year fps at Renton against Do Nothing, 2030 brief, column "Airbus launches NGSA", at 10.5%. Closing costs are slightly against the fps here: building at Renton ends the MAX in 2045,
so its closing costs come earlier than Do Nothing's in 2060.</p></div>
<div class="panel">{bridge_table()}
<p class="cap">Low and high cases move every parameter together (the low case's 10-year total at 10.5% is {b(lo_case10)}, the high case's {b(hi_case10)}). The 787 Re-engine alone is the plan the CEO's rule
compares the fps with: for the CEO to pick an fps plan, it has to be worth more than $1B above the Re-engine alone.</p></div>
</div></section>

<section><h2>Does it change the decision?</h2><div class="stack">
<div class="panel"><p class="ctitle">The margin Boeing needs falls by {K.rnd(min(DROP), 0):.0f}-{K.rnd(max(DROP), 0):.0f} points in 2030, but reaches the fps's margin only at 8.1%, in the high case</p>
<div class="legend"><span><i class="sw" style="background:var(--s1)"></i>at 10.5%</span><span><i class="sw" style="background:var(--s2)"></i>at 8.1%</span><span>bars span the four readings of the CEO's rule</span></div>
<p class="label">2030 brief</p>
<div class="cw only-wide">{margin_chart(1)}</div><div class="cw only-narrow">{margin_chart(1, True)}</div>
<p class="label" style="margin-top:14px">2035 brief</p>
<div class="cw only-wide">{margin_chart(2)}</div><div class="cw only-narrow">{margin_chart(2, True)}</div>
<p class="cap">Margin the fps needs for Boeing to launch, with the bill as briefed. The game's fps earns {pct(M0, 2)} (dashed line). Below it, Boeing launches.</p></div>
<div class="panel">{threshold_table()}
<p class="cap">Bill cut: the share of Boeing's fps bill someone else would have to carry (partners, customers or government) for Boeing to launch at the game's margin. The four readings of the CEO's rule are those on the main report;
where they differ, the range is shown. In 2045 and 2050 the fps enters service so late that others would have to carry most or all of the bill.</p></div>
</div></section>

<section><h2>Launch now or later</h2><div class="panel">{launch_table()}
<p class="cap">Each plan launched in that round against never launching, in the columns the CEO expected that round, in today's money. Rivals' moves up to each round are as the game played them, so the later rows
show the path the game took, not what Boeing could expect in 2030. The franchise terms shrink with every delay because the fps's later years move further out.</p></div></section>

<section><h2>What the result depends on</h2><div class="stack">
<div class="panel"><p class="ctitle">Demand after 2061 moves the 2030 threshold by about 2-3 points</p>{tail_table()}
<p class="cap">New 737/A320-class demand a year. All terms on, base values otherwise. The run's own curve holds only replacement of today's fleet plus growth, so it falls after 2060; holding the 2060 market is the base.</p></div>
<div class="panel"><p class="ctitle">Two terms left out of the views, and what they would do</p><ul class="cav">
<li><b>Overhead read the other way.</b> If the game's margins are programme margins with no overhead in them, every plan carries the overhead it keeps, and an fps keeps all of it for 50 years.
The term then works against the fps ({b(C3P)} for the 10-year in 2030, instead of {b(item(1, "base|10.5%", TEN, "C3_loaded"))}), and the 2030 margin needed is {rtxt(*PRG30)}. The repo does not document the margins' basis; Boeing's programme accounting absorbs production overhead, so the fully loaded reading is the base.</li>
<li><b>The MAX conceding price against NGSA.</b> 1.5% of the MAX price from 2037, full in Do Nothing, half on fps plans: {b(C5)} for the 10-year in 2030. With it, the 2030 margin needed is {rtxt(*PRC30)} at 10.5% and {rtxt(*PRC30_8)} at 8.1%.
It is left out because it conflicts with the game's own supply-and-demand state, which already sets the MAX's sales.</li>
</ul></div>
<div class="panel"><p class="ctitle">The brief values the narrowbody at a fraction of what analysts do</p>{calib_table()}
<p class="cap">The comparison is an inference: the brief's figures are pre-tax operating profit in constant dollars; the analysts' are after-tax enterprise values. The gap comes mostly from the discount rate and the 20-year window.</p></div>
</div></section>

<section><h2>Notes</h2><div class="panel"><ul class="cav">
<li><b>Not counted:</b> anything after the fps's 50th year (no successor, no perpetuity), tax and working capital, a probability that the franchise case fails (the MAX grounding cost about $18.6B; a 20% failure chance would cut continuing value and services by a fifth), and the option to come back after leaving (valued at zero).</li>
<li><b>Overlay, not a replay:</b> rivals do not react to Boeing's valuation, and the CEO's and the Board's rules (the $1B business-case test, the −$1B downside test, the $2B rating buffer and the $1B tie rule) are applied unchanged.</li>
<li><b>Derivative:</b> the sustaining derivative is always bought. In the low case (25% of the bill) it can cost more than the late-life profit it sustains, which is why the low case slightly raises the 2045 and 2050 thresholds.</li>
<li><b>Rates:</b> at 8.1% every line of the brief is re-discounted and the debt penalty re-priced at the new present value; the dashboard's debt logic is not re-run.</li>
<li><b>Sources:</b> {n_find} sourced findings from Boeing's calls and filings in the repo, Goldman Sachs and Morgan Stanley models (analyst estimates) and published sources, with the model design and two adversarial checks, in data/franchise_research.json.
Some web quotes come from search excerpts because the hosts could not be fetched; the file marks each finding's confidence.</li>
<li><b>Files:</b> franchise.py writes data/franchise.json; make_franchise_html.py builds this page and asserts its claims against it.</li>
</ul></div></section>
<footer>BOEING PROPRIETARY. Built by make_franchise_html.py from run dash-2050-phaseout.</footer></div>
<script>{K.JS}</script></body></html>'''
    assert "Milk" not in page and "Sabotage" not in page and "C3_" not in page and "pi_s" not in page
    with open(out_path, "w") as f:
        f.write(page)
    print("wrote", out_path, len(page))


if __name__ == "__main__":
    build(os.path.join(HERE, "fps_franchise.html"))
