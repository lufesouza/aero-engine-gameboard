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
W, WC = PJ["worlds"]["base"], PJ["worlds"]["comac on plan"]
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
        return "none launches"
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
CUT = {(n, rt): case(n, BASE, rt)["cut_needed"] for n in (1, 2, 3, 4) for rt in (R10, R8)}
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
# at 8.1% in 2030 the premium is small, within the Board's $2B cap even in 2030 money; a CEO who anticipates the Board's
# veto of the 787 Re-engine alone launches the 7-year fps with no premium at all
assert SY[(1, R8)][1] < 1.0 and s_rng(1, BASE, R8, "cash rating") == S[(1, R8)]
assert s_rng(1, BASE, R8, "anticipating") == (0.0, 0.0) and plan_of(1, BASE, R8, "anticipating") == SEVEN
assert s_rng(1, "base|full|cash low", R8, "anticipating") == (0.0, 0.0) and plan_of(1, "base|full|cash low", R8, "anticipating") == SEVEN
# the premium solved on the rule as played launches the 10-year fps on new sites in 2030, the 10-year at Renton later
assert plan_of(1, BASE, R10) == TEN_NEW and all(plan_of(n, BASE, R10) == TEN for n in (2, 3, 4))
# the government share of the bill that would launch, against US practice (about 2%)
assert 0.2 < CUT[(1, R10)] < 0.3 and 0.03 < CUT[(1, R8)] < 0.04 and CUT[(4, R10)] > 0.75 and CUT[(4, R8)] > 0.5
# the revealed-premium ladder in 2026 dollars
LADDER = [("Commercial segments left or walked away from", 0.0, "757, 717, 747, NMA, the 100-150-seat segment, Embraer: nothing paid to stay in",
           "B-1620, B-1666, B-1674, 10-K FY2020"),
          ("T-X and MQ-25 bids (2018)", 0.91, "$0.69B pre-tax charges taken up front, by choice, to win two long-lived defence franchises: franchise logic, as in continuing value",
           "B-1458, BX-1545"),
          ("The Board's cap on soft choices", 2.0, "a rule of the game (H8), not evidence about Boeing", "profile.md H8"),
          ("VC-25B, Air Force One (2018)", 3.4, "a fixed-price deal accepted under presidential pressure; about $3.1B of losses to 2026. \"Risks that Boeing probably shouldn't have taken\" (Calhoun)",
           "BX-0314; 10-Ks FY2020-24; FQ2 2026 call"),
          ("Keeping the 737 line in the 2020 suspension", 4.0, "about $4B of abnormal costs (the pre-COVID estimate) to keep the workforce and 600-plus suppliers: mostly ordinary value for a programme that would restart",
           "B-1618, B-1675, B-1584")]
