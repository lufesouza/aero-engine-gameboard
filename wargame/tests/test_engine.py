"""Regression tests for the war-game engine: python3 -m unittest discover -s wargame/tests"""

import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from wargame import model as M  # noqa: E402
from wargame import solver as S  # noqa: E402


def orders(side, launch=(), cancel=(), **flags):
    o = M.empty_orders(side)
    o["launch"] = list(launch)
    o["cancel"] = list(cancel)
    o.update(flags)
    return o


def L(cfg, pid, year, variant=None, engine=None):
    pc = cfg["programs"][pid]
    e = {"program": pid, "year": year, "engine": engine or pc["default_engine"]}
    if "variants" in pc:
        e["variant"] = variant or pc["default_variant"]
    return e


def rec(turn, b=None, a=None, injects=(), market=None):
    return {"turn": turn, "injects": list(injects),
            "orders": {"boeing": b or M.empty_orders("boeing"), "airbus": a or M.empty_orders("airbus")},
            "market": market or {}}


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.cfg = M.load_config("base")

    def pay(self, hist, cfg=None):
        return M.payoff(cfg or self.cfg, hist)

    def test_status_quo_is_zero(self):
        for inj in ([], ["nb_demand_shock"], ["trade_dispute"], ["boeing_quality_escape"]):
            u = self.pay([rec(1, injects=inj), rec(2)])
            self.assertAlmostEqual(u["boeing"], 0.0, places=9)
            self.assertAlmostEqual(u["airbus"], 0.0, places=9)

    def test_components_sum_exactly(self):
        c = self.cfg
        hist = [rec(1, orders("boeing", [L(c, "fps", 2026, "jv")], rate_increase=True),
                    orders("airbus", [L(c, "ngsa", 2027)], delay_tactics=True, poaching=True), injects=["supply_chain_crunch"]),
                rec(2, orders("boeing", [L(c, "re787", 2029)]), orders("airbus", [L(c, "rea350", 2030)], delay_tactics=True))]
        r = M.evaluate(c, M.build_world(c, hist))
        for s in M.SIDES:
            self.assertAlmostEqual(sum(r[s]["components_pv_b"].values()), r[s]["delta_pv_b"], places=2)
            self.assertLess(r[s]["components_pv_b"]["strain"], 0)

    def test_fps_margin_direction(self):
        hist = [rec(1, orders("boeing", [L(self.cfg, "fps", 2026)]))]
        lo = self.pay(hist)["boeing"]
        cfg = M.load_config("base", {"programs": {"fps": {"margin_alone": 0.28, "margin_both": 0.28}}})
        self.assertGreater(self.pay(hist, cfg)["boeing"], lo)

    def test_capex_and_strain_direction(self):
        c = self.cfg
        hist = [rec(1, orders("boeing", [L(c, "fps", 2026), L(c, "re787", 2027)]))]
        base = self.pay(hist)["boeing"]
        more_capex = M.load_config("base", {"programs": {"fps": {"capex_b": 35.0}}})
        more_strain = M.load_config("base", {"strain": {"full_overlap_b": 6.0}})
        self.assertLess(self.pay(hist, more_capex)["boeing"], base)
        self.assertLess(self.pay(hist, more_strain)["boeing"], base)

    def test_strain_matches_overlap_formula(self):
        c = self.cfg
        # NB in development 2026-2032, WB 2029-2033: overlap 2029..2032 = 4 years -> 3.0 * 4/5 = 2.4 nominal
        hist = [rec(1, orders("boeing", [L(c, "fps", 2026)])), rec(2, orders("boeing", [L(c, "re787", 2029)]))]
        r = M.evaluate(c, M.build_world(c, hist))
        self.assertAlmostEqual(r["boeing"]["undiscounted_b"]["strain"], -2.4 * (1 + c["players"]["boeing"]["alpha"]), places=3)

    def test_delay_tactics_hurt_boeing_only_when_fps_in_development(self):
        c = self.cfg
        with_fps = [rec(1, orders("boeing", [L(c, "fps", 2026)]), orders("airbus", delay_tactics=True))]
        without = [rec(1, orders("boeing", [L(c, "fps", 2026)]))]
        self.assertLess(self.pay(with_fps)["boeing"], self.pay(without)["boeing"])
        w = M.build_world(c, with_fps)
        self.assertEqual(w.programs["fps"].eis, 2026 + 7 + 1)
        no_fps = [rec(1, a=orders("airbus", delay_tactics=True))]
        self.assertAlmostEqual(self.pay(no_fps)["boeing"], 0.0, places=9)
        self.assertLess(self.pay(no_fps)["airbus"], 0.0)

    def test_delay_slip_cap_and_exposure(self):
        c = self.cfg
        hist = [rec(t, orders("boeing", [L(c, "fps", 2026)]) if t == 1 else None, orders("airbus", delay_tactics=True))
                for t in (1, 2, 3)]
        w = M.build_world(c, hist)
        self.assertEqual(w.programs["fps"].delay_slip_years, c["tactics"]["delay_tactics"]["max_total_slip"])
        self.assertEqual(w.exposure_turn, 2)
        self.assertEqual(w.exposure_year, M.turn_years(c, 2)[1] + 1)

    def test_poaching(self):
        c = self.cfg
        idle = [rec(1, a=orders("airbus", poaching=True))]
        self.assertAlmostEqual(self.pay(idle)["boeing"], 0.0, places=9)
        both_dev = [rec(1, orders("boeing", [L(c, "fps", 2026)]), orders("airbus", [L(c, "ngsa", 2026)], poaching=True))]
        no_poach = [rec(1, orders("boeing", [L(c, "fps", 2026)]), orders("airbus", [L(c, "ngsa", 2026)]))]
        self.assertLess(self.pay(both_dev)["boeing"], self.pay(no_poach)["boeing"])
        self.assertGreater(self.pay(both_dev)["airbus"], self.pay(no_poach)["airbus"])

    def test_share_capture_and_freeze(self):
        c = self.cfg
        hist = [rec(1, orders("boeing", [L(c, "fps", 2028)]), orders("airbus", [L(c, "ngsa", 2026)]))]
        w = M.build_world(c, hist)
        self.assertEqual((w.programs["ngsa"].eis, w.programs["fps"].eis), (2033, 2035))
        r = M.evaluate(c, w)
        speed = c["segments"]["nb"]["capture_pp_per_year"] / 100
        self.assertAlmostEqual(r["shares"]["nb"]["2035"]["airbus"], 0.60 + 2 * speed, places=4)
        self.assertAlmostEqual(r["shares"]["nb"]["2050"]["airbus"], 0.60 + 2 * speed, places=4)

    def test_market_multiplier_direction(self):
        c = self.cfg
        hist = [rec(1, orders("boeing", [L(c, "fps", 2026)]))]
        hot = [dict(hist[0], market={"capture_mult": {"fps": 1.25}})]
        self.assertGreater(self.pay(hot)["boeing"], self.pay(hist)["boeing"])

    def test_rate_increase_raises_nb_operating(self):
        c = self.cfg
        r0 = M.evaluate(c, M.build_world(c, [rec(1)]))
        r1 = M.evaluate(c, M.build_world(c, [rec(1, orders("boeing", rate_increase=True))]))
        self.assertGreater(r1["boeing"]["components_pv_b"]["nb_operating"], r0["boeing"]["components_pv_b"]["nb_operating"])
        self.assertLess(r1["airbus"]["components_pv_b"]["nb_operating"], 0)

    def test_jv_shares_capex(self):
        c = self.cfg
        solo = M.evaluate(c, M.build_world(c, [rec(1, orders("boeing", [L(c, "fps", 2026, "solo")]))]))
        jv = M.evaluate(c, M.build_world(c, [rec(1, orders("boeing", [L(c, "fps", 2026, "jv")]))]))
        ratio = jv["boeing"]["undiscounted_b"]["capex"] / solo["boeing"]["undiscounted_b"]["capex"]
        self.assertAlmostEqual(ratio, 1 - c["programs"]["fps"]["variants"]["jv"]["capex_share_partner"], places=6)

    def test_cancel_stops_capex_and_service(self):
        c = self.cfg
        hist = [rec(1, orders("boeing", [L(c, "fps", 2026)])), rec(2, orders("boeing", cancel=["fps"]))]
        r = M.evaluate(c, M.build_world(c, hist))
        self.assertAlmostEqual(r["boeing"]["components_pv_b"]["nb_operating"], 0.0, places=9)
        spent = sum(c["programs"]["fps"]["capex_b"] / 7 for _ in range(2026, 2029)) * (1 + c["players"]["boeing"]["alpha"])
        self.assertAlmostEqual(r["boeing"]["undiscounted_b"]["capex"], -spent, places=3)

    def test_widebody_chicken_landmark(self):
        """Calibration landmark from the combined_dash.py board: the widebody sub-game is Chicken.

        Both lone re-engine cells are pure Nash; neither re-engining is not Nash;
        both re-engining is not Nash.
        """
        c = self.cfg
        res = S.plan_game(c, [], 1, 4, 1, [], segment="wb")
        cells = {(n["boeing_plan"].startswith("re787"), n["airbus_plan"].startswith("rea350")) for n in res["pure_nash"]}
        self.assertEqual(cells, {(True, False), (False, True)})

    def test_validation(self):
        c = self.cfg
        hist = [rec(1, orders("boeing", [L(c, "fps", 2026)]))]
        pend = hist + [rec(2)]
        bad = [
            ("boeing", {"launch": [{"program": "fps"}]}, "already launched"),
            ("boeing", {"launch": [{"program": "ngsa"}]}, "not a boeing program"),
            ("boeing", {"launch": [{"program": "re787", "year": 2026}]}, "must be an integer in this turn"),
            ("boeing", {"launch": [{"program": "re787", "engine": "cfm_ducted"}]}, "not available"),
            ("boeing", {"cancel": ["re787"]}, "has not been launched"),
            ("airbus", {"rate_increase": True}, "boeing lever"),
            ("boeing", {"delay_tactics": "yes"}, "true or false"),
        ]
        for side, o, msg in bad:
            canon, errors, _ = M.validate_orders(c, pend, 2, side, o)
            self.assertIsNone(canon, (side, o))
            self.assertTrue(any(msg in e for e in errors), (msg, errors))
        canon, errors, _ = M.validate_orders(c, pend, 2, "boeing", {"launch": ["re787"], "cancel": ["fps"]})
        self.assertEqual(errors, [])
        self.assertEqual(canon["launch"][0]["year"], 2029)

    def test_belief_mask_hides_unexposed_delay(self):
        c = self.cfg
        hist = [rec(1, orders("boeing", [L(c, "fps", 2026)]), orders("airbus", delay_tactics=True))]
        mask = M.belief_mask(c, hist, "boeing")
        self.assertEqual(mask, frozenset({1}))
        seen = M.payoff(c, hist, mask)
        true = M.payoff(c, hist)
        self.assertAlmostEqual(seen["boeing"], true["boeing"], places=9)  # own payoff exact
        self.assertGreater(seen["airbus"], true["airbus"])  # hidden cost not in the estimate
        hist2 = hist + [rec(2, a=orders("airbus", delay_tactics=True))]
        self.assertEqual(M.belief_mask(c, hist2, "boeing"), frozenset())  # exposed after two turns


