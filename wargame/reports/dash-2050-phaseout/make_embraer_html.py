"""Build fps_embraer.html: Embraer, with a South Korean partner, as a third single-aisle maker in the MAX phase-out game,
and whether a partner could carry enough of Boeing's fps bill to launch it.

Reads data/embraer.json (embraer.py), data/politics.json (politics.py) and data/embraer_research.json (five research
tracks, each checked by an adversarial verifier). Every figure comes from those files; the claims in the copy are
asserted below.

  python3 make_embraer_html.py
"""
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050-obj"))
import page_kit as K  # noqa: E402
import make_franchise_html as MF  # noqa: E402

esc, b, bp, pct, nw, ctable = K.esc, MF.b, MF.bp, MF.pct, MF.nw, MF.ctable
EJ = json.load(open(os.path.join(HERE, "data", "embraer.json")))
PJ = json.load(open(os.path.join(HERE, "data", "politics.json")))
RS = json.load(open(os.path.join(HERE, "data", "embraer_research.json")))
EMB = EJ["embraer"]
PL, PLB = EJ["p_launch"]["base"], EJ["p_launch_if_boeing"]["base"]
PLN = EJ["p_launch_if_not"]["base"]
PLT, PLBT, PLNT = f"{round(100 * PL)}%", f"{round(100 * PLB)}%", f"{round(100 * PLN)}%"
EIS_B, PEAK_B = EMB["eis"]["base"], EMB["peak_a_month"]["base"]
YEAR = {1: 2030, 2: 2035, 3: 2045, 4: 2050}
R10, R8 = "10.5%", "8.1%"
MODES = ("rule", "pairwise", "worst_first", "premium")
TEN, TEN_NEW, SEVEN = "10-year at Renton", "10-year, new sites", "7-year at Renton"
FPS = ["10-year at Renton", "10-year, new sites", "7-year at Renton", "7-year, new sites", "10-year at Renton + Re-engine", "10-year, new sites + Re-engine"]
FR, BR, PO = "franchise", "brief", "franchise + politics"
RATE = {R10: 0.105, R8: 1.105 / 1.022 - 1}


def R(world, n, case, rate):
    return EJ["worlds"][world][str(n)]["%s|%s" % (case, rate)]


def best_fps(world, n, case, rate):
    """The best fps plan against Do Nothing in the CEO's columns, and its value."""
    e = R(world, n, case, rate)["e"]
    p = max(FPS, key=e.get)
    return p, e[p]


def rng(xs):
    if any(x is None for x in xs):
        known = [x for x in xs if x is not None]
        return (min(known), None) if known else None
    return min(xs), max(xs)


def s_rng(world, n, rate, dy=False):
    """Premium needed across the four readings of the CEO's rule (franchise + politics case)."""
    c = R(world, n, PO, rate)["S_needed_decision_year" if dy else "S_needed"]
    return rng([c[md] for md in MODES])


def s_txt(r_, dp=1):
    if r_ is None:
        return "none"
    lo, hi = r_
    a = bp(lo, dp, False)
    if hi is None:
        return f"{a} or more"
    z = bp(hi, dp, False)
    return a if a == z else f"{a}–{z[1:]}"


def p_rng(world, n, case, rate, key):
    c = R(world, n, case, rate)["partner"][key]
    return rng([c[md]["p"] for md in MODES])


def share_txt(r_):
    if r_ is None:
        return "over 60%"
    lo, hi = r_
    a = MF.cut_pct(lo)
    if hi is None:
        return f"{a}–over 60%"
    z = MF.cut_pct(hi)
    return a if a == z else f"{a[:-1]}–{z}"


def pkey(rp):
    return "boeing's rate" if rp is None else "%.0f%%" % (100 * rp)


# ─────────────────────────────── the claims, asserted ───────────────────────────────
PW = PJ["worlds"]["base"]
for n in (1, 2, 3, 4):
    for rt in (R10, R8):
        a = R("as played", n, PO, rt)
        p = PW[str(n)]["cases"]["base|full|cash base|" + rt]
        for md in MODES:      # with Embraer off, the premium and the government share are the politics page's
            x, y = a["S_needed"][md], p["readings"]["as played"][md]["S"]
            assert (x is None and y is None) or abs(x - y) < 1e-4, (n, rt, md, x, y)
            c, d = a["free_cut_needed"][md], p["cut_needed_by_reading"][md]
            assert abs(c + 0.02 - d) < 1e-4, (n, rt, md, c, d)
        x, y = a["S_needed"]["anticipating"], p["readings"]["anticipating"]["rule"]["S"]
        assert (x is None and y is None) or abs(x - y) < 1e-4
assert EJ["checks"]["no_embraer_equals_politics"] < 1e-9 and EJ["checks"]["price_rule_engine_vs_overlay"] < 1e-9


# ─────────────────────────────── charts ───────────────────────────────
ROWS_A = [("as played", "The game as played (its overflow-only entrant)"),
          ("line only", "Embraer-Korea's smaller line, overflow only"),
          ("Embraer low", "Embraer launches: low case"), ("Embraer base", "Embraer launches: base case"), ("Embraer high", "Embraer launches: high case"),
          ("expected", f"A {PLT} chance it launches"),
          ("expected, partly deterred", f"{PLNT} if Boeing waits, {PLBT} if it launches"),
          ("expected, deterred", f"{PLNT} if Boeing waits, none if it launches"),
          ("deterred", "Certain to launch unless Boeing launches first")]


def fps_chart(narrow=False):
    """2030: the 10-year fps at Renton against Do Nothing, franchise view, in each world, at 10.5% and 8.1%."""
    vals = [(w, lab, R(w, 1, FR, R10)["e"][TEN], R(w, 1, FR, R8)["e"][TEN]) for w, lab in ROWS_A]
    lo = math.floor(min(min(a, c) for _, _, a, c in vals) / 2) * 2
    hi = max(2, math.ceil(max(max(a, c) for _, _, a, c in vals) / 2) * 2)
    if narrow:
        w, left, right, rh, top = 400, 52, 52, 64, 10
    else:
        w, left, right, rh, top = 760, 300, 70, 46, 10
    h = top + rh * len(vals) + 30
    sx = lambda v: left + (v - lo) / (hi - lo) * (w - left - right)
    out = [K.svg_open(w, h, "The 10-year fps at Renton against Do Nothing in 2030, with and without an Embraer airliner", "chart narrow" if narrow else "chart")]
    t = lo
    while t <= hi + 1e-9:
        x = sx(t)
        out.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{top}" y2="{h - 24}" class="{"zero" if abs(t) < 1e-9 else "grid"}"/>'
                   f'<text x="{x:.1f}" y="{h - 8}" text-anchor="middle" class="tick">{esc(bp(t, 0))}</text>')
        t += 4 if narrow else 2
    for i, (wd, lab, a, c) in enumerate(vals):
        y = top + i * rh
        if narrow:
            out.append(f'<text x="12" y="{y + 13}" class="rowlab sm">{esc(lab)}</text>')
            y0 = y + 21
        else:
            out.append(f'<text x="{left - 10}" y="{y + 17}" text-anchor="end" class="rowlab sm">{esc(lab)}</text>')
            y0 = y + 6
        for j, (v, col) in enumerate(((a, "var(--s1)"), (c, "var(--s2)"))):
            by = y0 + j * 17
            out.append(f'<path d="{K.hbar_path(sx(0), sx(v), by, 11)}" fill="{col}"/>')
            tx, anc = (sx(v) - 5, "end") if v < 0 else (sx(v) + 5, "start")
            out.append(f'<text x="{tx:.1f}" y="{by + 10}" text-anchor="{anc}" class="val sm">{esc(bp(v, 1))}</text>')
        out.append(f'<rect x="0" y="{y}" width="{w}" height="{rh}" class="hit" {K.mark_attrs((lab, "", None), (bp(a, 2), "at 10.5%", "var(--s1)"), (bp(c, 2), "at 8.1%", "var(--s2)"))}/>')
    out.append("</svg>")
    return "".join(out)


