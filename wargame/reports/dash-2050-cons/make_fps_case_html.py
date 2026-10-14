"""Build fps_business_case_cons.html: Boeing's fps business case on the user's conservative-case market (run
dash-2050-cons), why it differs from the war game without supply and demand (dash-2050-obj, where Boeing launched the
fps), and what would have to change for the fps to pass Boeing's own 2030 tests.

Every number comes from analysis/fps_business_case/case.json (make_case.py: reconciles exactly with the game's ΔPV),
analysis/fps_choice/thresholds.json (thresholds.py: Boeing's 2030 brief, column by column) and
analysis/fps_choice/bridge.json (bridge.py: the dashboard alone to this game, one change at a time).

Usage: python3 make_fps_case_html.py [out.html]"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050-obj"))
import page_kit as K  # noqa: E402

esc = K.esc
A = os.path.join(HERE, "analysis")
C = json.load(open(os.path.join(A, "fps_business_case", "case.json")))
T = json.load(open(os.path.join(A, "fps_choice", "thresholds.json")))
BR = json.load(open(os.path.join(A, "fps_choice", "bridge.json")))
CK = json.load(open(os.path.join(HERE, "data", "cons_checks.json")))
D = json.load(open(os.path.join(HERE, "data", "report_data.json")))
SDF = D["rounds"][-1]["sd"]
P = C["params"]
R = C["cases"]["renton"]
N = C["cases"]["new_site"]
ROWS = R["rows"]
BY = {r["year"]: r for r in ROWS}
EIS = R["eis"]
Y_LO, Y_HI = 2030, EIS + P["post_eis_years"] - 1
YEARS = list(range(Y_LO, Y_HI + 1))
MINUS = K.MINUS
SITE = {"renton": "Renton", "new_site": "new sites"}
RI = {x["year"]: x["briefed"] for x in CK["round_items"]}
assert abs(RI[2030]["fps_10yr_renton"] - R["game_npv"]) < 1e-9, "the business case is not the 2030 brief's played column"


def b(v, dp=2, sign=True):
    return K.usd(v, dp, sign)


def bp(v, dp=2, sign=True):
    """Plain-text $B for SVG text and tooltips (no HTML)."""
    return re.sub(r"<[^>]+>", "", K.usd(v, dp, sign))


def f1(v):
    x = K.rnd(v, 1)
    return (MINUS if x < 0 else "") + f"{abs(x):,.1f}"


def n0(v):
    return f"{K.rnd(v, 0):,.0f}"


def pc(v, dp=1):
    return f"{K.rnd(v * 100, dp):.{dp}f}%"


def legend(items):
    def key(var, kind):
        if kind in ("ln", "dash"):
            da = ' stroke-dasharray="6 4"' if kind == "dash" else ""
            return (f'<svg width="24" height="4" aria-hidden="true" style="vertical-align:middle;margin-right:6px">'
                    f'<line x1="0" y1="2" x2="24" y2="2" stroke="var(--{var})" stroke-width="2"{da}/></svg>')
        return f'<i class="sq" style="background:var(--{var})"></i>'
    return '<div class="legend">' + "".join(f'<span>{key(v, k)}{esc(l)}</span>' for l, v, k in items) + "</div>"


# ─────────────────────────────── derived facts ───────────────────────────────
TESTS = T["tests"]
BASE_R = T["base"]["renton"]
LEV = {x["key"]: x for x in T["levers"]}
AN = T["analytic"]
WORLDS = {x["world"]: x for x in T["worlds"]}
RAMP = T["ramp_profiles"]
GAME_RAMP = {int(y): v for y, v in RAMP["game"]["by_year"].items()}
THR_RAMP = {int(y): v for y, v in RAMP["threshold"]["by_year"].items()}
SW = T["sweeps"]
best_ = lambda pts: max(max(p["renton"], p["new_site"]) for p in pts)
DEMAND_CEIL = best_(SW["demand"])
PREF_CEIL = best_(SW["pref"])
DEMAND_SAT = next(p["x"] for p in SW["demand"] if max(p["renton"], p["new_site"]) >= DEMAND_CEIL - 1e-6)
PREF_SAT = next(p["x"] for p in SW["pref"] if max(p["renton"], p["new_site"]) >= PREF_CEIL - 1e-6)
assert LEV["demand"]["threshold"] is None and LEV["growth"]["threshold"] is None and LEV["pref"]["threshold"] is None
assert DEMAND_CEIL < TESTS["business_case"] and PREF_CEIL < TESTS["business_case"]
GAP = TESTS["business_case"] - BASE_R["expected"]
ST = BR["steps"]
SH = BR["shapley"]
OBJ = BR["obj_game_brief"]
DASH_ITEM = ST[0]["item_new_site"]
avg = lambda key, a, z: sum(v for y, v in zip(SDF["year"], SDF[key]) if a <= y <= z) / (z - a + 1)
DEM_AVG = avg("demand_gross", 2040, 2059)
first5 = lambda d: sum(d[y] for y in range(EIS, EIS + 5))
R90 = lambda d: next(y for y in sorted(d) if d[y] >= 1079.0)
LATER = [x for x in T["later_rounds"] if x["site"] == "renton"]
LATER_BEST = max(LATER, key=lambda x: x["year"])
pref_after = [BY[y]["pref_fps_case"] for y in range(EIS + 1, Y_HI + 1)]
PREF_MAX_Y = next(y for y in range(EIS + 1, Y_HI + 1) if abs(BY[y]["pref_fps_case"] - max(pref_after)) < 1e-9)
DASH_UNITS = ST[0]["fps_renton"]
GAME_UNITS = ST[-1]["fps_renton"]
DN_DASH, DN_GAME = ST[0]["dn"], ST[-1]["dn"]
B_SOLD_TO = max(y for y, d, c in zip(SDF["year"], [a + b_ for a, b_ in zip(SDF["dlv_max"], SDF["dlv_fps"])], SDF["cap_max"])
                if 2035 <= y <= 2050 and abs(d - c) < 0.5)
UNIT_FPS = P["price_fps_m"] * P["margin_fps"]
UNIT_MAX = P["price_737_m"] * P["margin_737"]
FUND = T["fundable"]
assert all(c["stress_ok"] for c in FUND["renton"]) and all(c["stress_ok"] for c in FUND["new_site"])
FUND_PEAK = max(c["stress_peak"] for c in FUND["renton"])
RE787 = T["re787"]["items"]
CAPA = [a + n for y, a, n in zip(SDF["year"], SDF["cap_a320"], SDF["cap_ngsa"]) if 2038 <= y <= 2059]


def binding(items):
    e = sum(items[i] * w for i, w in zip((1, 4), (0.5, 0.5)))
    parts = {"business case": e - TESTS["business_case"], "downside": min(items) - TESTS["downside"], "buffer": items[5] - TESTS["buffer"]}
    return min(parts, key=parts.get)


# ─────────────────────────────── charts ───────────────────────────────
def chart_annual():
    """Cash view, $B a year: incremental operating profit and the Renton credit up, development spend down."""
    w, h, left, right, top, bot = 760, 360, 58, 20, 20, 46
    lo, hi, step = -10, 15, 5
    sx = lambda i: left + i * (w - left - right) / len(YEARS)
    bw = (w - left - right) / len(YEARS) - 3
    sy = lambda v: top + (hi - v) / (hi - lo) * (h - top - bot)
    out = [K.svg_open(w, h, "fps cash flow by year against Do Nothing, cash view")]
    t = lo
    while t <= hi + 1e-9:
        cls = "zero" if t == 0 else "grid"
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(t):.1f}" y2="{sy(t):.1f}" class="{cls}"/>'
                   f'<text x="{left - 8}" y="{sy(t) + 4:.1f}" text-anchor="end" class="tick">{K.num(t, "+.0f") if t else "0"}</text>')
        t += step
    for i, y in enumerate(YEARS):
        r = BY[y]
        x = sx(i) + 1.5
        op, sp, rc = r["op_profit_inc"], r["bill_cash"], r["renton_cash"]
        neg = op < -1e-9
        if sp < -1e-9 or neg:
            v_down = sp + (op if neg else 0.0)
            if neg and sp < -1e-9:
                out.append(f'<rect x="{x:.1f}" y="{sy(0) + 1:.1f}" width="{bw:.1f}" height="{max(0, sy(op) - sy(0) - 1):.1f}" fill="var(--s1)"/>')
                out.append(f'<path d="{K.bar_path(x, bw, sy(op) + 2, sy(v_down))}" fill="var(--s2)"/>')
            elif neg:
                out.append(f'<path d="{K.bar_path(x, bw, sy(0) + 1, sy(op))}" fill="var(--s1)"/>')
            else:
                out.append(f'<path d="{K.bar_path(x, bw, sy(0) + 1, sy(sp))}" fill="var(--s2)"/>')
        y0 = 0.0
        if op > 1e-9:
            if rc <= 1e-9:
                out.append(f'<path d="{K.bar_path(x, bw, sy(0) - 1, sy(op))}" fill="var(--s1)"/>')
            else:
                out.append(f'<rect x="{x:.1f}" y="{sy(op):.1f}" width="{bw:.1f}" height="{max(0, sy(0) - 1 - sy(op)):.1f}" fill="var(--s1)"/>')
            y0 = op
        if rc > 1e-9:
            out.append(f'<path d="{K.bar_path(x, bw, sy(y0) - (2 if y0 > 0 else 1), sy(y0 + rc))}" fill="var(--s3)"/>')
        rows = [(bp(r["net_cash"]), f"{y}: net cash flow", None), (bp(op), "incremental operating profit", "var(--s1)")]
        if sp < -1e-9:
            rows.append((bp(sp), "development spend", "var(--s2)"))
        if rc > 1e-9:
            rows.append((bp(rc), "Renton: new-site capex avoided", "var(--s3)"))
        out.append(f'<rect x="{sx(i):.1f}" y="{top}" width="{bw + 3:.1f}" height="{h - top - bot}" class="hit" {K.mark_attrs(*rows)}/>')
        if y % 5 == 0:
            out.append(f'<text x="{x + bw / 2:.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick">{y}</text>')
    out.append(f'<text x="{left}" y="{h - 5}" class="tick">$B a year, pre-tax, constant 2026 dollars (fps at Renton minus Do Nothing)</text></svg>')
    lg = legend([("Incremental operating profit (fps minus Do Nothing, as delivered)", "s1", "sq"),
                 (f"Development spend (${P['bill_10yr']:.1f}B over {Y_LO}-{EIS - 1})", "s2", "sq"), ("Renton: new-site capex avoided", "s3", "sq")])
    return lg + f'<div class="cw">{"".join(out)}</div>'


def chart_cumulative():
    """Cumulative net cash, undiscounted and discounted to 2026 (cash view); the game view's discounted path dashed."""
    w, h, left, right, top, bot = 760, 340, 58, 206, 20, 46
    cum, cpv, gpv = [], [], []
    a = p_ = g_ = 0.0
    for y in YEARS:
        r = BY[y]
        a += r["net_cash"]; p_ += r["net_cash"] * r["df"]; g_ += r["net_game"] * r["df"]
        cum.append((y, a)); cpv.append((y, p_)); gpv.append((y, g_))
    vals = [v for d in (cum, cpv, gpv) for _, v in d]
    step = 30
    lo, hi = step * (min(vals) // step) - step, step * (max(vals) // step + 1)
    sx = lambda x: left + (x - Y_LO) / (Y_HI - Y_LO) * (w - left - right)
    sy = lambda v: top + (hi - v) / (hi - lo) * (h - top - bot)
    series = [("Cash", "s1", cum, False), ("Cash view PV", "fg", cpv, False), ("Game view PV", "muted", gpv, True)]
    out = [f'<svg viewBox="0 0 {w} {h}" class="chart xh" role="img" aria-label="Cumulative net cash of the fps, undiscounted and '
           f'discounted. Use the arrow keys to read values by year." tabindex="0">']
    t = lo
    while t <= hi + 1e-9:
        cls = "zero" if t == 0 else "grid"
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(t):.1f}" y2="{sy(t):.1f}" class="{cls}"/>'
                   f'<text x="{left - 8}" y="{sy(t) + 4:.1f}" text-anchor="end" class="tick">{K.num(t, "+.0f") if t else "0"}</text>')
        t += step
    for yr in range(2030, Y_HI + 1, 5):
        out.append(f'<text x="{sx(yr):.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick">{yr}</text>')
    pb = R["payback_cash"]
    out.append(f'<line x1="{sx(pb):.1f}" x2="{sx(pb):.1f}" y1="{top}" y2="{h - bot}" class="leader"/>'
               f'<text x="{sx(pb) + 5:.1f}" y="{top + 11}" class="ann">cash back {pb}</text>')
    py = R["peak_funding_cash_year"]
    out.append(f'<text x="{sx(py):.1f}" y="{sy(R["peak_funding_cash"]) + 20:.1f}" text-anchor="middle" class="ann">peak need {bp(-R["peak_funding_cash"], 1, False)} ({py})</text>')
    for name, var, d, dash in series:
        path = "M" + " L".join(f"{sx(x):.1f},{sy(v):.1f}" for x, v in d)
        da = ' stroke-dasharray="6 4"' if dash else ""
        out.append(f'<path d="{path}" fill="none" stroke="var(--{var})" stroke-width="2"{da} stroke-linejoin="round"/>')
    last = [d[-1][1] for _, _, d, _ in series]
    order = sorted(range(3), key=lambda i: -last[i])
    placed, prev = {}, None
    for i in order:
        p = sy(last[i]) if prev is None else max(sy(last[i]), prev + 18)
        placed[i] = p; prev = p
    for i, (name, var, d, _) in enumerate(series):
        x, v = d[-1]
        out.append(f'<circle cx="{sx(x):.1f}" cy="{sy(v):.1f}" r="4" fill="var(--{var})" class="ring"/>')
        out.append(f'<text x="{w - right + 8}" y="{placed[i] + 4:.1f}" class="endlab">{esc(name)} {bp(v, 1)}</text>')
    payload = {"x0": left, "x1": w - right, "xlo": Y_LO, "xhi": Y_HI, "w": w, "fmt": "int", "years": YEARS,
               "series": [{"name": n + " ($B)", "k": f"var(--{c})", "vals": {str(x): round(v, 1) for x, v in d}}
                          for n, (_, c, d, _) in zip(("Cumulative cash", "Cumulative PV, cash view", "Cumulative PV, game view"), series)]}
    out.append(f'<line class="cross" x1="0" x2="0" y1="{top}" y2="{h - bot}" visibility="hidden"/>')
    out.append(f'<rect x="{left}" y="{top}" width="{w - left - right}" height="{h - top - bot}" class="xhit" data-cross="{esc(json.dumps(payload), quote=True)}"/>')
    out.append(f'<text x="{left}" y="{h - 5}" class="tick">$B, cumulative from 2030; PV discounted at {pc(P["WACC_B"])} to 2026</text></svg>')
    lg = legend([("Cumulative net cash (cash view)", "s1", "ln"), ("Cumulative present value at 2026 (cash view)", "fg", "ln"),
                 (f"Cumulative present value, game view (bill and debt penalty booked in {EIS})", "muted", "dash")])
    return lg + f'<div class="cw">{"".join(out)}</div>'


