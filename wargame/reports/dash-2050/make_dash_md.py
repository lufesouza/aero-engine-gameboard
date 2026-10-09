"""Write dash_2050_report.md: the full written report of the dash-2050 war game, round by round, from
data/report_data.json (the same numbers as the HTML page) and the narrative in narrative.py.

Usage: python3 make_dash_md.py [out.md]"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import narrative as NAR  # noqa: E402
import page_kit as K  # noqa: E402
from make_dash_html import (AF, EN, NAME, ROUNDS, FINAL, SIDES, YEARS, RYEARS, D, order_text, BRIDGE_LABEL)  # noqa: E402

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


def tbl(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" if i == 0 else "---:" for i in range(len(head))) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
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
        rows.append([NAME[s], "; ".join(order_text(s, r["orders"][s])), (r["public_statements"].get(s) or "").replace("|", "/")])
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
    L += ["### Value after the round (board valuation; nobody moves afterwards)", ""]
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
    L += ["### Market shares projected after the round", ""]
    yrs = ["2030", "2035", "2040", "2045", "2050", "2055", "2060"]
    sn = r["snapshots"]
    rows = []
    for label, s, k in [("Boeing NB", "boeing", "nb_share"), ("Airbus NB", "airbus", "nb_share"), ("Boeing WB", "boeing", "wb_share"),
                        ("Airbus WB", "airbus", "wb_share"), ("CFM NB engines", "cfm", "nb_share"), ("P&W NB engines", "pratt_whitney", "nb_share"),
                        ("RR NB engines", "rolls_royce", "nb_share"), ("CFM/GE WB engines", "cfm", "wb_share"), ("RR WB engines", "rolls_royce", "wb_share")]:
        rows.append([label] + [pct(sn[y][s][k]) for y in yrs])
    L += [tbl(["Share"] + yrs, rows), ""]
    L += ["### Financials by period (nominal $B)", ""]
    rows = []
    for s in AF:
        for p in r["periods"][s]:
            rows.append([f"{NAME[s]} {p['period']}", f"{p['nb_units']:,.0f}", f"{p['wb_units']:,.0f}", f"{p['revenue']:,.1f}", f"{p['profit']:,.1f}",
                         f"{p['sq_profit']:,.1f}", f"{p['nonrecurring']:,.1f}"])
    L += [tbl(["Airframer", "NB deliveries", "WB deliveries", "Revenue", "Operating profit", "Status-quo profit", "Non-recurring"], rows), ""]
    rows = []
    for s in EN:
        for p in r["periods"][s]:
            rows.append([f"{NAME[s]} {p['period']}", f"{p['nb_units']:,.0f}", f"{p['wb_units']:,.0f}", f"{p['value']:,.1f}", f"{p['sq_value']:,.1f}",
                         f"{p['nonrecurring']:,.1f}"])
    L += [tbl(["Engine maker", "NB engines", "WB engines", "Engine lifecycle value", "Status-quo value", "R&D and write-offs"], rows), ""]
    L += ["### Year by year", ""]
    for s in SIDES:
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
    L += ["### Each player's reasoning (private during the game)", ""]
    for s in SIDES:
        x = r["returned"].get(s) or {}
        ex = x.get("exco") or {}
        L += [f"**{NAME[s]}.** Expected: {x.get('expected_scenario', '')}. Best grid plan there: {x.get('best_grid_plan_in_expected_scenario', '')}. "
              f"Premium {n2(x.get('premium_b', 0) or 0)} $B: {x.get('premium_reason', '')}", "",
              f"- CEO: {ex.get('ceo', '')}", f"- CFO: {ex.get('cfo', '')}", f"- Operations: {ex.get('coo', '')}",
              f"- Decision rule: {ex.get('decision_rule', '')}", f"- Rationale: {x.get('rationale', '')}",
              f"- Predictions: {x.get('predictions', '')}",
              f"- Expected ΔPV {n2(x.get('expected_pv_b', 0) or 0)} $B; board after the round {n2(r['value'][s]['pv_delta'])} $B", ""]
        om = x.get("other_moves") or []
        if om:
            L += ["- Other moves: " + "; ".join(f"{m.get('move', '')} ({'public' if m.get('public') else 'private'})" for m in om), ""]
    return "\n".join(L)


def build(out):
    L = [f"# {NAR.TITLE}", "", "BOEING PROPRIETARY. Boeing Product Development war game on the narrowbody/widebody game-theory dashboard.", "",
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
    for r in ROUNDS:
        L += [round_md(r), ""]
    L += ["## Method", "", strip(NAR.METHOD), ""]
    bc = D.get("board_check")
    if bc:
        L += ["### Your board alone against the GM valuation, final state", "",
              tbl(["Player", "Board alone ΔPV $B", "GM valuation ΔPV $B", "Difference"],
                  [[NAME[s], n2(bc[s]["board"]), n2(bc[s]["gm"]), n2(bc[s]["gm"] - bc[s]["board"])] for s in SIDES]), "",
              "Airbus differs by the Delay Tactics spending window; the engine makers by the GM's year-by-year narrowbody split "
              "(the board uses a fixed 50/50). With a fixed 50/50 split the GM engine model gives the board's numbers exactly.", ""]
    with open(out, "w") as f:
        f.write("\n".join(L))
    print("wrote", out)


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "dash_2050_report.md"))