RATES_X = [0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, None]
LINES_B = [("as played", "The game as played", "s1"), ("Embraer base", "Embraer launches (base)", "s2"),
           ("expected, partly deterred", f"Chance-weighted ({PLNT} if Boeing waits, {PLBT} if it launches)", "s3")]


def partner_chart(rate=R10, case=FR, narrow=False):
    """2030: the smallest share of the bill a partner must carry for Boeing's rule to launch an fps, by the partner's
    own cost of capital (low end of the range across the four readings)."""
    w, h = (400, 300) if narrow else (760, 330)
    left, right, top, bot = (44, 30, 18, 52) if narrow else (58, 40, 18, 46)
    xs = list(range(len(RATES_X)))
    sx = lambda i: left + i / (len(xs) - 1) * (w - left - right)
    ymax = 0.6
    sy = lambda v: top + (ymax - v) / ymax * (h - top - bot)
    out = [K.svg_open(w, h, "Share of the fps bill a partner must carry for Boeing to launch in 2030, by the partner's cost of capital", "chart narrow" if narrow else "chart")]
    for t in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6):
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(t):.1f}" y2="{sy(t):.1f}" class="grid"/>'
                   f'<text x="{left - 8}" y="{sy(t) + 4:.1f}" text-anchor="end" class="tick">{t * 100:.0f}%</text>')
    for i, rp in enumerate(RATES_X):
        lab = (rate if narrow else "Boeing's") if rp is None else f"{rp * 100:.0f}%"
        out.append(f'<text x="{sx(i):.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick">{lab}</text>')
    out.append(f'<text x="{left}" y="{h - 8}" class="tick">{"partner" + chr(39) + "s cost of money; last: Boeing" + chr(39) + "s" if narrow else "partner" + chr(39) + "s own cost of money (nominal); last: Boeing" + chr(39) + "s own, " + rate}</text>')
    for k, (wd, lab, col) in enumerate(LINES_B):
        pts = []
        for i, rp in enumerate(RATES_X):
            r_ = p_rng(wd, 1, case, rate, pkey(rp))
            pts.append((i, None if r_ is None else r_[0]))
        seg = [(i, v) for i, v in pts if v is not None]
        if len(seg) > 1:
            d = "M" + " L".join(f"{sx(i):.1f},{sy(v):.1f}" for i, v in seg)
            out.append(f'<path d="{d}" fill="none" stroke="var(--{col})" stroke-width="2" stroke-linejoin="round"/>')
        for i, v in pts:
            if v is None:            # open circles side by side where several lines have no share up to 60%
                out.append(f'<circle cx="{sx(i) + (k - 1) * 9:.1f}" cy="{sy(ymax):.1f}" r="4" fill="var(--surface)" stroke="var(--{col})" stroke-width="2"/>')
            else:
                out.append(f'<circle cx="{sx(i):.1f}" cy="{sy(v):.1f}" r="4" fill="var(--{col})" class="ring"/>')
    for i, rp in enumerate(RATES_X):
        rows = [(f"partner at {'Boeing' + chr(39) + 's rate' if rp is None else f'{rp * 100:.0f}%'}", "", None)]
        for wd, lab, col in LINES_B:
            r_ = p_rng(wd, 1, case, rate, pkey(rp))
            rows.append((share_txt(r_), lab, f"var(--{col})"))
        x0 = sx(i) - (sx(1) - sx(0)) / 2
        out.append(f'<rect x="{max(left, x0):.1f}" y="{top}" width="{sx(1) - sx(0):.1f}" height="{h - top - bot}" class="hit" {K.mark_attrs(*rows)}/>')
    out.append("</svg>")
    return "".join(out)


# ─────────────────────────────── tables ───────────────────────────────
def effect_table():
    """By round: the premium Boeing's rule would need (franchise and politics view), as the game was played and with
    Embraer-Korea, PV at 2026."""
    head = ["", "As played", "Embraer launches", "Low / high case", f"{PLT} chance", f"{PLNT}% / {PLBT}%".replace("%%", "%"),
            f"{PLNT}% / none".replace("%%", "%"), "Certain unless kept out"]
    rows = []
    for rt in (R10, R8):
        rows.append(f"Premium needed at {rt}, PV at 2026")
        for n in (1, 2, 3, 4):
            s0, sb, sl, sh = (s_rng(w, n, rt) for w in ("as played", "Embraer base", "Embraer low", "Embraer high"))
            later = "decided"
            cells = [s_txt(s_rng(w, n, rt), 2) if n == 1 else later for w in ("expected", "expected, partly deterred", "expected, deterred", "deterred")]
            rows.append([str(YEAR[n]), s_txt(s0, 2), s_txt(sb, 2), f"{s_txt(sl, 1)} / {s_txt(sh, 1)}"] + cells)
    return ctable(head, rows, num_cols=(1, 2, 3, 4, 5, 6, 7))


def units_table():
    U = EJ["units"]
    head = ["Aircraft a year", "2040", "2045", "2050", "2055", "2060"]
    ys = ("2040", "2045", "2050", "2055", "2060")
    rows = []
    for name, lab in (("Do Nothing", "Do Nothing"), (TEN, "10-year fps at Renton, launched 2030")):
        rows.append(lab)
        a, e = U[f"{name}|as played"], U[f"{name}|Embraer base"]
        rows.append(["Third maker: the game's entrant / Embraer-Korea"] + [f"{MF.n0(a[y]['embraer'])} / {MF.n0(e[y]['embraer'])}" for y in ys])
        rows.append(["Boeing: as played / with Embraer"] + [f"{MF.n0(a[y]['boeing'])} / {MF.n0(e[y]['boeing'])}" for y in ys])
        rows.append(["Airbus: as played / with Embraer"] + [f"{MF.n0(a[y]['airbus'])} / {MF.n0(e[y]['airbus'])}" for y in ys])
    return ctable(head, rows, num_cols=(1, 2, 3, 4, 5))


def partner_table():
    head = ["", "Partner at 3%", "4%", "5%", "6%", "7%", "At Boeing's own rate"]
    keys = ["3%", "4%", "5%", "6%", "7%", "boeing's rate"]
    rows = []
    for rt in (R10, R8):
        for case, clab in ((BR, "the brief"), (FR, "with the franchise terms"), (PO, "with the franchise and politics terms")):
            rows.append(f"At {rt}, {clab}")
            for n in (1, 2, 3, 4):
                rows.append([str(YEAR[n])] + [share_txt(p_rng("as played", n, case, rt, k)) for k in keys])
                if n == 1:
                    for w, lab in (("Embraer base", "2030, Embraer launches"), ("expected, partly deterred", f"2030, chance-weighted ({PLNT}/{PLBT})"),
                                   ("deterred", "2030, Embraer certain unless kept out")):
                        rows.append([lab] + [share_txt(p_rng(w, n, case, rt, k)) for k in keys])
    return ctable(head, rows, num_cols=(1, 2, 3, 4, 5, 6))


def inputs_table():
    lab = {"eis": "Embraer-Korea in service", "peak_a_month": "Peak rate, a month", "years_to_peak": "Years from service to peak",
           "share_fps": "Share of new customers once an fps is in service", "share_no_fps": "Share while Boeing has no new narrowbody in service",
           "cut": "Price cut on new single-aisles at full effect, with an fps in service", "no_fps_mult": "On Boeing's MAX while it has no new narrowbody, times that",
           "lead": "Years before Embraer's service the cut starts", "ramp": "Years to the full cut"}
    fmt = {"share_fps": pct, "share_no_fps": pct, "cut": lambda x: pct(x, 1), "no_fps_mult": lambda x: f"{x:g}x"}
    rows = []
    for k, l in lab.items():
        f = fmt.get(k, lambda x: f"{x:g}")
        rows.append([esc(l)] + [f(EMB[k][lv]) for lv in ("low", "base", "high")] + [esc(INPUT_BASIS[k])])
    rows.append([esc("Chance Embraer-Korea launches (about 2032)")] + [pct(EJ["p_launch"][lv], 0) for lv in ("low", "base", "high")] + [esc(INPUT_BASIS["p_launch"])])
    return ctable(["Input", "Low", "Base", "High", "Basis"], rows, num_cols=(1, 2, 3), txt_cols=(4,))


