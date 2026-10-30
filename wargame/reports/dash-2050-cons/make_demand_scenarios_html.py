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
assert not any(best(case(n, e))["passes"] for n, e in ALL), "an fps date passes: the page says none does"
for n in NS:                               # 2039 needs the smallest move on every lever, 2044 the largest
    m = [case(n, e)["margin_needed"] for e in EIS]
    bl = [case(n, e)["bill_needed"] for e in EIS]
    p = [case(n, e)["price_needed"] for e in EIS]
    assert m[0] < m[1] < m[2] and bl[0] > bl[1] > bl[2] and p[0] < p[1] < p[2], (n, m, bl, p)
    r = [case(n, e)["ramp_needed"] or 99.0 for e in EIS]
    assert r[0] <= r[1] < r[2], (n, r)
for key in ("tail", "tianjin", "page_supply"):
    for n in NS:
        m = [D["sensitivities"]["%s/N%s/%d" % (key, n, e)]["margin_needed"] for e in EIS]
        assert m[0] < m[1] < m[2], (key, n, m)
        assert not any(D["sensitivities"]["%s/N%s/%d" % (key, n, e)]["eval"][D["sensitivities"]["%s/N%s/%d" % (key, n, e)]["eval"]["best"]]["passes"] for e in EIS)
for n, e in ALL:
    c = case(n, e)
    assert all(abs(v) < 1e-5 for v in c["confirm"].values())
    assert all(x["stress_ok"] for x in c["fundable"])
    assert not any(w["passes"] for w in c["worlds"].values())
    assert c["pref_needed"] is None
EXP = {e: [best(case(n, e))["expected"] for n in NS] for e in EIS}
LO_EXP, HI_EXP = min(min(v) for v in EXP.values()), max(max(v) for v in EXP.values())
SPREAD = max(max(EXP[e][i] for e in EIS) - min(EXP[e][i] for e in EIS) for i in range(len(NS)))
LEAST_LOSS = {n: max(EIS, key=lambda e: best(case(n, e))["expected"]) for n in NS}
SPREAD1 = max(best(case("1", e))["expected"] for e in EIS) - min(best(case("1", e))["expected"] for e in EIS)
assert len({K.rnd(best(case("1", e))["expected"], 2) for e in EIS}) == 1, SPREAD1
assert LEAST_LOSS["0"] == 2039 and all(LEAST_LOSS[n] == 2044 for n in ("2", "3", "4")), LEAST_LOSS
assert all(c["eval"]["best"] == "renton" for c in C.values())
for n in NS:                               # a 3-year NGSA slip helps every date, the 2039 fps most
    w = [case(n, e)["worlds"]["ngsa2040"]["expected"] - best(case(n, e))["expected"] for e in EIS]
    assert w[0] > max(w[1:]) and min(w) > 0, (n, w)
    assert all(case(n, e)["worlds"]["ngsa2040"]["expected"] - best(case(n, e))["expected"] >
               case(n, e)["worlds"]["erosion3"]["expected"] - best(case(n, e))["expected"] for e in EIS)
PAGE_SUP_BETTER = all(D["sensitivities"]["page_supply/N%s/%d" % (n, e)]["eval"]["renton"]["expected"] > best(case(n, e))["expected"] for n, e in ALL)
assert PAGE_SUP_BETTER
TJ_WORSE = sum(D["sensitivities"]["tianjin/N%s/%d" % (n, e)]["eval"][D["sensitivities"]["tianjin/N%s/%d" % (n, e)]["eval"]["best"]]["expected"] < best(case(n, e))["expected"] for n, e in ALL)
for key in ("tail", "tianjin", "page_supply"):
    for n in NS:
        bl = [D["sensitivities"]["%s/N%s/%d" % (key, n, e)]["bill_needed"] for e in EIS]
        assert bl[0] > bl[1] > bl[2], (key, n, bl)