def short(lab):
    lab = lab.split(" (")[0]
    lab = {"three times as fast": "3× as fast", "50% more growth": "+50% growth", "20% more": "+20% demand",
           "+10 years at the 2059 profit": "+10 years"}.get(lab, lab)
    return lab.replace("-", MINUS)


def chart_tornado():
    S = sorted(C["sensitivities"], key=lambda s: -abs(s["high"] - s["low"]))
    base = C["base_for_sensitivities"]["game_npv"]
    w, left, right, top, row = 760, 20, 20, 40, 56
    h = top + row * len(S) + 44
    lo = 2 * int(min(min(s["low"], s["high"]) for s in S) // 2) - 2
    hi = max(4, 2 * int(max(max(s["low"], s["high"]) for s in S) // 2 + 2))
    sx = lambda v: left + (v - lo) / (hi - lo) * (w - left - right)
    halo = 'style="paint-order:stroke;stroke:var(--surface);stroke-width:4px;stroke-linejoin:round"'
    out = [K.svg_open(w, h, "Sensitivity of the fps value, game view")]
    for t in range(lo, hi + 1, 2):
        out.append(f'<line x1="{sx(t):.1f}" x2="{sx(t):.1f}" y1="{top - 8}" y2="{h - 38}" class="grid"/>'
                   f'<text x="{sx(t):.1f}" y="{h - 22}" text-anchor="middle" class="tick">{K.num(t, "+.0f") if t else "0"}</text>')
    out.append(f'<line x1="{sx(0):.1f}" x2="{sx(0):.1f}" y1="{top - 8}" y2="{h - 38}" class="zero"/>')
    out.append(f'<line x1="{sx(1):.1f}" x2="{sx(1):.1f}" y1="{top - 14}" y2="{h - 38}" class="ref"/>'
               f'<text x="{sx(1) + 4:.1f}" y="{top - 18}" class="reflab">Board bar +$1B</text>')
    out.append(f'<line x1="{sx(base):.1f}" x2="{sx(base):.1f}" y1="{top - 14}" y2="{h - 38}" class="leader"/>'
               f'<text x="{sx(base) - 4:.1f}" y="{top - 18}" text-anchor="end" class="ann">base {bp(base)}</text>')
    for i, s in enumerate(S):
        y = top + i * row
        out.append(f'<text x="{left}" y="{y + 12}" class="rowlab sm" {halo}>{esc(s["factor"])}</text>')
        for v, lab in ((s["low"], s["low_label"]), (s["high"], s["high_label"])):
            if abs(v - base) < 1e-6:
                continue
            col = "s1" if v > base else "s2"
            x0, x1 = sx(base), sx(max(lo, min(hi, v)))
            attrs = K.mark_attrs((bp(v), f"{s['factor']}: {lab}", f"var(--{col})"), (bp(s["low_cash"] if v == s["low"] else s["high_cash"]), "same change, cash view", None))
            out.append(f'<path d="{K.hbar_path(x0, x1, y + 20, 18)}" fill="var(--{col})" {attrs}/>')
            anchor = "start" if v > base else "end"
            tx = x1 + (6 if v > base else -6)
            out.append(f'<text x="{tx:.1f}" y="{y + 33}" text-anchor="{anchor}" class="val sm">{esc(short(lab))} {bp(v)}</text>')
    out.append(f'<text x="{left}" y="{h - 3}" class="tick">fps minus Do Nothing, $B PV at 2026, game view (Renton)</text></svg>')
    lg = legend([("Better than the base case", "s1", "sq"), ("Worse than the base case", "s2", "sq")])
    return lg + f'<div class="cw">{"".join(out)}</div>'


BRIDGE_SHORT = ["Dashboard alone", "Renton site saving", "Boeing's real factories", "Airbus's real factories",
                "Your demand curve", "Firm orders inside demand", "1 point a year after NGSA", "Airbus's slack to Boeing",
                "Airbus +1% capacity"]


def chart_bridge():
    """Horizontal waterfall: the 2030 fps at Renton against Do Nothing, from the dashboard alone to this game."""
    vals = [s["item_renton"] for s in ST]
    assert len(vals) == len(BRIDGE_SHORT)
    w, left, right, top, row = 760, 230, 70, 30, 34
    h = top + row * (len(vals) + 1) + 40
    lo, hi = 2 * int(min(vals) // 2) - 2, 2 * int(max(vals) // 2 + 1) + 2
    sx = lambda v: left + (v - lo) / (hi - lo) * (w - left - right)
    out = [K.svg_open(w, h, "From the dashboard alone to this game: the 2030 fps at Renton against Do Nothing")]
    for t in range(lo, hi + 1, 2):
        out.append(f'<line x1="{sx(t):.1f}" x2="{sx(t):.1f}" y1="{top - 8}" y2="{h - 38}" class="grid"/>'
                   f'<text x="{sx(t):.1f}" y="{h - 22}" text-anchor="middle" class="tick">{K.num(t, "+.0f") if t else "0"}</text>')
    out.append(f'<line x1="{sx(0):.1f}" x2="{sx(0):.1f}" y1="{top - 8}" y2="{h - 38}" class="zero"/>')
    out.append(f'<line x1="{sx(1):.1f}" x2="{sx(1):.1f}" y1="{top - 14}" y2="{h - 38}" class="ref"/>'
               f'<text x="{sx(1) + 4:.1f}" y="{top - 16}" class="reflab">Board bar +$1B</text>')
    labels = BRIDGE_SHORT + ["This game"]
    prev = None
    for i, lab in enumerate(labels):
        y = top + i * row
        out.append(f'<text x="{left - 10}" y="{y + 17}" text-anchor="end" class="rowlab sm">{esc(lab)}</text>')
        if i == 0 or i == len(labels) - 1:
            v = vals[0] if i == 0 else vals[-1]
            col = "s1" if v >= 0 else "s2"
            out.append(f'<path d="{K.hbar_path(sx(0), sx(v), y + 4, 20)}" fill="var(--fg)" {K.mark_attrs((bp(v), lab, None))}/>')
            out.append(f'<text x="{sx(v) + (6 if v >= 0 else -6):.1f}" y="{y + 18}" text-anchor="{"start" if v >= 0 else "end"}" class="val sm">{bp(v)}</text>')
            prev = v
            continue
        v = vals[i]
        d = v - prev
        col = "s1" if d >= 0 else "s2"
        if abs(d) > 1e-9:
            out.append(f'<rect x="{min(sx(prev), sx(v)):.1f}" y="{y + 4}" width="{max(1.0, abs(sx(v) - sx(prev))):.1f}" height="20" rx="3" fill="var(--{col})" '
                       f'{K.mark_attrs((bp(d), lab, f"var(--{col})"), (bp(v), "after this step", None))}/>')
        tx = max(sx(prev), sx(v)) + 6
        out.append(f'<text x="{tx:.1f}" y="{y + 18}" class="val sm">{bp(d)}</text>')
        prev = v
    out.append(f'<text x="{left}" y="{h - 3}" class="tick">fps at Renton minus Do Nothing, $B PV at 2026, 2030 decision</text></svg>')
    lg = legend([("Change that helps the fps", "s1", "sq"), ("Change that hurts the fps", "s2", "sq"), ("Start and end", "fg", "sq")])
    return lg + f'<div class="cw">{"".join(out)}</div>'


def xy_chart(series, x_lo, x_hi, x_step, x_fmt, y_lo, y_hi, y_step, label, aria, marks=()):
    """Line chart on a numeric x axis. series: [(name, css var, [(x, y)], dashed)]; marks: [(x, text)]."""
    w, h, left, right, top, bot = 760, 330, 58, 200, 26, 46
    sx = lambda x: left + (x - x_lo) / (x_hi - x_lo) * (w - left - right)
    sy = lambda v: top + (y_hi - v) / (y_hi - y_lo) * (h - top - bot)
    out = [K.svg_open(w, h, aria)]
    t = y_lo
    while t <= y_hi + 1e-9:
        cls = "zero" if abs(t) < 1e-9 else "grid"
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(t):.1f}" y2="{sy(t):.1f}" class="{cls}"/>'
                   f'<text x="{left - 8}" y="{sy(t) + 4:.1f}" text-anchor="end" class="tick">{K.num(t, "+.0f") if abs(t) > 1e-9 else "0"}</text>')
        t += y_step
    x = x_lo
    while x <= x_hi + 1e-9:
        out.append(f'<text x="{sx(x):.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick">{x_fmt(x)}</text>')
        x += x_step
    out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(1):.1f}" y2="{sy(1):.1f}" class="ref"/>'
               f'<text x="{left + 6}" y="{sy(1) - 6:.1f}" class="reflab">Board bar +$1B</text>')
    for xv, txt in marks:
        out.append(f'<line x1="{sx(xv):.1f}" x2="{sx(xv):.1f}" y1="{top}" y2="{h - bot}" class="leader"/>'
                   f'<text x="{sx(xv) + 5:.1f}" y="{top + 11}" class="ann">{esc(txt)}</text>')
    ends = []
    for name, var, pts, dash in series:
        d = "M" + " L".join(f"{sx(a):.1f},{sy(v):.1f}" for a, v in pts)
        da = ' stroke-dasharray="6 4"' if dash else ""
        out.append(f'<path d="{d}" fill="none" stroke="var(--{var})" stroke-width="2"{da} stroke-linejoin="round"/>')
        for a, v in pts:
            out.append(f'<circle cx="{sx(a):.1f}" cy="{sy(v):.1f}" r="5" fill="transparent" class="hit" {K.mark_attrs((bp(v), f"{name}: {x_fmt(a)}", f"var(--{var})"))}/>')
        ends.append((name, var, pts[-1]))
    placed, prev = {}, None
    for i in sorted(range(len(ends)), key=lambda i: sy(ends[i][2][1])):
        p = sy(ends[i][2][1]) if prev is None else max(sy(ends[i][2][1]), prev + 18)
        placed[i] = p; prev = p
    for i, (name, var, (a, v)) in enumerate(ends):
        out.append(f'<circle cx="{sx(a):.1f}" cy="{sy(v):.1f}" r="4" fill="var(--{var})" class="ring"/>'
                   f'<text x="{w - right + 8}" y="{placed[i] + 4:.1f}" class="endlab">{esc(name)} {bp(v)}</text>')
    out.append(f'<text x="{left}" y="{h - 5}" class="tick">{esc(label)}</text></svg>')
    return f'<div class="cw">{"".join(out)}</div>'


