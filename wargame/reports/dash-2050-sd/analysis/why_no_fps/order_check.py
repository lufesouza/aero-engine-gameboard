import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import why_fps as W   # reuses states and helpers (runs its main body once; output ignored)
SD, M = W.SD, W.M
REAL = W.REAL
res = {}
try:
    # (a) from the neutral case, switch on only Boeing's real capacity (fps ramp, MAX 57, 100 cap)
    SD.boeing_capacity = REAL[0]
    SD.airbus_capacity = W.unlimited_after_eis("ngsa", None)
    SD.demand, SD.firm_backlog = (lambda y: 2000.0), (lambda: (0.0, 0.0))
    res["neutral + Boeing's real capacity only"] = W.item(W.S_F10)[0]
    # (b) the full game but Airbus's NGSA instant and unlimited after EIS (no Airbus ceiling, no transition dip)
    W.restore()
    SD.airbus_capacity = W.unlimited_after_eis("ngsa", lambda s, y: (SD.a320_full(), 0.0))
    res["full game, but Airbus unlimited after NGSA EIS"] = W.item(W.S_F10)[0]
    # (c) the full game, Boeing's fps instant and unlimited after EIS (MAX path before)
    W.restore()
    SD.boeing_capacity = W.unlimited_after_eis("fps", lambda s, y: (SD.max_path(y), 0.0))
    res["full game, but fps instant and unlimited after EIS"] = W.item(W.S_F10)[0]
finally:
    W.restore()
res["full game"] = W.item(W.S_F10)[0]
print(json.dumps({k: round(v, 2) for k, v in res.items()}, indent=1))
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "order_check.json"), "w"), indent=1)
