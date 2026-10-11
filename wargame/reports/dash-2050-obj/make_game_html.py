"""Build dash_2050_obj_wargame.html: the dash-2050 ExCo and Board war game replayed with Control's added objectives
(Boeing repairs its balance sheet; Boeing and Airbus seek a stable engine supply; Rolls-Royce protects its widebody
cash cow) and each company's 2026 analyst-model baseline, on the user's combined_dash.py board (rounds 2030, 2035,
2045, 2050). Summaries, the objectives scorecard, Boeing's net-debt path, the engine sources, the decision chain of
each company in each round, and the comparison with the previous ExCo game (run dash-2050-exco).

Every number comes from data/report_data.json, written by wargame/dashgame/reports.py from the game record. The
narrative (what happened and why) is in narrative.py and cites only those numbers and the players' own returns.

Usage: python3 make_game_html.py [out.html]"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import page_kit as K  # noqa: E402
import narrative as NAR  # noqa: E402

esc = K.esc
D = json.load(open(os.path.join(HERE, "data", "report_data.json")))
XV = None
OLD = json.load(open(os.path.join(HERE, "..", "dash-2050-exco", "data", "report_data.json")))     # the previous ExCo game
PREV = json.load(open(os.path.join(HERE, "data", "compare_prev.json")))     # the previous game scored on Control's objectives
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


def order_text(side, o, prev_codes=None):
    """Orders in words. An engine code restated unchanged from `prev_codes` (codes after the previous round) is not an
    order and is left out."""
    o = dict(o)
    for k in ("fps_engine_code", "ngsa_engine_code"):
        key = k[:-12]
        if prev_codes and o.get(k) and str(prev_codes.get(key)) == str(o.get(k)) and not str(o.get(key, "")).startswith("launch"):
            o[k] = None
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
    out.append(f'<text x="10" y="{top - 22}" class="tick">ΔPV vs status quo, $B at 2026 (nobody moves after the round)</text>')
    out.append("</svg>")
    rows = [[NAME[s]] + [K.num(r["value"][s]["pv_delta"]) for r in ROUNDS] for s in SIDES]
    legend = "".join(f'<span><i class="sq" style="background:var(--{SEQ[j]})"></i>After round {j + 1} ({r["year"]})</span>' for j, r in enumerate(ROUNDS))
    return (f'<div class="legend">{legend}</div><div class="cw">{"".join(out)}</div>'
            + K.tview("ΔPV by round, $B", ["Player"] + [f"After {y}" for y in RYEARS], rows))


def spread(values, y_lo, y_hi, gap=18, plot_h=274, floor=14):
    """dy offsets (px) that keep end labels at least `gap` apart (18 also clears the larger phone font) and at least
    `floor` above the x-axis tick row. line_chart's plot area is 274 px tall."""
    pos = [(y_hi - v) / (y_hi - y_lo) * plot_h for v in values]
    order = sorted(range(len(values)), key=lambda i: pos[i])
    placed = {}
    last = None
    for i in order:
        p = pos[i] if last is None else max(pos[i], last + gap)
        placed[i] = p
        last = p
    limit = plot_h - floor
    for i in reversed(order):                 # push the lowest labels up off the tick row, keeping the gaps
        if placed[i] > limit:
            placed[i] = limit
        limit = placed[i] - gap
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
    # rounds that end on the same value share one label (the later lines draw over the earlier ones)
    labels = []
    for j, v in enumerate(last):
        same = [k for k, w in enumerate(last) if abs(w - v) < 1e-9]
        if j == same[-1]:
            tag = f"R{same[0] + 1}" if len(same) == 1 else f"R{same[0] + 1}-R{same[-1] + 1}"
            labels.append(f"{tag}: {pct(v, 0)}")
        else:
            labels.append("")
    ends = list(zip(spread([v if lab else -1 for v, lab in zip(last, labels)], 0, .8), labels))
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
        out.append(f'<text x="{left - 10}" y="{y + 15}" text-anchor="end" class="rowlab sm">{esc(p["name"].replace("production-rate ", "rate "))}</text>')
        x0, x1 = sx(p["launch"]), sx(end)
        out.append(f'<path d="{K.hbar_path(x0, max(x1, x0 + 3), y + 4, 14)}" class="{cls}" '
                   f'{K.mark_attrs((p["status"], p["name"] + ": launched " + str(p["launch"]) + ", " + p["due_kind"] + " " + str(end), None))}/>')
        out.append(f'<text x="{max(x1, x0 + 3) + 5:.1f}" y="{y + 15}" class="val sm">{esc(p["due_kind"])} {end}{(" (folded into the Joint Venture " + p["status"].split()[-1] + ")") if "folded" in p["status"] else (" (cancelled)" if cancelled else "")}</text>')
    out.append("</svg>")
    legend = ('<div class="legend"><span><i class="bar" style="background:var(--pos)"></i>Airframe programme</span>'
              '<span><i class="bar" style="background:var(--s1)"></i>Engine programme</span>'
              '<span><i class="bar" style="background:var(--neg)"></i>Cancelled or folded</span></div>')
    rows = [[esc(p["name"]), str(p["launch"]), f'{p["due_kind"]} {p["due"]}', esc(p["status"])] for p in progs]
    return legend + f'<div class="cw">{"".join(out)}</div>' + K.tview("Programme timeline", ["Programme", "Launched", "Due", "Status"], rows, num_cols=[1])


def small_lines(series, label, aria, y_fmt="int", hi=None):
    """Compact line chart for small multiples: series = [(name, css var, [(year, value)], dashed)]."""
    w, h, left, right, top, bot = 440, 250, 40, 122, 18, 34
    x_lo, x_hi = 2026, 2060
    vals = [v for _, _, d, _ in series for _, v in d]
    hi = hi or max(5, 5 * (int(max(vals) / 5) + 1))
    step = 5 if hi <= 25 else 10 if hi <= 60 else 20
    sx = lambda x: left + (x - x_lo) / (x_hi - x_lo) * (w - left - right)
    sy = lambda v: top + (hi - v) / hi * (h - top - bot)
    out = [f'<svg viewBox="0 0 {w} {h}" class="chart sm" role="img" aria-label="{esc(aria, quote=True)}">']
    t = 0
    while t <= hi + 1e-9:
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(t):.1f}" y2="{sy(t):.1f}" class="grid"/>'
                   f'<text x="{left - 6}" y="{sy(t) + 4:.1f}" text-anchor="end" class="tick">{t:g}</text>')
        t += step
    for yr in (2030, 2040, 2050, 2060):
        out.append(f'<text x="{sx(yr):.1f}" y="{h - bot + 16}" text-anchor="middle" class="tick">{yr}</text>')
    for j, yr in enumerate(RYEARS):
        out.append(f'<line x1="{sx(yr):.1f}" x2="{sx(yr):.1f}" y1="{top}" y2="{h - bot}" class="leader"/>')
    last = [d[-1][1] for _, _, d, _ in series]
    dys = spread(last, 0, hi, gap=14, plot_h=h - top - bot)
    for (name, var, d, dashed), dy in zip(series, dys):
        path = "M" + " L".join(f"{sx(x):.1f},{sy(v):.1f}" for x, v in d)
        dash = ' stroke-dasharray="5 4"' if dashed else ""
        out.append(f'<path d="{path}" fill="none" stroke="var(--{var})" stroke-width="2"{dash} stroke-linejoin="round"/>')
        x, v = d[-1]
        out.append(f'<text x="{w - right + 6}" y="{sy(v) + dy + 4:.1f}" class="endlab">{esc(name)} {K.rnd(v, 1):.1f}</text>')
    out.append(f'<text x="{left}" y="{h - 4}" class="tick">{esc(label)}</text></svg>')
    return f'<div class="cw">{"".join(out)}</div>'


