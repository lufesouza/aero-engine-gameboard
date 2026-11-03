"""Build fps_politics.html: jobs and Washington, Boeing's brand as an engineering company, China and Brazil in Boeing's
fps decision in the MAX phase-out game. How Boeing has behaved under such pressure, what can be sized as cash, and the
non-financial weight the Board would need to put on staying in, against what Boeing has actually paid for such
reasons.

Reads data/politics.json (politics.py), data/franchise.json (franchise.py), data/politics_research.json (209 sourced
findings, the design and two adversarial checks). Every figure comes from those files; the claims in the copy are
asserted below.

  python3 make_politics_html.py
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
PJ = json.load(open(os.path.join(HERE, "data", "politics.json")))
RS = json.load(open(os.path.join(HERE, "data", "politics_research.json")))
W, WC = PJ["worlds"]["base"], PJ["worlds"]["comac takes china"]
YEAR = {int(n): r["year"] for n, r in W.items()}
R10, R8 = "10.5%", "8.1%"
MODES = ("rule", "pairwise", "worst_first", "premium")
TEN, SEVEN, TEN_NEW = MF.TEN, MF.SEVEN, MF.TEN_NEW
RATE = {R10: 0.105, R8: 1.105 / 1.022 - 1}


def case(n, key, rate, world=W):
    return world[str(n)]["cases"]["%s|%s" % (key, rate)]


def s_rng(n, key, rate, reading="as played", world=W, dy=False):
    """Low and high of the premium needed across the readings of the CEO's rule (None: no premium launches)."""
    c = case(n, key, rate, world)["readings"][reading]
    xs = [v["S_decision_year" if dy else "S"] for v in c.values()]
    if all(x is None for x in xs):
        return None
    xs = [x for x in xs if x is not None]
    return min(xs), max(xs)


def s_txt(r_, dp=1):
    if r_ is None:
        return "none"
    a, z = (bp(x, dp, False) for x in r_)
    return a if a == z else f"{a}–{z[1:]}"


def plan_of(n, key, rate, reading="as played", world=W):
    return case(n, key, rate, world)["readings"][reading]["rule"]["plan"]


BASE = "base|full|cash base"            # the brief, all franchise terms, base cash-like terms
ITEM = lambda n, rate, plan, world=W, view="full": world[str(n)]["items"]["%s|%s" % (view, rate)][plan]

# ─────────────────────────────── the claims, asserted ───────────────────────────────
assert PJ["decide2_checked"] >= 900                                     # the rule as re-implemented gives back every stored decision
assert PJ["cash"]["c_gov"]["base"] == 0.02 and PJ["cash"]["exit_p"]["base"] == 0.2
# the franchise page's 2030 numbers are this page's starting point
assert abs(ITEM(1, R10, TEN) - (MF.G10 + MF.F10)) < 1e-9 and abs(ITEM(1, R10, "Re-engine") - 3.30) < 0.005
S = {(n, rt): s_rng(n, BASE, rt) for n in (1, 2, 3, 4) for rt in (R10, R8)}
SY = {(n, rt): s_rng(n, BASE, rt, dy=True) for n in (1, 2, 3, 4) for rt in (R10, R8)}
CUT = {(n, rt): tuple(case(n, BASE, rt)["cut_needed"]) for n in (1, 2, 3, 4) for rt in (R10, R8)}
HI = {(n, rt): s_rng(n, "high|full|cash high", rt, dy=True) for n in (1, 2, 3, 4) for rt in (R10, R8)}
LO = {(n, rt): s_rng(n, "low|full|cash low", rt, dy=True) for n in (1, 2, 3, 4) for rt in (R10, R8)}
DFL = {(n, rt): case(n, BASE, rt)["deflated_tests"] for n in (1, 2, 3, 4) for rt in (R10, R8)}
X = {(n, rt): case(n, BASE, rt)["exit_cost_pv"] for n in (1, 2, 3, 4) for rt in (R10, R8)}
S0 = {(n, rt): s_rng(n, "base|full|cash low", rt) for n in (1, 2, 3, 4) for rt in (R10, R8)}
# at 10.5% the premium needed falls with each round in today's money but rises in the decision year's money
assert S[(1, R10)][0] > S[(2, R10)][0] > S[(3, R10)][0] > S[(4, R10)][0] > 2.0
assert SY[(1, R10)][0] < SY[(2, R10)][0] < SY[(3, R10)][0] < SY[(4, R10)][0]
# the cash-like terms lower it a little
assert all(S[(n, R10)][0] < S0[(n, R10)][0] for n in (1, 2, 3, 4)) and S0[(1, R10)][0] - S[(1, R10)][0] < 1.0
assert all(X[(n, rt)] < 0.25 for n in (1, 2, 3, 4) for rt in (R10, R8))
# the Board's rating test on cash only: no premium launches at 10.5% in 2030-2045; it does in 2050
for n in (1, 2, 3):
    assert s_rng(n, BASE, R10, "cash rating") is None