def chart_sweeps():
    best = lambda p: max(p["renton"], p["new_site"])
    ramp = [(p["x"], best(p)) for p in SW["ramp"]]
    dem = [(p["x"], best(p)) for p in SW["demand"]]
    a = xy_chart([("Faster ramp", "s1", ramp, False)], 1, 5, 0.5, lambda x: f"{x:g}×", -6, 4, 2,
                 "How many times faster the fps ramps up than your NGSA curve (better site)",
                 "fps value against Do Nothing in Boeing's expected case as the ramp speeds up",
                 marks=[(LEV["ramp"]["threshold"], f"passes at {LEV['ramp']['threshold']:.1f}×")])
    b_ = xy_chart([("More demand", "s2", dem, False)], 1, 3, 0.25, lambda x: f"{x:g}×", -6, 4, 2,
                  "Demand as a multiple of your conservative curve (better site)",
                  "fps value against Do Nothing in Boeing's expected case as demand rises",
                  marks=[(DEMAND_SAT, f"no gain beyond {DEMAND_SAT:.1f}×")])
    rows_r = [[f"{p['x']:g}×", K.num(p["renton"]), K.num(p["new_site"]), K.num(p["worst_renton"]), K.num(p["worst_new_site"])] for p in SW["ramp"]]
    rows_d = [[f"{p['x']:g}×", K.num(p["renton"]), K.num(p["new_site"]), K.num(p["worst_renton"]), K.num(p["worst_new_site"])] for p in SW["demand"]]
    rows_p = [[f"+{p['x']:g}", K.num(p["renton"]), K.num(p["new_site"]), K.num(p["worst_renton"]), K.num(p["worst_new_site"])] for p in SW["pref"]]
    head = ["Setting", "Expected, Renton", "Expected, new sites", "Worst column, Renton", "Worst column, new sites"]
    return (f'<p class="ctitle">A faster ramp crosses the Board\'s +$1B at {LEV["ramp"]["threshold"]:.1f}× ...</p>' + a
            + K.tview("Expected value as the ramp speeds up", head, rows_r)
            + f'<p class="ctitle" style="margin-top:18px">... but more demand stops helping at {DEMAND_SAT:.1f}× your curve, at {bp(DEMAND_CEIL)}</p>' + b_
            + K.tview("Expected value as demand rises", head, rows_d)
            + K.tview("Expected value as Boeing's preference for the fps rises (points)", head, rows_p))


