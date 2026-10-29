"""A fake OpenAI-compatible chat server for testing engine/run_game.py's API path: it calls the seat's tools first
(read_file on its profile, a calculation), then answers in prose with the JSON in a fence; the first framing note of
each company comes back malformed, to exercise the format retry. Answers hold everything (valid per the step's format).

  python3 fake_llm_server.py <port> <path to engine/>
"""
import json
import os
import re
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.insert(0, sys.argv[2])
import run_game as RG  # noqa: E402

COMPANY = {"Boeing": "boeing", "Airbus": "airbus", "CFM/GE": "cfm", "Pratt & Whitney": "pratt_whitney", "Rolls-Royce": "rolls_royce"}
STEP = {"guidance": "guidance", "frame": "frame", "test": "test", "decide": "decide", "veto_check": "veto", "revise": "decide",
        "review": "review", "board_revise": "decide", "confirm": "review"}
SEEN = {"frame": set(), "calls": 0, "tools": 0}


def side_of(msgs):
    u = msgs[1]["content"]
    m = re.search(r"You are .*? of (Boeing|Airbus|CFM/GE|Pratt & Whitney|Rolls-Royce)\.", u) or \
        re.search(r"(Boeing|Airbus|GE Aerospace|RTX|Rolls-Royce)", u)
    k = m.group(1)
    return {"GE Aerospace": "cfm", "RTX": "pratt_whitney"}.get(k, COMPANY.get(k))


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def fail(self, code, msg):
        out = json.dumps({"error": {"message": msg}}).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        msgs = body["messages"]
        # FAKE_FAIL=<step>:<company>: that step gets HTTP 400 while the file FAKE_FAIL_FLAG exists
        ff = os.environ.get("FAKE_FAIL")
        if ff and os.path.exists(os.environ.get("FAKE_FAIL_FLAG", "")):
            step_, side_ = ff.split(":")
            if ("Your step: **%s**" % step_) in msgs[1]["content"] and side_of(msgs) == side_:
                return self.fail(400, "bad request (simulated)")
        # FAKE_ANTHROPIC=1: tool history without tool definitions is refused, as Anthropic's API does
        if os.environ.get("FAKE_ANTHROPIC") and not body.get("tools") and any(m.get("role") == "tool" or m.get("tool_calls") for m in msgs):
            return self.fail(400, "Requests which include tool_use or tool_result blocks must define tools.")
        SEEN["calls"] += 1
        user = msgs[1]["content"]
        step = re.search(r"Your step: \*\*([a-z_]+)\*\*", user).group(1)
        side = side_of(msgs)
        kind = STEP[step]
        sch = RG.SCHEMAS[kind] if kind in ("guidance", "frame", "veto", "review") else RG.SCHEMAS[kind][side]
        has_tool_reply = any(m.get("role") == "tool" for m in msgs)
        if body.get("tools") and not has_tool_reply:
            SEEN["tools"] += 1
            msg = {"role": "assistant", "content": "", "tool_calls": [
                {"id": "c1", "type": "function", "function": {"name": "read_file", "arguments": json.dumps({"path": "profile.md"})}},
                {"id": "c2", "type": "function", "function": {"name": "calculate", "arguments": json.dumps({"expression": "0.5*(-4.39)+0.5*(-4.80)"})}}]}
        else:
            tool_out = [m["content"] for m in msgs if m.get("role") == "tool"]
            assert not body.get("tools") or tool_out, "tools were offered but no tool reply came back"
            if tool_out:
                assert "error" not in tool_out[0][:20], tool_out[0][:200]
                assert abs(float(tool_out[1]) - (-4.595)) < 1e-9, tool_out[1]
            ans = RG.Mock(None).answer(1, side, step, sch)
            if step == "frame" and side not in SEEN["frame"] and not any("does not match the format" in (m.get("content") or "") for m in msgs):
                SEEN["frame"].add(side)
                ans = {k: v for k, v in ans.items() if k != "question"}       # malformed on purpose
            msg = {"role": "assistant", "content": "Here is my answer.\n\n```json\n" + json.dumps(ans) + "\n```\nDone."}
        out = json.dumps({"choices": [{"message": msg}]}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)


HTTPServer(("127.0.0.1", int(sys.argv[1])), H).serve_forever()