class History2010Tests(unittest.TestCase):
    """The hist-2010-neo backtest scenario and the engine features it relies on."""

    def setUp(self):
        self.cfg = M.load_config("hist-2010-neo")

    def B(self, year, variant):
        o = M.empty_orders("boeing")
        o["launch"] = [{"program": "b737next", "year": year, "engine": "cfm_leap", "variant": variant}]
        return o

    def neo(self):
        o = M.empty_orders("airbus")
        o["launch"] = [{"program": "a320neo", "year": 2010, "engine": "cfm_leap"}]
        return o

    def test_scenario_replaces_sections(self):
        self.assertEqual(set(self.cfg["programs"]), {"b737next", "a320neo"})
        self.assertEqual(self.cfg["years"]["pv_base"], 2010)
        self.assertFalse(M.tactic_enabled(self.cfg, "delay_tactics"))
        self.assertAlmostEqual(M.payoff(self.cfg, [rec(1)])["boeing"], 0.0, places=9)

    def test_variant_economics(self):
        w = M.build_world(self.cfg, [rec(1, a=self.neo()), rec(2, self.B(2011, "cleansheet"))])
        self.assertEqual(w.programs["b737next"].eis, 2020)
        w = M.build_world(self.cfg, [rec(1, a=self.neo()), rec(2, self.B(2011, "reengine"))])
        self.assertEqual(w.programs["b737next"].eis, 2017)
        r = M.evaluate(self.cfg, M.build_world(self.cfg, [rec(1, a=self.neo()), rec(2, self.B(2011, "cleansheet"))]))
        self.assertAlmostEqual(r["boeing"]["undiscounted_b"]["capex"], -18.0 * (1 + self.cfg["players"]["boeing"]["alpha"]), places=3)

    def test_disabled_tactics_rejected(self):
        _, errors, _ = M.validate_orders(self.cfg, [rec(1)], 1, "airbus", {"delay_tactics": True})
        self.assertTrue(any("not available in this scenario" in e for e in errors))

    def test_background_development_adds_strain(self):
        r = M.evaluate(self.cfg, M.build_world(self.cfg, [rec(1, self.B(2010, "reengine"))]))
        self.assertLess(r["boeing"]["components_pv_b"]["strain"], 0)  # overlaps 787/747-8 to 2012
        r = M.evaluate(self.cfg, M.build_world(self.cfg, [rec(1), rec(2), rec(3, self.B(2012, "reengine"))]))
        self.assertAlmostEqual(r["boeing"]["components_pv_b"]["strain"], 0.0, places=9)  # background ends 2012

    def test_conditional_share_shift(self):
        hit = [rec(1, a=self.neo()), rec(2, injects=["major_order_split"])]
        answered = [rec(1, a=self.neo()), rec(2, self.B(2011, "reengine"), injects=["major_order_split"])]
        base_answered = [rec(1, a=self.neo()), rec(2, self.B(2011, "reengine"))]
        # doing nothing: the defection is in the status quo too, so no extra delta
        self.assertAlmostEqual(M.payoff(self.cfg, hit)["boeing"],
                               M.payoff(self.cfg, [rec(1, a=self.neo()), rec(2)])["boeing"], places=1)
        # answering in the same turn averts the loss: worth more than without the shock
        self.assertGreater(M.payoff(self.cfg, answered)["boeing"], M.payoff(self.cfg, base_answered)["boeing"])

    def test_tech_edge_recaptures_share(self):
        r = M.evaluate(self.cfg, M.build_world(self.cfg, [rec(1, a=self.neo()), rec(2, self.B(2011, "cleansheet"))]))
        self.assertGreater(r["shares"]["nb"]["2040"]["boeing"], r["shares"]["nb"]["2030"]["boeing"])
        r = M.evaluate(self.cfg, M.build_world(self.cfg, [rec(1, a=self.neo()), rec(2, self.B(2011, "reengine"))]))
        self.assertAlmostEqual(r["shares"]["nb"]["2040"]["boeing"], r["shares"]["nb"]["2030"]["boeing"], places=6)


class CliBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = dict(os.environ, WARGAME_RUNS_DIR=self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args, stdin=None, ok=True):
        p = subprocess.run([sys.executable, "-m", "wargame.engine", *args], cwd=ROOT, env=self.env,
                           input=json.dumps(stdin) if stdin is not None else None, capture_output=True, text=True)
        if ok:
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        return p.returncode, (json.loads(p.stdout) if p.stdout.strip().startswith("{") else p.stdout)


class CliTests(CliBase):
    def test_full_turn_cycle_and_fog(self):
        self.run_cli("new", "--run-id", "g", "--turns", "2")
        _, inj = self.run_cli("inject", "--run", "g", "--auto")
        _, inj2 = self.run_cli("inject", "--run", "g", "--auto", ok=False)
        self.assertEqual(inj2["status"], "error")  # max one inject per turn
        good = {"boeing": {"launch": [{"program": "fps"}], "public_statement": "Boeing's fps: go", "rationale": "secret"},
                "airbus": {"launch": [{"program": "ngsa"}], "delay_tactics": True, "rationale": "slow them"},
                "market": {"capture_mult": {"fps": 1.1}, "narrative": "Airlines queue for fps."}}
        bad = dict(good, boeing={"launch": [{"program": "ngsa"}]})
        code, res = self.run_cli("adjudicate", "--run", "g", "--turn", "1", stdin=bad, ok=False)
        self.assertEqual((code, res["status"]), (2, "invalid"))
        _, st = self.run_cli("status", "--run", "g")
        self.assertEqual(st["current_turn"], 1)
        _, res = self.run_cli("adjudicate", "--run", "g", "--turn", "1", stdin=good)
        self.assertEqual(res["orders_received"]["airbus"]["delay_tactics"], True)
        _, bb = self.run_cli("brief", "--run", "g", "--side", "boeing")
        text = json.dumps(bb)
        self.assertNotIn("Delay Tactics", text)
        self.assertNotIn("slow them", text)
        self.assertIn("supplier bottleneck", text)
        _, ba = self.run_cli("brief", "--run", "g", "--side", "airbus")
        self.assertNotIn("secret", json.dumps(ba))
        self.assertIn("Boeing's fps: go", json.dumps(ba))
        _, opt = self.run_cli("options", "--run", "g", "--side", "boeing", "--compact")
        self.assertTrue(opt["your_options"])
        _, wi = self.run_cli("whatif", "--run", "g", "--side", "boeing", stdin={"boeing": {"2": {"launch": ["re787"]}}})
        self.assertIn("change_vs_current_projection_b", wi["boeing"])
        _, rb = self.run_cli("rollback", "--run", "g", "--to-turn", "1")
        self.assertEqual(rb["pending_injects"], [inj["applied"]["id"]])
        self.run_cli("adjudicate", "--run", "g", "--turn", "1", stdin=good)
        self.run_cli("inject", "--run", "g", "--none")
        _, res = self.run_cli("adjudicate", "--run", "g", "--turn", "2", stdin={"boeing": {}, "airbus": {"delay_tactics": True}})
        self.assertTrue(res["game_complete"])
        _, eq = self.run_cli("equilibria", "--run", "g", "--segment", "wb")
        self.assertIn("regret_vs_actual", eq)
        code, md = self.run_cli("report", "--run", "g", "--format", "md")
        self.assertIn("Scoreboard", md)
        _, bb = self.run_cli("brief", "--run", "g", "--side", "boeing")
        self.assertTrue(bb["delay_tactics_exposed"])

    def test_referee_disclosure_relay_and_scorecard(self):
        self.run_cli("new", "--run-id", "ref", "--turns", "2")
        self.run_cli("inject", "--run", "ref", "--none")
        orders = {
            "boeing": {"launch": [], "rate_increase": True, "public_statement": "Stability first.",
                       "disclose": ["We will not launch a new airplane before 2029."],
                       "prediction": {"launch": ["ngsa"], "delay_tactics": False, "poaching": True},
                       "rationale": "BOEING-PRIVATE", "expected_delta_pv_b": 1.5},
            "airbus": {"launch": [{"program": "ngsa", "year": 2028, "engine": "pw_gtf2"}], "delay_tactics": True,
                       "poaching": True, "disclose": ["NGSA enters service in 2035."],
                       "prediction": {"launch": [], "rate_increase": True},
                       "rationale": "AIRBUS-PRIVATE", "expected_delta_pv_b": 20.0},
        }
        _, res = self.run_cli("adjudicate", "--run", "ref", "--turn", "1", stdin=orders)
        self.assertEqual(res["status"], "ok")
        self.run_cli("annotate", "--run", "ref", "--turn", "1", "--side", "airbus", "--note", "consistent with the public record")
        _, bb = self.run_cli("brief", "--run", "ref", "--side", "boeing")
        text = json.dumps(bb)
        self.assertIn("NGSA enters service in 2035.", text)          # rival disclosure relayed
        self.assertIn("consistent with the public record", text)     # with the referee note
        for secret in ("AIRBUS-PRIVATE", "Delay Tactics", '"prediction"', '"expected_delta_pv_b"'):
            self.assertNotIn(secret, text)  # no rival rationale, covert move, prediction or expectation
        _, ba = self.run_cli("brief", "--run", "ref", "--side", "airbus")
        self.assertIn("We will not launch a new airplane before 2029.", json.dumps(ba))
        self.assertNotIn("BOEING-PRIVATE", json.dumps(ba))
        _, sc = self.run_cli("scorecard", "--run", "ref")
        rows = {r["side"]: r for r in sc["rows"]}
        self.assertEqual(rows["boeing"]["prediction_accuracy"], 0.833)  # 5 of 6: missed the covert Delay Tactics
        self.assertEqual(rows["airbus"]["prediction_accuracy"], 1.0)
        for side in ("boeing", "airbus"):
            r = rows[side]
            self.assertGreaterEqual(r["best_response_value_b"], r["myopic_value_b"])
            self.assertTrue(0.0 <= r["capture"] <= 1.0)
            self.assertAlmostEqual(r["regret_b"], r["best_response_value_b"] - r["myopic_value_b"], places=2)
        self.assertAlmostEqual(rows["airbus"]["expectation_error_b"],
                               res["projection"]["airbus"]["delta_pv_b"] - 20.0, places=2)
        code, _ = self.run_cli("scorecard", "--run", "ref", "--final", ok=False)
        self.assertEqual(code, 1)  # game not complete yet

    def test_auto_inject_is_deterministic(self):
        picks = []
        for rid in ("x", "x"):
            self.run_cli("new", "--run-id", rid, "--force", "--seed", "7")
            picks.append(self.run_cli("inject", "--run", rid, "--auto")[1]["applied"]["id"])
        self.assertEqual(picks[0], picks[1])


