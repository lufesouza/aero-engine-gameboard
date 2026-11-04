"""Build dash_2050_emb.html: the MAX phase-out game replayed with Embraer as a sixth player (its new narrowbody with
Team Korea, in service four years after launch: slightly better than the 737 MAX and A320neo, worse than fps or NGSA)
and political terms in the payoffs. Boeing's financials, the market by maker, how Boeing, Airbus and Embraer decided
each round, what Embraer's choice did, the politics, and the comparison with the previous game (dash-2050-phaseout).

Reads data/emb.json (extract_emb.py), data/what_if.json (what_if.py) and the round records under record/
(exco_result_rN.json). Every figure on the page comes from those files.

  python3 make_emb_html.py [out.html]
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050-obj"))
import page_kit as K  # noqa: E402

esc = K.esc
J = lambda n: json.load(open(os.path.join(HERE, "data", n)))
D = J("emb.json")
C, P = D["run"], D["prev"]
W = J("what_if.json") if os.path.exists(os.path.join(HERE, "data", "what_if.json")) else None
RECDIR = os.environ.get("EMB_RECORD", os.path.join(HERE, "record"))
REC = lambda n: json.load(open(os.path.join(RECDIR, "exco_result_r%d.json" % n)))["sides"]
SIDES = C["sides"]
NAME = {"boeing": "Boeing", "airbus": "Airbus", "cfm": "CFM/GE", "pratt_whitney": "Pratt & Whitney",
        "rolls_royce": "Rolls-Royce", "embraer": "Embraer"}
EMB = "embraer" in SIDES
YEARS = [r["year"] for r in C["rounds"]]
NR = len(C["rounds"])
FIN = {r["year"]: r for r in C["boeing_fin"]}
PFIN = {r["year"]: r for r in P["boeing_fin"]}
MK = {r["year"]: r for r in C["market"]}
PMK = {r["year"]: r for r in P["market"]}
KEY = [2030, 2035, 2040, 2045, 2050, 2055, 2060]
EMB_OPT = C["options"].get("embraer_player", {})
POL = C["options"].get("politics", {})
DEFAULTS = {"hold", None, "none", "new_site", "base"}
EMB_DLV = EMB and any(r["embraer"] > 0.5 for r in C["market"])      # Embraer delivered anything in the final state


def b(v, dp=2, sign=True):
    return K.usd(v, dp, sign and K.rnd(v, dp) != 0)


def bp(v, dp=2, sign=True):
    return re.sub(r"<[^>]+>", "", b(v, dp, sign))


def n0(v):
    return f"{K.rnd(v or 0.0, 0):,.0f}"


def pc(v, dp=1):
    return f"{K.rnd(100 * (v or 0.0), dp):.{dp}f}%"


CODES = [(r"`?fps:\s*launch_10yr`?", "the 10-year fps"), (r"`?fps:\s*launch_7yr`?", "the 7-year fps"),
         (r"`?fps:\s*launch_via_embraer`?", "the fps via Embraer"), (r"`?fps:\s*hold`?", "fps held"), (r"`?fps:\s*cancel`?", "fps cancelled"),
         (r"`?re787:\s*launch`?", "the 787 Re-engine"), (r"`?re787:\s*hold`?", "787 held"), (r"`?rate_737:\s*increase`?", "the 737 rate increase"),
         (r"`?rate_737:\s*hold`?", "737 rate held"), (r"`?rea350:\s*launch`?", "the A350 Re-engine"), (r"`?rea350:\s*hold`?", "A350 held"),
         (r"`?ngsa:\s*launch`?", "the NGSA launch"), (r"`?ngsa:\s*hold`?", "NGSA continuing"), (r"`?ngsa:\s*cancel`?", "cancelling NGSA"),
         (r"`?a320_plan:\s*alt`?", "the A320 Alt plan"), (r"`?a320_plan:\s*base`?", "the A320 base plan"),
         (r"`?delay_tactics:\s*(none|bottleneck|poaching|both)`?", "Delay Tactics (\\1)"), (r"`?enb:\s*launch`?", "the Embraer launch"),
         (r"`?enb:\s*hold`?", "Embraer holding"), (r"`?jv_with_(?:pw|rr):\s*commit`?", "the Joint Venture commitment"),
         (r"`?jv_with_(?:pw|rr):\s*hold`?", "no Joint Venture move"), (r"`?jv_with_(?:pw|rr):\s*withdraw`?", "withdrawing from the Joint Venture"),
         (r"`?gtf2_solo:\s*launch_if_selected`?", "GTF2 if selected"), (r"`?gtf2_solo:\s*hold`?", "GTF2 held"),
         (r"`?ultrafan_nb_solo:\s*launch_if_selected`?", "UltraFan NB if selected"), (r"`?ultrafan_nb_solo:\s*hold`?", "UltraFan NB held"),
         (r"`?fps_engine_code`?", "fps engine code"), (r"`?ngsa_engine_code`?", "NGSA engine code"), (r"`?fps_site`?", "fps site"),
         (r"\bnew_site\b", "new sites"), (r"\bngsa\b", "NGSA"), (r"`?premium_b`?", "premium"), (r"`?board_response`?", "Board response"),
         (r"`?launch_if_selected`?", "launch if selected"), (r"`?launch_10yr`?", "10-year launch"), (r"`?launch_7yr`?", "7-year launch"),
         (r"`?launch_via_embraer`?", "launch via Embraer"), (r"`?(re787|rea350|rate_737|delay_tactics|a320_plan|jv_with_pw|jv_with_rr|gtf2_solo|ultrafan_nb_solo|ultrafan_wb|t1000_upgrade|partner_embraer|lobby_emissions|open_fan|ducted|enb)`?",
                                                                                  lambda m: {"re787": "787 Re-engine", "rea350": "A350 Re-engine", "rate_737": "737 rate", "delay_tactics": "Delay Tactics",
                                                                                             "a320_plan": "A320 plan", "jv_with_pw": "Joint Venture", "jv_with_rr": "Joint Venture", "gtf2_solo": "GTF2",
                                                                                             "ultrafan_nb_solo": "UltraFan NB", "ultrafan_wb": "UltraFan WB", "t1000_upgrade": "Trent 1000 upgrade",
                                                                                             "partner_embraer": "Embraer partnership", "lobby_emissions": "emissions lobbying", "open_fan": "Open Fan",
                                                                                             "ducted": "Ducted engine", "enb": "Embraer's new narrowbody"}[m.group(1)])]


def clean(t):
    """Agent prose for the page: no order codes or evidence ids, no code ticks."""
    t = re.sub(r"\s*\[(?:[A-Z]{1,3}X?G?-\d{3,4}(?:,\s*)?)+[^\]]*\]", "", str(t or ""))
    t = re.sub(r"\((?:inference|research, unverified)\)", "", t)
    for pat, sub in CODES:
        t = re.sub(pat, sub, t)
    # people's pronouns are not stated in the sources: name the thing instead, or use they/them
    for pat, sub in ((r"\bHe reads his test\b", "The CFO reads the test"), (r"\b(?:his|her) (memo|correction|test|expected column|veto|tests|view|record)\b", r"the \1"),
                     (r"\b(?:with|from|to|for) (?:him|her)\b", lambda m: m.group(0).split()[0] + " them"),
                     (r"\b(?:his|her)\b", "their"), (r"\b(?:He|She)\b", "They"), (r"\b(?:he|she)\b", "they"), (r"\b(?:him)\b", "them")):
        t = re.sub(pat, sub, t)
    return t.replace("`", "")


def short(t, n=320):
    t = re.sub(r"\s+", " ", clean(t)).strip()
    if len(t) <= n:
        return t
    cut = t[:n]
    k = max(cut.rfind(". "), cut.rfind("; "))
    return (cut[:k + 1] if k > n * 0.5 else cut.rsplit(" ", 1)[0] + " …")


# ─────────────────────────────── orders ───────────────────────────────
ORDER_TXT = {
    "boeing": {"fps": {"launch_7yr": "fps, 7-year", "launch_10yr": "fps, 10-year", "launch_via_embraer": "fps via Embraer", "cancel": "cancel fps"},
               "rate_737": {"increase": "737 rate up"}, "re787": {"launch": "787 Re-engine", "cancel": "cancel 787 Re-engine"},
               "fps_site": {"renton": "fps at Renton"}},
    "airbus": {"ngsa": {"launch": "NGSA", "cancel": "cancel NGSA"}, "rea350": {"launch": "A350 Re-engine", "cancel": "cancel A350 Re-engine"},
               "delay_tactics": {"bottleneck": "Delay Tactics", "poaching": "Delay Tactics", "both": "Delay Tactics (both)"},
               "a320_plan": {"alt": "A320 Alt plan"}},
    "cfm": {"ducted": {"launch": "Ducted engine", "cancel": "cancel Ducted"}, "open_fan": {"launch": "Open Fan", "cancel": "cancel Open Fan"},
            "partner_embraer": {"launch": "Embraer partnership", "cancel": "end Embraer partnership"},
            "lobby_emissions": {"launch": "emissions lobbying"}, "genx": {"upgrade_genx9": "GEnx upgrade", "invest_genx": "GEnx investment", "cancel": "cancel GEnx"}},
    "pratt_whitney": {"gtf2_solo": {"launch": "GTF2", "launch_if_selected": "GTF2 if selected", "cancel": "cancel GTF2"},
                      "jv_with_rr": {"commit": "commits to the Joint Venture", "withdraw": "withdraws from the Joint Venture"}},
    "rolls_royce": {"ultrafan_nb_solo": {"launch": "UltraFan NB", "launch_if_selected": "UltraFan NB if selected", "cancel": "cancel UltraFan NB"},
                    "jv_with_pw": {"commit": "commits to the Joint Venture", "withdraw": "withdraws from the Joint Venture"},
                    "ultrafan_wb": {"launch": "UltraFan WB", "cancel": "cancel UltraFan WB"}, "t1000_upgrade": {"launch": "Trent 1000 upgrade"}},
    "embraer": {"enb": {"launch": "new narrowbody with Korea", "cancel": "cancel new narrowbody"}},
}
CODE = {1: "RR", 2: "P&W", 3: "CFM", 4: "RR & P&W Joint Venture", 5: "RR and CFM", 6: "P&W and CFM", 7: "all three makers"}


def move_list(side, o):
    out = []
    for f, val in o.items():
        if f.endswith("_engine_code") or val in DEFAULTS:
            continue
        t = ORDER_TXT.get(side, {}).get(f, {}).get(val, f"{f}: {val}")
        if f in ("fps", "ngsa") and val.startswith("launch") and o.get(f + "_engine_code"):
            t += f" (engines: {CODE[int(o[f + '_engine_code'])]})"
        out.append(t)
    return out


def move_txt(side, o):
    m = move_list(side, o)
    return ", ".join(m) if m else "Do Nothing"


def moves_table(R):
    head = ["Round"] + [NAME[s] for s in SIDES]
    rows = [[f"{r['year']}"] + [esc(move_txt(s, r["orders"][s])) for s in SIDES] for r in R["rounds"]]
    return K.table(head, rows).replace("<table>", '<table class="moves">', 1)


# ─────────────────────────────── charts ───────────────────────────────
def lc(series, lo, hi, step, fmt, label, aria, end_labels, refs=(), notes=(), x_hi=2063):
    return K.line_chart(series, lo, hi, step, fmt, label, list(refs), aria, end_labels, list(notes), x_lo=2026, x_hi=x_hi)


def spread(vals, gap=22, span=(30, 300)):
    """End-label offsets so labels at the right edge do not collide and stay inside the plot: vals are y positions."""
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    pos = [vals[i] for i in order]
    for k in range(1, len(pos)):
        pos[k] = max(pos[k], pos[k - 1] + gap)
    over = pos[-1] - span[1] if pos else 0
    if over > 0:
        pos = [max(span[0], x - over) for x in pos]
        for k in range(1, len(pos)):
            pos[k] = max(pos[k], pos[k - 1] + gap)
    off = [0.0] * len(vals)
    for k, i in enumerate(order):
        off[i] = pos[k] - vals[i]
    return off


def profit_chart():
    ys = list(range(2026, 2061))
    s_c = [(y, FIN[y]["profit"]) for y in ys]
    s_p = [(y, PFIN[y]["profit"]) for y in ys]
    s_q = [(y, C["status_quo"]["boeing_profit"][y - 2026]) for y in ys]
    hi = max(v for _, v in s_c + s_p + s_q)
    hi = (int(hi / 2) + 1) * 2
    yfun = lambda v: 26 + (hi - v) / hi * (346 - 26 - 46)
    offs = spread([yfun(s[-1][1]) for s in (s_c, s_p, s_q)])
    return lc([("Status quo", "s2", s_q), ("Previous game", "muted", s_p), ("This game", "s1", s_c)], 0, hi, 2, "int",
              "Boeing commercial operating profit, $B a year (2026 prices)", "Boeing's operating profit by year, this game, the previous game and the status quo",
              [(offs[2], "Status quo"), (offs[1], "Previous game"), (offs[0], "This game")])


def debt_chart():
    ys = [y for y in range(2027, 2061) if FIN[y]["debt"] is not None]
    s_c = [(y, FIN[y]["debt"]) for y in ys]
    s_s = [(y, FIN[y]["debt_stress"]) for y in ys]
    s_p = [(y, PFIN[y]["debt"]) for y in ys if PFIN[y]["debt"] is not None]
    lo = min(v for _, v in s_c + s_s + s_p)
    lo = (int(lo / 25) - 1) * 25 if lo < 0 else 0
    hi = max(25, (int(max(v for _, v in s_c + s_s + s_p) / 25) + 1) * 25)
    yfun = lambda v: 26 + (hi - v) / (hi - lo) * (346 - 26 - 46)
    offs = spread([yfun(s[-1][1]) for s in (s_c, s_s, s_p)])
    return lc([("This game", "s1", s_c), ("Stress case", "s2", s_s), ("Previous game", "muted", s_p)], lo, hi, 25, "int",
              "Boeing net debt at year end, $B (2026 prices)", "Boeing's net debt path, this game, its stress case and the previous game",
              [(offs[0], "This game"), (offs[1], "Stress case"), (offs[2], "Previous game")],
              refs=[(C["debt_inputs"]["historical_level_b"], "Historical level", "above")] if abs(C["debt_inputs"]["historical_level_b"]) > 1e-9 else [])


def deliveries_chart(narrow=False):
    w, h, left, right, top, bot = (360, 300, 44, 22, 20, 44) if narrow else (760, 330, 54, 16, 20, 44)
    ys = list(range(2026, 2061))
    segs_def = [("boeing", "s1", "Boeing"), ("airbus", "s2", "Airbus"), ("comac", "comac", "COMAC"), ("embraer", "s3", "Embraer")]
    val = lambda m, k: (m["max"] + m["fps"]) if k == "boeing" else (m["a320"] + m["ngsa"]) if k == "airbus" else m[k]
    top_v = max(max(MK[y]["demand"] or 0, sum(val(MK[y], k) for k, _, _ in segs_def)) for y in ys)
    hi = (int(top_v / 500) + 1) * 500
    bw = (w - left - right) / len(ys)
    sx = lambda y: left + (y - ys[0] + 0.5) * bw
    sy = lambda v: top + (hi - v) / hi * (h - top - bot)
    out = [K.svg_open(w, h, "Single-aisle aircraft delivered each year by maker, final state of this game", "chart narrow" if narrow else "chart")]
    v = 0
    while v <= hi:
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" class="grid"/><text x="{left - 6}" y="{sy(v) + 4:.1f}" text-anchor="end" class="tick">{n0(v)}</text>')
        v += 500
    for y in ys:
        m = MK[y]
        acc = 0.0
        segs = [(k, var) for k, var, _ in segs_def if val(m, k) > 0.5]
        for j, (k, var) in enumerate(segs):
            x = val(m, k)
            y0, y1 = sy(acc), sy(acc + x)
            gap = 1.0 if j else 0.0
            if j == len(segs) - 1:
                out.append(f'<path d="{K.bar_path(sx(y) - bw * 0.38, bw * 0.76, y0 - gap, y1)}" fill="var(--{var})"/>')
            else:
                out.append(f'<rect x="{sx(y) - bw * 0.38:.1f}" width="{bw * 0.76:.1f}" y="{y1 + 1:.1f}" height="{max(0.0, y0 - y1 - 1 - gap):.1f}" fill="var(--{var})"/>')
            acc += x
        out.append(f'<rect x="{sx(y) - bw / 2:.1f}" width="{bw:.1f}" y="{top}" height="{h - top - bot}" class="hit" '
                   + K.mark_attrs((str(y), "", None), (n0(m["max"] + m["fps"]), "Boeing (MAX + fps)", "var(--s1)"),
                                  (n0(m["a320"] + m["ngsa"]), "Airbus (A320 + NGSA)", "var(--s2)"), (n0(m["comac"]), "COMAC", "var(--comac)"),
                                  (n0(m["embraer"]), "Embraer", "var(--s3)"), (n0(m["lost"] or 0), "Customers lost", None),
                                  (n0(m["demand"] or 0), "Demand", None)) + "/>")
    d = "M" + " L".join(f"{sx(y):.1f},{sy(MK[y]['demand'] or 0):.1f}" for y in ys)
    out.append(f'<path d="{d}" fill="none" stroke="var(--fg)" stroke-width="2" pointer-events="none"/>')
    for y in ys:
        if y % (10 if narrow else 5) == 0:
            out.append(f'<text x="{sx(y):.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick">{y}</text>')
    out.append(f'<text x="{left}" y="{h - 6}" class="tick">{"Aircraft a year" if narrow else "737/A320-class aircraft delivered a year (bars) and demand (line), final state"}</text></svg>')
    return "".join(out)


def share_chart():
    ys = list(range(2026, 2061))
    ser = [("Boeing", "s1", [(y, MK[y]["sh_boeing"]) for y in ys]), ("Airbus", "s2", [(y, MK[y]["sh_airbus"]) for y in ys]),
           ("COMAC", "comac", [(y, MK[y]["sh_comac"]) for y in ys])]
    if EMB_DLV:
        ser.append(("Embraer", "s3", [(y, MK[y]["sh_embraer"]) for y in ys]))
    ser.append(("Boeing (prev.)", "muted", [(y, PMK[y]["sh_boeing"]) for y in ys]))
    yfun = lambda v: 26 + (0.8 - v) / 0.8 * (346 - 26 - 46)
    offs = spread([yfun(s[2][-1][1]) for s in ser])
    return lc(ser, 0, 0.8, 0.2, "pct", "Share of single-aisle deliveries", "Single-aisle delivery shares by maker, final state",
              [(o, s[0]) for o, s in zip(offs, ser)])


# ─────────────────────────────── tables ───────────────────────────────
def fin_table():
    head = ["Year", "NB deliveries", "WB deliveries", "Revenue $B", "Operating profit $B", "Status-quo profit $B",
            "Programme cash $B", "Free cash flow $B", "Net debt $B", "Cash for owners $B", "Net debt, stress $B", "Net debt, previous game $B"]
    rows = []
    for y in KEY:
        f, p_ = FIN[y], PFIN[y]
        rows.append([str(y), n0(f["nb_units"]), n0(f["wb_units"]), f"{f['revenue']:.1f}", f"{f['profit']:.1f}", f"{f['sq_profit']:.1f}",
                     f"{f['spend']:.1f}" if f["spend"] else "—", K.num(f["fcf"], "+.1f") if f["fcf"] is not None else "—",
                     f"{f['debt']:.1f}" if f["debt"] is not None else "—", f"{f['owners']:.1f}" if f.get("owners") is not None else "—",
                     f"{f['debt_stress']:.1f}" if f["debt_stress"] is not None else "—",
                     f"{p_['debt']:.1f}" if p_["debt"] is not None else "—"])
    return K.table(head, rows, num_cols=tuple(range(1, len(head))))


def share_table():
    head = ["Year", "Demand", "Boeing", "of which fps", "Airbus", "of which NGSA", "COMAC"] + (["Embraer"] if EMB_DLV else []) + \
           ["Boeing share", "Airbus share", "COMAC share"] + (["Embraer share"] if EMB_DLV else []) + ["Boeing share, previous game", "Boeing widebody share"]
    rows = []
    for y in KEY:
        m, q = MK[y], PMK[y]
        r = [str(y), n0(m["demand"]), n0(m["max"] + m["fps"]), n0(m["fps"]), n0(m["a320"] + m["ngsa"]), n0(m["ngsa"]), n0(m["comac"])]
        r += [n0(m["embraer"])] if EMB_DLV else []
        r += [pc(m["sh_boeing"]), pc(m["sh_airbus"]), pc(m["sh_comac"])] + ([pc(m["sh_embraer"])] if EMB_DLV else []) + [pc(q["sh_boeing"]), pc(m["wb_boeing"])]
        rows.append(r)
    return K.table(head, rows, num_cols=tuple(range(1, len(head))))


BRIDGE_LBL = {"nb_profit_vs_sq": "Narrowbody profit against the status quo (the board's market)", "wb_profit_vs_sq": "Widebody profit against the status quo",
              "programme_investment": "Programme investment", "rate_hike": "737 rate increase", "delay_tactics_spend": "Delay Tactics spend",
              "write_offs": "Write-offs", "debt_penalty": "Debt penalty", "two_front_strain": "Two-front strain", "naked_fine": "Naked Delay Tactics fine",
              "supply_demand": "Supply and demand: what the factories deliver, and Embraer's price pressure", "supply_plan": "Supply plan",
              "government_cofunding": "Politics: governments carry part of the fps bill",
              "political_exit_cost": "Politics: the cost of leaving the narrowbody market"}


def bridge_table(br, prev=None):
    keys = [k for k in br if abs(br[k]) > 1e-9 or (prev and abs(prev.get(k, 0.0)) > 1e-9)]
    head = ["Component", "This game"] + (["Previous game"] if prev else [])
    rows = [[esc(BRIDGE_LBL.get(k, k)), b(br[k])] + ([b(prev.get(k, 0.0))] if prev else []) for k in keys]
    rows.append(["<b>Boeing ΔPV</b>", f"<b>{b(sum(br.values()))}</b>"] + ([f"<b>{b(sum(prev.values()))}</b>"] if prev else []))
    return K.table(head, rows, num_cols=(1, 2))


def value_table():
    head = ["Company"] + [f"After {y}" for y in YEARS] + ["Previous game, final"]
    rows = []
    for s in SIDES:
        rows.append([NAME[s]] + [b(r["value"][s]) for r in C["rounds"]] + [b(P["rounds"][-1]["value"][s]) if s in P["rounds"][-1]["value"] else "—"])
    return K.table(head, rows, num_cols=tuple(range(1, len(head))))


# ─────────────────────────────── decision chains ───────────────────────────────
SEATS = {"boeing": ("Kelly Ortberg", "Jay Malave", "Stephanie Pope"), "airbus": ("Guillaume Faury", "Thomas Toepfer", "Lars Wagner"),
         "embraer": ("Francisco Gomes Neto", "Felipe Santana", "Arjan Meijer")}


def tests_list(memo):
    if not memo:
        return "<p class=muted>No memo returned.</p>"
    items = []
    for t in memo.get("tests", [])[:6]:
        res = t.get("result", "")
        cls = {"pass": "pos", "fail": "neg"}.get(res, "muted")
        items.append(f'<li><span class="tag {cls}">{esc(res)}</span> <b>{esc(short(t.get("name", ""), 90))}</b>: {esc(short(t.get("numbers", ""), 220))}</li>')
    vet = [v for v in memo.get("vetoes", []) if v]
    vtxt = "".join(f'<li><span class="tag neg">veto{" (binding)" if v.get("binding") else ""}</span> {esc(short(v.get("plan", ""), 100))}: {esc(short(v.get("ground", ""), 200))}</li>' for v in vet[:3])
    return f'<ul class="tl">{"".join(items)}{vtxt}</ul><p class="memo">{esc(short(memo.get("memo", ""), 520))}</p>'


def chain(side, n):
    x = REC(n).get(side)
    if not x:
        return "<p>No record.</p>"
    ceo, cfo, ops = SEATS[side]
    g, fr, dec = x.get("board_guidance") or {}, x.get("frame") or {}, x.get("final") or x.get("decision") or {}
    bits = []
    if g:
        bits.append(f'<div class="step"><p class="sh">1 · Board guidance</p><p><b>Risk appetite:</b> {esc(short(g.get("risk_appetite", ""), 360))}</p>'
                    f'<p><b>First priority:</b> {esc(short((g.get("priorities") or [""])[0], 360))}</p>'
                    f'<p><b>Would veto:</b> {esc(short("; ".join(short(v, 140) for v in (g.get("would_veto") or [])[:3]), 480))}</p></div>')
    bits.append(f'<div class="step"><p class="sh">2 · {esc(ceo)} (CEO) frames the round</p><p><b>Question:</b> {esc(short(fr.get("question", ""), 300))}</p>'
                f'<p><b>Initial lean:</b> {esc(short(fr.get("initial_lean", ""), 420))}</p></div>')
    bits.append(f'<div class="step"><p class="sh">3 · {esc(cfo)} (CFO) tests it</p>{tests_list(x.get("cfo"))}</div>')
    bits.append(f'<div class="step"><p class="sh">3 · {esc(ops)} (operating head) tests it</p>{tests_list(x.get("ops"))}</div>')
    d0 = x.get("decision") or {}
    bits.append(f'<div class="step"><p class="sh">4 · {esc(ceo)} decides</p><p><b>Orders:</b> {esc(move_txt(side, d0.get("orders", {})))}</p>'
                f'<p><b>Expected column:</b> {esc(short(d0.get("expected_scenario", ""), 260))}</p>'
                f'<p><b>Best grid plan there:</b> {esc(short(d0.get("best_grid_plan_in_expected_scenario", ""), 220))}'
                + (f' · premium {b(d0.get("premium_b"), 2, False)}' if d0.get("premium_b") else "") + "</p>"
                f'<p class="memo">{esc(short(d0.get("rationale", ""), 700))}</p></div>')
    vc = x.get("veto_checks") or {}
    vtxt = []
    for seat, nm in (("cfo", cfo), ("ops", ops)):
        v = vc.get(seat) or {}
        if v:
            state = "concurs" if v.get("concur") else ("vetoes" + (" (binding)" if (v.get("veto") or {}).get("binding") else ""))
            vtxt.append(f"<li><b>{esc(nm)}</b> {state}{': ' + esc(short(v.get('note', ''), 220)) if v.get('note') else ''}</li>")
    if x.get("revision"):
        vtxt.append(f"<li><b>Revision:</b> {esc(move_txt(side, x['revision'].get('orders', {})))}. {esc(short(x['revision'].get('rationale', ''), 260))}</li>")
    bits.append(f'<div class="step"><p class="sh">5 · Veto check{" and revision" if x.get("revision") else ""}</p><ul class="tl">{"".join(vtxt)}</ul></div>')
    rv = x.get("board_review") or {}
    items = rv.get("items") or []
    if items:
        it = "".join(f'<li><span class="tag {"pos" if i.get("decision") == "approve" else "neg"}">{esc(i.get("decision", ""))}</span> '
                     f'<b>{esc(clean(str(i.get("order_field", "")) + ": " + str(i.get("value", ""))))}</b>: {esc(short(i.get("ground", ""), 260))}</li>' for i in items)
    else:
        it = f'<li>{esc(rv.get("note", "No Board items: every order is the default."))}</li>'
    if x.get("board_revision"):
        it += f"<li><b>CEO revises within the veto:</b> {esc(move_txt(side, x['board_revision'].get('orders', {})))}</li>"
    if x.get("board_reverted"):
        it += f"<li><b>Reverted to the default:</b> {esc(', '.join(clean(k) for k in x['board_reverted']))}</li>"
    bits.append(f'<div class="step"><p class="sh">6 · Board review</p><ul class="tl">{it}</ul></div>')
    bits.append(f'<div class="step final"><p class="sh">Sealed orders</p><p><b>{esc(move_txt(side, x.get("final_orders", {})))}</b></p></div>')
    return '<div class="chain">' + "".join(bits) + "</div>"


def chains_section(side):
    blocks = []
    for r in C["rounds"]:
        n = r["round"]
        blocks.append(f'<details class="panel rnd"{" open" if n == 1 else ""}><summary><b>{r["year"]}</b> · {esc(move_txt(side, r["orders"][side]))}</summary>{chain(side, n)}</details>')
    return "".join(blocks)


CSS_EXTRA = """
:root { --comac: #8a5cc4; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --comac: #9b6fd6; } }
:root[data-theme="dark"] { --comac: #9b6fd6; }
.scroll { background:
    linear-gradient(to right, var(--surface) 40%, transparent) left / 32px 100% no-repeat local,
    linear-gradient(to left, var(--surface) 40%, transparent) right / 32px 100% no-repeat local,
    linear-gradient(to right, color-mix(in srgb, var(--fg) 22%, transparent), transparent) left / 14px 100% no-repeat scroll,
    linear-gradient(to left, color-mix(in srgb, var(--fg) 22%, transparent), transparent) right / 14px 100% no-repeat scroll; }
.scroll > table { background: transparent; }
ul.cav li, footer { overflow-wrap: anywhere; }
.legend .solid { display: inline-block; width: 18px; height: 0; border-top: 2px solid var(--fg); vertical-align: middle; margin-right: 6px; }
.legend .dash { display: inline-block; width: 18px; height: 0; border-top: 2px dashed var(--muted); vertical-align: middle; margin-right: 6px; }
.chain { display: grid; gap: 10px; margin-top: 10px; }
.step { border-left: 3px solid var(--line); padding: 2px 0 2px 12px; }
.step.final { border-left-color: var(--s1); }
.step .sh { font: 600 12px var(--font-mono); text-transform: uppercase; letter-spacing: .04em; color: var(--muted); margin: 0 0 4px; }
.step p { margin: 4px 0; } .memo { color: var(--muted); }
ul.tl { margin: 4px 0; padding-left: 18px; } ul.tl li { margin: 3px 0; }
.tag { font: 600 11px var(--font-mono); text-transform: uppercase; padding: 1px 6px; border-radius: 4px; border: 1px solid currentColor; }
.tag.pos { color: var(--pos); } .tag.neg { color: var(--neg); } .tag.muted { color: var(--muted); }
details.rnd > summary { cursor: pointer; } details.rnd { margin-bottom: 10px; }
.chart path[stroke="var(--muted)"] { stroke-dasharray: 5 4; }
@media (max-width: 760px) { .moves thead { display: none; } .moves, .moves tbody, .moves tr, .moves th, .moves td { display: block; width: auto; }
  .moves tr { border-bottom: 1px solid var(--line); padding: 8px 0; } .moves td { border: 0; padding: 2px 0; }
  .moves td::before { display: block; font: 600 11px var(--font-mono); color: var(--muted); text-transform: uppercase; letter-spacing: .04em; } }
"""


def moves_css():
    return "".join(f'.moves td:nth-of-type({i + 1})::before {{ content: "{NAME[s]}"; }} ' for i, s in enumerate(SIDES))


# ─────────────────────────────── what Embraer's choice did ───────────────────────────────
def emb_flip_table():
    if not W:
        return ""
    pl, fl = W["played"], W["flipped"]
    head = ["Company", "As played", "If Embraer had " + ("held" if W["embraer_2030_order"] == "launch" else "launched") + " in 2030", "Difference"]
    rows = [[NAME[s], b(pl["value"][s]), b(fl["value"][s]), b(fl["value"][s] - pl["value"][s])] for s in SIDES]
    return K.table(head, rows, num_cols=(1, 2, 3))


def emb_flip_market():
    if not W:
        return ""
    pl, fl = W["played"], W["flipped"]
    head = ["Year", "Embraer deliveries", "Boeing deliveries, as played", "Boeing deliveries, with Embraer", "Boeing's price cut", "Boeing profit change $B",
            "Boeing net debt, as played", "with Embraer"]
    rows = []
    for y in KEY:
        k = str(y)
        rows.append([k, n0(fl["embraer_units"][k]), n0(pl["boeing_nb_units"][k]), n0(fl["boeing_nb_units"][k]), pc(fl["boeing_cut"][k]),
                     K.num(fl["boeing_profit"][k] - pl["boeing_profit"][k], "+.2f"),
                     f'{pl["boeing_debt"].get(k, 0.0):.1f}', f'{fl["boeing_debt"].get(k, 0.0):.1f}'])
    return K.table(head, rows, num_cols=tuple(range(1, len(head))))


def break_even_table():
    if not W:
        return ""
    be = W["break_even"]
    o = EMB_OPT
    rows = [["Korea's share of the bill", pc(o["partner_share"], 0), pc(be["partner_share"], 0) if be["partner_share"] is not None else "not reachable",
             f"Embraer's own share falls from {pc(be['own_share'], 0)} to {pc(1 - be['partner_share'] - o['supplier_share'] - o['state_share'], 0)}" if be["partner_share"] is not None else ""],
            ["Operating margin", pc(o["margin"], 0), pc(be["margin"], 1) if be["margin"] is not None else "not reachable", "against 13% on the A320neo and 26% on a new-generation type"],
            ["Line peak rate (a month)", f"{o['peak_a_month']:.0f}", f"{be['peak_a_month']:.0f}" if be["peak_a_month"] is not None else "not reachable", "Embraer's best was about 9 E-Jets a month"],
            ["Development bill", f"${o['bill_b']:.1f}B", f"${be['bill_b']:.1f}B" if be["bill_b"] is not None else "not reachable", "with the same 55% own share"],
            ["No US tariff cut", f"{pc(o['us_tariff_share_cut'], 0)} fewer customers", b(be["no_tariff"]), "Embraer's line is full anyway, so the tariff barely matters"]]
    return K.table(["Lever (one at a time)", "This game", "Break-even", "Note"], rows, num_cols=(1, 2))


# ─────────────────────────────── per-round decision summaries ───────────────────────────────
def col_index(txt, n):
    m = re.search(r"\bS(\d+)\b", txt or "")
    return int(m.group(1)) - 1 if m else 0


def grid(n, side):
    return C["grids"][str(n)][side]


def row(n, side, plan):
    for r in grid(n, side)["rows"]:
        if r["plan"] == plan:
            return r["cells"]
    return None


def boeing_round_rows():
    out = []
    for r in C["rounds"]:
        n = r["round"]
        g = grid(n, "boeing")
        x = REC(n)["boeing"]
        j = col_index((x.get("decision") or {}).get("expected_scenario"), n)
        dn = row(n, "boeing", "fps: hold + 787: hold")
        fps = [(p["plan"], p["cells"][j] - dn[j]) for p in g["rows"] if p["plan"].startswith("fps ") and "787: hold" in p["plan"] and "Embraer" not in p["plan"]]
        bf = max(fps, key=lambda t: t[1]) if fps else ("—", 0.0)
        re_ = row(n, "boeing", "fps: hold + 787 Re-engine")
        re_gap = (re_[j] - dn[j]) if re_ else None
        re_worst = min(a - b_ for a, b_ in zip(re_, dn)) if re_ else None
        emb_col = [k for k, s in enumerate(g["scenarios"]) if s.startswith("Embraer launches")]
        emb_hit = (dn[emb_col[0]] - dn[0]) if emb_col else None
        vet = [(s, v.get("plan", "")) for s in ("cfo", "ops") for v in ((x.get(s) or {}).get("vetoes") or []) if v.get("binding")]
        out.append({"year": r["year"], "expected": g["scenarios"][j], "best_fps": bf, "re787": re_gap, "re787_worst": re_worst,
                    "emb_hit": emb_hit, "vetoes": vet, "board_items": x.get("board_items") or [], "board_vetoed": x.get("board_vetoed") or [],
                    "orders": r["orders"]["boeing"]})
    return out


def airbus_round_rows():
    out = []
    for r in C["rounds"]:
        n = r["round"]
        g = grid(n, "airbus")
        x = REC(n)["airbus"]
        j = col_index((x.get("decision") or {}).get("expected_scenario"), n)
        best = max(g["rows"], key=lambda p: p["cells"][j])
        out.append({"year": r["year"], "expected": g["scenarios"][j], "best": (best["plan"], best["cells"][j]),
                    "chosen": move_txt("airbus", r["orders"]["airbus"]), "board_items": x.get("board_items") or [],
                    "board_vetoed": x.get("board_vetoed") or []})
    return out


def embraer_round_rows():
    out = []
    for r in C["rounds"]:
        n = r["round"]
        g = grid(n, "embraer")
        la = row(n, "embraer", "Launch the new narrowbody with Korea")
        x = REC(n)["embraer"]
        out.append({"year": r["year"], "launch": la, "scen": g["scenarios"], "chosen": move_txt("embraer", r["orders"]["embraer"]),
                    "cfo": [(t.get("name", ""), t.get("result", "")) for t in (x.get("cfo") or {}).get("tests", [])[:3]],
                    "ops_window": next((t.get("result") for t in (x.get("ops") or {}).get("tests", []) if "window" in t.get("name", "").lower()), "")})
    return out


VETO_PLAN = {"launch_10yr": "10-year", "launch_7yr": "7-year", "launch_via_embraer": "via Embraer"}


def veto_txt(vs):
    if not vs:
        return "none"
    by = {}
    for seat, plan in vs:
        m = re.search(r"fps: (launch_\w+)", plan)
        by.setdefault(seat, []).append(VETO_PLAN.get(m.group(1), m.group(1)) if m else short(plan, 40))
    seat_lbl = {"cfo": "CFO's buffer test", "ops": "operating head's KPI test"}
    return "; ".join(f"{seat_lbl[k]} on the fps {', '.join(dict.fromkeys(v))}" for k, v in by.items())


def board_txt(x):
    f = lambda xs: ", ".join(clean(k) for k in xs)
    return ("vetoed " + f(x["board_vetoed"])) if x["board_vetoed"] else ("approved " + f(x["board_items"])) if x["board_items"] else "no Board item"


def plan_lbl(p):
    p = p.replace(" + 787: hold", "").replace("fps 10-yr", "10-year fps").replace("fps 7-yr", "7-year fps")
    return p.replace("NGSA: hold", "NGSA continuing").replace("A350: hold", "A350 held")


def boeing_summary_table(rows):
    head = ["Round", "CEO's expected column", "Best fps against Do Nothing there", "787 Re-engine against Do Nothing (worst column)",
            "Embraer's launch would cost Boeing", "Binding vetoes raised in the tests", "Board", "Orders"]
    body = []
    for x in rows:
        body.append([str(x["year"]), esc(x["expected"]), f'{esc(plan_lbl(x["best_fps"][0]))}: {b(x["best_fps"][1])}',
                     (f'{b(x["re787"])} ({b(x["re787_worst"])})' if x["re787"] is not None else "—"),
                     (b(x["emb_hit"]) if x["emb_hit"] is not None else "—"),
                     esc(veto_txt(x["vetoes"])),
                     esc(board_txt(x)), esc(move_txt("boeing", x["orders"]))])
    return K.table(head, body, num_cols=(3, 4))


def airbus_summary_table(rows):
    head = ["Round", "CEO's expected column", "Best grid plan there", "Orders", "Board"]
    body = [[str(x["year"]), esc(x["expected"]), f'{esc(plan_lbl(x["best"][0]))}: {b(x["best"][1])}', esc(x["chosen"]),
             esc(board_txt(x))] for x in rows]
    return K.table(head, body)


def embraer_summary_table(rows):
    head = ["Round", "Launch against Do Nothing, by column", "CFO's funding test (legs 1-3)", "Market window (operating head)", "Orders"]
    body = []
    for x in rows:
        cols = "; ".join(f"{esc(s)} {b(v)}" for s, v in zip(x["scen"], x["launch"])) if x["launch"] else "—"
        body.append([str(x["year"]), cols, esc(", ".join(r for _, r in x["cfo"])), esc(x["ops_window"] or "—"), esc(x["chosen"])])
    return K.table(head, body)


# ─────────────────────────────── page ───────────────────────────────
def first_year_at(rows, key, level):
    for r in rows:
        if r.get(key) is not None and r["year"] >= 2027 and r[key] <= level + 1e-9:
            return r["year"]
    return None


def tiles():
    fin = C["rounds"][-1]
    bv = fin["value"]["boeing"]
    pv = P["rounds"][-1]["value"]["boeing"]
    H = C["debt_inputs"]["historical_level_b"]
    rep = first_year_at(C["boeing_fin"], "debt", H)
    er = embraer_round_rows() if EMB else []
    best_emb = max((max(x["launch"]) for x in er if x["launch"]), default=None)
    best_emb_y = next((x["year"] for x in er if x["launch"] and max(x["launch"]) == best_emb), None)
    t = [("Boeing's value, end of game", bp(bv), f"against the status quo (PV at 2026), after four rounds of Do Nothing; {b(pv)} in the previous game"),
         ("Boeing's share of single-aisle deliveries", f"{pc(MK[2030]['sh_boeing'], 0)} → {pc(MK[2050]['sh_boeing'], 0)}",
          f"2030 to 2050, as the MAX phases out and NGSA ramps; {pc(MK[2060]['sh_boeing'], 0)} in 2060"),
         ("Boeing's net debt", f"back to ${H:.0f}B in {rep}" if rep else "not repaired",
          f"and {('held there to 2060' if all((r['debt'] or 0) <= H + 1e-9 for r in C['boeing_fin'] if r['year'] >= (rep or 9999)) else 'not held')}; the stress case (free cash flow a third lower) peaks at ${max((r['debt_stress'] or 0) for r in C['boeing_fin'] if r['year'] >= 2030):.1f}B after 2030")]
    if EMB:
        t.append(("Embraer's new narrowbody", "Never launched",
                  f"its best launch case was {b(best_emb)} ({best_emb_y}); its CFO's binding funding test failed in every round"))
    return '<div class="tiles">' + "".join(f'<div class="panel tile"><div class="k">{esc(k)}</div><div class="v">{esc(v)}</div><div class="d">{d}</div></div>' for k, v, d in t) + "</div>"


def politics_table():
    if not W:
        return ""
    po = W["politics"]
    rows = [["Governments carry part of the fps bill", f"{pc(POL.get('boeing_cofund', 0), 0)} of the bill (state siting packages, federal research money)",
             b(po["terms"]["government_cofunding"]) + " (no fps launched)", "on a 10-year fps launched in 2030 it was worth about $0.30B, plus $0.17B less debt penalty"],
            ["Political cost of leaving the narrowbody market", f"{pc(POL.get('exit_p', 0), 0)} chance × ${POL.get('exit_loss_b', 0):.2f}B a year of defence profit, 20 years from {POL.get('exit_from', 2045)}",
             b(po["terms"]["political_exit_cost"]), f"charged to every plan with no fps: {b(-po['exit_cost_2030'])} in the 2030 brief, {b(-po['exit_cost_2050'])} in 2050"],
            ["Boeing's ΔPV without the political terms", "—", b(po["boeing_without"]), f"with them: {b(po['boeing_with'])}"]]
    if EMB:
        rows.append(["US tariffs on Embraer's jets", f"{pc(EMB_OPT.get('us_tariff_share_cut', 0), 0)} fewer new customers for Embraer", "—",
                     f"a 2030 launch without it: {b(W['break_even']['no_tariff'])} against {b(W['break_even']['base'])}; Embraer's line is full anyway"])
        rows.append(["Korea, suppliers and Brazil carry part of Embraer's bill",
                     f"{pc(EMB_OPT['partner_share'], 0)} Korea, {pc(EMB_OPT['supplier_share'], 0)} suppliers, {pc(EMB_OPT['state_share'], 0)} Brazil's state", "—",
                     f"Embraer still carries {pc(W['break_even']['own_share'], 0)} (${EMB_OPT['bill_b'] * W['break_even']['own_share']:.1f}B)"])
    return K.table(["Political term", "As set in this game", "Effect on the final value", "Note"], rows, num_cols=(2,))


def compare_table():
    head = ["Round"] + [f"{NAME[s]}: this game / previous" for s in ("boeing", "airbus", "cfm", "pratt_whitney", "rolls_royce")]
    rows = []
    for rc, rp in zip(C["rounds"], P["rounds"]):
        cells = [str(rc["year"])]
        for s in ("boeing", "airbus", "cfm", "pratt_whitney", "rolls_royce"):
            a, p_ = move_txt(s, rc["orders"][s]), move_txt(s, rp["orders"][s])
            cells.append(esc(a) + ("" if a == p_ else f' <span class="muted">/ {esc(p_)}</span>'))
        rows.append(cells)
    return K.table(head, rows).replace("<table>", '<table class="cmp">', 1)


def section(title, inner, sid=None):
    return f'<section{f" id={sid}" if sid else ""}><h2>{esc(title)}</h2>{inner}</section>'


def panel(inner, title=None, cap=None):
    return ('<div class="panel">' + (f'<p class="ctitle">{title}</p>' if title else "") + inner +
            (f'<p class="cap">{cap}</p>' if cap else "") + "</div>")


def build(out_path, text):
    """text: the page's narrative strings (lede, captions), written in narrative() from the same data."""
    br = C["rounds"][-1]["bridge"]["boeing"]
    pbr = P["rounds"][-1]["bridge"]["boeing"]
    body = [
        f'<header class="top"><p class="eyebrow">Boeing Product Development · war game rerun · six players · BOEING PROPRIETARY</p>'
        f'<h1>{esc(text["h1"])}</h1><p class="lede">{text["lede"]}</p><p class="gloss">{text["gloss"]}</p></header>',
        f'<section style="margin-top:18px">{tiles()}</section>',
        section("What each company did", panel(moves_table(C), cap=text["moves_cap"])),
        section("Boeing's financials", '<div class="stack">' +
                panel(f'<div class="cw">{profit_chart()}</div>', text["profit_title"], text["profit_cap"]) +
                panel(f'<div class="cw">{debt_chart()}</div>', text["debt_title"], text["debt_cap"]) +
                panel(fin_table(), "Boeing by year: deliveries, P&amp;L and cash", text["fin_cap"]) +
                panel(bridge_table(br, pbr), "Boeing's value against the status quo, by component", text["bridge_cap"]) + "</div>"),
        section("Market shares", '<div class="stack">' +
                panel(f'<div class="cw only-wide">{deliveries_chart()}</div><div class="cw only-narrow">{deliveries_chart(True)}</div>'
                      '<div class="legend"><span><i class="sq" style="background:var(--s1)"></i>Boeing</span><span><i class="sq" style="background:var(--s2)"></i>Airbus</span>'
                      '<span><i class="sq" style="background:var(--comac)"></i>COMAC</span>' + ('<span><i class="sq" style="background:var(--s3)"></i>Embraer</span>' if EMB_DLV else "") +
                      '<span><i class="solid" style="border-top-color:var(--fg)"></i>Demand</span></div>', text["mkt_title"], text["mkt_cap"]) +
                panel(f'<div class="cw">{share_chart()}</div>', text["share_title"], text["share_cap"]) +
                panel(share_table(), "Deliveries and shares by year", text["share_tab_cap"]) + "</div>"),
        section("How Boeing decided, round by round", panel(boeing_summary_table(boeing_round_rows()), cap=text["boeing_dec_cap"]) + chains_section("boeing"), "boeing"),
        section("How Airbus decided, round by round", panel(airbus_summary_table(airbus_round_rows()), cap=text["airbus_dec_cap"]) + chains_section("airbus"), "airbus"),
    ]
    if EMB:
        body.append(section("Embraer, the third airframer", panel(embraer_summary_table(embraer_round_rows()), cap=text["emb_dec_cap"]) +
                            panel(break_even_table(), "What would make Embraer's 2030 launch pay", text["be_cap"]) +
                            panel(emb_flip_table(), "If Embraer had launched in 2030", text["flip_cap"]) +
                            panel(emb_flip_market(), "Boeing with and without Embraer's jet", text["flip_mkt_cap"]) +
                            chains_section("embraer"), "embraer"))
    body.append(section("Politics in the payoffs", panel(politics_table(), cap=text["pol_cap"])))
    body.append(section("Against the previous game", panel(compare_table(), cap=text["cmp_cap"]) + panel(value_table(), "Every company's value after each round", text["val_cap"])))
    body.append(section("How this game was run", panel(f'<ul class="cav">{text["method"]}</ul>')))
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Six-Player Rerun</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{K.CSS + CSS_EXTRA + moves_css()}</style></head><body><div class="wrap">
{"".join(body)}
<footer><p>BOEING PROPRIETARY. Run {esc(C["run"])} on the combined_dash.py board (v3), against {esc(P["run"])}. Values are $B, PV at 2026, against the status quo; Boeing's cash and net debt come from the game master's balance-sheet tracker in 2026 dollars.</p></footer>
</div><script>{K.JS}</script></body></html>'''
    open(out_path, "w").write(page)
    return page


# ─────────────────────────────── narrative (every number from the data; claims asserted) ───────────────────────────────
def narrative():
    R4 = C["rounds"][-1]
    V, PVv = R4["value"], P["rounds"][-1]["value"]
    br, pbr = R4["bridge"]["boeing"], P["rounds"][-1]["bridge"]["boeing"]
    BR, AR, ER = boeing_round_rows(), airbus_round_rows(), embraer_round_rows()
    all_hold = lambda s: all(move_txt(s, r["orders"][s]) in ("Do Nothing", "A320 Alt plan") for r in C["rounds"][1:])
    # claims the copy makes, checked against the record
    assert all(move_txt("boeing", r["orders"]["boeing"]) == "Do Nothing" for r in C["rounds"]), "Boeing did something"
    assert all(move_txt("embraer", r["orders"]["embraer"]) == "Do Nothing" for r in C["rounds"]), "Embraer launched"
    assert C["rounds"][0]["orders"]["airbus"]["ngsa"] == "launch" and all_hold("airbus")
    assert all(max(x["launch"]) < 0 for x in ER), "an Embraer launch was positive"
    assert all(x["best_fps"][1] < -1.0 for x in BR)
    assert all(any(s == "cfo" for s, _ in x["vetoes"]) for x in BR)
    e_by = {x["year"]: x["launch"][0] for x in ER}
    be = W["break_even"]
    fl, pl = W["flipped"]["value"], W["played"]["value"]
    cof = W["cofund"]
    cf = lambda y: cof[str(y)]["fps 10-yr at Renton"]
    H = C["debt_inputs"]["historical_level_b"]
    rep = first_year_at(C["boeing_fin"], "debt", H)
    srep = first_year_at(C["boeing_fin"], "debt_stress", H)
    own = sum(r["owners"] or 0 for r in C["boeing_fin"])
    sd_d = br["supply_demand"] - pbr["supply_demand"]
    a_sd = C["rounds"][-1]["bridge"]["airbus"]["supply_demand"] - P["rounds"][-1]["bridge"]["airbus"]["supply_demand"]
    peak_y = max(range(2026, 2061), key=lambda y: FIN[y]["profit"])
    T = {}
    T["h1"] = "With Embraer and politics in the game, nobody new launches a narrowbody after Airbus"
    T["lede"] = (
        f"The MAX phase-out game, replayed with <b>Embraer as a sixth player</b> and <b>political terms in the payoffs</b>. "
        f"Embraer can launch a new 150-180 seat narrowbody with Team Korea in any round. It enters service four years later "
        f"({EMB_OPT['dev_years'] + 2030} for a 2030 launch, before 2035 as you asked). It is slightly better for airlines than the 737 MAX and A320neo "
        f"and worse than a new-generation fps or NGSA, so it wins {pc(EMB_OPT['share_by_newgen'][0] * (1 - EMB_OPT['us_tariff_share_cut']), 1)} of new customers while "
        f"neither is in service, {pc(EMB_OPT['share_by_newgen'][1] * (1 - EMB_OPT['us_tariff_share_cut']), 1)} with one and {pc(EMB_OPT['share_by_newgen'][2] * (1 - EMB_OPT['us_tariff_share_cut']), 1)} with both, "
        f"after a cut for US tariffs, on a line rising to {EMB_OPT['peak_a_month']:.0f} a month. Its campaigns would cut single-aisle prices by "
        f"{pc(EMB_OPT['cut'], 0)}, or {pc(EMB_OPT['cut'] * EMB_OPT['cut_boeing_no_fps_mult'], 1)} on Boeing's MAX while Boeing has no fps. "
        f"Embraer's executives and Board were profiled from its own calls to May 2026 and played its seat like every other company. "
        f"<b>What happened:</b> Airbus launched NGSA in 2030 (in service 2037), as in the previous game. Boeing did nothing in all four rounds. "
        f"Embraer held in all four: its launch was below zero in every column of every brief ({b(e_by[2030])} in 2030, {b(e_by[2050])} in 2050), "
        f"so its CFO's funding test failed each time. The engine makers moved less than before. Boeing ends at {b(V['boeing'])} against the status quo "
        f"({b(PVv['boeing'])} in the previous game), and its share of single-aisle deliveries falls from {pc(MK[2030]['sh_boeing'], 0)} in 2030 to "
        f"{pc(MK[2050]['sh_boeing'], 0)} in 2050 and none in 2060, when the last MAX is built.")
    T["gloss"] = ("<b>How to read the figures.</b> Values are $B, present value at 2026, against the <b>status quo</b>, in which nobody launches "
                  "anything (and Embraer builds no airliner). <b>Do Nothing</b> is Boeing launching nothing while the others move. Each round every "
                  "company's ExCo gets a brief: a grid that values each of its plans against the moves its rivals could make that round, one "
                  "<b>column</b> per move. The CEO names the column it expects. Boeing's Board approves a launch only if it adds more than +$1B in the "
                  "expected column and loses no more than $1B in any column it finds plausible, and its CFO vetoes any plan more than $2B below "
                  "Do Nothing in the risk case. P&amp;L figures are the game's commercial-airplane model at 2026 prices; cash and net debt come "
                  "from the game master's balance-sheet tracker in 2026 dollars.")
    diffs = []
    for s, txt in (("rolls_royce", "Rolls-Royce held its UltraFan NB in 2030 (in the previous game it launched it on NGSA's selection) and committed to the Joint Venture in 2035"),
                   ("pratt_whitney", "Pratt &amp; Whitney never matched that commitment, so no Joint Venture formed and GTF2 stayed its own engine on NGSA"),
                   ("cfm", "CFM/GE launched no ducted engine and no Embraer partnership in 2035, as it did before")):
        diffs.append(txt)
    T["moves_cap"] = ("Boeing and Embraer held in every round, and Airbus made its one launch in 2030 (NGSA, on the A320 Alt plan, naming all three "
                      "engine makers). NGSA's selection set off P&amp;W's GTF2, and CFM/GE upgraded the GEnx. Against the previous game: "
                      + "; ".join(diffs) + ".")
    T["profit_title"] = (f"Boeing's commercial profit peaks at {b(FIN[peak_y]['profit'], 1, False)} a year ({peak_y}) and falls to "
                         f"{b(FIN[2060]['profit'], 1, False)} in 2060, when only the 787 is left")
    T["profit_cap"] = (f"Operating profit on narrowbodies and widebodies, $B a year at 2026 prices. Revenue goes from {b(FIN[2030]['revenue'], 1, False)} (2030) "
                       f"to {b(FIN[2040]['revenue'], 1, False)} (2040), {b(FIN[2050]['revenue'], 1, False)} (2050) and {b(FIN[2060]['revenue'], 1, False)} (2060). "
                       "The MAX is phased out from 2045 and none is built from 2060, in every plan and in the status quo, so Do Nothing "
                       "tracks the status quo closely: Boeing loses only some customers to NGSA in 2045-46. The previous game is the same "
                       "path, except in 2043-46, when its overflow entrant took customers who were waiting for a Boeing slot.")
    T["debt_title"] = (f"Net debt is back at the historical level (${H:.0f}B) in {rep} and stays there; the stress case gets there in {srep}")
    T["debt_cap"] = ("The game master's tracker: net debt starts at the consensus end-2026 $22.5B and falls by free cash flow (the analysts' "
                     "consensus to 2030, then held flat, moved only by the profit the game adds or takes away against the status quo, after tax, "
                     "less programme cash). Once net debt is at the historical level, surplus cash goes to the owners: "
                     f"{b(own, 0, False)} in 2029-2060 on this path. Boeing launched nothing, so no programme cash was spent. "
                     "<b>A limit to read with it:</b> because the MAX phase-out is in the status quo too, the tracker's free cash flow does not "
                     "fall with the P&amp;L after 2045; the profit chart above shows that decline.")
    T["fin_cap"] = ("NB and WB deliveries are aircraft a year; revenue and operating profit $B at 2026 prices; free cash flow, net debt and cash "
                    "for owners $B in 2026 dollars (the tracker). The stress case runs the same path with base free cash flow a third lower.")
    T["bridge_cap"] = (f"The board's market (2,000 narrowbodies a year at fixed shares) gives {b(br['nb_profit_vs_sq'])}; supply and demand corrects it to "
                       f"what the factories actually deliver ({b(br['supply_demand'])}), and the political cost of leaving the narrowbody market takes "
                       f"{b(br['political_exit_cost'])}. The supply-and-demand line is {b(sd_d)} better than in the previous game because its overflow entrant "
                       "is gone (Embraer replaced it and never launched), so Boeing keeps some waiting customers that entrant took.")
    T["mkt_title"] = (f"Airbus's NGSA and COMAC take the single-aisle market as the MAX runs down: in 2050 Boeing delivers {n0(MK[2050]['max'])}, "
                      f"Airbus {n0(MK[2050]['ngsa'])} and COMAC {n0(MK[2050]['comac'])}")
    T["mkt_cap"] = ("737/A320-class aircraft delivered each year in the final state, with demand (the line). COMAC sells its capacity first to its own "
                    "customers (150 a year in 2035, 250 from 2050). Embraer built nothing, so there is no Embraer bar.")
    T["share_title"] = (f"Boeing's share of deliveries: {pc(MK[2030]['sh_boeing'], 0)} in 2030, {pc(MK[2040]['sh_boeing'], 0)} in 2040, "
                        f"{pc(MK[2050]['sh_boeing'], 0)} in 2050, none in 2060")
    T["share_cap"] = (f"Shares of the market's deliveries. Airbus reaches {pc(MK[2060]['sh_airbus'], 0)} and COMAC {pc(MK[2060]['sh_comac'], 0)} in 2060. "
                      "Boeing's line in the previous game (dashed) is almost the same. Boeing's widebody share stays at "
                      f"{pc(MK[2050]['wb_boeing'], 0)}: nobody re-engined a widebody.")
    T["share_tab_cap"] = "Aircraft a year and shares of deliveries, final state."
    T["boeing_dec_cap"] = (
        "Each round Boeing's chain ran: Board guidance (priorities, risk appetite, what it would approve or veto), the CEO's framing, the CFO's "
        "and the head of Commercial Airplanes' tests, the CEO's decision, their veto checks, and the Board's review of any order that differed "
        "from Do Nothing. Every round the CFO's binding buffer test struck the fps on every schedule, and the best fps in the CEO's expected "
        f"column ran from {b(BR[0]['best_fps'][1])} (2030) to {b(BR[-1]['best_fps'][1])} (2050) against Do Nothing, far from the Board's +$1B. "
        f"The 787 Re-engine led Do Nothing by {b(BR[0]['re787'])} in 2030 and {b(BR[1]['re787'])} in 2035 but lost {b(-BR[0]['re787_worst'], 2, False)} "
        f"and {b(-BR[1]['re787_worst'], 2, False)} if Airbus re-engined the A350 in the same round, outside the Board's $1B downside limit, so the "
        f"CEO held it; in 2045 and 2050 its lead ({b(BR[2]['re787'])}, {b(BR[3]['re787'])}) fell short of the +$1B business case. "
        "Embraer's launch column shows what Embraer would have cost Boeing: "
        f"{b(BR[0]['emb_hit'])} in 2030, falling to {b(BR[-1]['emb_hit'])} by 2050. No Boeing order reached the Board.")
    T["airbus_dec_cap"] = (
        "Airbus's chain is the same; its CFO and head of Commercial Aircraft hold soft vetoes the CEO can override only for a plan $1B better, "
        "and five pillars (safety, quality, integrity, compliance, security) no one overrides. In 2030 it launched NGSA on its own clock "
        "(the last year of its window), with all three engine makers named, and deleted every row with the A350 Re-engine on its one-launch "
        "rule and its CFO's $5.2B peak-cash line, and every Delay Tactics row on the pillars. In 2035 it held the Re-engine for the cash line "
        "again. In 2045 and 2050 the Re-engine passed on cash, but its lead "
        f"({b(AR[2]['best'][1] - row(3, 'airbus', 'NGSA: hold (A320 Alt plan) + A350: hold')[col_index(REC(3)['airbus']['decision']['expected_scenario'], 3)])}, then "
        f"{b(AR[3]['best'][1] - row(4, 'airbus', 'NGSA: hold (A320 Alt plan) + A350: hold')[col_index(REC(4)['airbus']['decision']['expected_scenario'], 4)])}) "
        "sat inside the CEO's $1B band and the CEO held, logging the value given up as a premium.")
    T["emb_dec_cap"] = (
        "Embraer's chain: its Board (the Brazilian state holds a golden share), CEO Francisco Gomes Neto, CFO Felipe Santana (in post since May 2026, "
        "running the funding test inherited from Antonio Carlos Garcia) and Arjan Meijer, head of Commercial Aviation. The CFO's funding test is "
        "binding: Team Korea's share in the brief, ΔPV with the debt penalty at or above zero in the expected column, and no more than 5 yield points "
        "lost in the risk column. Leg 2 failed in every round. The market-window test (a soft veto) passed in 2030 and failed from 2035, once NGSA "
        "was due in service before Embraer's jet could be. The launch row improves from round to round only because its bill is booked later.")
    T["be_cap"] = (
        f"At the 2030 decision, with the rivals' actual orders and nobody moving after: a launch is worth {b(be['base'])} to Embraer. One lever at a "
        f"time, it breaks even if Korea carries {pc(be['partner_share'], 0)} of the bill instead of {pc(EMB_OPT['partner_share'], 0)} (Embraer's own share falling "
        f"to about {pc(1 - be['partner_share'] - EMB_OPT['supplier_share'] - EMB_OPT['state_share'], 0)}), if its margin is {pc(be['margin'], 0)} instead of "
        f"{pc(EMB_OPT['margin'], 0)}, if its line reaches {be['peak_a_month']:.0f} a month instead of {EMB_OPT['peak_a_month']:.0f}, or if the bill is "
        f"${be['bill_b']:.1f}B instead of ${EMB_OPT['bill_b']:.0f}B. Removing the US tariff cut barely helps: the line, not demand, sets its deliveries.")
    T["flip_cap"] = (
        f"The whole game replayed with every company's recorded orders, but Embraer launching in 2030 (in service 2034). Embraer loses "
        f"{b(-fl['embraer'], 2, False)}. Boeing loses {b(pl['boeing'] - fl['boeing'], 2, False)} and Airbus {b(pl['airbus'] - fl['airbus'], 2, False)}, mostly through "
        "the price cut; P&amp;W gains because Embraer's jet flies its engines. The others did not get to respond, so this is a bound on the threat, "
        "not a forecast.")
    T["flip_mkt_cap"] = ("Boeing's deliveries, the price cut on its aircraft and its profit with Embraer's jet in the market, against the game as played. "
                         "Net debt is the tracker's, as above.")
    T["pol_cap"] = (
        "Boeing's terms come from the earlier politics study: US governments carry a share of an fps bill (state siting packages and federal "
        "research money, as in the past; no federal launch funding), and leaving the narrowbody market has a political cost (defence, export "
        "finance, the FAA). Both are small against the fps gap. With the rivals' actual orders, governments would have to carry "
        f"{pc(cf(2030)['needed'], 0)} of the bill for a 10-year fps at Renton to clear the Board's +$1B in 2030, {pc(cf(2035)['needed'], 0)} in 2035 and "
        f"{pc(cf(2045)['needed'], 0)} in 2045, and no share is enough in 2050 (the game's 2% is worth {b(cf(2030)['as_played'] - cf(2030)['none'])} in 2030). "
        "Airbus has no cash term: its launch aid is on market terms. Embraer's partners and the US tariff are in its economics.")
    T["cmp_cap"] = "Orders that differ from the previous game are shown with the previous game's order after the slash."
    T["val_cap"] = (f"Each company's ΔPV with nobody moving after that round. Airbus is {b(V['airbus'] - PVv['airbus'])} against the previous game, "
                    f"{b(a_sd)} of it in supply and demand, because the overflow entrant is gone from the market and its status quo. "
                    "The engine makers differ because they moved differently.")
    T["method"] = "".join(f"<li>{x}</li>" for x in [
        "Six companies played four rounds (2030, 2035, 2045, 2050) on the combined_dash.py board in the MAX phase-out world, each through its own "
        "Board and ExCo agents, with sealed orders and the public bulletin as the only view of rivals. Run dash-2050-emb; the previous game is "
        "dash-2050-phaseout.",
        "Embraer's executives and Board were built from the repo's Embraer call transcripts (2011 to May 2026) and S&amp;P workbooks, each file "
        "checked quote by quote by an adversarial verifier (881 evidence items). Felipe Santana holds the CFO seat; Antonio Carlos Garcia's six "
        "years as CFO are the doctrine the seat inherits. Embraer's decision rule and vetoes are inferences from calls.",
        "In round 1 Embraer's seats ran as general-purpose agents given their files (the session could not yet load them as agent types); an audit "
        "replayed all 62 of their tool calls through the isolation hook and none would have been denied. From round 2 they ran as their own agent "
        "types under the hook.",
        f"Embraer's economics are this game's assumptions: a ${EMB_OPT['bill_b']:.0f}B bill (industry estimates of $10-11B), Korea "
        f"{pc(EMB_OPT['partner_share'], 0)}, risk-sharing suppliers {pc(EMB_OPT['supplier_share'], 0)}, Brazilian state research money {pc(EMB_OPT['state_share'], 0)}, "
        f"${EMB_OPT['price_m']:.0f}M a jet at a {pc(EMB_OPT['margin'], 0)} margin, a {pc(EMB_OPT['wacc'], 0)} cost of capital, net debt ${EMB_OPT['debt_b']:.1f}B and "
        f"enterprise value ${EMB_OPT['ev_b']:.0f}B (the S&amp;P workbooks, converted), and the debt penalty the airframers pay. The four-year development "
        "is your premise; the earlier research put a credible entry into service no earlier than 2037.",
        "Embraer replaces the previous game's generic overflow entrant. Its first-year deliveries are lost to the firm-order backlog (all 2034 demand "
        "is served from Boeing's and Airbus's firm orders), a small understatement. It does not cannibalise the E195-E2.",
        "Engine makers count Embraer's engines (P&amp;W, or CFM with CFM's Embraer partnership). The political exit cost starts at the later of 2045 "
        "and the decision year, so Boeing's value moves by a few cents between rounds with no move.",
        "Runs without the Embraer and politics options are unchanged: every earlier game replays exactly and the board's cells reproduce."])
    return T


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "dash_2050_emb.html")
    page = build(out, narrative())
    print("wrote", out, len(page))
