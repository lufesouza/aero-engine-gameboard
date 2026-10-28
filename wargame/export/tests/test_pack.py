"""End-to-end checks of the built pack (run after build_llm_pack.py):
1. the full zip's engine self-test passes, and prints nothing about the original game;
2. the runner, fed the original agents' answers (--provider replay), reproduces the original game exactly: every
   company's orders and value each round, and all 24 briefs and bulletins;
3. the runner's round logic matches the original round script on scripted answers (test_runner_vs_js.py);
4. the runner's API path works against a fake OpenAI-compatible server (tools, JSON in prose, a format retry);
5. the players' zip has no spoilers and refuses the self-test and the replay.

  python3 test_pack.py
"""
import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
EXPORT = os.path.dirname(HERE)
SIDES = ["boeing", "airbus", "cfm", "pratt_whitney", "rolls_royce"]


def run(cmd, cwd, **kw):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, **kw)
    return r.returncode, r.stdout + r.stderr


def main():
    ok = True
    with tempfile.TemporaryDirectory() as tmp:
        zipfile.ZipFile(os.path.join(EXPORT, "dash-2050-cons-llm.zip")).extractall(tmp)
        pack = os.path.join(tmp, "dash-2050-cons-llm")
        # 1
        code, out = run([sys.executable, "engine/play.py", "selftest"], pack)
        quiet = all(w not in out for w in ("NGSA", "launched", "+14.09", "-28.04"))
        print("1 self-test:", "PASS" if code == 0 else "FAIL", "| prints nothing about the game:", quiet)
        ok &= code == 0 and quiet
        # 2
        code, out = run([sys.executable, "engine/run_game.py", "--game", "replaycheck", "--provider", "replay"], pack)
        eng = os.path.join(pack, "engine")
        ref = json.load(open(os.path.join(eng, "reference", "played_orders.json"), encoding="utf-8"))
        same = code == 0
        for n in "1234":
            rec = json.load(open(os.path.join(eng, "runs", "replaycheck", "record_r%s.json" % n), encoding="utf-8"))
            for s in SIDES:
                same &= rec["orders"][s] == ref["rounds"][n]["orders_file"][s]["orders"]
                same &= abs(rec["value"][s]["pv_delta"] - ref["rounds"][n]["value"][s]) < 1e-9
            for part in SIDES + ["bulletin"]:
                a = open(os.path.join(eng, "runs", "replaycheck", ("bulletin_r%s.md" % n) if part == "bulletin" else ("brief_r%s_%s.md" % (n, part))), encoding="utf-8").read()
                b = open(os.path.join(eng, "reference", "briefs", "round%s_%s.md" % (n, part)), encoding="utf-8").read()
                same &= a == b
        print("2 runner replay reproduces the original game:", same)
        ok &= same
        # 4
        with socket.socket() as so:
            so.bind(("127.0.0.1", 0))
            port = so.getsockname()[1]
        srv = subprocess.Popen([sys.executable, os.path.join(HERE, "fake_llm_server.py"), str(port), eng],
                               stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        time.sleep(1.5)
        env = dict(os.environ, LLM_API_KEY="x", NO_PROXY="127.0.0.1", no_proxy="127.0.0.1")
        code, out = run([sys.executable, "engine/run_game.py", "--game", "apitest", "--base-url", "http://127.0.0.1:%d/v1" % port,
                         "--model", "fake", "--rounds", "1", "--companies", "boeing,pratt_whitney"], pack, env=env)
        srv.terminate()
        calls = os.listdir(os.path.join(eng, "runs", "apitest", "calls"))
        api = code == 0 and "round 1 2030 adjudicated" in out and "r1_boeing_frame_1.json" in calls
        print("4 API path (tools, JSON in prose, retry):", api)
        ok &= api
    # 3
    code, out = run([sys.executable, os.path.join(HERE, "test_runner_vs_js.py")], HERE)
    print("3 runner logic = original round script:", code == 0, "|", out.strip().splitlines()[-1])
    ok &= code == 0
    # 5
    with tempfile.TemporaryDirectory() as tmp:
        z = zipfile.ZipFile(os.path.join(EXPORT, "dash-2050-cons-llm-players.zip"))
        names = z.namelist()
        clean = not any("RESULTS_AS_PLAYED" in n or "/engine/reference/" in n for n in names)
        z.extractall(tmp)
        pack = os.path.join(tmp, "dash-2050-cons-llm")
        c1, o1 = run([sys.executable, "engine/play.py", "selftest"], pack)
        c2, o2 = run([sys.executable, "engine/run_game.py", "--game", "x", "--provider", "replay"], pack)
        refuse = c1 != 0 and "full pack" in o1 and c2 != 0 and "full pack" in o2
        print("5 players' pack has no spoilers:", clean, "| refuses self-test and replay:", refuse)
        ok &= clean and refuse
    print("ALL PACK CHECKS PASSED" if ok else "SOME PACK CHECKS FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
