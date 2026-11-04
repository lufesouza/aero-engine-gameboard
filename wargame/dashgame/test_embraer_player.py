"""Checks for Embraer as a sixth player (supply_demand option embraer_player) and the political terms (option
politics), on the MAX phase-out market of sd_options_embraer.json.

1. Embraer holding changes nothing: every other player's value equals the same market with no Embraer player.
2. Political terms: with no fps, Boeing pays exactly the exit cost; with an fps, the co-funding line is the share of
   the bill at EIS and the debt penalty falls; Airbus and the engine makers are untouched.
3. Embraer launched: EIS 4 years on, its line and won share follow the rule (by new-generation types in service),
   nothing above capacity or negative, its ΔPV equals a manual build, and its price pressure starts a year before EIS.
4. Engines: Embraer's aircraft fly P&W (CFM with CFM's Embraer partnership); engine volumes cover every delivery.
5. Rules: a 2030 launch cannot be cancelled in 2035 (in service); fps via Embraer and Embraer's own jet exclude each
   other.
6. Briefs: the public rules name Embraer and the politics; Embraer's own terms stay in its brief, Boeing's in Boeing's.

  python3 test_embraer_player.py
"""
import copy
import json
import os
import sys

os.environ["DASH_SD"] = "1"
os.environ["DASH_BOARD"] = "v3"
os.environ.pop("DASH_RUN", None)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import model as M  # noqa: E402
import rules as R  # noqa: E402
import briefs as B  # noqa: E402
import supply_demand as SD  # noqa: E402

FULL = {k: v for k, v in json.load(open(os.path.join(HERE, "sd_options_embraer.json"))).items() if not k.startswith("_")}
fails, ok = [], []


def check(cond, msg):
    (ok if cond else fails).append(msg)
    print(("ok   " if cond else "FAIL ") + msg)


def use(o):
    SD.options = lambda: o
    SD._curve.cache_clear()
    M.refresh_sides()


def opts(emb=True, pol=True):
    o = copy.deepcopy(FULL)
    if not emb:
        o.pop("embraer_player")
    if not pol:
        o.pop("politics")
    return o


def play(orders, year=2030, s=None):
    s1, log = R.adjudicate(s or M.new_state(), year, orders)
    return s1, log


def val(s):
    return M.value(s, covert=True, series=True)


NGSA = {"airbus": {"ngsa": "launch", "ngsa_engine_code": 6}}
FPS = {"boeing": {"fps": "launch_10yr", "fps_engine_code": 7}}
EMB = {"embraer": {"enb": "launch"}}
both = lambda *d: {k: v for x in d for k, v in x.items()}

# 1. Embraer holding changes nothing for anyone else
worst = 0.0
for orders in ({}, NGSA, FPS, both(NGSA, FPS)):
    use(opts(emb=False, pol=False)); a = val(play(orders)[0])
    use(opts(emb=True, pol=False)); b = val(play(orders)[0])
    for side in M.BASE_SIDES:
        worst = max(worst, abs(a[side]["pv_delta"] - b[side]["pv_delta"]))
    check(abs(b["embraer"]["pv_delta"]) < 1e-12, "Embraer holding: its ΔPV is 0 (%s)" % (sorted(orders) or "rivals hold"))
check(worst < 1e-9, "Embraer holding: every other player's ΔPV is unchanged, 4 plans (worst gap %.1e)" % worst)
use(opts(emb=False, pol=False))
check(M.SIDES == M.BASE_SIDES, "without the option there are five players")

# 2. political terms
pol = FULL["politics"]
use(opts(emb=False, pol=False)); off_dn, off_f = val(play(NGSA)[0]), val(play(both(NGSA, FPS))[0])
use(opts(emb=False, pol=True)); s_dn = play(NGSA)[0]; s_f = play(both(NGSA, FPS))[0]; on_dn, on_f = val(s_dn), val(s_f)
w = on_dn["boeing"]["wacc"]
x = pol["exit_p"] * pol["exit_loss_b"] * sum((1 + w) ** -t for t in range(20)) * (1 + w) ** -(2045 - 2026)
check(abs((off_dn["boeing"]["pv_delta"] - on_dn["boeing"]["pv_delta"]) - x) < 1e-9 and abs(x - M.exit_cost(w, 2030)) < 1e-12,
      "no fps: Boeing pays the exit cost exactly (%.3f $B; 2050 decision %.3f $B)" % (x, M.exit_cost(w, 2050)))