# ─────────────────────────────── tables ───────────────────────────────
def cash_table():
    head = ["Year", "fps delivered", "Boeing delivered: fps case", "Boeing delivered: Do Nothing", "Incremental operating profit",
            "Development spend", "Renton credit", "Net cash flow", "Cumulative cash", "Discount factor", "Present value"]
    rows, cum = [], 0.0
    for y in YEARS:
        r = BY[y]
        cum += r["net_cash"]
        rows.append([str(y), n0(r["fps_units"]), n0(r["boeing_units_fps_case"]), n0(r["boeing_units_dn"]),
                     f1(r["op_profit_inc"]), f1(r["bill_cash"]), f1(r["renton_cash"]), f1(r["net_cash"]), f1(cum),
                     f"{r['df']:.3f}", f"{K.num(r['net_cash'] * r['df'], '+.2f')}"])
    tot_op = sum(BY[y]["op_profit_inc"] for y in YEARS)
    tot_sp = sum(BY[y]["bill_cash"] for y in YEARS)
    tot_rc = sum(BY[y]["renton_cash"] for y in YEARS)
    rows.append(["<b>Total</b>", "", "", "", f"<b>{f1(tot_op)}</b>", f"<b>{f1(tot_sp)}</b>", f"<b>{f1(tot_rc)}</b>",
                 f"<b>{f1(tot_op + tot_sp + tot_rc)}</b>", "", "", f"<b>{K.num(R['cash_npv'], '+.2f')}</b>"])
    return K.table(head, rows, num_cols=tuple(range(1, len(head))))


def value_table():
    head = ["$B, present value at 2026", "Game view, Renton", "Cash view, Renton", "Game view, new sites", "Cash view, new sites"]
    def row(lab, gr, cr, gn, cn):
        return [lab] + [("—" if v is None else K.num(v, "+.2f")) for v in (gr, cr, gn, cn)]
    rows = [
        row(f"Incremental operating profit, as delivered ({Y_LO}-{Y_HI})", R["op_profit_pv"], R["op_profit_pv"], N["op_profit_pv"], N["op_profit_pv"]),
        row(f"Development bill (${P['bill_10yr']:.1f}B)", -R["bill_pv_game"], -R["bill_pv_cash"], -N["bill_pv_game"], -N["bill_pv_cash"]),
        row("Debt penalty (valuation haircut, not cash)", -R["debt_penalty_pv"], None, -N["debt_penalty_pv"], None),
        row(f"Renton: new-site capex avoided (${P['sd']['renton_saving_b']:.1f}B)", R["renton_pv_game"], R["renton_pv_cash"], None, None),
        ["<b>Net present value</b>"] + [f"<b>{K.num(v, '+.2f')}</b>" for v in (R["game_npv"], R["cash_npv"], N["game_npv"], N["cash_npv"])],
        row("Same, valued at 2030 (the decision year)", R["game_npv_2030"], R["cash_npv_2030"], N["game_npv_2030"], N["cash_npv_2030"]),
    ]
    return K.table(head, rows, num_cols=(1, 2, 3, 4))


def steps_table():
    head = ["Step", "Do Nothing", "fps at Renton", "fps minus Do Nothing, Renton", "Same, new sites",
            "Boeing aircraft 2040-2059: Do Nothing", "Boeing aircraft 2040-2059: fps case", "of which fps"]
    rows = []
    for s in ST:
        rows.append([esc(s["step"]), K.num(s["dn"]), K.num(s["renton"]), K.num(s["item_renton"]), K.num(s["item_new_site"]),
                     n0(s["dlv_dn"]), n0(s["dlv_renton"]), n0(s["fps_renton"])])
    return K.table(head, rows, num_cols=tuple(range(1, 8)))