assert s_rng(4, BASE, R10, "cash rating") is not None
assert all(s_rng(n, BASE, R8, "cash rating") is None for n in (3, 4)) and all(s_rng(n, BASE, R8, "cash rating") is not None for n in (1, 2))
# at 8.1% in 2030 the premium is small, within the CEO's $2B allowance; a CEO who anticipates the Board's veto of the 787
# Re-engine alone launches the 7-year fps with no premium at all, and no co-funding or cost of leaving either
assert SY[(1, R8)][1] < 1.0 and s_rng(1, BASE, R8, "cash rating") == S[(1, R8)]
S0_8 = S0[(1, R8)][0]
assert 1.3 < S0_8 < 1.45 and 0.8 < S0_8 - S[(1, R8)][0] < 0.95
E7 = MF.item(1, "base|8.1%", SEVEN, "game") + MF.terms_sum(1, "base|8.1%", SEVEN, "full")
assert 2.0 < E7 < 2.2
assert s_rng(1, BASE, R8, "anticipating") == (0.0, 0.0) and plan_of(1, BASE, R8, "anticipating") == SEVEN
assert s_rng(1, "base|full|cash low", R8, "anticipating") == (0.0, 0.0) and plan_of(1, "base|full|cash low", R8, "anticipating") == SEVEN
# the premium solved on the rule as played launches the 10-year fps on new sites in 2030, the 10-year at Renton later
assert plan_of(1, BASE, R10) == TEN_NEW and all(plan_of(n, BASE, R10) == TEN for n in (2, 3, 4))
# the government share of the bill that would launch (across the four readings), against US practice (about 2%)
assert 0.19 < CUT[(1, R10)][0] < CUT[(1, R10)][1] < 0.26 and 0.03 < CUT[(1, R8)][0] <= CUT[(1, R8)][1] < 0.04 and CUT[(4, R10)][0] > 0.75 and CUT[(4, R8)][0] > 0.5
# at 10.5% in 2030, $1.08B of the premium is the cost of beating the 787 Re-engine the CEO prefers and the Board vetoes
ANT30 = s_rng(1, BASE, R10, "anticipating")
ANT30Y = s_rng(1, BASE, R10, "anticipating", dy=True)
assert abs((S[(1, R10)][0] - ANT30[0]) - 1.08) < 0.01
# the high case changes the 10.5% verdict for 2030-35; the low case raises everything
assert HI[(1, R10)][1] < 3.0 and HI[(2, R10)][1] < 3.0 and HI[(3, R10)][0] > 5.0 and HI[(4, R10)][0] > 10.0
assert s_rng(1, "high|full|cash high", R10, "cash rating", dy=True) == HI[(1, R10)] and s_rng(2, "high|full|cash high", R10, "cash rating", dy=True) == HI[(2, R10)]
assert all(HI[(n, R8)][0] == 0.0 for n in (1, 2, 3, 4)) and LO[(1, R8)][0] > 7.0
# the Board's tests in decision-year money: no change in 2030 (the CEO's $1B margin binds there), lower in 2050
assert abs(DFL[(1, R10)]["S"] - S[(1, R10)][0]) < 1e-6 and DFL[(4, R10)]["S"] < S[(4, R10)][0]
BIZ50 = (1 + RATE[R10]) ** (2050 - 2026)          # the game's $1B business-case test, in 2050 money
assert 10.5 < BIZ50 < 11.5
# what Boeing has paid, in 2026 dollars (CPI to about 330): chosen up front, and absorbed after the fact
CPI26 = 330.0
LADDER = [("Commercial segments left or walked away from", 0.0, "757, 717, NMA, the 100-150-seat segment, Embraer: nothing paid to stay in",
           "B-1620, B-1666, B-1674, 10-K FY2020", "up front"),
          ("T-X and MQ-25 bids (2018)", 0.691 * CPI26 / 251.1, "$0.69B of pre-tax charges taken up front, by choice, to win two long-lived defence franchises: franchise logic, as in continuing value (the T-7A lost a further $1.8B in 2024)",
           "B-1458, BX-1545", "up front"),
          ("Keeping the 737 line through the 2020 suspension", 4.0 * CPI26 / 258.8, "about $4B of abnormal costs in 2020 money (the pre-COVID estimate) to keep the production system, labour and 600-plus suppliers: mostly ordinary value for a programme that would restart",
           "B-1650, B-1618, B-1675, B-1584", "up front"),
          ("747-8 kept through the 2008-09 losses", 3.1, "about $2.0B of reach-forward losses on contracted aircraft; \"I think this is a good product that serves a good market\" (McNerney, 2009): kept on product grounds, ended in 2023",
           "B-0143, B-0563, B-0192", "after the fact"),
          ("Air Force One (VC-25B), from 2018", 3.4, "a fixed-price deal accepted under presidential pressure; about $3.1B of losses to 2026. \"Risks that Boeing probably shouldn't have taken\" (Calhoun)",
           "BX-0314; 10-Ks FY2020-24; FQ2 2026 call", "after the fact"),
          ("KC-46 tanker, from 2014", 11.2, "about $9.1B of losses on a development bid at zero margin for \"a 50-, 60-year widebody franchise\"; \"I don't think we can walk away from these contracts\" (Ortberg, 2024)",
           "B-0918, BX-1033, B-2203; 10-Ks", "after the fact")]
TOP = max(x for _, x, _, _, k in LADDER if k == "up front")
assert 5.0 < TOP < 5.2 and 0.9 < LADDER[1][1] < 0.92
RATIO = (SY[(1, R10)][0] / TOP, SY[(4, R10)][0] / TOP)
assert all(SY[(n, R10)][0] > TOP for n in (1, 2, 3, 4)) and 1.5 < RATIO[0] < 1.7 and 4.8 < RATIO[1] < 5.3
KC46 = LADDER[-1][1]
assert SY[(1, R10)][0] < KC46 and SY[(2, R10)][0] < KC46 < SY[(3, R10)][0]
# the deliveries Boeing gives up when the MAX ends go to Airbus and the entrant, none to COMAC (who_picks_up.py)
WP = json.load(open(os.path.join(HERE, "data", "who_picks_up.json")))["effect_of_phase_out"]
assert abs(WP["comac"]) < 1e-9 and WP["airbus"] > 400 and WP["entrant"] > 400
# COMAC takes all of China's single-aisle demand: a stronger COMAC lowers the fps's value and raises the premium needed,
# even with the political cost of leaving raised (an assumption)
XC = case(1, BASE, R10, WC)["exit_cost_pv"] - X[(1, R10)]
assert 0.15 < XC < 0.2
for rt in (R10, R8):
    assert ITEM(1, rt, TEN, WC) < ITEM(1, rt, TEN) and ITEM(1, rt, TEN, WC, "game") < ITEM(1, rt, TEN, W, "game")
    assert s_rng(1, BASE, rt, world=WC)[0] > S[(1, rt)][0] and s_rng(2, BASE, rt, world=WC)[0] > S[(2, rt)][0]
