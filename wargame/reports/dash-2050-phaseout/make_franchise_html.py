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
FRANCHISE = tuple(c for c, _ in TERMS)
VIEWS = [("game", "The brief"), ("core", "+ continuing value, services, closing costs"), ("core+overhead", "+ stranded overhead"),
         ("full", "+ widebody erosion")]
VSHORT = {"game": "The brief", "core": "+ Core terms", "core+overhead": "+ Overhead", "full": "+ Widebody", "high": "High case, all terms"}
IN_VIEW = {"game": (), "core": ("C0", "C1", "C2", "C6"), "core+overhead": ("C0", "C1", "C2", "C6", "C3_loaded"),
           "full": ("C0", "C1", "C2", "C6", "C3_loaded", "C4")}
for v, cs in IN_VIEW.items():
    assert tuple(FR["scenarios"][v]) == cs
assert tuple(FR["scenarios"]["full+programme"]) == ("C0", "C1", "C2", "C6", "C3_programme", "C4")
assert abs(FR["rates"][R8] - (1.105 / 1.022 - 1)) < 1e-12 and FR["rates"][R10] == 0.105
assert FR["params"]["c_exit"]["low"] == FR["params"]["c_exit"]["base"] == FR["params"]["c_exit"]["high"] == 3.0


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


def terms_sum(n, key, name, view, only=None):
    return sum(item(n, key, name, c) for c in IN_VIEW[view] if only is None or c in only)


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


def point(n, key, at="base"):
    """Every row's values in every column at a decision point (base, or just past the rule reading's thresholds), and
    the decision there."""
    p = RND[str(n)]["thresholds"][key]["points"][at]
    V = p["values"]
    return V, p["decision"], (lambda a, z: [x - y for x, y in zip(V[a], V[z])])


# the game-only thresholds are thresholds.json's, and the brief's items are cashflows.json's
for n in (1, 2, 3, 4):
    g = rng(n, "base|game|10.5%")
    th = TH["rounds"][str(n)]["range"]["margin"]
    assert abs(g[0] - th["low"]) < 1e-5 and ((g[1] is None and th["high"] is None) or abs(g[1] - th["high"]) < 1e-5)
CF = json.load(open(os.path.join(HERE, "data", "cashflows.json")))
assert abs(item(1, "base|10.5%", TEN, "game") - CF["plans"][TEN]["item_vs_dn"]) < 1e-9
assert abs(item(1, "base|10.5%", SEVEN, "game") - CF["plans"][SEVEN]["item_vs_dn"]) < 1e-9
# a 2030 launch has no counted year after 2060, so the demand restatement is zero in 2030 in every case and column
for key in ("base|10.5%", "base|8.1%", "low|10.5%", "high|10.5%", "low|8.1%", "high|8.1%"):
    for name, cols in RND["1"]["terms"][key].items():
        assert all(abs(c["C0"]) < 1e-12 for c in cols), (key, name)

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
# what happens at the base in 2030: the CEO picks the Re-engine, which fails the Board's downside test (as in the game)
RE_MIN = {}
for rate in (R10, R8):
    V, dec, it = point(1, "base|full|%s" % rate)
    assert dec["pick"] == "Re-engine" and not any(dec[md] for md in MODES)
    RE_MIN[rate] = min(it("Re-engine", "Do Nothing"))
    assert RE_MIN[rate] < -1.0
assert abs(RE_MIN[R10] - (-2.48)) < 0.01          # record/exco_result_r1.json: the Board vetoed the Re-engine at -2.48
# a 4% cut at 8.1%: the CEO picks the 10-year fps on new sites with the Re-engine; the Board vetoes the Re-engine beside
# it; the fps goes ahead alone
PAIR = TEN_NEW + " + Re-engine"
assert all(RND["1"]["thresholds"]["base|full|8.1%"][md]["plan_at_cut"] == TEN_NEW for md in MODES)
assert all(RND["1"]["thresholds"]["base|full|8.1%"][md]["plan_at_margin"] == TEN_NEW for md in MODES)
VETO = {}
for key, at in (("base|full|8.1%", "rule_cut"), ("high|full|8.1%", "base"), ("tail rising|full|8.1%", "base")):
    V, dec, it = point(1, key, at)
    assert dec["pick"] == PAIR and all(dec[md] == TEN_NEW for md in MODES), (key, dec)
    VETO[key] = {"pair_vs_alone": min(it(PAIR, TEN_NEW)), "alone": dec["e"][TEN_NEW]}
    assert VETO[key]["pair_vs_alone"] < -1.0