TOP = max(x for _, x, _, _ in LADDER if x > 0)
RATIO = (SY[(1, R10)][0] / TOP, SY[(4, R10)][0] / TOP)
assert all(SY[(n, R10)][0] > TOP for n in (1, 2, 3, 4)) and 2.0 <= RATIO[0] and RATIO[1] < 7.0
# the deliveries Boeing gives up when the MAX ends go to Airbus and the entrant, none to COMAC (who_picks_up.py)
WP = json.load(open(os.path.join(HERE, "data", "who_picks_up.json")))["effect_of_phase_out"]
assert abs(WP["comac"]) < 1e-9 and WP["airbus"] > 400 and WP["entrant"] > 400
# COMAC on its own plan: a stronger COMAC lowers the fps's value and raises the premium needed, even with Washington's
# stakes raised
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
        w, left, right, rh, top = 400, 26, 12, 58, 64
    else:
        w, left, right, rh, top = 760, 120, 70, 46, 64
    rows = [(n, YEAR[n]) for n in (1, 2, 3, 4)]
    h = top + rh * len(rows) + 28
    sx = lambda v: left + (math.log10(max(v, 0.1)) - lo) / (hi - lo) * (w - left - right)
    out = [K.svg_open(w, h, "Premium Boeing would need to launch the fps, by round, against the premiums Boeing has paid", "chart narrow" if narrow else "chart")]
    for v in (0.1, 0.3, 1, 3, 10, 30):
        x = sx(v)
        out.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{top}" y2="{h - 24}" class="grid"/><text x="{x:.1f}" y="{h - 8}" text-anchor="middle" class="tick">{bp(v, 1 if v < 1 else 0, False)}</text>')
    refs = [(0.91, "T-X/MQ-25 $0.9B"), (2.0, "Board cap $2B"), (3.4, "Air Force One $3.4B")]
    for i, (v, lab) in enumerate(refs):
        x = sx(v)
        out.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{12 + i * 16}" y2="{h - 24}" class="ref" stroke-dasharray="4 3"/>'
                   f'<text x="{x + 4:.1f}" y="{20 + i * 16}" class="reflab">{esc(lab)}</text>')
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
    head = ["", "Premium needed, today's money", "In the decision year's money", "Rating test on cash only", "CEO anticipates the Board", "Government share of the bill instead"]
    rows = []
    for rt in (R10, R8):
        rows.append(f"At {rt}")
        for n in (1, 2, 3, 4):
            cr = s_rng(n, BASE, rt, "cash rating")
            an = s_rng(n, BASE, rt, "anticipating")
            rows.append([f"{YEAR[n]} brief", s_txt(S[(n, rt)], 2), s_txt(SY[(n, rt)]), s_txt(cr, 2) if cr != S[(n, rt)] else "same",
                         ("no premium needed (" + esc(plan_of(n, BASE, rt, "anticipating")) + ")") if an == (0.0, 0.0) else (s_txt(an, 2) if an != S[(n, rt)] else "same"),
                         MF.cut_pct(CUT[(n, rt)])])
    return ctable(head, rows, num_cols=(1, 2, 3, 4, 5))


def ladder_table():
    return ctable(["What Boeing paid", "2026 dollars", "What it bought", "Evidence"],
                  [[esc(a), b(v, 1, False) if v else "$0", esc(c), esc(d)] for a, v, c, d in LADDER], num_cols=(1,), txt_cols=(2, 3))


def comac_table():
    head = ["", "fps against Do Nothing, the game's market", "With COMAC on its own plan", "Premium needed, the game's market", "With COMAC on its own plan"]
    rows = []
    for rt in (R10, R8):
        rows.append(f"At {rt}, 10-year fps at Renton")
        for n in (1, 2):
            rows.append([f"{YEAR[n]} brief", b(ITEM(n, rt, TEN)), b(ITEM(n, rt, TEN, WC)), s_txt(S[(n, rt)], 2), s_txt(s_rng(n, BASE, rt, world=WC), 2)])
    return ctable(head, rows, num_cols=(1, 2, 3, 4))


TERMS = [
    ("Government co-funding", "Cash: state siting incentives and federal technology money, as a cut in Boeing's share of the fps bill (the bill's debt penalty falls with it)",
     "2% of the bill (0 / 5%)",
     "No federal money has launched a US airliner since the SST was cancelled in 1971. Washington's 2013 package for the 777X ($8.7B on paper, about $1.5B in present value) and South Carolina's 2009 package ($450-900M) were won by site competitions; NASA put $425M into the X-66, paused in 2025. Boeing itself backed 'market terms' for all future support (2021, B-1825), and the WTO let the EU tariff $4B a year of US goods over one Washington tax break (B-1761). Airbus-style launch aid (up to a third of a programme) is not US practice"),
    ("Political cost of leaving", "Cash-like goodwill: a chance that Washington makes Boeing pay for leaving, through defence, export finance or the FAA's rate approvals, on the plans without an fps; kept out of the Board's rating test",
     "20% x $0.44B a year of defence profit for 20 years from 2045 (0 / 50% x $0.66B from 2040)",
     "Washington's leverage is real: 35-51% of Boeing's revenue came from the US government in 2020-25, the FAA sets the 737 rate cap, and in 2025-26 the administration sold Boeing jets in trade deals. But no precedent shows a penalty for a commercial product choice: Boeing's own exits, job cuts and moves out of Washington state passed without one. The size is judgement"),
    ("Strategic premium", "The weight the Board would put on staying in: identity as an engineering company, engineering talent, standing as the last US airliner maker. Added to every fps plan in every column and solved for the amount that launches",
     "Solved, then compared with what Boeing has paid",
     "Subjective by construction. It leaves out everything the franchise terms already count (continuing value, services, overhead, widebody erosion, closing costs)"),
    ("Not added", "Military 737s (P-8, E-7) after the line ends, Washington's help selling jets (both options keep it while the MAX sells), China market access (Boeing plans without China), a federal safety net under the Board's tests (Boeing funded itself privately in 2020 and 2024)",
     "Zero",
     "Military 737s are worth about $0.03B today; Boeing took China out of its guidance in 2023 (B-2052); it raised $25B of bonds rather than take CARES Act loans (BX-1636)"),
    ("Counter-weight", "The brand risk of launching and failing: the MAX crisis cost about $20B directly and halved Boeing's market value; the 787 ran far over budget",
     "Shown, not added", "The game's bill is the planning value; adding an overrun would only widen the gap"),
]