# ─────────────────────────────── the numbers the copy uses ───────────────────────────────
E = lambda w, n=1, rt=R10, case=FR, plan=TEN: R(w, n, case, rt)["e"][plan]
S = {(w, n, rt): s_rng(w, n, rt) for w in ("as played", "line only", "Embraer base", "Embraer low", "Embraer high") for n in (1, 2, 3, 4) for rt in (R10, R8)}
for w in ("deterred", "expected", "expected, deterred", "expected, partly deterred"):
    for rt in (R10, R8):
        S[(w, 1, rt)] = s_rng(w, 1, rt)
SY = lambda w, n, rt=R10: s_rng(w, n, rt, dy=True)
ANT = lambda w, rt=R10: R(w, 1, PO, rt)["S_needed"]["anticipating"]
PP = lambda w, rp, n=1, rt=R10, case=FR: p_rng(w, n, case, rt, pkey(rp))
DEC = lambda w, n=1, rt=R10, case=FR, md="rule": R(w, n, case, rt)["decision"][md]
FIX = lambda w, key, n=1, rt=R10, case=FR: R(w, n, case, rt)["fixed"][key]
PK = lambda w, key, rt=R10: R(w, 1, FR, rt)["packages"][key]
U = EJ["units"]
G = {w: E(w) for w in ("as played", "line only", "share only", "price only", "Embraer base", "deterred", "expected, partly deterred")}
G8 = {w: E(w, rt=R8) for w in ("as played", "Embraer base", "deterred")}
LINE, SHARE, PRICEC = G["line only"] - G["as played"], G["share only"] - G["line only"], G["price only"] - G["line only"]
TOTAL, COMP = G["Embraer base"] - G["as played"], G["Embraer base"] - G["line only"]
# if Embraer launches it costs the 2030 fps about $0.7B against Do Nothing at 10.5%: about $1.1B as a competitor, less about
# $0.4B because its line is smaller than the game's own entrant
assert 0.3 < LINE < 0.5 and -1.3 < COMP < -0.9 and -0.9 < TOTAL < -0.5 and SHARE < 0 and PRICEC < 0
assert all(S[("as played", n, R10)][0] < S[("Embraer base", n, R10)][0] for n in (1, 2, 3, 4))
assert 0.6 < S[("Embraer base", 1, R10)][0] - S[("as played", 1, R10)][0] < 1.0
assert S[("as played", 1, R8)][0] < 0.6 and S[("Embraer base", 1, R8)][0] > 2.0
# in each round's own money the effect does not shrink much; in 2026 money it does
dy = [SY("Embraer base", n)[0] - SY("as played", n)[0] for n in (1, 2, 3, 4)]
d26 = [S[("Embraer base", n, R10)][0] - S[("as played", n, R10)][0] for n in (1, 2, 3, 4)]
assert d26[0] > d26[1] > d26[2] > d26[3] and min(dy) > 0.4 * max(dy)
# at the evidence's chances a 2030 launch keeps the premium near the as-played level; only a certain Embraer makes it bite
s_pd, s_ed, s_det = S[("expected, partly deterred", 1, R10)][0], S[("expected, deterred", 1, R10)][0], S[("deterred", 1, R10)][0]
assert abs(s_pd - S[("as played", 1, R10)][0]) < 0.3 and s_ed < s_pd and s_det < s_ed < S[("as played", 1, R10)][0]
assert all(DEC(w) is None for w in ("expected", "expected, partly deterred", "expected, deterred", "deterred"))
assert DEC("deterred", rt=R8) == TEN_NEW and S[("deterred", 1, R8)] == (0.0, 0.0) and S[("expected, deterred", 1, R8)][0] == 0.0
assert S[("expected, partly deterred", 1, R8)][0] < S[("as played", 1, R8)][0]
# Embraer sells mostly to customers Airbus would have had
dn_a, dn_e = U["Do Nothing|as played"], U["Do Nothing|Embraer base"]
assert dn_a["2050"]["airbus"] - dn_e["2050"]["airbus"] > 3 * (dn_a["2050"]["boeing"] - dn_e["2050"]["boeing"])
# a partner in 2030 at 10.5%: a third to a half of the bill at 3-7%, none up to 60% at Boeing's own rate
pp3, pp7 = PP("as played", 0.03), PP("as played", 0.07)
assert 0.27 < pp3[0] < pp3[1] < 0.37 and 0.37 < pp7[0] < pp7[1] < 0.52 and PP("as played", None) is None
assert PP("as played", 0.02, n=3) is None and PP("as played", 0.02, n=4) is None
assert PP("as played", 0.03, rt=R8)[1] < 0.07 and PP("as played", None, rt=R8)[1] < 0.12
pw3, pw7 = PP("expected, partly deterred", 0.03), PP("expected, partly deterred", 0.07)
pd3, pd7 = PP("deterred", 0.03), PP("deterred", 0.07)
assert pw3[0] < pp3[0] and pd3[0] < pw3[0] and 0.2 < pd3[0] < 0.25 and 0.27 < pd3[1] < 0.31
# packages: none launches under the strict rule at 10.5% unless Embraer is certain to launch otherwise; at 8.1% Japan and
# Korea at their past scale do
ASIA, ASIA_HI, P35 = list(EJ["packages"])
assert EJ["packages"][ASIA] == [0.11, 0.06] and EJ["packages"][ASIA_HI] == [0.21, 0.045] and EJ["packages"][P35] == [0.35, 0.04]
for w in ("as played", "Embraer base", "expected", "expected, partly deterred", "expected, deterred"):
    assert all(PK(w, k)["decision"]["rule"] is None for k in (ASIA, ASIA_HI, P35)), w
assert PK("deterred", P35)["decision"]["rule"] == TEN_NEW and PK("deterred", ASIA_HI)["decision"]["rule"] is None
assert PK("as played", P35)["decision"]["premium"] == SEVEN and PK("as played", P35)["decision"]["anticipating"] == SEVEN
assert PK("as played", ASIA, R8)["decision"]["rule"] == TEN_NEW and PK("expected, partly deterred", ASIA, R8)["decision"]["rule"] == TEN_NEW
assert PK("Embraer base", ASIA, R8)["decision"]["rule"] is None
SP = {k: PK("as played", k)["s_over_p"][TEN_NEW] for k in (ASIA, ASIA_HI, P35)}
assert all(0.35 < v < 0.65 for v in SP.values())
# set terms: the repo's Joint Venture (35% for 25% of the profit) and pro-rata packages
JV, PR20, PR20X, PR35 = list(EJ["fixed"])
JV_RATE, JV_SPREAD = FIX("as played", JV)["implied_rate_nominal"][TEN], FIX("as played", JV)["implied_rate_spread"][TEN]
PR_RATE, PR_SPREAD = FIX("as played", PR20)["implied_rate_nominal"][TEN], FIX("as played", PR20)["implied_rate_spread"][TEN]
assert 0.08 < JV_RATE < 0.09 and 0.05 < JV_SPREAD < 0.06 and 0.115 < PR_RATE < 0.125 and 0.07 < PR_SPREAD < 0.08
assert all(FIX("as played", k)["decision"]["rule"] is None for k in (JV, PR20, PR20X, PR35))
assert FIX("as played", JV, rt=R8)["decision"]["rule"] == TEN_NEW and FIX("as played", PR20, rt=R8)["decision"]["rule"] is None
DEBT = EJ["checks"]["partner_at_boeing_rate"]["1|10-year at Renton"]["debt_penalty_saving"]
assert 2.1 < DEBT < 2.3
VERD = RS["verdicts"]


