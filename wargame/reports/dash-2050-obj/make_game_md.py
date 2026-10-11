"""Write dash_2050_exco_report.md: the full written report of the dash-2050-exco war game (ExCo and Board agents on the
combined_dash.py board), round by round, from data/report_data.json (the same numbers as the HTML page) and the
narrative in narrative.py.

Usage: python3 make_game_md.py [out.md]"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import narrative as NAR  # noqa: E402
import page_kit as K  # noqa: E402
from make_game_html import (AF, EN, NAME, ROUNDS, FINAL, SIDES, YEARS, RYEARS, D, order_text, BRIDGE_LABEL, PEOPLE,  # noqa: E402
                             chain_summary, SEAT, OLD, XV, lab_af, plain, PLAIN_FIELD, prev_codes,
                             unchanged_since, memo_binding_count)  # noqa: E402

M = K.MINUS


def n2(v):
    return K.num(v)


def pct(v):
    return f"{K.rnd(v * 100, 1):.1f}%"


def strip(html_txt):
    import re
    t = re.sub(r"\s*<li>\s*", "\n- ", html_txt)
    t = re.sub(r"</?(ul|li|p|h3)[^>]*>", "\n", t)
    t = re.sub(r"<[^>]+>", "", t).replace("&amp;", "&")
    return re.sub(r"\n\s*\n+", "\n", t).strip()


def _numeric(c):
    import re
    c = str(c).replace("*", "").strip()
    return c in ("—", "") or bool(re.fullmatch(r"[+\-\u2212]?\$?[\d,]*\.?\d+[%B]?", c))


def tbl(head, rows):
    """Markdown table: a column is right-aligned only if every cell in it is a number."""
    right = [i > 0 and rows and all(_numeric(r[i]) for r in rows) for i in range(len(head))]
    cell = lambda c: " ".join(str(c).split()).replace("|", "/")
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---:" if right[i] else "---" for i in range(len(head))) + "|"]
    out += ["| " + " | ".join(cell(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def round_md(r):
    n = r["round"]
    nar = NAR.ROUNDS.get(n, {})
    L = [f"## Round {n}: decision year {r['year']}", ""]
    if nar.get("title"):
        L += [f"**{nar['title']}**", ""]
    if nar.get("lede"):
        L += [strip(nar["lede"]), ""]
    L += ["### Orders (as adjudicated)", ""]
    rows = []
    for s in SIDES:
        rows.append([NAME[s], "; ".join(order_text(s, r["orders"][s], prev_codes(ROUNDS, r))), (r["public_statements"].get(s) or "").replace("|", "/")])
    L += [tbl(["Player", "Orders", "Public statement"], rows), ""]
    cov = [f"{k} ordered {y}" for k, y in r["timeline"]["delay_tactics"].items() if y]
    if cov:
        L += [f"Covert (revealed after the game): Airbus Delay Tactics, {', '.join(cov)}.", ""]
    L += ["### Programme dates after the round", ""]
    L += [tbl(["Programme", "Launched", "Due", "Status"],
              [[p["name"], p["launch"], f"{p['due_kind']} {p['due']}", p["status"]] for p in r["timeline"]["programmes"]]), ""]
    fit = r["timeline"]["engine_fit"]
    if fit:
        L += [tbl(["Airframe", "Engines requested", "Engines fitted", "Note"],
                  [["fps" if k == "fps" else "NGSA", f["requested"], f["fitted_if_no_change"], f["note"] or "—"] for k, f in fit.items()]), ""]
    L += ["### Value after the round (GM valuation; nobody moves afterwards)", ""]
    keys = []
    for s in SIDES:
        for k in r["value"][s]["bridge"]:
            if k not in keys:
                keys.append(k)
    rows = []
    for k in keys:
        cells = [n2(r["value"][s]["bridge"][k]) if abs(r["value"][s]["bridge"].get(k, 0) or 0) > 1e-9 else "—" for s in SIDES]
        if any(c != "—" for c in cells):
            rows.append([BRIDGE_LABEL.get(k, k)] + cells)
    rows.append(["**ΔPV, $B at 2026**"] + [f"**{n2(r['value'][s]['pv_delta'])}**" for s in SIDES])
    rows.append(["Yield"] + [f"{K.rnd(r['value'][s]['yield'], 2):.2f}%" for s in SIDES])
    L += [tbl(["Component"] + [NAME[s] for s in SIDES], rows), ""]
    same = unchanged_since(r)
    if same:
        L += [f"Market shares, financials and the year-by-year tables are unchanged since round {same['round']} ({same['year']}).", ""]
    L += [] if same else ["### Market shares projected after the round", ""]
    yrs = ["2030", "2035", "2040", "2045", "2050", "2055", "2060"]
    sn = r["snapshots"]
    rows = []
    for label, s, k in [("Boeing NB", "boeing", "nb_share"), ("Airbus NB", "airbus", "nb_share"), ("Boeing WB", "boeing", "wb_share"),
                        ("Airbus WB", "airbus", "wb_share"), ("CFM NB engines", "cfm", "nb_share"), ("P&W NB engines", "pratt_whitney", "nb_share"),
                        ("RR NB engines", "rolls_royce", "nb_share"), ("CFM/GE WB engines", "cfm", "wb_share"), ("RR WB engines", "rolls_royce", "wb_share")]:
        rows.append([label] + [pct(sn[y][s][k]) for y in yrs])
    if not same:
        L += [tbl(["Share"] + yrs, rows), ""]
        L += ["### Financials by period (nominal $B)", ""]
    rows = []
    for s in AF:
        for p in r["periods"][s]:
            rows.append([f"{NAME[s]} {p['period']}", f"{p['nb_units']:,.0f}", f"{p['wb_units']:,.0f}", f"{p['revenue']:,.1f}", f"{p['profit']:,.1f}",
                         f"{p['sq_profit']:,.1f}", f"{p['nonrecurring']:,.1f}"])
    if not same:
        L += [tbl(["Airframer", "NB deliveries", "WB deliveries", "Revenue", "Operating profit", "Status-quo profit", "Non-recurring"], rows), ""]
    rows = []
    for s in EN:
        for p in r["periods"][s]:
            rows.append([f"{NAME[s]} {p['period']}", f"{p['nb_units']:,.0f}", f"{p['wb_units']:,.0f}", f"{p['value']:,.1f}", f"{p['sq_value']:,.1f}",
                         f"{p['nonrecurring']:,.1f}"])
    if not same:
        L += [tbl(["Engine maker", "NB engines", "WB engines", "Engine lifecycle value", "Status-quo value", "R&D and write-offs"], rows), ""]
        L += ["### Year by year", ""]
    for s in ([] if same else SIDES):
        y = r["years"][s]
        L += [f"**{NAME[s]}**", ""]
        if s in AF:
            L += [tbl(["Year", "NB share", "WB share", "NB deliveries", "WB deliveries", "Revenue $B", "Operating profit $B", "Status-quo $B", "Non-recurring $B"],
                      [[yr, pct(y["nb_share"][i]), pct(y["wb_share"][i]), f"{y['nb_units'][i]:,.0f}", f"{y['wb_units'][i]:,.0f}", f"{y['revenue'][i]:,.1f}",
                        f"{y['profit'][i]:,.2f}", f"{y['sq_profit'][i]:,.2f}", f"{y['nonrecurring'][i]:,.2f}" if y["nonrecurring"][i] else "—"]
                       for i, yr in enumerate(YEARS)]), ""]
        else:
            L += [tbl(["Year", "NB engine share", "WB engine share", "NB engines", "WB engines", "Engine value $B", "Status-quo $B", "R&D, write-offs $B"],
                      [[yr, pct(y["nb_share"][i]), pct(y["wb_share"][i]), f"{y['nb_units'][i]:,.0f}", f"{y['wb_units'][i]:,.0f}", f"{y['value'][i]:,.2f}",
                        f"{y['sq_value'][i]:,.2f}", f"{y['nonrecurring'][i]:,.2f}" if y["nonrecurring"][i] else "—"]
                       for i, yr in enumerate(YEARS)]), ""]
    L += ["### How each company decided (private during the game)", ""]
    for s in SIDES:
        x = r["returned"].get(s) or {}
        ex = x.get("exco") or {}
        dec = ex.get("decision") or {}
        L += [f"**{NAME[s]}** ({', '.join(PEOPLE[s][:3])}; {PEOPLE[s][3]})", ""]
        L += [tbl(["Step", "What happened"], [[a, plain(b_)] for a, b_ in chain_summary(s, x, prev_codes(ROUNDS, r))]), ""]
        for seat in ("cfo", "ops"):
            m = ex.get(seat) or {}
            tests = m.get("tests") or []
            if tests:
                L += [{"cfo": "CFO tests:", "ops": "Operating head tests:"}[seat], "",
                      tbl(["Test", "Threshold", "Result", "Numbers"],
                          [[plain(t.get("name", "")), plain(t.get("threshold", "")), t.get("result", ""), plain(t.get("numbers", ""))]
                           for t in tests]), ""]
        rv = ex.get("board_review") or {}
        if rv.get("items"):
            L += ["Board review:", "", tbl(["Board item", "Value", "Decision", "Ground", "Alternatives"],
                  [[PLAIN_FIELD.get(i.get("order_field", ""), i.get("order_field", "")), plain(i.get("value", "")), i.get("decision", ""), plain(i.get("ground", "")),
                    plain("; ".join(i.get("acceptable_alternatives") or [])) or "—"] for i in rv["items"]]), ""]
        L += [f"- Decision rationale: {plain(dec.get('rationale', ''))}",
              f"- Expected scenario: {plain(x.get('expected_scenario', ''))}. Best grid plan there: {plain(x.get('best_grid_plan_in_expected_scenario', ''))}. "
              f"Premium {n2(x.get('premium_b', 0) or 0)} $B: {plain(x.get('premium_reason', ''))}",
              f"- Predictions: {plain(x.get('predictions', ''))}",
              f"- Expected ΔPV {n2(x.get('expected_pv_b', 0) or 0)} $B; GM valuation after the round {n2(r['value'][s]['pv_delta'])} $B", ""]
        om = x.get("other_moves") or []
        if om:
            L += ["- Other moves: " + "; ".join(f"{m.get('move', '')} ({'public' if m.get('public') else 'private'})" for m in om), ""]
    return "\n".join(L)


def build(out):
    L = [f"# {NAR.TITLE}", "", "BOEING PROPRIETARY. Boeing Product Development war game on the narrowbody/widebody game-theory dashboard, "
         "played by ExCo and Board agents.", "",
         strip(NAR.LEDE), "", "## Summary", ""]
    rows = []
    for s in SIDES:
        v = FINAL["value"][s]
        obj = FINAL["objectives"][s]
        rows.append([NAME[s], n2(v["pv_delta"]), f"{K.rnd(v['yield'], 2):.2f}%", f"{sum(o['met'] for o in obj)} of {len(obj)}"])
    L += [tbl(["Player", "Final ΔPV $B", "Yield", "Objectives met"], rows), ""]
    for t, x in NAR.FINDINGS:
        L += [f"**{t}**", strip(x), ""]
    L += ["", "### ΔPV after each round ($B at 2026)", "",
          tbl(["Player"] + [f"After {y}" for y in RYEARS], [[NAME[s]] + [n2(r["value"][s]["pv_delta"]) for r in ROUNDS] for s in SIDES]), "",
          "### Objectives at the end", "",
          tbl(["Player", "Metric", "Status", "Detail"], [[NAME[s], o["label"], "met" if o["met"] else "not met", o["detail"]]
                                                        for s in SIDES for o in FINAL["objectives"][s]]), ""]
    L += ["### Regret (final ΔPV of the best alternative minus actual, everyone else's actual orders held)", "",
          tbl(["Player"] + [f"Round {n}" for n in range(1, len(ROUNDS) + 1)],
              [[NAME[s]] + [n2(D["regret"][str(n)][s]["regret_ex_post"]) for n in range(1, len(ROUNDS) + 1)] for s in SIDES]), ""]
    # how the companies decided
    L += ["## How the companies decided", "", strip(NAR.GOV_LEDE), ""]
    rows = []
    for r in ROUNDS:
        for s in SIDES:
            ex = ((r["returned"].get(s) or {}).get("exco")) or {}
            rows.append([f"R{r['round']} {NAME[s]}", ", ".join(SEAT.get(v, v) for v in ex.get("binding_vetoes") or []) or "—",
                         ", ".join(SEAT.get(v, v) for v in ex.get("red_line_flags") or []) or "—", "yes" if ex.get("revision") else "—",
                         ", ".join(PLAIN_FIELD.get(f, f) for f in ex.get("board_items") or []) or "—",
                         ", ".join(PLAIN_FIELD.get(f, f) for f in ex.get("board_vetoed") or []) or "—",
                         ", ".join(PLAIN_FIELD.get(f, f) for f in ex.get("board_reverted") or []) or "—"])
    L += [tbl(["Round, company", "Binding vetoes at the veto check", "Red-line flags", "ExCo revised", "Board items", "Board vetoed", "Reverted"], rows), "",
          f"The binding vetoes in the CFOs' and operating heads' test memos ({memo_binding_count()} in all) fell on options the CEO did not choose.", ""]
    for t, x in NAR.GOV_POINTS:
        L += [f"**{t}**", strip(x), ""]
    # equilibria and the stage game
    bd = D.get("board") or {}
    if bd:
        L += ["### Your snapshot's equilibria (default dates: fps 2041, NGSA 2037, Re-engines 2042)", "",
              tbl(["Pure Nash", "Airbus", "Boeing", "Yield Airbus / Boeing"],
                  [[i + 1, e["airbus"], e["boeing"], f'{K.rnd(e["yield_airbus"], 1):.1f}% / {K.rnd(e["yield_boeing"], 1):.1f}%']
                   for i, e in enumerate(bd.get("airframer_pure") or [])]), "",
              f"{bd.get('airframer_near_count', 0)} Near-Nash besides. Engine game: {len(bd.get('engine_pure') or [])} Pure Nash, "
              f"{bd.get('engine_near_count', 0)} Near-Nash.", "",
              f"Where the game ended, as a board cell: Airbus {lab_af(FINAL['board_inputs']['a'])}; Boeing {lab_af(FINAL['board_inputs']['b'])}; "
              f"at fps {FINAL['board_inputs']['eis'][0]}, NGSA {FINAL['board_inputs']['eis'][1]}.", ""]
    S = D.get("stage") or {}
    if S:
        rows = []
        for n in range(1, len(ROUNDS) + 1):
            x = S.get(str(n))
            if x:
                rows.append([f"Round {n} ({x['year']})", "; ".join(f"Boeing {p[0]} / Airbus {p[1]} ({n2(p[2])} / {n2(p[3])})" for p in x["pure"]) or "none",
                             f"Boeing {x['played'][0]} / Airbus {x['played'][1]} ({n2(x['played_value'][0])} / {n2(x['played_value'][1])})"])
        L += ["### The airframer stage game each round (engine makers as played; nobody moves later)", "",
              tbl(["Round", "Pure equilibria (ΔPV Boeing / Airbus)", "What was played"], rows), ""]
    for t, x in NAR.PLAY_POINTS:
        L += [f"**{t}**", strip(x), ""]
    for r in ROUNDS:
        L += [round_md(r), ""]
    # the earlier game
    L += ["## Against the earlier game", "", strip(NAR.COMPARE_LEDE), ""]
    rows = []
    for i, (r_old, r_new) in enumerate(zip(OLD["rounds"], ROUNDS)):
        for s in SIDES:
            rows.append([f"R{i + 1} {NAME[s]}", "; ".join(order_text(s, r_old["orders"][s], prev_codes(OLD["rounds"], r_old))),
                         "; ".join(order_text(s, r_new["orders"][s], prev_codes(ROUNDS, r_new)))])
    L += [tbl(["Round, company", "Earlier game (one strategist agent, earlier dashboard)", "This game (ExCo and Board agents, new dashboard)"], rows), ""]
    if XV:
        L += ["Final ΔPV, $B, each game's final state on both versions of the dashboard:", "",
              tbl(["Company", "Earlier game, earlier dashboard (as played)", "Earlier game's state, new dashboard", "This game, new dashboard (as played)",
                   "This game's state, earlier dashboard"],
                  [[NAME[s], n2(XV["earlier_v2"][s]), n2(XV["earlier_v3"][s]), n2(XV["this_v3"][s]), n2(XV["this_v2"][s])] for s in SIDES]), ""]
    for t, x in NAR.COMPARE_POINTS:
        L += [f"**{t}**", strip(x), ""]
    L += ["## Method", "", strip(NAR.METHOD), ""]
    bc = D.get("board_check")
    if bc:
        L += ["### Your dashboard alone against the GM valuation, final state", "",
              tbl(["Player", "Dashboard alone ΔPV $B", "GM valuation ΔPV $B", "GM minus dashboard"],
                  [[NAME[s], n2(bc[s]["board"]), n2(bc[s]["gm"]), n2(bc[s]["gm"] - bc[s]["board"])] for s in SIDES]), "",
              ] + [f"- {NAME[s]}: {NAR.BOARD_WHY.get(s, '')}" for s in SIDES] + ["",
              "With a fixed 50/50 split and the board's own engine moves, the GM engine model gives the board's numbers exactly.", ""]
    with open(out, "w") as f:
        f.write("\n".join(L))
    print("wrote", out)


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "dash_2050_exco_report.md"))
