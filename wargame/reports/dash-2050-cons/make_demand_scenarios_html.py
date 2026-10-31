"""Build fps_demand_scenarios.html: the fps in service in 2039, 2041 or 2044 on the demand of the user's page
"Single-Aisle Replacement Story" (chart 4.1, every aircraft retiring 0-4 years later), valued as Boeing's 2030 brief
values it (run dash-2050-cons): which date is better for Boeing, and what would make each one a launch.

Every number comes from analysis/demand_scenarios/demand_scenarios.json (demand_scenarios.py) and the page's own demand
(analysis/demand_scenarios/page_demand.json, make_page_demand.py). The ranking claims the page makes are asserted.

Usage: python3 make_demand_scenarios_html.py [out.html]"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050-obj"))
import page_kit as K  # noqa: E402

esc = K.esc
A = os.path.join(HERE, "analysis", "demand_scenarios")
D = json.load(open(os.path.join(A, "demand_scenarios.json")))
PG = json.load(open(os.path.join(A, "page_demand.json")))
GAME = json.load(open(os.path.join(HERE, "..", "..", "dashgame", "demand_conservative.json")))
MINUS = K.MINUS
EIS = [int(e) for e in D["eis"]]
NS = list(D["scenarios"])
C = D["cases"]
BASE = D["base"]
M0, P0, B0 = BASE["margin"], BASE["price"], BASE["bill"]
TESTS = D["tests"]
SITE = {"renton": "Renton", "new_site": "new sites"}
NLAB = {"0": "As chapter 1 sets out", "1": "1 year later", "2": "2 years later", "3": "3 years later", "4": "4 years later"}
COL = {2039: "s1", 2041: "s2", 2044: "s3"}
UNIT_FPS = P0 * M0                        # $M operating profit per fps
UNIT_737 = 48.0 * 0.08                    # the dashboard's 737 MAX: $48M at 8%


def case(n, e):
    return C["N%s/%d" % (n, e)]


def best(c):
    return c["eval"][c["eval"]["best"]]


def b(v, dp=2, sign=True):
    return K.usd(v, dp, sign)


def bp(v, dp=2, sign=True):
    return re.sub(r"<[^>]+>", "", K.usd(v, dp, sign))


def pc(v, dp=1):
    return f"{K.rnd(v * 100, dp):.{dp}f}%"


def n0(v):
    return f"{K.rnd(v, 0):,.0f}"


def rng(vals, f):
    lo, hi = min(vals), max(vals)
    a, z = f(lo), f(hi)
    return a if a == z else f"{a} to {z}"


def mrange(e):
    return rng([case(n, e)["margin_needed"] for n in NS], lambda v: pc(v))


def brange(e):
    return rng([case(n, e)["bill_needed"] for n in NS], lambda v: f"${K.rnd(v, 1):.1f}B")


def erange(e):
    return rng([best(case(n, e))["expected"] for n in NS], lambda v: bp(v))


# ─────────────────────────────── facts the page states (asserted) ───────────────────────────────
ALL = [(n, e) for n in NS for e in EIS]
S = D["sensitivities"]


def sens(key, n, e):
    return S["%s/N%s/%d" % (key, n, e)]


def sbest(r):
    return r["eval"][r["eval"]["best"]]


def sw(n, e):
    return case(n, e)["same_window"]


def an(c):
    return c["analytic"][c["eval"]["best"]]


SENS_KEYS = ("tail", "page_from_2026", "tianjin", "page_supply")
assert not any(best(case(n, e))["passes"] for n, e in ALL), "an fps date passes: the page says none does"
assert not any(sbest(sw(n, e))["passes"] for n, e in ALL)
for n in NS:                               # 2039 needs the smallest move on margin, price, bill and ramp; 2044 the largest
    m = [case(n, e)["margin_needed"] for e in EIS]
    bl = [case(n, e)["bill_needed"] for e in EIS]
    p = [case(n, e)["price_cost_held"] for e in EIS]
    assert m[0] < m[1] < m[2] and bl[0] > bl[1] > bl[2] and p[0] < p[1] < p[2], (n, m, bl, p)
    r = [case(n, e)["ramp_needed"] or 99.0 for e in EIS]
    assert r[0] <= r[1] < r[2], (n, r)
    m = [sw(n, e)["margin_needed"] for e in EIS]
    bl = [sw(n, e)["bill_needed"] for e in EIS]
    assert m[0] < m[1] < m[2] and bl[0] > bl[1] > bl[2], (n, m, bl)
    for key in SENS_KEYS:
        m = [sens(key, n, e)["margin_needed"] for e in EIS]
        bl = [sens(key, n, e)["bill_needed"] for e in EIS]
        assert m[0] < m[1] < m[2] and bl[0] > bl[1] > bl[2], (key, n, m, bl)
        assert not any(sbest(sens(key, n, e))["passes"] for e in EIS)
    # feasibility of 2039: at a 9-year bill it still beats 2041; as the game's 7-year fps launched in 2032 it does not
    c39, c41 = case(n, 2039), case(n, 2041)
    assert c39["margin_bill9"] < c41["margin_needed"] < c39["margin_bill7"], (n, c39["margin_bill9"], c41["margin_needed"], c39["margin_bill7"])
for n, e in ALL:
    c = case(n, e)
    assert all(abs(v) < 1e-5 for v in c["confirm"].values())
    assert all(abs(v) < 1e-5 for v in sw(n, e)["confirm"].values())
    assert all(x["stress_ok"] for x in c["fundable"])
    assert not any(w["passes"] for w in c["worlds"].values())
    assert c["pref_needed"] is None
    assert c["eval"]["best"] == "renton" and sw(n, e)["eval"]["best"] == "renton"
for key in SENS_KEYS:
    for n, e in ALL:
        assert all(abs(v) < 1e-5 for v in sens(key, n, e)["confirm"].values())
EXP = {e: [best(case(n, e))["expected"] for n in NS] for e in EIS}
SWX = {e: [sbest(sw(n, e))["expected"] for n in NS] for e in EIS}
LO_EXP, HI_EXP = min(min(v) for v in EXP.values()), max(max(v) for v in EXP.values())
GAP_ALL = min(1.0 - x for v in EXP.values() for x in v)
SPREAD = max(max(EXP[e][i] for e in EIS) - min(EXP[e][i] for e in EIS) for i in range(len(NS)))
assert all(max(EIS, key=lambda e: SWX[e][i]) == 2044 for i in range(len(NS)))          # same window: 2044 loses least
P26X = {e: [sbest(sens("page_from_2026", n, e))["expected"] for n in NS] for e in EIS}
assert all(max(EIS, key=lambda e: P26X[e][i]) == 2044 for i in range(len(NS)))         # page demand from 2026: 2044 too
LEAST_BRIEF = {n: max(EIS, key=lambda e: best(case(n, e))["expected"]) for n in NS}
assert LEAST_BRIEF["0"] == 2039 and all(LEAST_BRIEF[n] == 2044 for n in ("2", "3", "4")), LEAST_BRIEF
for n in NS:                               # a 3-year NGSA slip helps every date, the 2039 fps most; more than faster erosion
    w = [case(n, e)["worlds"]["ngsa2040"]["expected"] - best(case(n, e))["expected"] for e in EIS]
    assert w[0] > max(w[1:]) and min(w) > 0, (n, w)
    assert all(case(n, e)["worlds"]["ngsa2040"]["expected"] - best(case(n, e))["expected"] >
               case(n, e)["worlds"]["erosion3"]["expected"] - best(case(n, e))["expected"] for e in EIS)
assert all(sbest(sens("page_supply", n, e))["expected"] > best(case(n, e))["expected"] for n, e in ALL)
TJ_WORSE = sum(sbest(sens("tianjin", n, e))["expected"] < best(case(n, e))["expected"] for n, e in ALL)
R44 = [case(n, 2044)["ramp_needed"] for n in NS]
assert all(case(n, 2044)["ramp_instant"]["margin"] > 0 for n in NS)
TO90 = {e: [case(n, e)["ramp_profiles"]["needed"]["to_90"] for n in NS if case(n, e)["ramp_needed"]] for e in EIS}
GAME_TO50, GAME_TO90 = case("0", 2039)["ramp_profiles"]["game"]["to_50"], case("0", 2039)["ramp_profiles"]["game"]["to_90"]
assert all(case(n, e)["ramp_profiles"]["game"]["to_90"] == GAME_TO90 for n, e in ALL)
SDJ = json.load(open(os.path.join(HERE, "..", "..", "dashgame", "supply_demand.json")))
D_CLASS = pc(SDJ["demand"]["class_share"], 2)
COST0 = BASE["cost"]
BILL7, BILL9 = BASE["bill7"], BASE["bill9"]
# partners: money free, the profit share it can take back, a fair partner
PT = {e: {paid: [an(case(n, e))["partner"][paid] for n in NS] for paid in ("0.25", "0.5")} for e in EIS}
assert all(x["passes_free"] for x in PT[2039]["0.25"]) and not any(x["passes_free"] for x in PT[2041]["0.25"] + PT[2044]["0.25"])
assert all(x["passes_free"] for e in EIS for x in PT[e]["0.5"])
PKG = {e: [case(n, e)["package"] for n in NS] for e in EIS}
assert all(x["passes_free"] for e in (2039, 2041) for x in PKG[e])
PKG44_PASS = [n for n, x in zip(NS, PKG[2044]) if x["passes_free"]]
assert PKG44_PASS == ["2", "3", "4"], PKG44_PASS
# preference: what +10 points is worth, where it levels off, how full Boeing's factories are
PREF = {e: [case(n, e)["pref_sweep"] for n in NS] for e in EIS}
PREF10 = {e: [p["10.0"]["expected"] - p["0.0"]["expected"] for p in PREF[e]] for e in EIS}
PREFMAX = {e: [p["100.0"]["expected"] for p in PREF[e]] for e in EIS}
assert all(abs(p["100.0"]["expected"] - p["60.0"]["expected"]) < 1e-9 for e in EIS for p in PREF[e])
USED0 = [p["0.0"]["used"] for e in EIS for p in PREF[e]]
PER_POINT = {e: [0.5 * (an(case(n, e))["per_point"][1] + an(case(n, e))["per_point"][4]) for n in NS] for e in EIS}
BR0 = {e: case("0", e)["bridge"] for e in EIS}
for e in EIS:
    assert abs(sum(BR0[e].values()) - best(case("0", e))["expected"]) < 1e-3
PROFIT = {e: BR0[e]["nb_profit_vs_sq"] + BR0[e]["supply_demand"] for e in EIS}
COST = {e: -(BR0[e]["programme_investment"] + BR0[e]["debt_penalty"]) for e in EIS}
DEM = {n: dict(zip(PG["years"], PG["retire_later"][n]["demand"])) for n in NS}
SUM3860 = {n: sum(DEM[n][y] for y in range(2038, 2061)) for n in NS}
PEAK = {n: max(range(2038, 2061), key=lambda y: DEM[n][y]) for n in NS}
GD = dict(zip(GAME["years"], GAME["total"]))
GREP = dict(zip(GAME["years"], GAME["replacements"]))
PRE = {n: sum(DEM[n][y] for y in range(2026, 2038)) for n in NS}
GAME_PRE = sum(GD[y] for y in range(2026, 2038))
TWICE = {n: sum(GREP[y] for y in range(2026, 2038)) - sum(DEM[n][y] / 2.0 for y in range(2026, 2038)) for n in NS}
FIRM_LEFT = D["firm_left_2038"]["page_from_2026"]
# launch year: the margin needed for each date by programme length (7 and 10 years: the game's bills; 8 and 9: interpolated)
MBY = {e: [an(case(n, e))["margin_by_years"] for n in NS] for e in EIS}
LAUNCH = {}                                  # launch year -> {eis: (years, [margin by N])}
for e in EIS:
    for yrs in (10, 9, 8, 7):
        LAUNCH.setdefault(e - yrs, {})[e] = (yrs, [m[str(yrs)] for m in MBY[e]])
STEP = [m[str(k - 1)] - m[str(k)] for e in EIS for m in MBY[e] for k in (10, 9, 8)]      # one year later, same date
TIE = [max(abs(a - b) for a, b in zip(LAUNCH[y][2039][1], LAUNCH[y][2041][1])) for y in (2031, 2032)]
assert max(TIE) < 0.006, TIE
TIE_39_LESS = sum(a < b for y in (2031, 2032) for a, b in zip(LAUNCH[y][2039][1], LAUNCH[y][2041][1]))
assert TIE_39_LESS == 8, TIE_39_LESS          # 2039 needs less in four of five timings at each launch year
# the same bills spent over the development years (the game's cash phasing) instead of booked at entry into service
MBYP = {e: [an(case(n, e))["margin_by_years_phased"] for n in NS] for e in EIS}
LAUNCH_P = {}
for e in EIS:
    for yrs in (10, 9, 8, 7):
        LAUNCH_P.setdefault(e - yrs, {})[e] = (yrs, [m[str(yrs)] for m in MBYP[e]])
STEP_P = [m[str(k)] - m[str(k - 1)] for e in EIS for m in MBYP[e] for k in (10, 9, 8)]   # one year later, same date: a saving
assert min(STEP_P) > 0
for y in LAUNCH:                               # robust on both bookings: at the same launch year the earliest date needs the least
    if len(LAUNCH[y]) > 1:
        e0 = min(LAUNCH[y])
        for others in [e for e in LAUNCH[y] if e != e0]:
            assert all(a < b for a, b in zip(LAUNCH_P[y][e0][1], LAUNCH_P[y][others][1])), (y, e0, others)
            assert all(a < b for a, b in zip(LAUNCH[y][e0][1], LAUNCH[y][others][1])) or y in (2031, 2032), (y, e0, others)
for yrs in (10, 9, 8, 7):                      # robust on both bookings: at the same programme length the earlier date needs less
    for book in (MBY, MBYP):
        for i in range(len(NS)):
            v = [book[e][i][str(yrs)] for e in EIS]
            assert v[0] < v[1] < v[2], (yrs, v)
LEVEL = [MBYP[e][i][k] - MBY[e][i][k] for e in EIS for i in range(len(NS)) for k in ("10", "9", "8", "7")]
assert all(a < b for a, b in zip(LAUNCH[2034][2041][1], LAUNCH[2034][2044][1]))
assert all(case(n, 2039)["margin_needed"] < x for n in NS for y in LAUNCH for e, (k, v) in LAUNCH[y].items() if (y, e) != (2029, 2039)
           for x in [v[NS.index(n)]])
MATCH = {e: {k: [case(n, e)["pref_to_match"][k] for n in NS] for k in ("10", "9")} for e in (2041, 2044)}
SW_LEAD = [sorted(SWX[e][i] for e in EIS)[-1] - sorted(SWX[e][i] for e in EIS)[-2] for i in range(len(NS))]
MOVE = {e: max(case(n, e)["margin_needed"] for n in NS) - min(case(n, e)["margin_needed"] for n in NS) for e in EIS}
MOVE_SW = {e: max(sw(n, e)["margin_needed"] for n in NS) - min(sw(n, e)["margin_needed"] for n in NS) for e in EIS}
assert LEAST_BRIEF["1"] == 2039
PREF_ORDER = [max(EIS, key=lambda e: PREFMAX[e][i]) for i in range(len(NS))]
assert all(x == 2044 for x in PREF_ORDER)
ALONE_MAX30 = min(min(case(n, e)["margin_needed"] for n in NS) for e in EIS)
assert ALONE_MAX30 > 0.30


def pts(v):
    """A margin difference in percentage points."""
    return f"{K.rnd(v * 100, 1):.1f}"


def nw(x):
    return f'<span class="nw">{x}</span>'


# ─────────────────────────────── charts ───────────────────────────────
def end_offsets(vals, sy, gap=20):
    """dy for each end label so that labels sit at least `gap` px apart (order kept by value)."""
    order = sorted(range(len(vals)), key=lambda i: sy(vals[i]))
    groups = []                                  # clusters of labels closer than `gap`, each centred on its points
    for i in order:
        if groups and sy(vals[i]) - groups[-1][-1][1] < gap:
            groups[-1].append((i, sy(vals[i])))
        else:
            groups.append([(i, sy(vals[i]))])
    pos = {}
    for g in groups:
        mid = sum(y for _, y in g) / len(g)
        start = mid - gap * (len(g) - 1) / 2
        for k, (i, y) in enumerate(g):
            pos[i] = start + gap * k - y
    return [pos[i] for i in range(len(vals))]


def chart_demand():
    x_lo, x_hi, y_lo, y_hi = 2028, 2065, 0, 2600
    series = [("Game's conservative curve", "faint", [(y, GD[y]) for y in range(2030, x_hi + 1)])]
    for n in NS:
        series.append((f"Retiring {NLAB[n].lower()}" if n != "0" else "Retiring as chapter 1 sets out", f"d{n}",
                       [(y, DEM[n][y]) for y in range(2038, x_hi + 1)]))
    h, top, bot = 346, 26, 46
    sy = lambda v: top + (y_hi - v) / (y_hi - y_lo) * (h - top - bot)
    dys = end_offsets([s[2][-1][1] for s in series], sy)
    labels = ["Game's curve"] + [("+%s yr" % n if n == "1" else "+%s yrs" % n) if n != "0" else "As set out" for n in NS]
    return K.line_chart(series, y_lo, y_hi, 500, "int", "Single-aisle aircraft a year, whole market (A220 included)", [],
                        "Single-aisle demand on the user's page for five retirement timings, 2038-2065, and the game's conservative curve",
                        list(zip(dys, labels)), [], x_lo=x_lo, x_hi=x_hi)


def dot_chart(rows, x_lo, x_hi, step, fmt, refs, label, aria):
    """rows: [(label, {eis: (value, tip rows)})]; a dot per date on one line per row."""
    w, left, right, top, rh = 760, 190, 24, 30, 34
    h = top + rh * len(rows) + 40
    sx = lambda v: left + (v - x_lo) / (x_hi - x_lo) * (w - left - right)
    out = [K.svg_open(w, h, aria)]
    t = x_lo
    while t <= x_hi + 1e-9:
        out.append(f'<line x1="{sx(t):.1f}" x2="{sx(t):.1f}" y1="{top - 6}" y2="{top + rh * len(rows)}" class="grid"/>'
                   f'<text x="{sx(t):.1f}" y="{top + rh * len(rows) + 16}" text-anchor="middle" class="tick">{fmt(t)}</text>')
        t += step
    for v, txt in refs:
        out.append(f'<line x1="{sx(v):.1f}" x2="{sx(v):.1f}" y1="{top - 14}" y2="{top + rh * len(rows)}" class="ref"/>'
                   f'<text x="{sx(v) + 5:.1f}" y="{top - 16}" class="reflab">{esc(txt)}</text>')
    for i, (lab, pts) in enumerate(rows):
        y = top + rh * i + rh / 2
        out.append(f'<text x="{left - 12}" y="{y + 4:.1f}" text-anchor="end" class="rowlab sm">{esc(lab)}</text>')
        xs = [sx(v) for v, _ in pts.values()]
        out.append(f'<line x1="{min(xs):.1f}" x2="{max(xs):.1f}" y1="{y:.1f}" y2="{y:.1f}" class="conn"/>')
        for e, (v, tip) in pts.items():
            out.append(f'<circle cx="{sx(v):.1f}" cy="{y:.1f}" r="6" fill="var(--{COL[e]})" class="ring" {K.mark_attrs(*tip)}/>')
    out.append(f'<text x="{left}" y="{h - 4}" class="tick">{esc(label)}</text></svg>')
    return "".join(out)


def legend_dates():
    return '<div class="legend">' + "".join(f'<span><i class="sq" style="background:var(--{COL[e]});border-radius:50%"></i>fps in service {e}</span>' for e in EIS) + "</div>"


def chart_margin():
    rows = []
    for n in NS:
        pts = {}
        for e in EIS:
            c = case(n, e)
            pts[e] = (c["margin_needed"], [(pc(c["margin_needed"]), f"fps margin needed, in service {e}", f"var(--{COL[e]})"),
                                            ("", f"retiring {NLAB[n].lower()}; today {pc(M0, 2)}", None)])
        rows.append((NLAB[n], pts))
    return dot_chart(rows, 0.24, 0.42, 0.02, lambda v: f"{v * 100:.0f}%", [(M0, "fps margin today, 25.64%")],
                     "fps operating margin needed to pass all three of Boeing's tests (better site)",
                     "fps margin needed to pass Boeing's tests, by retirement timing and entry into service")


def chart_value():
    rows = []
    for n in NS:
        pts = {}
        for e in EIS:
            c = case(n, e)
            x = best(c)
            pts[e] = (x["expected"], [(bp(x["expected"]), f"fps against Do Nothing, expected case, in service {e}", f"var(--{COL[e]})"),
                                      ("", f"retiring {NLAB[n].lower()}; {SITE[c['eval']['best']]}", None)])
        rows.append((NLAB[n], pts))
    return dot_chart(rows, -4.8, -4.1, 0.1, lambda v: (MINUS if v < 0 else "") + f"${abs(v):.1f}B", [],
                     "fps against Do Nothing in Boeing's expected case, $B PV at 2026 (better site)",
                     "Value of the fps against Do Nothing by retirement timing and entry into service")


# ─────────────────────────────── other tables ───────────────────────────────
def worlds_table():
    def cell(w, e):
        xs = [case(n, e)["worlds"][w]["expected"] for n in NS]
        return rng(xs, bp)
    head = ["If the world were different (not Boeing's levers)"] + [f"In service {e}" for e in EIS]
    rows = [["Boeing loses 3 points a year while NGSA flies alone (instead of 1)"] + [cell("erosion3", e) for e in EIS],
            ["NGSA enters service in 2040, 3 years late"] + [cell("ngsa2040", e) for e in EIS]]
    return K.table(head, rows, num_cols=(1, 2, 3))


def demand_table():
    head = ["Retirement", "2038", "2041", "2044", "2050", "2055", "2060", "Total 2038-60", "Peak year"]
    rows = [[esc(NLAB[n])] + [n0(DEM[n][y]) for y in (2038, 2041, 2044, 2050, 2055, 2060)] + [n0(SUM3860[n]), str(PEAK[n])] for n in NS]
    rows.append(['<span class="muted">Game\'s conservative curve</span>'] +
                [f'<span class="muted">{n0(GD[y])}</span>' for y in (2038, 2041, 2044, 2050, 2055, 2060)] +
                [f'<span class="muted">{n0(sum(GD[y] for y in range(2038, 2061)))}</span>', '<span class="muted">—</span>'])
    return K.table(head, rows, num_cols=tuple(range(1, 9)))


def tview_demand():
    ys = list(range(2038, 2066))
    head = ["Year"] + [NLAB[n] for n in NS] + ["Game's curve"]
    rows = [[str(y)] + [n0(DEM[n][y]) for n in NS] + [n0(GD[y])] for y in ys]
    return K.tview("demand by year", head, rows)


def quotes():
    return '<div class="dcards">' + "".join(
        f'<div class="panel dcard"><p class="label">{esc(s)}</p><p>{esc(q)}</p><p class="muted small"><b>For this page:</b> {esc(m)}</p></div>'
        for s, q, m in QUOTES) + "</div>"


EXTRA_CSS = """
:root { --d0: #9dc0ea; --d1: #6fa2e0; --d2: #2a78d6; --d3: #1c5aa6; --d4: #123e76; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --d0: #2d5c99; --d1: #3a76c4; --d2: #3987e5; --d3: #78aef0; --d4: #b4d2f7; } }
:root[data-theme="dark"] { --d0: #2d5c99; --d1: #3a76c4; --d2: #3987e5; --d3: #78aef0; --d4: #b4d2f7; }
ul.cav li, footer { overflow-wrap: anywhere; }
.lev tbody th { min-width: 17rem; } .lev td.n { white-space: normal; }
@media (max-width: 760px) { .lev tbody th { min-width: 11rem; } }
"""


# ─────────────────────────────── tables ───────────────────────────────
def matrix_table():
    head = ["Retirement"] + [f"In service {e}" for e in EIS]
    rows = []
    for n in NS:
        r = [esc(NLAB[n])]
        for e in EIS:
            x = best(case(n, e))
            r.append(f'{b(x["expected"])}<br><span class="muted small">worst {bp(x["worst"])} · risk {bp(x["risk_case"])}</span>'
                     f'<br><span class="muted small">same years {bp(sbest(sw(n, e))["expected"])}</span>')
        rows.append(r)
    g = D["game_curve"]
    rows.append(['<span class="muted">Game\'s own curve (reference)</span>'] +
                [f'<span class="muted">{b(g[str(e)][g[str(e)]["best"]]["expected"])}</span>' for e in EIS])
    return K.table(head, rows, num_cols=(1, 2, 3))


def ramp_txt(c):
    k = c["ramp_needed"]
    if not k:
        return '<span class="muted">over 12×</span>'
    t = c["ramp_profiles"]["needed"]["to_90"]
    return f"{k:.1f}×<br><span class=\"muted small\">90/mo by year {t}</span>"


def floor_pc(v):
    """A maximum, rounded down: one decimal under 10%, whole points above."""
    import math
    return f"{math.floor(v * 1000) / 10:.1f}%" if v < 0.1 else f"{math.floor(v * 100):.0f}%"


def partner_txt(x):
    if not x["passes_free"]:
        return f'{pc(x["margin_free"])}<br><span class="muted small">margin needed; fails at the current margin even free</span>'
    return f'passes<br><span class="muted small">if it takes back ≤{floor_pc(x["max_profit_share"])} of fps profit</span>'


def levers_table(e):
    head = ["What changes", "Today"] + [NLAB[n] for n in NS]
    cs = [case(n, e) for n in NS]
    def row(lab, today, vals):
        return [lab, today] + vals
    rows = [
        row("<b>fps margin</b> (alone)", pc(M0, 2), [pc(c["margin_needed"]) for c in cs]),
        row("<b>fps price</b> (alone; today's cost of $%.1fM an aircraft held)" % COST0, f"${P0:.0f}M", [f"${c['price_cost_held']:.1f}M" for c in cs]),
        row("<b>Development bill</b> (alone)", f"${B0:.1f}B", [f"${c['bill_needed']:.1f}B" for c in cs]),
        row("<b>Ramp-up speed</b> (alone)", f"1×<br><span class=\"muted small\">90/mo by year {GAME_TO90}</span>", [ramp_txt(c) for c in cs]),
        row("<b>Customer preference</b> (alone): best it can do", "—",
            [f'{bp(c["pref_sweep"]["100.0"]["expected"])}<br><span class="muted small">never passes</span>' for c in cs]),
        row("A partner pays 25% of the bill: the most fps profit it can take back (or, if it fails even free, the margin needed)", pc(M0, 2),
            [partner_txt(an(c)["partner"]["0.25"]) for c in cs]),
        row("A partner pays 50% of the bill: the most fps profit it can take back (or the margin needed)", pc(M0, 2),
            [partner_txt(an(c)["partner"]["0.5"]) for c in cs]),
        row("A partner pays 25% and takes 25% of fps profit: margin needed", pc(M0, 2), [pc(an(c)["partner"]["0.25"]["margin_fair"]) for c in cs]),
        row("1.5× ramp (90/mo by year %d): margin needed" % case("0", e)["ramp_profiles"]["x1.5"]["to_90"], pc(M0, 2),
            [pc(c["ramp15"]["margin_needed"]) for c in cs]),
        row("1.5× ramp and a partner paying 25%: the most fps profit it can take back (or the margin needed)", pc(M0, 2), [partner_txt(c["package"]) for c in cs]),
        row("Customers preferring the fps by 10 more points: margin needed", pc(M0, 2),
            [pc(c["pref10_margin"]) + ('' if c["pref10_site"] == "renton" else '<br><span class="muted small">at new sites</span>') for c in cs]),
    ]
    if e == 2039:
        rows += [row("A 9-year programme from 2030 (bill $%.1fB, interpolated): margin needed" % BILL9, pc(M0, 2), [pc(c["margin_bill9"]) for c in cs]),
                 row("The game's 7-year fps launched in 2032 (bill $%.1fB): margin needed" % BILL7, pc(M0, 2), [pc(c["margin_bill7"]) for c in cs])]
    return '<div class="lev">' + K.table(head, rows, num_cols=tuple(range(1, 2 + len(NS)))) + "</div>"


def launch_table():
    head = ["Launch in", "In service 2039", "In service 2041", "In service 2044"]
    rows = []
    for y in sorted(LAUNCH):
        r = [str(y)]
        lows = {e: min(v) for e, (k, v) in LAUNCH[y].items()}
        for e in EIS:
            if e not in LAUNCH[y]:
                r.append('<span class="muted">—</span>')
                continue
            k, v = LAUNCH[y][e]
            vp = LAUNCH_P[y][e][1]
            bill = {10: B0, 9: BILL9, 8: BASE["bill9"] + (BILL7 - BILL9) / 2, 7: BILL7}[k]
            cell = (f'{rng(v, pc)}<br><span class="muted small">spent over development: {rng(vp, pc)}</span>'
                    f'<br><span class="muted small">{k}-year programme, ${bill:.1f}B{"" if k in (7, 10) else " (interpolated)"}</span>')
            if len(lows) > 1 and lows[e] == min(lows.values()):
                cell = f"<b>{cell}</b>"
            r.append(cell)
        rows.append(r)
    return K.table(head, rows, num_cols=(1, 2, 3))


LINE_LAB = {"nb_profit_vs_sq": "Boeing narrowbody profit (fps and 737) on the dashboard's own market: 2,000 a year, every sale built",
            "supply_demand": "Real factories and your demand (the supply and demand layer)",
            "programme_investment": "Development bill, booked at entry into service",
            "debt_penalty": "Debt penalty on the bill",
            "supply_plan": "Renton saving (new-site capex avoided)"}


def bridge_table():
    head = ["Line, expected case, retiring as chapter 1 sets out"] + [f"In service {e}" for e in EIS]
    rows = []
    for k, lab in LINE_LAB.items():
        rows.append([esc(lab)] + [b(BR0[e].get(k, 0.0)) for e in EIS])
    other = {e: sum(v for k, v in BR0[e].items() if k not in LINE_LAB) for e in EIS}
    if any(abs(v) > 5e-3 for v in other.values()):
        rows.append(["Other lines"] + [b(other[e]) for e in EIS])
    rows.append(["<b>fps against Do Nothing</b>"] + [f"<b>{b(sum(BR0[e].values()))}</b>" for e in EIS])
    rows.append(['<span class="muted">Value of one more point of fps margin</span>'] +
                [f'<span class="muted">{bp(PER_POINT[e][0])}</span>' for e in EIS])
    return K.table(head, rows, num_cols=(1, 2, 3))


def sens_table():
    def cell(xs):
        ex = [sbest(x)["expected"] for x in xs]
        mg = [x["margin_needed"] for x in xs]
        bl = [x["bill_needed"] for x in xs]
        return (f'{rng(ex, bp)}<br><span class="muted small">margin {rng(mg, pc)}</span>'
                f'<br><span class="muted small">bill {rng(bl, lambda v: f"${K.rnd(v, 1):.1f}B")}</span>')
    head = ["World (range over the five retirement timings)"] + [f"In service {e}" for e in EIS]
    rows = [["<b>Main case</b>: your demand from 2038, the game's supply, the brief's counting"] + [cell([case(n, e) for n in NS]) for e in EIS],
            ["Do Nothing counted over the same years as each fps (2026 to entry into service + 19)"] + [cell([sw(n, e) for n in NS]) for e in EIS],
            ["Your page's own demand from 2026 (no splice)"] + [cell([sens("page_from_2026", n, e) for n in NS]) for e in EIS],
            ["Your demand's tail after 2055 replaced by the game's curve"] + [cell([sens("tail", n, e) for n in NS]) for e in EIS],
            ["Tianjin building 20 a month on top of Airbus's plan, 2035-2050"] + [cell([sens("tianjin", n, e) for n in NS]) for e in EIS],
            ["Your page's supply: 737 at 52 a month, then down to none by end-2050; fps to 80 a month in 7 years; Tianjin on"] +
            [cell([sens("page_supply", n, e) for n in NS]) for e in EIS]]
    return K.table(head, rows, num_cols=(1, 2, 3))


def tview_dots():
    head = ["Retirement"] + [f"{e}: value" for e in EIS] + [f"{e}: margin needed" for e in EIS]
    rows = [[esc(NLAB[n])] + [bp(best(case(n, e))["expected"]) for e in EIS] + [pc(case(n, e)["margin_needed"]) for e in EIS] for n in NS]
    return K.tview("both charts", head, rows)


QUOTES = [
    ("Q2 2026 earnings call, 28 Jul 2026 (Kelly Ortberg)",
     "“The actual share of the overall aerospace profitability is kind of embedded in the supply chain architecture, and we're "
     "not going to change that on the existing airplanes. … So it points to the next airplane as the opportunity to change that.” "
     "It “could require a little more vertical integration. I don't think a massive amount. I think it could require different kind "
     "of business partnerships, different type of ventures, certainly a different level of engagement with our supply chain "
     "depending on the commodity.”",
     "The margin lever: taking more of the value chain's profit on the next airplane. If such partners also carried part of the "
     "development cost, that would be the bill lever; management did not say so."),
    ("Q3 2026 earnings call, 27 Oct 2026 (Kelly Ortberg, Jesus Malave)",
     "“Nothing has changed on our outlook on new airplane. We've got a team working in our product development right now, trying "
     "to define what that … looks like and what the market timing is.” Investment is “contemplated in our cash outlook”, mostly "
     "“R&D tech development”; after the 777X, “a shift of resources and spending from those development programs to new programs.”",
     "No launch is planned yet. A 10-year programme launched in 2031 or 2034 enters service in 2041 or 2044; the game's 7-year fps "
     "launched in 2032 enters service in 2039."),
    ("Company conference, 17 Mar 2026 (Jesus Malave)",
     "“There will be a day where we have to enter into a new program. That day is not today, and it's not any time near.” Three "
     "conditions: the market, the technology and The Boeing Company must be ready.",
     "Our reading: whenever Boeing launches, the earliest date it can then reach is the best target; 2039 needs a launch by about 2032."),
    ("Q3 2026 call and May 2026 conference (Ortberg, Malave)",
     "Rate 52 “in the back half of 2027”, and “it's more important that we do this ramp right than what particular month we achieve "
     "a rate break”; deliveries in 2029 give “runway to deliver at a rate 63”; “we'd like to get some day to 63 a month rate.”",
     "The ramp lever needs a factory that fills the fps line fast (for 2039, 90 a month by year 3 or 4 after entry into service, against "
     "year 7 on the game's ramp). Management wants more capacity but at a disciplined pace, so these remarks do not support a faster "
     "ramp. In the game the 737 stays at 57 a month from 2030 (Boeing did not order the rate increase)."),
]


def tiles():
    t = [("Which date", "2039, if Boeing can launch by about 2032",
          "At the same bill it needs the smallest margin, price, bill and ramp change in every timing; 2044 the most. At the same launch "
          "year, the earliest date Boeing can reach needs about the same or less, however the bill is booked."),
         ("fps against Do Nothing", f"{nw(bp(LO_EXP))} to {nw(bp(HI_EXP))}",
          f"Boeing's expected case, all 15 combinations; none passes, all at least {bp(GAP_ALL, 2, False)} short of the Board's +$1B. "
          f"Launched as they stand, the dates are within {bp(SPREAD, 2, False)} as Boeing's brief counts them; counted over the same years, 2044 loses least "
          f"(by {rng(SW_LEAD, lambda v: bp(v, 2, False))} over the next date)."),
         ("Margin needed (alone)", " ".join(nw(rng([case(n, e)["margin_needed"] for n in NS], pc).replace(" to ", "–") + (" ·" if e != EIS[-1] else "")) for e in EIS),
          f"For 2039 · 2041 · 2044, against {pc(M0, 2)} today (${UNIT_FPS:.1f}M of profit an aircraft)."),
         ("Bill needed (alone)", " ".join(nw(rng([case(n, e)["bill_needed"] for n in NS], lambda v: f"${K.rnd(v, 1):.1f}B").replace(" to ", "–") + (" ·" if e != EIS[-1] else "")) for e in EIS),
          f"For 2039 · 2041 · 2044, against ${B0:.1f}B today. A partner paying a quarter works only for 2039, and only if it takes back at most "
          f"{rng([x['max_profit_share'] for x in PT[2039]['0.25']], floor_pc)} of the profit; one paying half can take back up to "
          f"{rng([x['max_profit_share'] for x in PT[2039]['0.5']], floor_pc)} (2039), {rng([x['max_profit_share'] for x in PT[2041]['0.5']], floor_pc)} (2041) "
          f"or {rng([x['max_profit_share'] for x in PT[2044]['0.5']], floor_pc)} (2044).")]
    return '<div class="tiles">' + "".join(f'<div class="panel tile"><div class="k">{esc(k)}</div><div class="v">{v if "<" in v else esc(v)}</div><div class="d">{esc(d)}</div></div>' for k, v, d in t) + "</div>"


def build(out_path):
    css = K.CSS + EXTRA_CSS
    r39 = [case(n, 2039)["ramp_needed"] for n in NS]
    m39_p = [case(n, 2039)["pref10_margin"] for n in NS]
    pk44_short = [x["margin_free"] for n, x in zip(NS, PKG[2044]) if not x["passes_free"]]
    answers = [
        ("Which date is more advantageous for Boeing: 2039.",
         f" None makes the fps pay on your demand: in Boeing's expected case it is worth {bp(LO_EXP)} to {bp(HI_EXP)} against Do Nothing in every "
         f"combination, at least {bp(GAP_ALL, 2, False)} short of the Board's +$1B. Launched as they stand, the dates lose about the same: within "
         f"{bp(SPREAD, 2, False)} as Boeing's brief counts them, and counted over the same years 2044 loses least by "
         f"{rng(SW_LEAD, lambda v: bp(v, 2, False))}. But a date is only worth aiming for if it can become a launch, and there "
         f"<strong>2039 needs the least</strong>: at the same bill, a {mrange(2039)} margin against {mrange(2041)} for 2041 and {mrange(2044)} for 2044, or a "
         f"bill of {brange(2039)} against {brange(2041)} and {brange(2044)}, in all five timings, under both countings and in every sensitivity. "
         f"The catch is timing. 2039 at the 10-year bill means launching in 2029; launched in 2030 (a 9-year programme) it needs "
         f"{rng([case(n, 2039)['margin_bill9'] for n in NS], pc)}, and as the game's 7-year fps launched in 2032 {rng([case(n, 2039)['margin_bill7'] for n in NS], pc)}. "
         f"At the same launch year, the earliest date Boeing can reach needs about the same or less: for a launch in 2031 or 2032, 2039 and 2041 "
         f"are within about half a point as the brief books the bill (2039 slightly less in four of five timings), and 2039 needs clearly less if "
         f"the bill is spent over the development years; for a launch in 2034, 2041 beats 2044 either way. So: <strong>the earliest date Boeing can "
         f"commit to, which is 2039 for a launch by about 2032; 2044 is the hardest to make work.</strong>"),
        ("Why the later dates need more.",
         f" The game counts each fps for 20 years from entry into service, discounted at 10.5%. A later fps sells its aircraft later, so each point "
         f"of margin is worth less at 2026: one more point is worth {bp(PER_POINT[2039][0], 2, False)} for 2039 and {bp(PER_POINT[2044][0], 2, False)} for 2044 "
         f"(aircraft retiring as chapter 1 sets out). The fps's profit against Do Nothing falls from {bp(PROFIT[2039], 1, False)} to "
         f"{bp(PROFIT[2044], 1, False)}, while the bill and its debt penalty fall from {bp(COST[2039], 1, False)} to {bp(COST[2044], 1, False)}: about the same "
         f"amount, which is why the losses look alike. A later fps also waits longer behind NGSA (in service 2037) while Boeing's preference erodes, "
         f"and an fps in 2044 is counted to 2063, into the years when your demand falls back."),
        ("The retirement timing matters little to the ranking.",
         f" Every timing gives about the same demand over 2038-2060 ({n0(min(SUM3860.values()))} to {n0(max(SUM3860.values()))} aircraft); "
         f"later retirement moves the peak from {PEAK['0']} to {PEAK['4']}. That moves the fps by at most "
         f"{bp(max(max(EXP[e]) - min(EXP[e]) for e in EIS), 2, False)} and the margin needed by {pts(MOVE[2039])} points for 2039, {pts(MOVE[2041])} for 2041 "
         f"and {pts(MOVE[2044])} for 2044 ({pts(MOVE_SW[2044])} counted over the same years): small for 2039, real for 2044. Which date loses least as "
         f"launched is not a robust result: it depends on how Do Nothing is counted and on the demand assumed before 2038. Which date needs the "
         f"least to become a launch does not."),
        ("How Boeing could make each date a launch.",
         f" <strong>2039:</strong> any one of a {mrange(2039)} margin ({rng([P0 * case(n, 2039)['margin_needed'] for n in NS], lambda v: f'${K.rnd(v, 1):.1f}M')} of profit "
         f"an aircraft instead of ${UNIT_FPS:.1f}M; at today's cost per aircraft, a price of about ${K.rnd(min(case(n, 2039)['price_cost_held'] for n in NS), 0):.0f}M), a bill of "
         f"{brange(2039)}, or a ramp {min(r39):.1f} to {max(r39):.1f} times as fast (90 a month by year {rng(TO90[2039], str)} after entry into service instead of "
         f"year {GAME_TO90}). A partner paying a quarter of the bill is enough only if it takes back at most "
         f"{rng([x['max_profit_share'] for x in PT[2039]['0.25']], floor_pc)} of the fps's profit; one paying half can take up to "
         f"{rng([x['max_profit_share'] for x in PT[2039]['0.5']], floor_pc)}. Customers preferring the fps by 10 more points cut the margin "
         f"needed to {rng(m39_p, pc)}. <strong>2041:</strong> a {mrange(2041)} margin or a {brange(2041)} bill; a 1.5× ramp plus a partner paying a quarter "
         f"(taking back at most {rng([x['max_profit_share'] for x in PKG[2041]], floor_pc)} of the profit) passes. <strong>2044:</strong> a "
         f"{mrange(2044)} margin or a {brange(2044)} bill; a 1.5× ramp plus a free quarter of the bill passes only if aircraft retire 2-4 years later, and "
         f"otherwise still needs {rng(pk44_short, pc)}. A faster ramp alone would have to be near-instant. More customer preference "
         f"helps every date but makes none a launch on its own; it is the one lever on which 2044 comes closest."),
        ("A caveat: the same aircraft at every date.",
         f" Only the entry into service moves; the aircraft, its price, margin and appeal do not. A later fps could be a better aircraft (management's "
         f"'technology has to be ready'). 2039's lead is thin: if two more years made the 2041 fps preferred by "
         f"{rng(MATCH[2041]['9'], lambda v: f'{K.rnd(v, 1):.1f}')} more points of customer preference, it would need no more margin than a 2039 fps launched in 2030 "
         f"({rng(MATCH[2041]['10'], lambda v: f'{K.rnd(v, 1):.1f}')} points to match 2039 at the 10-year bill). 2044 would need "
         f"{rng(MATCH[2044]['9'], lambda v: f'{K.rnd(v, 0):.0f}')} points ({rng(MATCH[2044]['10'], lambda v: f'{K.rnd(v, 0):.0f}')} to match 2039 at the 10-year bill). If the later aircraft would be that much better, "
         f"waiting can pay; if not, earlier is better."),
    ]
    panels = '<div class="bl">' + "".join(f'<div class="panel"><div><b>{esc(t)}</b>{x}</div></div>' for t, x in answers) + "</div>"
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>fps Date and Demand</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{css}</style></head><body><div class="wrap">
<header class="top"><p class="eyebrow">Boeing Product Development · conservative-case war game (dash-2050-cons) · BOEING PROPRIETARY</p>
<h1>fps in 2039, 2041 or 2044 on your replacement demand</h1>
<p class="lede">The demand of your page "Single-Aisle Replacement Story" (chart 4.1: today's fleet replaced, plus as much
again for growth), with every aircraft retiring as chapter 1 sets out or 1-4 years later, run against an fps entering service in 2039, 2041 or
2044. Each fps is valued exactly as Boeing's 2030 brief values it, in all six rival cases, at the better site, and held to Boeing's
three tests. Then we ask what would make each one a launch.</p>
<nav class="toc"><a href="#answers">Summary</a><a href="#demand">Demand scenarios</a><a href="#which">Which date</a><a href="#why">Why</a><a href="#launch">Making it a launch</a><a href="#said">What Boeing has said</a><a href="#sens">Sensitivities</a><a href="#notes">Notes</a></nav></header>

<section id="answers" style="margin-top:22px">{tiles()}{panels}</section>

<section id="demand"><h2>Demand scenarios</h2><p class="lede">Your page draws demand from 2038 ("before then half and half
understates it"), so each scenario uses the game's conservative curve to 2037 and your page from 2038. The game then takes the
737/A320 class share ({D_CLASS}) as it does for its own curve. Two costs of that splice: every timing has the same demand before 2038
(the game's {n0(GAME_PRE)} aircraft over 2026-2037, against your page's {n0(PRE['0'])} as chapter 1 sets out down to {n0(PRE['4'])} four years later),
and the game's early replacements are not taken off your page's later ones, so about {n0(min(TWICE.values()))} to {n0(max(TWICE.values()))} of today's
fleet are counted twice. A sensitivity below uses your page's own demand from 2026 instead; it does not change which date needs the least.</p><div class="stack">
<div class="panel"><p class="ctitle">Retiring later moves the peak from {PEAK["0"]} to {PEAK["4"]}; 2038-2060 totals are within {n0(max(SUM3860.values()) - min(SUM3860.values()))} aircraft of each other</p>
<div class="legend"><span><i class="ln" style="background:var(--faint)"></i>Game's conservative curve</span>{"".join(f'<span><i class="ln" style="background:var(--d{n})"></i>{esc(NLAB[n])}</span>' for n in NS)}</div>
<div class="cw" data-focus="300">{chart_demand()}</div>{tview_demand()}
<p class="cap">Whole single-aisle market (A220 included), before the class share; the game's curve is the faint line. Your chart 4.1 draws 2038-2050;
the years after 2050 come from the same data on your page (its later-retirement series), which the chart does not draw. The game counts an fps
for 20 years from entry into service: 2039-2058, 2041-2060 or 2044-2063. Your curve falls after 2055 because it counts only today's fleet,
so a sensitivity below hands that tail back to the game's curve.</p></div>
<div class="panel"><p class="label">Aircraft a year on your page</p>{demand_table()}</div>
</div></section>

<section id="which"><h2>Which date is better for Boeing</h2><p class="lede">Launched as they stand, every date loses about the
same, {bp(LO_EXP)} to {bp(HI_EXP)} against Do Nothing in Boeing's expected case. Which loses least is not robust. Boeing's brief counts
Do Nothing to 2060 whatever the fps date; on that count 2039 loses least when aircraft retire as chapter 1 sets out or 1 year later (a near-tie at
1 year) and 2044 when they retire 2-4 years later. Counted over the same years as each fps (2026 to its entry into service + 19), or with your page's
own demand before 2038, 2044 loses least in every timing. Turning the fps into a launch is another matter: at the same bill, 2039 needs the least
margin, price or bill change in every timing and on both counts (and the least ramp change as the brief counts it), 2044 by far the most.
Preference is the exception (below). And at the same launch year, the earliest date Boeing can reach needs about the same or less: see the table.</p><div class="stack">
{legend_dates()}
<div class="panel"><p class="ctitle">2039 needs a {mrange(2039)} margin to become a launch; 2044 needs {mrange(2044)}</p><div class="cw" data-focus="560">{chart_margin()}</div></div>
<div class="panel"><p class="ctitle">As they stand, all 15 lose {bp(-HI_EXP, 2, False)} to {bp(-LO_EXP, 2, False)} against Do Nothing, at least {bp(GAP_ALL, 2, False)} short of the Board's +$1B</p><div class="cw" data-focus="460">{chart_value()}</div>
<p class="cap">Zoomed axis, Boeing's brief counting: the dates differ by at most {bp(SPREAD, 2, False)} in any timing. Do Nothing is at $0 and the Board's line at +$1B, far to the right.</p></div>
{tview_dots()}
<div class="panel"><p class="ctitle">At the same launch year, the earliest date Boeing can reach needs about the same margin or less, however the bill is booked</p><div class="lev">{launch_table()}</div>
<p class="cap">Margin needed alone, better site, range over the five timings; bold: the least for that launch year as the brief books the bill. The game has
a 10-year fps (${B0:.2f}B) and a 7-year fps (${BILL7:.1f}B); the 8- and 9-year bills are straight-line between them (our assumption). Boeing's brief books
the whole bill at entry into service, so for a given date a shorter programme (a later launch) needs about {pts(min(STEP))} to {pts(max(STEP))} more points of
margin a year, only because its bill is bigger. Spent over the development years on the game's cash phasing curve, the same bills go out earlier and cost
more today, so every figure is {pts(min(LEVEL))} to {pts(max(LEVEL))} points higher, and within a column the order reverses: a later, shorter programme saves
{pts(min(STEP_P))} to {pts(max(STEP_P))} points a year because its money goes out later. What holds on both bookings is the comparison across a row: in 2031 and
2032 the 2039 and 2041 routes are within about half a point as the brief books it (2039 slightly less in four of five timings) and 2039 needs clearly less when
spent over the development years; in 2034, 2041 beats 2044 either way.</p></div>
<div class="panel"><p class="label">fps against Do Nothing, Boeing's expected case (better site), with the worst and risk cases</p>{matrix_table()}
<p class="cap">The expected case is Airbus launching NGSA, with or without an A350 Re-engine, at even odds, as Boeing's CEO
expected in 2030. The tests: more than +$1B there, no case below {MINUS}$1B, and the risk case (NGSA with Airbus's Delay Tactics)
no more than $2B below Do Nothing. "Same years": Do Nothing counted over the same years as the fps (2026 to its entry into service + 19) rather than to 2060. Renton is the better site
in every combination. The game's own curve is shown for reference.</p></div>
</div></section>

<section id="why"><h2>Why the dates look alike but are not alike</h2><p class="lede">The fps's value against Do Nothing, line by line, for aircraft
retiring as chapter 1 sets out. A later date shrinks the profit and the bill at 2026 by about the same amount, so the losses look alike. But
every point of margin, the main thing a launch case can add, is worth half as much for 2044 as for 2039.</p><div class="stack">
<div class="panel">{bridge_table()}<p class="cap">The first line is what the dashboard alone would book: a 2,000-a-year market where every sale is built.
It covers the 737 too, from 2026, because the dashboard's Do Nothing already loses share once NGSA flies. The second line takes it to this game:
Boeing's real factories (the fps ramps up like Airbus's NGSA plan), Airbus's real factories, your demand and the firm orders. The fps is counted
over 2039-2058, 2041-2060 or 2044-2063; Do Nothing to 2060, as Boeing's brief does.</p></div>
</div></section>

<section id="launch"><h2>What would make each date a launch</h2><p class="lede">Each lever alone, at the better site, valued in all six cases
as Boeing's brief does; then packages. The margin, price and bill are exact (they change only the value of the aircraft the game
delivers), and every pass line in these tables was re-checked on a re-solved dashboard. The ramp and preference are game runs. The test that
binds is always the business case.</p><div class="stack">
<div class="panel"><p class="ctitle">In service 2039: a {mrange(2039)} margin, a {brange(2039)} bill, or a ramp {min(r39):.1f}-{max(r39):.1f} times as fast</p>{levers_table(2039)}</div>
<div class="panel"><p class="ctitle">In service 2041: a {mrange(2041)} margin or a {brange(2041)} bill; a 1.5× ramp plus a partner paying a quarter passes</p>{levers_table(2041)}</div>
<div class="panel"><p class="ctitle">In service 2044: a {mrange(2044)} margin or a {brange(2044)} bill; a 1.5× ramp plus a partner paying a quarter passes only if aircraft retire 2-4 years later</p>{levers_table(2044)}
<p class="cap">Ramp: the game's fps ramp (your NGSA chart moved to the fps date) run that many times as fast. "90/mo by year N" is the first calendar
year after entry into service averaging 90 a month: on the game's ramp it first passes 50 a month in year {GAME_TO50} and reaches 90 in year {GAME_TO90}; until 2050 the fps then
stays at 90, because Boeing's total is capped at 100 a month and the 737 keeps a 10-a-month tail.
"Over 12×": not reached at 12 times as fast; at full rate from entry into service the 2044 fps would reach {rng([case(n, 2044)["ramp_instant"]["expected"] for n in NS], bp)}.</p></div>
<div class="panel"><p class="label">Reading the levers</p><ul class="cav">
<li><b>Margin is unit profit.</b> Today ${P0:.0f}M at {pc(M0, 2)} is ${UNIT_FPS:.1f}M an aircraft (the 737 MAX makes ${UNIT_737:.2f}M). A launch at 2039 needs about
${K.rnd(P0 * min(case(n, 2039)["margin_needed"] for n in NS), 0):.0f}M, through lower cost, more content or a higher price. Holding today's cost per aircraft
(${COST0:.1f}M), that is a price of about ${K.rnd(min(case(n, 2039)["price_cost_held"] for n in NS), 0):.0f}M; holding the margin at {pc(M0, 2)} instead (cost rising with
price), it would take about ${K.rnd(min(case(n, 2039)["price_needed"] for n in NS), 0):.0f}M.</li>
<li><b>The bill is the dashboard's ${B0:.1f}B for a 10-year fps.</b> A partner's share is counted first as free money. Real partners (an engine maker, a structures
partner, a venture) are paid back through prices or a share of the profit: one that takes the same share of the fps's profit as it pays of the bill makes
the launch harder, not easier (at 2039 a quarter-for-a-quarter partner raises the margin needed to {rng([x['margin_fair'] for x in PT[2039]['0.25']], pc)}),
because Boeing still loses the 737 profit the fps replaces. Spending the same money earlier would cost more in today's money (10.5% a year), not less.</li>
<li><b>Ramp is how fast the fps fills its line.</b> 2039 needs 90 a month by year {rng(TO90[2039], str)} after entry into service, against year {GAME_TO90} on the game's ramp. At 2044 only a near-instant ramp is enough.</li>
<li><b>Preference is a strong lever with a ceiling.</b> At today's preference Boeing uses only {rng(USED0, lambda v: pc(v, 0))} of its narrowbody capacity over the
fps's 20 years: it is short only while the fps ramps up. More preference fills the rest: 10 more points is worth {rng(PREF10[2039], lambda v: bp(v, 1, False))} for 2039,
{rng(PREF10[2041], lambda v: bp(v, 1, False))} for 2041 and {rng(PREF10[2044], lambda v: bp(v, 1, False))} for 2044. It stops helping once Boeing builds everything
customers want or its factories are full; at that ceiling the fps reaches {rng(PREFMAX[2039], bp)} (2039), {rng(PREFMAX[2041], bp)} (2041) and {rng(PREFMAX[2044], bp)} (2044),
still short of +$1B. Here the order reverses: the 2044 fps has the most room to fill, so it comes closest.</li>
<li><b>Fundable.</b> Boeing's cash test holds in every combination: in the game's cash view net debt is repaid by 2030 and stays repaid even in the stress case.</li></ul></div>
</div></section>

<section id="said"><h2>What Boeing has said in 2026</h2><p class="lede">From the 2026 earnings calls and conferences you uploaded
(S&amp;P Global transcripts). Management points at the margin lever: a bigger share of the value chain's profit on the next airplane, through a little
more vertical integration and different partnerships, ventures and supplier relationships. Partners of that kind could also carry part of the bill,
as risk-sharing partners do, but that is our reading, not something management said. No launch year is given. Our reading: no launch soon, which
makes 2039 tight: it needs a launch by about 2032.</p>{quotes()}</section>

<section id="sens"><h2>Sensitivities</h2><p class="lede">The ranking holds in every case in the first table: 2039 always needs the least margin and the
least bill cut, 2044 the most; no date passes.</p><div class="stack">
<div class="panel"><p class="label">fps against Do Nothing (expected case), margin needed and bill needed, range over the five retirement timings</p>{sens_table()}
<p class="cap">Same years: Do Nothing counted over the fps's own 20 years; Boeing's Do Nothing profit year by year is unchanged (checked), only which
years count. Your page's demand from 2026: your page understates demand before 2038 by its own account, so the firm orders are not used up by 2038
({n0(min(FIRM_LEFT.values()))} to {n0(max(FIRM_LEFT.values()))} still open at the end of 2038, against none with the splice). Tianjin: your chart 4.1 adds 20 a month on top of
Airbus's plan; in the game it also scales with Airbus's capacity response and slows it. It mostly helps Airbus: the fps is worse in {TJ_WORSE} of the 15
combinations. Your page's supply makes the fps better in every combination: its fps ramps faster in the first years (a straight line to 80 a month in
7 years), for 2039 and 2041 its 737 winds down more gradually after the fps enters service than the game's Renton plan, and without the fps the 737 stays at 52 a month,
below the game's 57.</p></div>
<div class="panel"><p class="label">Worlds Boeing does not control</p>{worlds_table()}
<p class="cap">Faster erosion of Boeing's preference makes Do Nothing worse, but Airbus cannot build the share it wins. Customers it cannot serve
still buy 737s, so the fps gains little. A 3-year NGSA slip helps more, and helps the 2039 fps most in every timing. Neither passes.</p></div>
</div></section>

<section id="notes"><h2>Notes</h2><div class="panel"><ul class="cav">
<li><b>The fps at each date</b> is the game's 10-year fps: the ${B0:.1f}B bill booked at entry into service as the dashboard books it, the game's capture speed,
the NGSA-shaped ramp. Only its entry into service moves. In the game a 2030 launch enters service in 2040, so at this bill (a 10-year programme) 2039 implies a 2029
launch, and 2041 and 2044 imply launches in 2031 and 2034. The 2039 rows "9-year programme" (bill ${BILL9:.2f}B, between the 7- and
10-year bills) and "7-year fps launched in 2032" (${BILL7:.1f}B; the game's own 7-year fps, checked to match exactly) show what other routes to 2039 cost; the 8-year route from 2031 (${(BILL9 + BILL7) / 2:.2f}B, interpolated) is in the launch-year table.</li>
<li><b>Everything else is the game as played:</b> NGSA in service 2037 in the NGSA cases, the firm orders inside demand, Boeing losing 1 point a year while
NGSA flies alone, Boeing taking Airbus's slack, Airbus adding 1% capacity a year when short. Do Nothing is unchanged.</li>
<li><b>Counting.</b> Boeing's brief counts each plan from 2026 to its fps's entry into service + 19, and Do Nothing to 2060 (the default fps date, 2041, + 19). The
dashboard itself compares a plan with its baseline over the same years; the "same years" figures do that. Both are shown; the lever ranking is the same.</li>
<li><b>Booking the bill.</b> Boeing's brief books the whole bill at entry into service, as the dashboard does. Spent as the cash goes out over the
development years (the game's cash phasing curve, the debt penalty kept), every margin needed here would be {pts(min(LEVEL))} to {pts(max(LEVEL))} points higher. The
ranking of the dates, at the same bill or at the same launch year, is the same either way.</li>
<li><b>The tests</b> are Boeing's 2030 Board tests, applied to the six rival cases of Boeing's 2030 brief, as in the earlier fps pages.</li>
<li><b>Beyond the dashboard's sliders.</b> Every margin a lever needs on its own ({pc(ALONE_MAX30)} or more), and the fair-partner, 9-, 8- and 7-year margins, are above 30%,
the top of the dashboard's fps margin slider. The headless solve does not clamp it, so they are exact in the dashboard's arithmetic, but you cannot set them on the
dashboard itself. The package margins below 30% can be set.</li>
<li><b>Checks:</b> with the game's own curve and the fps in 2040, the analysis gives back Boeing's 2030 brief exactly ({b(D["game_curve"]["2040"]["renton"]["expected"])} at Renton). Every
margin, price, bill, partner, package, 9-, 8- and 7-year, same-years and sensitivity threshold was re-checked on a re-solved dashboard. The line-by-line values add to the total exactly.</li>
<li><b>Dollars:</b> PV at 2026, constant 2026 dollars, Boeing's 10.5% WACC, as the dashboard does.</li>
<li><b>Source:</b> analysis/demand_scenarios/make_page_demand.py reads your page's data, and demand_scenarios.py runs the game (demand_scenarios.json).</li>
</ul></div></section>
<footer>BOEING PROPRIETARY. Built by make_demand_scenarios_html.py from analysis/demand_scenarios/demand_scenarios.json and page_demand.json (run dash-2050-cons).</footer></div>
<script>{K.JS}</script></body></html>'''
    with open(out_path, "w") as f:
        f.write(page)
    print("wrote", out_path, len(page))


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "fps_demand_scenarios.html"))