assert launched(1, "high|full|8.1%") == [TEN_NEW] * 4 and HM30_8[1] < M0         # the high case launches in 2030
assert launched(2, "high|full|8.1%") == [TEN] * 4 and all(not launched(n, "high|full|8.1%") for n in (3, 4))
assert launched(1, "tail rising|full|8.1%") == [TEN_NEW] * 4 and not launched(1, "tail as run|full|8.1%")
# how far the franchise moves the 2030 threshold (points of margin), at each end of the range and each rate
DROP = [100 * (a - z) for a, z in ((GM30[0], FM30[0]), (GM30[1], FM30[1]), (GM30_8[0], FM30_8[0]), (GM30_8[1], FM30_8[1]))]
assert 4.0 <= min(DROP) and max(DROP) <= 6.1
# launching later: the franchise terms fall about as discounting alone would; at 10.5% the total improves with every
# delay but stays behind Do Nothing; at 8.1% only a 2030 launch beats never launching, because share is lost
FV = {n: terms_sum(n, "base|10.5%", TEN, "full", only=FRANCHISE) for n in (1, 2, 3, 4)}
C0V = {n: item(n, "base|10.5%", TEN, "C0") for n in (1, 2, 3, 4)}
assert FV[1] > FV[2] > FV[3] > FV[4] > 0 and C0V[1] == 0 and min(C0V[n] for n in (2, 3, 4)) > 0
LW10 = {n: RND[str(n)]["launch_when"]["base|full|10.5%"][TEN] for n in (1, 2, 3, 4)}
LW8 = {n: RND[str(n)]["launch_when"]["base|full|8.1%"][TEN] for n in (1, 2, 3, 4)}
assert LW8[1] > 0 and all(LW8[n] < 0 for n in (2, 3, 4))
assert all(LW10[n] < 0 for n in (1, 2, 3, 4)) and LW10[1] < LW10[2] < LW10[3] < LW10[4]
for n in (1, 2, 3, 4):
    assert abs(LW10[n] - (item(n, "base|10.5%", TEN, "game") + FV[n] + C0V[n])) < 1e-9
for n in (2, 3):                                        # the fall is about what five or fifteen more years of discounting give
    disc = FV[1] / 1.105 ** (YEAR[n] - 2030)
    assert 0.8 < disc / FV[n] < 1.0, (n, disc, FV[n])