def terms_table():
    return ctable(["Term", "How it enters", "Base (low / high)", "Evidence"], [[f"<b>{esc(a)}</b>", esc(b_), esc(c), esc(d)] for a, b_, c, d in TERMS],
                  cls="cards wide", txt_cols=(1, 2, 3))


CHANGED = [
    ("Air Force One (2018)", "A fixed-price deal of about $4B accepted under presidential pressure; about $3.1B of losses since. Calhoun: \"risks that Boeing probably shouldn't have taken\" (BX-0314)."),
    ("Keeping the 737 line (2019-21)", "Kept building the grounded MAX in 2019, citing \"600-some suppliers, hundreds of thousands of jobs\" (Muilenburg, B-1584), then paid about $4B to keep the workforce through the 2020 suspension (B-1618, B-1675)."),
    ("Safety under Senate pressure (2024)", "Withdrew the MAX 7 exemption request (B-2140)."),
    ("Terms, through site competitions", "Washington's $8.7B for the 777X (2013); South Carolina's 2009 package for the second 787 line."),
    ("Selling through Washington (2025-26)", "Trade-deal orders, and a 200-aircraft China commitment in May 2026. Ortberg: \"my primary objective was to reopen that market to our narrowbody airplanes\" (Transcript Digest (4))."),
]
NOT_CHANGED = [
    ("Jobs", "About 10,000 cut in 2009 (B-0147), 26,000 in 2020 (B-1767) and 17,000 in 2024 (B-2206)."),
    ("Washington state", "The second 787 line went to South Carolina in 2009 (B-0218) and all 787 production in 2020, which Governor Inslee called \"an insult\"."),
    ("Segments", "The 757 (2004), 717 (2005), 747 (2023) and 767 freighter (2027) ended; the NMA was shelved in 2020 (B-1620); the 100-150-seat segment was left to the A220 and E2 (B-1666)."),
    ("Embraer (2020)", "Walked away from the $4.2B joint venture when cash was at risk (B-1674); the 2024 settlement was $150M."),
    ("Government money with strings", "Raised $25B of bonds rather than take CARES Act loans (2020, BX-1636), and $24B of public equity in 2024 (B-2258)."),
    ("China", "Taken out of guidance: \"our $10 billion in '25, '26 ... has no China\" (Calhoun, 2023, B-2052)."),
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
    tiles = [
        ("What Boeing has paid to stay in a commercial market", "about $0", "the 757, 717, 747, NMA, the 100-150-seat segment and Embraer were left on the numbers. Pressure changed where and on what terms Boeing built, not whether."),
        ("Weight needed to launch in 2030, at 10.5%", bp(s30, 1, False), f"today's money ({bp(s30y, 1, False)} in 2030 money), on top of the franchise terms, US co-funding and the cost of leaving. None is enough if the Board's rating test counts cash only."),
        ("The same at 8.1%", bp(s30_8, 1, False), f"({bp(s30y_8, 1, False)} in 2030 money): inside the Board's $2B cap for soft choices. Here it is a new airplane against a 787 Re-engine, and Boeing's identity could decide it."),
        ("Government money Boeing could expect", "about 2% of the bill", f"a 2030 launch would need a government to carry {MF.cut_pct(CUT[(1, R10)])} of it at 10.5% ({MF.cut_pct(CUT[(1, R8)])} at 8.1%). No US airliner launch has had federal money since the SST."),
    ]
    tiles_html = '<div class="tiles">' + "".join(f'<div class="panel tile"><div class="k">{esc(k)}</div><div class="v">{esc(v)}</div><div class="d">{esc(d)}</div></div>' for k, v, d in tiles) + "</div>"
    r = RS["research"]
    n_find = sum(len(x["findings"]) for x in r)
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
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
in the columns the CEO expected each round, at the game's 10.5% and at 8.1%. Rivals' moves are held as the game played them. The weight is added to every plan with an fps in every column, and found as the
smallest amount at which Boeing's decision rule launches one. The rule as re-implemented here gives back every one of the {PJ["decide2_checked"]} decisions stored by the franchise model.</p></header>
<section style="margin-top:18px">{tiles_html}</section>

<section><h2>The answer</h2><div class="bl">
<div class="panel"><div><b>Pressure has changed where and how Boeing builds, not whether</b>
Washington, jobs and reputation have moved Boeing on government contracts it could not walk away from, on safety, on where it builds and on what terms, and on keeping the 737 line together through the grounding.
They have not made it launch, or keep, a commercial programme whose numbers failed: it cut jobs, moved the 787 out of Washington state, shelved the NMA, left the 100-150-seat segment and walked away from Embraer.
Boeing has never been tested on leaving its core 737 market, so the record bounds the answer rather than settling it.</div></div>
<div class="panel"><div><b>At 10.5% the weight needed is {K.rnd(RATIO[0], 0):.0f} to {K.rnd(RATIO[1], 0):.0f} times the most Boeing has paid</b>
To launch in 2030 the Board would have to value staying in at {b(s30, 2, False)} today, {b(s30y, 1, False)} in 2030 money, after the franchise terms, about 2% government co-funding and a political cost of leaving
({b(X[(1, R10)], 2, False)} today). Later rounds need less in today's money but more in their own: {b(SY[(2, R10)][0], 1, False)} in 2035, {b(SY[(3, R10)][0], 1, False)} in 2045, {b(SY[(4, R10)][0], 1, False)} in 2050.
The most Boeing has paid for such reasons is about {b(TOP, 1, False)} in 2026 dollars (keeping the 737 line in 2020, mostly ordinary value; Air Force One's losses, about $3.4B), and to stay in a commercial segment about nothing. And if the Board's rating test reads cash only, as a balance-sheet test should,
no weight of any size launches the fps in 2030, 2035 or 2045: the balance sheet, not the will, binds.</div></div>
<div class="panel"><div><b>At 8.1% it is within reach, and it is a choice between airplanes, not about leaving</b>
In 2030 at 8.1% the weight needed is {b(s30_8, 2, False)} ({b(s30y_8, 2, False)} in 2030 money), inside the Board's $2B cap for soft choices. The fps already beats Do Nothing here; what it has to beat is a 787 Re-engine,
which the CEO prefers and the Board then vetoes on its downside test. "Boeing's an airplane company ... we need to develop a new airplane" (Ortberg, 2024) is the kind of weight that could tip it.
If the CEO anticipates that veto instead of proposing the Re-engine, Boeing launches the 7-year fps at Renton with no premium at all.</div></div>
<div class="panel"><div><b>Exit pressure bites at the point of no return, and there it would buy a late launch at most</b>
Not launching in 2030 is not leaving: Boeing can still launch in 2035, 2045 or 2050, and a 10-year fps launched in 2050 enters service as the last MAX is built. The weight of leaving falls on the 2050 decision,
where it would have to be worth {b(SY[(4, R10)][0], 1, False)} in 2050 money at 10.5% ({b(SY[(4, R8)][0], 1, False)} at 8.1%), or a government would have to carry {MF.cut_pct(CUT[(4, R10)])} of the bill ({MF.cut_pct(CUT[(4, R8)])}).
That fits Boeing's record: jobs and politics have bought delay, not reversal.</div></div>
<div class="panel"><div><b>China raises the political stakes and lowers the commercial case; Brazil is not an adversary</b>
China is a competitor in US strategy, not a declared enemy (the December 2025 National Security Strategy frames it mainly as an economic, "near-peer" competitor), and the Pentagon listed COMAC as a
Chinese military company in January 2025. Brazil has been a US Major Non-NATO Ally since July 2019, civil aircraft were exempt from the 2025 tariffs on Brazil, and Embraer builds with more than 40% US content.
If COMAC grows to serve all of China's single-aisle demand by 2050, the fps is worth less ({b(ITEM(1, R10, TEN, WC))} against Do Nothing in 2030, from {b(ITEM(1, R10, TEN))}) and the weight needed rises
(to {b(s_rng(1, BASE, R10, world=WC)[0], 2, False)} at 10.5% and {b(s_rng(1, BASE, R8, world=WC)[0], 2, False)} at 8.1%), even with Washington's stakes raised.</div></div>
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
<li><b>Washington as shareholder.</b> Since 2025 the government has taken equity in strategic firms (Intel 9.9%, MP Materials about 15%, a golden share in US Steel); in August 2025 the Commerce Secretary named Boeing among defence firms where stakes were discussed (one report; no stake taken). Boeing has funded itself privately each time.</li>
<li><b>What leaving would leave behind.</b> Airbus already builds A320s and A220s in Mobile, Alabama (three lines, more than 2,000 staff), so not all final-assembly jobs would leave the US. No US official or member of Congress was found asking for a 737 successor in the searches; that may be a gap in the searches.</li>
</ul></div></section>

<section><h2>Brand and engineering identity</h2><div class="panel"><ul class="cav">
<li><b>Since 1997, finance has won almost every product decision:</b> the Sonic Cruiser cancelled (2002), the MAX chosen over the clean sheet its engineers wanted (2011), the NMA shelved (2020), and $43B of buybacks in 2013-19, about twice R&D. The exception was 2011, when share was at risk, and even then Boeing took the cheapest option.</li>
<li><b>Boeing's reputation costs came from failing to execute, not from declining to launch.</b> The MAX crisis cost about $20B directly, Boeing's market value fell from about $240B to about $112B, and it needed a $24B equity raise. Buyers came back once supply did: 1,173 net orders in 2025 against Airbus's 889, and Brand Finance put the brand up 34% in 2026, with no new airplane. Only about 3% of passengers rank aircraft type first.</li>
<li><b>Talent cuts both ways.</b> Boeing hired 10,000 engineers in 2022 without a new airliner, and the F-47 and F/A-XX give engineers frontier work. What erodes without a programme is design experience: engineer tenure fell from about 16 to about 13 years, and design starts per team fell from about 2.5 a decade to about one every two decades (RAND).</li>
<li><b>The brand risk runs both ways.</b> A launch that fails costs more reputation than a launch deferred: the 787's overruns and the MAX show the downside a brand premium would have to be set against.</li>
</ul></div></section>

<section><h2>China and COMAC</h2><div class="panel"><ul class="cav">
<li><b>The weight.</b> China was 21.5% of Commercial Airplanes revenue in 2018 and about 10% of the commercial backlog in April 2025 (B-2292). Boeing's 2026 China outlook has 7,215 single-aisle deliveries in 2026-45, about 21% of world single-aisle demand and about 360 a year.</li>
<li><b>Boeing's behaviour.</b> Since 2023 it plans without China (B-2052). When China stopped deliveries (2019-24, and April-May 2025) it waited and remarketed aircraft (B-2293). Ortberg calls the 2026 China order "100% dependent" on the US-China talks.</li>
<li><b>Washington's behaviour is transactional.</b> Export licences for COMAC were suspended in May 2025, restored in July 2025 and capped in October 2026 as leverage; the May 2026 deal paired Boeing orders with US "strict supply guarantees" for aircraft engine parts (which COMAC needs; the link to COMAC is an inference). A July 2026 Section 232 finding said aircraft imports threaten national security but set no tariffs.</li>
<li><b>COMAC is slow but backed by the state.</b> About 13-15 C919 deliveries in 2025 against a target of 75; a target of 200 a year by 2029; no Western approval before about 2028-31; LEAP engines until China's CJ-1000A arrives around 2030; $49-72B of state support (CSIS estimate). Calhoun in 2023: "even in an optimistic case, maybe in 2050, they get to be a 10% player" (BX-0380).</li>
<li><b>In the game</b> COMAC sells 250 a year from 2050 to its home market first, and gains none of the {MF.n0(-WP["boeing"])} deliveries Boeing gives up when the MAX ends in 2045-60: they go to Airbus ({MF.n0(WP["airbus"])}) and an unnamed entrant ({MF.n0(WP["entrant"])}). The scenario below lets COMAC follow its own plan to about 360 a year by 2050.</li>
</ul></div>
<div class="panel" style="margin-top:14px"><p class="ctitle">A stronger COMAC makes the fps worth less and the premium needed larger</p>{comac_table()}
<p class="cap">COMAC on its own plan: 120 a year in 2030, 200 in 2032, 280 in 2040, 330 in 2045 and 360 in 2050 (all of China's single-aisle demand in Boeing's outlook), sold to its home market first. The brief and the franchise terms are re-run in that market,
and the political cost of leaving is raised (a 50% chance instead of 20%). COMAC takes demand from both Boeing options, but an fps has more years in that market than the MAX run-out.</p></div></section>

<section><h2>Brazil and Embraer</h2><div class="panel"><ul class="cav">
<li><b>Not an adversary.</b> Brazil has been a US Major Non-NATO Ally since 31 July 2019. The July 2025 US tariffs on Brazil were over the Bolsonaro prosecution, and civil aircraft and parts were exempt (Embraer paid $54M at the 10% baseline in 2025); the Supreme Court struck down those tariffs on 20 February 2026.</li>
<li><b>Tied into the US.</b> Embraer's jets carry more than 40% US content and Pratt & Whitney engines on the E2; it employs about 2,500 people in the US and sells the C-390 to NATO air forces.</li>
<li><b>Small next to the 737.</b> 78 commercial deliveries in 2025 against about 564 737s a year at rate 47; no narrowbody decision before about 2030; it has sounded out Saudi, Turkish, Indian and Korean partners (2024 report, exploratory).</li>
<li><b>Boeing's own record with Embraer</b> is the clearest case of strategy giving way to cash: $4.2B for 80% of its commercial business agreed in 2018, terminated in April 2020, settled for $150M in 2024.</li>
<li><b>In the game</b> Embraer matters as a limit, not a threat: the "fps via Embraer" plan has Embraer paying 35% of the bill, $21-23B, about three times its 2025 revenue.</li>
</ul></div></section>

<section><h2>How these enter the decision</h2><div class="panel">{terms_table()}</div></section>

<section><h2>The weight needed, round by round</h2><div class="stack">
<div class="panel"><p class="ctitle">At 10.5% the weight needed is {K.rnd(RATIO[0], 0):.0f} to {K.rnd(RATIO[1], 0):.0f} times the most Boeing has paid; at 8.1% in 2030 it is within the Board's cap</p>
<div class="legend"><span><i class="sw" style="background:var(--s1)"></i>at 10.5%</span><span><i class="sw" style="background:var(--s2)"></i>at 8.1%</span><span>in the decision year's money; log scale</span></div>
<div class="cw only-wide">{ladder_chart()}</div><div class="cw only-narrow">{ladder_chart(True)}</div>
<p class="cap">Premium the Board would have to put on an fps for its rule to launch one, in money of the decision year (constant 2026 dollars), with the franchise terms and the base government terms on. Dashed lines: what Boeing has paid, in 2026 dollars.</p></div>
<div class="panel">{needed_table()}
<p class="cap">Premium needed, as the game's rule is written, and two other readings: the Board's rating test reading cash only (a brand or political weight does not make spend affordable), and a CEO who proposes only what the Board would approve
(the Board vetoes the 787 Re-engine alone in every round here, as it did in the game's 2030 round). Government share: the share of Boeing's fps bill a government would have to carry instead, with no premium, rounded up. At 8.1% the bill weighs more in today's money,
so the rating test also binds in 2045 and 2050.</p></div>
<div class="panel"><p class="ctitle">What Boeing has paid for strategic or political reasons</p>{ladder_table()}
<p class="cap">Only the T-X and MQ-25 bids were chosen up front, and they bought future franchise value, which the franchise terms already credit to the fps. Air Force One was a loss on a contract accepted under pressure, which Boeing regrets; keeping the 737 line was mostly ordinary value.</p></div>
</div></section>

<section><h2>Notes</h2><div class="panel"><ul class="cav">
<li><b>The point of no return.</b> The weight is solved round by round, but only the 2050 decision is an exit: before that, not launching keeps the option to launch later. A premium that is real only at the point of no return pushes a launch to the last round, where it is cheapest in today's money.</li>
<li><b>The Board's dollar tests</b> are in 2026 money in the game. Stated in the decision year's money instead, the 2030 premium at 10.5% would be {b(case(1, BASE, R10)["deflated_tests"]["S"], 2, False)} today and the 2050 one {b(case(4, BASE, R10)["deflated_tests"]["S"], 2, False)}.</li>
<li><b>Readings.</b> "As played" is the game's rule with its four readings, as on the main report; the rating-on-cash and anticipating readings are this page's, not the game's.</li>
<li><b>Sizes.</b> Government co-funding and the political cost of leaving are inferences from precedents, labelled so in the research file; the political cost is small in any case ({b(X[(1, R10)], 2, False)} today at 10.5%) because it falls after 2045.</li>
<li><b>Framing checked against sources:</b> Brazil's Major Non-NATO Ally designation ({FRAMING["mnna"]}, <a href="https://www.govinfo.gov/content/pkg/FR-2019-08-19/html/2019-17998.htm">Federal Register</a>); the China wording of the {FRAMING["nss"]} National Security Strategy (<a href="https://www.brookings.edu/articles/how-china-reads-the-2025-u-s-national-security-strategy">Brookings</a>, <a href="https://www.cfr.org/expert-brief/unpacking-trump-twist-national-security-strategy">CFR</a>); COMAC's listing as a Chinese military company ({FRAMING["1260h"]}, <a href="https://aviationweek.com/defense/budget-policy-operations/pentagon-identifies-comac-chinese-military-contractor">Aviation Week</a>); the Supreme Court's IEEPA ruling ({FRAMING["ieepa"]}, <a href="https://www.thompsoncoburn.com/insights/65-february-20-2026-supreme-court-issues-ruling-on-ieepa-tariffs/">Thompson Coburn</a>).</li>
<li><b>Sources:</b> {n_find} findings from six research sweeps (Washington and jobs, brand, China, Brazil and Embraer, governments and national champions, decision practice), with the model design and two adversarial checks, in data/politics_research.json. Many web facts rest on search excerpts because the hosts blocked fetching; the file marks each finding's confidence.</li>
<li><b>Files:</b> politics.py writes data/politics.json; make_politics_html.py builds this page and asserts its claims against it.</li>
</ul></div></section>
<footer>BOEING PROPRIETARY. Built by make_politics_html.py from run dash-2050-phaseout.</footer></div>
<script>{K.JS}</script></body></html>'''
    for bad in ("Milk", "Sabotage", "C3_", "c_gov", "exit_p", " his ", " he ", " she ", " her "):
        assert bad not in page, bad
    with open(out_path, "w") as f:
        f.write(page)
    print("wrote", out_path, len(page))


if __name__ == "__main__":
    build(os.path.join(HERE, "fps_politics.html"))