def shapley_table():
    g = SH["groups"]
    rows = [[esc(g[k]), K.num(SH["shares"]["renton"][k]), K.num(SH["shares"]["new_site"][k]), K.num(SH["dn_shares"][k])]
            for k in sorted(g, key=lambda k: SH["shares"]["renton"][k])]
    rows.append(["<b>Total</b>", f'<b>{K.num(sum(SH["shares"]["renton"].values()))}</b>', f'<b>{K.num(sum(SH["shares"]["new_site"].values()))}</b>',
                 f'<b>{K.num(sum(SH["dn_shares"].values()))}</b>'])
    return K.table(["Change from the dashboard's world", "fps minus Do Nothing, Renton", "Same, new sites", "Do Nothing alone"], rows, num_cols=(1, 2, 3))


def tests_table():
    t = T["base"]["renton"]
    risk = t["risk_case"]
    rows = [
        ["Business case", f"More than +$1B against Do Nothing in the expected case (Boeing's CEO: S2 and S5 at even odds)", K.num(t["expected"]), "fails"],
        ["Downside", "No worse than −$1B in any of the six cases", K.num(t["worst"]), "fails"],
        ["Rating first (buffer)", "In the risk case (S6: NGSA plus covert Delay Tactics), no more than $2B below Do Nothing", K.num(risk), "fails"],
        ["Fundable", "Net debt back to its historical level by 2030 and held, in the stress case", f"${FUND_PEAK:.1f}B peak, every case", "passes"],
    ]
    return K.table(["Test", "What Boeing's Board requires", "fps at Renton, 2030", "Result"], rows, num_cols=(2,))


def columns_table():
    head = ["Case in Boeing's 2030 brief", "Do Nothing", "fps at Renton", "fps minus Do Nothing", "fps, new sites, minus Do Nothing"]
    rows = []
    for i, lab in enumerate(T["columns"]):
        rows.append([f"S{i + 1}: {esc(lab)}", K.num(BASE_R["dn_row"][i]), K.num(BASE_R["plan_row"][i]), K.num(BASE_R["items"][i]),
                     K.num(T["base"]["new_site"]["items"][i])])
    return K.table(head, rows, num_cols=(1, 2, 3, 4))


def thresholds_table():
    rp = LEV["ramp"]
    ar, an = AN["renton"], AN["new_site"]
    bind = lambda items: binding(items)
    rows = [
        ["fps production ramp-up", f"Your NGSA curve: {n0(first5(GAME_RAMP))} aircraft in the first five years, 90 a month in {R90(GAME_RAMP)}",
         f"<b>{rp['threshold']:.1f}× as fast</b>: {n0(first5(THR_RAMP))} in the first five years, 90 a month in {R90(THR_RAMP)}", SITE[rp["site"]], rp["binding"]],
        ["fps operating margin", pc(ar["margin"]["base"]), f"<b>{pc(ar['margin']['threshold'])}</b> (${P['price_fps_m'] * ar['margin']['threshold']:.1f}M an aircraft, against ${UNIT_FPS:.1f}M)",
         "Renton", bind(ar["margin"]["items"])],
        ["fps price", f"${ar['price']['base']:.0f}M", f"<b>${ar['price']['threshold']:.1f}M</b> at the same margin", "Renton", bind(ar["price"]["items"])],
        ["Development bill", f"${ar['bill']['base']:.1f}B", f"<b>${ar['bill']['threshold']:.1f}B</b> ({pc(ar['bill']['threshold'] / ar['bill']['base'] - 1, 0).replace('-', MINUS)})", "Renton",
         bind(ar["bill"]["items"])],
    ]
    assert ar["margin"]["threshold"] <= an["margin"]["threshold"] and ar["bill"]["threshold"] >= an["bill"]["threshold"]
    return K.table(["Lever, alone", "In this game", "Needed for the fps to pass", "Site", "Test that binds"], rows)


def cannot_table():
    W = WORLDS
    def w(lab):
        x = W[lab]
        return K.num(x["expected"])
    rows = [
        ["More demand (your whole curve scaled up)", f"Best {bp(DEMAND_CEIL)}, reached at {DEMAND_SAT:.1f}× your curve; more adds nothing"],
        ["More fleet growth (replacement unchanged)", f"Best {bp(best_(SW['growth']))}: the same ceiling as demand"],
        ["Customers prefer the fps more", f"Best {bp(PREF_CEIL)}, at +{PREF_SAT:g} points of preference"],
        ["Boeing loses share faster in Do Nothing (2 or 3 points a year)", w("Boeing loses 3 points a year after NGSA")],
        ["No slack floor (Airbus's unbuilt orders do not come to Boeing)", w("No slack floor")],
        ["Airbus does not add capacity, or adds 2% a year", f"{w('No Airbus capacity response')} / {w('Airbus capacity response 2% a year')}"],
        ["Firm orders on top of demand (not part of it)", w("Firm orders on top of demand")],
        ["NGSA late: in service 2040 / 2043", f"{w('NGSA in service 2040 (3 years late)')} / {w('NGSA in service 2043 (6 years late)')}"],
        ["Airbus does not launch NGSA at all (the S1 case)", K.num(BASE_R["items"][0])],
        ["Boeing's single-aisle cap 120 a month instead of 100", w("Boeing's total cap 120 a month")],
        ["The previous game's market (dash-2050-sd)", w("Previous game's market (dash-2050-sd)")],
        [f"Waiting: launch in a later round (best: {LATER_BEST['year']}, its best case)", K.num(max(LATER_BEST["items"]))],
    ]
    return K.table(["Change, alone", "fps against Do Nothing, $B (Boeing's expected case unless stated)"], rows, num_cols=(1,))


def combos_table():
    rd = {x["ramp"]: x for x in T["combos"]["ramp_vs_demand"]}
    rm = {x["ramp"]: x for x in T["combos"]["ramp_vs_margin"]}
    rb = {x["ramp"]: x for x in T["combos"]["ramp_vs_bill"]}
    rows = []
    for k in sorted(rd):
        d = rd[k]["demand_k"]
        rows.append([f"{k:g}×" + (" (as played)" if k == 1 else ""),
                     ("never" if d is None else f"{d:.2f}× ({n0(rd[k]['demand_avg'])} a year in 2040-2060)"),
                     pc(rm[k]["margin"]), f"${rb[k]['bill']:.1f}B"])
    return K.table(["fps ramp speed", "and demand of at least", "or a margin of at least", "or a bill of at most"], rows)


def worlds_table():
    rows = []
    for x in T["worlds"]:
        rows.append([esc(x["world"]), SITE[x["site"]], K.num(x["expected"]), K.num(x["worst"]), K.num(x["risk_case"]),
                     "passes" if x["passes"] else "fails"])
    return K.table(["World", "Better site", "Expected case", "Worst case", "Risk case", "Boeing's tests"], rows, num_cols=(2, 3, 4))


def later_table():
    rows = []
    for x in LATER:
        rows.append([str(x["year"]), f"{x['year'] + 10}", K.num(max(x["items"])), K.num(min(x["items"]))])
    return K.table(["Launch round", "In service", "Best case in that brief", "Worst case"], rows, num_cols=(2, 3))


def sens_table():
    S = sorted(C["sensitivities"], key=lambda s: -abs(s["high"] - s["low"]))
    head = ["Factor (base)", "Change", "Game view", "Cash view", "Change", "Game view", "Cash view", "Note"]
    rows = [[esc(s["factor"]), esc(s["low_label"]), K.num(s["low"], "+.2f"), K.num(s["low_cash"], "+.2f"),
             esc(s["high_label"]), K.num(s["high"], "+.2f"), K.num(s["high_cash"], "+.2f"), esc(s["note"])] for s in S]
    rows.insert(0, ["<b>Base case</b>", "", f'<b>{K.num(R["game_npv"], "+.2f")}</b>', f'<b>{K.num(R["cash_npv"], "+.2f")}</b>', "", "", "", "fps at Renton"])
    return K.table(head, rows, num_cols=(2, 3, 5, 6))


def risk_table():
    rows = [[esc(x["risk"]), K.num(x["game"], "+.2f"), K.num(x["cash"], "+.2f"), esc(x["note"])] for x in C["risks"]]
    return K.table(["Risk", "Game view", "Cash view", "Why"], rows, num_cols=(1, 2))