assert PJ["comac_plan"]["2050"] == 360
# the framing: verified facts (sources in the notes)
FRAMING = {"mnna": "31 July 2019", "nss": "December 2025", "ieepa": "20 February 2026", "1260h": "January 2025"}


# ─────────────────────────────── chart: premium needed vs what Boeing has paid ───────────────────────────────
def ladder_chart(narrow=False):
    lo, hi = math.log10(0.1), math.log10(40.0)
    if narrow:
        w, left, right, rh, top = 400, 26, 12, 58, 80
    else:
        w, left, right, rh, top = 760, 120, 70, 46, 80
    rows = [(n, YEAR[n]) for n in (1, 2, 3, 4)]
    h = top + rh * len(rows) + 28
    sx = lambda v: left + (math.log10(max(v, 0.1)) - lo) / (hi - lo) * (w - left - right)
    out = [K.svg_open(w, h, "Premium Boeing would need to launch the fps, by round, against the premiums Boeing has paid", "chart narrow" if narrow else "chart")]
    for v in (0.1, 0.3, 1, 3, 10, 30):
        x = sx(v)
        out.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{top}" y2="{h - 24}" class="grid"/><text x="{x:.1f}" y="{h - 8}" text-anchor="middle" class="tick">{bp(v, 1 if v < 1 else 0, False)}</text>')
    refs = [(LADDER[1][1], "T-X/MQ-25 $0.9B, up front"), (LADDER[4][1], "Air Force One $3.4B, after"), (TOP, "737 line $5.1B, up front"), (KC46, "KC-46 $11.2B, after")]
    for i, (v, lab) in enumerate(refs):
        x = sx(v)
        anchor, dx = ("end", -4) if x > w * (0.5 if narrow else 0.8) else ("start", 4)
        out.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{12 + i * 16}" y2="{h - 24}" class="ref" stroke-dasharray="4 3"/>'
                   f'<text x="{x + dx:.1f}" y="{20 + i * 16}" text-anchor="{anchor}" class="reflab">{esc(lab)}</text>')
    for i, (n, yr) in enumerate(rows):
        y = top + i * rh
        txt = []
        for j, (rt, col) in enumerate(((R10, "var(--s1)"), (R8, "var(--s2)"))):
            v = SY[(n, rt)][0]
            t = bp(v, 1, False)
            txt.append(t)
            by = y + (22 if narrow else 8) + j * 15
            out.append(f'<rect x="{left}" y="{by:.1f}" width="{max(3.0, sx(v) - left):.1f}" height="10" rx="3" fill="{col}"/>')
            if not narrow:
                out.append(f'<text x="{sx(v) + 6:.1f}" y="{by + 9:.1f}" class="val sm">{esc(t)}</text>')
        if narrow:
            out.append(f'<text x="12" y="{y + 14}" class="rowlab sm">{yr} brief</text>'
                       f'<text x="{w - right}" y="{y + 14}" text-anchor="end" class="val sm">{esc(txt[0])} · {esc(txt[1])}</text>')
        else:
            out.append(f'<text x="{left - 10}" y="{y + 22}" text-anchor="end" class="rowlab sm">{yr} brief</text>')
        out.append(f'<rect x="0" y="{y}" width="{w}" height="{rh}" class="hit" {K.mark_attrs((f"{yr} brief", "", None), (txt[0], "at 10.5%, in " + str(yr) + " money", "var(--s1)"), (txt[1], "at 8.1%", "var(--s2)"))}/>')
    out.append("</svg>")
    return "".join(out)


# ─────────────────────────────── tables ───────────────────────────────
def needed_table():
    head = ["", "Premium, PV at 2026", "Premium, decision year's money", "Low / high cases, decision year's money", "Rating test on cash only, PV", "CEO anticipates the Board, PV", "Government share of the bill instead"]
    rows = []
    for rt in (R10, R8):
        rows.append(f"At {rt}")
        for n in (1, 2, 3, 4):
            cr = s_rng(n, BASE, rt, "cash rating")
            an = s_rng(n, BASE, rt, "anticipating")
            lh = f"{s_txt(LO[(n, rt)])} / {'$0' if HI[(n, rt)][0] == 0 else s_txt(HI[(n, rt)])}"
            cut = MF.rtxt(CUT[(n, rt)][0], CUT[(n, rt)][1], MF.cut_pct)
            rows.append([str(YEAR[n]), s_txt(S[(n, rt)], 2), s_txt(SY[(n, rt)]), lh, s_txt(cr, 2) if cr != S[(n, rt)] else "same",
                         ("$0 (" + esc(plan_of(n, BASE, rt, "anticipating").replace(" at Renton", "")) + ")") if an == (0.0, 0.0) else (s_txt(an, 2) if an != S[(n, rt)] else "same"),
                         cut])
    return ctable(head, rows, num_cols=(1, 2, 3, 4, 5, 6))


def ladder_table():
    rows = []
    for kind, title in (("up front", "Chosen up front"), ("after the fact", "Absorbed after the fact (not premiums Boeing chose)")):
        rows.append(title)
        rows += [[esc(a), b(v, 1, False) if v else "$0", esc(c), esc(d)] for a, v, c, d, k in LADDER if k == kind]
    return ctable(["What Boeing paid", "2026 prices", "What it bought", "Evidence"], rows, num_cols=(1,), txt_cols=(2, 3))


def comac_table():
    head = ["", "10-year fps at Renton against Do Nothing, the game's market", "COMAC takes China", "Premium needed for any fps (base government terms), the game's market", "COMAC takes China"]
    rows = []
    for rt in (R10, R8):
        rows.append(f"At {rt}")
        for n in (1, 2):
            rows.append([f"{YEAR[n]} brief", b(ITEM(n, rt, TEN)), b(ITEM(n, rt, TEN, WC)), s_txt(S[(n, rt)], 2), s_txt(s_rng(n, BASE, rt, world=WC), 2)])
    return ctable(head, rows, num_cols=(1, 2, 3, 4))


