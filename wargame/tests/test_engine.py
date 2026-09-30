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


class CliTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