R44 = [case(n, 2044)["ramp_needed"] for n in NS]
assert all(case(n, 2044)["ramp_instant"]["margin"] > 0 for n in NS)
TO90 = {e: [case(n, e)["ramp_profiles"]["needed"]["to_90"] for n in NS if case(n, e)["ramp_needed"]] for e in EIS}
SDJ = json.load(open(os.path.join(HERE, "..", "..", "dashgame", "supply_demand.json")))
D_CLASS = pc(SDJ["demand"]["class_share"], 2)
GAP39 = min(1.0 - x for x in EXP[2039])
PARTNER25_PASSES_39 = all(case(n, 2039)["analytic"][case(n, 2039)["eval"]["best"]]["margin_with_partner"]["0.25"] == "passes" for n in NS)
assert PARTNER25_PASSES_39
BR0 = {e: case("0", e)["bridge"] for e in EIS}
for e in EIS:
    assert abs(sum(BR0[e].values()) - best(case("0", e))["expected"]) < 1e-3
PROFIT = {e: BR0[e]["nb_profit_vs_sq"] + BR0[e]["supply_demand"] for e in EIS}
COST = {e: -(BR0[e]["programme_investment"] + BR0[e]["debt_penalty"]) for e in EIS}
DEM = {n: dict(zip(PG["years"], PG["retire_later"][n]["demand"])) for n in NS}
SUM3860 = {n: sum(DEM[n][y] for y in range(2038, 2061)) for n in NS}
PEAK = {n: max(range(2038, 2061), key=lambda y: DEM[n][y]) for n in NS}
GD = dict(zip(GAME["years"], GAME["total"]))


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


# ─────────────────────────────── tables ───────────────────────────────
def matrix_table():
    head = ["Retirement"] + [f"In service {e}" for e in EIS]
    rows = []
    for n in NS:
        r = [esc(NLAB[n])]
        for e in EIS:
            c = case(n, e)
            x = best(c)
            r.append(f'{b(x["expected"])}<br><span class="muted small">worst {bp(x["worst"])} · risk {bp(x["risk_case"])}</span>')
        rows.append(r)
    g = D["game_curve"]
    rows.append(['<span class="muted">Game\'s own curve (reference)</span>'] +
                [f'<span class="muted">{b(g[str(e)][g[str(e)]["best"]]["expected"])}</span>' for e in EIS])
    return K.table(head, rows, num_cols=(1, 2, 3))


def levers_table(e):
    head = ["What changes", "Today"] + [NLAB[n] for n in NS]
    def row(lab, today, vals):
        return [lab, today] + vals
    cs = [case(n, e) for n in NS]
    def mm(v):
        return "passes" if v == "passes" else pc(v)
    def ramp_txt(c):
        k = c["ramp_needed"]
        if not k:
            return '<span class="muted">not reached</span>'
        p = c["ramp_profiles"]["needed"]
        return f"{k:.1f}×<br><span class=\"muted small\">90/mo in {p['to_90']} yr{'s' if p['to_90'] != 1 else ''}</span>"
    def an(c, key):
        return c["analytic"][c["eval"]["best"]][key]
    rows = [
        row("<b>fps margin</b> (alone)", pc(M0, 2), [pc(c["margin_needed"]) for c in cs]),
        row("<b>fps price</b> (alone)", f"${P0:.0f}M", [f"${c['price_needed']:.0f}M" for c in cs]),
        row("<b>Development bill</b> (alone)", f"${B0:.1f}B", [f"${c['bill_needed']:.1f}B" for c in cs]),
        row("<b>Ramp-up speed</b> (alone)", "1×<br><span class=\"muted small\">90/mo in 7 yrs</span>", [ramp_txt(c) for c in cs]),
        row("<b>Customer preference</b> (alone)", "—", ['<span class="muted">not reached</span>' for c in cs]),
        row("Margin needed if a partner pays 25% of the bill", pc(M0, 2), [mm(an(c, "margin_with_partner")["0.25"]) for c in cs]),
        row("Margin needed if a partner pays 50% of the bill", pc(M0, 2), [mm(an(c, "margin_with_partner")["0.5"]) for c in cs]),
        row("Margin needed with a 1.5× ramp (90/mo in 5 yrs)", pc(M0, 2),
            [pc(min(c["ramp15"]["analytic"][s]["margin"] for s in c["ramp15"]["analytic"])) for c in cs]),
        row("Margin needed with a 1.5× ramp and a partner paying 25%", pc(M0, 2),
            [mm("passes" if any(v == "passes" for v in c["package"].values()) else min(c["package"].values())) for c in cs]),
        row("Margin needed with customers preferring the fps by 10 more points", pc(M0, 2), [pc(c["pref10_margin"]) for c in cs]),
    ]
    return '<div class="lev">' + K.table(head, rows, num_cols=tuple(range(1, 2 + len(NS)))) + "</div>"