TERMS = [
    ("Government co-funding", "Cash: state siting incentives and federal technology money, as a cut in Boeing's share of the fps bill (the bill's debt penalty falls with it)",
     "2% of the bill (0 / 5%)",
     "No US airliner has had direct federal launch funding since the SST was cancelled in 1971; federal help has come as research money (in 2012 the WTO found that NASA and DoD research, about $2.6B in 1989-2006, helped Boeing develop the 787's technologies) and demonstrators such as NASA's X-66 ($425M, paused in 2025). Washington's 2013 package for the 777X ($8.7B on paper, about $1.5B in present value) and South Carolina's 2009 package ($450-900M) were won by site competitions. Boeing backed 'market terms' for all future support (2021, B-1825), and the WTO let the EU tariff about $4B a year of US goods over one Washington tax break (B-1761). Airbus-style launch aid (up to a third of a programme) is not US practice"),
    ("Political cost of leaving", "Cash-like goodwill: a chance that Washington makes Boeing pay for leaving, through defence, export finance or the FAA's rate approvals, on the plans without an fps. Charged in every round from 2045 (the brief's Do Nothing never launches), although only 2050 is a real exit; in the rating test as the game's rule is written, out of it in the rating-on-cash reading",
     "20% x $0.44B a year of defence profit for 20 years from 2045 (0 / 50% x $0.66B from 2040)",
     "Washington's leverage is real: 35-51% of Boeing's revenue came from the US government in 2020-25, the FAA sets the 737 rate cap, and in 2025-26 the administration sold Boeing jets in trade deals. But no precedent shows a penalty for a commercial product choice: Boeing's own exits, job cuts and moves out of Washington state passed without one. The size is judgement"),
    ("Strategic premium", "The weight the Board would put on staying in: identity as an engineering company, engineering talent, standing as the last US airliner maker (Washington's reaction to that standing is in the political cost of leaving). Added to every fps plan in every column and solved for the amount that launches",
     "Solved, then compared with what Boeing has paid",
     "Subjective by construction. It leaves out everything the franchise terms already count (continuing value, services, overhead, widebody erosion, closing costs)"),
    ("Not added", "Military 737s (P-8, E-7) after the line ends, Washington's help selling jets (both options keep it while the MAX sells), China market access (Boeing plans without China), a federal safety net under the Board's tests",
     "Zero",
     "Military 737s are worth about $0.03B today on this page's estimate (an assumed $0.15B a year of derivative profit for 10 years after 2060); Boeing took China out of its guidance in 2022 (B-1971, B-2052); it raised $25B of bonds rather than take CARES Act loans (BX-1636)"),
    ("Counter-weight", "The brand risk of launching and failing: the MAX crisis cost about $20B directly and halved Boeing's market value; the 787 ran far over budget",
     "Shown, not added", "The game's bill is the planning value; adding an overrun would only widen the gap"),
]


def terms_table():
    return ctable(["Term", "How it enters", "Base (low / high)", "Evidence"], [[f"<b>{esc(a)}</b>", esc(b_), esc(c), esc(d)] for a, b_, c, d in TERMS],
                  cls="cards wide", txt_cols=(1, 2, 3))


CHANGED = [
    ("Air Force One (2018)", "A fixed-price deal of about $4B accepted under presidential pressure; about $3.1B of losses since. Calhoun: \"risks that Boeing probably shouldn't have taken\" (BX-0314)."),
    ("Keeping the 737 line (2019-21)", "Kept building the grounded MAX in 2019, citing \"600-some suppliers, hundreds of thousands of jobs\" (Muilenburg, B-1584), then paid about $4B to keep the production system through the 2020 suspension (B-1618, B-1675)."),
    ("Safety under Senate pressure (2024)", "Withdrew the MAX 7 exemption request (B-2140)."),
    ("Terms, through site competitions", "Washington's $8.7B for the 777X (2013); South Carolina's 2009 package for the second 787 line."),
    ("Selling through Washington (2025-26)", "Trade-deal orders, and a 200-aircraft China commitment in May 2026. Ortberg: \"my primary objective was to reopen that market to our narrowbody airplanes\" (Transcript Digest (4))."),
]
NOT_CHANGED = [
    ("Jobs", "About 10,000 cut in 2009 (B-0147), 26,000 in 2020 (B-1767) and about 17,000 (10%) in 2024 (announced 11 October 2024, press reports; aimed at overhead, B-2206)."),
    ("Washington state", "The second 787 line went to South Carolina in 2009 (B-0218) and all 787 production in 2020, which Governor Inslee called \"an insult\"."),
    ("Segments", "Production of the 757 (2004), 717 (2006) and 747 (2022) ended, and the 767 freighter ends in 2027; the NMA was shelved in 2020 (B-1620); the 100-150-seat segment was left to the A220 and E2 (B-1666)."),
    ("Embraer (2020)", "Walked away from the $4.2B joint venture when cash was at risk (B-1674); the 2024 settlement was $150M."),
    ("Government money with strings", "Raised $25B of bonds rather than take CARES Act loans (2020, BX-1636; it took a general $1.2B CARES tax benefit), and $24B of public equity in 2024 (B-2258; no state support is documented as on offer)."),
    ("China", "Out of guidance from late 2022 (B-1971): \"our $10 billion in '25, '26 ... has no China\" (Calhoun, 2023, B-2052)."),
    ("The next airplane", "\"That day is not today, and it's not any time near\" (Malave, March 2026); \"nothing has changed\" (Ortberg, 27 October 2026)."),
]


def cards(items):
    return "<ul class=\"cav\">" + "".join(f"<li><b>{esc(a)}.</b> {esc(t)}</li>" for a, t in items) + "</ul>"


CSS_EXTRA = MF.CSS_EXTRA + """
.two { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
@media (max-width: 900px) { .two { grid-template-columns: 1fr; } }
"""


