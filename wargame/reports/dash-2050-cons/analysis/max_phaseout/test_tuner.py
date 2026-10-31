"""Check do_nothing_tuner.html's JavaScript model against the Python, year by year (needs Playwright's Chromium and node).

- Preset "Game's Do Nothing" on every demand curve = supply_demand.year_rows (the game's own Do Nothing rows).
- Preset "Manual build" = build_scenario.year_rows with the MAX phase-out, Airbus's extra lines and the COMAC/entrant tier.
- Demand levels and the protected tiers: a run with both demand levels moved and COMAC and the entrant protected must stay
  within every maker's capacity, with nothing negative.

  python3 test_tuner.py
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_scenario as B  # noqa: E402

D, L, M, SD = B.D, B.L, B.M, B.SD
PAGE = os.path.abspath(os.path.join(HERE, "..", "..", "do_nothing_tuner.html"))
CURVES = {"N0": D.demand_kw("0"), "N3": D.demand_kw("3"), "game": {}}


def python_rows():
    out = {}
    for name, kw in CURVES.items():
        with L.patched(**kw):
            st, cv = L.grid_states(L.PLAN_DN)[1]
            eis, a, b, dt = M.af_inputs(st, cv)
            cell = M.eval_cell(eis, a, b, trace=True)
            ser = M.af_series(st, cell, eis, dt)
            pref = {r["year"]: r["boeing"]["nb_share"] for r in ser["years"]}
            ys = list(range(2026, 2061))
            game = SD.year_rows(st, pref, ys)
            out["game/" + name] = {y: (game[y]["delivered_b"], game[y]["delivered_a"], game[y]["lost"]) for y in ys}
            if name == "N0":
                bld = B.year_rows(st, pref, ys, phase=True, extra=True, third=True)
                out["build/N0"] = {y: (bld[y]["delivered_b"], bld[y]["delivered_a"], bld[y]["lost"], bld[y]["dlv_comac"],
                                       bld[y]["dlv_entrant"]) for y in ys}
    return out


JS = r"""
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  const errors = [];
  p.on('pageerror', e => errors.push(String(e)));
  await p.goto('file://' + process.argv[2]);
  const res = await p.evaluate(() => {
    const pr = window.__presets, out = {};
    for (const c of ['N0', 'N3', 'game']) out['game/' + c] = window.__run(Object.assign({}, pr.DEF, {curve: c}));
    out['build/N0'] = window.__run(Object.assign({}, pr.P_BUILD));
    out['moved'] = window.__run(Object.assign({}, pr.P_PROT, {dA: 90, dB: 120, curve: 'N2'}));
    return out;
  });
  console.log(JSON.stringify({res, errors}));
  await b.close();
})();
"""


def main():
    ref = python_rows()
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, dir=os.environ.get("TMPDIR")) as f:
        f.write(JS)
        js = f.name
    try:
        r = subprocess.run(["node", js, PAGE], capture_output=True, text=True, check=True)
    finally:
        os.unlink(js)
    got = json.loads(r.stdout)
    assert not got["errors"], got["errors"]
    worst = 0.0
    for key, rows in ref.items():
        js_rows = {x["y"]: x for x in got["res"][key]}
        for y, vals in rows.items():
            x = js_rows[y]
            mine = (x["max"], x["airbus"], x["lost"]) + ((x["comac"], x["entrant"]) if key.startswith("build") else ())
            for a, b in zip(vals, mine):
                worst = max(worst, abs(a - b))
                assert abs(a - b) < 1e-6, (key, y, vals, mine)
    print("JavaScript = Python on %d year-rows (worst gap %.2e)" % (sum(len(v) for v in ref.values()), worst))
    # the moved run: deliveries never exceed capacity, nothing negative
    for x in got["res"]["moved"]:
        assert x["max"] <= x["capMax"] + 1e-6 and x["airbus"] <= x["capA"] + 1e-6, x
        assert x["comac"] <= x["capC"] + 1e-6 and x["entrant"] <= x["capE"] + 1e-6, x
        assert min(x["max"], x["airbus"], x["comac"], x["entrant"], x["lost"]) >= -1e-9, x
    print("moved run: within capacity, nothing negative")


if __name__ == "__main__":
    main()