LINE_LAB = {"nb_profit_vs_sq": "fps profit on the dashboard's market (2,000 a year, every sale built)",
            "supply_demand": "Real factories and your demand (supply and demand layer)",
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
    return K.table(head, rows, num_cols=(1, 2, 3))


def sens_table():
    S = D["sensitivities"]
    def cell(key, e):
        xs = [S["%s/N%s/%d" % (key, n, e)] for n in NS]
        ex = [x["eval"][x["eval"]["best"]]["expected"] for x in xs]
        mg = [x["margin_needed"] for x in xs]
        return f'{rng(ex, bp)}<br><span class="muted small">margin needed {rng(mg, pc)}</span>'
    def main(e):
        return f'{erange(e)}<br><span class="muted small">margin needed {mrange(e)}</span>'
    head = ["World (all five retirement timings)"] + [f"In service {e}" for e in EIS]
    rows = [["<b>Main case</b>: your demand from 2038, the game's supply"] + [main(e) for e in EIS],
            ["Your demand's tail after 2055 replaced by the game's curve"] + [cell("tail", e) for e in EIS],
            ["Tianjin building 20 a month on top of Airbus's plan, 2035-2050"] + [cell("tianjin", e) for e in EIS],
            ["Your page's supply: 737 at 52 a month, then down to none by end-2050; fps to 80 a month in 7 years; Tianjin on"] +
            [cell("page_supply", e) for e in EIS]]
    return K.table(head, rows, num_cols=(1, 2, 3))


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


def tview_dots():
    head = ["Retirement"] + [f"{e}: value" for e in EIS] + [f"{e}: margin needed" for e in EIS]
    rows = [[esc(NLAB[n])] + [bp(best(case(n, e))["expected"]) for e in EIS] + [pc(case(n, e)["margin_needed"]) for e in EIS] for n in NS]
    return K.tview("both charts", head, rows)


def tview_demand():
    ys = list(range(2038, 2066))
    head = ["Year"] + [NLAB[n] for n in NS] + ["Game's curve"]
    rows = [[str(y)] + [n0(DEM[n][y]) for n in NS] + [n0(GD[y])] for y in ys]
    return K.tview("demand by year", head, rows)


QUOTES = [
    ("Q2 2026 earnings call, 28 Jul 2026 (Kelly Ortberg)",
     "“The actual share of the overall aerospace profitability is kind of embedded in the supply chain architecture, and we're "
     "not going to change that on the existing airplanes. … So it points to the next airplane as the opportunity to change that.” "
     "It “could require a little more vertical integration … different kind of business partnerships, different type of ventures.”",
     "The margin and the bill: the two levers this page says matter most."),
    ("Q3 2026 earnings call, 27 Oct 2026 (Kelly Ortberg, Jesus Malave)",
     "“Nothing has changed on our outlook on new airplane. We've got a team working in our product development right now, trying "
     "to define … what that looks like and what the market timing is.” Investment is “contemplated in our cash outlook”, mostly "
     "“R&D tech development”; after the 777X, “a shift of resources and spending from those development programs to new programs.”",
     "No launch is planned yet. A 10-year programme launched in 2031-2034 would enter service in 2041-2044."),
    ("Company conference, 17 Mar 2026 (Jesus Malave)",
     "“There will be a day where we have to enter into a new program. That day is not today, and it's not any time near.” Three "
     "conditions: the market, the technology and The Boeing Company must be ready.",
     "An fps in service in 2039 would need a launch in 2029-2030, earlier than this stance suggests."),
    ("Q3 2026 call and May 2026 conference (Ortberg, Malave)",
     "Rate 52 “in the back half of 2027”; deliveries in 2029 give “runway to deliver at a rate 63”; “we'd like to get some day "
     "to 63 a month.”",
     "The ramp lever: a production system that can add the fps quickly. The game's 737 path tops out at 57 a month plus the rate increase."),
]


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


def tiles():
    c39 = [case(n, 2039) for n in NS]
    t = [("Better date", "In service 2039",
          f"Needs the smallest change on every lever tested, in all five retirement timings; the margin and bill ranking holds in every sensitivity."),
         ("fps against Do Nothing", f"{bp(LO_EXP)} to {bp(HI_EXP)}",
          f"Boeing's expected case, all 15 combinations; none passes the Board's +$1B. The three dates are never more than {bp(SPREAD, 2, False)} apart."),
         ("Margin needed (alone)", " · ".join(rng([case(n, e)["margin_needed"] for n in NS], lambda v: f"{K.rnd(v * 100, 0):.0f}%").replace(" to ", "–") for e in EIS),
          f"For 2039 · 2041 · 2044, against {pc(M0, 2)} today (${UNIT_FPS:.1f}M of profit an aircraft)."),
         ("Bill needed (alone)", " · ".join(rng([case(n, e)["bill_needed"] for n in NS], lambda v: f"${K.rnd(v, 0):.0f}B").replace(" to ", "–") for e in EIS),
          f"For 2039 · 2041 · 2044, against ${B0:.1f}B today. For 2039, a partner paying a quarter of the bill is enough on its own.")]
    return '<div class="tiles">' + "".join(f'<div class="panel tile"><div class="k">{esc(k)}</div><div class="v">{esc(v)}</div><div class="d">{esc(d)}</div></div>' for k, v, d in t) + "</div>"


def build(out_path):
    css = K.CSS + EXTRA_CSS
    least = sorted(set(LEAST_LOSS.values()))
    r39 = [case(n, 2039)["ramp_needed"] for n in NS]
    r41 = [case(n, 2041)["ramp_needed"] for n in NS]
    m39_p = [case(n, 2039)["pref10_margin"] for n in NS]
    pkg = lambda n, e: "passes" if any(v == "passes" for v in case(n, e)["package"].values()) else min(case(n, e)["package"].values())
    pk41 = [pkg(n, 2041) for n in NS]
    pk44 = {n: pkg(n, 2044) for n in NS}
    assert all(v == "passes" for v in pk41), pk41
    pk44_pass = [n for n in NS if pk44[n] == "passes"]
    pk44_short = [n for n in NS if pk44[n] != "passes"]
    assert pk44_pass == ["2", "3", "4"] and pk44_short == ["0", "1"], pk44
    p25_41 = [case(n, 2041)["analytic"][case(n, 2041)["eval"]["best"]]["margin_with_partner"]["0.25"] for n in NS]
    p25_44 = [case(n, 2044)["analytic"][case(n, 2044)["eval"]["best"]]["margin_with_partner"]["0.25"] for n in NS]
    answers = [
        ("Which date is better for Boeing: 2039.",
         f" No date makes the fps pay on your demand. In Boeing's expected case it is worth {bp(LO_EXP)} to {bp(HI_EXP)} against Do Nothing "
         f"in every combination, at least {bp(GAP39, 2, False)} short of the Board's +$1B. On today's numbers the three dates lose about the same "
         f"(never more than {bp(SPREAD, 2, False)} apart; the later date loses a little less when aircraft retire 2-4 years later, because its "
         f"$60B bill is discounted further). But 2039 is the date Boeing could actually turn into a launch: it needs a {mrange(2039)} margin "
         f"against {mrange(2041)} for 2041 and {mrange(2044)} for 2044, or a bill of {brange(2039)} against {brange(2041)} and {brange(2044)}. "
         f"That holds in all five retirement timings and in every sensitivity below."),
        ("Why the later dates need more.",
         f" The game counts each fps for 20 years from entry into service, discounted at 10.5%. A later fps sells its aircraft later, so each point "
         f"of margin is worth less at 2026: with aircraft retiring as chapter 1 sets out, the fps's profit against Do Nothing falls from "
         f"{bp(PROFIT[2039], 1, False)} for 2039 to {bp(PROFIT[2044], 1, False)} for 2044. It also waits longer behind NGSA (in service 2037) while "
         f"Boeing's preference erodes, and an fps in 2044 is counted to 2063, into the years when your demand falls back. The bill and its debt "
         f"penalty shrink too ({bp(COST[2039], 1, False)} to {bp(COST[2044], 1, False)}), which is why the losses look alike. But a launch case "
         f"has to be built on the fps's own profit, and 2039 has the most of it to work with."),
        ("The retirement timing matters little.",
         f" Every timing gives about the same demand over 2038-2060 ({n0(min(SUM3860.values()))} to {n0(max(SUM3860.values()))} aircraft); "
         f"later retirement only moves the peak from {PEAK['0']} to {PEAK['4']}. That moves the fps by at most "
         f"{bp(max(max(EXP[e]) - min(EXP[e]) for e in EIS), 2, False)}, and helps the 2044 fps most because its first years sit in the later peak."),
        ("How Boeing could make each date a launch.",
         f" <strong>2039:</strong> Any one of a {mrange(2039)} margin (${K.rnd(P0 * min(case(n, 2039)['margin_needed'] for n in NS), 1):.1f}M of profit an aircraft "
         f"instead of ${UNIT_FPS:.1f}M), a bill of {brange(2039)} (a partner paying a quarter of it is enough), or a ramp about "
         f"{min(r39):.1f}-{max(r39):.1f} times as fast (90 a month within {rng(TO90[2039], str)} years of entry into service instead of 7). Customers preferring the fps by 10 more points "
         f"cuts the margin needed to {rng(m39_p, pc)}. <strong>2041:</strong> A {mrange(2041)} margin or a {brange(2041)} bill; a partner paying a quarter needs "
         f"{rng(p25_41, pc)} as well; a 1.5× ramp plus a partner paying a quarter passes on its own. <strong>2044:</strong> A {mrange(2044)} margin or a "
         f"{brange(2044)} bill; a partner paying a quarter still needs {rng(p25_44, pc)}. A 1.5× ramp plus that partner passes only if aircraft retire "
         f"2-4 years later; otherwise it still needs {rng([pk44[n] for n in pk44_short], pc)}. A faster ramp alone would have to be near-instant."),
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
again for growth), with every aircraft retiring as chapter 1 sets out or 1-4 years later. We run each against an fps entering service in 2039, 2041 or
2044. Each fps is valued exactly as Boeing's 2030 brief values it, in all six rival cases, at the better site, and held to Boeing's
three tests. Then we ask what would make each one a launch.</p>
<nav class="toc"><a href="#answers">Summary</a><a href="#demand">Demand scenarios</a><a href="#which">Which date</a><a href="#why">Why</a><a href="#launch">Making it a launch</a><a href="#said">What Boeing has said</a><a href="#sens">Sensitivities</a><a href="#notes">Notes</a></nav></header>

<section id="answers" style="margin-top:22px">{tiles()}{panels}</section>

<section id="demand"><h2>Demand scenarios</h2><p class="lede">Your page draws demand from 2038 ("before then half and half
understates it"), so each scenario uses the game's conservative curve to 2037 and your page from 2038. The game then takes the
737/A320 class share ({D_CLASS}) as it does for its own curve. The five timings carry almost the same aircraft; they differ in when the wave peaks.
Your curve falls after 2055 because it counts only today's fleet, so a sensitivity below hands the tail back to the game's curve.</p><div class="stack">
<div class="panel"><p class="ctitle">Retiring later moves the peak from {PEAK["0"]} to {PEAK["4"]}; 2038-2060 totals are within {n0(max(SUM3860.values()) - min(SUM3860.values()))} aircraft of each other</p>
<div class="legend"><span><i class="ln" style="background:var(--faint)"></i>Game's conservative curve</span>{"".join(f'<span><i class="ln" style="background:var(--d{n})"></i>{esc(NLAB[n])}</span>' for n in NS)}</div>
<div class="cw" data-focus="300">{chart_demand()}</div>{tview_demand()}
<p class="cap">Whole single-aisle market as your page draws it (A220 included), before the class share; the game's curve is the faint line. The game counts an fps
for 20 years from entry into service: 2039-2058, 2041-2060 or 2044-2063.</p></div>
<div class="panel"><p class="label">Aircraft a year on your page</p>{demand_table()}</div>
</div></section>

<section id="which"><h2>Which date is better for Boeing</h2><p class="lede">On today's numbers every date loses about the
same, {bp(LO_EXP)} to {bp(HI_EXP)} against Do Nothing in Boeing's expected case. The least-bad date depends on retirement
timing: 2039 loses least when aircraft retire as chapter 1 sets out, 2044 when they retire 2-4 years later (1 year later the three are
equal to the nearest $0.01B). Turning the fps into a launch is another matter: 2039 needs the least in every timing, 2044 by far the most.</p><div class="stack">
{legend_dates()}
<div class="panel"><p class="ctitle">2039 needs a {mrange(2039)} margin to become a launch; 2044 needs {mrange(2044)}</p><div class="cw">{chart_margin()}</div></div>
<div class="panel"><p class="ctitle">As they stand, all 15 lose {bp(-HI_EXP, 2, False)} to {bp(-LO_EXP, 2, False)} against Do Nothing, {bp(GAP39, 2, False)} or more short of the Board's +$1B</p><div class="cw">{chart_value()}</div>
<p class="cap">Zoomed axis: the dates differ by at most {bp(SPREAD, 2, False)} in any timing. Do Nothing is at $0 and the Board's line at +$1B, far to the right.</p></div>
{tview_dots()}
<div class="panel"><p class="label">fps against Do Nothing, Boeing's expected case (better site), with the worst and risk cases</p>{matrix_table()}
<p class="cap">The expected case is Airbus launching NGSA, with or without an A350 Re-engine, at even odds, as Boeing's CEO
expected in 2030. The tests: more than +$1B there, no case below {MINUS}$1B, and the risk case (NGSA with Airbus's Delay Tactics)
no more than $2B below Do Nothing. Renton is the better site in every combination. The game's own curve is shown for reference.</p></div>
</div></section>

<section id="why"><h2>Why the dates look alike but are not alike</h2><p class="lede">The fps's value against Do Nothing, line by line, for aircraft
retiring as chapter 1 sets out. A later date shrinks both the bill and the profit at 2026. The losses net out alike; the profit, the
only line a launch case can grow, shrinks fastest.</p><div class="stack">
<div class="panel">{bridge_table()}<p class="cap">The first line is what the dashboard alone would book: a 2,000-a-year market where every sale is built. The
second takes it to this game: Boeing's real factories (the fps ramps up like Airbus's NGSA plan), Airbus's real factories, your demand and the
firm orders. In service 2039, the fps is counted over 2039-2058; in 2044, over 2044-2063. Do Nothing is counted to 2060.</p></div>
</div></section>

<section id="launch"><h2>What would make each date a launch</h2><p class="lede">Each lever alone, at the better site, valued in all six cases
as Boeing's brief does; then packages. The margin, price and bill are exact (they change only the value of the aircraft the game
delivers), and each was re-checked on a re-solved dashboard. The ramp and preference are game runs. The test that binds is always the
business case.</p><div class="stack">
<div class="panel"><p class="ctitle">In service 2039: a {mrange(2039)} margin, a {brange(2039)} bill, or a ramp about twice as fast</p>{levers_table(2039)}</div>
<div class="panel"><p class="ctitle">In service 2041: a {mrange(2041)} margin or a {brange(2041)} bill; a 1.5× ramp plus a partner paying a quarter passes</p>{levers_table(2041)}</div>
<div class="panel"><p class="ctitle">In service 2044: a {mrange(2044)} margin or a {brange(2044)} bill; a 1.5× ramp plus a partner paying a quarter passes only if aircraft retire 2-4 years later</p>{levers_table(2044)}
<p class="cap">Ramp: the game's fps ramp (your NGSA chart moved to the fps date: 50 a month after 5 years, 90 after 7) run that many times as fast.
"Not reached": the ramp would have to exceed 12 times as fast (at full rate from entry into service: {rng([case(n, 2044)["ramp_instant"]["expected"] for n in NS], bp)} for 2044). Customer
preference alone never passes: Boeing already sells all it can build, so more preference only adds customers Boeing cannot serve
(at +60 points the 2039 fps reaches {rng([case(n, 2039)["pref_sweep"]["60.0"]["expected"] for n in NS], bp)}).</p></div>
<div class="panel"><p class="label">Reading the levers</p><ul class="cav">
<li><b>Margin is unit profit.</b> Today ${P0:.0f}M at {pc(M0, 2)} is ${UNIT_FPS:.1f}M an aircraft (the 737 MAX makes ${UNIT_737:.2f}M). A launch at 2039 needs about
${K.rnd(P0 * min(case(n, 2039)["margin_needed"] for n in NS), 1):.0f}M, through cost, content or price. The price column is the same unit profit taken entirely through price.</li>
<li><b>The bill is the dashboard's $60.3B for a 10-year fps.</b> A partner sharing it (an engine maker, a structures partner or a venture) counts only if the money is truly
off Boeing's books: moving the same spend into earlier R&D does not help.</li>
<li><b>Ramp is how fast the fps fills its line.</b> 2039 needs 90 a month within {rng(TO90[2039], str)} years of entry into service, against 7 in the game. At 2044 only a near-instant ramp is enough ({min(r for r in R44 if r):.1f} times as fast or more).</li>
<li><b>Fundable.</b> Boeing's cash test holds in every combination: in the game's cash view, net debt stays repaid from 2030 even in the stress case.</li></ul></div>
</div></section>

<section id="said"><h2>What Boeing has said in 2026</h2><p class="lede">From the 2026 earnings calls and conferences you uploaded
(S&amp;P Global transcripts). Management points at the same two levers this analysis does: a bigger share of the value chain on the next
airplane, which is the margin, and partnerships or ventures, which are the bill. Its timing points to the later dates.</p>{quotes()}</section>

<section id="sens"><h2>Sensitivities</h2><p class="lede">The ranking holds in every world below. 2039 always needs the least margin; no date passes.</p><div class="stack">
<div class="panel"><p class="label">fps against Do Nothing (expected case) and the margin needed, range over the five retirement timings</p>{sens_table()}
<p class="cap">Tianjin: your page's chart 4.1 adds 20 a month on top of Airbus's plan. That mostly helps Airbus: the fps is worse in {TJ_WORSE} of the 15 combinations.
Your page's supply makes the fps better in every combination: its fps ramps faster in the first years (a straight line to 80 a month in 7 years), and
without the fps the 737 stays at 52 a month, below the game's 57.</p></div>
<div class="panel"><p class="label">Worlds Boeing does not control</p>{worlds_table()}
<p class="cap">Faster erosion of Boeing's preference makes Do Nothing worse, but Airbus cannot build the share it wins. Customers it cannot serve
still buy 737s, so the fps gains little. A 3-year NGSA slip helps more, and helps the 2039 fps most in every timing. Neither passes.</p></div>
</div></section>

<section id="notes"><h2>Notes</h2><div class="panel"><ul class="cav">
<li><b>The fps at each date</b> is the game's 10-year fps: the $60.3B bill booked at entry into service as the dashboard books it, the 10-year
capture speed, the NGSA-shaped ramp. Only its entry into service moves. In the game a 2030 launch enters service in 2040, so 2039 implies a 9-year
programme from 2030 or a 2029 launch. 2041 and 2044 imply launches in 2031 and 2034.</li>
<li><b>Everything else is the game as played:</b> NGSA in service 2037 in the NGSA cases, the firm orders inside demand, Boeing losing 1 point a year while
NGSA flies alone, Boeing taking Airbus's slack, Airbus adding 1% capacity a year when short. Do Nothing is unchanged.</li>
<li><b>The tests</b> are Boeing's 2030 Board tests, applied to the six rival cases of Boeing's 2030 brief, as in the earlier fps pages.</li>
<li><b>Checks:</b> with the game's own curve and the fps in 2040, the analysis gives back Boeing's 2030 brief exactly ({b(D["game_curve"]["2040"]["renton"]["expected"])} at Renton). Every margin, price
and bill threshold was re-checked on a re-solved dashboard. The line-by-line values add to the total exactly.</li>
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