MAIN = {n: max(RND[str(n)]["weights"], key=RND[str(n)]["weights"].get) for n in (1, 2, 3, 4)}
SHARE = {n: RND[str(n)]["plans"][TEN][int(MAIN[n])]["pref_last"] for n in (1, 2, 3, 4)}
assert SHARE[1] > SHARE[2] > SHARE[3] > SHARE[4]
# most of the continuing value is earned after 2060
CAL = FR["calibration"]
DF60 = 1.105 ** -(2060 - 2026)
assert 0.03 < DF60 < 0.035
# the other overhead reading works against the fps; the price concession works for it (both like for like with the full view)
C3P = item(1, "base|10.5%", TEN, "C3_programme")
C5 = item(1, "base|10.5%", TEN, "C5")
assert C3P < 0 < item(1, "base|10.5%", TEN, "C3_loaded") and C5 > 0
PRG30, PRC30 = rng(1, "base|full+programme|10.5%"), rng(1, "base|full+price|10.5%")
PRC30_8 = rng(1, "base|full+price|8.1%")
assert PRG30[0] > FM30[0] > M0 and PRC30[0] > M0 and not launched(1, "base|full+price|10.5%") and not launched(1, "base|full+price|8.1%")
TL = {t: rng(1, "tail %s|full|10.5%%" % t) for t in ("as run", "held", "rising")}
TL8 = {t: rng(1, "tail %s|full|8.1%%" % t) for t in ("as run", "held", "rising")}
assert TL["held"] == FM30 and TL8["held"] == FM30_8
assert TL["rising"][1] < TL["held"][1] < TL["as run"][1]
SP10 = [100 * (TL["as run"][i] - TL["rising"][i]) for i in (0, 1)]
SP8 = [100 * (TL8["as run"][i] - TL8["rising"][i]) for i in (0, 1)]
assert 1.5 < min(SP10) and max(SP10) < 2.5 and 2.5 < min(SP8) and max(SP8) < 5.5
# 2045 and 2050: out of reach on any tail; most of the fall from the brief is the counted years restated on held demand
M3, M4 = rng(3, "base|full|10.5%"), rng(4, "base|full|10.5%")
M3R, M4R = rng(3, "tail as run|full|10.5%"), rng(4, "tail as run|full|10.5%")
assert M3[0] > 0.6 and M4[0] > 0.9 and M3R[0] > 0.95 and M4R[0] > 2.0
# closing costs: held at $3.0B in the combined cases; +-$1.5B moves the 2030 10-year item by half its closing-cost line
C6_10 = item(1, "base|10.5%", TEN, "C6")
assert C6_10 < 0 and abs(0.5 * C6_10) < 0.1
LAST_MAX = RND["1"]["terms"]["base|10.5%"][TEN][1]["_years"]["last_max"]
assert LAST_MAX == 2045 and RND["1"]["terms"]["base|10.5%"]["Do Nothing"][1]["_years"]["last_max"] == 2059
# the low case's derivative (25% of the bill) can cost more than the late-life profit it sustains: at 8.1% the low case
# needs a slightly higher margin than the brief for a 2045 or 2050 launch
for n in (3, 4):
    assert rng(n, "low|full|8.1%")[0] > rng(n, "base|game|8.1%")[0]


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
    cols = (("base|10.5%", TEN), ("base|10.5%", SEVEN), ("base|8.1%", TEN), ("base|8.1%", SEVEN))
    rows = [["<b>The brief</b>"] + [b(item(1, k, p, "game")) for k, p in cols]]
    for c, label in TERMS:
        rows.append([label] + [b(item(1, k, p, c)) for k, p in cols])
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
    head = ["", "The brief, 10.5%", "Counted years after 2060, 10.5%", "Franchise terms, 10.5%", "With the franchise, 10.5%", "The brief, 8.1%", "With the franchise, 8.1%"]
    rows = []
    for plan in (TEN, SEVEN):
        rows.append(f"{plan}, against Do Nothing")
        for n in (1, 2, 3, 4):
            g = item(n, "base|10.5%", plan, "game")
            c0 = item(n, "base|10.5%", plan, "C0")
            f = terms_sum(n, "base|10.5%", plan, "full", only=FRANCHISE)
            g8 = item(n, "base|8.1%", plan, "game")
            f8 = terms_sum(n, "base|8.1%", plan, "full")
            assert abs(RND[str(n)]["launch_when"]["base|full|8.1%"][plan] - (g8 + f8)) < 1e-9
            assert abs(RND[str(n)]["launch_when"]["base|full|10.5%"][plan] - (g + c0 + f)) < 1e-9
            rows.append([f"Launch in {YEAR[n]}", b(g), b(c0) if abs(c0) >= 0.005 else '<span class="muted">·</span>', b(f), f"<b>{b(g + c0 + f)}</b>", b(g8), f"<b>{b(g8 + f8)}</b>"])
    return ctable(head, rows, num_cols=(1, 2, 3, 4, 5, 6))


def tail_table():
    head = ["Demand after 2060", "Margin needed, 10.5%", "Margin needed, 8.1%"]
    f0 = lambda v: f"{K.rnd(v, 0):,.0f}"
    lab = {"as run": f"As run: the run's own curve, from {f0(DEM['as run'][2060])} a year in 2060 to {f0(DEM['as run'][2075])} in 2075; COMAC's protected sales take what is left",
           "held": f"Held at the 2060 market, {f0(DEM['held'][2075])} a year (base)",
           "rising": f"Rising: the conservative game's curve shape from 2060, {f0(DEM['rising'][2070])} a year by 2070"}
    rows = [[esc(lab[t]), rtxt(*TL[t]), rtxt(*TL8[t]) + (" (launches)" if launched(1, "tail %s|full|8.1%%" % t) else "")] for t in ("as run", "held", "rising")]
    return ctable(head, rows, num_cols=(1, 2))