def chart_money(side, key, sq_key, title):
    return small_lines([("Game", "s1", ser(side, key), False), ("Status quo", "sq", ser(side, sq_key), True)],
                       "$B a year, nominal; vertical lines mark the rounds", f"{NAME[side]}: {title}")


def chart_money_old(side, key, sq_key, title):
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
def prev_codes(rounds, r):
    i = rounds.index(r)
    return rounds[i - 1]["timeline"]["codes"] if i > 0 else None


def decisions_table(r):
    rows = []
    for s in SIDES:
        o = r["orders"][s]
        txt = order_text(s, o, prev_codes(ROUNDS, r))
        adj = r["adjustments"].get(s) or []
        cell = "<br>".join(esc(t) for t in txt)
        if adj:
            cell += '<br><span class="muted small">GM adjustment: ' + esc("; ".join(adj)) + "</span>"
        st = r["public_statements"].get(s) or ""
        if st:
            cell += f'<p class="small muted" style="margin:6px 0 0">Public statement: “{esc(st)}”</p>'
        rows.append([esc(NAME[s]), cell])
    return K.table(["Player", "Orders (as adjudicated) and public statement"], rows)


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
    return t1 + '<p class="cap">Nominal $B, summed over each period. Non-recurring spend is booked as the dashboard books it: each airframe programme in full at its entry into service.</p>' + t2


