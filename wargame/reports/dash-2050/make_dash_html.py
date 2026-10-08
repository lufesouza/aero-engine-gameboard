"""Build dash_2050_wargame.html: the five-player war game played on the user's game-theory dashboard (rounds 2030,
2035, 2045, 2050), with summaries and full per-round detail.

Every number comes from data/report_data.json, written by wargame/dashgame/reports.py from the game record. The
narrative (what happened and why) is in narrative.py and cites only those numbers and the players' own returns.

Usage: python3 make_dash_html.py [out.html]"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import page_kit as K  # noqa: E402
import narrative as NAR  # noqa: E402

esc = K.esc
D = json.load(open(os.path.join(HERE, "data", "report_data.json")))
ROUNDS = D["rounds"]
FINAL = ROUNDS[-1]
SIDES = ["boeing", "airbus", "cfm", "pratt_whitney", "rolls_royce"]
NAME = {"boeing": "Boeing", "airbus": "Airbus", "cfm": "CFM/GE", "pratt_whitney": "Pratt & Whitney", "rolls_royce": "Rolls-Royce"}
AF, EN = ["boeing", "airbus"], ["cfm", "pratt_whitney", "rolls_royce"]
YEARS = FINAL["years"]["year"]
RYEARS = [r["year"] for r in ROUNDS]
SEQ = ["seq1", "seq2", "seq3", "seq4"]          # rounds 1-4, light to dark (ordinal)
CODE_LABEL = {1: "RR", 2: "P&W", 3: "CFM", 4: "RR & P&W Joint Venture", 5: "RR and CFM", 6: "P&W and CFM", 7: "RR, P&W and CFM"}


def pct(v, dp=1):
    return f"{K.rnd(v * 100, dp):.{dp}f}%"


def b(v, dp=2, sign=True):
    return K.usd(v, dp, sign)


def ser(side, key, block=None):
    blk = (block or FINAL)["years"][side][key]
    return list(zip(YEARS, blk))


# ─────────────────────────────── order text ───────────────────────────────
ORDER_TXT = {
    "fps": {"launch_7yr": "Launch fps, 7-year ramp-up", "launch_10yr": "Launch fps, 10-year ramp-up",
            "launch_via_embraer": "Launch fps via Embraer", "cancel": "Cancel fps"},
    "rate_737": {"increase": "Increase 737 rate"},
    "re787": {"launch": "Launch 787 Re-engine", "cancel": "Cancel 787 Re-engine"},
    "ngsa": {"launch": "Launch NGSA", "cancel": "Cancel NGSA"},
    "rea350": {"launch": "Launch A350 Re-engine", "cancel": "Cancel A350 Re-engine"},
    "delay_tactics": {"bottleneck": "Delay Tactics: supply-chain bottleneck (covert)", "poaching": "Delay Tactics: talent poaching (covert)",
                      "both": "Delay Tactics: bottleneck and poaching (covert)"},
    "ducted": {"launch": "Launch ducted engine", "cancel": "Cancel ducted engine"},
    "open_fan": {"launch": "Launch Open Fan", "cancel": "Cancel Open Fan"},
    "partner_embraer": {"launch": "Partner with Embraer", "cancel": "End Embraer partnership"},
    "lobby_emissions": {"launch": "Lobby governments on emissions"},
    "genx": {"upgrade_genx9": "GEnx upgrade", "invest_genx": "GEnx investment", "cancel": "Cancel GEnx programme"},
    "gtf2_solo": {"launch": "Launch GTF2 Solo", "launch_if_selected": "Launch GTF2 if selected", "cancel": "Cancel GTF2"},
    "jv_with_rr": {"commit": "Commit to Joint Venture with RR", "withdraw": "Withdraw Joint Venture commitment"},
    "ultrafan_nb_solo": {"launch": "Launch UltraFan NB Solo", "launch_if_selected": "Launch UltraFan NB if selected", "cancel": "Cancel UltraFan NB"},
    "jv_with_pw": {"commit": "Commit to Joint Venture with P&W", "withdraw": "Withdraw Joint Venture commitment"},
    "ultrafan_wb": {"launch": "Launch UltraFan WB", "cancel": "Cancel UltraFan WB"},
    "t1000_upgrade": {"launch": "Launch Trent 1000 upgrade", "cancel": "Cancel Trent 1000 upgrade"},
}


def order_text(side, o):
    parts = []
    for k, v in o.items():
        if k.endswith("engine_code"):
            continue
        t = ORDER_TXT.get(k, {}).get(v)
        if t:
            if k in ("fps", "ngsa") and v.startswith("launch"):
                code = o.get(k + "_engine_code")
                if code:
                    t += f" (engines requested: {CODE_LABEL[int(code)]})"
            parts.append(t)
    for k in ("fps_engine_code", "ngsa_engine_code"):
        if o.get(k) and not str(o.get(k[:-12], "")).startswith("launch"):
            parts.append(f"{'fps' if k.startswith('fps') else 'NGSA'} engines: {CODE_LABEL[int(o[k])]}")
    return parts or ["Do Nothing"]


# ─────────────────────────────── charts ───────────────────────────────
def chart_dpv_rounds():
    """Dot plot: each player's ΔPV as the board values the state after each round."""
    w, left, right, top, row = 760, 150, 96, 40, 46
    h = top + row * len(SIDES) + 34
    vals = [r["value"][s]["pv_delta"] for r in ROUNDS for s in SIDES]
    lo = min(-10, 10 * (min(vals) // 10)); hi = max(10, 10 * (max(vals) // 10 + 1))
    sx = lambda v: left + (v - lo) / (hi - lo) * (w - left - right)
    out = [K.svg_open(w, h, "Change in present value by player after each round")]
    t = lo
    while t <= hi + 1e-9:
        cls = "zero" if abs(t) < 1e-9 else "grid"
        out.append(f'<line x1="{sx(t):.1f}" x2="{sx(t):.1f}" y1="{top - 10}" y2="{h - 30}" class="{cls}"/>'
                   f'<text x="{sx(t):.1f}" y="{h - 12}" text-anchor="middle" class="tick">{K.num(t, "+.0f") if t else "0"}</text>')
        t += 10
    for i, s in enumerate(SIDES):
        y = top + i * row + row / 2
        out.append(f'<text x="{left - 12}" y="{y + 5:.1f}" text-anchor="end" class="rowlab">{esc(NAME[s])}</text>')
        xs = [sx(r["value"][s]["pv_delta"]) for r in ROUNDS]
        out.append(f'<line x1="{min(xs):.1f}" x2="{max(xs):.1f}" y1="{y:.1f}" y2="{y:.1f}" class="conn"/>')
        for j, r in enumerate(ROUNDS):
            v = r["value"][s]["pv_delta"]
            attrs = K.mark_attrs((K.num(v) + " $B", f"{NAME[s]} after round {j + 1} ({r['year']})", None))
            out.append(f'<circle cx="{xs[j]:.1f}" cy="{y:.1f}" r="7" fill="var(--{SEQ[j]})" class="ring" {attrs}/>')
        v = ROUNDS[-1]["value"][s]["pv_delta"]
        out.append(f'<text x="{w - right + 10}" y="{y + 4:.1f}" class="val">{K.num(v)}</text>')
    out.append(f'<text x="{left}" y="{top - 22}" class="tick">ΔPV against the status quo, $B at 2026 (board valuation; nobody moves after the round)</text>')
    out.append("</svg>")
    rows = [[NAME[s]] + [K.num(r["value"][s]["pv_delta"]) for r in ROUNDS] for s in SIDES]
    legend = "".join(f'<span><i class="sq" style="background:var(--{SEQ[j]})"></i>After round {j + 1} ({r["year"]})</span>' for j, r in enumerate(ROUNDS))
    return (f'<div class="legend">{legend}</div><div class="cw">{"".join(out)}</div>'
            + K.tview("ΔPV by round, $B", ["Player"] + [f"After {y}" for y in RYEARS], rows))


def spread(values, y_lo, y_hi, gap=15, plot_h=274):
    """dy offsets (px) that keep end labels at least `gap` px apart (line_chart's plot area is 274 px tall)."""
    pos = [(y_hi - v) / (y_hi - y_lo) * plot_h for v in values]
    order = sorted(range(len(values)), key=lambda i: pos[i])
    placed = {}
    last = None
    for i in order:
        p = pos[i] if last is None else max(pos[i], last + gap)
        placed[i] = p
        last = p
    return [placed[i] - pos[i] for i in range(len(values))]


def share_chart(sides, key, title, aria, refs, block=None, y_hi=1.0, step=.2):
    blk = block or FINAL
    cols = ["s1", "s2", "s3"]
    series = [(NAME[s], cols[i], [(y, v) for y, v in zip(YEARS, blk["years"][s][key])]) for i, s in enumerate(sides)]
    last = [blk["years"][s][key][-1] for s in sides]
    ends = list(zip(spread(last, 0, y_hi), [f"{NAME[s]} {pct(v, 0)}" for s, v in zip(sides, last)]))
    notes = [(y, f"R{j + 1}") for j, y in enumerate(RYEARS)]
    svg = K.line_chart(series, 0, y_hi, step, "pct", title, refs=refs, aria_label=aria, end_labels=ends, notes=notes,
                       x_lo=2026, x_hi=2060)
    rows = [[str(y)] + [pct(blk["years"][s][key][i]) for s in sides] for i, y in enumerate(YEARS)]
    return f'<div class="cw">{svg}</div>' + K.tview(title, ["Year"] + [NAME[s] for s in sides], rows)


def chart_boeing_paths():
    series = []
    for j, r in enumerate(ROUNDS):
        series.append((f"After round {j + 1} ({r['year']})", SEQ[j], [(y, v) for y, v in zip(YEARS, r["years"]["boeing"]["nb_share"])]))
    last = [r["years"]["boeing"]["nb_share"][-1] for r in ROUNDS]
    ends = list(zip(spread(last, 0, .8), [f"R{j + 1}: {pct(v, 0)}" for j, v in enumerate(last)]))
    svg = K.line_chart(series, 0, .8, .1, "pct", "Boeing share of narrowbody deliveries, as projected after each round",
                       refs=[(.5, "50/50 objective", "above"), (.4, "status quo 40%", "below")],
                       aria_label="Boeing narrowbody share as projected after each round", end_labels=ends, notes=[], x_lo=2026, x_hi=2060)
    rows = [[str(y)] + [pct(r["years"]["boeing"]["nb_share"][i]) for r in ROUNDS] for i, y in enumerate(YEARS)]
    return f'<div class="cw">{svg}</div>' + K.tview("Boeing NB share by projection", ["Year"] + [f"After {y}" for y in RYEARS], rows)


def chart_gantt():
    progs = FINAL["timeline"]["programmes"]
    w, left, right, top, row = 760, 250, 20, 30, 26
    h = top + row * len(progs) + 40
    x_lo, x_hi = 2026, 2062
    sx = lambda x: left + (x - x_lo) / (x_hi - x_lo) * (w - left - right)
    out = [K.svg_open(w, h, "Programme timeline: launch to entry into service or engine ready")]
    for yr in range(2030, x_hi + 1, 5):
        out.append(f'<line x1="{sx(yr):.1f}" x2="{sx(yr):.1f}" y1="{top - 6}" y2="{h - 34}" class="grid"/>'
                   f'<text x="{sx(yr):.1f}" y="{h - 18}" text-anchor="middle" class="tick">{yr}</text>')
    for j, yr in enumerate(RYEARS):
        out.append(f'<line x1="{sx(yr):.1f}" x2="{sx(yr):.1f}" y1="{top - 14}" y2="{h - 34}" class="ref"/>'
                   f'<text x="{sx(yr) + 3:.1f}" y="{top - 16}" class="ann">R{j + 1}</text>')
    for i, p in enumerate(progs):
        y = top + i * row
        cancelled = "cancel" in p["status"] or "folded" in p["status"]
        end = p["due"]
        cls = "b neg" if cancelled else ("b pos" if p["owner"] in ("boeing", "airbus") else "b t41")
        out.append(f'<text x="{left - 10}" y="{y + 15}" text-anchor="end" class="rowlab sm">{esc(p["name"])}</text>')
        x0, x1 = sx(p["launch"]), sx(end)
        out.append(f'<path d="{K.hbar_path(x0, max(x1, x0 + 3), y + 4, 14)}" class="{cls}" '
                   f'{K.mark_attrs((p["status"], p["name"] + ": launched " + str(p["launch"]) + ", " + p["due_kind"] + " " + str(end), None))}/>')
        out.append(f'<text x="{max(x1, x0 + 3) + 5:.1f}" y="{y + 15}" class="val sm">{esc(p["due_kind"])} {end}{" (cancelled)" if cancelled else ""}</text>')
    out.append("</svg>")
    legend = ('<div class="legend"><span><i class="bar" style="background:var(--pos)"></i>Airframe programme</span>'
              '<span><i class="bar" style="background:var(--s1)"></i>Engine programme</span>'
              '<span><i class="bar" style="background:var(--neg)"></i>Cancelled or folded</span></div>')
    rows = [[esc(p["name"]), str(p["launch"]), f'{p["due_kind"]} {p["due"]}', esc(p["status"])] for p in progs]
    return legend + f'<div class="cw">{"".join(out)}</div>' + K.tview("Programme timeline", ["Programme", "Launched", "Due", "Status"], rows, num_cols=[1])


def chart_money(side, key, sq_key, title):
    series = [("This game", "s1", ser(side, key)), ("Status quo", "sq", ser(side, sq_key))]
    vals = FINAL["years"][side][key] + FINAL["years"][side][sq_key]
    hi = max(5, 5 * (int(max(vals) / 5) + 1))
    last = [FINAL["years"][side][key][-1], FINAL["years"][side][sq_key][-1]]
    ends = list(zip(spread(last, 0, hi), [f"Game {K.rnd(last[0], 1):.1f}", f"Status quo {K.rnd(last[1], 1):.1f}"]))
    step = 5 if hi <= 30 else 10
    svg = K.line_chart(series, 0, hi, step, "int", title, refs=[], aria_label=f"{NAME[side]}: {title}", end_labels=ends,
                       notes=[(y, f"R{j + 1}") for j, y in enumerate(RYEARS)], x_lo=2026, x_hi=2060)
    return f'<div class="cw">{svg}</div>'


# ─────────────────────────────── tables ───────────────────────────────
def decisions_table(r):
    rows = []
    for s in SIDES:
        o = r["orders"][s]
        txt = order_text(s, o)
        adj = r["adjustments"].get(s) or []
        cell = "<br>".join(esc(t) for t in txt)
        if adj:
            cell += '<br><span class="muted small">GM adjustment: ' + esc("; ".join(adj)) + "</span>"
        st = r["public_statements"].get(s) or ""
        rows.append([esc(NAME[s]), cell, f'<span class="small">{esc(st)}</span>'])
    return K.table(["Player", "Orders (as adjudicated)", "Public statement"], rows)


def value_table(r):
    rows = []
    for s in SIDES:
        v = r["value"][s]
        rows.append([esc(NAME[s]), K.num(v["pv_delta"]), f'{K.rnd(v["yield"], 1):.1f}%'])
    return K.table(["Player", "ΔPV $B", "Yield"], rows, num_cols=(1, 2))


def shares_table(r):
    yrs = [2030, 2035, 2040, 2045, 2050, 2055, 2060]
    sn = r["snapshots"]
    rows = []
    for label, s, k in [("Boeing NB", "boeing", "nb_share"), ("Airbus NB", "airbus", "nb_share"), ("Boeing WB (787)", "boeing", "wb_share"),
                        ("Airbus WB (A350)", "airbus", "wb_share"), ("CFM NB engines", "cfm", "nb_share"),
                        ("P&W NB engines", "pratt_whitney", "nb_share"), ("RR NB engines", "rolls_royce", "nb_share"),
                        ("CFM/GE WB engines", "cfm", "wb_share"), ("RR WB engines", "rolls_royce", "wb_share")]:
        rows.append([label] + [pct(sn[str(y)][s][k]) for y in yrs])
    return K.table(["Market share"] + [str(y) for y in yrs], rows, num_cols=tuple(range(1, 8)))


def periods_table(r):
    rows = []
    for s in AF:
        for p in r["periods"][s]:
            rows.append([f"{NAME[s]} {p['period']}", f"{p['nb_units']:,.0f}", f"{p['wb_units']:,.0f}", f"{p['revenue']:,.1f}",
                         f"{p['profit']:,.1f}", f"{p['sq_profit']:,.1f}", f"{p['nonrecurring']:,.1f}"])
    t1 = K.table(["Airframer, period", "NB deliveries", "WB deliveries", "Revenue $B", "Operating profit $B", "Status-quo profit $B",
                  "Non-recurring $B"], rows, num_cols=(1, 2, 3, 4, 5, 6))
    rows = []
    for s in EN:
        for p in r["periods"][s]:
            rows.append([f"{NAME[s]} {p['period']}", f"{p['nb_units']:,.0f}", f"{p['wb_units']:,.0f}", f"{p['value']:,.1f}",
                         f"{p['sq_value']:,.1f}", f"{p['nonrecurring']:,.1f}"])
    t2 = K.table(["Engine maker, period", "NB engines", "WB engines", "Engine lifecycle value $B", "Status-quo value $B",
                  "R&D and write-offs $B"], rows, num_cols=(1, 2, 3, 4, 5))
    return t1 + '<p class="cap">Nominal $B, summed over each period. Non-recurring spend is booked as the board books it: each airframe programme in full at its entry into service.</p>' + t2


BRIDGE_LABEL = {"nb_profit_vs_sq": "NB operating profit vs status quo", "wb_profit_vs_sq": "WB operating profit vs status quo",
                "programme_investment": "Programme investment", "rate_hike": "737 rate increase", "delay_tactics_spend": "Delay Tactics spend",
                "write_offs": "Cancellation write-offs", "debt_penalty": "Debt penalty (α)", "two_front_strain": "Two-front strain",
                "naked_fine": "Naked Delay Tactics fine", "engine_value_vs_sq": "Engine value vs status quo", "r_and_d": "R&D",
                "strain": "Strain", }


def bridge_table(r):
    keys = []
    for s in SIDES:
        for k in r["value"][s]["bridge"]:
            if k not in keys:
                keys.append(k)
    rows = []
    for k in keys:
        cells = []
        for s in SIDES:
            v = r["value"][s]["bridge"].get(k)
            cells.append(K.num(v) if v is not None and abs(v) > 1e-9 else "—")
        if any(c != "—" for c in cells):
            rows.append([BRIDGE_LABEL.get(k, k)] + cells)
    rows.append(["<b>ΔPV</b>"] + [f'<b>{K.num(r["value"][s]["pv_delta"])}</b>' for s in SIDES])
    return K.table(["Component, PV $B at 2026"] + [NAME[s] for s in SIDES], rows, num_cols=(1, 2, 3, 4, 5))


def year_table(r, side):
    y = r["years"][side]
    if side in AF:
        head = ["Year", "NB share", "WB share", "NB deliveries", "WB deliveries", "NB price $M", "NB margin", "Revenue $B", "Operating profit $B", "Status-quo profit $B", "Non-recurring $B"]
        rows = [[str(yr), pct(y["nb_share"][i]), pct(y["wb_share"][i]), f'{y["nb_units"][i]:,.0f}', f'{y["wb_units"][i]:,.0f}',
                 f'{y["nb_price"][i]:.0f}', pct(y["nb_margin"][i]), f'{y["revenue"][i]:,.1f}', f'{y["profit"][i]:,.2f}', f'{y["sq_profit"][i]:,.2f}',
                 (f'{y["nonrecurring"][i]:,.2f}' if y["nonrecurring"][i] else "—")] for i, yr in enumerate(YEARS)]
    else:
        head = ["Year", "NB engine share", "WB engine share", "NB engines", "WB engines", "Engine lifecycle value $B", "Status-quo value $B", "R&D and write-offs $B"]
        rows = [[str(yr), pct(y["nb_share"][i]), pct(y["wb_share"][i]), f'{y["nb_units"][i]:,.0f}', f'{y["wb_units"][i]:,.0f}',
                 f'{y["value"][i]:,.2f}', f'{y["sq_value"][i]:,.2f}', (f'{y["nonrecurring"][i]:,.2f}' if y["nonrecurring"][i] else "—")]
                for i, yr in enumerate(YEARS)]
    return K.tview(f"{NAME[side]}, year by year after round {r['round']} ({r['year']})", head, rows)


def objectives_table(r):
    rows = []
    for s in SIDES:
        for o in r["objectives"][s]:
            rows.append([esc(NAME[s]), esc(o["label"]), "met" if o["met"] else "not met", esc(o["detail"])])
    return K.table(["Player", "Objective metric", "Status", "Detail"], rows)


def regret_table():
    R = D["regret"]
    rows = []
    for s in SIDES:
        cells = []
        for n in range(1, len(ROUNDS) + 1):
            x = R[str(n)][s]
            cells.append(f'{K.num(x["regret_ex_post"])}')
        best = [R[str(n)][s]["best_ex_post"]["plan"] for n in range(1, len(ROUNDS) + 1)]
        rows.append([esc(NAME[s])] + cells)
    return K.table(["Player"] + [f"Round {n} ({y})" for n, y in enumerate(RYEARS, 1)], rows, num_cols=tuple(range(1, len(ROUNDS) + 1)))


def stage_table():
    S = D.get("stage") or {}
    rows = []
    for n in range(1, len(ROUNDS) + 1):
        x = S.get(str(n))
        if not x:
            continue
        eq = "<br>".join(f"Boeing: {esc(p[0])} · Airbus: {esc(p[1])} ({K.num(p[2])} / {K.num(p[3])})" for p in x["pure"]) or "none"
        pv = x["played_value"]
        played = f"Boeing: {esc(x['played'][0] or '?')} · Airbus: {esc(x['played'][1] or '?')} ({K.num(pv[0])} / {K.num(pv[1])})"
        rows.append([f"Round {n} ({x['year']})", eq, played,
                     f"Boeing {esc(x['boeing_best_response_to_played_airbus'][0])} ({K.num(x['boeing_best_response_to_played_airbus'][1])})<br>"
                     f"Airbus {esc(x['airbus_best_response_to_played_boeing'][0])} ({K.num(x['airbus_best_response_to_played_boeing'][1])})"])
    if not rows:
        return ""
    return ('<p class="label">The airframer stage game on the board, each round (engine makers as played; nobody moves later; ΔPV $B Boeing / Airbus)</p>'
            + K.table(["Round", "Pure equilibria", "What was played", "Best reply to the other's actual play"], rows))


def regret_detail():
    R = D["regret"]
    rows = []
    for n in range(1, len(ROUNDS) + 1):
        for s in SIDES:
            x = R[str(n)][s]
            act = order_text(s, ROUNDS[n - 1]["orders"][s])
            rows.append([f"R{n} {esc(NAME[s])}", esc("; ".join(act)), K.num(x["actual_ex_post"]), esc(x["best_ex_post"]["plan"]),
                         K.num(x["best_ex_post"]["ex_post"]), K.num(x["regret_ex_post"]), K.num(x["regret_myopic"])])
    return K.tview("Regret by round and player", ["Round, player", "Actual orders", "Final ΔPV (actual)", "Best alternative (ex post)",
                                                  "Its final ΔPV", "Regret ex post", "Regret myopic"], rows, num_cols=[2, 4, 5, 6])


def rationale_block(r):
    out = []
    for s in SIDES:
        x = r["returned"].get(s) or {}
        ex = x.get("exco") or {}
        om = x.get("other_moves") or []
        oms = "".join(f'<li>{esc(m.get("move", ""))}{" (public)" if m.get("public") else " (private)"}{(": " + esc(m.get("detail", ""))) if m.get("detail") else ""}</li>' for m in om)
        out.append(f'''<details class="tv"><summary>{esc(NAME[s])}: ExCo deliberation and rationale</summary><div class="panel stack small">
<p><b>Expected scenario.</b> {esc(str(x.get("expected_scenario", "")))}</p>
<p><b>Best grid plan in that scenario.</b> {esc(str(x.get("best_grid_plan_in_expected_scenario", "")))}. <b>Premium paid:</b> {esc(K.num(x.get("premium_b", 0) or 0))} $B. {esc(str(x.get("premium_reason", "")))}</p>
<p><b>CEO.</b> {esc(str(ex.get("ceo", "")))}</p><p><b>CFO.</b> {esc(str(ex.get("cfo", "")))}</p><p><b>Operations.</b> {esc(str(ex.get("coo", "")))}</p>
<p><b>Decision rule.</b> {esc(str(ex.get("decision_rule", "")))}</p>
<p><b>Rationale.</b> {esc(str(x.get("rationale", "")))}</p>
<p><b>Objective.</b> {esc(str(x.get("objective_note", "")))}</p>
<p><b>Predictions.</b> {esc(str(x.get("predictions", "")))}</p>
<p><b>Expected ΔPV.</b> {esc(K.num(x.get("expected_pv_b", 0) or 0))} $B (board after the round: {esc(K.num(r["value"][s]["pv_delta"]))} $B)</p>
{("<p><b>Other moves.</b></p><ul>" + oms + "</ul>") if oms else ""}
</div></details>''')
    return "".join(out)


def round_section(r):
    n = r["round"]
    tl = r["timeline"]
    fit = tl["engine_fit"]
    fit_rows = [[("fps" if k == "fps" else "NGSA"), esc(f["requested"]), esc(f["fitted_if_no_change"]), esc(f["note"] or "—")] for k, f in fit.items()]
    covert = [f"{k} ordered {y}" for k, y in tl["delay_tactics"].items() if y]
    nar = NAR.ROUNDS.get(n, {})
    return f'''<section id="r{n}"><p class="eyebrow">Round {n} · decision year {r["year"]}</p><h2>{esc(nar.get("title", f"Round {n}"))}</h2>
<p class="lede">{nar.get("lede", "")}</p>
<div class="stack">
<div class="panel"><p class="label">What each player ordered</p>{decisions_table(r)}
{('<p class="cap"><b>Covert (revealed after the game):</b> Airbus Delay Tactics ' + esc(", ".join(covert)) + ".</p>") if covert else ""}</div>
<div class="grid2"><div class="panel"><p class="label">Value after the round (board; nobody moves later)</p>{value_table(r)}</div>
<div class="panel"><p class="label">Engines on the new narrowbodies</p>{K.table(["Airframe", "Requested", "Fitted", "Note"], fit_rows) if fit_rows else '<p class="muted">No new narrowbody launched yet.</p>'}</div></div>
<div class="panel"><p class="label">Market shares projected after the round</p>{shares_table(r)}</div>
<div class="panel"><p class="label">Financials projected after the round</p>{periods_table(r)}{bridge_table(r)}
{"".join(year_table(r, s) for s in SIDES)}</div>
<div class="panel"><p class="label">Each player's reasoning (private during the game)</p>{rationale_block(r)}</div>
</div></section>'''


def audit_table():
    A = D.get("audit") or {}
    if not A:
        return ""
    rows = []
    for s in SIDES:
        cells = []
        for n in range(1, len(ROUNDS) + 1):
            a = (A.get(str(n)) or {}).get(s)
            cells.append("—" if not a else (f'clean ({a["tool_calls"]} calls)' if a["clean"] else
                                            f'check: {len(a["foreign_paths"])} foreign paths, {len(a["denied"])} denials'))
        rows.append([esc(NAME[s])] + cells)
    return ('<p class="label">Isolation audit of every player agent\'s tool calls</p>'
            + K.table(["Player"] + [f"Round {n}" for n in range(1, len(ROUNDS) + 1)], rows))


def tiles():
    out = []
    for s in SIDES:
        v = FINAL["value"][s]
        obj = FINAL["objectives"][s]
        met = sum(1 for o in obj if o["met"])
        out.append(f'<div class="panel tile"><div class="k">{esc(NAME[s])}</div><div class="v">{b(v["pv_delta"])}</div>'
                   f'<div class="d">Yield {K.rnd(v["yield"], 1):.1f}% · objectives met {met} of {len(obj)}<br>{esc(NAR.TILES.get(s, ""))}</div></div>')
    return '<div class="tiles">' + "".join(out) + "</div>"


def build(out_path):
    css = K.CSS.replace("--pos: #3b4a5e; --neg: #8792a3;",
                        "--pos: #3b4a5e; --neg: #8792a3; --sq: #8a95a5; --seq1: #9ec5f4; --seq2: #5598e7; --seq3: #256abf; --seq4: #0d366b;")
    css = css.replace("--pos: #c9d3e0; --neg: #5d6a7c; color-scheme: dark; }",
                      "--pos: #c9d3e0; --neg: #5d6a7c; --sq: #6f7b8d; --seq1: #184f95; --seq2: #256abf; --seq3: #5598e7; --seq4: #b7d3f6; color-scheme: dark; }")
    rounds_html = "".join(round_section(r) for r in ROUNDS)
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>dash-2050 War Game</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{css}</style></head><body><div class="wrap">
<header class="top"><p class="eyebrow">Boeing Product Development · war game on the game-theory dashboard · BOEING PROPRIETARY</p>
<h1>{esc(NAR.TITLE)}</h1><p class="lede">{NAR.LEDE}</p>
<nav class="toc"><a href="#summary">Summary</a><a href="#shares">Market shares</a><a href="#money">Financials</a><a href="#timeline">Dates</a>
{"".join(f'<a href="#r{r["round"]}">Round {r["round"]} ({r["year"]})</a>' for r in ROUNDS)}<a href="#play">How well each played</a><a href="#method">Method</a></nav></header>

<section id="summary"><h2>Summary</h2>{tiles()}
<div class="bl">{"".join(f'<div class="panel"><div><b>{esc(t)}</b>{x}</div></div>' for t, x in NAR.FINDINGS)}</div>
<div class="panel" style="margin-top:14px"><p class="ctitle">{esc(NAR.DPV_TITLE)}</p>{chart_dpv_rounds()}</div>
<div class="panel" style="margin-top:14px"><p class="label">Objectives at the end of the game</p>{objectives_table(FINAL)}</div></section>

<section id="shares"><h2>Market shares</h2><p class="lede">{NAR.SHARES_LEDE}</p><div class="stack">
<div class="panel"><p class="ctitle">{esc(NAR.NB_TITLE)}</p>{share_chart(AF, "nb_share", "Share of narrowbody deliveries", "Narrowbody shares by year", [(.5, "50/50", "above")])}</div>
<div class="panel"><p class="ctitle">{esc(NAR.BOEING_PATH_TITLE)}</p>{chart_boeing_paths()}</div>
<div class="panel"><p class="ctitle">{esc(NAR.WB_TITLE)}</p>{share_chart(AF, "wb_share", "Share of widebody deliveries", "Widebody shares by year", [])}</div>
<div class="panel"><p class="ctitle">{esc(NAR.ENG_NB_TITLE)}</p>{share_chart(EN, "nb_share", "Share of narrowbody engines", "Narrowbody engine shares by year", [(.5, "50%", "above")])}</div>
<div class="panel"><p class="ctitle">{esc(NAR.ENG_WB_TITLE)}</p>{share_chart(EN, "wb_share", "Share of widebody engines", "Widebody engine shares by year", [(.5, "50%", "above")])}</div>
</div></section>

<section id="money"><h2>Financials</h2><p class="lede">{NAR.MONEY_LEDE}</p><div class="stack">
<div class="panel"><p class="label">How each player's final ΔPV is built</p>{bridge_table(FINAL)}</div>
<div class="grid2"><div class="panel"><p class="ctitle">Boeing operating profit, $B a year</p>{chart_money("boeing", "profit", "sq_profit", "Boeing operating profit, $B nominal")}</div>
<div class="panel"><p class="ctitle">Airbus operating profit, $B a year</p>{chart_money("airbus", "profit", "sq_profit", "Airbus operating profit, $B nominal")}</div></div>
<div class="grid2"><div class="panel"><p class="ctitle">CFM/GE engine lifecycle value, $B a year</p>{chart_money("cfm", "value", "sq_value", "CFM/GE engine value, $B nominal")}</div>
<div class="panel"><p class="ctitle">Pratt &amp; Whitney engine lifecycle value, $B a year</p>{chart_money("pratt_whitney", "value", "sq_value", "P&W engine value, $B nominal")}</div></div>
<div class="grid2"><div class="panel"><p class="ctitle">Rolls-Royce engine lifecycle value, $B a year</p>{chart_money("rolls_royce", "value", "sq_value", "RR engine value, $B nominal")}</div>
<div class="panel"><p class="label">Totals by period (final state)</p>{periods_table(FINAL)}</div></div>
{"".join(year_table(FINAL, s) for s in SIDES)}
</div></section>

<section id="timeline"><h2>Programme dates</h2><p class="lede">{NAR.TIMELINE_LEDE}</p><div class="panel">{chart_gantt()}</div></section>

{rounds_html}

<section id="play"><h2>How well each player played</h2><p class="lede">{NAR.PLAY_LEDE}</p><div class="stack">
<div class="panel">{stage_table()}</div>
<div class="panel"><p class="label">Regret by round, $B (final ΔPV of the best alternative minus the actual, holding everyone else's actual orders)</p>{regret_table()}{regret_detail()}</div>
<div class="bl">{"".join(f'<div class="panel"><div><b>{esc(t)}</b>{x}</div></div>' for t, x in NAR.PLAY_POINTS)}</div>
</div></section>

<section id="method"><h2>Method</h2><div class="panel stack">{NAR.METHOD}{audit_table()}</div></section>
<footer>{NAR.FOOTER}</footer></div>
<script>{K.JS}</script></body></html>'''
    with open(out_path, "w") as f:
        f.write(page)
    print("wrote", out_path, len(page))


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "dash_2050_wargame.html"))