INPUT_BASIS = {
    "eis": "Embraer will define its next product from 2030 and launch only on mature engines and safe funding; the E2 took five years from launch to service, the government-funded KC-390 about ten, the A220 eight. Waiting for the next engines puts it no earlier than Airbus's NGSA (2037). The game's own entrant is in service in 2040.",
    "peak_a_month": "Embraer's best was about 9 a month (108 commercial jets in 2016, 101 in 2017) and it aims for about 120 a year across its E-Jets by 2030; the A220 is still climbing to 12-13 ten years in. Korea could add a second line (high).",
    "years_to_peak": "The E2 delivered 44 in 2025, seven years after entering service; the A220 has not reached its 14-a-month break-even rate in ten years.",
    "share_fps": "Three new Western types compete; the A220 took about 1,100 orders in 18 years against an A320neo backlog of about 7,500. Korea's flag carrier has ordered 50 737-10s.",
    "share_no_fps": "With the MAX running out and no new Boeing airplane, Embraer-Korea is the only Western alternative to Airbus: 71% of airlines and lessors surveyed would buy an Embraer narrowbody on its merits. Embraer's production line, not its share, is the limit at base.",
    "cut": "A simple competition model calibrated on the 14-17% margins Irwin and Pavcnik estimate gives about a 1.5-2% fall in the average net price at the ~5% share Embraer-Korea reaches with an fps in service (3-6% would need 10-30%); contested campaigns go far deeper (Bombardier to Delta, Boeing to United, the A220 to JetBlue). Long backlogs argue for the low end; a launch-period price war would be bigger but temporary.",
    "no_fps_mult": "Without a new Boeing airplane Embraer's share is larger and customers use it to discipline Airbus: the research's multiplier on the cut is 1.3 (1.0-1.8). It falls on the MAX in Do Nothing and the status quo alike, so it helps an fps that escapes it.",
    "lead": "Deals feel it about 4 years before the entrant's service (the neo/MAX price war began 5-6 years before service); deliveries are priced at order, about 3 years earlier.",
    "ramp": "Half the effect at the entrant's service, all of it about 3 years later, on deals; deliveries follow orders.",
    "p_launch": "Embraer's CEO in May 2026: studying \"either a commercial jet or a business jet\", no segment chosen, funding must not risk the company; it dropped its turboprop in 2025. Korea is pushing (July 2026) but calls the talks \"very early stage\" and its main track is Airbus and Boeing. The research said 35%; its check said 20%.",
}


def cards(items):
    return "<ul class=\"cav\">" + "".join(f"<li><b>{esc(a)}.</b> {esc(t)}</li>" for a, t in items) + "</ul>"


def fixed_table():
    head = ["Terms", "Partner pays", "Takes of the fps's profit", "Partner's return: money at entry into service / over development",
            "2030 at 10.5%", "2030 at 8.1%", "2030 at 10.5%, Embraer certain unless kept out"]
    lab = {JV: "The repo's own Joint Venture terms", PR20: "A 20% package, pro rata", PR20X: "A 20% package, 1.2 times the profit share", PR35: "A 35% package, pro rata"}
    rows = []
    for key, (p, s) in EJ["fixed"].items():
        a, c, d = FIX("as played", key), FIX("as played", key, rt=R8), FIX("deterred", key)
        rows.append([esc(lab[key]), pct(p, 0), pct(s, 0), f"{pct(a['implied_rate_nominal'][TEN], 1)} / {pct(a['implied_rate_spread'][TEN], 1)}", verdict(a), verdict(c), verdict(d)])
    return ctable(head, rows, num_cols=(1, 2, 3), txt_cols=(4, 5, 6))


def verdict(d):
    """Which readings of the CEO's rule launch an fps under a set of values."""
    dec = d["decision"]
    short = lambda p: esc(p.replace("10-year", "10-yr").replace("7-year", "7-yr").replace(" at Renton", " Renton").replace(", new sites", " new sites"))
    if dec["rule"]:
        return f"yes ({short(dec['rule'])})"
    if dec["premium"] and dec["anticipating"]:
        return f"only with the $2B allowance or a CEO anticipating the Board ({short(dec['premium'])})"
    if dec["premium"]:
        return f"only with the $2B allowance ({short(dec['premium'])})"
    if dec["anticipating"]:
        return f"only if the CEO anticipates the Board ({short(dec['anticipating'])})"
    return "no"


def packages_table():
    keys = list(EJ["packages"])
    head = [""] + [f"{esc(k)} ({pct(EJ['packages'][k][0], 0)} at {pct(EJ['packages'][k][1], 1)})" for k in keys]
    rows = []
    for rt in (R10, R8):
        rows.append(f"2030 at {rt}")
        cases = (("as played", "The game as played"), ("Embraer base", "Embraer launches"),
                 ("expected, partly deterred", f"Chance-weighted: {PLNT} if Boeing waits, {PLBT} if it launches"),
                 ("deterred", "Embraer certain to launch unless kept out"))
        for w, lab in (cases if rt == R10 else cases[:3]):
            rows.append([esc(lab)] + [verdict(R(w, 1, FR, rt)["packages"][k]) for k in keys])
    rows.append("What the partner takes back")
    rows.append(["Share of the fps's profit per share of the bill (precedent about 0.7-1.2)"] + [f"{PK('as played', k)['s_over_p'][TEN_NEW]:.2f}" for k in keys])
    return ctable(head, rows, txt_cols=(1, 2, 3))


def proposed_table():
    O = json.load(open(os.path.join(HERE, "data", "sd_options_embraer_proposed.json")))
    t, pp = O["third_party"], O["price_pressure"]
    rows = [["Embraer-Korea's line", f"in service {t['entrant']['eis']}, {t['entrant']['peak_a_month']:.0f} a month {t['entrant']['years_to_peak']} years later (the game's entrant: 2040, 20 a month)"],
            ["Customers it wins", f"{pct(t['entrant_share_no_fps'], 0)} of new customers while Boeing has no new narrowbody in service, {pct(t['entrant_share'], 0)} once an fps is (the game's entrant: none, only customers nobody else can serve)"],
            ["Prices", f"every new single-aisle delivered, Boeing's and Airbus's, {pct(pp['cut'], 0)} cheaper at full effect, from {pp['from']}, full after {pp['ramp_years']} years (the game: none)"],
            ["Both makers and the status quo", "run the same rules, so Airbus's payoffs feel Embraer too"],
            ["Not in it", "a move for Boeing to sign up partners: the game has only \"fps via Embraer\", whose bill the board sets at $100B; a partner move would be a new order (share of the bill, share of the profit)"]]
    return ctable(["Setting", "Proposed"], rows, txt_cols=(1,))