PARAM_ROWS = [
    ("Continuing value",
     "fps profit after its 20 counted years, to its 50th year in service (\"a product that's going to be out there for 50 years\", Boeing's CFO, 2025, B-2278). The margin fades from 25.64% toward the game's A320neo margin of 13.14% by year 50 (Mauboussin's fade of excess returns; Morningstar gives wide-moat firms at least 20 years). Less a sustaining derivative at year 27, with the game's debt penalty.",
     "Derivative 12.5% of the bill (25% / 10%); fade by year 50 (in 10 years / none); demand held at 2060 (as run / rising)",
     "Moderate: the horizon and fade are standard analyst practice (Morningstar, McKinsey, Mauboussin). The derivative share rests on Boeing's CFO putting re-engine R&D at 10-15% of a clean sheet's (2011, B-0432); the 25% low case uses Bair's $2-3B for the MAX against $10-12B for a clean sheet (research file)"),
    ("Services",
     "Boeing's services profit on every narrowbody it delivers, by the aircraft's age, over a 25-year average life. Boeing's NMA study counted this kind of lifecycle value on top of the airplane's own NPV (Muilenburg, 2018, B-1457).",
     "$0.084M per aircraft-year ($0.045M / $0.135M): $0.38M of fleet-tied revenue at 22% ($0.30M at 15% / $0.45M at 30%)",
     "Weak to moderate: Boeing Global Services' 2024 commercial revenue and margin are sourced (10-K FY2024; Goldman Sachs split, an analyst estimate). The revenue per narrowbody (from a 14,000-aircraft fleet count, an inferred fleet-tied share and a size weighting) and the 15-30% margin range are inferences; cross-checked against the price Mitsubishi paid for CRJ support"),
    ("Stranded overhead",
     "Shared Boeing Commercial Airplanes overhead carried by narrowbody volume. When volume falls it can be cut only 15% a year, and 35% of it never goes. The game's margins are read as fully loaded, so only the unabsorbed part counts.",
     "$1.91B a year ($1.51B / $2.40B): depreciation $0.74B plus 45% of $5.0B G&A, times a 64% narrowbody share; never-cut share 35% (20% / 50%); cut 15% a year (25% / 10%)",
     "Moderate for the pools: FY2024 10-K (BCA depreciation $0.74B, Boeing's G&A $5.0B) and Goldman Sachs's narrowbody shares (analyst estimates). BCA's 40-50% share of G&A, the never-cut share and the cut speed are judgement: no source gives them. Goldman Sachs estimates $1.1-3.7B a year of unabsorbed BCA overhead in 2019-23 (its split of Boeing's reported loss; analyst estimate)"),
    ("Widebody erosion",
     "Widebody share Boeing loses while it has no new narrowbody in service, phased in as the MAX runs off (package and single-supplier campaigns lost).",
     "5 points of the 170-a-year widebody market (0 / 15)",
     "Weak, judgement: no source sizes it. The 15-point case is by analogy with McDonnell Douglas, whose order share fell to 3-4% once it stopped launching new aircraft and which the FTC found no longer a meaningful competitive force (1997); the MD-11 ended after the merger"),
    ("Closing costs",
     "Half when the MAX ends (every plan; about 2042-45 with an fps, as its buyers move to the fps), half when Boeing leaves narrowbodies (Do Nothing by 2060). The option to come back is valued at zero.",
     "$3.0B, in every case (it costs the fps in 2030-35 and helps it later, so it is not moved with the others)",
     "Moderate: Douglas $1.4B pre-tax in 1997 (about $2.8B today), Saab's SKr4bn after-tax provision, BAE £250M for the RJ; none of eight airliner makers that left came back (research file)"),
    ("Counted years after 2060",
     "Not a franchise term but consistency: where the brief's own 20 counted years run past 2060 (launches from 2035), they are restated on the same demand tail as the rest, so each tail is one world. Zero for a 2030 launch and on the run's own curve.",
     "Follows the demand tail",
     "Arithmetic on the game's own supply-and-demand engine"),
]


def param_table():
    return ctable(["Term", "What it counts", "Base (low / high)", "Evidence"], [[f"<b>{esc(a)}</b>", esc(b_), esc(c), esc(d)] for a, b_, c, d in PARAM_ROWS],
                  cls="cards wide", txt_cols=(1, 2, 3))


