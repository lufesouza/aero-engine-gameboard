"""Differential test: the pack's runner (engine/run_game.py, Company.play) against the original round script
(wargame/dashgame/workflows/exco_round.js) on scripted seat answers, for every branch the protocol has: binding vetoes,
red-line flags, Board vetoes with the step-7 merge, a confirm veto, fail-closed and missing steps, standing supply plans.

  python3 test_runner_vs_js.py      (from anywhere; needs node and a built pack)
"""
import copy
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
EXPORT = os.path.dirname(HERE)
ENGINE = os.path.join(EXPORT, "dash-2050-cons-llm", "engine")
JS = os.path.join(EXPORT, "..", "dashgame", "workflows", "exco_round.js")
sys.path.insert(0, ENGINE)
import run_game as RG  # noqa: E402

MAP = {"guidance": "board:guidance", "frame": "frame", "test_cfo": "test:cfo", "test_ops": "test:ops", "decide": "decide",
       "veto_cfo": "veto:cfo", "veto_ops": "veto:ops", "revise": "revise", "board_review": "board:review",
       "board_revise": "board:revise", "board_confirm": "board:confirm"}


def dec(orders, stmt="statement"):
    return {"orders": orders, "other_moves": [], "public_statement": stmt, "rationale": "r", "memo_weighing": {"cfo": "c", "ops": "o"},
            "expected_scenario": "e", "best_grid_plan_in_expected_scenario": "b", "premium_b": 0, "premium_reason": "p",
            "objective_note": "n", "predictions": "p", "expected_pv_b": 0}


def memo(orders):
    return {"tests": [], "recommended_orders": orders, "vetoes": [], "would_change_mind_if": "w", "memo": "m"}


CONCUR = {"concur": True, "red_line_breach": False, "note": "ok"}
GUIDE = {"priorities": [], "risk_appetite": "low", "expect_to_see": "x", "would_approve": [], "would_veto": [], "recommendations": [], "evidence_ids": []}
FRAME = {"question": "q", "situation": "s", "levers_in_play": [], "options_to_test": [], "red_lines": [], "asks_cfo": "a", "asks_ops": "a", "initial_lean": "l", "evidence_ids": []}
B0 = {"fps": "hold", "fps_engine_code": None, "rate_737": "hold", "re787": "hold", "fps_site": "new_site"}
A0 = {"ngsa": "hold", "ngsa_engine_code": None, "rea350": "hold", "delay_tactics": "none", "a320_plan": "alt"}


def review(items, recs=None):
    return {"items": [{"order_field": f, "value": "v", "decision": d, "ground": "g", "acceptable_alternatives": alts} for f, d, alts in items],
            "recommendations": recs or [], "overall": "partial", "note": "n"}


def base(side, orders):
    return {"guidance": GUIDE, "frame": FRAME, "test_cfo": memo(orders), "test_ops": memo(orders), "decide": dec(orders),
            "veto_cfo": CONCUR, "veto_ops": CONCUR}


