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


def b(v, dp=2, sign=True):
    return K.usd(v, dp, sign and K.rnd(v, dp) != 0)


def bp(v, dp=2, sign=True):
    return re.sub(r"<[^>]+>", "", b(v, dp, sign))


def n0(v):
    return f"{K.rnd(v or 0.0, 0):,.0f}"


def pc(v, dp=1):
    return f"{K.rnd(100 * (v or 0.0), dp):.{dp}f}%"


def short(t, n=320):
    t = re.sub(r"\s+", " ", str(t or "")).strip()
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


def spread(vals, gap=16, span=(0, 280)):
    """End-label offsets so labels at the right edge do not collide: vals are pixel y positions."""
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    pos = [vals[i] for i in order]
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
    return lc([("This game", "s1", s_c), ("Previous game", "muted", s_p), ("Status quo", "s2", s_q)], 0, hi, 2, "int",
              "Boeing commercial operating profit, $B a year (2026 prices)", "Boeing's operating profit by year, this game, the previous game and the status quo",
              [(offs[0], "This game"), (offs[1], "Previous game"), (offs[2], "Status quo")])


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
              refs=[(C["debt_inputs"]["historical_level_b"], "Historical level", "below")])


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
    if EMB:
        ser.append(("Embraer", "s3", [(y, MK[y]["sh_embraer"]) for y in ys]))
    ser.append(("Boeing, previous game", "muted", [(y, PMK[y]["sh_boeing"]) for y in ys]))
    yfun = lambda v: 26 + (0.8 - v) / 0.8 * (346 - 26 - 46)
    offs = spread([yfun(s[2][-1][1]) for s in ser])
    return lc(ser, 0, 0.8, 0.2, "pct", "Share of single-aisle deliveries", "Single-aisle delivery shares by maker, final state",
              [(o, s[0]) for o, s in zip(offs, ser)])


# ─────────────────────────────── tables ───────────────────────────────
def fin_table():
    head = ["Year", "NB deliveries", "WB deliveries", "Revenue $B", "Operating profit $B", "Status-quo profit $B",
            "Programme cash $B", "Free cash flow $B", "Net debt $B", "Net debt, stress $B", "Net debt, previous game $B"]
    rows = []
    for y in KEY:
        f, p_ = FIN[y], PFIN[y]
        rows.append([str(y), n0(f["nb_units"]), n0(f["wb_units"]), f"{f['revenue']:.1f}", f"{f['profit']:.1f}", f"{f['sq_profit']:.1f}",
                     f"{f['spend']:.1f}" if f["spend"] else "—", K.num(f["fcf"], "+.1f") if f["fcf"] is not None else "—",
                     f"{f['debt']:.1f}" if f["debt"] is not None else "—", f"{f['debt_stress']:.1f}" if f["debt_stress"] is not None else "—",
                     f"{p_['debt']:.1f}" if p_["debt"] is not None else "—"])
    return K.table(head, rows, num_cols=tuple(range(1, len(head))))


def share_table():
    head = ["Year", "Demand", "Boeing", "of which fps", "Airbus", "of which NGSA", "COMAC"] + (["Embraer"] if EMB else []) + \
           ["Boeing share", "Airbus share", "COMAC share"] + (["Embraer share"] if EMB else []) + ["Boeing share, previous game", "Boeing widebody share"]
    rows = []
    for y in KEY:
        m, q = MK[y], PMK[y]
        r = [str(y), n0(m["demand"]), n0(m["max"] + m["fps"]), n0(m["fps"]), n0(m["a320"] + m["ngsa"]), n0(m["ngsa"]), n0(m["comac"])]
        r += [n0(m["embraer"])] if EMB else []
        r += [pc(m["sh_boeing"]), pc(m["sh_airbus"]), pc(m["sh_comac"])] + ([pc(m["sh_embraer"])] if EMB else []) + [pc(q["sh_boeing"]), pc(m["wb_boeing"])]
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
                     f'<b>{esc(i.get("order_field", ""))} = {esc(str(i.get("value", "")))}</b>: {esc(short(i.get("ground", ""), 260))}</li>' for i in items)
    else:
        it = f'<li>{esc(rv.get("note", "No Board items: every order is the default."))}</li>'
    if x.get("board_revision"):
        it += f"<li><b>CEO revises within the veto:</b> {esc(move_txt(side, x['board_revision'].get('orders', {})))}</li>"
    if x.get("board_reverted"):
        it += f"<li><b>Reverted to the default:</b> {esc(', '.join(x['board_reverted']))}</li>"
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
