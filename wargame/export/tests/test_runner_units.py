"""Unit checks of engine/run_game.py's helpers (run after build_llm_pack.py): the seats' file view (isolation), JSON
extraction, the format check, the tool-history flattening, and the shared tools flag under concurrent fallbacks.

  python3 test_runner_units.py
"""
import json
import os
import shutil
import sys
import tempfile
import threading

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(os.path.dirname(HERE), "dash-2050-cons-llm", "engine")
sys.path.insert(0, ENGINE)
import run_game as RG  # noqa: E402

bad = []


def ok(cond, what):
    print(("ok   " if cond else "FAIL ") + what)
    if not cond:
        bad.append(what)


# 1. the file view
tmp = tempfile.mkdtemp()
RG.RUNS = tmp
run = os.path.join(tmp, "g", "players", "boeing")
os.makedirs(os.path.join(run, "exco"))
for f in ("rules.md", "round1.md", "round2.md", "round3.md", "my_orders_r1.json", "my_orders_r2.json",
          "exco/r1_decision.md", "exco/r2_test_cfo.md", "exco/r2_frame.json"):
    open(os.path.join(run, f), "w").write(f)
os.makedirs(os.path.join(tmp, "g", "players", "airbus"))
open(os.path.join(tmp, "g", "players", "airbus", "round2.md"), "w").write("AIRBUS PRIVATE")
F = RG.Files("g", "boeing", 2)
opened = ["rules.md", "round1.md", "round2.md", "my_orders_r1.json", "exco/r1_decision.md", "./round2.md",
          "exco//r1_decision.md", "/tmp/wargame-boeing/dash-2050/round2.md", "profile.md", "companies/boeing/profile.md",
          "executives/teams.md", "x/../rules.md"]
closed = ["round3.md", "./round3.md", "x/../round3.md", "my_orders_r2.json", "./my_orders_r2.json", "exco/r2_test_cfo.md",
          "./exco/r2_test_cfo.md", "exco/./r2_test_cfo.md", "exco//r2_test_cfo.md", "exco/../exco/r2_frame.json",
          "exco\\r2_test_cfo.md", "../airbus/round2.md", "../../../reference/played_orders.json", "/etc/passwd",
          "../../../../RESULTS_AS_PLAYED.md", "../../../dashgame/model.py", "../../../../companies/airbus/profile.md"]
for p in opened:
    try:
        F.read(p)
        ok(True, "open:   %s" % p)
    except ValueError as e:
        ok(False, "open:   %s (%s)" % (p, e))
for p in closed:
    try:
        out = F.read(p)
        ok(False, "closed: %s (read %r)" % (p, out[:40]))
    except ValueError:
        ok(True, "closed: %s" % p)
lst = F.read("exco")
ok("r1_decision.md" in lst and "r2_" not in lst, "the exco listing shows earlier rounds only")
root = F.read("")
ok("round3.md" not in root and "my_orders_r2.json" not in root and "profile.md" in root, "the root listing: run folder (open files) and company files")
os.symlink("/etc", os.path.join(run, "exco", "r1_link"))
try:
    F.read("exco/r1_link/passwd")
    ok(False, "a symlink out of the folder is closed")
except ValueError:
    ok(True, "a symlink out of the folder is closed")
shutil.rmtree(tmp)

# 2. JSON extraction
ok(RG.extract_json('<think>{"a": 1}</think>Answer: {"a": 2}') == {"a": 2}, "a <think> draft is ignored")
ok(RG.extract_json('Draft:\n```json\n{"a": 1}\n```\nFinal:\n```json\n{"a": 2}\n```') == {"a": 2}, "the last fenced block wins")
ok(RG.extract_json([{"type": "text", "text": '{"a": 3}'}]) == {"a": 3}, "content as a list of parts")
ok(RG.extract_json('text {"s": "a \\"quoted\\" }"} end') == {"s": 'a "quoted" }'}, "escaped quotes and braces in strings")
ok(RG.extract_json("no json here") is None, "no object: None")

# 3. the format check
S = RG.SCHEMAS
d = {"orders": {"fps": "launch_10yr", "fps_engine_code": True, "rate_737": "hold", "re787": "hold", "fps_site": "new_site"},
     "other_moves": [], "public_statement": "", "rationale": "", "memo_weighing": {"cfo": "", "ops": ""}, "expected_scenario": "",
     "best_grid_plan_in_expected_scenario": "", "premium_b": 0, "premium_reason": "", "objective_note": "", "predictions": "", "expected_pv_b": 0}
ok(any("fps_engine_code" in e for e in RG.check(S["decide"]["boeing"], d)), "JSON true is not engine code 1")
d["orders"]["fps_engine_code"] = 7
ok(RG.check(S["decide"]["boeing"], d) == [], "a valid decision passes")
d["orders"]["fps_engine"] = 7
ok(any("unknown order field" in e for e in RG.check(S["decide"]["boeing"], d)), "an unknown order field is refused")
v = RG.clean(S["veto"], {"concur": True, "veto": None, "red_line_breach": False, "red_line": None, "note": "n"})
ok(RG.check(S["veto"], v) == [] and "veto" not in v, "a null optional field counts as absent")

# 4. flattening tool history for a call without tools
msgs = [{"role": "system", "content": "s"}, {"role": "user", "content": "u"},
        {"role": "assistant", "content": "", "tool_calls": [{"id": "1", "type": "function", "function": {"name": "read_file", "arguments": "{}"}}]},
        {"role": "tool", "tool_call_id": "1", "content": "file text"}]
fl = RG.OpenAICompatible._flatten(msgs)
ok(all(m["role"] in ("system", "user", "assistant") and "tool_calls" not in m for m in fl), "flattened history has no tool messages")

# 5. the shared tools flag stays on under concurrent fallbacks
A = type("A", (), dict(base_url="http://x", api_key_env="NONE", no_tools=False, json_mode="auto", seat_model=None, url_query=None,
                       model="m", temperature=None, max_tokens=None, max_tokens_field="max_tokens", extra_body=None, max_tool_calls=0,
                       auth_header="Authorization", auth_prefix="Bearer ", retries=0, timeout=5))()
P = RG.OpenAICompatible(A)
seen = []


def fake_post(body):
    seen.append("tools" in body)
    if "tools" in body:
        return {"choices": [{"message": {"content": "", "tool_calls": [{"id": "c", "function": {"name": "calculate", "arguments": '{"expression": "1+1"}'}}]}}]}
    return {"choices": [{"message": {"content": '{"x": 1}'}}]}


P._post = fake_post
ts = [threading.Thread(target=P.complete, args=([{"role": "system", "content": "s"}, {"role": "user", "content": "u"}], "ceo", None, True)) for _ in range(8)]
[t.start() for t in ts]
[t.join() for t in ts]
ok(P.tools_ok, "the shared tools flag is still on after 8 concurrent tool-budget fallbacks")
print("ALL UNIT CHECKS PASSED" if not bad else "%d UNIT CHECK(S) FAILED" % len(bad))
sys.exit(1 if bad else 0)