def build(out_path):
    s30, s30y, s30_8, s30y_8 = S[(1, R10)][0], SY[(1, R10)][0], S[(1, R8)][0], SY[(1, R8)][0]
    cut30 = MF.rtxt(CUT[(1, R10)][0], CUT[(1, R10)][1], MF.cut_pct)
    tiles = [
        ("What Boeing has paid to stay in a commercial market", "about $0", "the 757, 717, NMA, the 100-150-seat segment and Embraer were left on the numbers; the 747-8 was kept through losses on product grounds and ended in 2023. Pressure changed where and on what terms Boeing built, not whether."),
        ("Premium needed to launch in 2030, at 10.5%", bp(s30, 1, False), f"PV at 2026 ({bp(s30y, 1, False)} in 2030 money) at base values, on top of the franchise terms, US co-funding and the cost of leaving; {bp(HI[(1, R10)][0], 1, False)} in 2030 money in the high case. At base values none is enough if the rating test counts cash only."),
        ("The same at 8.1%", bp(s30_8, 1, False), f"({bp(s30y_8, 1, False)} in 2030 money): inside the CEO's $2B allowance for soft choices. Here it is a new airplane against a 787 Re-engine; none at all is needed if the CEO anticipates the Board's veto of the Re-engine."),
        ("Government money Boeing could expect", "about 2% of the bill", f"a 2030 launch would need a government to carry {cut30} of it at 10.5% ({MF.cut_pct(CUT[(1, R8)][0])} at 8.1%). No US airliner has had direct federal launch funding since the SST."),
    ]
    tiles_html = '<div class="tiles">' + "".join(f'<div class="panel tile"><div class="k">{esc(k)}</div><div class="v">{esc(v)}</div><div class="d">{esc(d)}</div></div>' for k, v, d in tiles) + "</div>"
    r = RS["research"]
    n_find = sum(len(x["findings"]) for x in r)
    sc10, sc8 = s_rng(1, BASE, R10, world=WC)[0], s_rng(1, BASE, R8, world=WC)[0]
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Politics, Brand and Rivals</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{K.CSS + CSS_EXTRA}</style></head><body><div class="wrap">
<header class="top"><p class="eyebrow">Boeing Product Development · war game rerun · MAX phase-out world · BOEING PROPRIETARY</p>
<h1>Jobs, Washington, brand and China: can they launch the fps when the numbers say no?</h1>
<p class="lede">Leaving the narrowbody market would put the weight of Washington, of hundreds of thousands of jobs and of Boeing's identity as an engineering company on the decision,
and would leave the market to Airbus and, in time, COMAC. This page looks at how Boeing has behaved when that kind of pressure was on it, sizes what can be sized
(government money and a political cost of leaving), and asks how much weight the Board would have to put on staying in to launch the fps, against what Boeing has actually paid for such reasons.</p>
<p class="gloss"><b>Basis.</b> The franchise page's full view (the brief plus continuing value, services, stranded overhead, widebody erosion and closing costs), constant 2026 $B, against Do Nothing,
in the columns the CEO expected each round, at the game's 10.5% and at 8.1%; base values unless a case is named. Rivals' moves are held as the game played them.
<b>Strategic premium:</b> the weight the Board would put on staying in, added to every plan with an fps in every column, found as the smallest amount at which Boeing's decision rule launches one.
<b>Decision-year money:</b> that premium carried forward at the rate to the year of the decision, in constant 2026 dollars: what the Board would be giving up when it decides. What Boeing paid in the past is in 2026 prices at the time it was paid, so it is compared with decision-year money.
<b>Rating test:</b> the Board's check that the plan's risk-case column is no more than $2B below Do Nothing. The rule as re-implemented here gives back all {PJ["decide2_checked"]} decisions stored by the franchise model and matches the game's rule on 12,000 random cases.</p></header>
<section style="margin-top:18px">{tiles_html}</section>