EMB_FACTS = [
    ("Korea asked", "President Lee Jae Myung named joint development of a next-generation commercial aircraft with Brazil as one of three priorities, in Sao Paulo on 28 July 2026: \"Let's build civilian aircraft together in the future, if possible.\" Lee's policy chief said Seoul wants in from the development stage, but the talks are \"very early stage\", with no form or terms agreed (Korea Herald, 28-29 July 2026; search extracts)."),
    ("A first paper", "KAI (Korea Aerospace Industries) and Embraer signed a non-binding memorandum on civil aviation and aerostructures on 28 July 2026, signed by both chief executives; it names no airliner. KAI and Korean Air each held talks with Embraer (Korean press). The 150-200-seat size comes from the Korean side; Embraer has not chosen a segment. Lula's state visit to Seoul in February 2026 had raised ties to a strategic partnership."),
    ("Embraer is careful", "Its chief executive: \"making studies for a new product, but we don't have any concrete plans yet\" (October 2024), and in May 2026 \"studies for a new cycle of products ... either a commercial jet or a business jet\", with no segment or timeline chosen and a funding strategy that must not \"put in risk the financial health of the company\"; until 2030 it focuses on its current products. It cancelled its turboprop in November 2025 (immature engines and no launch partner were the reported reasons), and was reported in 2025 as saying the market has room for \"three or four\" makers."),
    ("But able", "E-Jet and E2 each took about five years from launch to service, the E2 on a $1.7B budget; 78 commercial deliveries in 2025, about 120 a year targeted by 2030; $7.6B revenue in 2025, a $35.7B backlog (Q3 2026, reported), $11-13B market value. A narrowbody would cost about $10B (industry and Korean estimates), which Embraer cannot fund alone."),
    ("Korea's main track is Boeing and Airbus", "Korea's space agency (KASA) set up a public-private task force on 16 July 2026 for Korean firms to become core risk-sharing partners on the Airbus and Boeing successors expected around 2030; Embraer is a parallel option. Korean Air finalised 103 Boeing aircraft on 16 September 2026, including 50 737-10s (reported)."),
    ("Others warn", "Airbus's chief executive said Embraer should \"think twice\" (June 2026); analysts split between a bet-the-company move and one Embraer's low debt could absorb (Leeham, September 2026)."),
]
BRAZIL_FACTS = [
    ("At loggerheads", "Lula won the run-off on 25 October 2026 (about 51.8%) after running on sovereignty against US tariffs and sanctions; Xi congratulated Lula on 27 October; no US statement was found by 28 October (search extracts). A 25% US Section 301 tariff on most Brazilian goods has applied since 22 July 2026, after a May 2026 White House meeting brought only a working group."),
    ("Aircraft spared, Brazil's least", "Civil aircraft were exempt from the 2025 40% tariff on Brazil and from the 2026 Section 301 and forced-labour tariffs. But from April 2025 to February 2026 Brazilian jets still paid the 10% baseline on their non-US content (US airlines paid it on commercial jets; Embraer paid $80M on business jets and parts), while deals with the EU, the UK and Japan had put their aircraft back to zero: Embraer \"was the only manufacturer to pay tariffs on aircraft exports\" (its chief executive, March 2026). The Supreme Court struck the emergency tariffs down on 20 February 2026. A July 2026 Section 232 finding says aircraft imports \"threaten to impair\" US national security and keeps tariffs possible (reported); Embraer had already kept a tariff assumption in its 2026 guidance pending the investigation (May 2026)."),
    ("A narrowbody loses Embraer's defence", "Embraer's US case rests on its US ties (more than 40% US content; $21B of US purchases against $13B of exports to the US over five years) and on jets the US does not build; a 737-class jet would compete head-on with Boeing. The Bombardier precedent: Commerce set duties of 292% on the CSeries in 2017; Airbus took control and planned US assembly in October 2017; the trade commission cancelled the duties 4-0 in January 2018 because Boeing had lost no sale."),
    ("Still allied, and tied in", "Brazil remains a Major Non-NATO Ally (2019; no revocation found); North America is 58.7% of Embraer's revenue; the government holds a golden share that can veto a change of control; Brazil's development bank BNDES approved about R$9.6B a year for Embraer in 2023-25, mostly export credit."),
]
PRICE_FACTS = [
    ("The average moves a few percent", "Irwin and Pavcnik estimate aircraft price-cost margins of about 14-17% and a 3.7% price rise after the 1992 US-EU subsidy rules; in their simulation of the A380's entry, rival prices moved only a few percent (wide-body data; abstracts only)."),
    ("Contested deals go much deeper", "Bombardier sold CS100s to Delta at close to two-thirds off list and booked a $492M loss on its 127 launch orders; Boeing sold United 737-700s at an estimated $22M, about 73% off list, to keep the CS100 out; JetBlue paid an estimated 66-72% off for A220s against the E2 (Moody's); Brazilian export finance gave Embraer a 13-15% edge over Bombardier's CRJ."),
    ("Before service, not after", "The neo/MAX price war began at the 2010-11 launches, 5-6 years before either entered service."),
    ("The makers see it coming", "Airbus's FY2025 Board Report: \"the period of a duopoly in the mainline commercial aircraft market has ended\". But slots are scarce: Boeing's CFO saw \"a better pricing environment\" in March 2026, partly because \"there's minimal slots available\", which argues for the low end while backlogs stay long. Embraer's commercial margin was 2.5-2.7% in 2024-25 and it says \"we don't sell our aircraft below cost\" (2024)."),
    ("Airlines want a third", "71% of 492 respondents (45% of them airlines) to an Aviation Week/Bank of America survey would buy an Embraer narrowbody on its merits; United's chief executive: \"we need more competition\"; Ryanair's: playing two makers against each other is \"doomed to failure\". The trade commission found the CSeries unlikely to depress prices generally."),
]
PRECEDENTS = [
    ["767 (1978)", "Aeritalia and a Japanese consortium (CTDC)", "about 10% each of the airframe; paid back with supply contracts", "Christian Science Monitor, 1983"],
    ["777 (1991)", "Mitsubishi, Kawasaki, Fuji (JADC, the Japan Aircraft Development Corporation)", "21% of the airframe and of the risk capital; a state bank lent ¥60B, 60% of their share", "MHI; FlightGlobal"],
    ["787 (2005)", "Mitsubishi, Kawasaki, Fuji; Alenia; Vought", "about 35% of the structure in Japan; state loans sought for 70% of the Japanese part, $1.6-2B reported", "FlightGlobal; Seattle Times, 2005"],
    ["777X (2014)", "Japanese partners", "about 21% of the major structure", "Boeing, 12 June 2014"],
    ["A350 (2006-09)", "risk-sharing suppliers; four governments", "a target of about 16% from partners (€1.8B of €11B) and about 29% pledged as state launch loans", "FlightGlobal; UK government"],
    ["CSeries/A220 (2016-20)", "Quebec; then Airbus", "Quebec $1B for 49.5%; Airbus took 50.01% for no cash; Quebec at 25% since 2020, with write-downs reported", "Airbus; BNN Bloomberg"],
    ["Embraer (1990s)", "risk-sharing partners and suppliers", "about 43% of the development bill; Embraer itself about a third, Brazilian loans about a quarter", "Flight International"],
    ["SpaceJet (2008-23)", "Mitsubishi, with state support", "about ¥1 trillion (about $7.6B) spent; cancelled in February 2023 with no delivery", "MHI, 7 February 2023"],
    ["Spirit AeroSystems (2005, 2024)", "Boeing's own Wichita plant, sold and bought back", "sold to Onex in 2005; bought back in an all-stock deal of about $4.7B ($8.3B with debt) agreed in 2024", "Boeing, Q2 2024 call"],
    ["Boeing-Embraer (2018-20)", "Boeing buying in", "$4.2B for 80% of Embraer's commercial business; Boeing walked away in April 2020 and paid $150M in 2024", "Embraer filings"],
]
PARTNER_RETURNS = ("Partners have not done well, and Boeing has bought them back: it paid $590M in cash and released $416M of advances for Vought's 787 plant in 2009 (Boeing's 10-K), "
                   "bought Alenia out of Global Aeronautica the same year, and agreed in 2024 to buy back Spirit AeroSystems, the Wichita business it sold in 2005, in an all-stock deal of about $4.7B ($8.3B with debt). "
                   "Leonardo's aerostructures unit, which builds 787 barrels, was reported losing €129M in the first nine months of 2024. The structure shares (21% of the 777, about 35% of the 787) are shares of the airframe, not of the whole bill, and the A350's €1.8B was a target.")


