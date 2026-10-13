"""Build supply_demand.json, the inputs of the supply-and-demand layer (supply_demand.py).

  python3 make_supply_demand.py <Single-Aisle_Replacement_Demand html>

Sources:
- Airbus supply: the user's chart "Airbus NGSA Production Assessment, A320 Program and NGSA Transition (Rev. B)",
  digitised here as (calendar year, aircraft a month) points: A320 final-assembly rate (base and Alt) and the NGSA
  rate, drawn for NGSA entry into service in mid-2037. The Alt plan keeps the A320 lines longer: "+~1,500 A320
  airplanes, +~$700-800M".
- Demand: the user's page "Single-Aisle Replacement Demand" (Cirium fleet data, 5 and 7 Oct 2026): replacements a
  year of today's 737 MAX, A320neo-family and A220 fleets, firm orders included, on the page's default schedule
  (delivery streams, historical pace, history start), and the split of those replacements by customer group.
- Boeing supply: 737 MAX path and site split from the research notes in supply_demand_sources.md.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# ── Airbus chart (Rev. B), x read off the axis: year = 2029.5 + (px - 391) / 62 (labels at mid-year; the
#    "End of 2029" marker at px 419 reads 2029.95 and "NGSA EIS (Mid 2037)" at px 882 reads 2037.45) ──
CHART_EIS = 2037.45
A320_BASE = [(2025.0, 64), (2025.61, 64), (2025.82, 85), (2037.30, 85), (2037.50, 72), (2038.03, 72), (2038.27, 52),
             (2039.80, 52), (2040.05, 42), (2040.26, 42), (2040.50, 14), (2042.27, 14), (2042.50, 0)]
A320_ALT = [(2025.0, 64), (2025.61, 64), (2025.82, 85), (2037.30, 85), (2037.45, 82), (2038.03, 82), (2038.27, 62),
            (2039.80, 62), (2040.05, 52), (2040.26, 52), (2040.50, 42), (2042.27, 42), (2042.50, 14), (2045.05, 14),
            (2045.25, 0)]
NGSA = [(2037.10, 0), (2037.55, 1), (2038.30, 1), (2038.55, 2), (2038.80, 4), (2039.10, 4), (2039.40, 6), (2039.60, 8),
        (2039.80, 11), (2040.05, 15), (2040.30, 19), (2040.45, 24), (2040.80, 31), (2041.10, 37), (2041.37, 42),
        (2041.55, 50), (2041.80, 50), (2042.00, 59), (2042.27, 59), (2042.50, 70), (2042.75, 70), (2043.00, 76),
        (2043.25, 78), (2043.50, 78), (2043.62, 80), (2043.75, 84), (2044.00, 84), (2044.25, 90), (2044.50, 90),
        (2044.75, 96), (2045.00, 96), (2045.25, 100)]
MILESTONES = {"Toulouse M91 closure": "End of 2029", "NGSA EIS": "Mid 2037", "NGSA rate 50": "3Q41",
              "NGSA rate 80": "4Q43", "NGSA rate 100": "2Q45"}


def demand_from_page(path):
    t = open(path, encoding="utf8").read()
    s = re.findall(r"<script[^>]*>(.*?)</script>", t, flags=re.S)[0]
    i = s.index("const P = ") + len("const P = ")
    P, _ = json.JSONDecoder().raw_decode(s[i:])
    st = P["streams"]["1|history|1"]               # the page's default: streams, historical pace, history start, orders
    yrs = P["years"]
    return {"years": yrs, "replacements": [round(x, 2) for x in st["sched"]],
            "groups": {k: [round(x, 2) for x in v] for k, v in st["groups"].items()},
            "scope": P["summary"], "n": st["n"]}


def main(page):
    R = demand_from_page(page)
    yrs, rep = R["years"], R["replacements"]
    # long-run demand: the board's 2,000 a year is its 20-year market (40,000 aircraft, 2026-2045). Demand = a
    # constant (growth plus replacement of older types) + the replacement of today's fleets from the page, with the
    # constant set so that 2026-2045 averages 2,000 a year.
    w = [r for y, r in zip(yrs, rep) if 2026 <= y <= 2045]
    base = 2000.0 - sum(w) / len(w)
    g = R["groups"]
    lo, hi = 2030, 2060
    idx = [i for i, y in enumerate(yrs) if lo <= y <= hi]
    flex_num = sum(g["both"][i] + g["open"][i] for i in idx)
    tot = sum(g[k][i] for k in g for i in idx)
    out = {
        "_about": __doc__,
        "airbus": {"chart_eis": CHART_EIS, "a320_base": A320_BASE, "a320_alt": A320_ALT, "ngsa": NGSA,
                   "a320_rate_no_ngsa": 85, "milestones": MILESTONES,
                   "alt_cost_b": 0.75, "alt_cost_note": "midpoint of the chart's '+ ~$700-800M' for the Alt plan, "
                   "booked in the NGSA entry-into-service year"},
        "demand": {"years": yrs, "replacements": rep, "groups": g, "base_per_year": round(base, 2),
                   "flex_share": round(flex_num / tot, 4), "flex_window": [lo, hi],
                   "note": "demand(y) = base_per_year + replacements(y); base set so 2026-2045 averages the "
                           "board's 2,000 a year. flex_share: customers flying both types, lessors and unannounced "
                           "customers, as a share of replacements over the flex window; they take the other "
                           "maker's spare slots when their first choice cannot deliver; single-fleet customers wait "
                           "(their unmet demand is lost to the year)."},
    }
    path = os.path.join(HERE, "supply_demand.json")
    old = json.load(open(path)) if os.path.exists(path) else {}
    if "boeing" in old:                             # Boeing inputs are set by hand from the research notes
        out["boeing"] = old["boeing"]
    json.dump(out, open(path, "w"), indent=1)
    print("base per year %.1f, flex share %.3f" % (base, out["demand"]["flex_share"]))
    print("demand 2030/2040/2050/2060:", [round(base + rep[yrs.index(y)]) for y in (2030, 2040, 2050, 2060)])


if __name__ == "__main__":
    main(sys.argv[1])