HISTORY = [
    ("2003-06", "Leaves niches on a plain business case",
     "Ended the 757 (2004) and the 717 (2005, about $380M of charges: \"the overall market for the airplane does not support continuing 717 production\"). The A321neo later took 71% of the upper narrowbody against 29% for the MAX 9/10 (Avolon, 2017); the NMA that was meant to win it back was shelved in 2020.",
     "Boeing releases 2003-10-16, 8-K Jan 2005; AIN 2017-08-31; B-1436, B-1613"),
    ("2011", "Defends the core with the cheapest adequate product",
     "\"If it looked like we are putting meaningful market share at risk by waiting to do a new airplane, we would re-engine instead\" (McNerney). Boeing's CFO put re-engine R&D at about 10-15% of a clean sheet's. The MAX came after American put 260 of 460 aircraft with Airbus, three months after the CEO said a three-to-four-year gap would not lose customers.",
     "B-0422, B-0432, B-0338; AMR 8-K 2011-07-20"),
    ("2012", "Sets a share red line of about 40%",
     "\"We do not want them to get to 60% and us, 40%... they come down the learning curve faster than we do, they have pricing power\" (Albaugh). Boeing now holds about 34% of the single-aisle backlog.",
     "B-0638; AIN 2026-01-07"),
    ("2016-22", "Says share is not the test",
     "\"It will not be based on market share. We are not in business just to chase market share\" (Muilenburg, 2016). In 2022 Calhoun dropped 50-50 as an objective: \"Whether we get to 50-50 ... is not an objective of ours. I want to get to stable\", putting a stable 737 production rate first.",
     "B-1131, B-1936"),
    ("2016-18", "Values programmes as franchises",
     "Tanker: \"a 50-, 60-year widebody franchise. And that's the way we think about it\" (Muilenburg). T-X and MQ-25 bids were made \"to create long-term, valuable products and services franchises\". The NMA study counted services and lifecycle value on top of the airplane's own NPV (2018); the NMA was not launched.",
     "BX-1033, BX-1545, B-1457"),
    ("2019-21", "Pays to keep the capability",
     "Kept the 737 workforce and supply chain through the grounding: about $5B of abnormal production costs, a revealed price for not losing the line.",
     "B-1618, FY2020 10-K"),
    ("2025-26", "Today: a successor will come, on three conditions",
     "Market, technology and Boeing's own financial and capacity readiness, \"not now on all 3\" (Ortberg, 2025). \"There will be a day where we have to enter into a new program. That day is not today, and it's not any time near\" (Malave, 2026). The CFO before him called it a 50-year product.",
     "BX-1296, B-2278; Transcript Digest (4) p.100"),
]

OTHERS = [
    ("Analysts never stop at a programme's horizon",
     ["Morningstar runs an explicit forecast, a fade and a perpetuity, and gives wide-moat firms such as Boeing at least 20 years of excess returns. It estimates that \"half of Boeing's enterprise value is derived from its 737 product line\" (analyst estimate).",
      "Barclays (2019) put the whole narrowbody industry at $238B of present value, about $2.4B per share point (analyst estimate).",
      "McKinsey's value-driver formula and Mauboussin's competitive-advantage period are the standard tools: excess returns fade toward the cost of capital rather than stopping."]),
    ("Airbus pays to stay in",
     ["Airbus launched the A320neo for just over EUR 1bn of investment and, in Leahy's words, left the CSeries \"virtually no business case\"; it has 11,529 orders.",
      "When customers rejected the first A350, Airbus committed about EUR 11.6bn to the A350 XWB (EADS launch budget, 2006) rather than cede the segment.",
      "Faury on the next single-aisle: \"If we move first, the supply chain will come to us.\""]),
    ("Leaving is close to permanent",
     ["McDonnell Douglas took 3-4% of 1996 world orders, against a 12% ten-year average share in the EEA (EC M.877), once it stopped launching new aircraft; the FTC found it \"no longer ... a meaningful competitive force\".",
      "None of eight airliner makers that left the market since 1962 came back: three large-jet makers (Convair, Lockheed, Douglas) and five regional and small-jet makers (Fokker to Bombardier).",
      "Exits cost more than a year's losses (Saab's SKr4bn after-tax provision was about four years of its average loss; Douglas $1.4B pre-tax; BAE £250M for the RJ, plus £150M for other commercial activities), and the installed base outlives the exit: Rolls-Royce sold its IAE stake for $1.5bn plus flight-hour payments, and says its installed base \"is where the majority of the value of the business lies\"."]),
    ("Other industries say the same",
     ["Christensen and colleagues (HBR, 2008): the do-nothing case wrongly assumes \"the present health of the company will persist\".",
      "Dixit (1989): exit and re-entry are hysteretic (firms stay in below breakeven and come back only well above it); with a re-entry cost of at least the fps bill, Boeing's exit would be close to irreversible (inference).",
      "Intel left DRAM and GE applied \"number one or two\" only once the position was already lost and the capital had a better use; Boeing's narrowbody meets neither condition (inference)."]),
]