def assumptions():
    sd, d = P["sd"], P["demand"]
    g = lambda y: SDF["demand_gross"][SDF["year"].index(y)]
    ramp = [n0(GAME_RAMP[y]) for y in range(EIS, EIS + 7)]
    dn_pref = [r["pref_dn"] for r in ROWS if r["year"] >= 2037]
    groups = [
        ("Decision", [
            ("Option", f"Launch a 10-year fps in 2030: in service {EIS}, engines code 7 ({esc(R['engines'])}). Base case at Renton (the better site); new sites shown alongside."),
            ("Counterfactual", "Do Nothing: the 737 MAX carries on, no fps, no 787 Re-engine, no rate increase."),
            ("Rivals", "As played in 2030: Airbus launches NGSA (in service 2037) on the A320 Alt plan; no A350 Re-engine; no Delay Tactics. Nobody moves after 2030."),
        ]),
        ("Your market", [
            ("Demand", f"Your conservative-case curve, 737/A320 class: {n0(g(2030))} aircraft in 2030, {n0(g(2040))} in 2040, {n0(g(2050))} in 2050, {n0(g(2059))} in 2059."),
            ("Firm orders (option B)", f"737 MAX {d['firm_backlog']['boeing']:,}, A320neo family {d['firm_backlog']['airbus']:,}: the first slice of each year's demand, not extra."),
            ("Customer preference", f"Do Nothing: 40% less 1 point a year from NGSA's 2037 entry into service, never below the share Airbus cannot build (it rises to {pc(max(dn_pref), 0)} in 2038 in the NGSA transition) and down to {pc(BY[Y_HI]['pref_dn'], 0)} in {Y_HI}. "
                                    f"With the fps: the same until {EIS}, then the dashboard's share rule: {pc(BY[EIS + 1]['pref_fps_case'], 0)} in {EIS + 1}, rising 1 point a year to {pc(max(pref_after), 0)} from {PREF_MAX_Y}."),
            ("Airbus", "Your Rev. B plan on the Alt plan, plus 1% capacity after each year it cannot build all its customers want."),
            ("Overflow", f"{pc(d['flex_share'])} of unserved customers take the other maker's free slots; {pc(d['lapse_per_year'], 0)} of those still waiting drop out each year."),
        ]),
        ("Prices and margins (constant 2026 $, no escalation)", [
            ("fps", f"${P['price_fps_m']:.0f}M at {pc(P['margin_fps'], 2)} = ${UNIT_FPS:.1f}M operating profit an aircraft."),
            ("737 MAX", f"${P['price_737_m']:.0f}M at {pc(P['margin_737'], 0)} = ${UNIT_MAX:.2f}M an aircraft."),
        ]),
        ("Capacity", [
            ("737 MAX", f"{', '.join(f'{v:g}' for v in sd['max_rate'].values())} a month in 2026-2029, then {sd['max_rate_after']:g} (684 a year). With the fps it gives way under Boeing's {sd['total_rate_cap']:g}-a-month total, keeping a {sd['max_tail_rate']:g}-a-month tail to 2050; at Renton, Renton's three lines (47 a month) wind down as the fps ramps and Everett carries on."),
            ("fps ramp", f"Your NGSA Rev. B curve, moved to {EIS}: {', '.join(ramp)} aircraft a year in {EIS}-{EIS + 6}, then 1,080 (90 a month) to 2050 and 1,200 from 2051."),
        ]),
        ("Investment", [
            ("Development bill", f"${P['bill_10yr']:.2f}B for the 10-year fps, constant 2026 $, from the dashboard (v3 snapshot)."),
            ("Timing", f"Game view: one lump in {EIS}, the entry-into-service year (the dashboard's convention). Cash view: spent over {Y_LO}-{EIS - 1} on the game's development curve: "
                       + ", ".join(f"{int(v * 100)}%" for v in P["phasing_curve"]) + "."),
            ("Renton", f"${sd['renton_saving_b']:.1f}B of new-site capex avoided (range ${sd['renton_saving_range_b'][0]:.1f}B-${sd['renton_saving_range_b'][1]:.1f}B): in {EIS} in the game view, $1.0B a year in {EIS - 3}-{EIS - 1} in the cash view."),
        ]),
        ("Financing and valuation", [
            ("Debt penalty (game view only)", f"The dashboard adds a leverage haircut as if the whole bill were added to Boeing's ${P['debt_boeing']:.0f}B gross debt: α × ((D+bill)³ − D³) / EV², with α {P['alpha']}, EV ${P['ev_boeing']:.0f}B. That is ${R['debt_penalty_nominal']:.1f}B booked in {EIS}, {b(R['debt_penalty_pv'], 2, False)} in present value at 2026. It is not a cash flow."),
            ("Discount rate", f"Boeing's WACC, {pc(P['WACC_B'], 1)}, to 2026, applied to constant-2026-dollar flows."),
            ("Horizon", f"The dashboard counts {P['post_eis_years']} years from entry into service ({EIS}-{Y_HI}). Nothing is counted after that."),
            ("Basis", "Pre-tax operating profit. No tax, working capital, recurring capex or support revenue. Widebody unaffected (no 787 Re-engine in either case)."),
        ]),
    ]
    rows = []
    for g_, items in groups:
        rows.append([f"<b>{g_}</b>", ""])
        for k, v in items:
            rows.append([k, v])
    return K.table(["Assumption", "Value and source"], rows)


def tiles():
    t = [("Net present value, game view", b(R["game_npv"]), f"The game's own valuation, as Boeing was briefed in 2030. Boeing's Board needs more than +$1B. New sites {b(N['game_npv'])}."),
         ("Net present value, cash view", b(R["cash_npv"]), f"The bill spent over {Y_LO}-{EIS - 1}, no debt penalty. New sites {b(N['cash_npv'])}."),
         ("Internal rate of return, cash view", pc(R["irr_cash"]), f"Against Boeing's {pc(P['WACC_B'])} cost of capital."),
         ("Peak funding need", b(-R["peak_funding_cash"], 1, False), f"Cumulative cash at its lowest, end-{R['peak_funding_cash_year']}."),
         ("Cash payback", str(R["payback_cash"]), f"Undiscounted. Discounted at {pc(P['WACC_B'])}, it never pays back within the {P['post_eis_years']} years counted."),
         ("Game without supply and demand", b(DASH_ITEM), "The same decision on the dashboard alone, where every forecast aircraft is built and sold: the case Boeing launched on in that game.")]
    return '<div class="tiles">' + "".join(
        f'<div class="panel tile"><div class="k">{esc(k)}</div><div class="v">{v}</div><div class="d">{d_}</div></div>' for k, v, d_ in t) + "</div>"