def rr_orders(launch=(), cancel=(), t1000=False):
    return {"launch": list(launch), "cancel": list(cancel), "t1000_upgrade": t1000}


def rr_rec(turn, b=None, a=None, rr=None, injects=()):
    r = rec(turn, b, a, injects)
    r["orders"]["rolls_royce"] = rr or rr_orders()
    return r


class RollsRoyceTests(unittest.TestCase):
    """The optional supplier player (Rolls-Royce)."""

    def setUp(self):
        self.cfg = M.load_config("base", {"suppliers": {"rolls_royce": {"active": True}}})

    def ev(self, hist):
        return M.evaluate(self.cfg, M.build_world(self.cfg, hist))

    def uf_nb(self, year, variant="solo", terms="standard"):
        return {"program": "uf_nb", "year": year, "variant": variant, "terms": terms}

    def test_inactive_by_default(self):
        cfg = M.load_config("base")
        self.assertEqual(M.players(cfg), M.SIDES)
        self.assertNotIn("rolls_royce", M.evaluate(cfg, M.build_world(cfg, [rec(1)])))
        self.assertEqual(M.players(self.cfg), ("boeing", "airbus", "rolls_royce"))

    def test_status_quo_is_zero(self):
        for inj in ([], ["rr_durability_crisis"], ["nb_demand_shock"], ["supply_chain_crunch"]):
            u = M.payoff(self.cfg, [rr_rec(1, injects=inj), rr_rec(2)])
            for s in M.players(self.cfg):
                self.assertAlmostEqual(u[s], 0.0, places=9)

    def test_uncommitted_engine_falls_back(self):
        c = self.cfg
        with_rr = [rr_rec(1, a=orders("airbus", [L(c, "ngsa", 2028, engine="rr_ultrafan_nb")]))]
        with_cfm = [rr_rec(1, a=orders("airbus", [L(c, "ngsa", 2028, engine="cfm_ducted")]))]
        w = M.build_world(c, with_rr)
        self.assertEqual((w.programs["ngsa"].engine, w.programs["ngsa"].engine_requested), ("cfm_ducted", "rr_ultrafan_nb"))
        self.assertAlmostEqual(M.payoff(c, with_rr)["airbus"], M.payoff(c, with_cfm)["airbus"], places=9)
        self.assertAlmostEqual(M.payoff(c, with_rr)["rolls_royce"], 0.0, places=9)

    def test_commitment_same_turn_and_components(self):
        c = self.cfg
        hist = [rr_rec(1, a=orders("airbus", [L(c, "ngsa", 2028, engine="rr_ultrafan_nb")]), rr=rr_orders([self.uf_nb(2026)]))]
        w = M.build_world(c, hist)
        self.assertEqual((w.programs["ngsa"].engine, w.programs["ngsa"].supplier), ("rr_ultrafan_nb", "rolls_royce"))
        r = self.ev(hist)["rolls_royce"]
        self.assertGreater(r["components_pv_b"]["nb_engines"], 0)
        self.assertLess(r["components_pv_b"]["capex"], 0)
        self.assertAlmostEqual(sum(r["components_pv_b"].values()), r["delta_pv_b"], places=2)
        self.assertAlmostEqual(r["undiscounted_b"]["capex"], -8.0 * 1.25, places=6)
        self.assertEqual(r["programs"][0]["selected_by"], ["airbus:ngsa"])

    def test_airframe_waits_for_late_engine(self):
        c = self.cfg
        hist = [rr_rec(1, b=orders("boeing", [L(c, "fps", 2026, engine="rr_ultrafan_nb")]), rr=rr_orders([self.uf_nb(2028)]))]
        p = M.build_world(c, hist).programs["fps"]
        self.assertEqual((p.engine_wait, p.eis), (2, 2035))  # own EIS 2033, engine ready 2028 + 7
        hist2 = [dict(hist[0], injects=[]), rr_rec(2, injects=["ultrafan_test_setback"])]
        self.assertEqual(M.build_world(c, hist2).programs["fps"].eis, 2037)

    def test_losing_the_a350_costs_rr(self):
        c = self.cfg
        r = self.ev([rr_rec(1, a=orders("airbus", [L(c, "rea350", 2026, engine="ge_genx_next")]))])["rolls_royce"]
        self.assertLess(r["components_pv_b"]["wb_engines"], 0)

    def test_jv_halves_capex_and_value(self):
        c = self.cfg
        def run(v):
            return self.ev([rr_rec(1, a=orders("airbus", [L(c, "ngsa", 2028, engine="rr_ultrafan_nb")]),
                                   rr=rr_orders([self.uf_nb(2026, v)]))])["rolls_royce"]
        solo, jv = run("solo"), run("jv_pw")
        self.assertAlmostEqual(jv["undiscounted_b"]["capex"], solo["undiscounted_b"]["capex"] / 2, places=6)
        self.assertAlmostEqual(jv["undiscounted_b"]["nb_engines"], solo["undiscounted_b"]["nb_engines"] / 2, places=2)

    def test_aggressive_terms_shift_value_to_airframer(self):
        c = self.cfg
        def run(t):
            return M.payoff(c, [rr_rec(1, a=orders("airbus", [L(c, "ngsa", 2028, engine="rr_ultrafan_nb")]),
                                       rr=rr_orders([self.uf_nb(2026, terms=t)]))])
        std, agg = run("standard"), run("aggressive")
        self.assertGreater(agg["airbus"], std["airbus"])
        self.assertLess(agg["rolls_royce"], std["rolls_royce"])

    def test_t1000_upgrade(self):
        r = self.ev([rr_rec(1, rr=rr_orders(t1000=True))])["rolls_royce"]
        self.assertGreater(r["components_pv_b"]["wb_engines"], 0)
        self.assertGreater(r["components_pv_b"]["installed_base"], 0)
        self.assertAlmostEqual(r["undiscounted_b"]["capex"], -2.0 * 1.25, places=6)

    def test_validation_and_digest(self):
        c = self.cfg
        canon, errs, _ = M.validate_orders(c, [], 1, "rolls_royce", {"launch": [{"program": "uf_nb", "variant": "jv_pw", "terms": "aggressive"}],
                                                                     "t1000_upgrade": True})
        self.assertEqual(errs, [])
        self.assertEqual(canon["launch"][0], {"program": "uf_nb", "year": 2026, "terms": "aggressive", "variant": "jv_pw"})
        self.assertEqual(M.canonical_key("rolls_royce", canon), "rolls_royce|L=uf_nb/jv_pw/aggressive/2026|C=|F=t1000_upgrade:1")
        for bad in ({"launch": ["fps"]}, {"launch": [{"program": "uf_nb", "terms": "cheap"}]}, {"delay_tactics": True},
                    {"launch": [{"program": "uf_wb", "variant": "solo"}]}):
            self.assertTrue(M.validate_orders(c, [], 1, "rolls_royce", bad)[1], bad)
        flown = [rr_rec(1, a=orders("airbus", [L(c, "ngsa", 2028, engine="rr_ultrafan_nb")]), rr=rr_orders([self.uf_nb(2026)]))]
        self.assertTrue(M.validate_orders(c, flown, 2, "rolls_royce", {"cancel": ["uf_nb"]})[1])
        unused = [rr_rec(1, rr=rr_orders([self.uf_nb(2026)]))]
        self.assertEqual(M.validate_orders(c, unused, 2, "rolls_royce", {"cancel": ["uf_nb"]})[1], [])
        _, _, warns = M.validate_orders(c, [], 1, "airbus", {"launch": [{"program": "rea350", "engine": "rr_ultrafan_wb"}]})
        self.assertTrue(any("falls back" in w for w in warns))
        self.assertTrue(M.validate_orders(M.load_config("base"), [], 1, "rolls_royce", {})[1])  # inactive: not a player

    def test_supplier_stage_and_scorecard(self):
        c = self.cfg
        rep = S.supplier_stage(c, [], 1, [], "rolls_royce")
        self.assertEqual(len(rep["your_options"]), 30)
        self.assertIn("nobody launches", rep["scenarios"])
        idle = next(r for r in rep["your_options"] if r["label"] == "no new moves")
        self.assertAlmostEqual(idle["by_scenario_b"]["nobody launches"], 0.0, places=6)
        hist = [rr_rec(1, a=orders("airbus", [L(c, "ngsa", 2028, engine="rr_ultrafan_nb")]), rr=rr_orders([self.uf_nb(2026)]))]
        hist[0]["statements"] = {"rolls_royce": {"prediction": {"airbus": {"launch": [{"program": "ngsa", "engine": "rr_ultrafan_nb"}]},
                                                                 "boeing": {"launch": []}}}}
        sc = S.turn_scorecard(c, hist)
        row = next(r for r in sc["rows"] if r["side"] == "rolls_royce")
        self.assertEqual(row["prediction_accuracy"], 1.0)
        self.assertGreaterEqual(row["best_response_value_b"], row["myopic_value_b"])
        self.assertIn("rolls_royce", sc["summary"])


