"""Build boeing_supply_curves.html: Boeing's single-aisle supply curves assumed in the supply-and-demand game
(supply_demand.boeing_capacity), for an fps launched in 2030 on the 7-year and the 10-year option, against the
737 MAX with no fps. Aircraft a month; the 737 rate increase is not ordered.

Usage: python3 make_supply_curves.py [out.html]"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "dashgame"))
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050-obj"))
sys.path.insert(0, HERE)
import page_kit as K  # noqa: E402
import supply_demand as SD  # noqa: E402
from make_sd_html import lines, legend, n0  # noqa: E402

esc = K.esc
LAUNCH = 2030
YEARS = list(range(2026, 2061))
VARIANTS = [("7-year", 7), ("10-year", 10)]


def state(eis, site="new_site"):
    return {"prog": {"fps": {"launch": LAUNCH, "eis": eis}} if eis else {}, "rate737": None, "sd": {"fps_site": site}}


def month(x):
    return x / 12.0


def curves(dev):
    eis = LAUNCH + dev
    out = {"eis": eis, "fps": [], "max": [], "max_renton": [], "max_no_fps": []}
    for y in YEARS:
        m, f = SD.boeing_capacity(state(eis), y)
        mr, _ = SD.boeing_capacity(state(eis, "renton"), y)
        m0, _ = SD.boeing_capacity(state(None), y)
        out["fps"].append(month(f))
        out["max"].append(month(m))
        out["max_renton"].append(month(mr))
        out["max_no_fps"].append(month(m0))
    return out


def first(series, test):
    return next(y for y, v in zip(YEARS, series) if test(v))


def panel(name, dev):
    c = curves(dev)
    b = SD.inputs()["boeing"]
    cap_tail = b["total_rate_cap"] - b["max_tail_rate"]
    series = [("MAX, no fps", "sq", list(zip(YEARS, c["max_no_fps"])), True),
              ("MAX, Renton", "s1", list(zip(YEARS, c["max_renton"])), True),
              ("MAX", "s1", list(zip(YEARS, c["max"])), False),
              ("fps", "s3", list(zip(YEARS, c["fps"])), False)]
    notes = [(LAUNCH, "launch"), (c["eis"], "in service"), (b["max_last_year"], "MAX ends")]
    svg = lines(series, 110, 20, "int", "Aircraft a month", f"Boeing single-aisle supply with the fps {name} option",
                notes=notes, end_fmt=lambda v: f"{v:.0f}")
    full = first(c["fps"], lambda v: v >= cap_tail - 1e-9)
    title = (f"fps {name}: launched {LAUNCH}, in service {c['eis']}, {cap_tail:.0f} a month by {full} "
             f"and 100 a month from {b['max_last_year'] + 1}")
    rows = [[str(y), f"{c['fps'][i]:.1f}", f"{c['max'][i]:.1f}", f"{c['max_renton'][i]:.1f}", f"{c['max_no_fps'][i]:.1f}"]
            for i, y in enumerate(YEARS)]
    tv = K.tview(f"fps {name}, aircraft a month", ["Year", "fps", "MAX (new sites)", "MAX (Renton reassigned)", "MAX, no fps"], rows)
    return f'<div class="panel"><p class="ctitle">{esc(title)}</p>{svg}{tv}</div>', c


def build(out_path):
    b = SD.inputs()["boeing"]
    panels, data = [], {}
    for name, dev in VARIANTS:
        html, c = panel(name, dev)
        panels.append(html)
        data[name] = c
    # the NGSA curve of the chart, moved to the fps entry into service (identical for both options), before the hold
    eis = data["10-year"]["eis"]
    curve = [SD._annual("ngsa", eis - SD.CHART_YEAR, y) / 12.0 for y in range(eis, eis + 9)]
    hold = b["total_rate_cap"] - b["max_tail_rate"]
    n_free = next(i for i, v in enumerate(curve) if v > hold)
    # the game's own record: Boeing's deliveries against its capacity (no fps was launched)
    rd = json.load(open(os.path.join(HERE, "data", "report_data.json")))["rounds"][-1]["sd"]
    below = [y for i, y in enumerate(rd["year"]) if y > 2030 and rd["dlv_max"][i] + rd["dlv_fps"][i] < rd["cap_max"][i] + rd["cap_fps"][i] - 0.5]
    css = K.CSS.replace("--pos: #3b4a5e; --neg: #8792a3;", "--pos: #3b4a5e; --neg: #8792a3; --sq: #8a95a5;")
    css = css.replace("--pos: #c9d3e0; --neg: #5d6a7c; color-scheme: dark; }", "--pos: #c9d3e0; --neg: #5d6a7c; --sq: #6f7b8d; color-scheme: dark; }")
    css += "\np, li, footer { overflow-wrap: break-word; }\n"
    lg = legend([("fps", "s3", "ln"), ("737 MAX, fps at new sites (default)", "s1", "ln"),
                 ("737 MAX, Renton reassigned to the fps", "s1", "dash"), ("737 MAX with no fps", "sq", "dash")])
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Boeing Supply Curves</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{css}</style></head><body><div class="wrap">
<header class="top"><p class="eyebrow">Boeing Product Development · supply-and-demand war game (dash-2050-sd) · BOEING PROPRIETARY</p>
<h1>Boeing supply curves in the game</h1>
<p class="lede">The fps ramps on the NGSA curve of your Airbus Rev. B chart, moved to the fps's entry into service:
{", ".join(f"{v:.0f}" for v in curve[:n_free])} a month in its first {n_free} years. The curve goes on to
{" and ".join(f"{v:.0f}" for v in curve[n_free:n_free + 2])}, but the fps is held to {hold:.0f} a month until {b["max_last_year"]}
and runs at {b["total_rate_cap"]:.0f} from {b["max_last_year"] + 1}. The 7-year and 10-year options share that ramp; they
differ only in when the fps enters service (7 or 10 years after launch). As the fps ramps, the 737 MAX gives way, keeping a
tail of {b["max_tail_rate"]:.0f} a month until {b["max_last_year"]}, so Boeing never builds more than {b["total_rate_cap"]:.0f}
a month in total. Shown for a launch in {LAUNCH}, the game's first decision year.</p></header>
<section style="margin-top:20px"><div class="stack">{lg}{"".join(panels)}
<div class="panel"><p class="label">The rules behind the curves</p><ul class="cav">
<li><b>737 MAX.</b> {", ".join(f"{v:g}" for v in b["max_rate"].values())} a month in 2026-2029, then {b["max_rate_after"]:g}. With no fps it
carries on at {b["max_rate_after"]:g} a month. The 737 rate increase (+100 aircraft a year from {b["rate_increase_from"]}) is not shown; it could be ordered only in 2030.</li>
<li><b>fps.</b> Annual output on the NGSA curve of your chart (rate 50 about four years after entry into service, 100 about eight years after), moved to the fps date.
Until {b["max_last_year"]} it is held to {b["total_rate_cap"] - b["max_tail_rate"]:.0f} a month so the MAX keeps its tail; from {b["max_last_year"] + 1} the MAX ends and the fps runs at {b["total_rate_cap"]:.0f}.</li>
<li><b>New sites (default).</b> The MAX carries on at Renton and Everett and gives way only to Boeing's {b["total_rate_cap"]:.0f}-a-month total.</li>
<li><b>Renton reassigned.</b> Renton's MAX lines ({b["renton_rate"]:g} a month) wind down as the fps ramps there, on the shape of the A320's base rundown on your chart;
the Everett North Line carries on at up to {b["everett_rate"]:g} a month. This saves about ${b["renton_saving_b"]:.1f}B of new-site capex, net of the cost of
converting Renton (range ${b["renton_saving_range_b"][0]:.1f}B-${b["renton_saving_range_b"][1]:.1f}B), pro-rated if Renton is chosen less than three years before entry into service.</li>
</ul><p class="cap">These are capacities; deliveries fall below them when demand does. In the game Boeing did not launch the fps, and its
deliveries fell below the {b["max_rate_after"]:g}-a-month MAX-only capacity in {below[0]}-{below[-1]}, while NGSA entered service and ramped up.
Sources: supply_demand.json and supply_demand_sources.md (Boeing rate path and sites: research notes, October 2026).</p></div>
</div></section>
<footer>BOEING PROPRIETARY. Curves computed by make_supply_curves.py from wargame/dashgame/supply_demand.py (boeing_capacity).</footer></div>
<script>{K.JS}</script></body></html>'''
    with open(out_path, "w") as f:
        f.write(page)
    with open(os.path.join(HERE, "data", "supply_curves.json"), "w") as f:
        json.dump({"launch": LAUNCH, "years": YEARS, "unit": "aircraft a month", "variants": data}, f, indent=1)
    print("wrote", out_path, len(page))


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "boeing_supply_curves.html"))