def build(out_path):
    css = K.CSS + "\np, li, footer, td { overflow-wrap: break-word; }\n.tiles { grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); }\n"
    top3 = [s["factor"].split(" (")[0] for s in sorted(C["sensitivities"], key=lambda s: -abs(s["high"] - s["low"]))[:3]]
    sh = SH["shares"]["renton"]
    ramp_r, ar = LEV["ramp"], AN["renton"]
    op_peak = max(BY[y]["op_profit_inc"] for y in YEARS)
    op_peak_y = max(YEARS, key=lambda y: BY[y]["op_profit_inc"])
    neg_years = [y for y in YEARS if y >= EIS and BY[y]["op_profit_inc"] < 0]
    aft = [BY[y]["op_profit_inc"] for y in YEARS if y > op_peak_y]
    op_after = (min(aft), max(aft))
    binds = {LEV["ramp"]["binding"]} | {binding(AN["renton"][k]["items"]) for k in ("margin", "price", "bill")}
    assert binds == {"business case"}, binds
    S_ = sorted(C["sensitivities"], key=lambda s: -max(s["low"], s["high"]))
    assert max(S_[0]["low"], S_[0]["high"]) < 1 and S_[0]["factor"].startswith("fps ramp")
    steps = {s["step"].split(" (")[0]: s for s in ST}
    d_boeing = ST[2]["item_renton"] - ST[1]["item_renton"]
    d_airbus = ST[3]["item_renton"] - ST[2]["item_renton"]
    d_demand = ST[4]["item_renton"] - ST[3]["item_renton"]
    d_firm = ST[5]["item_renton"] - ST[4]["item_renton"]
    d_rules = ST[-1]["item_renton"] - ST[5]["item_renton"]
    rd = {x["ramp"]: x for x in T["combos"]["ramp_vs_demand"]}
    rm = {x["ramp"]: x for x in T["combos"]["ramp_vs_margin"]}
    answers = [
        ("The case.", f" A 10-year fps launched in 2030 is worth {b(R['game_npv'])} against Do Nothing at Renton as the game values it "
                      f"({b(N['game_npv'])} at new sites), and {b(R['cash_npv'])} with the bill spent as it goes out. It returns "
                      f"{pc(R['irr_cash'])} against Boeing's {pc(P['WACC_B'])} cost of capital. In Boeing's expected case it is "
                      f"{b(BASE_R['expected'])}, {b(GAP, 2, False)} short of the +$1B its Board requires."),
        ("Why it paid in the game without supply and demand.", f" There the same decision was worth {b(DASH_ITEM)}, and Boeing launched. The "
                      f"dashboard sells every aircraft it forecasts from day one. It books {n0(DASH_UNITS)} fps over {EIS}-{Y_HI}, all at fps margins from "
                      f"the first year. Your factories build the fps up slowly: {n0(first5(GAME_RAMP))} in its first five years and {n0(GAME_UNITS)} "
                      f"over {EIS}-{Y_HI}. And Do Nothing is not the disaster the dashboard thinks ({b(DN_GAME)} against {b(DN_DASH)}), because Airbus "
                      f"cannot build the share it wins, so Boeing sells every 737 MAX it can build until {B_SOLD_TO}."),
        ("What would make it Boeing's choice.", f" On its own, any one of these: the fps ramping up {ramp_r['threshold']:.1f} times as fast "
                      f"(90 a month by {R90(THR_RAMP)} instead of {R90(GAME_RAMP)}); a {pc(ar['margin']['threshold'])} margin instead of "
                      f"{pc(ar['margin']['base'])}; a ${ar['price']['threshold']:.0f}M price instead of ${ar['price']['base']:.0f}M; or a "
                      f"${ar['bill']['threshold']:.1f}B bill instead of ${ar['bill']['base']:.1f}B. More demand or more customer preference "
                      f"cannot do it alone, however large: the slow ramp caps what the fps can add. With the ramp twice as fast, "
                      f"{pc(rd[2.0]['demand_k'] - 1, 0)} more demand or a {pc(rm[2.0]['margin'])} margin would be enough."),
    ]
    panels = '<div class="bl">' + "".join(f'<div class="panel"><div><b>{esc(t)}</b>{x}</div></div>' for t, x in answers) + "</div>"
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>fps Case, Conservative Market</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{css}</style></head><body><div class="wrap">
<header class="top"><p class="eyebrow">Boeing Product Development · conservative-case war game (dash-2050-cons) · BOEING PROPRIETARY</p>
<h1>The fps business case on your conservative market</h1>
<p class="lede">The decision Boeing faced in 2030: launch a 10-year fps (in service {EIS}) or Do Nothing, with Airbus
launching NGSA the same year. On your market (the conservative demand curve with firm orders inside it, Boeing losing 1
point a year after NGSA but taking Airbus's slack, and Airbus adding 1% capacity a year when short), the fps adds about
{b(R["op_profit_undiscounted"], 0, False)} of operating profit over {EIS}-{Y_HI}. But it needs {b(P["bill_10yr"], 1, False)} first, and its
profit arrives late as production ramps up. It is worth {b(R["game_npv"])} against Do Nothing as the game values it, and
{b(R["cash_npv"])} in cash. Below: the case, why it is so different from the game without supply and demand, and what would
have to change for the fps to become Boeing's choice.</p>
<nav class="toc"><a href="#answers">Summary</a><a href="#cash">Cash flow</a><a href="#table">Year by year</a><a href="#value">From cash flow to value</a><a href="#why">Why it differs</a><a href="#choice">What would make it Boeing's choice</a><a href="#assumptions">Key assumptions</a><a href="#sens">Sensitivities</a><a href="#notes">Notes</a></nav></header>

<section id="answers" style="margin-top:22px">{tiles()}{panels}</section>

<section id="cash"><h2>Cash flow</h2><p class="lede">Ten years of development spend, then a slow climb. Production follows
your NGSA ramp, so the fps adds little profit until {EIS + 3}. In {" and ".join(str(y) for y in neg_years)} it even costs
profit: at Renton the 737 MAX lines wind down as the fps ramps up, while with Do Nothing the MAX would have sold all it
can build. Cumulative cash bottoms out at {b(R["peak_funding_cash"], 1)} in {R["peak_funding_cash_year"]} and turns positive
in {R["payback_cash"]}. Discounted at {pc(P["WACC_B"])}, it never does within the {P["post_eis_years"]} years the game counts.</p><div class="stack">
<div class="panel"><p class="ctitle">Spend {b(P["bill_10yr"], 1, False)} in {Y_LO}-{EIS - 1}; incremental profit peaks at {b(op_peak, 1, False)} in {op_peak_y}, then runs {b(op_after[0], 1, False)}-{b(op_after[1], 1, False)} a year</p>{chart_annual()}</div>
<div class="panel"><p class="ctitle">Cash comes back in {R["payback_cash"]}; in present value the fps ends {b(-R["cash_npv"], 1, False)} short (cash view) or {b(-R["game_npv"], 1, False)} short (game view)</p>{chart_cumulative()}
<p class="cap">The game view books the whole bill, and the debt penalty, in {EIS}; that is why its line is flat until then and then drops. The cash view spends the bill as it goes out, so it is further below zero in present value.</p></div>
</div></section>

<section id="table"><h2>Year by year (cash view, fps at Renton)</h2><p class="lede">Aircraft and $B, pre-tax, constant 2026
dollars. Incremental operating profit is the fps case minus Do Nothing, each against the status quo, as delivered. The game
counts it to {Y_HI} ({P["post_eis_years"]} years from entry into service). $B flows are rounded to one decimal and present values to two; totals and the
cumulative column use unrounded values, so they may not add exactly.</p><div class="panel">{cash_table()}
<p class="cap">No incremental profit before {EIS}: under your rule Boeing's preference falls 1 point a year after NGSA in both cases until the fps is in service. In {EIS} the game view also books the {b(P["bill_10yr"], 2, False)} bill, the {b(R["debt_penalty_nominal"], 1, False)} debt penalty and the {b(R["renton_saving"], 1, False)} Renton saving (net {f1(BY[EIS]["net_game"])}); the cash view spreads them as shown.</p></div></section>

<section id="value"><h2>From cash flow to value</h2><p class="lede">The two views share the operating profit. They differ in when
the bill and the Renton saving are counted, and in the debt penalty. The game books the bill at entry into service, which cuts its present
value to {b(R["bill_pv_game"], 2, False)} from {b(R["bill_pv_cash"], 2, False)}; the cash view spends it over {Y_LO}-{EIS - 1} and drops the penalty, which is not a cash flow.</p><div class="stack">
<div class="panel">{value_table()}<p class="cap">The game view equals the game's ΔPV exactly (fps {b(R["dpv_fps"])} minus Do Nothing {b(R["dpv_dn"])} at Renton).</p></div>
</div></section>

<section id="why"><h2>Why it differs from the game without supply and demand</h2>
<p class="lede">In the game without supply and demand (dash-2050-obj) Boeing's 2030 brief showed the same 10-year fps at
{b(min(OBJ["item_10yr"]))} to {b(max(OBJ["item_10yr"]))} against Do Nothing, and Boeing launched it. Here the identical
decision shows {b(min(BASE_R["items"]))} to {b(max(BASE_R["items"]))}. Nothing about the fps itself changed: the same bill,
price, margin and entry into service. What changed is how many aircraft get built and sold, by whom, and when.</p><div class="stack">
<div class="panel"><ul class="cav">
<li><b>The dashboard sells every aircraft it forecasts, from day one.</b> It assumes 2,000 narrowbodies are sold every
year and that Boeing builds whatever its share is. The day the fps enters service, every Boeing narrowbody is an fps at
the fps margin: {n0(DASH_UNITS)} of them over {EIS}-{Y_HI}. In your world the fps is built on a production ramp like
Airbus's NGSA plan: {", ".join(n0(GAME_RAMP[y]) for y in range(EIS, EIS + 5))} aircraft in its first five years, 90 a
month only in {R90(GAME_RAMP)}. Profit that arrives late is worth far less at {pc(P["WACC_B"])}, while the bill is the
same. This one change takes {b(-d_boeing, 2, False)} off the fps. It is the main reason.</li>
<li><b>Do Nothing is not the disaster the dashboard thinks.</b> On the dashboard, once NGSA flies Boeing's share falls 3
points a year to 20%, and Do Nothing is worth {b(DN_DASH)}. In your world Airbus cannot build the share it wins: its
factories make {n0(min(CAPA))}-{n0(max(CAPA))} aircraft a year in 2038-2059. The customers it cannot serve buy 737 MAXs, and Boeing sells every MAX it builds
until {B_SOLD_TO}. Do Nothing is worth {b(DN_GAME)}. The fps is judged against that better alternative: Airbus's real
factories alone move the comparison by {b(d_airbus)}.</li>
<li><b>Your demand is smaller when the fps would sell.</b> Your conservative curve averages {n0(DEM_AVG)} aircraft a year
over 2040-2059, against the dashboard's 2,000. With fewer customers there is less for the fps to win: {b(d_demand)}.
Putting the firm orders inside demand (option B) pushes new customers later: {b(d_firm)}.</li>
<li><b>Your share rules make Do Nothing better</b>: Boeing loses 1 point a year instead of the dashboard's 3, and takes
Airbus's slack. That counts against the fps: {b(sh["rules"])} averaged over every order of the changes, but only
{b(d_rules)} with Airbus's capacity response when added last, because by then Airbus's real factories already cap how
much of the market it can take.</li>
</ul></div>
<div class="panel"><p class="ctitle">From {bp(ST[0]["item_renton"])} to {bp(ST[-1]["item_renton"])}: Boeing's real factories take {bp(-d_boeing, 2, False)} off the fps</p>{chart_bridge()}
<p class="cap">One change at a time, in this order, fps at Renton (the dashboard has no site choice, so the second bar adds the Renton saving). The layer with every limit off gives back the dashboard's own values exactly. The order matters; the table below splits the same change fairly over all orders.</p></div>
<div class="panel"><p class="label">Each step: Boeing's ΔPV against the status quo and its aircraft</p>{steps_table()}</div>
<div class="panel"><p class="label">The same change split over every order of the five groups (Shapley values), $B</p>{shapley_table()}
<p class="cap">Averaged over every order, Boeing's real factories account for {b(sh["boeing"])} of the {b(sum(sh.values()))} change at Renton. Do Nothing gains {b(sum(SH["dn_shares"].values()))} in all, mostly from Airbus's real factories and your share rules.</p></div>
</div></section>

<section id="choice"><h2>What would make the fps Boeing's choice</h2>
<p class="lede">Boeing decides through its ExCo and Board, and its Board set the tests in 2030. The fps fails three of them,
the first by {b(GAP, 2, False)}. Below: what would have to change, one lever at a time, then in combination. Each is valued
exactly as Boeing's 2030 brief valued the decision, in all six cases, with the better site. Nothing else moves.</p><div class="stack">
<div class="panel"><p class="label">Boeing's 2030 tests and where the fps stands</p>{tests_table()}
<p class="cap">The 787 Re-engine, Boeing's other option, was worth {bp(max(RE787))} but failed the downside test ({bp(min(RE787))} if Airbus also re-engined the A350), so an fps that passed would be Boeing's choice.</p></div>
<div class="panel"><p class="label">The fps in each case of Boeing's 2030 brief, $B against the status quo</p>{columns_table()}</div>
<div class="panel"><p class="label">Any one of these, alone, makes the fps pass</p>{thresholds_table()}
<p class="cap">Margin, price and bill are exact: they change only the value of the aircraft the game delivers, case by case. The ramp is a game run: your NGSA curve run faster, with Renton's MAX lines winding down at the same speed. In each case the business case is the test that binds; once it passes, the downside and buffer tests pass too.</p></div>
<div class="panel">{chart_sweeps()}
<p class="cap">Why demand runs out of road: beyond {DEMAND_SAT:.1f}× your curve, Boeing sells every aircraft it can build with or without the fps. The fps is then worth only the extra aircraft it lets Boeing build, and its slow ramp limits those in the years that count most. Customer preference hits the same wall at {bp(PREF_CEIL)}.</p></div>
<div class="panel"><p class="label">These cannot make the fps pass on their own</p>{cannot_table()}</div>
<div class="panel"><p class="label">In combination: what else is needed at a given ramp speed</p>{combos_table()}
<p class="cap">Each column is one combination with the ramp: demand alone, the margin alone, or the bill alone, at the better site.</p></div>
<div class="panel"><p class="label">Other worlds, the same 2030 decision</p>{worlds_table()}</div>
<div class="panel"><p class="label">Waiting does not fix it: the 10-year fps at Renton in each later round's brief, $B against Do Nothing</p>{later_table()}
<p class="cap">The rise comes from discounting: a later launch's loss is smaller at 2026. None reaches +$1B.</p></div>
</div></section>

<section id="assumptions"><h2>Key assumptions</h2><div class="panel">{assumptions()}</div></section>

<section id="sens"><h2>Sensitivities</h2><p class="lede">What moves the value of the played case (NGSA on the Alt plan), one factor
at a time from the Renton base. The {top3[0].lower()}, the {top3[1].lower()} and the {top3[2].lower()} matter most. Nothing
shown clears the Board's +$1B in this case; a three-times-faster ramp comes closest.</p><div class="stack">
<div class="panel"><p class="ctitle">The {top3[0].lower()}, the {top3[1].lower()} and the {top3[2].lower()} move the value most</p>{chart_tornado()}</div>
<div class="panel"><p class="label">The same changes in both views</p>{sens_table()}
<p class="cap">Margin and price change only the fps's profit an aircraft: deliveries in the game do not depend on them, so these rows are exact. The ramp, demand and growth rows are game runs at Renton. The tornado uses the case Airbus played; the thresholds above use Boeing's expected case, where the fps does a little better.</p></div>
<div class="panel"><p class="label">Two risks the tornado leaves out</p>{risk_table()}</div>
</div></section>

<section id="notes"><h2>Notes</h2><div class="panel"><ul class="cav">
<li><b>Two views, one decision.</b> The game view is the game's own valuation, the one Boeing's ExCo and Board decided on (briefed in 2030 at {b(RI[2030]["fps_10yr_renton"])} at Renton). The cash view spends the bill as it would go out and drops the debt penalty, which is a valuation haircut, not cash.</li>
<li><b>Real or nominal.</b> All flows are constant 2026 dollars, discounted at Boeing's {pc(P["WACC_B"])} WACC, as the dashboard does.</li>
<li><b>What is ours, not yours.</b> The fps ramp (your NGSA curve), the overflow and drop-out rates, the MAX path, the Renton figures and the development curve are game-master assumptions. The demand curve and the share and capacity rules are yours; the prices, margins, bill and debt penalty are the dashboard's.</li>
<li><b>Source.</b> analysis/fps_business_case/make_case.py writes case.json and reconciles with the game's ΔPV. analysis/fps_choice/thresholds.py reproduces Boeing's 2030 brief exactly, then moves one lever at a time; bridge.py checks that the layer with every limit off gives back the dashboard.</li>
</ul></div></section>
<footer>BOEING PROPRIETARY. Built by make_fps_case_html.py from analysis/fps_business_case/case.json, analysis/fps_choice/thresholds.json and analysis/fps_choice/bridge.json (run dash-2050-cons).</footer></div>
<script>{K.JS}</script></body></html>'''
    with open(out_path, "w") as f:
        f.write(page)
    print("wrote", out_path, len(page))


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "fps_business_case_cons.html"))