class PrattWhitneyTests(unittest.TestCase):
    """The second supplier player (Pratt & Whitney) and the RR-PW Joint Venture."""

    def setUp(self):
        self.cfg = M.load_config("base", {"suppliers": {"rolls_royce": {"active": True}, "pratt_whitney": {"active": True}}})
        c = self.cfg
        self.ngsa = lambda eng: orders("airbus", [L(c, "ngsa", 2028, engine=eng)])

    def rec4(self, turn=1, b=None, a=None, rr=None, pw=None, injects=()):
        r = rec(turn, b, a, injects)
        r["orders"]["rolls_royce"] = rr or M.empty_orders("rolls_royce")
        r["orders"]["pratt_whitney"] = pw or M.empty_orders("pratt_whitney")
        return r

    def pw(self, launch=(), **flags):
        return orders("pratt_whitney", list(launch), **flags)

    def test_four_players_and_status_quo(self):
        self.assertEqual(M.players(self.cfg), ("boeing", "airbus", "rolls_royce", "pratt_whitney"))
        for inj in ([], ["gtf_durability_crisis"], ["nb_demand_shock"]):
            u = M.payoff(self.cfg, [self.rec4(injects=inj), self.rec4(2)])
            for s in M.players(self.cfg):
                self.assertAlmostEqual(u[s], 0.0, places=9)

    def test_pw_engine_needs_commitment_and_ngsa_on_cfm_costs_pw(self):
        c = self.cfg
        w = M.build_world(c, [self.rec4(a=self.ngsa("pw_gtf2"))])
        self.assertEqual(w.programs["ngsa"].engine, "cfm_ducted")  # PW did not commit: fallback
        won = M.evaluate(c, M.build_world(c, [self.rec4(a=self.ngsa("pw_gtf2"), pw=self.pw([{"program": "gtf_next", "year": 2026, "terms": "standard"}]))]))
        self.assertGreater(won["pratt_whitney"]["components_pv_b"]["nb_engines"], 0)
        lost = M.evaluate(c, M.build_world(c, [self.rec4(a=self.ngsa("cfm_ducted"))]))
        self.assertLess(lost["pratt_whitney"]["components_pv_b"]["nb_engines"], 0)  # A320neo share lost at NGSA EIS

    def test_joint_venture_needs_both(self):
        c = self.cfg
        rr = orders("rolls_royce", [{"program": "uf_nb", "year": 2026, "variant": "jv_pw", "terms": "standard"}])
        alone = M.build_world(c, [self.rec4(a=self.ngsa("rr_ultrafan_nb"), rr=rr)])
        self.assertNotIn("uf_nb", alone.sup_programs)
        self.assertEqual(alone.programs["ngsa"].engine, "cfm_ducted")
        both = [self.rec4(a=self.ngsa("rr_ultrafan_nb"), rr=rr, pw=self.pw(join_rr_jv=True))]
        w = M.build_world(c, both)
        self.assertEqual(w.sup_programs["uf_nb"].partner, "pratt_whitney")
        r = M.evaluate(c, w)
        for sup in ("rolls_royce", "pratt_whitney"):  # each pays half the $8B, loaded by its own alpha
            self.assertAlmostEqual(r[sup]["undiscounted_b"]["capex"], -4.0 * (1 + c["suppliers"][sup]["alpha"]), places=6)
        self.assertGreater(r["pratt_whitney"]["components_pv_b"]["nb_engines"], -3.0)  # JV value offsets part of the lost share
        solo = [self.rec4(a=self.ngsa("rr_ultrafan_nb"), rr=orders("rolls_royce", [{"program": "uf_nb", "year": 2026, "variant": "solo"}]))]
        self.assertLess(M.evaluate(c, M.build_world(c, solo))["pratt_whitney"]["components_pv_b"]["nb_engines"],
                        r["pratt_whitney"]["components_pv_b"]["nb_engines"])

    def test_join_validation(self):
        c = self.cfg
        self.assertEqual(M.validate_orders(c, [], 1, "pratt_whitney", {"join_rr_jv": True})[1], [])
        rr_only = M.load_config("base", {"suppliers": {"pratt_whitney": {"active": True}}})
        self.assertTrue(M.validate_orders(rr_only, [], 1, "pratt_whitney", {"join_rr_jv": True})[1])  # RR not playing
        launched = [self.rec4(rr=orders("rolls_royce", [{"program": "uf_nb", "year": 2026, "variant": "solo"}]))]
        self.assertTrue(M.validate_orders(c, launched, 2, "pratt_whitney", {"join_rr_jv": True})[1])
        self.assertEqual(M.canonical_key("pratt_whitney", M.empty_orders("pratt_whitney")),
                         "pratt_whitney|L=|C=|F=gtf_upgrade:0,join_rr_jv:0")

    def test_gtf_upgrade_and_crisis(self):
        c = self.cfg
        r = M.evaluate(c, M.build_world(c, [self.rec4(pw=self.pw(gtf_upgrade=True))]))["pratt_whitney"]
        self.assertGreater(r["components_pv_b"]["nb_engines"], 0)
        self.assertGreater(r["components_pv_b"]["installed_base"], 0)
        self.assertEqual(r["upgrade_year"], 2026)

    def test_pw_stage(self):
        rep = S.supplier_stage(self.cfg, [], 1, [], "pratt_whitney")
        self.assertEqual(len(rep["your_options"]), 18)  # (1 + 2 terms)^2 x upgrade on/off
        jv = next(r for r in S.supplier_stage(self.cfg, [], 1, [], "rolls_royce")["your_options"] if "jv_pw" in r["label"])
        self.assertGreater(jv["best_case"], 0)  # a JV option assumes the partner joins