BRIDGE_LABEL = {"nb_profit_vs_sq": "NB operating profit vs status quo", "wb_profit_vs_sq": "WB operating profit vs status quo",
                "programme_investment": "Programme investment", "rate_hike": "737 rate increase", "delay_tactics_spend": "Delay Tactics spend",
                "write_offs": "Write-offs (cancellation or fold-in)", "debt_penalty": "Debt penalty (α)", "two_front_strain": "Two-front strain",
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
    return ('<p class="label">The airframer stage game on the dashboard, each round (engine makers as played; nobody moves later; ΔPV $B Boeing / Airbus)</p>'
            + K.table(["Round", "Pure equilibria", "What was played", "Best reply to the other's actual play"], rows))


def regret_detail():
    R = D["regret"]
    rows = []
    for n in range(1, len(ROUNDS) + 1):
        for s in SIDES:
            x = R[str(n)][s]
            act = order_text(s, ROUNDS[n - 1]["orders"][s], prev_codes(ROUNDS, ROUNDS[n - 1]))
            best = "the actual orders (tie)" if x["regret_ex_post"] < 0.005 else x["best_ex_post"]["plan"]
            ob = x["best_ex_post"].get("objectives_ex_post") or []
            fin = FINAL["objectives"][s]
            k = sum(1 for o in fin if o["met"])
            objs = (f'{k} → {sum(1 for _, m in ob if m)} of {len(fin)}' if ob else
                    f'{k} → {k} of {len(fin)}' if x["regret_ex_post"] < 0.005 else "—")
            rows.append([f"R{n} {esc(NAME[s])}", esc("; ".join(act)), K.num(x["actual_ex_post"]), esc(best),
                         K.num(x["best_ex_post"]["ex_post"]), K.num(x["regret_ex_post"]), K.num(x["regret_myopic"]), objs])
    return K.tview("Regret by round and player", ["Round, player", "Actual orders", "Final ΔPV (actual)", "Best alternative (ex post)",
                                                  "Its final ΔPV", "Regret ex post", "Regret myopic",
                                                  "Objectives met: actual → best alternative"], rows, num_cols=[2, 4, 5, 6])


# Order fields and values in plain words, for display only (the record keeps the agents' text verbatim)
import re as _re
PLAIN_FIELD = {"fps_engine_code": "fps engine code", "ngsa_engine_code": "NGSA engine code", "rate_737": "737 rate",
               "re787": "787 Re-engine", "rea350": "A350 Re-engine", "delay_tactics": "Delay Tactics", "open_fan": "Open Fan",
               "partner_embraer": "Embraer partnership", "lobby_emissions": "emissions lobbying", "gtf2_solo": "GTF2 Solo",
               "jv_with_rr": "Joint Venture with RR", "jv_with_pw": "Joint Venture with P&W", "ultrafan_nb_solo": "UltraFan NB Solo",
               "ultrafan_wb": "UltraFan WB", "t1000_upgrade": "Trent 1000 upgrade", "pv_delta": "ΔPV", "expected_pv_b": "expected ΔPV",
               "premium_b": "premium", "ngsa": "NGSA", "genx": "GEnx", "ducted": "ducted engine", "fps": "fps"}
PLAIN_VALUE = {"launch_7yr": "launch (7-year ramp-up)", "launch_10yr": "launch (10-year ramp-up)", "launch_via_embraer": "launch via Embraer",
               "launch_if_selected": "launch if selected", "upgrade_genx9": "GEnx upgrade", "invest_genx": "GEnx investment"}
_PLAIN = {**PLAIN_FIELD, **PLAIN_VALUE}
_PLAIN_RE = _re.compile(r"(?<![\w/.-])(" + "|".join(sorted((_re.escape(k) for k in _PLAIN), key=len, reverse=True)) + r")(?![\w-])")
_ONLY_AS_FIELD = {"ngsa", "genx", "ducted", "fps"}     # ordinary words too: replaced only when written as a field ("ngsa:")


def plain(t):
    """Agent text with order-field and value names in plain words (display only)."""
    t = str(t if t is not None else "")
    t = _re.sub(r"(engine[ _]code)(:?) None\b", r"\1\2 none", t)

    def rep(m):
        k = m.group(1)
        if k in _ONLY_AS_FIELD and t[m.end():m.end() + 1] != ":":
            return k
        return _PLAIN[k]
    return _PLAIN_RE.sub(rep, t)


def escp(t):
    """Agent text for display: plain order names, HTML-escaped, the agents' markdown bold rendered, code ticks dropped."""
    h = esc(plain(t))
    h = _re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", h)
    return h.replace("`", "")


SEAT = {"ceo": "CEO", "cfo": "CFO", "ops": "operating head"}
PEOPLE = {"boeing": ("Kelly Ortberg", "Jay Malave", "Stephanie Pope", "Boeing Board"),
          "airbus": ("Guillaume Faury", "Thomas Toepfer", "Lars Wagner", "Airbus Board"),
          "cfm": ("Larry Culp", "Rahul Ghai", "Mohamed Ali", "GE Aerospace Board"),
          "pratt_whitney": ("Chris Calio", "Neil Mitchill", "Shane Eddy", "RTX Board"),
          "rolls_royce": ("Tufan Erginbilgic", "Helen McCabe", "Rob Watson", "Rolls-Royce Board")}


def _li(items):
    items = [i for i in (items or []) if i]
    return ("<ul>" + "".join(f"<li>{escp(str(i))}</li>" for i in items) + "</ul>") if items else '<p class="muted">none</p>'


def _orders_line(side, o, prev=None):
    """Orders in words, raw text (escape at render); engine codes restated unchanged from `prev` are left out."""
    return "; ".join(order_text(side, o or {}, prev))


def tests_table(memo):
    rows = [[escp(t.get("name", "")), escp(t.get("threshold", "")), escp(t.get("result", "")), escp(t.get("numbers", ""))]
            for t in (memo or {}).get("tests") or []]
    return K.table(["Test", "Threshold", "Result", "Numbers"], rows) if rows else ""


def vetoes_table(memo):
    rows = [[escp(v.get("plan", "")), escp(v.get("ground", "")), "binding" if v.get("binding") else "not binding"]
            for v in (memo or {}).get("vetoes") or []]
    return ('<p><b>Vetoes on options.</b></p>' + K.table(["Option", "Ground", "Status"], rows)) if rows else ""


def vetocheck_block(vc, names):
    out = []
    for seat, nm in (("cfo", names[1]), ("ops", names[2])):
        v = (vc or {}).get(seat)
        if not v:
            continue
        vt = v.get("veto") or {}
        line = f"<b>{escp(nm)} ({SEAT[seat]}):</b> {'concurs' if v.get('concur') else 'does not concur'}"
        if vt.get("ground"):
            line += f"; veto {'(binding)' if vt.get('binding') else '(not binding)'}: {escp(vt['ground'])}"
        if v.get("red_line_breach"):
            line += f"; red-line flag: {escp(v.get('red_line', ''))}"
        out.append(f"<p>{line}</p><p>{escp(v.get('note', ''))}</p>")
    return ('<p class="label">Veto check on the CEO\'s decision</p>' + "".join(out)) if out else ""


def review_table(rv):
    rows = [[escp(i.get("order_field", "")), escp(str(i.get("value", ""))), escp(i.get("decision", "")), escp(i.get("ground", "")),
             escp("; ".join(i.get("acceptable_alternatives") or []) or "—")] for i in (rv or {}).get("items") or []]
    return K.table(["Board item", "Value", "Decision", "Ground", "Acceptable alternatives"], rows) if rows else ""


def short(t, n=260):
    """Collapse whitespace; cut at a word boundary (the full text is in the step's own panel)."""
    t = " ".join(str(t or "").split())
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + " …"


def chain_summary(side, x, prev=None):
    """One line per step: what each seat did, from the ExCo record. Long free text is shortened; the panel below gives it in full."""
    ex = x.get("exco") or {}
    ceo, cfo, ops, board = PEOPLE[side]
    g = ex.get("board_guidance") or {}
    dec = ex.get("decision") or {}
    vc = ex.get("veto_checks") or {}
    out = []
    if g:
        out.append(("Board guidance", f"{board}: risk appetite: {short(g.get('risk_appetite', ''))}"))
    fr = ex.get("frame") or {}
    if fr:
        out.append(("Frame", f"{ceo}: initial lean: {short(fr.get('initial_lean', ''))}"))
    for seat, nm in (("cfo", cfo), ("ops", ops)):
        m = ex.get(seat) or {}
        if m:
            fails = [t.get("name", "") for t in m.get("tests") or [] if t.get("result") == "fail"]
            vet = [v.get("plan", "") + (" (binding)" if v.get("binding") else " (not binding)") for v in m.get("vetoes") or []]
            out.append((f"Test ({SEAT[seat]})", f"{nm} recommends: {_orders_line(side, m.get('recommended_orders'), prev)}"
                        + (f". Tests failed: {short('; '.join(f.rstrip('.') for f in fails), 300)}" if fails else ". No test failed")
                        + (f". Vetoes on options: {short('; '.join(vet), 300)}" if vet else "")))
    if dec:
        ov = [o.get("veto", "") for o in dec.get("overrides") or []]
        out.append(("Decide", f"{ceo}: {_orders_line(side, dec.get('orders'), prev)}" + (f"; overrides: {short('; '.join(ov), 200)}" if ov else "")))
    for seat, nm in (("cfo", cfo), ("ops", ops)):
        v = vc.get(seat)
        if v:
            t = "concurs" if v.get("concur") else "does not concur"
            vg = (v.get("veto") or {}).get("ground") or ""
            if vg and (v["veto"].get("binding") or not v.get("concur")) and not vg.lstrip().lower().startswith("none"):
                t += f"; veto{' (binding)' if v['veto'].get('binding') else ' (not binding)'}: {short(vg)}"
            if v.get("red_line_breach"):
                t += f"; red line: {short(v.get('red_line', ''))}"
            out.append((f"Veto check ({SEAT[seat]})", f"{nm} {t}"))
    if ex.get("revision"):
        out.append(("Revise", f"{ceo}: {_orders_line(side, ex['revision'].get('orders'), prev)}"))
    rv = ex.get("board_review")
    if rv and not (rv.get("items") or ex.get("board_items")):
        out.append(("Board review", f"{board}: not called; no Board item (every launch, commit or cancel order at its default)"))
    elif rv:
        items = rv.get("items") or []
        ap = [PLAIN_FIELD.get(i["order_field"], i["order_field"]) for i in items if i.get("decision") == "approve"]
        ve = [PLAIN_FIELD.get(i["order_field"], i["order_field"]) for i in items if i.get("decision") == "veto"]
        nrec = len(rv.get("recommendations") or [])
        out.append(("Board review", f"{board}: {rv.get('overall', '')}" + (f"; approved {', '.join(ap)}" if ap else "")
                    + (f"; vetoed {', '.join(ve)}" if ve else "") + ("" if items else " (no Board items)")
                    + (f"; {nrec} recommendation{'s' if nrec != 1 else ''}" if nrec else "")))
    elif ex.get("board_items") == [] or (ex.get("board_items") is None and not rv):
        out.append(("Board review", f"{board}: no Board item (every order is the default)"))
    if ex.get("board_revision"):
        out.append(("Board revise", f"{ceo}: {_orders_line(side, ex['board_revision'].get('orders'), prev)}"))
    if ex.get("board_confirm"):
        cf = ex["board_confirm"]
        out.append(("Board confirm", f"{board}: {cf.get('overall', '')}"))
    if ex.get("board_reverted"):
        out.append(("Reverted to the default", ", ".join(PLAIN_FIELD.get(f, f) for f in ex["board_reverted"])))
    return out


NOT_CALLED = ('<p class="muted">Not called: no Board item (every launch, commit or cancel order at its default). '
              "The Board's guidance above stands as its view for the round.</p>")


def chain_block(r):
    out = []
    for s in SIDES:
        x = r["returned"].get(s) or {}
        ex = x.get("exco") or {}
        ceo, cfo, ops, board = PEOPLE[s]
        g = ex.get("board_guidance") or {}
        fr = ex.get("frame") or {}
        dec = ex.get("decision") or {}
        rv = ex.get("board_review") or {}
        pc = prev_codes(ROUNDS, r)
        steps = K.table(["Step", "What happened"], [[escp(a), escp(b_)] for a, b_ in chain_summary(s, x, pc)])
        om = x.get("other_moves") or []
        oms = "".join(f'<li>{escp(m.get("move", ""))}{" (public)" if m.get("public") else " (private)"}{(": " + escp(m.get("detail", ""))) if m.get("detail") else ""}</li>' for m in om)
        mw = x.get("memo_weighing") or {}
        ovr = "".join(f"<li>{escp(o.get('veto', ''))}: {escp(o.get('reason', ''))}</li>" for o in x.get("overrides") or [])
        br = "".join(f"<li><b>{escp(o.get('recommendation', ''))}</b> {escp(o.get('response', ''))}</li>" for o in x.get("board_response") or [])
        out.append(f'''<details class="tv"><summary>{escp(NAME[s])}: the decision chain ({escp(ceo)}, {escp(cfo)}, {escp(ops)}; {escp(board)})</summary><div class="panel stack small chain">
{steps}
<p class="label">Board guidance before the ExCo met</p><p><b>Priorities.</b></p>{_li(g.get("priorities"))}<p><b>Expects to see.</b> {escp(g.get("expect_to_see", ""))}</p>
<p><b>Would approve.</b></p>{_li(g.get("would_approve"))}<p><b>Would veto.</b></p>{_li(g.get("would_veto"))}
<p><b>Recommendations.</b></p>{_li([i.get("text") for i in g.get("recommendations") or []])}
<p class="label">{escp(ceo)} frames the round</p><p><b>Question.</b> {escp(fr.get("question", ""))}</p><p><b>Situation.</b> {escp(fr.get("situation", ""))}</p>
<p><b>Options to test.</b></p>{_li(fr.get("options_to_test"))}<p><b>Red lines.</b></p>{_li(fr.get("red_lines"))}
<p><b>Initial lean.</b> {escp(fr.get("initial_lean", ""))}</p>
<p class="label">{escp(cfo)} (CFO) tests</p>{tests_table(ex.get("cfo"))}{vetoes_table(ex.get("cfo"))}<p>{escp((ex.get("cfo") or {}).get("memo", ""))}</p>
<p class="label">{escp(ops)} (operating head) tests</p>{tests_table(ex.get("ops"))}{vetoes_table(ex.get("ops"))}<p>{escp((ex.get("ops") or {}).get("memo", ""))}</p>
<p class="label">{escp(ceo)} decides</p><p><b>Orders.</b> {esc(_orders_line(s, dec.get("orders"), pc))}</p><p><b>Rationale.</b> {escp(dec.get("rationale", ""))}</p>
<p><b>Weighing the CFO.</b> {escp(((dec.get("memo_weighing") or {}).get("cfo", "")))}</p><p><b>Weighing the operating head.</b> {escp(((dec.get("memo_weighing") or {}).get("ops", "")))}</p>
{("<p><b>Overrides.</b></p><ul>" + ovr + "</ul>") if ovr else ""}
{vetocheck_block(ex.get("veto_checks"), PEOPLE[s])}
<p class="label">Board review</p>{review_table(rv) or NOT_CALLED}{('<p>' + escp(rv.get("note", "")) + '</p>') if rv.get("items") else ""}
{("<p><b>The Board's recommendations at review.</b></p>" + _li([i.get("text") for i in rv.get("recommendations") or []])) if rv.get("recommendations") else ""}
{(review_table(ex.get("board_confirm")) and '<p class="label">Board confirmation</p>' + review_table(ex.get("board_confirm"))) or ""}
<p class="label">Final</p><p><b>Orders (as adjudicated).</b> {esc(_orders_line(s, r["orders"][s], pc))}</p>
<p><b>Expected scenario.</b> {escp(str(x.get("expected_scenario", "")))}</p>
<p><b>Best grid plan in that scenario.</b> {escp(str(x.get("best_grid_plan_in_expected_scenario", "")).rstrip(". "))}. <b>Premium paid:</b> {escp(K.num(x.get("premium_b", 0) or 0))} $B. {escp(str(x.get("premium_reason", "")))}</p>
{("<p><b>Answers to the Board.</b></p><ul>" + br + "</ul>") if br else ""}
<p><b>Objective.</b> {escp(str(x.get("objective_note", "")))}</p>
<p><b>Predictions.</b> {escp(str(x.get("predictions", "")))}</p>
<p><b>Expected ΔPV.</b> {escp(K.num(x.get("expected_pv_b", 0) or 0))} $B (GM valuation after the round: {escp(K.num(r["value"][s]["pv_delta"]))} $B)</p>
{("<p><b>Other moves.</b></p><ul>" + oms + "</ul>") if oms else ""}
</div></details>''')
    return "".join(out)


def governance_table():
    """Per round and company: binding vetoes and red-line flags inside the ExCo, revisions, Board vetoes, reversions."""
    rows = []
    for r in ROUNDS:
        for s in SIDES:
            ex = ((r["returned"].get(s) or {}).get("exco")) or {}
            items = ex.get("board_items") or []
            rows.append([f"R{r['round']} {escp(NAME[s])}",
                         escp(", ".join(SEAT.get(v, v) for v in ex.get("binding_vetoes") or []) or "—"),
                         escp(", ".join(SEAT.get(v, v) for v in ex.get("red_line_flags") or []) or "—"),
                         "yes" if ex.get("revision") else "—",
                         escp(", ".join(PLAIN_FIELD.get(f, f) for f in items) or "—"),
                         escp(", ".join(PLAIN_FIELD.get(f, f) for f in ex.get("board_vetoed") or []) or "—"),
                         escp(", ".join(PLAIN_FIELD.get(f, f) for f in ex.get("board_reverted") or []) or "—")])
    return K.table(["Round, company", "Binding vetoes at the veto check", "Red-line flags", "ExCo revised", "Board items", "Board vetoed",
                    "Reverted to the default"], rows)


def unchanged_since(r):
    """The earliest earlier round whose valuation and year-by-year projection equal this round's, if any."""
    i = ROUNDS.index(r)
    j = i
    while j > 0 and ROUNDS[j - 1]["years"] == r["years"] and all(
            ROUNDS[j - 1]["value"][s]["pv_delta"] == r["value"][s]["pv_delta"] for s in SIDES):
        j -= 1
    return ROUNDS[j] if j < i else None


def round_section(r):
    n = r["round"]
    same = unchanged_since(r)
    tl = r["timeline"]
    fit = tl["engine_fit"]
    pw = lambda t: _re.sub(r"\bPW\b", "P&W", str(t))
    fit_rows = [[("fps" if k == "fps" else "NGSA"), escp(pw(f["requested"])), escp(pw(f["fitted_if_no_change"])), escp(pw(f["note"] or "—"))] for k, f in fit.items()]
    covert = [f"{k} ordered {y}" for k, y in tl["delay_tactics"].items() if y]
    nar = NAR.ROUNDS.get(n, {})
    if same:
        body = (f'<div class="panel"><p class="muted">Market shares, financials and the ΔPV build are unchanged since round '
                f'{same["round"]} ({same["year"]}): see that round and the Financials section.</p></div>')
    else:
        body = (f'<div class="panel"><p class="label">Market shares projected after the round</p>{shares_table(r)}</div>'
                f'<div class="panel"><p class="label">Financials projected after the round</p>{periods_table(r)}'
                "<p class=\"label\" style=\"margin-top:14px\">How each player's ΔPV is built</p>" + bridge_table(r)
                + "".join(year_table(r, s) for s in SIDES) + '</div>')
    return f'''<section id="r{n}"><p class="eyebrow">Round {n} · decision year {r["year"]}</p><h2>{escp(nar.get("title", f"Round {n}"))}</h2>
<p class="lede">{nar.get("lede", "")}</p>
<div class="stack">
<div class="panel"><p class="label">What each player ordered</p>{decisions_table(r)}
{('<p class="cap"><b>Covert (revealed after the game):</b> Airbus Delay Tactics ' + escp(", ".join(covert)) + ".</p>") if covert else ""}</div>
<div class="grid2"><div class="panel"><p class="label">Value after the round (GM valuation; nobody moves later)</p>{value_table(r)}</div>
<div class="panel"><p class="label">Engines on the new narrowbodies</p>{K.table(["Airframe", "Requested", "Fitted", "Note"], fit_rows) if fit_rows else '<p class="muted">No new narrowbody launched yet.</p>'}</div></div>
{body}
<div class="panel"><p class="label">How each company decided: Board guidance, ExCo, Board review (private during the game)</p>
<p class="cap">In the agents' own words. S1, S2, … are the scenario columns of that company's own payoff grid in its brief (they differ by
company); ids in brackets are the agents' evidence citations; order names are shown in plain words.</p>{chain_block(r)}</div>
</div></section>'''


def memo_binding_count():
    """Binding vetoes marked in the CFOs' and operating heads' test memos, over the whole game."""
    return sum(1 for r in ROUNDS for s in SIDES for seat in ("cfo", "ops")
               for v in ((((r["returned"].get(s) or {}).get("exco") or {}).get(seat) or {}).get("vetoes") or []) if v.get("binding"))


def governance_section():
    return (f'<section id="exco"><h2>How the companies decided</h2><p class="lede">{NAR.GOV_LEDE}</p><div class="stack">'
            f'<div class="panel"><p class="label">ExCo vetoes, revisions and Board votes, by round and company</p>{governance_table()}'
            '<p class="cap">A Board item is any order that differs from its default (hold, or none for Delay Tactics); an engine code rides '
            'with its launch and is never a Board item on its own. A binding veto or a red-line flag at the veto check (the CFO\'s and '
            'operating head\'s check of the CEO\'s actual decision) sends it back to the CEO for one revision; a Board veto sends it back '
            'once more, and a still-vetoed item reverts to the default. The binding vetoes in the CFOs\' and operating heads\' test memos '
            f'({memo_binding_count()} in all) fell on options the CEO did not choose or, where conditional, were answered by the CEO\'s wording; none was invoked against a chosen order, so none appears here.</p></div>'
            f'<div class="bl">{"".join(f"<div class=panel><div><b>{esc(t)}</b>{x}</div></div>" for t, x in NAR.GOV_POINTS)}</div>'
            '</div></section>')


def equilibria_panel():
    bd = D.get("board") or {}
    if not bd:
        return ""
    rows = [[f"Pure Nash {i + 1}", esc(e["airbus"]), esc(e["boeing"]), f'{K.rnd(e["yield_airbus"], 1):.1f}% / {K.rnd(e["yield_boeing"], 1):.1f}%']
            for i, e in enumerate(bd.get("airframer_pure") or [])]
    t1 = K.table(["Snapshot (default dates)", "Airbus", "Boeing", "Yield Airbus / Boeing"], rows)
    rows = [[f"Pure Nash {i + 1}", esc(e["cfm"]), esc(e["pw"]), esc(e["rr"]), f'{e["yield_cfm"]}% / {e["yield_rr"]}%']
            for i, e in enumerate(bd.get("engine_pure") or [])]
    t2 = K.table(["Snapshot engine game, engine selection (7, 6)", "CFM/GE", "P&amp;W", "Rolls-Royce", "Yield CFM / RR"], rows)
    inp = FINAL["board_inputs"]
    eis = inp["eis"]
    played = (f'<p class="cap">Where the game ended, as a board cell: Airbus {esc(lab_af(inp["a"]))}; Boeing {esc(lab_af(inp["b"]))}; '
              f'at fps {eis[0]}, NGSA {eis[1]}, 787 Re-engine {eis[2]}, A350 Re-engine {eis[3]} (unlaunched Re-engines at the snapshot date); '
              f'engine selection ({FINAL["timeline"]["codes"].get("fps")}, {FINAL["timeline"]["codes"].get("ngsa")}) with the P&amp;W-Rolls-Royce Joint Venture. '
              'The engine moves listed are narrowbody; in the snapshot\'s engine Pure Nash both widebody engines Do Nothing (GEnx and Trent).</p>')
    return ('<p class="label">Your snapshot\'s equilibria (default dates: fps 2041, NGSA 2037, Re-engines 2042), solved on the board</p>'
            + t1 + f'<p class="cap">{bd.get("airframer_near_count", 0)} Near-Nash cells besides (ε 1%). Engine game: '
            f'{len(bd.get("engine_pure") or [])} Pure Nash and {bd.get("engine_near_count", 0)} Near-Nash (ε 5%).</p>' + t2 + played)


AF_LAB = {"Launch_NGSA": "Launch NGSA", "Milk_A320neo": "Do Nothing (A320neo)", "Sabotage_Bottleneck": "Delay fps Bottleneck",
          "Sabotage_Poaching": "Delay fps Poaching", "Re_engine_A350": "Re-engine A350", "Milk_A350": "Do Nothing A350",
          "Launch_fps_7yr_Solo": "fps 7yr Solo", "Launch_fps_10yr_Solo": "fps 10yr Solo", "Launch_fps_via_Embraer": "fps via Embraer",
          "Milk_737MAX": "Do Nothing (737 MAX)", "Increase_737_Rate": "737 Rate Increase", "Re_engine_787": "Re-engine 787",
          "Milk_787": "Do Nothing 787"}


def lab_af(strat):
    return " + ".join(AF_LAB[m] for m in strat if m in AF_LAB)



# ─────────────────────────────── Control's objectives ───────────────────────────────
C2 = FINAL.get("control2") or {}


def chart_debt():
    """Boeing's net debt as played (final state): base case, stress case, and no new programme. All three end at the
    historical level, so they share one end label; the axis starts below zero to keep it off the year ticks."""
    rows = C2["debt_base"]
    st = C2["debt_stress"]
    series = [("Net debt, base case", "s1", [(r["year"], r["debt"]) for r in rows]),
              ("Net debt, stress case", "s2", [(r["year"], r["debt"]) for r in st]),
              ("No new programme", "sq", [(r["year"], r["debt_no_programme"]) for r in rows])]
    ends = [(-10, "All three: $0"), (0, ""), (0, "")]
    svg = K.line_chart(series, -5, 25, 5, "int", "Boeing net debt, $B at year end, 2026 dollars (below zero would be net cash)",
                       refs=[(0, "historical level (about zero)", "below")],
                       aria_label="Boeing net debt by year: base case, stress case and no new programme", end_labels=ends,
                       notes=[(y, f"R{j + 1}") for j, y in enumerate(RYEARS)], x_lo=2026, x_hi=2060)
    legend = ('<div class="legend"><span><i class="ln" style="background:var(--s1)"></i>Base case</span>'
              '<span><i class="ln" style="background:var(--s2)"></i>Stress case (free cash flow one-third lower)</span>'
              '<span><i class="ln" style="background:var(--sq)"></i>No new programme</span></div>')
    trows = [[str(r["year"]), K.num(r["base_fcf"], ".1f"), K.num(r["profit_vs_baseline"]), (f'{r["spend"]:.1f}' if r["spend"] else "—"),
              K.num(r["fcf"]), f'{r["debt"]:.1f}', f'{r["debt_no_programme"]:.1f}', f'{s_["debt"]:.1f}']
             for r, s_ in zip(rows, st) if r["year"] <= 2042 or r["year"] % 5 == 0]
    return (legend + f'<div class="cw">{svg}</div>'
            + K.tview("Boeing net-debt path (final state)", ["Year", "Base free cash flow", "Profit vs game baseline", "Programme cash",
                                                         "Free cash flow", "Net debt", "No new programme", "Net debt, stress case"],
                      trows, num_cols=list(range(1, 8))))


def chart_cash():
    """Boeing's programme cash against the stress-case free cash flow it must fit inside."""
    rows = C2["debt_base"]
    sc = C2["debt_inputs"]["stress_fcf_scale"]
    series = [("Stress FCF", "s2", [(r["year"], r["base_fcf"] * sc) for r in rows], False),
              ("fps cash", "s1", [(r["year"], r["spend"]) for r in rows], False)]
    return small_lines(series, "$B a year, 2026 dollars", "Boeing programme cash against stress-case free cash flow", y_fmt="int", hi=15)


def objectives_scorecard(rounds, side_list=None):
    sides = side_list or SIDES
    rows = []
    for s in sides:
        labels = [o["label"] for o in rounds[-1]["objectives"][s]]
        for i, lab in enumerate(labels):
            cells = []
            for r in rounds:
                o = r["objectives"][s][i]
                cells.append("met" if o["met"] else "<b>not met</b>")
            rows.append([esc(NAME[s]), esc(lab)] + cells + [esc(rounds[-1]["objectives"][s][i]["detail"])])
    return K.table(["Company", "Objective (Control's additions start at 'Repair', 'Enabler' and 'Protect')"]
                   + [f"After {r['year']}" for r in rounds] + ["Detail, final state"], rows)


def sources_table():
    rows = []
    for r in ROUNDS:
        c = r["control2"]
        fps, ngsa = c["sources"]["boeing"], c["sources"]["airbus"]
        rows.append([f"After round {r['round']} ({r['year']})",
                     f'{esc(" + ".join(fps["2040"][1]))} ({len(fps["2040"][1])})', f'{esc(" + ".join(fps["2050"][1]))} ({len(fps["2050"][1])})',
                     f'{esc(" + ".join(ngsa["2040"][1]))} ({len(ngsa["2040"][1])})', f'{esc(" + ".join(ngsa["2050"][1]))} ({len(ngsa["2050"][1])})',
                     str(len(c["makers"]["2050"])), b(c["rr_nb_exposure"], sign=False), b(c["rr_strain"], sign=False)])
    p = PREV["rounds"][-1]
    pf, pn = p["sources"]["boeing"], p["sources"]["airbus"]
    rows.append(["<i>Previous game, final</i>", f'{esc(" + ".join(pf["2040"][1]))} ({len(pf["2040"][1])})',
                 f'{esc(" + ".join(pf["2050"][1]))} ({len(pf["2050"][1])})', f'{esc(" + ".join(pn["2040"][1]))} ({len(pn["2040"][1])})',
                 f'{esc(" + ".join(pn["2050"][1]))} ({len(pn["2050"][1])})', str(len(p["makers"]["2050"])), b(p["rr_nb_exposure"], sign=False),
                 b(p["rr_strain"], sign=False)])
    return K.table(["State", "fps engines 2040", "fps engines 2050", "NGSA engines 2040", "NGSA engines 2050", "NB engine makers 2050",
                    "RR own NB development money", "RR NB+WB strain"], rows, num_cols=(5, 6, 7))


def objectives_section():
    if not C2:
        return ""
    return (f'<section id="objectives"><h2>Control\'s objectives</h2><p class="lede">{NAR.OBJ_LEDE}</p><div class="stack">'
            f'<div class="panel"><p class="label">Every objective, after each round (the state as of that round, nobody moving later)</p>'
            f'{objectives_scorecard(ROUNDS)}</div>'
            f'<div class="panel"><p class="ctitle">{esc(NAR.DEBT_TITLE)}</p>{chart_debt()}<p class="cap">{NAR.DEBT_CAP}</p></div>'
            f'<div class="grid2"><div class="panel"><p class="ctitle">{esc(NAR.CASH_TITLE)}</p>{chart_cash()}</div>'
            f'<div class="panel"><p class="label">Why the stress case holds</p>{NAR.CASH_NOTE}</div></div>'
            f'<div class="panel"><p class="label">Engine sources on the new narrowbodies and Rolls-Royce\'s narrowbody exposure</p>{sources_table()}'
            f'<p class="cap">{NAR.SOURCES_CAP}</p></div>'
            f'<div class="bl">{"".join(f"<div class=panel><div><b>{esc(t)}</b>{x}</div></div>" for t, x in NAR.OBJ_POINTS)}</div>'
            '</div></section>')


def analysts_section():
    rows = [[esc(c), esc(f), esc(src)] for c, f, src in NAR.ANALYST_TABLE]
    return (f'<section id="analysts"><h2>The analyst models: prediction against the game</h2><p class="lede">{NAR.ANALYST_LEDE}</p>'
            f'<div class="stack"><div class="panel"><p class="label">What the July-August 2026 analyst models say</p>'
            + K.table(["Company", "Fact", "Source"], rows) + f'<p class="cap">{NAR.ANALYST_CAP}</p></div>'
            f'<div class="bl">{"".join(f"<div class=panel><div><b>{esc(t)}</b>{x}</div></div>" for t, x in NAR.ANALYST_POINTS)}</div>'
            '</div></section>')

def compare_section():
    """The previous ExCo game (run dash-2050-exco: same board, same agents, base objectives) against this one."""
    rows = []
    for i, (r_old, r_new) in enumerate(zip(OLD["rounds"], ROUNDS)):
        for sd in SIDES:
            rows.append([f"R{i + 1} {esc(NAME[sd])}", "<br>".join(esc(t) for t in order_text(sd, r_old["orders"][sd], prev_codes(OLD["rounds"], r_old))),
                         "<br>".join(esc(t) for t in order_text(sd, r_new["orders"][sd], prev_codes(ROUNDS, r_new)))])
    t1 = K.table(["Round, company", "Previous game: base objectives", "This game: Control's added objectives and the analyst baselines"], rows)
    of, nf = OLD["rounds"][-1], FINAL
    rows = [[esc(NAME[sd]), K.num(of["value"][sd]["pv_delta"]), K.num(nf["value"][sd]["pv_delta"]),
             K.num(nf["value"][sd]["pv_delta"] - of["value"][sd]["pv_delta"])] for sd in SIDES]
    t2 = K.table(["Company", "Final ΔPV, previous game", "Final ΔPV, this game", "Change"], rows, num_cols=(1, 2, 3))
    rows = []
    for lab, side, key in (("Boeing narrowbody", "boeing", "nb_share"), ("Airbus narrowbody", "airbus", "nb_share"),
                           ("CFM/GE narrowbody engines", "cfm", "nb_share"), ("P&amp;W narrowbody engines", "pratt_whitney", "nb_share"),
                           ("Rolls-Royce narrowbody engines", "rolls_royce", "nb_share"), ("CFM/GE widebody engines", "cfm", "wb_share"),
                           ("Rolls-Royce widebody engines", "rolls_royce", "wb_share")):
        rows.append([lab] + [f'{pct(g["snapshots"][str(y)][side][key])}' for y in (2040, 2045, 2050) for g in (of, nf)])
    t3 = K.table(["Share", "2040 previous", "2040 this", "2045 previous", "2045 this", "2050 previous", "2050 this"], rows, num_cols=tuple(range(1, 7)))
    pr = PREV["rounds"][-1]["objectives"]
    rows = []
    for sd in ("boeing", "airbus", "rolls_royce"):
        new = [o for o in nf["objectives"][sd] if o["label"] in [p["label"] for p in pr[sd]]]
        for p, n in zip(pr[sd], new):
            rows.append([esc(NAME[sd]), esc(p["label"]), "met" if p["met"] else "<b>not met</b>", "met" if n["met"] else "<b>not met</b>"])
    t4 = K.table(["Company", "Control's objective (the previous game is scored after the fact)", "Previous game", "This game"], rows)
    return (f'<section id="compare"><h2>Against the previous game</h2><p class="lede">{NAR.COMPARE_LEDE}</p><div class="stack">'
            f'<div class="panel"><p class="label">Orders, round by round</p>{t1}</div>'
            f'<div class="grid2"><div class="panel"><p class="label">Final ΔPV, $B (same dashboard)</p>{t2}</div>'
            f'<div class="panel"><p class="label">Control\'s objectives on both games (final state)</p>{t4}</div></div>'
            f'<div class="panel"><p class="label">Market outcome of both games (final state)</p>{t3}'
            '<p class="cap">The previous game is run dash-2050-exco, reported in wargame/reports/dash-2050-exco/dash_2050_exco_wargame.html.</p></div>'
            f'<div class="bl">{"".join(f"<div class=panel><div><b>{esc(t)}</b>{x}</div></div>" for t, x in NAR.COMPARE_POINTS)}</div>'
            '</div></section>')


def board_table():
    bc = D.get("board_check")
    if not bc:
        return ""
    why = NAR.BOARD_WHY
    rows = [[esc(NAME[s]), K.num(bc[s]["board"]), K.num(bc[s]["gm"]), K.num(bc[s]["gm"] - bc[s]["board"]), esc(why[s])] for s in SIDES]
    return ('<h3>Your dashboard alone against the GM valuation, final state</h3>'
            + K.table(["Player", "Dashboard alone, ΔPV $B", "GM valuation, ΔPV $B", "GM minus dashboard", "Why"], rows, num_cols=(1, 2, 3))
            + f'<p class="cap">The dashboard alone means evaluate_scenario() at the game\'s dates (fps {bc["_engine_inputs"]["eis"][0]}, NGSA {bc["_engine_inputs"]["eis"][1]}; '
              f'the unlaunched Re-engines at the dashboard default {bc["_engine_inputs"]["eis"][2]}) for the airframers, and simulate() with the final engine '
              f'selections (codes {bc["_engine_inputs"]["codes"][0]} and {bc["_engine_inputs"]["codes"][1]}) and moves at the dashboard\'s fixed 50/50 split for the '
              'engine makers. With every programme ready at the dashboard\'s entry-into-service dates and a fixed 50/50 split, the GM engine model '
              'gives the dashboard\'s numbers exactly. The Joint Venture step here is measured from the dashboard-alone baseline (P&amp;W locked to '
              'GTF2 Solo), so it differs from the Joint Venture\'s value quoted elsewhere (+$5.51B for P&amp;W, +$2.29B for Rolls-Royce, on the '
              'game\'s year-by-year split). Parts are rounded and may not add exactly to the totals.</p>')


def audit_table():
    A = D.get("audit") or {}
    if not A:
        return ""
    rows = []
    for s in SIDES:
        cells = []
        for n in range(1, len(ROUNDS) + 1):
            a = (A.get(str(n)) or {}).get(s)
            cells.append("—" if not a else (f'clean ({a["tool_calls"]} calls, {len(a["paths"])} paths)' if a["clean"] else
                                            f'check: {len(a["foreign_paths"])} foreign paths, {len(a["denied"])} denials'))
        rows.append([esc(NAME[s])] + cells)
    return ('<p class="label">Isolation audit: every path each player agent touched and every tool output it received</p>'
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


def check_narrative():
    """The narrative's headline numbers must match the data (to their printed precision)."""
    bad = []
    for desc, ri, side, field, val in NAR.CHECKS:
        got = ROUNDS[ri]["value"][side][field]
        if abs(K.rnd(got, 2) - val) > 1e-9:
            bad.append((desc, side, val, got))
    for side, key, yr, val in NAR.SHARE_CHECKS:
        got = FINAL["years"][side][key][yr - 2026]
        dp = len(str(val).split(".")[1]) if "." in str(val) else 0
        if abs(K.rnd(got, dp) - val) > 1e-9:
            bad.append(("share", side, key, yr, val, got))
    assert not bad, bad


def build(out_path):
    check_narrative()
    css = K.CSS.replace("--pos: #3b4a5e; --neg: #8792a3;",
                        "--pos: #3b4a5e; --neg: #8792a3; --sq: #8a95a5; --seq1: #9ec5f4; --seq2: #5598e7; --seq3: #256abf; --seq4: #0d366b;")
    css = css.replace("--pos: #c9d3e0; --neg: #5d6a7c; color-scheme: dark; }",
                      "--pos: #c9d3e0; --neg: #5d6a7c; --sq: #6f7b8d; --seq1: #184f95; --seq2: #256abf; --seq3: #5598e7; --seq4: #b7d3f6; color-scheme: dark; }")
    css += """
.grid3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
.grid3 > * { min-width: 0; }
.chart.sm .tick { font-size: 12px; } .chart.sm .endlab { font-size: 12px; }
.bl li b { display: inline; font: 600 1em var(--font-body); letter-spacing: 0; margin: 0; }
.bl ul { margin: 6px 0 0; padding-left: 18px; } .bl li { margin-bottom: 4px; }
.chain p { white-space: pre-line; } .chain .label { margin-top: 16px; } .chain ul { margin: 4px 0 8px; padding-left: 18px; }
@media (max-width: 900px) { .grid3 { grid-template-columns: 1fr; } }
@media (max-width: 760px) { .chart.sm { min-width: 0; } }
"""
    rounds_html = "".join(round_section(r) for r in ROUNDS)
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>dash-2050 Objectives Replay</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{css}</style></head><body><div class="wrap">
<header class="top"><p class="eyebrow">Boeing Product Development · war game on the game-theory dashboard · ExCo and Board agents · Control's added objectives · BOEING PROPRIETARY</p>
<h1>{esc(NAR.TITLE)}</h1><p class="lede">{NAR.LEDE}</p>
<nav class="toc"><a href="#summary">Summary</a><a href="#objectives">Control's objectives</a><a href="#shares">Market shares</a><a href="#money">Financials</a><a href="#timeline">Dates</a>
<a href="#exco">How they decided</a>{"".join(f'<a href="#r{r["round"]}">Round {r["round"]} ({r["year"]})</a>' for r in ROUNDS)}<a href="#play">How well each played</a><a href="#compare">Against the previous game</a><a href="#analysts">Analyst models</a><a href="#method">Method</a></nav></header>

<section id="summary"><h2>Summary</h2>{tiles()}
<div class="bl">{"".join(f'<div class="panel"><div><b>{esc(t)}</b>{x}</div></div>' for t, x in NAR.FINDINGS)}</div>
<div class="panel" style="margin-top:14px"><p class="ctitle">{esc(NAR.DPV_TITLE)}</p>{chart_dpv_rounds()}</div>
</section>

{objectives_section()}

<section id="shares"><h2>Market shares</h2><p class="lede">{NAR.SHARES_LEDE}</p><div class="stack">
<div class="panel"><p class="ctitle">{esc(NAR.NB_TITLE)}</p>{share_chart(AF, "nb_share", "Share of narrowbody deliveries", "Narrowbody shares by year", [(.5, "50/50", "above")])}</div>
<div class="panel"><p class="ctitle">{esc(NAR.BOEING_PATH_TITLE)}</p>{chart_boeing_paths()}</div>
<div class="panel"><p class="ctitle">{esc(NAR.WB_TITLE)}</p>{share_chart(AF, "wb_share", "Share of widebody deliveries", "Widebody shares by year", [])}</div>
<div class="panel"><p class="ctitle">{esc(NAR.ENG_NB_TITLE)}</p>{share_chart(EN, "nb_share", "Share of narrowbody engines", "Narrowbody engine shares by year", [(.5, "50%", "above")])}</div>
<div class="panel"><p class="ctitle">{esc(NAR.ENG_WB_TITLE)}</p>{share_chart(EN, "wb_share", "Share of widebody engines", "Widebody engine shares by year", [(.5, "50%", "above")])}</div>
</div></section>

<section id="money"><h2>Financials</h2><p class="lede">{NAR.MONEY_LEDE}</p><div class="stack">
<div class="panel"><p class="label">How each player's final ΔPV is built</p>{bridge_table(FINAL)}</div>
<div class="grid2"><div class="panel"><p class="ctitle">{esc(NAR.MONEY_TITLES["boeing"])}</p>{chart_money("boeing", "profit", "sq_profit", "operating profit")}</div>
<div class="panel"><p class="ctitle">{esc(NAR.MONEY_TITLES["airbus"])}</p>{chart_money("airbus", "profit", "sq_profit", "operating profit")}</div></div>
<div class="grid3"><div class="panel"><p class="ctitle">{esc(NAR.MONEY_TITLES["cfm"])}</p>{chart_money("cfm", "value", "sq_value", "engine lifecycle value")}</div>
<div class="panel"><p class="ctitle">{esc(NAR.MONEY_TITLES["pratt_whitney"])}</p>{chart_money("pratt_whitney", "value", "sq_value", "engine lifecycle value")}</div>
<div class="panel"><p class="ctitle">{esc(NAR.MONEY_TITLES["rolls_royce"])}</p>{chart_money("rolls_royce", "value", "sq_value", "engine lifecycle value")}</div></div>
<div class="legend"><span><i class="ln" style="background:var(--s1)"></i>This game</span><span><i class="ln" style="background:var(--sq)"></i>Status quo (dashed)</span></div>
<div class="panel"><p class="label">Totals by period (final state)</p>{periods_table(FINAL)}</div>
{"".join(year_table(FINAL, s) for s in SIDES)}
</div></section>

<section id="timeline"><h2>Programme dates</h2><p class="lede">{NAR.TIMELINE_LEDE}</p><div class="panel">{chart_gantt()}</div></section>

{governance_section()}

{rounds_html}

<section id="play"><h2>How well each player played</h2><p class="lede">{NAR.PLAY_LEDE}</p><div class="stack">
<div class="panel">{equilibria_panel()}</div>
<div class="panel">{stage_table()}</div>
<div class="panel"><p class="label">Regret by round, $B (final ΔPV of the best alternative minus the actual, holding everyone else's actual orders)</p>{regret_table()}{regret_detail()}</div>
<div class="bl">{"".join(f'<div class="panel"><div><b>{esc(t)}</b>{x}</div></div>' for t, x in NAR.PLAY_POINTS)}</div>
</div></section>

{compare_section()}

{analysts_section()}

<section id="method"><h2>Method</h2><div class="panel stack">{NAR.METHOD}{board_table()}{audit_table()}</div></section>
<footer>{NAR.FOOTER}</footer></div>
<script>{K.JS}</script></body></html>'''
    with open(out_path, "w") as f:
        f.write(page)
    print("wrote", out_path, len(page))


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "dash_2050_obj_wargame.html"))