def calib_table():
    dn = CAL["dn_max_profit_pv"]["Airbus launches NGSA"]
    head = ["", "The brief", "Analysts and practice"]
    rows = [["Do Nothing's 737 MAX profit, 2026-2060", f"{b(dn, 1, False)} today", "Morningstar: about half of Boeing's enterprise value comes from the 737 line, about $65B on the game's $130B enterprise value for Boeing (analyst estimate)"],
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
    vc, vh, vr = VETO["base|full|8.1%"], VETO["high|full|8.1%"], VETO["tail rising|full|8.1%"]
    tiles = [
        ("2030 margin needed, the brief", rtxt(*GM30), f"the fps margin at which Boeing launches in 2030, across the four readings of the CEO's rule. The game's fps earns {pct(M0, 2)}."),
        ("With the franchise, 10.5%", rtxt(*FM30), f"all five terms at their base values: about {K.rnd(100 * (GM30[0] - FM30[0]), 0):.0f} points lower, still {K.rnd(100 * (FM30[0] - M0), 0):.0f}-{K.rnd(100 * (FM30[1] - M0), 0):.0f} points short. No launch."),
        ("With the franchise, 8.1%", rtxt(*FM30_8), f"the fps now beats Do Nothing ({bp(G10_8 + F10_8, 1)} to {bp(G7_8 + F7_8, 1)}) but not the 787 Re-engine alone ({bp(RE_8, 1)}), which the CEO picks and the Board vetoes, as in the game: Do Nothing. A {pct(FC30_8[0], 0)} cut in Boeing's share of the bill launches the 10-year fps on new sites."),
        ("What waiting costs, at 8.1%", " → ".join(nw(esc(bp(LW8[n], 1))) for n in (1, 2, 3)), "the 10-year fps at Renton with the franchise, against Do Nothing, launched in 2030, 2035 or 2045, in today's money. At 10.5% it is behind on every date."),
    ]
    tiles_html = '<div class="tiles">' + "".join(f'<div class="panel tile"><div class="k">{esc(k)}</div><div class="v">{v if v.startswith("<") else esc(v)}</div><div class="d">{esc(d)}</div></div>' for k, v, d in tiles) + "</div>"
    hist = ctable(["When", "What Boeing did", "What it shows", "Evidence"], [[esc(a), f"<b>{esc(b_)}</b>", esc(c), esc(d)] for a, b_, c, d in HISTORY],
                  txt_cols=(1, 2, 3))
    others = '<div class="ev">' + "".join(f'<div class="panel"><h3>{esc(t)}</h3><ul>{"".join(f"<li>{esc(x)}</li>" for x in xs)}</ul></div>' for t, xs in OTHERS) + "</div>"
    lo_case10 = item(1, "low|10.5%", TEN, "game") + terms_sum(1, "low|10.5%", TEN, "full")
    hi_case10 = item(1, "high|10.5%", TEN, "game") + terms_sum(1, "high|10.5%", TEN, "full")
    m2 = rng(2, "base|full|10.5%")
    c1_10 = item(1, "base|10.5%", TEN, "C1")
    sh = lambda n: f"{K.rnd(100 * SHARE[n], 0):.0f}%"
    n_find = sum(len(r["findings"]) for r in RS["research"])
    pts = lambda xs: f"{K.rnd(min(xs), 0):.0f}" if K.rnd(min(xs), 0) == K.rnd(max(xs), 0) else f"{K.rnd(min(xs), 0):.0f}-{K.rnd(max(xs), 0):.0f}"
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
2045 and 2050 stay out of reach ({rtxt(*M3)} and {rtxt(*M4)}). Most of that fall is demand, not franchise: a 2045 or 2050 fps's own counted years run past 2060, where the run's curve collapses,
and the base holds that demand up. On the run's own curve the margin needed is {rtxt(*M3R)} and {rtxt(*M4R)}.</div></div>
<div class="panel"><div><b>At 8.1% the fps comes close; it launches only in the high case or if demand rises</b>
Most of the franchise is earned after 2060, when a dollar is worth {K.rnd(DF60 * 100, 0):.0f} cents today at 10.5%. At 8.1% the brief's own 2030 threshold drops to {rtxt(*GM30_8)} and the franchise
takes it to {rtxt(*FM30_8)}. The fps then beats Do Nothing, but the 787 Re-engine alone is worth more, so the CEO picks the Re-engine; the Board vetoes it on its downside test
({b(RE_MIN[R8])} in the two A350 Re-engine columns), as it did in the game's 2030 round at 10.5% ({b(RE_MIN[R10])}), and Boeing does nothing.
In the high case, or if demand rises after 2061, the CEO picks the 10-year fps on new sites with the Re-engine; the Board vetoes the Re-engine beside it (about {b(vh["pair_vs_alone"], 1)} in the A350 Re-engine column)
and the fps goes ahead alone, at {b(vh["alone"], 1)} against Do Nothing in the high case and {b(vr["alone"], 1)} with rising demand. The high case also launches the 10-year at Renton in the 2035 brief.</div></div>
<div class="panel"><div><b>At 8.1%, only a 2030 launch beats never launching</b>
With the franchise, the 10-year at Renton is {b(LW8[1])} against Do Nothing launched in 2030, {b(LW8[2])} in 2035 and {b(LW8[3])} in 2045. Delay costs share: Boeing's preference at the end of the game's years
falls from {sh(1)} for a 2030 launch to {sh(2)} for 2035 and {sh(3)} for 2045. At 10.5% discounting outweighs that: each delay makes the fps less bad ({b(LW10[1])}, {b(LW10[2])}, {b(LW10[3])}) but never good,
while the margin it needs rises ({rtxt(*FM30)} in 2030, {rtxt(*m2)} in 2035). The franchise terms themselves fall from {b(FV[1])} to {b(FV[3])} between a 2030 and a 2045 launch, about what fifteen more years of discounting give.</div></div>
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
(the latest fps's 50th year in service). After 2060, every year, counted by the brief or not, comes from the game's own supply-and-demand engine run on one of three demand tails,
with Boeing's preference held where the game left it, so each tail is one consistent world. In this world the 737 MAX is gone from 2060 in every plan and in the status quo,
so Do Nothing earns no narrowbody profit after 2060.</p>
<p class="cap">Views used below: <b>core</b> is continuing value, services and closing costs (with the brief's counted years after 2060 put on the same demand, which is zero for a 2030 launch); then <b>+ overhead</b> adds stranded overhead;
then <b>+ widebody</b> adds widebody erosion (judgement). The high and low cases move every parameter together toward or against the fps, except closing costs.</p></div>
<div class="panel">{param_table()}</div>
</div></section>

<section><h2>2030: what the franchise adds</h2><div class="stack">
<div class="panel"><p class="ctitle">The franchise terms close about a third of the 10-year fps's gap to Do Nothing; continuing value is most of it</p>
<div class="legend"><span><i class="sq" style="background:var(--pos)"></i>Value against Do Nothing</span><span><i class="sq" style="background:var(--s1)"></i>Adds to the fps</span><span><i class="sq" style="background:var(--s2)"></i>Takes from it</span></div>
<div class="cw only-wide">{waterfall()}</div><div class="cw only-narrow">{waterfall(True)}</div>
<p class="cap">10-year fps at Renton against Do Nothing, 2030 brief, column "Airbus launches NGSA", at 10.5%. Closing costs are slightly against the fps here: the fps takes over the MAX's deliveries by {LAST_MAX},
so half the closing costs come about {2060 - (LAST_MAX + 1)} years before Do Nothing's in 2060.</p></div>
<div class="panel">{bridge_table()}
<p class="cap">Low and high cases move every parameter together toward or against the fps (the low case's 10-year total at 10.5% is {b(lo_case10)}, the high case's {b(hi_case10)}), except closing costs,
held at $3.0B: $1.5B either way moves the 10-year's 2030 value by {b(0.5 * abs(C6_10), 2, False)}. The 787 Re-engine alone is the plan the CEO's rule compares the fps with: under the plain reading an fps plan
has to be worth more than $1B above it; the worst-column and premium readings set a lower bar.</p></div>
</div></section>

<section><h2>Does it change the decision?</h2><div class="stack">
<div class="panel"><p class="ctitle">The margin Boeing needs falls by {K.rnd(min(DROP), 0):.0f}-{K.rnd(max(DROP), 0):.0f} points in 2030; among these views only the high case at 8.1% reaches the fps's margin (rising demand after 2061 does too, below)</p>
<div class="legend"><span><i class="sw" style="background:var(--s1)"></i>at 10.5%</span><span><i class="sw" style="background:var(--s2)"></i>at 8.1%</span><span>bars span the four readings of the CEO's rule</span></div>
<p class="label">2030 brief</p>
<div class="cw only-wide">{margin_chart(1)}</div><div class="cw only-narrow">{margin_chart(1, True)}</div>
<p class="label" style="margin-top:14px">2035 brief</p>
<div class="cw only-wide">{margin_chart(2)}</div><div class="cw only-narrow">{margin_chart(2, True)}</div>
<p class="cap">Margin the fps needs for Boeing to launch, with the bill as briefed. The game's fps earns {pct(M0, 2)} (dashed line). Below it, Boeing launches.</p></div>
<div class="panel">{threshold_table()}
<p class="cap">Bill cut: the share of Boeing's fps bill someone else would have to carry (partners, customers or government) for Boeing to launch at the game's margin. The four readings of the CEO's rule are those on the main report;
where they differ, the range is shown. In 2045 and 2050 the fps enters service so late that others would have to carry most of the bill. At 8.1% the 2030 cut launches the 10-year fps on new sites alone,
at {b(vc["alone"], 1)} against Do Nothing, after the Board vetoes the Re-engine beside it.</p></div>
</div></section>

<section><h2>Launch now or later</h2><div class="panel">{launch_table()}
<p class="cap">Each plan launched in that round against never launching, in the columns the CEO expected that round, in today's money. Rivals' moves up to each round are as the game played them, so the later rows
show the path the game took, not what Boeing could expect in 2030. Counted years after 2060: the brief's own years for a 2035-2050 launch, put on the base's held demand instead of the run's falling curve.
The franchise terms fall with delay about as discounting alone would.</p></div></section>

<section><h2>What the result depends on</h2><div class="stack">
<div class="panel"><p class="ctitle">Demand after 2060 moves the 2030 threshold by about {pts(SP10)} points at 10.5% and {pts(SP8)} at 8.1%, enough to launch the fps at 8.1% if demand rises</p>{tail_table()}
<p class="cap">New 737/A320-class demand a year. All terms on, base values otherwise. The run's own curve holds only replacement of today's fleet plus growth, so it falls after 2060; holding the 2060 market is the base.</p></div>
<div class="panel"><p class="ctitle">Two terms left out of the views, and what they would do</p><ul class="cav">
<li><b>Overhead read the other way.</b> If the game's margins are programme margins with no overhead in them, every plan carries the overhead it keeps, and an fps keeps all of it for 50 years.
The term then works against the fps ({b(C3P)} for the 10-year in 2030, instead of {b(item(1, "base|10.5%", TEN, "C3_loaded"))}), and with all other terms on the 2030 margin needed is {rtxt(*PRG30)} instead of {rtxt(*FM30)}.
The repo does not document the margins' basis; Boeing's programme accounting absorbs production overhead, so the fully loaded reading is the base.</li>
<li><b>The MAX conceding price against NGSA.</b> 1.5% of the MAX price from 2037, full in Do Nothing, half on fps plans: {b(C5)} for the 10-year in 2030. Added to all the other terms, the 2030 margin needed is {rtxt(*PRC30)} at 10.5% and {rtxt(*PRC30_8)} at 8.1%.
It is left out because it conflicts with the game's own supply-and-demand state, which already sets the MAX's sales.</li>
</ul></div>
<div class="panel"><p class="ctitle">The brief values the narrowbody at a fraction of what analysts do</p>{calib_table()}
<p class="cap">The comparison is an inference: the brief's figures are pre-tax operating profit in constant dollars; the analysts' are after-tax enterprise values. The gap comes mostly from the discount rate and the 20-year window.</p></div>
</div></section>

<section><h2>Notes</h2><div class="panel"><ul class="cav">
<li><b>Not counted:</b> anything after the fps's 50th year in service (no successor, no perpetuity), tax and working capital, a probability that the franchise case fails (the MAX grounding cost about $18.6B; a 20% failure chance would cut continuing value and services by a fifth), and the option to come back after leaving (valued at zero).</li>
<li><b>Overlay, not a replay:</b> rivals do not react to Boeing's valuation, and the CEO's and the Board's rules (the $1B business-case test, the −$1B downside test, the $2B rating buffer and the $1B tie rule) are applied unchanged.</li>
<li><b>Derivative:</b> the sustaining derivative is always bought. In the low case (25% of the bill) it can cost more than the late-life profit it sustains: at 8.1% the low case needs a slightly higher margin than the brief for a 2045 or 2050 launch.</li>
<li><b>Rates:</b> at 8.1% every line of the brief is re-discounted and the debt penalty re-priced at the new present value; the dashboard's debt logic is not re-run.</li>
<li><b>Sources:</b> {n_find} sourced findings from Boeing's calls and filings in the repo, Goldman Sachs and Morgan Stanley models (analyst estimates) and published sources, with the model design and two adversarial checks, in data/franchise_research.json.
Some web quotes come from search excerpts because the hosts could not be fetched; the file marks each finding's confidence.</li>
<li><b>Files:</b> franchise.py writes data/franchise.json; make_franchise_html.py builds this page and asserts its claims against it.</li>
</ul></div></section>
<footer>BOEING PROPRIETARY. Built by make_franchise_html.py from run dash-2050-phaseout.</footer></div>
<script>{K.JS}</script></body></html>'''
    for bad in ("Milk", "Sabotage", "C3_", "C0", "C1 ", "pi_s", "F_nb", "kappa", " his ", " he ", " she ", " her "):
        assert bad not in page, bad
    with open(out_path, "w") as f:
        f.write(page)
    print("wrote", out_path, len(page))


if __name__ == "__main__":
    build(os.path.join(HERE, "fps_franchise.html"))
