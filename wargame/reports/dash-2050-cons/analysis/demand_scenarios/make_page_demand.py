"""Extract the demand and supply behind chart 4.1 of the user's page "Single-Aisle Replacement Story" into
page_demand.json (data only; nothing from the page is run).

Chart 4.1 (the page's script, data41/data42): demand = replacement of today's fleet + as much again for growth,
  old(y)    the 737NG / A320ceo still flying that the page replaces (chapter 4b), rounded as the page rounds it
  new(y)    today's MAX, neo and A220 (and the counted NG/ceo) replaced as chapters 1-3 set out
  demand(y) = old + new + growth, growth = old + new
with "every aircraft retiring N years later" for N = 1..4 (ch4L), N = 0 being chapter 4 as it stands. The page draws
demand from 2038 ("before then half and half understates it"). Whole single-aisle market, A220 included.
Supply on the page (kept for the supply sensitivity): the 737 at 42/47/52 a month (2026/27/28 on) until the fps
enters service (mid-year), then in a straight line to none at the end of 2050; the fps from entry into service up to
80 a month seven years later; Airbus's A320neo family (plan) and NGSA a month at a time off Airbus's chart; Tianjin
20 a month on top in 2035-2050.

  python3 -I make_page_demand.py <page.html>
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def page_data(path):
    src = open(path, encoding="utf-8").read()
    key = "const P = "
    i = src.index(key) + len(key)
    obj, _ = json.JSONDecoder().raw_decode(src[i:])
    return obj


def main(path):
    P = page_data(path)
    c4, c4b, lat = P["ch4"], P["ch4b"], P["ch4L"]
    years = c4["years"]
    scen = {}
    for n in lat["ns"]:
        if n == 0:
            old, new = [round(x) for x in c4b["old"]], c4["demand"]["all"]
        else:
            old, new = [round(x) for x in lat["old"][str(n)]], lat["new"][str(n)]
        scen[str(n)] = {"old": old, "new": [float(x) for x in new],
                        "demand": [2.0 * (a + b) for a, b in zip(old, new)]}
    mon = c4["monthly"]
    assert all(len(v) == 12 * len(years) for v in mon.values())
    out = {"source": "the user's page 'Single-Aisle Replacement Story' (chart 4.1, 30 Oct 2026): P.ch4, P.ch4b, P.ch4L",
           "years": years, "retire_later": scen,
           "drawn_from": 2038,
           "firm_orders": c4["n_order"],
           "supply": {"monthly_from": years[0], "a320_plan": mon["a320"], "a320_alt": mon["a320_alt"], "ngsa": mon["ngsa"],
                      "ngsa_eis": c4["ngsa_eis"], "fps": c4["fps"], "b737": c4b["b737"],
                      "tianjin": {"rate": 20, "years": [2035, 2050]}}}
    with open(os.path.join(HERE, "page_demand.json"), "w") as f:
        json.dump(out, f, indent=None, separators=(",", ":"))
    for n, s in scen.items():
        d = dict(zip(years, s["demand"]))
        print("N=%s  2038 %5.0f  2041 %5.0f  2044 %5.0f  2050 %5.0f  2060 %5.0f  sum 2038-60 %6.0f" % (
            n, d[2038], d[2041], d[2044], d[2050], d[2060], sum(d[y] for y in range(2038, 2061))))


if __name__ == "__main__":
    main(sys.argv[1])