<section><h2>The answer</h2><div class="bl">
<div class="panel"><div><b>Pressure has changed where and how Boeing builds, not whether</b>
Washington, jobs and reputation have moved Boeing on government contracts it could not walk away from, on safety, on where it builds and on what terms, and on keeping the 737 line together through the grounding.
They have not made it launch a commercial programme whose numbers failed: it cut jobs, moved the 787 out of Washington state, shelved the NMA, left the 100-150-seat segment and walked away from Embraer.
The one it kept through losses, the 747-8, it kept on product grounds ("a good product that serves a good market") and ended in 2023. Boeing has never been tested on leaving its core 737 market, so the record bounds the answer rather than settling it.</div></div>
<div class="panel"><div><b>At 10.5% the premium needed is {K.rnd(RATIO[0], 1):.1f} to {K.rnd(RATIO[1], 0):.0f} times the most Boeing has chosen to pay up front</b>
To launch in 2030 the Board would have to value staying in at {b(s30, 2, False)} (PV at 2026), {b(s30y, 1, False)} in 2030 money, after the franchise terms, about 2% government co-funding and a political cost of leaving
({b(X[(1, R10)], 2, False)} at 2026). {b(S[(1, R10)][0] - ANT30[0], 2, False)} of that is the cost of beating the 787 Re-engine the CEO prefers and the Board vetoes; against leaving alone it is {b(ANT30[0], 2, False)} ({b(ANT30Y[0], 1, False)} in 2030 money).
Later rounds need less at 2026 but more in their own money: {b(SY[(2, R10)][0], 1, False)} in 2035, {b(SY[(3, R10)][0], 1, False)} in 2045, {b(SY[(4, R10)][0], 1, False)} in 2050.
The most Boeing has chosen to pay up front for such reasons is about {b(TOP, 1, False)} in 2026 prices (keeping the 737 line in 2020, mostly ordinary value), and to stay in a commercial segment about nothing.
It has absorbed larger losses after the fact on contracts it could not walk away from (the KC-46, about {b(KC46, 1, False)}), but never chose them up front.
At base values, if the rating test reads cash only, no premium of any size launches the fps in 2030, 2035 or 2045: the balance sheet binds. With the franchise and government terms at their high values, though,
the 2030 and 2035 premiums fall to {b(HI[(1, R10)][0], 1, False)} and {b(HI[(2, R10)][0], 1, False)} in decision-year money, within what Boeing has paid, and the cash-only rating test no longer blocks them: then politics and brand could tip a launch even at 10.5%.</div></div>
<div class="panel"><div><b>At 8.1% it is within reach, and it is a choice between airplanes, not about leaving</b>
In 2030 at 8.1% the premium needed is {b(s30_8, 2, False)} ({b(s30y_8, 2, False)} in 2030 money), inside the CEO's $2B allowance for soft choices (a game rule). It rests on the base franchise terms, and on co-funding and the cost of leaving,
which supply {b(S0_8 - s30_8, 2, False)} of the {b(S0_8, 2, False)} needed without them; with the franchise terms low it is {b(LO[(1, R8)][0], 1, False)} in 2030 money. The fps already beats Do Nothing here;
what it has to beat is a 787 Re-engine, which the CEO prefers and the Board then vetoes on its downside test. "Boeing's an airplane company ... we need to develop a new airplane" (Ortberg, 2024) is the kind of weight that could tip it.
If the CEO anticipates that veto instead of proposing the Re-engine, Boeing launches the 7-year fps at Renton with no premium and no politics at all: on the franchise terms alone it is {b(E7)} against Do Nothing.
The franchise page's "Boeing does nothing" at 8.1% is the game's rule as written, this page's "as played".</div></div>
<div class="panel"><div><b>Exit pressure bites at the point of no return, and there it would buy a late launch at most</b>
Not launching in 2030 is not leaving: Boeing can still launch in 2035, 2045 or 2050, and a 10-year fps launched in 2050 enters service as the last MAX is built. The weight of leaving falls on the 2050 decision,
where the premium would have to be worth {b(SY[(4, R10)][0], 1, False)} in 2050 money at 10.5% ({b(SY[(4, R8)][0], 1, False)} at 8.1%). The game's $1B tests are in 2026 money, about {b(BIZ50, 0, False)} in 2050 money;
stated in 2050 money instead, the premium would be {b(DFL[(4, R10)]["S_decision_year"], 1, False)}. Or a government would have to carry {MF.cut_pct(CUT[(4, R10)][0])} of the bill ({MF.cut_pct(CUT[(4, R8)][0])} at 8.1%).
That fits Boeing's record: jobs and politics have bought delay, not reversal.</div></div>
<div class="panel"><div><b>A stronger COMAC lowers the commercial case; Brazil is at odds with Washington, and Embraer could become a third maker</b>
China is a competitor in US strategy, not a declared enemy (the December 2025 National Security Strategy frames it mainly as an economic, "near-peer" competitor), and the Pentagon listed COMAC as a
Chinese military company in January 2025. Brazil is still formally a US Major Non-NATO Ally (since July 2019), but its government and Washington are at loggerheads: a 25% US tariff on most Brazilian goods since July 2026 (civil aircraft exempt),
and Lula, re-elected on 25 October 2026, ran against US pressure. Korea's president has asked Brazil to build a next-generation airliner together; <a href="fps_embraer.html">the Embraer page</a> prices Embraer as a third maker, on price and share.
If COMAC grows to take all of China's single-aisle demand by 2050, the fps is worth less ({b(ITEM(1, R10, TEN, WC))} against Do Nothing in 2030, from {b(ITEM(1, R10, TEN))}) and the premium needed rises
(to {b(sc10, 2, False)} at 10.5% and {b(sc8, 2, False)} at 8.1%), even with a higher chance that Washington makes Boeing pay for leaving (an assumption).</div></div>
</div></section>

<section><h2>How Boeing has behaved under pressure</h2><div class="two">
<div class="panel"><p class="ctitle">Where pressure changed the decision</p>{cards(CHANGED)}</div>
<div class="panel"><p class="ctitle">Where it did not</p>{cards(NOT_CHANGED)}</div>
</div>
<div class="panel" style="margin-top:14px"><p class="ctitle">What Boeing's leaders say about the next airplane</p>
<p>"Boeing's an airplane company. And at the right time in the future, we need to develop a new airplane" (Ortberg, October 2024, B-2217). "We'll do one" (Calhoun, 2020, B-1620). Always on three conditions:
"when is the market ready? ... when are we ready, both financially and from a capacity perspective? ... when is the technology ready?" (Ortberg, 2025, B-2303). And earlier: "It will not be based on market share" (Muilenburg, 2016, B-1131).</p></div></section>

<section><h2>Washington and jobs</h2><div class="panel"><ul class="cav">
<li><b>The jobs.</b> About 172,000 employees at the end of 2024 (15% outside the US) and about 182,000 at the end of 2025, about 65,000 of them in Washington state; IAM 751 represents more than 30,000 machinists, and 33,000 struck for 53 days in 2024. Boeing says it supports about 1.5 million US jobs and the Commerce Department says 1.8 million: multiplier estimates, not headcount.</li>
<li><b>The leverage.</b> The US government provided 35-51% of Boeing's revenue in 2020-25; Boeing won both sixth-generation fighter awards (F-47 in 2025, F/A-XX in 2026); the FAA sets the 737 rate cap (38, then 42, then 47 a month); the 737 MAX criminal case ended in a non-prosecution agreement and was dismissed in November 2025.</li>
<li><b>Washington as salesman.</b> In 2025 Boeing and GE made up about $215B of the $244B of foreign deals the Commerce Department helped win, and the May 2026 Trump-Xi summit brought a 200-aircraft China commitment.</li>
<li><b>Washington as shareholder.</b> Since 2025 the government has taken equity in strategic firms (Intel 9.9%, MP Materials about 15%, a golden share in US Steel). Asked on CNBC in August 2025 about stakes in firms such as Boeing and Palantir, the Commerce Secretary said stakes in defence contractors were being discussed and named Lockheed Martin; no Boeing stake has been taken.
Boeing has avoided state money with equity strings: it raised $25B of bonds rather than take CARES Act loans in 2020 (taking only a general $1.2B CARES tax benefit), and $24B of public equity in 2024.</li>
<li><b>What leaving would leave behind.</b> Airbus already builds A320s and A220s in Mobile, Alabama (three lines, more than 2,000 staff), so not all final-assembly jobs would leave the US. No US official or member of Congress was found asking for a 737 successor in the searches; that may be a gap in the searches.</li>
</ul></div></section>