def build(out_path):
    s0, se, sl, sh = (S[(w, 1, R10)][0] for w in ("as played", "Embraer base", "Embraer low", "Embraer high"))
    s8, se8 = S[("as played", 1, R8)][0], S[("Embraer base", 1, R8)][0]
    sx, sx8 = S[("expected", 1, R10)][0], S[("expected", 1, R8)][0]
    s_pd8 = S[("expected, partly deterred", 1, R8)][0]
    ue, ua = U["Do Nothing|Embraer base"], U["Do Nothing|as played"]
    pe3 = PP("Embraer base", 0.03)
    p8a, p8b = PP("as played", 0.03, rt=R8), PP("as played", 0.07, rt=R8)
    tiles = [
        ("An Embraer-Korea airliner", "talks, not a programme", f"Korea's president proposed building a next-generation airliner with Embraer (July 2026) and KAI and Embraer signed a non-binding memorandum; Embraer has not chosen a segment. Base: a {PLT} chance of a launch by about 2032 ({PLNT} if Boeing waits, {PLBT} if it launches in 2030), in service in {EIS_B}."),
        ("If it launches: the 2030 fps at 10.5%", bp(TOTAL, 1), f"against Do Nothing: {bp(COMP, 1)} as a competitor (its price cut and the customers it wins), {bp(LINE, 1)} back because its line is smaller than the game's own entrant. The premium Boeing would need rises from {bp(s0, 1, False)} to {bp(se, 1, False)}."),
        ("A 2030 launch to keep it out", "worth little", f"at the evidence's chances the premium needed is {bp(s_pd, 1, False)} at 10.5%, against {bp(s0, 1, False)} as played; only if Embraer were certain to launch otherwise would it fall to {bp(s_det, 1, False)}."),
        ("Partner share of the bill to launch in 2030", f"{MF.cut_pct(pp3[0])[:-1]}–{MF.cut_pct(pp7[1])}", f"at 10.5%, for a partner whose money costs 3-7%, across the readings of the CEO's rule; none up to 60% at Boeing's own rate. Japan's 787 package would be about 8% of the bill today, Korea's perhaps 3%. At 8.1%: {MF.cut_pct(p8a[0])[:-1]}–{MF.cut_pct(p8b[1])}."),
    ]
    tiles_html = '<div class="tiles">' + "".join(f'<div class="panel tile"><div class="k">{esc(k)}</div><div class="v">{esc(v)}</div><div class="d">{esc(d)}</div></div>' for k, v, d in tiles) + "</div>"
    n_find = sum(len(t["research"]["findings"]) for t in RS["tracks"].values())
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Embraer and Partners</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{K.CSS + CSS_EXTRA}</style></head><body><div class="wrap">
<header class="top"><p class="eyebrow">Boeing Product Development · war game rerun · MAX phase-out world · BOEING PROPRIETARY</p>
<h1>Embraer as a third maker, and a partner for the fps bill</h1>
<p class="lede">Two questions. South Korea has proposed building a next-generation airliner with Embraer, and Brazil's government is at odds with Washington: what does a competent third maker,
competing on price, do to Boeing's fps decision? And, separately, could Boeing close the bill with a partner? Both are priced here inside Boeing's own decision rule, before the game is re-run.</p>
<p class="gloss"><b>Basis.</b> The franchise page's view (the brief plus continuing value, services, overhead, widebody erosion and closing costs), constant 2026 $B against Do Nothing, in the columns the CEO
expected each round, at the game's 10.5% and at 8.1%. Where premiums are shown, the politics page's base government terms are on as well. Rivals' moves are held as the game played them; Embraer is priced through the game's own
supply-and-demand engine (who buys whose airplane, year by year) and a price cut on every new single-aisle delivered. With Embraer off, every value, premium and government share here equals the politics page's.
<b>The game as played</b> already has an unnamed third maker: an entrant in service in 2040 at up to 20 a month that sells only to customers Boeing and Airbus cannot serve. Here Embraer-Korea takes its place, with a smaller line that also competes.
<b>Readings:</b> where a range is shown it spans the four readings of the CEO's rule on the main report (strictly; pairwise; worst column first; and with the CEO's $2B allowance, the leeway to pick a plan up to $2B below the best one). A fifth, a CEO who anticipates the Board and proposes only what it would approve, is named where it differs.
<b>Premium:</b> the non-financial value the Board would need to put on staying in the business for its rule to launch an fps (the politics page's measure).
<b>NGSA:</b> Airbus's next single-aisle, launched in 2030 and in service in 2037 in the game.</p></header>
<section style="margin-top:18px">{tiles_html}</section>

<section><h2>The answer</h2><div class="bl">
<div class="panel"><div><b>Embraer-Korea is a possible third maker, and Brazil is at odds with Washington</b>
Korea's president proposed building a next-generation airliner with Brazil in July 2026, and KAI and Embraer signed a first, non-binding memorandum on aerostructures. Embraer says it is studying either a commercial jet or a business jet, with no segment or timeline chosen;
Korea calls the talks very early, and its main track is a core role on Boeing's and Airbus's next airplanes. Lula, re-elected on 25 October, has been in a tariff fight with Washington all year, and a US national-security finding on aircraft imports keeps tariffs on an Embraer narrowbody possible.
This page takes a {PLT} chance of an Embraer-Korea airliner ({PLNT} if Boeing waits, {PLBT} if Boeing launches in 2030), in service in {EIS_B} at up to {PEAK_B:.0f} a month.</div></div>
<div class="panel"><div><b>If Embraer launches, it hurts the fps more than Do Nothing, mostly through the customers it wins and the prices it cuts</b>
In 2030 at 10.5% the 10-year fps at Renton falls from {b(G['as played'])} to {b(G['Embraer base'])} against Do Nothing. As a competitor Embraer costs it {b(COMP)}: the customers it wins {b(SHARE)} alone, a 2% cut in single-aisle prices (2.6% on the MAX while Boeing has no new airplane) {b(PRICEC)} alone.
Its line is smaller than the game's own entrant, which gives {b(LINE)} back. In Do Nothing, Boeing's factories are already the limit and the MAX is running out, so Embraer sells mostly to customers Airbus would have had (in 2050 Airbus delivers {MF.n0(ua['2050']['airbus'] - ue['2050']['airbus'])} fewer, Boeing {MF.n0(ua['2050']['boeing'] - ue['2050']['boeing'])} fewer);
with an fps it competes for the fps's customers and cuts the price of every fps sold. The premium Boeing would need rises from {b(s0, 2, False)} to {b(se, 2, False)} ({b(sl, 2, False)} and {b(sh, 2, False)} in the low and high cases); at 8.1% from {b(s8, 2, False)} to {b(se8, 2, False)}, turning a near-launch into a no.
In 2026 money the effect shrinks in later rounds, but in each round's own money it stays at about {bp(min(dy), 1, False)}-{bp(max(dy), 1, False)}. Weighted by the {PLT} chance, the 2030 premium is {b(sx, 2, False)} at 10.5% and {b(sx8, 2, False)} at 8.1%.</div></div>
<div class="panel"><div><b>A 2030 launch to keep Embraer out is worth little at the chances the evidence gives</b>
Embraer would bet the company on a gap: a 737 at the end of its life and no new Boeing airplane. Korea's support for Embraer is put at 12% if Boeing launches in 2030 and 45% if it waits (research, judgement), which makes Embraer's chance about {PLBT} and {PLNT}.
At those chances the premium Boeing would need in 2030 is {b(s_pd, 2, False)} at 10.5%, against {b(s0, 2, False)} as played, and {b(s_pd8, 2, False)} at 8.1% (against {b(s8, 2, False)}); if a launch kept Embraer out altogether, {b(s_ed, 2, False)} at 10.5%. Only if Embraer were certain to launch otherwise
would it fall to {b(s_det, 2, False)} at 10.5% (where the fps is worth {b(G['deterred'])} against Do Nothing) and launch the 10-year fps at 8.1% with no premium at all. So Embraer is a modest reason to launch early, not a decisive one; it works only in 2030, as by 2035 Embraer has decided.</div></div>
<div class="panel"><div><b>At 10.5% no partner package with any precedent closes the bill; at 8.1% a modest one does</b>
A partner that carries part of the bill and takes back a share of the fps's profit helps Boeing in two ways: the game's debt penalty falls (a partner carrying 30% of the bill saves Boeing about {b(DEBT, 1, False)} in 2030 even at Boeing's own rate),
and a partner whose money is cheaper than Boeing's values the fps's long, late profits more. In 2030 at 10.5% a partner whose money costs 3% must carry {share_txt(pp3)} of the bill, at 7% {share_txt(pp7)}; at Boeing's own rate no share up to 60% launches; in 2035 it takes {share_txt(PP('as played', 0.03, n=2))} at 3%, and from 2045 none up to 60%. If Embraer launches anyway, {share_txt(pe3)} at 3%.
Precedent sets the size: in dollars Japan's 787 package would be about 8% of an fps bill today, and Korea's firms could add about 3% (judgement). At that scale (11% at about 6%) a partner closes the 2030 bill at 8.1%, not at 10.5%. At 10.5% even a 35% state-loan package (about four times Japan's 787 package) launches the 7-year fps only with the CEO's $2B allowance or a CEO anticipating the Board.
And these are break-even terms for the partner: it takes back {min(SP.values()):.2f}-{max(SP.values()):.2f} of a pro-rata share of the profit, where precedent is about 0.7-1.2. On pro-rata terms (a 20% or 35% package taking the same share of the profit) nothing launches at 10.5%; the repo's own Joint Venture terms (35% of the bill for 25% of the profit) launch the fps at 8.1%.</div></div>
<div class="panel"><div><b>The two together: Korea as Boeing's partner, not Embraer's</b>
Korea wants a core, risk-sharing role on the next Boeing or Airbus airplane, and it is Embraer's most likely partner; Embraer said in 2016 that it would go bigger only if Boeing and Airbus gave up part of the market. A Boeing package that gives Korea (with Japan) that role carries part of the bill and lowers Embraer's chance of launching.
At the evidence's chances the second effect is small: in 2030 at 10.5% the share needed falls only from {share_txt(pp3)} to {share_txt(pw3)} at 3%. Only if Embraer were certain to launch otherwise does it fall to {share_txt(pd3)}, and then a 35% state-loan package launches the fps.
The risks are the ones Boeing knows: partners who lose money and are bought back, Airbus courting the same partners for its own 2030 launch, Lula's Brazil, and the memory of 2020, when Boeing walked away from Embraer.</div></div>
<div class="panel"><div><b>For the re-run: the engine is ready, the game is not re-run</b>
Embraer-Korea's second-source share and the price cut are new options in the game's engine (off unless set; every existing test and the played game's replay unchanged); its line uses the game's existing entrant settings. The base settings are ready in data/sd_options_embraer_proposed.json.
The game has no move for Boeing to sign partners: "fps via Embraer" carries a $100B bill on the board. A partner move would be a new order.</div></div>
</div></section>

<section><h2>Embraer and Korea: what is public</h2><div class="two">
<div class="panel"><p class="ctitle">Embraer and Korea</p>{cards(EMB_FACTS)}</div>
<div class="panel"><p class="ctitle">Brazil and Washington</p>{cards(BRAZIL_FACTS)}</div>
</div></section>

<section><h2>How Embraer enters the game</h2><div class="stack">
<div class="panel"><p>Two channels, both through the game's own rules. <b>Customers:</b> Embraer-Korea wins a share of each year's new customers (after COMAC's home market), up to what its line can build: more while Boeing has no new narrowbody in service, when it is the only Western alternative to Airbus, less once an fps is. Like the game's own entrant, it also sells to customers nobody else can serve. The rest are split between Boeing and Airbus as before, and every plan, the status quo included, is re-delivered year by year.
<b>Prices:</b> its campaigns cut the price of every new single-aisle delivered, Boeing's and Airbus's, by a market-average share at full effect, more on Boeing's MAX while Boeing has no new airplane; costs do not change, so profit falls by the whole cut. The status quo faces the same cuts, so only what an fps adds or loses against it counts.</p>
{inputs_table()}
<p class="cap">Embraer's inputs; the base settings are what the research's check suggested where it differed (a 20% launch chance rather than 35%, in service 2040, 8 a month). A 2% price cut takes $1.1M of an fps's $14.1M profit, and $1.0-1.2M of a 737 MAX's $3.8M (a quarter to a third, at 2-2.6%) on the game's margins.</p></div>
<div class="panel"><p class="ctitle">Price: what a third maker has done before</p>{cards(PRICE_FACTS)}</div>
</div></section>

<section><h2>What Embraer does to Boeing's decision</h2><div class="stack">
<div class="panel"><p class="ctitle">In 2030, an Embraer launch costs the fps about {b(-TOTAL, 1, False)} against Do Nothing at 10.5%; keeping it out is worth little at the evidence's chances</p>
<div class="legend"><span><i class="sw" style="background:var(--s1)"></i>at 10.5%</span><span><i class="sw" style="background:var(--s2)"></i>at 8.1%</span><span>the 10-year fps at Renton against Do Nothing, PV at 2026</span></div>
<div class="cw only-wide">{fps_chart()}</div><div class="cw only-narrow">{fps_chart(True)}</div>
<p class="cap">The franchise view, without the politics page's government terms. The chance-weighted rows weight the worlds with and without an Embraer airliner; where a Boeing launch lowers the chance, the fps plans see the lower one and Do Nothing the higher. "Certain to launch unless Boeing launches first" is a bound, not a forecast.</p></div>
<div class="panel">{effect_table()}
<p class="cap">Columns: the game as played; Embraer launches (base, then the low and high cases); a {PLT} chance it launches whatever Boeing does; {PLNT} if Boeing waits and {PLBT} if it launches in 2030; {PLNT} if Boeing waits and none if it launches; Embraer certain to launch unless Boeing launches first (a bound). "None": no premium up to $60B launches an fps. "Decided": Boeing decides in 2030 before Embraer does; by 2035 Embraer has launched or not, so the chance-weighted and kept-out cases apply to 2030 only.</p></div>
<div class="panel"><p class="ctitle">Embraer takes mostly from Airbus, with or without an fps; with one it also takes from Boeing</p>{units_table()}
<p class="cap">Deliveries a year in the CEO's 2030 column (Airbus launches NGSA), from the game's engine, as played (with its own overflow-only entrant) and with Embraer-Korea (base). In Do Nothing Boeing's MAX is limited by its factories and phased out from 2045, so Embraer's sales come mostly from Airbus; the game's larger entrant also takes overflow customers who would otherwise wait for Boeing's fps.</p></div>
</div></section>

<section><h2>A partner for the bill</h2><div class="stack">
<div class="panel"><p class="ctitle">How airframers have shared development bills</p>{ctable(["Programme", "Partners", "What they carried", "Source"], [[esc(a), esc(b_), esc(c), esc(d)] for a, b_, c, d in PRECEDENTS], txt_cols=(1, 2, 3))}
<p class="cap">{esc(PARTNER_RETURNS)}</p></div>
<div class="panel"><p class="ctitle">Who could partner Boeing</p>{cards(CANDIDATES)}</div>
<div class="panel"><p>A partner pays share p of the fps bill and takes back share s of the fps's operating profit, after any price cut, for as long as the view counts the fps (its 50 years in service here).
s is set where the partner breaks even at its own cost of money in the CEO's expected columns, so the partner carries the risk of the other columns. The partner's money is booked at entry into service, as the game books Boeing's bill. Boeing keeps the game's own saving on the bill, debt penalty included, and gives up s of the profit.
A partner sees the fps's own return; Boeing sees only what the fps adds over the MAX after its debt penalty. On pro-rata terms a partner would earn about {pct(PR_RATE, 0)} if its money is counted at entry into service, as the game counts Boeing's, and about {pct(PR_SPREAD, 0)} if it is spent over the development years: above or close to the 7% the research puts on a state-backed partner, below Boeing's 10.5%.</p></div>
<div class="panel"><p class="ctitle">In 2030 at 10.5% a partner whose money costs 3-7% must carry a third to a half of the bill</p>
<div class="legend"><span><i class="ln" style="background:var(--s1)"></i>the game as played</span><span><i class="ln" style="background:var(--s2)"></i>Embraer launches (base)</span><span><i class="ln" style="background:var(--s3)"></i>chance-weighted ({PLNT} if Boeing waits, {PLBT} if it launches)</span><span>open circle: no share up to 60% launches</span></div>
<div class="cw only-wide">{partner_chart()}</div><div class="cw only-narrow">{partner_chart(narrow=True)}</div>
<p class="cap">Smallest share of the fps bill a partner must carry for Boeing's rule to launch an fps in 2030 at 10.5%, by the partner's own cost of money (the low end across the readings of the CEO's rule; the anticipating reading is lower still). The franchise view. 2% is below any rate the research found for a partner.</p></div>
<div class="panel">{partner_table()}
<p class="cap">Share of the bill, across the four readings of the CEO's rule; "over 60%": no share up to 60% launches. At 8.1% the partner's rate is deflated the same way as Boeing's. With the politics page's government terms on, about 2% of the bill is already carried by government.</p></div>
<div class="panel"><p class="ctitle">Packages partners could plausibly put up</p>{packages_table()}
<p class="cap">Each partner breaks even at its own cost of money on the fps's profit in the CEO's 2030 column; the franchise view. Japan at its 787 scale (about 8% at about 5.5%) plus Korea (about 3% at about 7%): research estimates in dollars, judgement. A large Asian package: 15% and 6%. A 35% state-loan package is about four times Japan's 787 package in dollars; the 35% structure share Japan took on the 787 was a share of the airframe, not of the bill.</p></div>
<div class="panel"><p class="ctitle">Set terms</p>{fixed_table()}
<p class="cap">Partner's return: the rate at which the terms break the partner even on the fps's profit in the CEO's 2030 column, with its money counted at entry into service or over the development years. The repo's original war game (wargame/config/default.json) gave an Embraer Joint Venture the first terms, with half the two-front strain relieved too (no solo fps plan carries strain in 2030).</p></div>
</div></section>

<section><h2>For the game's re-run</h2><div class="panel">{proposed_table()}
<p class="cap">Not played. The engine options are tested to change nothing when they are not set (test_embraer_options.py), and the played game's replay is unchanged.</p></div></section>

<section><h2>Notes</h2><div class="panel"><ul class="cav">
<li><b>What is not modelled.</b> Airbus's response (a cheaper NGSA, or its own Korean or Japanese partners): rivals' moves are held as played. Embraer-Korea is priced as one launch with a chance, not as a player choosing. US trade action against an Embraer narrowbody (some action about 50% likely, a block about 8%, per the research) is inside the share range, not modelled separately. A launch-period price war, deeper but temporary, is not modelled.</li>
<li><b>Price.</b> The cut is a market average on every delivery, from {EJ['price_options']['base']['from']} at base, at full effect after {EJ['price_options']['base']['ramp_years']} years. Campaigns where Embraer bids would see far more; the many it does not bid in, less. In the high case the larger cut on the MAX while Boeing has no new airplane partly favours the fps, which escapes it.</li>
<li><b>Partners.</b> Partner money is valued at the partner's own rate; nothing here prices the strategic value a government puts on the work (jobs, a wing), which is what has let state-backed partners accept low returns. The game's debt penalty is what makes Boeing's balance sheet bind; a partner's balance sheet is outside it.</li>
<li><b>Checks.</b> With Embraer off, every value equals the politics page's to {EJ['checks']['no_embraer_equals_politics']:.0e} and every premium and government share to the cent; the engine's price rule and this page's give the same value to {EJ['checks']['price_rule_engine_vs_overlay']:.0e}; a partner at Boeing's own rate leaves Boeing exactly the debt-penalty saving (plus a few million of two-front strain on the plans beside the Re-engine). An independent review of the model and the page was run and its findings fixed.</li>
<li><b>Sources:</b> {n_find} findings from five research tracks, each followed by a verifier, in data/embraer_research.json. The verifiers could not open web pages (the session's search budget ran out and many hosts did not resolve), so they checked what they could against the Boeing and Embraer call transcripts, 10-Ks and Airbus's Board Report in the repository: {VERD['confirmed']} findings confirmed, {VERD['corrected']} corrected (the corrections are used here), {VERD['unverifiable']} could not be checked.
Embraer's and Boeing's own statements quoted here are confirmed there; the Korean, Brazilian-election and US-tariff facts dated 2026 and the price and partner-package estimates rest on search extracts and judgement, and are reported, not verified.</li>
<li><b>Files:</b> embraer.py writes data/embraer.json and data/sd_options_embraer_proposed.json; make_embraer_html.py builds this page and asserts its claims against them.</li>
</ul></div></section>
<footer>BOEING PROPRIETARY. Built by make_embraer_html.py from run dash-2050-phaseout.</footer></div>
<script>{K.JS}</script></body></html>"""
    text = re.sub(r"<svg.*?</svg>|<style>.*?</style>|<script>.*?</script>", " ", page, flags=re.S)
    for bad in ("Milk", "Sabotage", "C3_", "c_gov", "exit_p", "H8", "share_fps", "entrant_share", "787-style"):
        assert bad not in text, bad
    m = re.search(r"\b(he|she|his|her|hers|him|himself|herself)\b", text, re.I)
    assert not m, text[m.start() - 80:m.end() + 20]
    with open(out_path, "w") as f:
        f.write(page)
    print("wrote", out_path, len(page))


CSS_EXTRA = MF.CSS_EXTRA + """
.two { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
@media (max-width: 900px) { .two { grid-template-columns: 1fr; } }
.chart .endlab { fill: var(--fg); font: 500 12px var(--font-body); }
"""
CANDIDATES = [
    ("Japan", "Boeing's partner for four decades: about 10% of the 767, 21% of the 777's airframe and risk capital, about 35% of the 787's structure and about 21% of the 777X's, through JADC, with state loans for 60-70% of their part. In dollars the 787 package was about $2.3-2.9B (2005), about 8% of an fps bill today (4-15%). Japan's own airliner, the SpaceJet, ended in February 2023 after about ¥1 trillion and no delivery; Japan committed to 100 Boeing aircraft in its 2025 US trade deal."),
    ("Korea", "Korea's space agency launched a task force on 16 July 2026 to win core risk-sharing roles on the Airbus and Boeing successors (a target of up to 135 trillion won of orders over 20 years from 2035). KAI ($2.6B revenue) builds 737NG wing parts, 777X wing ribs and A320 and A350 parts; Korean Air builds 737-787 structures; Hanwha is a partner on Pratt & Whitney's GTF. Its share of an fps bill: about 3% (1-8%). The research puts the chance Korea backs Embraer rather than Boeing at 25%: 12% if Boeing launches in 2030, 45% if it has not by 2035 (judgement)."),
    ("Embraer itself", "Not as Boeing's supplier: \"we do not contemplate any architecture where Embraer will be a sub-supplier ... or a major risk-sharing partner\" (2011), though it agreed to Boeing's 80% joint venture in 2018. In 2016 it said it would go bigger only if Boeing and Airbus \"give up a little bit of this market\", the condition the MAX phase-out creates; since 2025 it studies larger airplanes without that condition. Brazil's golden share can veto a change of control, and Boeing walked away from the last deal."),
    ("Boeing's own stance", "The next airplane \"could require different kind of business partnerships, different type of ventures\" (Ortberg, 28 July 2026). But Boeing has pulled core IP back since the 787 (\"we paid people to develop IP that they now own\", 2011) and built the 777X wing itself, which limits what it would hand a partner."),
    ("Airbus wants the same partners", "Airbus plans to pick the NGSA's engine in 2027, launch around 2030 and enter service in 2037-38: it will be signing risk-sharing partners when Korea's task force is looking for a role, and KAI and Korean Air already build A320 and A350 parts."),
    ("Not researched", "Saudi Arabia's PIF, Turkey, India, Italy's Leonardo and the UK were named in 2024 reports on Embraer's search for partners or are past Boeing and Airbus partners; the research ran out of search budget before reaching them."),
]

if __name__ == "__main__":
    build(os.path.join(HERE, "fps_embraer.html"))