f = s_f["prog"]["fps"]
cof = pol["boeing_cofund"] * M.af_bill("fps", f["variant"]) / (1 + w) ** (f["eis"] - 2026)
d_pen = on_f["boeing"]["bridge"]["debt_penalty"] - off_f["boeing"]["bridge"]["debt_penalty"]
check(abs(on_f["boeing"]["bridge"]["government_cofunding"] - cof) < 1e-12 and d_pen > 0 and
      abs((on_f["boeing"]["pv_delta"] - off_f["boeing"]["pv_delta"]) - (cof + d_pen)) < 1e-9,
      "fps: co-funding = 2%% of the bill at EIS (%.3f $B) and the debt penalty falls (%.3f $B)" % (cof, d_pen))
check(all(abs(on_f[s]["pv_delta"] - off_f[s]["pv_delta"]) < 1e-12 for s in ("airbus", "cfm", "pratt_whitney", "rolls_royce")),
      "politics leaves Airbus and the engine makers unchanged")

# 3. Embraer launched
use(opts())
em = FULL["embraer_player"]
s1, _ = play(both(EMB, NGSA, FPS))
v = val(s1)
r = s1["prog"]["enb"]
check(r["eis"] == 2034, "a 2030 launch enters service in 2034")
rows = {x["year"]: x for x in v["_af_series"]["years"]}
bad_cap = bad_sh = 0
for y, x in rows.items():
    sd = x["sd"]
    cap = 12 * em["peak_a_month"] * min(1.0, (y - 2034 + 1) / em["years_to_peak"]) if y >= 2034 else 0.0
    n = (y >= 2037) + (y >= 2040)
    sh = em["share_by_newgen"][n] * (1 - em["us_tariff_share_cut"])
    bad_cap += abs(sd["cap_entrant"] - cap) > 1e-9 or sd["dlv_embraer"] > cap + 1e-9 or sd["dlv_embraer"] < -1e-12
    bad_sh += abs(sd["share_embraer"] - sh) > 1e-12
check(bad_cap == 0, "Embraer's line: 0 before 2034, then up to 96 a year in 6 years; deliveries within it, never negative")
check(bad_sh == 0, "Embraer's won share: 10.8% with no new-generation type, 6.3% with one (NGSA 2037), 3.6% with both (fps 2040)")
neg = [y for y, x in rows.items() for k in ("dlv_max", "dlv_fps", "dlv_a320", "dlv_ngsa", "dlv_comac", "dlv_embraer") if x["sd"][k] < -1e-9]
over = [y for y, x in rows.items() if x["sd"]["dlv_max"] + x["sd"]["dlv_fps"] > x["sd"]["cap_max"] + x["sd"]["cap_fps"] + 1e-6 or
        x["sd"]["dlv_a320"] + x["sd"]["dlv_ngsa"] > x["sd"]["cap_a320"] + x["sd"]["cap_ngsa"] + 1e-6]
check(not neg and not over, "books balance: no maker above its capacity, nothing negative")
wE = em["wacc"]
prof = sum(rows[y]["sd"]["dlv_embraer"] * em["price_m"] * em["margin"] / 1000 / (1 + wE) ** (y - 2026) for y in range(2034, 2054))
own = em["bill_b"] * (1 - em["partner_share"] - em["supplier_share"] - em["state_share"])
tc = M.true_cost(own, own / (1 + wE) ** 8, em["debt_b"], em["ev_b"], em["alpha"])
check(abs(v["embraer"]["pv_delta"] - (prof - tc)) < 1e-9,
      "Embraer's ΔPV = profit %.3f − (bill %.3f + debt penalty %.3f) = %.3f $B (manual build)" % (
          prof, own / (1 + wE) ** 8, tc - own / (1 + wE) ** 8, prof - tc))