def scen():
    S = []
    fps10 = dict(B0, fps="launch_10yr", fps_engine_code=3)
    # 1 binding CFO veto, revision to hold
    a = base("boeing", fps10)
    a["veto_cfo"] = {"concur": False, "veto": {"ground": "buffer", "binding": True}, "red_line_breach": False, "note": "n"}
    a["revise"] = dec(B0, "revised")
    S.append(("binding veto", "boeing", a))
    # 2 red-line flag only; revision keeps the order; Board approves
    a = base("boeing", fps10)
    a["veto_ops"] = {"concur": True, "red_line_breach": True, "red_line": "H4", "note": "n"}
    a["revise"] = dec(fps10, "kept")
    a["board_review"] = review([("fps", "approve", [])])
    S.append(("red-line flag", "boeing", a))
    # 3 Board vetoes fps, approves re787; the revise also tries to change re787 (ignored by the merge); confirm approves
    d = dict(B0, fps="launch_7yr", fps_engine_code=5, re787="launch")
    a = base("boeing", d)
    a["board_review"] = review([("fps", "veto", ["launch_10yr", "hold"]), ("re787", "approve", [])])
    a["board_revise"] = dec(dict(B0, fps="launch_10yr", fps_engine_code=7, re787="hold"), "after board")
    a["board_confirm"] = review([("fps", "approve", [])])
    S.append(("Board veto, merge, confirm", "boeing", a))
    # 4 same, the confirm vetoes again: fps and its code revert
    a = copy.deepcopy(a)
    a["board_confirm"] = review([("fps", "veto", [])])
    S.append(("confirm veto", "boeing", a))
    # 5 Board review missing: fail closed
    a = base("boeing", d)
    a["board_review"] = None
    S.append(("review missing", "boeing", a))
    # 6 Board revise missing: vetoed items revert
    a = base("boeing", d)
    a["board_review"] = review([("fps", "veto", ["hold"]), ("re787", "approve", [])])
    a["board_revise"] = None
    S.append(("board revise missing", "boeing", a))
    # 7 frame missing: the company holds
    a = base("boeing", d)
    a["frame"] = None
    S.append(("frame missing", "boeing", a))
    # 8 standing Airbus plan alt: keeping it is not a Board item; changing NGSA is
    a = base("airbus", dict(A0, ngsa="launch", ngsa_engine_code=6))
    a["board_review"] = review([("ngsa", "approve", [])])
    S.append(("standing plan kept", "airbus", a))
    a = base("airbus", dict(A0, a320_plan="base"))
    a["board_review"] = review([("a320_plan", "veto", ["alt"])])
    a["board_revise"] = dec(dict(A0, a320_plan="alt"))
    S.append(("standing plan change vetoed, back to standing", "airbus", a))
    # 9 guidance missing, a test memo missing, a veto check missing
    a = base("pratt_whitney", {"gtf2_solo": "launch_if_selected", "jv_with_rr": "hold"})
    a["guidance"] = None
    a["test_cfo"] = None
    a["veto_ops"] = None
    a["board_review"] = review([("gtf2_solo", "approve", [])])
    S.append(("guidance, memo and veto check missing", "pratt_whitney", a))
    # 10 soft veto marked binding false: no revision
    a = base("airbus", dict(A0, rea350="launch"))
    a["veto_cfo"] = {"concur": False, "veto": {"ground": "peak cash", "binding": False}, "red_line_breach": False, "note": "n"}
    a["board_review"] = review([("rea350", "veto", ["hold"])])
    a["board_revise"] = dec(dict(A0, rea350="hold"), "held")
    S.append(("non-binding veto, Board veto to the default", "airbus", a))
    return S


class Scripted:
    def __init__(self, answers):
        self.a = answers

    def answer(self, n, side, step, schema=None):
        x = self.a.get(step, "MISSING")
        if x == "MISSING":
            raise KeyError(step)
        return copy.deepcopy(x)


def py_result(side, answers, plans, tmp):
    RG.RUNS = tmp
    args = type("A", (), {"history": "none", "persona": "full", "json_retries": 0})()
    c = RG.Company("t", 2, side, RG.Mock(None), args, plans)
    c.llm = Scripted(answers)
    RG_isinstance = RG.Company.call

    def call(self, key, seat, step, task, schema, note_key):
        return self.llm.answer(self.n, self.side, key)
    RG.Company.call = call
    try:
        return c.play()
    finally:
        RG.Company.call = RG_isinstance


def js_result(side, answers, plans, tmp):
    js_answers = {"%s:%s" % (side, MAP[k]): v for k, v in answers.items()}
    sc = {"args": {"run": "t", "round": 2, "year": 2035, "sides": [side], "plans": plans}, "answers": js_answers}
    p = os.path.join(tmp, "sc.json")
    json.dump(sc, open(p, "w"))
    r = subprocess.run(["node", os.path.join(HERE, "js_round.js"), JS, p], capture_output=True, text=True, check=True)
    out = json.loads(r.stdout)["sides"][side]
    if out is None:
        return None
    final = dict(out.get("final") or {})
    final["orders"] = out.get("final_orders")
    final["exco"] = {k: out.get(k) for k in ("binding_vetoes", "red_line_flags", "board_items", "board_vetoed", "board_reverted")}
    return final


def main():
    plans = {"boeing": {"fps_site": "new_site"}, "airbus": {"a320_plan": "alt"}}
    bad = 0
    for name, side, ans in scen():
        with tempfile.TemporaryDirectory() as tmp:
            py = py_result(side, ans, plans, tmp)
            js = js_result(side, ans, plans, tmp)
        keys = ("binding_vetoes", "red_line_flags", "board_items", "board_vetoed", "board_reverted")
        pv = None if py is None else (py["orders"], py.get("public_statement"), {k: sorted((py["exco"].get(k) or [])) for k in keys})
        jv = None if js is None else (js["orders"], js.get("public_statement"), {k: sorted((js["exco"].get(k) or [])) for k in keys})
        same = pv == jv
        bad += not same
        print("%-48s %s" % (name, "same" if same else "DIFFERENT\n  py %s\n  js %s" % (pv, jv)))
    print("ALL SCENARIOS MATCH THE ORIGINAL ROUND SCRIPT" if not bad else "%d SCENARIO(S) DIFFER" % bad)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
