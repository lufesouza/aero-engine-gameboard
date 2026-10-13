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
- Demand level: the board's 2,000 a year over 2026-2045; growth share from Airbus GMF 2025.
- Boeing supply: 737 MAX path and site split from the research notes in supply_demand_sources.md (kept on rebuild).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FLEET_2024, FLEET_2044 = 24730, 49210     # Airbus GMF 2025, in-service fleet
SA_SHARE_2024, SA_SHARE_2044 = 0.66, 0.72  # Boeing CMO 2025, single-aisle share of the fleet
GROWTH_2060 = 0.03                         # Boeing CMO 2026, fleet growth about 3% a year
LAPSE = 0.10

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
    # Total demand = replacement + growth (the user's framing).
    # - Replacement: the page's curve for today's MAX, A320neo-family and A220 fleets (firm orders included), as given.
    # - Firm backlog: the page's firm orders (MAX 4,769, A320neo family 7,330; Oct 2026) are committed customers,
    #   delivered first. They are, broadly, the replacement of the older 737NG / A320ceo fleets: Airbus GMF 2025 has
    #   34,250 single-aisle deliveries to 2044, about 15,100 of them replacements, and the page's curve gives about
    #   3,900 of those, leaving about 11,200, close to the 12,099 on order.
    # - Growth (not in the user's data): the single-aisle fleet grows from 66% of 24,730 aircraft in 2024 (Airbus GMF
    #   2025 fleet; Boeing CMO 2025 share) to 72% of 49,210 in 2044, about 3.95% a year; the growth rate then eases in a
    #   straight line to 3.0% a year by 2060 (Boeing CMO 2026: fleet growth about 3% a year).
    # - The A220 is outside the board's 737/A320 market: replacement and growth are scaled by the 737/A320 share of the
    #   page's scope (19,296 of 20,348 aircraft), and the A220's 512 firm orders are left out.
    sc = R["scope"]["by_type_status"]
    a220 = sc["a220"]["now"] + sc["a220"]["ord"]
    class_share = 1.0 - a220 / R["n"]
    f24 = FLEET_2024 * SA_SHARE_2024
    f44 = FLEET_2044 * SA_SHARE_2044
    g44 = (f44 / f24) ** (1 / 20) - 1
    fleet, growth = {2024: f24}, {}
    for y in range(2025, 2101):
        gr = g44 if y <= 2044 else g44 + (GROWTH_2060 - g44) * min(1.0, (y - 2044) / (2060 - 2044))
        fleet[y] = fleet[y - 1] * (1 + gr)
        growth[y] = fleet[y] - fleet[y - 1]           # whole single-aisle fleet; the class share is applied once, in demand()
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
        "demand": {"years": yrs, "replacements": rep, "groups": g, "class_share": round(class_share, 5),
                   "growth": {str(y): round(x, 3) for y, x in growth.items()},
                   "growth_source": "Airbus GMF 2025: fleet 24,730 (2024) to 49,210 (2044), 34,250 single-aisle "
                                    "deliveries to 2044; Boeing CMO 2025: single-aisle 66% of the fleet in 2024, 72% in "
                                    "2044; Boeing CMO 2026: fleet growth about 3% a year. Growth is not in the user's data.",
                   "fleet_growth_2025_44": round(g44, 5), "fleet_growth_2060": GROWTH_2060,
                   "firm_backlog": {"boeing": sc["max"]["ord"], "airbus": sc["neo"]["ord"]},
                   "firm_backlog_note": "the page's firm orders (Cirium, 5 Oct 2026): 737 MAX and A320neo family; "
                                        "delivered first, never lapse or switch maker",
                   "flex_share": round(flex_num / tot, 4), "flex_window": [lo, hi],
                   "lapse_per_year": LAPSE, "lapse_range": [0.05, 0.3],
                   "lapse_note": "share of the still-unserved new customers (not firm orders) who drop out each year: "
                                 "they keep old aircraft longer, defer growth or cancel. Not calibrated; firm-order "
                                 "cancellations run about 2-5% a year and unplaced demand lapses faster.",
                   "note": "total demand = replacement + growth. New demand(y) = (growth(y) + replacements(y)) x "
                           "class_share, split by preference; the firm backlog is delivered first. Replacements after "
                           "2075 are held at the 2075 value. flex_share: customers flying both types, lessors and "
                           "unannounced customers, as a share of replacements over the flex window; when their first "
                           "choice cannot deliver they take the other maker's free slots (each year, from the waiting "
                           "backlog too)."},
    }
    path = os.path.join(HERE, "supply_demand.json")
    old = json.load(open(path)) if os.path.exists(path) else {}
    if "boeing" in old:                             # Boeing inputs are set by hand from the research notes
        out["boeing"] = old["boeing"]
    json.dump(out, open(path, "w"), indent=1)
    nd = lambda y: (growth[y] + rep[yrs.index(min(max(y, yrs[0]), yrs[-1]))]) * class_share
    print("growth %.4f a year to 2044; class share %.4f; flex share %.3f" % (g44, class_share, out["demand"]["flex_share"]))
    print("new demand 2026/2030/2035/2040/2045/2050/2055/2060:", [round(nd(y)) for y in (2026, 2030, 2035, 2040, 2045, 2050, 2055, 2060)])
    print("growth 2026/2035/2044/2050/2060 (737/A320 class):", [round(growth[y] * class_share) for y in (2026, 2035, 2044, 2050, 2060)])
    print("2025-2044 total: growth %.0f + replacement %.0f + firm backlog %d" % (
        sum(growth[y] for y in range(2025, 2045)) * class_share, sum(rep[yrs.index(y)] for y in range(2026, 2045)) * class_share,
        sc["max"]["ord"] + sc["neo"]["ord"]))

if __name__ == "__main__":
    main(sys.argv[1])