pp = SD.price_pressure(s1)
check(pp == {"from": 2033, "ramp_years": em["ramp_years"], "cut": 0.02, "cut_boeing_no_fps": 0.02 * 1.3} and
      SD.price_pressure(SD.sq_state()) is None and SD.price_pressure(play(NGSA)[0]) is None,
      "price pressure from 2033 (a year before EIS), 2.6% on Boeing with no fps; none without Embraer's jet or in the status quo")
s_dn_e = play(both(EMB, NGSA))[0]
check(abs(SD.price_cut(s_dn_e, "boeing", 2040) - 0.026) < 1e-12 and abs(SD.price_cut(s_dn_e, "airbus", 2040) - 0.02) < 1e-12 and
      abs(SD.price_cut(s_dn_e, "airbus", 2034) - 0.02 * 2 / 7) < 1e-12, "the cut ramps over 7 years from 2033")

# 4. engines
en = {x["year"]: x for x in v["_en_series"]["years"]}
gap = max(abs(sum(en[y][m]["nb_units"] for m in ("cfm", "pratt_whitney", "rolls_royce")) -
              2 * (rows[y]["boeing"]["nb_units"] + rows[y]["airbus"]["nb_units"] + rows[y]["sd"]["dlv_embraer"])) for y in range(2026, 2061))
check(gap < 1e-6, "narrowbody engines = 2 x (Boeing + Airbus + Embraer deliveries), every year (worst gap %.1e)" % gap)
s_c = play(both(EMB, {"cfm": {"ducted": "launch", "partner_embraer": "launch"}}))[0]
s_p = play(EMB)[0]
vc, vp = val(s_c), val(s_p)
y = 2045
e = {x["year"]: x for x in vp["_af_series"]["years"]}[y]["sd"]["dlv_embraer"]
pw_e = vp["_en_series"]["years"][y - 2026]["pratt_whitney"]["nb_units"]
check(M.emb_engine_maker(s_p) == 1 and M.emb_engine_maker(s_c) == 0 and pw_e >= 2 * e - 1e-6,
      "Embraer flies P&W (2045: %d of P&W's %d engines), CFM with CFM's Embraer partnership" % (round(2 * e), round(pw_e)))

# 5. rules
check(R.legal_options(s1, "embraer", 2035)["enb"] == ["hold"], "a 2030 launch is in service by 2035: no cancel")
s3, _ = play(both(EMB))
check("launch_via_embraer" not in R.legal_options(s3, "boeing", 2035)["fps"], "Embraer's jet live: no fps via Embraer")
s4, log4 = play(both(EMB, {"boeing": {"fps": "launch_via_embraer", "fps_engine_code": 7}}))
check(not M.live(s4, "enb") and any("refused" in e_ for e_ in log4) and R.legal_options(s4, "embraer", 2035)["enb"] == ["hold"],
      "fps via Embraer and Embraer's jet in the same round: Boeing's order stands, Embraer's launch is refused")
s5, _ = play(both(EMB), year=2035)
c5, _ = R.validate(s5, "embraer", 2045, {"enb": "cancel"})
check(c5["enb"] == "hold", "a 2035 launch (EIS 2039) cannot be cancelled in 2045")

# 6. briefs
pub = B.public_rules()
check("Embraer is a sixth player" in pub and "## Politics (public context)" in pub and "`enb`: `launch`" in pub,
      "public rules: Embraer's move, its market rules and the politics")
st0 = M.new_state()
eb = B.private_brief(st0, "embraer", 2030, 1)[0]
bb = B.private_brief(st0, "boeing", 2030, 1)[0]
check("Your new narrowbody's economics" in eb and "If you launch this round" in eb and "Governments carry" not in eb,
      "Embraer's brief: its economics and a launch preview, not Boeing's terms")
check("Embraer launches its new narrowbody" in bb and "Team Korea (KAI" not in bb and "Governments carry 2%" in bb,
      "Boeing's brief: Embraer columns and its own political terms, not Embraer's economics")
use(opts(emb=False, pol=False))
check("Embraer is a sixth player" not in B.public_rules() and "Politics (public context)" not in B.public_rules(),
      "without the options the rules do not mention them")

if fails:
    print("FAILURES:", len(fails))
    for f_ in fails:
        print("  ", f_)
    sys.exit(1)
print("ALL CHECKS PASSED (%d)" % len(ok))