<section><h2>Brand and engineering identity</h2><div class="panel"><ul class="cav">
<li><b>In the narrowbody, finance has won since 2011</b> (this page's reading of the record): the MAX was chosen over the clean sheet its engineers wanted (2011), the NMA was shelved (2020), and $43B went to buybacks in 2013-19, about twice R&D. Boeing did launch the clean-sheet 787 (2004) after dropping the Sonic Cruiser for it, and the 747-8 and 777X derivatives. In 2011, when share was at risk, it still took the cheapest option.</li>
<li><b>Boeing's reputation costs came from failing to execute, not from declining to launch.</b> The MAX crisis cost about $20B directly, Boeing's market value fell from about $240B to about $112B, and it needed a $24B equity raise. Buyers came back once supply did: 1,173 net orders in 2025 against Airbus's 889, and Brand Finance put the brand up 34% in 2026, with no new airplane. Only about 3% of passengers rank aircraft type first.</li>
<li><b>Talent cuts both ways.</b> Boeing hired 10,000 engineers in 2022 without a new airliner, and the F-47 and F/A-XX give engineers frontier work. What erodes is design experience: average engineer tenure fell from 16.4 to 12.6 years over the decade to 2024 (FT, from SPEEA data; partly the 2022 hiring), and across the US military aircraft industry design starts per team fell from about 2.5 a decade in the 1950s to about one every two decades by 1990 (RAND, 1992).</li>
<li><b>The brand risk runs both ways.</b> A launch that fails costs more reputation than a launch deferred: the 787's overruns and the MAX show the downside a brand premium would have to be set against.</li>
</ul></div></section>

<section><h2>China and COMAC</h2><div class="panel"><ul class="cav">
<li><b>The weight.</b> China was 21.5% of Commercial Airplanes revenue in 2018 and about 10% of the commercial backlog in April 2025 (B-2292). Boeing's 2026 China outlook has 7,215 single-aisle deliveries in 2026-45, about 21% of world single-aisle demand and about 360 a year.</li>
<li><b>Boeing's behaviour.</b> Since late 2022 it plans without China (B-1971, B-2052). When China stopped deliveries (2019-24, and April-May 2025) it waited and remarketed aircraft (B-2293). Ortberg calls the 2026 China order "100% dependent" on the US-China talks.</li>
<li><b>Washington's behaviour is transactional.</b> Export licences for COMAC were suspended in May 2025, restored in July 2025 and capped in October 2026 as leverage; the May 2026 deal paired Boeing orders with US "strict supply guarantees" for aircraft engine parts (which COMAC needs; the link to COMAC is an inference). A July 2026 Section 232 finding said aircraft imports threaten national security but set no tariffs.</li>
<li><b>COMAC is slow but backed by the state.</b> About 13-15 C919 deliveries in 2025, against a target raised from 30 to 75 and then cut to 25; a target of 200 a year by 2029; no Western approval before about 2028-31; LEAP engines until China's CJ-1000A arrives around 2030; $49-72B of state support (CSIS estimate). Calhoun in 2023: "even in an optimistic case, maybe in 2050, they get to be a 10% player" (BX-0380).</li>
<li><b>In the game</b> COMAC sells 250 a year from 2050 to its home market first, and gains none of the {MF.n0(-WP["boeing"])} deliveries Boeing gives up when the MAX ends in 2045-60: they go to Airbus ({MF.n0(WP["airbus"])}) and an unnamed entrant ({MF.n0(WP["entrant"])}).</li>
</ul></div>
<div class="panel" style="margin-top:14px"><p class="ctitle">A stronger COMAC makes the fps worth less and the premium needed larger</p>{comac_table()}
<p class="cap">COMAC takes all of China's single-aisle demand by 2050: its 200-a-year target reached in 2032 instead of 2029, then 280 a year in 2040, 330 in 2045 and 360 in 2050 (all of China's single-aisle demand in Boeing's outlook), sold to its home market first.
The brief and the franchise terms are re-run in that market. COMAC still sells only its own capacity, so it gains none of the share Boeing gives up here either. The chance that Washington makes Boeing pay for leaving is raised from 20% to 50%, an assumption that adds {b(XC, 2, False)} to the cost of leaving at 10.5%.
Value columns: the franchise view, without co-funding or the cost of leaving.</p></div></section>

<section><h2>Brazil and Embraer</h2><div class="panel"><ul class="cav">
<li><b>Allied on paper, at odds in practice.</b> Brazil has been a US Major Non-NATO Ally since 31 July 2019. The July 2025 US tariffs on Brazil were over the Bolsonaro prosecution; civil aircraft and parts were exempt from the additional duty, but Brazilian jets still paid the 10% baseline until the Supreme Court struck those tariffs down on 20 February 2026, while EU, UK and Japanese aircraft were back at zero (Embraer \"was the only manufacturer to pay tariffs on aircraft exports\", March 2026). A 25% Section 301 tariff on most Brazilian goods followed in July 2026 (aircraft exempt), and Lula won re-election on 25 October 2026 running against US pressure (search extracts; see the Embraer page).</li>
<li><b>Tied into the US.</b> Embraer's jets carry more than 40% US content and Pratt & Whitney engines on the E2; it employs about 2,500 people in the US and sells the C-390 to NATO air forces.</li>
<li><b>Small next to the 737, but courted.</b> 78 commercial deliveries in 2025 against about 564 737s a year at rate 47; no narrowbody decision before about 2030; it sounded out Saudi, Turkish, Indian and Korean partners (2024 report, exploratory), and in July 2026 Korea's president proposed building a next-generation airliner together and KAI and Embraer signed a non-binding memorandum.</li>
<li><b>Boeing's own record with Embraer</b> is the clearest case of strategy giving way to cash: $4.2B for 80% of its commercial business agreed in 2018, terminated in April 2020, settled for $150M in 2024.</li>
<li><b>In the game</b> the "fps via Embraer" plan carries a $100B bill on the board, so it never competes, and the game's Embraer-like entrant sells only to customers nobody else can serve. <a href="fps_embraer.html">The Embraer page</a> prices Embraer as a competitor and partners for the bill.</li>
</ul></div></section>

<section><h2>How these enter the decision</h2><div class="panel">{terms_table()}</div></section>

<section><h2>The premium needed, round by round</h2><div class="stack">
<div class="panel"><p class="ctitle">At 10.5% the premium needed is {K.rnd(RATIO[0], 1):.1f} to {K.rnd(RATIO[1], 0):.0f} times the most Boeing has chosen to pay up front; at 8.1% in 2030 it is small</p>
<div class="legend"><span><i class="sw" style="background:var(--s1)"></i>at 10.5%</span><span><i class="sw" style="background:var(--s2)"></i>at 8.1%</span><span>in the decision year's money; log scale; bars show the low end of the range across readings</span></div>
<div class="cw only-wide">{ladder_chart()}</div><div class="cw only-narrow">{ladder_chart(True)}</div>
<p class="cap">Premium the Board would have to put on an fps for its rule to launch one, in money of the decision year (constant 2026 dollars), with the franchise terms and the base government terms on. Dashed lines: what Boeing has paid, in 2026 prices, chosen up front or absorbed after the fact.</p></div>
<div class="panel">{needed_table()}
<p class="cap">Premium needed as the game's rule is written ("as played"), and two other readings: the rating test reading cash only (a brand or political weight does not make spend affordable), and a CEO who proposes only what the Board would approve
(the Board vetoes the 787 Re-engine alone in every round here, as it did in the game's 2030 round); "none": no premium of any size launches an fps; "same": as played; $0 (7-year): the 7-year fps at Renton launches with no premium. Where a range is shown, it spans the four readings of the CEO's rule (as on the main report). Low and high cases: the franchise and government terms all at their low or high values.
Government share: the share of Boeing's fps bill a government would have to carry instead, with no premium, rounded up. At 8.1% the bill weighs more at 2026, so the rating test also binds in 2045 and 2050.</p></div>
<div class="panel"><p class="ctitle">What Boeing has paid for strategic or political reasons</p>{ladder_table()}
<p class="cap">Only the choices made up front are premiums Boeing chose; losses after signing a fixed-price contract, or on a programme already launched, are what it absorbed. The T-X and MQ-25 bids bought future franchise value, which the franchise terms already credit to the fps.
Counted the after-the-fact way, the KC-46 alone would exceed the 2030 and 2035 premiums at 10.5%.</p></div>
</div></section>

<section><h2>Notes</h2><div class="panel"><ul class="cav">
<li><b>The point of no return.</b> The premium is solved round by round, but only the 2050 decision is an exit. The 2030-45 figures value Do Nothing as never launching, as the brief does (the cost of leaving and closing costs are charged to it): they are the premium needed to launch now rather than never, and counting a later launch in Do Nothing would raise them.</li>
<li><b>The Board's dollar tests</b> ($1B business case, -$1B downside, -$2B rating) are in 2026 money in the game. Stated in the decision year's money instead, the 2030 premium at 10.5% would not change ({b(DFL[(1, R10)]["S"], 2, False)} at 2026: there the CEO's $1B margin over the Re-engine binds, not a Board test), and the 2050 one would be {b(DFL[(4, R10)]["S"], 2, False)} at 2026 ({b(DFL[(4, R10)]["S_decision_year"], 1, False)} in 2050 money).</li>
<li><b>Readings.</b> "As played" is the game's rule with its four readings, as on the main report; the rating-on-cash and anticipating readings are this page's, not the game's.</li>
<li><b>Sizes.</b> Government co-funding and the political cost of leaving are inferences from precedents, labelled so in the research file. The political cost is small ({b(X[(1, R10)], 2, False)} at 2026 at 10.5%) because the chance and amount are small (20% x $0.44B a year, about $0.8B in 2045 money); standing in for the 2050 premium would take about $2.9B a year at risk, more than all of the assumed defence profit.</li>
<li><b>Framing checked against sources:</b> Brazil's Major Non-NATO Ally designation ({FRAMING["mnna"]}, <a href="https://www.govinfo.gov/content/pkg/FR-2019-08-19/html/2019-17998.htm">Federal Register</a>); the China wording of the {FRAMING["nss"]} National Security Strategy (<a href="https://www.brookings.edu/articles/how-china-reads-the-2025-u-s-national-security-strategy">Brookings</a>, <a href="https://www.cfr.org/expert-brief/unpacking-trump-twist-national-security-strategy">CFR</a>); COMAC's listing as a Chinese military company ({FRAMING["1260h"]}, <a href="https://aviationweek.com/defense/budget-policy-operations/pentagon-identifies-comac-chinese-military-contractor">Aviation Week</a>); the Supreme Court's IEEPA ruling ({FRAMING["ieepa"]}, <a href="https://www.thompsoncoburn.com/insights/65-february-20-2026-supreme-court-issues-ruling-on-ieepa-tariffs/">Thompson Coburn</a>).</li>
<li><b>Sources:</b> {n_find} findings from six research sweeps (Washington and jobs, brand, China, Brazil and Embraer, governments and national champions, decision practice), with the model design and two adversarial checks, in data/politics_research.json. Many web facts rest on search excerpts because the hosts blocked fetching; the file marks each finding's confidence.</li>
<li><b>Files:</b> politics.py writes data/politics.json; make_politics_html.py builds this page and asserts its claims against it.</li>
</ul></div></section>
<footer>BOEING PROPRIETARY. Built by make_politics_html.py from run dash-2050-phaseout.</footer></div>
<script>{K.JS}</script></body></html>"""
    for bad in ("Milk", "Sabotage", "C3_", "c_gov", "exit_p", " his ", " he ", " she ", " her ", "H8"):
        assert bad not in page, bad
    with open(out_path, "w") as f:
        f.write(page)
    print("wrote", out_path, len(page))


if __name__ == "__main__":
    build(os.path.join(HERE, "fps_politics.html"))
