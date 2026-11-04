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


def spread(vals, gap=22, span=(0, 280)):
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
              refs=[(C["debt_inputs"]["historical_level_b"], "Historical level", "above")])


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
.scroll { background:
    linear-gradient(to right, var(--surface) 40%, transparent) left / 32px 100% no-repeat local,
    linear-gradient(to left, var(--surface) 40%, transparent) right / 32px 100% no-repeat local,
    linear-gradient(to right, color-mix(in srgb, var(--fg) 22%, transparent), transparent) left / 14px 100% no-repeat scroll,
    linear-gradient(to left, color-mix(in srgb, var(--fg) 22%, transparent), transparent) right / 14px 100% no-repeat scroll; }
.scroll > table { background: transparent; }
ul.cav li, footer { overflow-wrap: anywhere; }
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
        vet = [s for s in ("cfo", "ops") if any(v.get("binding") for v in ((x.get(s) or {}).get("vetoes") or []))]
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


def boeing_summary_table(rows):
    head = ["Round", "CEO's expected column", "Best fps against Do Nothing there", "787 Re-engine against Do Nothing (worst column)",
            "Embraer's launch would cost Boeing", "Binding vetoes in the ExCo", "Board", "Orders"]
    body = []
    for x in rows:
        body.append([str(x["year"]), esc(x["expected"]), f'{esc(x["best_fps"][0])}: {b(x["best_fps"][1])}',
                     (f'{b(x["re787"])} ({b(x["re787_worst"])})' if x["re787"] is not None else "—"),
                     (b(x["emb_hit"]) if x["emb_hit"] is not None else "—"),
                     esc(", ".join({"cfo": "CFO's buffer test", "ops": "operating head's KPI test"}[v] for v in x["vetoes"]) or "none"),
                     esc(("vetoed " + ", ".join(x["board_vetoed"])) if x["board_vetoed"] else ("approved " + ", ".join(x["board_items"])) if x["board_items"] else "no Board item"),
                     esc(move_txt("boeing", x["orders"]))])
    return K.table(head, body, num_cols=(2, 3, 4))


def airbus_summary_table(rows):
    head = ["Round", "CEO's expected column", "Best grid plan there", "Orders", "Board"]
    body = [[str(x["year"]), esc(x["expected"]), f'{esc(x["best"][0])}: {b(x["best"][1])}', esc(x["chosen"]),
             esc(("vetoed " + ", ".join(x["board_vetoed"])) if x["board_vetoed"] else ("approved " + ", ".join(x["board_items"])) if x["board_items"] else "no Board item")] for x in rows]
    return K.table(head, body, num_cols=(2,))


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