class RollsRoyceCliTests(CliBase):
    def test_three_player_turn(self):
        _, new = self.run_cli("new", "--run-id", "rr", "--turns", "2", "--suppliers", "rolls_royce")
        self.assertEqual(new["players"], ["boeing", "airbus", "rolls_royce"])
        code, err = self.run_cli("new", "--run-id", "h", "--scenario", "hist-2010-neo", "--suppliers", "rolls_royce", ok=False)
        self.assertEqual(code, 1)
        _, inj = self.run_cli("injects", "--run", "rr")
        self.assertIn("ultrafan_test_setback", [i["id"] for i in inj["eligible"]])
        self.run_cli("inject", "--run", "rr", "--none")
        _, br = self.run_cli("brief", "--run", "rr", "--side", "rolls_royce")
        self.assertIn("your_levers_this_turn", br)
        _, opt = self.run_cli("options", "--run", "rr", "--side", "rolls_royce")
        self.assertTrue(opt["your_options"])
        orders_in = {"boeing": {}, "airbus": {"launch": [{"program": "ngsa", "year": 2028, "engine": "rr_ultrafan_nb"}]},
                     "rolls_royce": {"launch": [{"program": "uf_nb", "variant": "solo"}], "rationale": "RR-PRIVATE",
                                     "disclose": ["We will build a narrowbody UltraFan."]}}
        code, res = self.run_cli("adjudicate", "--run", "rr", stdin={"boeing": {}, "airbus": {}}, ok=False)
        self.assertEqual((code, res["status"]), (2, "invalid"))  # Rolls-Royce orders missing
        code, res = self.run_cli("adjudicate", "--run", "rr", "--expect-digest", "boeing=0,airbus=0,rolls_royce=0",
                                 stdin=orders_in, ok=False)
        self.assertEqual(code, 1)
        _, res = self.run_cli("adjudicate", "--run", "rr", stdin=orders_in)
        self.assertIn("rolls_royce", res["projection"])
        self.assertEqual(res["warnings"].get("airbus", []), [w for w in res["warnings"].get("airbus", []) if "falls back" not in w])
        _, ba = self.run_cli("brief", "--run", "rr", "--side", "airbus")
        text = json.dumps(ba)
        self.assertIn("We will build a narrowbody UltraFan.", text)
        self.assertNotIn("RR-PRIVATE", text)
        self.assertEqual(ba["programs"][0]["engine"], "rr_ultrafan_nb")
        _, wi = self.run_cli("whatif", "--run", "rr", "--side", "rolls_royce", stdin={"rolls_royce": {"2": {"t1000_upgrade": True}}})
        self.assertGreater(wi["rolls_royce"]["change_vs_current_projection_b"], -5)
        self.run_cli("inject", "--run", "rr", "--id", "rr_durability_crisis")
        _, res = self.run_cli("adjudicate", "--run", "rr", stdin={"boeing": {}, "airbus": {}, "rolls_royce": {}})
        self.assertTrue(res["game_complete"])
        _, sc = self.run_cli("scorecard", "--run", "rr")
        self.assertEqual({r["side"] for r in sc["rows"]}, {"boeing", "airbus", "rolls_royce"})
        _, md = self.run_cli("report", "--run", "rr", "--format", "md")
        self.assertIn("Supplier engine programs", md)
        self.assertIn("Rolls-Royce", md)
        self.run_cli("new", "--run-id", "two", "--turns", "1")
        code, _ = self.run_cli("brief", "--run", "two", "--side", "rolls_royce", ok=False)
        self.assertEqual(code, 1)
        _, inj = self.run_cli("injects", "--run", "two")
        self.assertNotIn("ultrafan_test_setback", [i["id"] for i in inj["eligible"]])

    def test_four_player_turn_with_joint_venture(self):
        _, new = self.run_cli("new", "--run-id", "four", "--turns", "1", "--suppliers", "rolls_royce,pratt_whitney")
        self.assertEqual(new["players"], ["boeing", "airbus", "rolls_royce", "pratt_whitney"])
        self.run_cli("inject", "--run", "four", "--id", "gtf_durability_crisis")
        _, br = self.run_cli("brief", "--run", "four", "--side", "pratt_whitney")
        self.assertIn("join_rr_jv", [f["flag"] for f in br["your_levers_this_turn"]["flags"]])
        _, opt = self.run_cli("options", "--run", "four", "--side", "pratt_whitney")
        self.assertTrue(opt["your_options"])
        orders_in = {"boeing": {}, "airbus": {"launch": [{"program": "ngsa", "year": 2028, "engine": "rr_ultrafan_nb"}]},
                     "rolls_royce": {"launch": [{"program": "uf_nb", "variant": "jv_pw"}]},
                     "pratt_whitney": {"join_rr_jv": True, "gtf_upgrade": True}}
        _, res = self.run_cli("adjudicate", "--run", "four", stdin=orders_in)
        self.assertEqual(set(res["projection"]), {"boeing", "airbus", "rolls_royce", "pratt_whitney"})
        _, md = self.run_cli("report", "--run", "four", "--format", "md")
        self.assertIn("Rolls-Royce + Pratt & Whitney", md)
        _, sc = self.run_cli("scorecard", "--run", "four")
        self.assertEqual(len(sc["rows"]), 4)


if __name__ == "__main__":
    unittest.main()
