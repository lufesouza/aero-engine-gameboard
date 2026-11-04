"""Build dash_2050_emb.html: the MAX phase-out game replayed with Embraer as a sixth player (its new narrowbody with
Team Korea, in service four years after launch: slightly better than the 737 MAX and A320neo, worse than fps or NGSA)
and political terms in the payoffs. Boeing's financials, the market by maker, how Boeing, Airbus and Embraer decided
each round, what Embraer's choice did, the politics, and the comparison with the previous game (dash-2050-phaseout).

Reads data/emb.json (extract_emb.py), data/what_if.json (what_if.py) and the round records under record/
(exco_result_rN.json). Every figure on the page comes from those files.

  python3 make_emb_html.py [out.html]
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050-obj"))
import page_kit as K  # noqa: E402

esc = K.esc
J = lambda n: json.load(open(os.path.join(HERE, "data", n)))
D = J("emb.json")
C, P = D["run"], D["prev"]
W = J("what_if.json") if os.path.exists(os.path.join(HERE, "data", "what_if.json")) else None
RECDIR = os.environ.get("EMB_RECORD", os.path.join(HERE, "record"))
REC = lambda n: json.load(open(os.path.join(RECDIR, "exco_result_r%d.json" % n)))["sides"]
SIDES = C["sides"]
NAME = {"boeing": "Boeing", "airbus": "Airbus", "cfm": "CFM/GE", "pratt_whitney": "Pratt & Whitney",
        "rolls_royce": "Rolls-Royce", "embraer": "Embraer"}
EMB = "embraer" in SIDES
YEARS = [r["year"] for r in C["rounds"]]
NR = len(C["rounds"])
FIN = {r["year"]: r for r in C["boeing_fin"]}
PFIN = {r["year"]: r for r in P["boeing_fin"]}
MK = {r["year"]: r for r in C["market"]}
PMK = {r["year"]: r for r in P["market"]}
KEY = [2030, 2035, 2040, 2045, 2050, 2055, 2060]
EMB_OPT = C["options"].get("embraer_player", {})
POL = C["options"].get("politics", {})
DEFAULTS = {"hold", None, "none", "new_site", "base"}
EMB_DLV = EMB and any(r["embraer"] > 0.5 for r in C["market"])      # Embraer delivered anything in the final state
# Played-path values (what_if.py, model.played_path): the record values each round as a decision, so its round-4
# value counts the political exit cost from 2050; the played path carried 2045-49 with no fps and counts it from
# 2045. The page reports the played path; only Boeing's exit-cost line may differ from the record.
REC_VALUE = {r["round"]: dict(r["value"]) for r in C["rounds"]}
if W and W.get("played_path"):
    for r, pp in zip(C["rounds"], W["played_path"]):
        assert r["round"] == pp["round"]
        for s in SIDES:
            assert s == "boeing" or abs(pp["value"][s] - r["value"][s]) < 1e-9, (s, r["round"])
        old, new = r["bridge"]["boeing"], pp["bridge"]["boeing"]
        assert all(abs(old.get(k, 0.0) - new.get(k, 0.0)) < 1e-9 for k in set(old) | set(new) if k != "political_exit_cost")
        r["value"]["boeing"] = pp["value"]["boeing"]
        r["bridge"]["boeing"] = new
# Embraer launch cells the briefs cut short (data/grid_recheck.json, recheck_grids.py): the full 20-year window
RECHECK = json.load(open(os.path.join(HERE, "data", "grid_recheck.json"))) if os.path.exists(os.path.join(HERE, "data", "grid_recheck.json")) else {"moved": []}
assert all(m["side"] == "embraer" for m in RECHECK["moved"]), "a non-Embraer cell moved"
FULLWIN = {(m["round"], m["plan"], m["column"]): m["now"] for m in RECHECK["moved"]}


def b(v, dp=2, sign=True):
    return K.usd(v, dp, sign and K.rnd(v, dp) != 0)


def bp(v, dp=2, sign=True):
    return re.sub(r"<[^>]+>", "", b(v, dp, sign))


def n0(v):
    return f"{K.rnd(v or 0.0, 0):,.0f}"


def pc(v, dp=1):
    return f"{K.rnd(100 * (v or 0.0), dp):.{dp}f}%"


CODES = [(r"`?fps:\s*launch_10yr`?", "the 10-year fps"), (r"`?fps:\s*launch_7yr`?", "the 7-year fps"),
         (r"`?fps:\s*launch_via_embraer`?", "the fps via Embraer"), (r"`?fps:\s*hold`?", "fps held"), (r"`?fps:\s*cancel`?", "fps cancelled"),
         (r"`?re787:\s*launch`?", "the 787 Re-engine"), (r"`?re787:\s*hold`?", "787 held"), (r"`?rate_737:\s*increase`?", "the 737 rate increase"),
         (r"`?rate_737:\s*hold`?", "737 rate held"), (r"`?rea350:\s*launch`?", "the A350 Re-engine"), (r"`?rea350:\s*hold`?", "A350 held"),
         (r"`?ngsa:\s*launch`?", "the NGSA launch"), (r"`?ngsa:\s*hold`?", "NGSA continuing"), (r"`?ngsa:\s*cancel`?", "cancelling NGSA"),
         (r"`?a320_plan:\s*alt`?", "the A320 Alt plan"), (r"`?a320_plan:\s*base`?", "the A320 base plan"),
         (r"`?delay_tactics:\s*(none|bottleneck|poaching|both)`?", "Delay Tactics (\\1)"), (r"`?enb:\s*launch`?", "the Embraer launch"),
         (r"`?enb:\s*hold`?", "Embraer holding"), (r"`?jv_with_(?:pw|rr):\s*commit`?", "the Joint Venture commitment"),
         (r"`?jv_with_(?:pw|rr):\s*hold`?", "no Joint Venture move"), (r"`?jv_with_(?:pw|rr):\s*withdraw`?", "withdrawing from the Joint Venture"),
         (r"`?gtf2_solo:\s*launch_if_selected`?", "GTF2 if selected"), (r"`?gtf2_solo:\s*hold`?", "GTF2 held"),
         (r"`?ultrafan_nb_solo:\s*launch_if_selected`?", "UltraFan NB if selected"), (r"`?ultrafan_nb_solo:\s*hold`?", "UltraFan NB held"),
         (r"`?fps_engine_code`?", "fps engine code"), (r"`?ngsa_engine_code`?", "NGSA engine code"), (r"`?fps_site`?", "fps site"),
         (r"\bnew_site\b", "new sites"), (r"\bngsa\b", "NGSA"), (r"`?premium_b`?", "premium"), (r"`?board_response`?", "Board response"),
         (r"`?launch_if_selected`?", "launch if selected"), (r"`?launch_10yr`?", "10-year launch"), (r"`?launch_7yr`?", "7-year launch"),
         (r"`?launch_via_embraer`?", "launch via Embraer"), (r"`?(re787|rea350|rate_737|delay_tactics|a320_plan|jv_with_pw|jv_with_rr|gtf2_solo|ultrafan_nb_solo|ultrafan_wb|t1000_upgrade|partner_embraer|lobby_emissions|open_fan|ducted|enb)`?",
                                                                                  lambda m: {"re787": "787 Re-engine", "rea350": "A350 Re-engine", "rate_737": "737 rate", "delay_tactics": "Delay Tactics",
                                                                                             "a320_plan": "A320 plan", "jv_with_pw": "Joint Venture", "jv_with_rr": "Joint Venture", "gtf2_solo": "GTF2",
                                                                                             "ultrafan_nb_solo": "UltraFan NB", "ultrafan_wb": "UltraFan WB", "t1000_upgrade": "Trent 1000 upgrade",
                                                                                             "partner_embraer": "Embraer partnership", "lobby_emissions": "emissions lobbying", "open_fan": "Open Fan",
                                                                                             "ducted": "Ducted engine", "enb": "Embraer's new narrowbody"}[m.group(1)])]


ID1 = r"[A-Z]{1,3}X?G?-\d{3,4}"
IDS = r"(?:record:\s*)?\b" + ID1 + r"(?:,\s*" + ID1 + r")*\b"
ROUND_CTX = [None]        # the round whose record is being rendered (clean() words NGSA's hold by round)

PRE = [  # order values, engine codes, file names and section marks the agents quote: before CODES
    (r"\bleave the `?(?:fps_|fps |NGSA |ngsa_)?engine[_ ]code`? (?:null|None)\b", "make no engine order"),
    (r"\b(?:fps |NGSA )?engine code:? (?:null|None)\b|\bcode null\b", "no engine order"),
    (r"(?i)\b(?:NGSA )?(?:engine )?code:? 7\b", lambda m: ("The" if m.group(0)[0].isupper() and not m.group(0).startswith("NGSA") else "the") + " all-three-makers engine order"),
    (r"\bfps_site at new_site\b", "the fps at new sites"), (r",? ?fps_site:? new_site\b", ""),
    (r"\bA320 plan alt\b|\ba320_plan alt\b", "the A320 Alt plan"), (r"\bthe revision is null\b", "nothing was revised"),
    (r",? run dash-2050-\w+", ""), (r"\(?teams\.md Step 2; ?", "("),
    (r"`?\bteams\.md`? section \d+", "the team rule"), (r"`?\bteams\.md`?", "the team rule"),
    (r"`?\bdashboard_game\.md`?(?: section \d+| §\d+)?", "the board's rules"),
    (r" ?\((?:profile|brief) §\d+\)", ""), (r"`?\bprofile\.md`?(?: section \d+| §\d+)?", "the company profile"),
    (r"`?\bround\d\.md`?(?: section \d+)?", "the brief"),
    (r" ?\(`?rules\.md`?\)", ""), (r"`?\brules\.md`? allows\b", "the game rules allow"), (r"`?\brules\.md`?", "the game rules"),
    (r"\bBrief §\d+\.\s+", ""), (r"\bBrief §\d+(?: grid)?", "The brief"), (r"\bbrief §\d+(?: grid)?", "the brief"),
    (r"\bbrief section 2\b", "the brief's balance-sheet section"), (r"\b(?:brief )?[Ss]ection 1's\b", "the brief's 'position now'"),
    (r"\bSection 1\b", "The brief's 'position now'"), (r"\b(?:brief )?section 1\b", "the brief's 'position now'"),
    (r"\bbrief section \d\b", "the brief"),
    (r"\bMy agent file says that when\b", "Under the team rule, when"), (r"\bmy agent file\b", "the team rule"),
    (r" ?\(§ orders\)", ""), (r" ?\(profile §\d+\)", ""),
    (r"\s*\bfor `?other_moves`?", ""), (r"`?\bother_moves\b`?", "the other-moves order"),
    (r"That's a triple layer question[,.] (?:so |So )?(?:three parts\.|Three parts\.|let me start with the window\.)\s*", ""),
    (r"\b(?:he|she) judges\b", "they judge"),
    (r"\bon every field\b", "on every order"),
    (r",? ?`?[\w-]+\.md`?(?: §\d+)?", ""), (r"\bprofile §\d+\s*", "the company's "), (r"\(§\d+: ", "("), (r" ?§ ?\d+\b", ""),
    (r"\bagainst ((?:\d, )+\d) and None\b", "against the other engine orders and no order"),
    (r"\bI mean, (\w)", lambda m: m.group(1).upper()), (r", right\?", "."),
]
CODE_LBL = {1: "RR-only", 2: "P&W-only", 3: "CFM-only", 4: "Joint Venture", 5: "RR-and-CFM", 6: "P&W-and-CFM", 7: "all-three-makers"}


def _codes(m):
    names = [CODE_LBL[int(d)] for d in re.findall(r"[1-7]", m.group(2))]
    lab = names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]
    return ("The " if m.group(1)[0] == "C" else "the ") + lab + " engine order" + ("s" if len(names) > 1 else "")


POST = [  # one name for each thing, and the page's number style
    (r"no engine code \(7 has been final since EIS\)", "no new engine order (the all-three-makers order has been final since EIS)"),
    (r"there is no code order this round \(no engine order\)", "there is no engine order this round"),
    (r"\bwhich engine code\b", "which engine order"), (r"\bthe only code that\b", "the only engine order that"),
    (r"\bEngine code, tested\b", "Engine order, tested"), (r"\b([Ee])very field (is|stays) at its default\b", r"\1very order \2 at its default"),
    (r"Embraer's new narrowbody = hold\b", "Embraer holding"),
    (r"a valid value in the brief's order field \(`?hold`?, `?launch`?\)", "one of the brief's two choices (hold or launch)"),
    (r"(?i)\b(?:NGSA |fps )?engine code:? ([1-7])\b", lambda m: ("The " if m.group(0)[0] == "E" else "the ") + CODE_LBL[int(m.group(1))] + " engine order"),
    (r"\b([Cc]odes?):? ((?:[1-7](?:, | and | or )?)+)\b", _codes),
    (r"\b737 rate up\b", "737 Rate Increase"), (r"\b(?:the )?737 rate increase\b", lambda m: ("the " if m.group(0).startswith("the") else "") + "737 Rate Increase"),
    (r"\b10-yr\b", "10-year"), (r"\b7-yr\b", "7-year"), (r"\brenton\b", "Renton"), (r"\bfps site new sites\b", "the fps at new sites"),
    (r"(?<![\w$.])([-+−]?)(\d+\.\d+) \$B\b", lambda m: ("−" if m.group(1) in "-−" and m.group(1) else "+" if m.group(1) == "+" else "") + "$" + m.group(2) + "B"),
    (r"\byp\b", "yield points"), (r"ε \(\$1B\)", "the $1B tie band"), (r"ε", "the $1B tie band"),
]


def ngsa_hold(t):
    """In round 1 NGSA's hold is not launching it; from round 2 it is NGSA continuing."""
    if ROUND_CTX[0] == 1:
        return re.sub(r"`?\bngsa:\s*hold`?|\bNGSA:? hold\b", "NGSA not launched", t, flags=re.I)
    if ROUND_CTX[0]:
        return re.sub(r"`?\bngsa:\s*hold`?|\bNGSA:? hold\b", "NGSA continuing", t, flags=re.I)
    return t


def clean(t):
    """Agent prose for the page: no order codes, evidence ids, file names or code ticks."""
    t = re.sub(r"\s*\[(?:[A-Z]{1,3}X?G?-\d{3,4}(?:,\s*)?)+[^\]]*\]", "", str(t or ""))
    # evidence ids outside brackets, e.g. "(inference, BX-1331)", "(one remark, BX-1329; inference)" or "(record: BX-1331, applied ...)":
    # drop the id group and one separator, keep the other
    t = re.sub(r"\s+from\s+" + IDS + r"(?=\s*\))", "", t)
    t = re.sub(r"\(\s*" + IDS + r"\s*[,;:]?\s*", "(", t)
    t = re.sub(r"\s*[,;:]?\s*" + IDS + r"(?=\s*[;)])", "", t)
    t = re.sub(r"\s*[,;:]?\s*(?:record:\s*)?\b[A-Z]{1,3}X?G?-\d{3,4}\b\s*[,;]?", "", t)
    t = re.sub(r"\(\s*[,;:]?\s*", "(", t)
    t = re.sub(r"\s*[,;:]\s*\)", ")", t)
    t = re.sub(r"\(\s*\)", "", t)
    t = re.sub(r"\((?:inference|research, unverified)\)", "", t)
    for pat, sub in PRE:
        t = re.sub(pat, sub, t)
    t = ngsa_hold(t)
    for pat, sub in CODES:
        t = re.sub(pat, sub, t)
    for pat, sub in PRE[:3] + POST:            # engine codes again, now that CODES has spelled the field names
        t = re.sub(pat, sub, t)
    t = ngsa_hold(t)
    t = re.sub(r"\s*\((?:inference|research, unverified)(?: from)?\)", "", t)
    t = re.sub(r"\s*\(\s*\)", "", t)
    # people's pronouns are not stated in the sources: name the thing instead, or use they/them
    for pat, sub in ((r"\bHe reads his test\b", "The CFO reads the test"), (r"\b(?:his|her) (memo|correction|test|expected column|veto|tests|view|record)\b", r"the \1"),
                     (r"\b(?:with|from|to|for) (?:him|her)\b", lambda m: m.group(0).split()[0] + " them"),
                     (r"\b(?:his|her)\b", "their"), (r"\b(?:He|She)\b", "They"), (r"\b(?:he|she)\b", "they"), (r"\b(?:him)\b", "them")):
        t = re.sub(pat, sub, t)
    return t.replace("`", "")


def short(t, n=320):
    """Clean, one line, at most n characters: cut at a sentence end, else at a word with ' …'; never leave an open
    bracket or a dangling separator."""
    t = clean(t)
    t = re.sub(r"^\s*-\s+(\w)", lambda m: m.group(1).upper(), t)
    t = re.sub(r"([.;:])?\s*\n\s*-\s+", lambda m: (m.group(1) + " ") if m.group(1) else ". ", t)   # inline bullets become sentences
    t = re.sub(r"(?<=[.;:])\s+-\s+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"\.\s*\.", ".", t).replace(":.", ":").replace(". .", ".")
    t = re.sub(r"(?<!\be\.g)(?<!\bi\.e)([.!?] )([a-z])(?!ps\b)", lambda m: m.group(1) + m.group(2).upper(), t)
    if len(t) > n:
        cut = t[:n]
        k = cut.rfind(". ")
        t = cut[:k + 1] if k > n * 0.5 else cut.rsplit(" ", 1)[0].rstrip(",;:(") + " …"
        if t.count("(") > t.count(")"):               # an unclosed bracket: cut before it
            i = t.rfind("(")
            t = t[:i].rstrip(" ,;:") + (" …" if not t[:i].rstrip().endswith(".") else "")
    return t.rstrip(";, ")


# ─────────────────────────────── orders ───────────────────────────────
ORDER_TXT = {
    "boeing": {"fps": {"launch_7yr": "fps, 7-year", "launch_10yr": "fps, 10-year", "launch_via_embraer": "fps via Embraer", "cancel": "cancel fps"},
               "rate_737": {"increase": "737 rate up"}, "re787": {"launch": "787 Re-engine", "cancel": "cancel 787 Re-engine"},
               "fps_site": {"renton": "fps at Renton"}},
    "airbus": {"ngsa": {"launch": "NGSA", "cancel": "cancel NGSA"}, "rea350": {"launch": "A350 Re-engine", "cancel": "cancel A350 Re-engine"},
               "delay_tactics": {"bottleneck": "Delay Tactics", "poaching": "Delay Tactics", "both": "Delay Tactics (both)"},
               "a320_plan": {"alt": "A320 Alt plan"}},
    "cfm": {"ducted": {"launch": "Ducted engine", "cancel": "cancel Ducted"}, "open_fan": {"launch": "Open Fan", "cancel": "cancel Open Fan"},
            "partner_embraer": {"launch": "Embraer partnership", "cancel": "end Embraer partnership"},
            "lobby_emissions": {"launch": "emissions lobbying"}, "genx": {"upgrade_genx9": "GEnx upgrade", "invest_genx": "GEnx investment", "cancel": "cancel GEnx"}},
    "pratt_whitney": {"gtf2_solo": {"launch": "GTF2", "launch_if_selected": "GTF2 if selected", "cancel": "cancel GTF2"},
                      "jv_with_rr": {"commit": "commits to the Joint Venture", "withdraw": "withdraws from the Joint Venture"}},
    "rolls_royce": {"ultrafan_nb_solo": {"launch": "UltraFan NB", "launch_if_selected": "UltraFan NB if selected", "cancel": "cancel UltraFan NB"},
                    "jv_with_pw": {"commit": "commits to the Joint Venture", "withdraw": "withdraws from the Joint Venture"},
                    "ultrafan_wb": {"launch": "UltraFan WB", "cancel": "cancel UltraFan WB"}, "t1000_upgrade": {"launch": "Trent 1000 upgrade"}},
    "embraer": {"enb": {"launch": "new narrowbody with Korea", "cancel": "cancel new narrowbody"}},
}
CODE = {1: "RR", 2: "P&W", 3: "CFM", 4: "RR & P&W Joint Venture", 5: "RR and CFM", 6: "P&W and CFM", 7: "all three makers"}


def move_list(side, o):
    out = []
    for f, val in o.items():
        if f.endswith("_engine_code") or val in DEFAULTS:
            continue
        t = ORDER_TXT.get(side, {}).get(f, {}).get(val, f"{f}: {val}")
        if f in ("fps", "ngsa") and val.startswith("launch") and o.get(f + "_engine_code"):
            t += f" (engines: {CODE[int(o[f + '_engine_code'])]})"
        out.append(t)
    return out


def move_txt(side, o):
    m = move_list(side, o)
    return ", ".join(m) if m else "Do Nothing"


def move_txt_r(side, o, n):
    """move_txt for round n: Airbus's A320 Alt plan is a standing order from 2030, so later rounds read as NGSA
    continuing with the plan kept, not as a new move."""
    t = move_txt(side, o)
    if side == "airbus" and n > 1 and o.get("ngsa") in ("hold", None):
        t = t.replace("A320 Alt plan", "NGSA continues (A320 Alt plan kept)") if "A320 Alt plan" in t else ("NGSA continues, " + t if t != "Do Nothing" else "NGSA continues")
    return t


def moves_table(R):
    head = ["Round"] + [NAME[s] for s in SIDES]
    rows = [[f"{r['year']}"] + [esc(move_txt_r(s, r["orders"][s], r["round"])) for s in SIDES] for r in R["rounds"]]
    return K.table(head, rows).replace("<table>", '<table class="moves">', 1)


# ─────────────────────────────── charts ───────────────────────────────
def lc(series, lo, hi, step, fmt, label, aria, end_labels, refs=(), notes=(), x_hi=2063):
    return K.line_chart(series, lo, hi, step, fmt, label, list(refs), aria, end_labels, list(notes), x_lo=2026, x_hi=x_hi)


def spread(vals, gap=22, span=(30, 300)):
    """End-label offsets so labels at the right edge do not collide and stay inside the plot: vals are y positions."""
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    pos = [vals[i] for i in order]
    for k in range(1, len(pos)):
        pos[k] = max(pos[k], pos[k - 1] + gap)
    over = pos[-1] - span[1] if pos else 0
    if over > 0:
        pos = [max(span[0], x - over) for x in pos]
        for k in range(1, len(pos)):
            pos[k] = max(pos[k], pos[k - 1] + gap)
    off = [0.0] * len(vals)
    for k, i in enumerate(order):
        off[i] = pos[k] - vals[i]
    return off


def legend(items):
    """A line-chart key outside the scroller: (label, css var, 'solid' | 'dash' | 'dotl')."""
    return '<div class="legend">' + "".join(f'<span><i class="{st}" style="border-top-color:var(--{v})"></i>{esc(l)}</span>'
                                            for l, v, st in items) + "</div>"


def no_leaders(svg):
    """The kit draws a leader to each end label; these charts carry their key underneath, so drop the leaders."""
    return re.sub(r'<line [^>]*class="leader"/>', "", svg)


PROFIT_KEY = [("This game", "s1", "solid"), ("Previous game", "muted", "dash"), ("Status quo", "faint", "dotl")]
DEBT_KEY = [("This game", "s1", "solid"), ("Stress case", "faint", "dotl"), ("Previous game", "muted", "dash")]
DEBT_X_HI = 2040


def profit_chart():
    ys = list(range(2026, 2061))
    s_c = [(y, FIN[y]["profit"]) for y in ys]
    s_p = [(y, PFIN[y]["profit"]) for y in ys]
    s_q = [(y, C["status_quo"]["boeing_profit"][y - 2026]) for y in ys]
    hi = max(v for _, v in s_c + s_p + s_q)
    hi = (int(hi / 2) + 1) * 2
    # all three end at the same point in 2060, so the key sits under the chart (legend), not at the line ends
    return no_leaders(lc([("Status quo", "faint", s_q), ("Previous game", "muted", s_p), ("This game", "s1", s_c)], 0, hi, 2, "int",
              "Boeing commercial operating profit, $B a year (2026 prices)", "Boeing's operating profit by year, this game, the previous game and the status quo",
              [(0, ""), (0, ""), (0, "")]))


def debt_chart():
    ys = [y for y in range(2027, DEBT_X_HI + 1) if FIN[y]["debt"] is not None]
    s_c = [(y, FIN[y]["debt"]) for y in ys]
    s_s = [(y, FIN[y]["debt_stress"]) for y in ys]
    s_p = [(y, PFIN[y]["debt"]) for y in ys if PFIN[y]["debt"] is not None]
    lo = min(v for _, v in s_c + s_s + s_p)
    lo = (int(lo / 25) - 1) * 25 if lo < 0 else 0
    hi = max(25, (int(max(v for _, v in s_c + s_s + s_p) / 25) + 1) * 25)
    return no_leaders(lc([("Stress case", "faint", s_s), ("Previous game", "muted", s_p), ("This game", "s1", s_c)], lo, hi, 25, "int",
              f"Boeing net debt at year end, $B (2026 prices), 2027-{DEBT_X_HI}", "Boeing's net debt path, this game, its stress case and the previous game",
              [(0, ""), (0, ""), (0, "")],
              refs=[(C["debt_inputs"]["historical_level_b"], "Historical level", "above")] if abs(C["debt_inputs"]["historical_level_b"]) > 1e-9 else [],
              x_hi=DEBT_X_HI))


def deliveries_chart(narrow=False):
    w, h, left, right, top, bot = (360, 300, 44, 22, 20, 44) if narrow else (760, 330, 54, 16, 20, 44)
    ys = list(range(2026, 2061))
    segs_def = [("boeing", "s1", "Boeing"), ("airbus", "s2", "Airbus"), ("comac", "comac", "COMAC"), ("embraer", "s3", "Embraer")]
    val = lambda m, k: (m["max"] + m["fps"]) if k == "boeing" else (m["a320"] + m["ngsa"]) if k == "airbus" else m[k]
    top_v = max(max(MK[y]["demand"] or 0, sum(val(MK[y], k) for k, _, _ in segs_def)) for y in ys)
    hi = (int(top_v / 500) + 1) * 500
    bw = (w - left - right) / len(ys)
    sx = lambda y: left + (y - ys[0] + 0.5) * bw
    sy = lambda v: top + (hi - v) / hi * (h - top - bot)
    out = [K.svg_open(w, h, "Single-aisle aircraft delivered each year by maker, final state of this game", "chart narrow" if narrow else "chart")]
    v = 0
    while v <= hi:
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" class="grid"/><text x="{left - 6}" y="{sy(v) + 4:.1f}" text-anchor="end" class="tick">{n0(v)}</text>')
        v += 500
    for y in ys:
        m = MK[y]
        acc = 0.0
        segs = [(k, var) for k, var, _ in segs_def if val(m, k) > 0.5]
        for j, (k, var) in enumerate(segs):
            x = val(m, k)
            y0, y1 = sy(acc), sy(acc + x)
            gap = 1.0 if j else 0.0
            if j == len(segs) - 1:
                out.append(f'<path d="{K.bar_path(sx(y) - bw * 0.38, bw * 0.76, y0 - gap, y1)}" fill="var(--{var})"/>')
            else:
                out.append(f'<rect x="{sx(y) - bw * 0.38:.1f}" width="{bw * 0.76:.1f}" y="{y1 + 1:.1f}" height="{max(0.0, y0 - y1 - 1 - gap):.1f}" fill="var(--{var})"/>')
            acc += x
        out.append(f'<rect x="{sx(y) - bw / 2:.1f}" width="{bw:.1f}" y="{top}" height="{h - top - bot}" class="hit" '
                   + K.mark_attrs((str(y), "", None), (n0(m["max"] + m["fps"]), "Boeing (MAX + fps)", "var(--s1)"),
                                  (n0(m["a320"] + m["ngsa"]), "Airbus (A320 + NGSA)", "var(--s2)"), (n0(m["comac"]), "COMAC", "var(--comac)"),
                                  (n0(m["embraer"]), "Embraer", "var(--s3)"), (n0(m["lost"] or 0), "Customers lost", None),
                                  (n0(m["demand"] or 0), "Demand", None)) + "/>")
    d = "M" + " L".join(f"{sx(y):.1f},{sy(MK[y]['demand'] or 0):.1f}" for y in ys)
    out.append(f'<path d="{d}" fill="none" stroke="var(--fg)" stroke-width="2" pointer-events="none"/>')
    for y in ys:
        if y % (10 if narrow else 5) == 0:
            out.append(f'<text x="{sx(y):.1f}" y="{h - bot + 18}" text-anchor="middle" class="tick">{y}</text>')
    out.append(f'<text x="{left}" y="{h - 6}" class="tick">{"Aircraft a year" if narrow else "737/A320-class aircraft delivered a year (bars) and demand (line), final state"}</text></svg>')
    return "".join(out)


def share_chart():
    ys = list(range(2026, 2061))
    ser = [("Boeing", "s1", [(y, MK[y]["sh_boeing"]) for y in ys]), ("Airbus", "s2", [(y, MK[y]["sh_airbus"]) for y in ys]),
           ("COMAC", "comac", [(y, MK[y]["sh_comac"]) for y in ys])]
    if EMB_DLV:
        ser.append(("Embraer", "s3", [(y, MK[y]["sh_embraer"]) for y in ys]))
    ser.append(("Boeing, previous game", "muted", [(y, PMK[y]["sh_boeing"]) for y in ys]))
    yfun = lambda v: 26 + (0.8 - v) / 0.8 * (346 - 26 - 46)
    offs = spread([yfun(s[2][-1][1]) for s in ser])
    end = {"Boeing, previous game": "Boeing (prev.)"}          # the key under the chart carries the full name
    return lc(ser, 0, 0.8, 0.2, "pct", "Share of single-aisle deliveries", "Single-aisle delivery shares by maker, final state",
              [(o, end.get(s[0], s[0])) for o, s in zip(offs, ser)])


# ─────────────────────────────── tables ───────────────────────────────
def drop_flat(head, rows, keep=1):
    """Drop columns (after the first `keep`) whose cells are all the same; returns head, rows and the dropped
    column names with their one value, for the caption."""
    idx = [i for i in range(len(head)) if i < keep or len({r[i] for r in rows}) > 1]
    gone = [(head[i], rows[0][i]) for i in range(len(head)) if i not in idx]
    return [head[i] for i in idx], [[r[i] for i in idx] for r in rows], gone


def fin_cols():
    head = ["Year", "NB deliveries", "WB deliveries", "Revenue $B", "Commercial operating profit $B", "Status-quo profit $B",
            "Programme cash $B", "Free cash flow, all of Boeing (consensus to 2030, flat after) $B", "Net debt $B", "Cash for owners $B",
            "Net debt, stress $B", "Net debt, previous game $B"]
    rows = []
    for y in KEY:
        f, p_ = FIN[y], PFIN[y]
        rows.append([str(y), n0(f["nb_units"]), n0(f["wb_units"]), f"{f['revenue']:.1f}", f"{f['profit']:.1f}", f"{f['sq_profit']:.1f}",
                     f"{f['spend']:.1f}" if f["spend"] else "—", K.num(f["fcf"], "+.1f") if f["fcf"] is not None else "—",
                     f"{f['debt']:.1f}" if f["debt"] is not None else "—", K.num(f["owners"], "+.1f") if f.get("owners") is not None else "—",
                     f"{f['debt_stress']:.1f}" if f["debt_stress"] is not None else "—",
                     f"{p_['debt']:.1f}" if p_["debt"] is not None else "—"])
    # cash for owners repeats free cash flow when every year's surplus goes to the owners
    same_owners = all(r[7] == r[9] for r in rows)
    if same_owners:
        head, rows = head[:9] + head[10:], [r[:9] + r[10:] for r in rows]
    head, rows, gone = drop_flat(head, rows)
    return head, rows, gone, same_owners


def fin_table():
    head, rows, _, _ = fin_cols()
    return K.table(head, rows, num_cols=tuple(range(1, len(head))))


def share_cols():
    head = ["Year", "Demand", "Boeing", "of which fps", "Airbus", "of which NGSA", "COMAC"] + (["Embraer"] if EMB_DLV else []) + \
           ["Boeing share", "Airbus share", "COMAC share"] + (["Embraer share"] if EMB_DLV else []) + ["Boeing share, previous game", "Boeing widebody share"]
    rows = []
    for y in KEY:
        m, q = MK[y], PMK[y]
        r = [str(y), n0(m["demand"]), n0(m["max"] + m["fps"]), n0(m["fps"]), n0(m["a320"] + m["ngsa"]), n0(m["ngsa"]), n0(m["comac"])]
        r += [n0(m["embraer"])] if EMB_DLV else []
        r += [pc(m["sh_boeing"]), pc(m["sh_airbus"]), pc(m["sh_comac"])] + ([pc(m["sh_embraer"])] if EMB_DLV else []) + [pc(q["sh_boeing"]), pc(m["wb_boeing"])]
        rows.append(r)
    return drop_flat(head, rows)


def share_table():
    head, rows, _ = share_cols()
    return K.table(head, rows, num_cols=tuple(range(1, len(head))))


BRIDGE_LBL = {"nb_profit_vs_sq": "Narrowbody profit against the status quo (the game board's fixed-size market)", "wb_profit_vs_sq": "Widebody profit against the status quo",
              "programme_investment": "Programme investment", "rate_hike": "737 rate increase", "delay_tactics_spend": "Delay Tactics spend",
              "write_offs": "Write-offs", "debt_penalty": "Debt penalty", "two_front_strain": "Two-front strain", "naked_fine": "Naked Delay Tactics fine",
              "supply_demand": "Supply and demand: what the factories deliver, and Embraer's price pressure", "supply_plan": "Supply plan",
              "government_cofunding": "Politics: governments carry part of the fps bill",
              "political_exit_cost": "Politics: the cost of leaving the narrowbody market"}


def bridge_table(br, prev=None):
    keys = [k for k in br if abs(br[k]) > 1e-9 or (prev and abs(prev.get(k, 0.0)) > 1e-9)]
    head = ["Component", "This game"] + (["Previous game"] if prev else [])
    rows = [[esc(BRIDGE_LBL.get(k, k)), b(br[k])] + ([b(prev.get(k, 0.0))] if prev else []) for k in keys]
    rows.append(["<b>Boeing's value against the status quo</b>", f"<b>{b(sum(br.values()))}</b>"] + ([f"<b>{b(sum(prev.values()))}</b>"] if prev else []))
    return K.table(head, rows, num_cols=(1, 2))


def value_table():
    head = ["Company"] + [f"After {y}" for y in YEARS] + ["Previous game, final"]
    rows = []
    for s in SIDES:
        rows.append([NAME[s]] + [b(r["value"][s]) for r in C["rounds"]] + [b(P["rounds"][-1]["value"][s]) if s in P["rounds"][-1]["value"] else "—"])
    return K.table(head, rows, num_cols=tuple(range(1, len(head))))


# ─────────────────────────────── decision chains ───────────────────────────────
SEATS = {"boeing": ("Kelly Ortberg", "Jay Malave", "Stephanie Pope"), "airbus": ("Guillaume Faury", "Thomas Toepfer", "Lars Wagner"),
         "embraer": ("Francisco Gomes Neto", "Felipe Santana", "Arjan Meijer")}
# The codes the quoted memos use, from each company's profile (wargame/profiles/<company>/profile.md hard rules)
_COLS = ("<b>S1, S2 …</b> are the columns of that round's brief, one per rival move (listed at the top of each round; "
         "the same code means a different move for each company and in each round).")
CODE_KEY = {
    "boeing": ("<p><b>How to read Boeing's memos.</b> " + _COLS + " <b>A, B …</b> are the options the CEO put to the seats. "
               "<b>Ask (n)</b> is the CEO's numbered question to that seat; <b>Board ask n</b> is a numbered request in the Board's guidance. The <b>buffer test</b> is the CFO's binding veto on a plan "
               "more than $2B below Do Nothing in the risk case. <b>Boeing's hard rules:</b> H1 no fps order in round 1 · H2 no fps "
               "planned to enter service before its technology is ready · H3 no 787 Re-engine in round 1, and none once Airbus has "
               "launched the A350 Re-engine · H4 one major development at a time (a Solo fps and the 787 Re-engine overlap for at most "
               "two years) · H5 never cancel a launched fps or 787 Re-engine over slips or charges · H6 no 737 Rate Increase in reply to "
               "Airbus or during a quality, FAA or supply crisis · H7 no fps launch while a Boeing crisis is live · H8 the money rule: gaps "
               "within the $1B tie band are ties that doctrine decides, and at most $2B may be given up for a doctrine choice.</p>"),
    "airbus": ("<p><b>How to read Airbus's memos.</b> " + _COLS + " <b>Row A, Row B …</b> are the options the CEO put to the seats. "
               "<b>Ask n</b> is the CEO's numbered question to that seat; <b>Board ask n</b> is a numbered request in the Board's guidance. "
               "A <b>soft veto</b> from the CFO or the head of Commercial Aircraft binds unless the plan is at least $1B better, which "
               "lets the CEO override it; the five pillars (safety, quality, integrity, compliance, security) and the company's rules bind everyone. "
               "<b>Airbus's rules:</b> 1 NGSA never enters service before its technology is ready (launch window 2028-30) · 2 its own "
               "clock: NGSA is neither hurried nor delayed for Boeing · 3 no A350 Re-engine once Boeing has launched a 787 Re-engine · "
               "4 Delay Tactics at most once a game and only against an fps in development: with no fps on the public record any move is "
               "naked and draws a $48.32B fine · 5 poaching only while an Airbus programme is in development · 6 protect net cash: at "
               "most one new launch a round, and NGSA and the A350 Re-engine overlap two years or less · 7 never cancel NGSA in reaction "
               "to Boeing · 8 no engine that pushes NGSA past 2037.</p>"),
    "embraer": ("<p><b>How to read Embraer's memos.</b> " + _COLS + " <b>Row 1</b> is holding, <b>Row 2</b> launching the new "
                "narrowbody. A <b>yield point</b> is 1% of Embraer's enterprise value ($0.11B). <b>Ask (n)</b> is the CEO's numbered "
                "question to that seat; <b>Board ask n</b> is a numbered request in the Board's guidance. <b>Embraer's hard rules:</b> H1 no launch without Team Korea · H2 no launch that risks the "
                "balance sheet: the launch must be at or above zero in the expected column, debt penalty included, and the CFO's "
                "funding test must pass · H3 launch only into a window: it is shut when both fps and NGSA are in service, or due, "
                "within two years of Embraer's entry into service · H4 cancel only before entry into service, and only when writing "
                "off beats continuing by more than the tie band · H5 the money rule: within 2 yield points is a tie, and at most 5 may "
                "be given up for a doctrine choice · H6 no launch while Boeing's fps via Embraer is live.</p>"),
}


def veto_tag(v):
    """A seat's vetoes list holds binding vetoes and, marked not binding, advice and flags: tag each as it is."""
    if v.get("binding"):
        return '<span class="tag veto">veto (binding)</span>'
    txt = (v.get("plan", "") + " " + v.get("ground", "")).strip()
    return '<span class="tag muted">' + ("flag" if re.search(r"Hard-rule flag", txt) else "advice") + "</span>"


def tests_list(memo):
    if not memo:
        return "<p class=muted>No memo returned.</p>"
    items = []
    for t in memo.get("tests", []):
        res = t.get("result", "")
        cls = {"pass": "pass", "fail": "fail"}.get(res, "muted")
        items.append(f'<li><span class="tag {cls}">{esc(clean(res))}</span> <b>{esc(short(t.get("name", ""), 110))}</b>: {esc(short(t.get("numbers", ""), 240))}</li>')
    vet = sorted([v for v in memo.get("vetoes", []) if v], key=lambda v: not v.get("binding"))
    vtxt = "".join(f'<li>{veto_tag(v)} {esc(short(v.get("plan", ""), 120))}: {esc(short(v.get("ground", ""), 220))}</li>' for v in vet)
    return f'<ul class="tl">{"".join(items)}{vtxt}</ul><p class="memo">{esc(short(memo.get("memo", ""), 520))}</p>'


def option_key(fr):
    """The options the CEO put to the seats (frame.options_to_test), by letter or row number: the memos refer to
    them as A, B ... or Row 1, Row 2."""
    out = []
    for o in fr.get("options_to_test") or []:
        m = re.match(r"\s*(?:Row\s+)?([A-Z]|\d+)[.,]\s+(.*)", o, re.S)
        if not m:
            continue
        body = re.split(r":\s*[-+−]?\$?\d|\.\s|\n|\s\([-+−]\d", m.group(2), maxsplit=1)[0]
        if body.count("(") > body.count(")"):
            body = body[:body.rfind("(")].rstrip(" ,;:")
        out.append(f"<b>{esc(m.group(1))}</b> {esc(short(body, 110))}")
    return " · ".join(out)


def column_key(side, n):
    sc = grid(n, side)["scenarios"]
    return " · ".join(f"<b>S{i + 1}</b> {esc(clean(x))}" for i, x in enumerate(sc))


def chain(side, n):
    x = REC(n).get(side)
    if not x:
        return "<p>No record.</p>"
    ROUND_CTX[0] = n
    try:
        return _chain(side, n, x)
    finally:
        ROUND_CTX[0] = None


def _chain(side, n, x):
    ceo, cfo, ops = SEATS[side]
    g, fr, dec = x.get("board_guidance") or {}, x.get("frame") or {}, x.get("final") or x.get("decision") or {}
    bits = [f'<div class="key"><p><b>Columns in this round\'s brief:</b> {column_key(side, n)}</p>'
            + (f'<p><b>Options the CEO put to the seats:</b> {option_key(fr)}</p>' if option_key(fr) else "") + "</div>"]
    if g:
        wv = [short(v, 160).rstrip(".") for v in (g.get("would_veto") or [])]
        bits.append(f'<div class="step"><p class="sh">1 · Board guidance</p><p><b>Risk appetite:</b> {esc(short(g.get("risk_appetite", ""), 360))}</p>'
                    f'<p><b>First priority:</b> {esc(short((g.get("priorities") or [""])[0], 360))}</p>'
                    f'<p><b>Would veto:</b> {" · ".join(esc(v) for v in wv)}</p></div>')
    bits.append(f'<div class="step"><p class="sh">2 · {esc(ceo)} (CEO) frames the round</p><p><b>Question:</b> {esc(short(fr.get("question", ""), 300))}</p>'
                f'<p><b>Initial lean:</b> {esc(short(fr.get("initial_lean", ""), 420))}</p></div>')
    bits.append(f'<div class="step"><p class="sh">3 · {esc(cfo)} (CFO) tests it</p>{tests_list(x.get("cfo"))}</div>')
    bits.append(f'<div class="step"><p class="sh">3 · {esc(ops)} (operating head) tests it</p>{tests_list(x.get("ops"))}</div>')
    d0 = x.get("decision") or {}
    bits.append(f'<div class="step"><p class="sh">4 · {esc(ceo)} decides</p><p><b>Orders:</b> {esc(move_txt_r(side, d0.get("orders", {}), n))}</p>'
                f'<p><b>Expected column:</b> {esc(short(d0.get("expected_scenario", ""), 260))}</p>'
                f'<p><b>Best grid plan there:</b> {esc(short(d0.get("best_grid_plan_in_expected_scenario", ""), 620))}'
                + (f' · premium {b(d0.get("premium_b"), 2, False)}' if d0.get("premium_b") else "") + "</p>"
                f'<p class="memo">{esc(short(d0.get("rationale", ""), 700))}</p></div>')
    vc = x.get("veto_checks") or {}
    vtxt = []
    for seat, nm in (("cfo", cfo), ("ops", ops)):
        v = vc.get(seat) or {}
        if v:
            state = "concurs" if v.get("concur") else ("vetoes" + (" (binding)" if (v.get("veto") or {}).get("binding") else ""))
            vtxt.append(f"<li><b>{esc(nm)}</b> {state}{': ' + esc(short(v.get('note', ''), 220)) if v.get('note') else ''}</li>")
    if x.get("revision"):
        vtxt.append(f"<li><b>Revision:</b> {esc(move_txt_r(side, x['revision'].get('orders', {}), n))}. {esc(short(x['revision'].get('rationale', ''), 260))}</li>")
    bits.append(f'<div class="step"><p class="sh">5 · Veto check{" and revision" if x.get("revision") else ""}</p><ul class="tl">{"".join(vtxt)}</ul></div>')
    rv = x.get("board_review") or {}
    items = rv.get("items") or []
    if items:
        it = "".join(f'<li><span class="tag {"pass" if i.get("decision") == "approve" else "veto"}">{esc(i.get("decision", ""))}</span> '
                     f'<b>{esc(clean(str(i.get("order_field", "")) + ": " + str(i.get("value", ""))))}</b>: {esc(short(i.get("ground", ""), 260))}</li>' for i in items)
    else:
        it = f'<li>{esc(clean(rv.get("note", "No Board items: every order is the default.")))}</li>'
    if x.get("board_revision"):
        it += f"<li><b>CEO revises within the veto:</b> {esc(move_txt_r(side, x['board_revision'].get('orders', {}), n))}</li>"
    if x.get("board_reverted"):
        it += f"<li><b>Reverted to the default:</b> {esc(', '.join(clean(k) for k in x['board_reverted']))}</li>"
    bits.append(f'<div class="step"><p class="sh">6 · Board review</p><ul class="tl">{it}</ul></div>')
    bits.append(f'<div class="step final"><p class="sh">Sealed orders</p><p><b>{esc(move_txt_r(side, x.get("final_orders", {}), n))}</b></p></div>')
    return '<div class="chain">' + "".join(bits) + "</div>"


def chains_section(side):
    blocks = []
    for r in C["rounds"]:
        n = r["round"]
        blocks.append(f'<details class="panel rnd"{" open" if n == 1 else ""}><summary><b>{r["year"]}</b> · {esc(move_txt_r(side, r["orders"][side], n))}</summary>{chain(side, n)}</details>')
    return f'<div class="panel key">{CODE_KEY[side]}</div>' + "".join(blocks)


CSS_EXTRA = """
:root { --comac: #8a5cc4; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --comac: #9b6fd6; } }
:root[data-theme="dark"] { --comac: #9b6fd6; }
.scroll { background:
    linear-gradient(to right, var(--surface) 40%, transparent) left / 32px 100% no-repeat local,
    linear-gradient(to left, var(--surface) 40%, transparent) right / 32px 100% no-repeat local,
    linear-gradient(to right, color-mix(in srgb, var(--fg) 22%, transparent), transparent) left / 14px 100% no-repeat scroll,
    linear-gradient(to left, color-mix(in srgb, var(--fg) 22%, transparent), transparent) right / 14px 100% no-repeat scroll; }
.scroll > table { background: transparent; }
ul.cav li, footer { overflow-wrap: anywhere; }
.legend .solid { display: inline-block; width: 18px; height: 0; border-top: 2px solid var(--fg); vertical-align: middle; margin-right: 6px; }
.legend .dash { display: inline-block; width: 18px; height: 0; border-top: 2px dashed var(--muted); vertical-align: middle; margin-right: 6px; }
.chain { display: grid; gap: 10px; margin-top: 10px; }
.step { border-left: 3px solid var(--line); padding: 2px 0 2px 12px; }
.step.final { border-left-color: var(--s1); }
.step .sh { font: 600 12px var(--font-mono); text-transform: uppercase; letter-spacing: .04em; color: var(--muted); margin: 0 0 4px; }
.step p { margin: 4px 0; } .memo { color: var(--muted); }
ul.tl { margin: 4px 0; padding-left: 18px; } ul.tl li { margin: 3px 0; }
.tag { font: 600 11px var(--font-mono); text-transform: uppercase; padding: 1px 6px; border-radius: 4px; border: 1px solid currentColor; white-space: nowrap; }
.tag.pass { color: var(--muted); } .tag.fail { color: var(--fg); font-weight: 700; } .tag.muted { color: var(--muted); }
.tag.veto { color: var(--surface); background: var(--fg); border-color: var(--fg); font-weight: 700; }
.key p { margin: 4px 0; font-size: .88rem; color: var(--muted); } .key b { color: var(--fg); }
div.key { border-left: 3px solid var(--line); padding: 2px 0 2px 12px; }
.legend .dotl { display: inline-block; width: 18px; height: 0; border-top: 2px dotted var(--faint); vertical-align: middle; margin-right: 6px; }
.chart path[stroke="var(--faint)"] { stroke-dasharray: 2 4; }
.cw { background:
    linear-gradient(to right, var(--surface) 40%, transparent) left / 32px 100% no-repeat local,
    linear-gradient(to left, var(--surface) 40%, transparent) right / 32px 100% no-repeat local,
    linear-gradient(to right, color-mix(in srgb, var(--fg) 22%, transparent), transparent) left / 14px 100% no-repeat scroll,
    linear-gradient(to left, color-mix(in srgb, var(--fg) 22%, transparent), transparent) right / 14px 100% no-repeat scroll; }
.swipe { display: none; font-size: .8rem; color: var(--muted); margin: 2px 0 0; }
@media (max-width: 760px) { .swipe { display: block; } }
details.rnd > summary { cursor: pointer; } details.rnd { margin-bottom: 10px; }
.chart path[stroke="var(--muted)"] { stroke-dasharray: 5 4; }
@media (max-width: 760px) { .moves thead { display: none; } .moves, .moves tbody, .moves tr, .moves th, .moves td { display: block; width: auto; }
  .moves tr { border-bottom: 1px solid var(--line); padding: 8px 0; } .moves td { border: 0; padding: 2px 0; }
  .moves td::before { display: block; font: 600 11px var(--font-mono); color: var(--muted); text-transform: uppercase; letter-spacing: .04em; } }
"""


def moves_css():
    """Phone-only card labels for the moves table (inside the media query, so the desktop table has none)."""
    return "@media (max-width: 760px) { " + "".join(f'.moves td:nth-of-type({i + 1})::before {{ content: "{NAME[s]}"; }} ' for i, s in enumerate(SIDES)) + "}"


# ─────────────────────────────── what Embraer's choice did ───────────────────────────────
def emb_flip_table():
    if not W:
        return ""
    pl, fl = W["played"], W["flipped"]
    head = ["Company", "As played", "If Embraer had " + ("held" if W["embraer_2030_order"] == "launch" else "launched") + " in 2030", "Difference"]
    rows = [[NAME[s], b(pl["value"][s]), b(fl["value"][s]), b(fl["value"][s] - pl["value"][s])] for s in SIDES]
    return K.table(head, rows, num_cols=(1, 2, 3))


def emb_flip_market():
    if not W:
        return ""
    pl, fl = W["played"], W["flipped"]
    head = ["Year", "Embraer deliveries", "Boeing deliveries, as played", "Boeing deliveries, with Embraer", "Boeing's price cut", "Boeing profit change $B",
            "Boeing net debt, as played", "with Embraer"]
    rows = []
    for y in KEY:
        k = str(y)
        rows.append([k, n0(fl["embraer_units"][k]), n0(pl["boeing_nb_units"][k]), n0(fl["boeing_nb_units"][k]), pc(fl["boeing_cut"][k]),
                     K.num(fl["boeing_profit"][k] - pl["boeing_profit"][k], "+.2f"),
                     f'{pl["boeing_debt"].get(k, 0.0):.1f}', f'{fl["boeing_debt"].get(k, 0.0):.1f}'])
    head, rows, _ = drop_flat(head, rows)
    return K.table(head, rows, num_cols=tuple(range(1, len(head))))


def flip_debt_flat():
    """True when Boeing's net debt is the same in every key year, with and without Embraer's jet."""
    pl, fl = W["played"], W["flipped"]
    v = {round(pl["boeing_debt"].get(str(y), 0.0), 1) for y in KEY} | {round(fl["boeing_debt"].get(str(y), 0.0), 1) for y in KEY}
    return v.pop() if len(v) == 1 else None


def break_even_table():
    if not W:
        return ""
    be = W["break_even"]
    o = EMB_OPT
    rows = [["Korea's share of the bill", pc(o["partner_share"], 0), pc(be["partner_share"], 0) if be["partner_share"] is not None else "not reachable",
             f"Embraer's own share falls from {pc(be['own_share'], 0)} to {pc(1 - be['partner_share'] - o['supplier_share'] - o['state_share'], 0)}" if be["partner_share"] is not None else ""],
            ["Operating margin", pc(o["margin"], 0), pc(be["margin"], 1) if be["margin"] is not None else "not reachable", "against 13% on the A320neo and 26% on a new-generation type"],
            ["Line peak rate (a month)", f"{o['peak_a_month']:.0f}", f"{be['peak_a_month']:.0f}" if be["peak_a_month"] is not None else "not reachable", "Embraer's best was about 9 E-Jets a month"],
            ["Development bill", f"${o['bill_b']:.1f}B", f"${be['bill_b']:.1f}B" if be["bill_b"] is not None else "not reachable", "with the same 55% own share"],
            ["No US tariff cut", f"{pc(o['us_tariff_share_cut'], 0)} fewer customers", "not reached",
             f"with no tariff cut the launch is still {b(be['no_tariff'])}, against {b(be['base'])}: Embraer's line is full anyway, so the tariff barely matters"]]
    return K.table(["Lever (one at a time)", "This game", "Break-even", "Note"], rows)


# ─────────────────────────────── per-round decision summaries ───────────────────────────────
def col_index(txt, n):
    m = re.search(r"\bS(\d+)\b", txt or "")
    return int(m.group(1)) - 1 if m else 0


def grid(n, side):
    return C["grids"][str(n)][side]


def row(n, side, plan):
    for r in grid(n, side)["rows"]:
        if r["plan"] == plan:
            return r["cells"]
    return None


def boeing_round_rows():
    out = []
    for r in C["rounds"]:
        n = r["round"]
        g = grid(n, "boeing")
        x = REC(n)["boeing"]
        j = col_index((x.get("decision") or {}).get("expected_scenario"), n)
        dn = row(n, "boeing", "fps: hold + 787: hold")
        solo = [p for p in g["rows"] if p["plan"].startswith("fps ") and "Embraer" not in p["plan"]]
        alone = [(p["plan"], p["cells"][j] - dn[j]) for p in solo if "787: hold" in p["plan"]]
        withre = [(p["plan"], p["cells"][j] - dn[j]) for p in solo if "787 Re-engine" in p["plan"]]
        bf = max(alone, key=lambda t: t[1]) if alone else ("—", 0.0)
        bfr = max(withre, key=lambda t: t[1]) if withre else None
        re_ = row(n, "boeing", "fps: hold + 787 Re-engine")
        re_gap = (re_[j] - dn[j]) if re_ else None
        re_worst = min(a - b_ for a, b_ in zip(re_, dn)) if re_ else None
        sc = g["scenarios"]
        emb_col = [k for k, s_ in enumerate(sc) if s_.startswith("Embraer launches")]
        emb_hit = (dn[emb_col[0]] - dn[0]) if emb_col else None
        # with NGSA launched (as happened in 2030), the brief's "NGSA + Embraer" column against "NGSA"
        k_n = sc.index("Airbus launches NGSA") if "Airbus launches NGSA" in sc else None
        k_ne = sc.index("Airbus launches NGSA + Embraer launches") if "Airbus launches NGSA + Embraer launches" in sc else None
        emb_hit_ngsa = (dn[k_ne] - dn[k_n]) if k_n is not None and k_ne is not None else None
        vet = [(s_, v.get("plan", "")) for s_ in ("cfo", "ops") for v in ((x.get(s_) or {}).get("vetoes") or []) if v.get("binding")]
        passed = [v.get("plan", "") for v in ((x.get("cfo") or {}).get("vetoes") or [])
                  if not v.get("binding") and re.search(r"fps: launch_", v.get("plan", "")) and re.match(r"Not a veto\. The row passes", v.get("ground", ""))]
        out.append({"year": r["year"], "expected": sc[j], "best_fps": bf, "best_fps_re": bfr, "re787": re_gap, "re787_worst": re_worst,
                    "emb_hit": emb_hit, "emb_hit_ngsa": emb_hit_ngsa, "vetoes": vet, "passed": passed,
                    "board_items": x.get("board_items") or [], "board_vetoed": x.get("board_vetoed") or [], "orders": r["orders"]["boeing"]})
    return out


# what struck Airbus's A350 Re-engine in each round: the binding vetoes on its rows, by the reason they name
AB_REASON = [(r"Peak cash|peak-cash", "peak cash over the $5.2B line"), (r"rule 6", "one new launch a round (rule 6)"),
             (r"added-move robustness|\$1B launch condition", "the $1B launch condition"), (r"robustness test", "robustness against Do Nothing"),
             (r"A350F and Spirit absorption", "A350F and Spirit absorption"), (r"production-readiness test on the engine", "engine readiness")]
SEAT_LBL = {"cfo": "CFO", "ops": "head of Commercial Aircraft"}


def airbus_re_struck(x):
    out = []
    for seat in ("cfo", "ops"):
        for v in (x.get(seat) or {}).get("vetoes") or []:
            if v.get("binding") and "A350 Re-engine" in v.get("plan", "") and not re.search(r"\bcancel", v.get("plan", ""), re.I):
                lab = next((l for pat, l in AB_REASON if re.search(pat, v.get("ground", "")[:90])), None)
                assert lab, ("unlabelled Airbus veto", v.get("ground", "")[:80])
                out.append(f"{SEAT_LBL[seat]}: {lab}")
    return list(dict.fromkeys(out))


def airbus_round_rows():
    out = []
    for r in C["rounds"]:
        n = r["round"]
        g = grid(n, "airbus")
        x = REC(n)["airbus"]
        j = col_index((x.get("decision") or {}).get("expected_scenario"), n)
        best = max(g["rows"], key=lambda p: p["cells"][j])
        clean_rows = [p for p in g["rows"] if "Delay Tactics" not in p["plan"]]
        best_c = max(clean_rows, key=lambda p: p["cells"][j])
        hold = row(n, "airbus", "NGSA: hold (A320 Alt plan) + A350: hold") if n > 1 else None
        re_row = row(n, "airbus", "NGSA: hold (A320 Alt plan) + A350 Re-engine") if n > 1 else None
        out.append({"year": r["year"], "round": n, "expected": g["scenarios"][j], "best": (best["plan"], best["cells"][j]),
                    "best_clean": (best_c["plan"], best_c["cells"][j]),
                    "re_lead": (re_row[j] - hold[j]) if hold and re_row else None,
                    "struck": airbus_re_struck(x),
                    "chosen": move_txt_r("airbus", r["orders"]["airbus"], n), "board_items": x.get("board_items") or [],
                    "board_vetoed": x.get("board_vetoed") or []})
    return out


def embraer_round_rows():
    out = []
    for r in C["rounds"]:
        n = r["round"]
        g = grid(n, "embraer")
        la = row(n, "embraer", "Launch the new narrowbody with Korea")
        x = REC(n)["embraer"]
        full = [FULLWIN.get((n, "Launch the new narrowbody with Korea", c), v) for c, v in zip(g["scenarios"], la)] if la else None
        out.append({"year": r["year"], "launch": la, "launch_full": full, "scen": g["scenarios"], "chosen": move_txt("embraer", r["orders"]["embraer"]),
                    "cfo": [(t.get("name", ""), t.get("result", "")) for t in (x.get("cfo") or {}).get("tests", [])[:3]],
                    "ops_window": next((t.get("result") for t in (x.get("ops") or {}).get("tests", []) if "window" in t.get("name", "").lower()), "")})
    return out


VETO_PLAN = {"launch_10yr": "10-year", "launch_7yr": "7-year", "launch_via_embraer": "via Embraer"}


def veto_txt(vs, passed=()):
    """Binding vetoes by seat, naming the fps forms struck ('alone' when the veto covers the fps without the 787
    Re-engine), and any fps plan the CFO's buffer test passed."""
    if not vs:
        return "none"
    by = {}
    for seat, plan in vs:
        m = re.search(r"fps: (launch_\w+)( alone)?", plan)
        by.setdefault(seat, []).append((VETO_PLAN.get(m.group(1), m.group(1)) + (" alone" if m.group(2) else "")) if m else short(plan, 40))
    seat_lbl = {"cfo": "CFO's buffer test", "ops": "operating head's KPI test"}
    txt = "; ".join(f"{seat_lbl[k]} on the fps {', '.join(dict.fromkeys(v))}" for k, v in by.items())
    for p_ in passed:
        m = re.search(r"fps: (launch_\w+)", p_)
        if m and "re787: launch" in p_:
            txt += f" (the {VETO_PLAN.get(m.group(1), m.group(1))} with the 787 Re-engine passed)"
    return txt


BOARD_ITEM = {"ngsa": "the NGSA launch", "a320_plan": "the A320 Alt plan", "rea350": "the A350 Re-engine", "fps": "the fps", "re787": "the 787 Re-engine",
              "rate_737": "the 737 Rate Increase", "enb": "the Embraer launch", "delay_tactics": "Delay Tactics"}


def board_txt(x):
    f = lambda xs: " and ".join(BOARD_ITEM.get(k, clean(k)) for k in xs)
    return ("vetoed " + f(x["board_vetoed"])) if x["board_vetoed"] else ("approved " + f(x["board_items"])) if x["board_items"] else "no Board item"


def plan_lbl(p, n=2):
    p = p.replace(" + 787: hold", "").replace("fps 10-yr", "10-year fps").replace("fps 7-yr", "7-year fps")
    p = p.replace("NGSA: hold", "NGSA not launched" if n == 1 else "NGSA continuing")
    return p.replace("A350: hold", "A350 held")


def boeing_summary_table(rows):
    head = ["Round", "CEO's expected column", "Best fps on its own (787 held) against Do Nothing there", "Best fps with the 787 Re-engine",
            "787 Re-engine against Do Nothing (worst column)", "If Embraer launched that round: Boeing's value change (against rivals holding)",
            "Binding vetoes raised in the tests", "Board", "Orders"]
    body = []
    for x in rows:
        body.append([str(x["year"]), esc(clean(x["expected"])), f'{esc(plan_lbl(x["best_fps"][0]))}: {b(x["best_fps"][1])}',
                     (b(x["best_fps_re"][1]) if x["best_fps_re"] else "—"),
                     (f'{b(x["re787"])} ({b(x["re787_worst"])})' if x["re787"] is not None else "—"),
                     (b(x["emb_hit"]) if x["emb_hit"] is not None else "—"),
                     esc(veto_txt(x["vetoes"], x["passed"])),
                     esc(board_txt(x)), esc(move_txt("boeing", x["orders"]))])
    return K.table(head, body)


def airbus_summary_table(rows):
    head = ["Round", "CEO's expected column", "Best grid plan there", "Best plan without Delay Tactics", "What struck the A350 Re-engine (binding vetoes)",
            "Orders", "Board"]
    body = [[str(x["year"]), esc(clean(x["expected"])), f'{esc(plan_lbl(x["best"][0], x["round"]))}: {b(x["best"][1])}',
             ("same" if x["best_clean"][0] == x["best"][0] else f'{esc(plan_lbl(x["best_clean"][0], x["round"]))}: {b(x["best_clean"][1])}'),
             esc("; ".join(x["struck"]) or "none"), esc(x["chosen"]), esc(board_txt(x))] for x in rows]
    return K.table(head, body)


def embraer_summary_table(rows):
    head = ["Round", "Launch against Do Nothing, by column (as briefed)", "CFO's funding test (legs 1-3)", "Market window (operating head)", "Orders"]
    body = []
    for x in rows:
        if x["launch"]:
            cols = "; ".join(f"{esc(clean(s_))} {b(v)}" + (f' <span class="muted">(full window {b(f_)})</span>' if abs(f_ - v) > 1e-9 else "")
                             for s_, v, f_ in zip(x["scen"], x["launch"], x["launch_full"]))
        else:
            cols = "—"
        body.append([str(x["year"]), cols, esc(", ".join(r for _, r in x["cfo"])), esc(x["ops_window"] or "—"), esc(x["chosen"])])
    return K.table(head, body)


# ─────────────────────────────── page ───────────────────────────────
def first_year_at(rows, key, level):
    for r in rows:
        if r.get(key) is not None and r["year"] >= 2027 and r[key] <= level + 1e-9:
            return r["year"]
    return None


def tiles():
    fin = C["rounds"][-1]
    bv = fin["value"]["boeing"]
    pv = P["rounds"][-1]["value"]["boeing"]
    H = C["debt_inputs"]["historical_level_b"]
    rep = first_year_at(C["boeing_fin"], "debt", H)
    srep = first_year_at(C["boeing_fin"], "debt_stress", H)
    held = all((r["debt"] or 0) <= H + 1e-9 for r in C["boeing_fin"] if r["year"] >= (rep or 9999))
    sheld = all((r["debt_stress"] or 0) <= H + 1e-9 for r in C["boeing_fin"] if r["year"] >= (srep or 9999))
    er = embraer_round_rows() if EMB else []
    best_emb = max((max(x["launch_full"]) for x in er if x["launch"]), default=None)
    best_emb_y = next((x["year"] for x in er if x["launch"] and max(x["launch_full"]) == best_emb), None)
    bx = next((x for x in er if x["year"] == best_emb_y), None)
    best_brief = max(bx["launch"]) if bx else None
    best_brief_col = clean(bx["scen"][bx["launch"].index(best_brief)]) if bx else ""
    rec4 = REC_VALUE[NR]["boeing"]
    t = [("Boeing's value, end of game", bp(bv), f"against the status quo (PV at 2026), after four rounds of Do Nothing; {b(pv)} in the previous game"
          + (f". The 2050 record shows {b(rec4)}: it counts the political cost from 2050, not 2045" if abs(rec4 - bv) > 0.005 else "")),
         ("Boeing's share of single-aisle deliveries", f"{pc(MK[2030]['sh_boeing'], 0)} → {pc(MK[2050]['sh_boeing'], 0)}",
          f"2030 to 2050, as the MAX phases out and NGSA ramps; {pc(MK[2060]['sh_boeing'], 0)} in 2060"),
         ("Boeing's net debt", f"back to ${H:.0f}B in {rep}" if rep else "not repaired",
          f"the historical level (${H:.0f}B, {esc(C['debt_inputs']['historical_label'].replace('-$', '−$').replace('its ', 'Boeing' + chr(39) + 's ', 1))}), {'held to 2060' if held else 'not held'}; the stress case "
          f"(free cash flow a third lower) gets there in {srep}{' and holds' if sheld else ''}")]
    if EMB:
        t.append(("Embraer's new narrowbody", "Never launched",
                  f"its best launch case was {b(best_emb)} ({best_emb_y}, rivals hold, counted over its full 20 years; as briefed the best was "
                  f"{b(best_brief)}, in the column ‘{best_brief_col}’); its CFO's binding funding test failed in every round"))
    return '<div class="tiles">' + "".join(f'<div class="panel tile"><div class="k">{esc(k)}</div><div class="v">{esc(v)}</div><div class="d">{d}</div></div>' for k, v, d in t) + "</div>"


def politics_table():
    if not W:
        return ""
    po = W["politics"]
    rows = [["Governments carry part of the fps bill", f"{pc(POL.get('boeing_cofund', 0), 0)} of the bill (state siting packages, federal research money)",
             b(po["terms"]["government_cofunding"]) + " (no fps launched)", "on a 10-year fps launched in 2030 it was worth about $0.30B, plus $0.17B less debt penalty"],
            ["Political cost of leaving the narrowbody market", f"{pc(POL.get('exit_p', 0), 0)} chance × ${POL.get('exit_loss_b', 0):.2f}B a year of defence profit, "
             f"for 20 years from {POL.get('exit_from', 2045)} (Boeing had no fps from then on)",
             b(po["terms"]["political_exit_cost"]),
             f"charged to every plan with no fps. A brief counts it from the later of {POL.get('exit_from', 2045)} and its round, since earlier years are "
             f"sunk whatever is chosen: {b(-po['exit_cost_2030'])} in the 2030-45 briefs, {b(-po['exit_cost_2050'])} in 2050"],
            ["Boeing's value without the political terms", "—", b(po["boeing_without"]), f"with them: {b(po['boeing_with'])}"]]
    if EMB:
        rows.append(["US tariffs on Embraer's jets", f"{pc(EMB_OPT.get('us_tariff_share_cut', 0), 0)} fewer new customers for Embraer", "—",
                     f"a 2030 launch without it: {b(W['break_even']['no_tariff'])} against {b(W['break_even']['base'])}; Embraer's line is full anyway"])
        rows.append(["Korea, suppliers and Brazil carry part of Embraer's bill",
                     f"{pc(EMB_OPT['partner_share'], 0)} Korea, {pc(EMB_OPT['supplier_share'], 0)} suppliers, {pc(EMB_OPT['state_share'], 0)} Brazil's state", "—",
                     f"Embraer still carries {pc(W['break_even']['own_share'], 0)} (${EMB_OPT['bill_b'] * W['break_even']['own_share']:.1f}B)"])
    return K.table(["Political term", "As set in this game", "Effect on the final value", "Note"], rows, num_cols=(2,))


def compare_table():
    head = ["Round"] + [f"{NAME[s]}: this game / previous" for s in ("boeing", "airbus", "cfm", "pratt_whitney", "rolls_royce")]
    rows = []
    for rc, rp in zip(C["rounds"], P["rounds"]):
        cells = [str(rc["year"])]
        for s in ("boeing", "airbus", "cfm", "pratt_whitney", "rolls_royce"):
            a, p_ = move_txt_r(s, rc["orders"][s], rc["round"]), move_txt_r(s, rp["orders"][s], rp["round"])
            cells.append(esc(a) + ("" if a == p_ else f' <span class="muted">/ {esc(p_)}</span>'))
        rows.append(cells)
    return K.table(head, rows).replace("<table>", '<table class="cmp">', 1)


def section(title, inner, sid=None):
    return f'<section{f" id={sid}" if sid else ""}><h2>{esc(title)}</h2>{inner}</section>'


def panel(inner, title=None, cap=None):
    return ('<div class="panel">' + (f'<p class="ctitle">{title}</p>' if title else "") + inner +
            (f'<p class="cap">{cap}</p>' if cap else "") + "</div>")


def build(out_path, text):
    """text: the page's narrative strings (lede, captions), written in narrative() from the same data."""
    br = C["rounds"][-1]["bridge"]["boeing"]
    pbr = P["rounds"][-1]["bridge"]["boeing"]
    swipe = '<p class="swipe">Swipe the chart sideways for later years.</p>'
    share_svg = share_chart()
    share_key = [("Boeing", "s1", "solid"), ("Airbus", "s2", "solid"), ("COMAC", "comac", "solid")] + \
                ([("Embraer", "s3", "solid")] if EMB_DLV else []) + [("Boeing, previous game", "muted", "dash")]
    nav = [("fin", "Boeing's financials"), ("mkt", "Market shares"), ("boeing", "How Boeing decided"), ("airbus", "How Airbus decided")] + \
          ([("embraer", "Embraer")] if EMB else []) + [("politics", "Politics"), ("prev", "Against the previous game"), ("method", "How it was run")]
    body = [
        f'<header class="top"><p class="eyebrow">Boeing Product Development · war game rerun · six players · BOEING PROPRIETARY</p>'
        f'<h1>{esc(text["h1"])}</h1><p class="lede">{text["lede"]}</p><p class="gloss">{text["gloss"]}</p><p class="gloss">{text["terms"]}</p>'
        f'<nav class="toc" aria-label="Sections">{"".join(f"<a href=#{k}>{esc(v)}</a>" for k, v in nav)}</nav></header>',
        f'<section style="margin-top:18px">{tiles()}</section>',
        section("What each company did", panel(moves_table(C), cap=text["moves_cap"]), "moves"),
        section("Boeing's financials", '<div class="stack">' +
                panel(f'<div class="cw">{profit_chart()}</div>{swipe}{legend(PROFIT_KEY)}', text["profit_title"], text["profit_cap"]) +
                panel(f'<div class="cw">{debt_chart()}</div>{swipe}{legend(DEBT_KEY)}', text["debt_title"], text["debt_cap"]) +
                panel(fin_table(), "Boeing by year: deliveries, P&amp;L and cash", text["fin_cap"]) +
                panel(bridge_table(br, pbr), "Boeing's value against the status quo, by component", text["bridge_cap"]) + "</div>", "fin"),
        section("Market shares", '<div class="stack">' +
                panel(f'<div class="cw only-wide">{deliveries_chart()}</div><div class="cw only-narrow">{deliveries_chart(True)}</div>'
                      '<div class="legend"><span><i class="sq" style="background:var(--s1)"></i>Boeing</span><span><i class="sq" style="background:var(--s2)"></i>Airbus</span>'
                      '<span><i class="sq" style="background:var(--comac)"></i>COMAC</span>' + ('<span><i class="sq" style="background:var(--s3)"></i>Embraer</span>' if EMB_DLV else "") +
                      '<span><i class="solid" style="border-top-color:var(--fg)"></i>Demand</span></div>', text["mkt_title"], text["mkt_cap"]) +
                panel(f'<div class="cw">{share_svg}</div>{swipe}{legend(share_key)}', text["share_title"], text["share_cap"]) +
                panel(share_table(), "Deliveries and shares by year", text["share_tab_cap"]) + "</div>", "mkt"),
        section("How Boeing decided, round by round", panel(boeing_summary_table(boeing_round_rows()), cap=text["boeing_dec_cap"]) + chains_section("boeing"), "boeing"),
        section("How Airbus decided, round by round", panel(airbus_summary_table(airbus_round_rows()), cap=text["airbus_dec_cap"]) + chains_section("airbus"), "airbus"),
    ]
    if EMB:
        body.append(section("Embraer, the third airframer", panel(embraer_summary_table(embraer_round_rows()), cap=text["emb_dec_cap"]) +
                            panel(break_even_table(), "What would make Embraer's 2030 launch pay", text["be_cap"]) +
                            panel(emb_flip_table(), "If Embraer had launched in 2030", text["flip_cap"]) +
                            panel(emb_flip_market(), "Boeing with and without Embraer's jet", text["flip_mkt_cap"]) +
                            chains_section("embraer"), "embraer"))
    body.append(section("Politics in the payoffs", panel(politics_table(), cap=text["pol_cap"]), "politics"))
    body.append(section("Against the previous game", panel(compare_table(), cap=text["cmp_cap"]) + panel(value_table(), "Every company's value after each round", text["val_cap"]), "prev"))
    body.append(section("How this game was run", panel(f'<ul class="cav">{text["method"]}</ul>'), "method"))
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Six-Player Rerun</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{K.CSS + CSS_EXTRA + moves_css()}</style></head><body><div class="wrap">
{"".join(body)}
<footer><p>BOEING PROPRIETARY. The Boeing-Airbus game board, MAX phase-out world, with Embraer and political terms, against the previous MAX phase-out game. Values are $B, present value at 2026, against the status quo; Boeing's cash and net debt come from the game master's balance-sheet tracker in 2026 dollars.</p></footer>
</div><script>{K.JS}</script></body></html>'''
    open(out_path, "w").write(page)
    return page


# ─────────────────────────────── narrative (every number from the data; claims asserted) ───────────────────────────────
def spans(years):
    """[2037, 2038, 2045, 2046] -> '2037-38 and 2045-46'."""
    out, run = [], []
    for y in sorted(years):
        if run and y == run[-1] + 1:
            run.append(y)
        else:
            if run:
                out.append(run)
            run = [y]
    if run:
        out.append(run)
    lab = [str(r[0]) if len(r) == 1 else f"{r[0]}-{str(r[-1])[2:]}" for r in out]
    return lab[0] if len(lab) == 1 else ", ".join(lab[:-1]) + " and " + lab[-1]


def rec_text(n, side):
    return json.dumps(REC(n)[side], ensure_ascii=False)


def narrative():
    R4 = C["rounds"][-1]
    V, PVv = R4["value"], P["rounds"][-1]["value"]
    br, pbr = R4["bridge"]["boeing"], P["rounds"][-1]["bridge"]["boeing"]
    BR, AR, ER = boeing_round_rows(), airbus_round_rows(), embraer_round_rows()
    yrs = range(2026, 2061)
    # claims the copy makes, checked against the record
    assert all(move_txt("boeing", r["orders"]["boeing"]) == "Do Nothing" for r in C["rounds"]), "Boeing did something"
    assert all(move_txt("embraer", r["orders"]["embraer"]) == "Do Nothing" for r in C["rounds"]), "Embraer launched"
    assert C["rounds"][0]["orders"]["airbus"]["ngsa"] == "launch"
    assert all(move_txt("airbus", r["orders"]["airbus"]) in ("Do Nothing", "A320 Alt plan") for r in C["rounds"][1:])
    assert all(max(x["launch_full"]) < 0 for x in ER), "an Embraer launch was positive"
    assert all(x["best_fps"][1] < -1.0 for x in BR)
    assert all(any(s_ == "cfo" for s_, _ in x["vetoes"]) for x in BR)
    assert all(not x["passed"] for x in BR[:-1]) and BR[-1]["passed"], "the CFO's buffer test passed an fps plan before 2050, or none in 2050"
    e_full = {x["year"]: x["launch_full"] for x in ER}
    e_brief = {x["year"]: x["launch"] for x in ER}
    be = W["break_even"]
    fl, pl = W["flipped"]["value"], W["played"]["value"]
    cof = W["cofund"]
    cf = lambda y: cof[str(y)]["fps 10-yr at Renton"]
    H = C["debt_inputs"]["historical_level_b"]
    rep = first_year_at(C["boeing_fin"], "debt", H)
    srep = first_year_at(C["boeing_fin"], "debt_stress", H)
    own = sum(r["owners"] or 0 for r in C["boeing_fin"])
    sd_d = br["supply_demand"] - pbr["supply_demand"]
    a_d = V["airbus"] - PVv["airbus"]
    a_sd = R4["bridge"]["airbus"]["supply_demand"] - P["rounds"][-1]["bridge"]["airbus"]["supply_demand"]
    pmax = max(FIN[y]["profit"] for y in yrs)
    peak = [y for y in yrs if abs(FIN[y]["profit"] - pmax) < 1e-6]
    last_max = max(y for y in yrs if MK[y]["max"] > 0.5)
    gap_sq = [y for y in yrs if abs(FIN[y]["profit"] - FIN[y]["sq_profit"]) > 1e-3]
    worst_sq = min(gap_sq, key=lambda y: FIN[y]["profit"] - FIN[y]["sq_profit"])
    gap_pv = [y for y in yrs if abs(FIN[y]["profit"] - PFIN[y]["profit"]) > 1e-3]
    ent = [y for y in yrs if PMK[y]["entrant"] > 0.5 and y < min(gap_pv)]
    ent_lo, ent_hi = min(PMK[y]["entrant"] for y in ent), max(PMK[y]["entrant"] for y in ent)
    bsh = {int(k): v for k, v in W["played"]["boeing_board_share"].items()}
    sh0 = bsh[2030]
    sh_dn = min(y for y in yrs if bsh[y] < sh0 - 1e-6)
    sh_lo = min(bsh.values())
    sh_end = min(y for y in yrs if abs(bsh[y] - sh_lo) < 1e-6)
    lead = int(EMB_OPT.get("lead", 1)) if "lead" in EMB_OPT else 1
    cut_from = 2030 + EMB_OPT["dev_years"] - lead
    cut_full = cut_from + int(EMB_OPT["ramp_years"]) - 1
    # Boeing 2050: the one fps plan the CFO's buffer test passed, and why the CEO struck it
    g4 = grid(NR, "boeing")
    k_risk = next(i for i, x in enumerate(g4["scenarios"]) if x.startswith("Risk case"))
    j4 = col_index(REC(NR)["boeing"]["decision"]["expected_scenario"], NR)
    dn4, re4 = row(NR, "boeing", "fps: hold + 787: hold"), row(NR, "boeing", "fps 10-yr at Renton + 787 Re-engine")
    al4 = row(NR, "boeing", "fps 10-yr at Renton + 787: hold")
    ns4 = row(NR, "boeing", "fps 10-yr + 787 Re-engine")          # the same plan at new sites
    lim4 = dn4[k_risk] - 2.0
    best4 = max(r["cells"][j4] for r in g4["rows"])
    assert re4[k_risk] >= lim4 > al4[k_risk], "the 2050 buffer-test facts changed"
    assert ns4[k_risk] >= lim4 and re4[j4] > ns4[j4], "the 2050 new-sites row's facts changed"
    assert "Not a veto. The row passes my buffer test" in rec_text(NR, "boeing") and "H8" in REC(NR)["boeing"]["decision"]["rationale"]
    # Airbus: the record's own reasons
    t1, t2, t3, t4 = (rec_text(n, "airbus") for n in (1, 2, 3, 4))
    assert "-0.64 against Do Nothing" in t1 and "$48.32B fine" in t1 and "five pillars" in t1.lower() + t1
    assert "6.67B" in t2 and "declined the override" in t2 and "rule 4" in t2
    assert "no override is possible" in t3 and "two binding soft vetoes" in t4 and "No maker has an A350 engine programme on the record" in t4
    re2_lead = AR[1]["re_lead"]
    assert AR[1]["best"][0] != AR[1]["best_clean"][0] and "Delay Tactics" in AR[1]["best"][0] and re2_lead > 1.0
    assert AR[2]["re_lead"] < 1.0 and AR[3]["re_lead"] < 1.0
    rec4 = REC_VALUE[NR]["boeing"]
    po = W["politics"]
    T = {}
    T["h1"] = "With Embraer and politics in the game, nobody new launches a narrowbody after Airbus"
    T["lede"] = (
        f"The MAX phase-out game, replayed with <b>Embraer as a sixth player</b> and <b>political terms in the payoffs</b>. "
        f"Embraer can launch a new 150-180 seat narrowbody with Team Korea in any round. It enters service four years later "
        f"({EMB_OPT['dev_years'] + 2030} for a 2030 launch, before 2035 as you asked). It is slightly better for airlines than the 737 MAX and A320neo "
        f"and worse than a new-generation fps or NGSA, so it wins {pc(EMB_OPT['share_by_newgen'][0] * (1 - EMB_OPT['us_tariff_share_cut']), 1)} of new customers while "
        f"neither is in service, {pc(EMB_OPT['share_by_newgen'][1] * (1 - EMB_OPT['us_tariff_share_cut']), 1)} with one and {pc(EMB_OPT['share_by_newgen'][2] * (1 - EMB_OPT['us_tariff_share_cut']), 1)} with both, "
        f"after a cut for US tariffs, on a line rising to {EMB_OPT['peak_a_month']:.0f} a month. Its campaigns would cut single-aisle prices by "
        f"{pc(EMB_OPT['cut'], 0)}, or {pc(EMB_OPT['cut'] * EMB_OPT['cut_boeing_no_fps_mult'], 1)} on Boeing's MAX while Boeing has no fps, from a year before "
        f"it enters service ({cut_from} for a 2030 launch), rising evenly to the full cut in {cut_full}. "
        f"Embraer's executives and Board were profiled from its own calls to May 2026 and played its seat like every other company. "
        f"<b>What happened:</b> Airbus launched NGSA in 2030 (in service 2037), as in the previous game. Boeing did nothing in all four rounds. "
        f"Embraer held in all four: its launch was below zero in every column of every brief ({b(max(e_full[2030]))} at best in 2030, "
        f"{b(max(e_full[2050]))} in 2050 counted over its full 20 years), so its CFO's funding test failed each time. The engine makers moved less than "
        f"before. Boeing ends at {b(V['boeing'])} against the status quo ({b(PVv['boeing'])} in the previous game), and its share of single-aisle "
        f"deliveries falls from {pc(MK[2030]['sh_boeing'], 0)} in 2030 to {pc(MK[2050]['sh_boeing'], 0)} in 2050 and to none in {last_max + 1}: "
        f"the last MAX is built in {last_max}.")
    T["gloss"] = ("<b>How to read the figures.</b> Values are $B, present value at 2026, against the <b>status quo</b>, in which nobody launches "
                  "anything (and Embraer builds no airliner). <b>Do Nothing</b> is Boeing launching nothing while the others move. Each round every "
                  "company's ExCo gets a brief: a grid that values each of its plans against the moves its rivals could make that round, one "
                  "<b>column</b> per move. The CEO names the expected column. Boeing's Board approves a launch only if it adds more than +$1B in the "
                  "expected column and loses no more than $1B in any column it finds plausible, and its CFO vetoes any plan more than $2B below "
                  "Do Nothing in the risk case. P&amp;L figures are the game's commercial-airplane model at 2026 prices; cash and net debt come "
                  "from the game master's balance-sheet tracker in 2026 dollars.")
    T["terms"] = ("<b>Terms.</b> <b>A320 Alt plan:</b> Airbus keeps its A320 lines running longer through NGSA's ramp-up, about eight years "
                  "after NGSA enters service against about five on the base plan, for about 1,500 more A320s and $0.75B; set in 2030 and kept after. "
                  "<b>fps via Embraer:</b> Boeing builds its new narrowbody with Embraer as partner; it scored below the fps on its own in every brief, "
                  "and it and Embraer's own jet exclude each other. <b>Delay Tactics:</b> covert moves to slow a rival's programme (a supplier "
                  "bottleneck, poaching engineers); with no rival programme on the public record a move is naked and draws a $48.32B fine. "
                  f"<b>Team Korea:</b> the Korean industrial partners that carry {pc(EMB_OPT['partner_share'], 0)} of Embraer's bill. "
                  "<b>Risk case:</b> Boeing's column with covert Airbus Delay Tactics (with NGSA in 2030), the column the CFO's buffer test reads.")
    T["moves_cap"] = ("Boeing and Embraer held in every round, and Airbus made its one launch in 2030 (NGSA, on the A320 Alt plan, naming all three "
                      "engine makers). NGSA's selection set off P&amp;W's GTF2, and CFM/GE upgraded the GEnx. Against the previous game: "
                      "Rolls-Royce held its UltraFan NB in 2030 (in the previous game it launched it on NGSA's selection) and committed to the Joint "
                      "Venture in 2035; Pratt &amp; Whitney never matched that commitment, so no Joint Venture formed and GTF2 stayed its own engine "
                      "on NGSA; CFM/GE launched no ducted engine and no Embraer partnership in 2035 (in the previous game it launched both).")
    T["profit_title"] = (f"Boeing's commercial profit peaks at {b(pmax, 1, False)} a year in {spans(peak)} and falls to "
                         f"{b(FIN[2060]['profit'], 1, False)} in 2060, when only the 787 is left")
    T["profit_cap"] = (
        f"Operating profit on narrowbodies and widebodies, $B a year at 2026 prices. Revenue goes from {b(FIN[2030]['revenue'], 1, False)} (2030) "
        f"to {b(FIN[2040]['revenue'], 1, False)} (2040), {b(FIN[2050]['revenue'], 1, False)} (2050) and {b(FIN[2060]['revenue'], 1, False)} (2060). "
        f"The MAX is phased out from 2045 and none is built from {last_max + 1}, in every plan and in the status quo, so Do Nothing tracks the "
        f"status quo closely: Boeing loses some customers to NGSA in {spans(gap_sq)}, most in {worst_sq} "
        f"({n0(MK[worst_sq]['sq_boeing'] - MK[worst_sq]['max'])} aircraft and {b(FIN[worst_sq]['sq_profit'] - FIN[worst_sq]['profit'], 2, False)} of profit). "
        f"The previous game follows the same path except in {spans(gap_pv)}, when Boeing delivered fewer aircraft there "
        f"({' and '.join(n0(PFIN[y]['nb_units']) for y in gap_pv)}, against {' and '.join(n0(FIN[y]['nb_units']) for y in gap_pv)} here) and earned "
        f"{' and '.join(b(FIN[y]['profit'] - PFIN[y]['profit'], 2, False) for y in gap_pv)} less: its overflow entrant had served "
        f"{n0(ent_lo)}-{n0(ent_hi)} a year of the customers waiting for a Boeing slot in {spans(ent)}.")
    T["debt_title"] = (f"Net debt is back at the historical level (${H:.0f}B) in {rep} and stays there; the stress case gets there in {srep}")
    assert all(abs((r[k] or 0.0) - H) < 1e-9 for r in C["boeing_fin"] + P["boeing_fin"] if r["year"] > DEBT_X_HI for k in ("debt", "debt_stress") if k in r and r[k] is not None)
    same_prev = all(abs((FIN[y]["debt"] or 0) - (PFIN[y]["debt"] or 0)) < 1e-6 for y in range(2027, 2061))
    T["debt_cap"] = (f"The game master's tracker, 2027-{DEBT_X_HI}; net debt is ${H:.0f}B in every later year to 2060 on all three "
                     "paths" + (" (the previous game's path is the same as this game's, so its line lies under it)" if same_prev else "") + ". It starts at the consensus end-2026 $22.5B and falls by free cash flow (the analysts' "
                     "consensus for all of Boeing to 2030, then held flat, moved only by the profit the game adds or takes away against the status quo, "
                     f"after tax, less programme cash). The <b>historical level</b> is ${H:.0f}B, "
                     f"{esc(C['debt_inputs']['historical_label'].replace('-$', '−$').replace('its ', 'Boeing' + chr(39) + 's ', 1))}. Once net debt is there, surplus cash goes to the owners: "
                     f"{b(own, 0, False)} in 2029-2060 on this path. Boeing launched nothing, so no programme cash was spent. "
                     "<b>A limit to read with it:</b> because the MAX phase-out is in the status quo too, the tracker's free cash flow does not "
                     "fall with the P&amp;L after 2045; the profit chart above shows that decline.")
    fh, frows, fgone, same_owners = fin_cols()
    def gone_phrase(h, v):
        if h.startswith("WB deliveries"):
            return f"widebody deliveries are {v} a year"
        if h.startswith("Programme cash"):
            return "no programme cash was spent" if v == "—" else f"programme cash is ${v}B a year"
        return f"{h.replace(' $B', '').lower()} is ${v}B"
    nd = [h for h, v in fgone if h.startswith("Net debt")]
    gone_l = [gone_phrase(h, v) for h, v in fgone if not h.startswith("Net debt")]
    if nd:
        who = [{"Net debt $B": "this game", "Net debt, stress $B": "its stress case", "Net debt, previous game $B": "the previous game"}[h] for h in nd]
        v0 = float(fgone[[h for h, _ in fgone].index(nd[0])][1])
        gone_l.append(f"net debt is ${v0:.0f}B in " + (who[0] if len(who) == 1 else ", ".join(who[:-1]) + " and " + who[-1]))
    gone_txt = "; ".join(gone_l)
    dcols = [h for h in fh if h.endswith("deliveries")]
    T["fin_cap"] = ((" and ".join(h.replace(" deliveries", "") for h in dcols) + " deliveries are aircraft a year; " if dcols else "")
                    + "revenue and operating profit $B at 2026 prices, Commercial Airplanes only. Free "
                    "cash flow is the whole company's consensus in 2026 dollars and does not fall with the MAX phase-out (see the limit under the "
                    "debt chart)."
                    + (" Every year's free cash flow goes to the owners, so cash for owners equals it." if same_owners else "")
                    + (f" Columns left out because they do not change in the years shown: {gone_txt}." if gone_txt else ""))
    T["bridge_cap"] = (
        f"The game board's fixed-size market (2,000 narrowbodies a year, every one delivered, with Boeing's share stepping down from "
        f"{pc(sh0, 0)} to {pc(sh_lo, 0)} in {sh_dn}-{str(sh_end)[2:]} once NGSA is in service, against {pc(sh0, 0)} throughout in the status quo) gives "
        f"{b(br['nb_profit_vs_sq'])}; supply and demand corrects it to what the factories actually deliver ({b(br['supply_demand'])}), and the "
        f"political cost of leaving the narrowbody market takes {b(br['political_exit_cost'])}, counted from {POL.get('exit_from', 2045)}. The "
        f"supply-and-demand line is {b(sd_d, 2, False)} better than in the previous game because its overflow entrant is gone (Embraer replaced it and never "
        f"launched), so Boeing keeps waiting customers that entrant took; the political cost, new in this game, more than offsets it.")
    T["mkt_title"] = (f"Airbus's NGSA and COMAC take the single-aisle market as the MAX runs down: in 2050 Boeing delivers {n0(MK[2050]['max'])}, "
                      f"Airbus {n0(MK[2050]['ngsa'])} and COMAC {n0(MK[2050]['comac'])}")
    dl = lambda y: MK[y]["max"] + MK[y]["fps"] + MK[y]["a320"] + MK[y]["ngsa"] + MK[y]["comac"] + MK[y]["embraer"] + MK[y]["entrant"]
    short_y = [y for y in yrs if dl(y) < (MK[y]["demand"] or 0) - 30]
    over_y = [y for y in yrs if dl(y) > (MK[y]["demand"] or 0) + 30]
    late_y = [y for y in yrs if y >= 2050 and dl(y) < (MK[y]["demand"] or 0) - 1]
    assert short_y and over_y and min(over_y) > max(y for y in short_y if y < min(over_y))
    T["demand_note"] = (f"Demand is each year's new demand (replacement plus growth). Customers who cannot get a delivery slot wait, and a tenth of them "
                        f"drop out each year. So deliveries fall short of demand in {spans([y for y in short_y if y < min(over_y)])}, when the lines are full, "
                        f"exceed it in {spans(over_y)} as the waiting customers are served"
                        + (f", and run slightly below it from {min(late_y)} as the MAX phases out." if late_y else "."))
    T["mkt_cap"] = ("737/A320-class aircraft delivered each year in the final state, with demand (the line). COMAC sells its capacity first to its own "
                    "customers (150 a year in 2035, 250 from 2050). Embraer built nothing, so there is no Embraer bar. " + T["demand_note"])
    T["share_title"] = (f"Boeing's share of deliveries: {pc(MK[2030]['sh_boeing'], 0)} in 2030, {pc(MK[2040]['sh_boeing'], 0)} in 2040, "
                        f"{pc(MK[2050]['sh_boeing'], 0)} in 2050, none in 2060")
    T["share_cap"] = (f"Shares of the market's deliveries. Airbus reaches {pc(MK[2060]['sh_airbus'], 0)} and COMAC {pc(MK[2060]['sh_comac'], 0)} in 2060. "
                      "Boeing's line in the previous game (dashed) is almost the same. Boeing's widebody share stays at "
                      f"{pc(MK[2050]['wb_boeing'], 0)}: nobody re-engined a widebody.")
    sh_, srows, sgone = share_cols()
    T["share_tab_cap"] = "Aircraft a year and shares of deliveries, final state. " + T["demand_note"] + (
        " Columns left out because they do not change in the years shown: " +
        "; ".join({"of which fps": f"fps deliveries are {v}", "Boeing widebody share": f"Boeing's widebody share is {v}"}.get(h, f"{h} is {v}") for h, v in sgone) + "."
        if sgone else "")
    T["boeing_dec_cap"] = (
        "Each round Boeing's chain ran: Board guidance (priorities, risk appetite, what it would approve or veto), the CEO's framing, the CFO's "
        "and the head of Commercial Airplanes' tests, the CEO's decision, their veto checks, and the Board's review of any order that differed "
        f"from Do Nothing. In {', '.join(str(x['year']) for x in BR[:-2])} and {BR[-2]['year']} the CFO's binding buffer test struck every fps plan. "
        f"In {BR[-1]['year']} it struck the 10-year fps alone, the 7-year and the fps via Embraer, but the 10-year fps with the 787 Re-engine "
        f"passed it at both sites ({b(re4[k_risk])} at Renton and {b(ns4[k_risk])} at new sites in the risk case, against a {b(lim4)} limit). The CEO "
        f"struck both on their own tests: even the Renton row, the better of the two, was {b(dn4[j4] - re4[j4], 2, False)} below Do Nothing in the "
        f"expected column, passed only on the Re-engine's {b(re4[k_risk] - al4[k_risk])}, and was {b(best4 - re4[j4], 2, False)} below the grid's "
        f"best, over the $2B cap of the money rule (H8). The best fps on its own ran from "
        f"{b(BR[0]['best_fps'][1])} ({BR[0]['year']}) to {b(BR[-1]['best_fps'][1])} ({BR[-1]['year']}) against Do Nothing in the CEO's expected column, "
        f"far from the Board's +$1B. The 787 Re-engine led Do Nothing by {b(BR[0]['re787'])} in 2030 and {b(BR[1]['re787'])} in 2035 but lost "
        f"{b(-BR[0]['re787_worst'], 2, False)} and {b(-BR[1]['re787_worst'], 2, False)} if Airbus re-engined the A350 in the same round, outside "
        f"the Board's $1B downside limit, so the CEO held it; in 2045 and 2050 its lead ({b(BR[2]['re787'])}, {b(BR[3]['re787'])}) fell short of "
        f"the +$1B business case. Against rivals holding, an Embraer launch would have cost Boeing {b(-BR[0]['emb_hit'], 2, False)} in 2030 "
        f"(with NGSA launched, as happened, the brief gives {b(BR[0]['emb_hit_ngsa'])}, close to the {b(fl['boeing'] - pl['boeing'])} of the full "
        f"replay below), falling to {b(-BR[-1]['emb_hit'], 2, False)} by 2050. No Boeing order reached the Board.")
    T["airbus_dec_cap"] = (
        "Airbus's chain is the same; its CFO and head of Commercial Aircraft hold soft vetoes the CEO can override only for a plan $1B better, "
        "and the five pillars (safety, quality, integrity, compliance, security) and the company's rules bind everyone. In 2030 it launched NGSA "
        "on its own clock (the last year of its window), with all three engine makers named. It deleted NGSA plus the A350 Re-engine on its "
        "one-launch rule and its CFO's $5.2B peak-cash line; struck the Re-engine in place of NGSA on the CFO's robustness test ($0.64B below "
        "Do Nothing in two columns) and the operating head's A350F and Spirit absorption test; and deleted every Delay Tactics row, because with "
        "no fps public any move would draw the $48.32B fine, and on the five pillars. "
        f"In 2035 the best grid row ({b(AR[1]['best'][1])}) used a Delay Tactics move and was deleted under rule 4. The best row without one, "
        f"the A350 Re-engine at {b(AR[1]['best_clean'][1])} ({b(re2_lead)} over holding), failed the CFO's binding peak-cash soft veto "
        "($6.67B a year in 2035-36 against the $5.2B line), and the CEO declined to override. "
        f"In 2045 and 2050 the Re-engine passed on cash, but it added only {b(AR[2]['re_lead'])} and {b(AR[3]['re_lead'])}, short of Airbus's $1B "
        "launch condition, so the CFO's binding soft veto struck it; in 2050 the head of Commercial Aircraft also struck it, because no maker had "
        "an A350 engine programme on the record. With a gain under $1B no override was possible, so the CEO held and logged the gap as a premium.")
    cut_rows = [x for x in ER if any(abs(f_ - v) > 1e-9 for f_, v in zip(x["launch_full"], x["launch"]))]
    cut_txt = ""
    if cut_rows:
        cnt = [2061 - (x["year"] + EMB_OPT["dev_years"]) + 1 for x in cut_rows]
        cut_txt = (" <b>A correction:</b> the briefs Embraer saw in " + " and ".join(str(x["year"]) for x in cut_rows) +
                   " counted the rivals-hold column only to 2061, " + " and ".join(str(c) for c in cnt) + " of its 20 years. Counted in full it is " +
                   " and ".join(f"{b(x['launch_full'][0])} ({x['year']})" for x in cut_rows) + ", not " +
                   " and ".join(b(x["launch"][0]) for x in cut_rows) + "; that cut is why a Boeing fps launch looked better for Embraer than rivals "
                   "holding in 2050. The launch stays below zero in every column, so the decisions stand; the engine now counts the full window.")
    T["emb_dec_cap"] = (
        "Embraer's chain: its Board (the Brazilian state holds a golden share), CEO Francisco Gomes Neto, CFO Felipe Santana (in post since May 2026, "
        "running the funding test inherited from Antonio Carlos Garcia) and Arjan Meijer, head of Commercial Aviation. The CFO's funding test is "
        "binding: Team Korea's share in the brief, the launch's value with the debt penalty at or above zero in the expected column, and no more "
        "than 5 yield points lost in the risk column. Leg 2 failed in every round. The market-window test (a soft veto) passed in 2030 and failed "
        "from 2035, once NGSA was due in service before Embraer's jet could be. The launch row shrinks toward zero from round to round only because "
        "a later launch books the loss-making programme later." + cut_txt)
    T["be_cap"] = (
        f"At the 2030 decision, with the rivals' actual orders and nobody moving after: a launch is worth {b(be['base'])} to Embraer. One lever at a "
        f"time, it breaks even if Korea carries {pc(be['partner_share'], 0)} of the bill instead of {pc(EMB_OPT['partner_share'], 0)} (Embraer's own share falling "
        f"to about {pc(1 - be['partner_share'] - EMB_OPT['supplier_share'] - EMB_OPT['state_share'], 0)}), if its margin is {pc(be['margin'], 0)} instead of "
        f"{pc(EMB_OPT['margin'], 0)}, if its line reaches {be['peak_a_month']:.0f} a month instead of {EMB_OPT['peak_a_month']:.0f}, or if the bill is "
        f"${be['bill_b']:.1f}B instead of ${EMB_OPT['bill_b']:.0f}B. Removing the US tariff cut barely helps: the line, not demand, sets its deliveries.")
    T["flip_cap"] = (
        f"The whole game replayed with every company's recorded orders, but Embraer launching in 2030 (in service 2034). Embraer loses "
        f"{b(-fl['embraer'], 2, False)}. Boeing loses {b(pl['boeing'] - fl['boeing'], 2, False)} and Airbus {b(pl['airbus'] - fl['airbus'], 2, False)}, mostly through "
        "the price cut; P&amp;W gains because Embraer's jet flies its engines. The others did not get to respond, so this is a bound on the threat, "
        "not a forecast.")
    fd = flip_debt_flat()
    T["flip_mkt_cap"] = ("Boeing's deliveries, the price cut on its aircraft and its profit with Embraer's jet in the market, against the game as played. "
                         + (f"Boeing's net debt (the tracker's) is ${fd:.0f}B in every year shown, with or without Embraer's jet." if fd is not None
                            else "Net debt is the tracker's, as above."))
    T["pol_cap"] = (
        "Boeing's terms come from the earlier politics study: US governments carry a share of an fps bill (state siting packages and federal "
        "research money, as in the past; no federal launch funding), and leaving the narrowbody market has a political cost (defence, export "
        "finance, the FAA). Boeing had no fps from 2045 on, so the final value counts that cost from 2045 "
        f"({b(br['political_exit_cost'])}); the 2050 record counted it from 2050, as that round's brief did, and shows Boeing at {b(rec4)}. "
        "Both terms are small against the fps gap. With the rivals' actual orders, governments would have to carry "
        f"{pc(cf(2030)['needed'], 0)} of the bill for a 10-year fps at Renton to clear the Board's +$1B in 2030, {pc(cf(2035)['needed'], 0)} in 2035 and "
        f"{pc(cf(2045)['needed'], 0)} in 2045, and no share is enough in 2050 (the game's 2% is worth {b(cf(2030)['as_played'] - cf(2030)['none'])} in 2030). "
        "Airbus has no cash term: its launch aid is on market terms. Embraer's partners and the US tariff are in its economics.")
    T["cmp_cap"] = "Orders that differ from the previous game are shown with the previous game's order after the slash."
    T["val_cap"] = (f"Each company's value against the status quo, with nobody moving after that round; Boeing's counts the political cost from 2045 in "
                    f"every round (the 2050 record shows {b(rec4)}). Airbus is {b(-a_d, 2, False)} {'lower' if a_d < 0 else 'higher'} than in the "
                    f"previous game, {'all' if abs(a_sd - a_d) < 0.005 else b(a_sd)} of it in supply and demand, because the overflow entrant is "
                    "gone from the market and its status quo. The engine makers differ because they moved differently.")
    T["method"] = "".join(f"<li>{x}</li>" for x in [
        "Six companies played four rounds (2030, 2035, 2045, 2050) on the Boeing-Airbus game board in the MAX phase-out world, each through its "
        "own Board and executive agents, with sealed orders and the public bulletin as the only view of rivals. The previous game is the same "
        "world with five players and no political terms.",
        "Embraer's executives and Board were built from Embraer's call transcripts (2011 to May 2026) and S&amp;P workbooks, each file checked "
        "quote by quote by an adversarial verifier (881 evidence items). Felipe Santana holds the CFO seat; Antonio Carlos Garcia's six years "
        "as CFO are the doctrine the seat inherits. Embraer's decision rule and vetoes are inferences from calls.",
        f"Embraer's economics are this game's assumptions: a ${EMB_OPT['bill_b']:.0f}B bill (industry estimates of $10-11B), Korea "
        f"{pc(EMB_OPT['partner_share'], 0)}, risk-sharing suppliers {pc(EMB_OPT['supplier_share'], 0)}, Brazilian state research money {pc(EMB_OPT['state_share'], 0)}, "
        f"${EMB_OPT['price_m']:.0f}M a jet at a {pc(EMB_OPT['margin'], 0)} margin, an {pc(EMB_OPT['wacc'], 0)} cost of capital, net debt ${EMB_OPT['debt_b']:.1f}B and "
        f"enterprise value ${EMB_OPT['ev_b']:.0f}B (the S&amp;P workbooks, converted), and the debt penalty the airframers pay. The four-year development "
        "is your premise; the earlier research put a credible entry into service no earlier than 2037.",
        "Embraer replaces the previous game's generic overflow entrant. Its first-year deliveries are lost to the firm-order backlog (all 2034 demand "
        "is served from Boeing's and Airbus's firm orders), a small understatement. It does not cannibalise the E195-E2. Its price cut applies to "
        "every single-aisle delivery, firm orders included, so the threat it shows is a little high.",
        "Engine makers count Embraer's engines (P&amp;W, or CFM with CFM's Embraer partnership).",
        f"Political exit cost: each round's brief counts it from the later of {POL.get('exit_from', 2045)} and that round, because earlier years are "
        f"sunk whatever is chosen. The values on this page follow the played path and count it from {POL.get('exit_from', 2045)}, when the MAX "
        "phase-out begins, because Boeing had no fps in service or in development from then on.",
        f"After the game a review found that a launch's 20-year window was cut at 2061 in the rivals-hold column. It affected two of the game's "
        f"{RECHECK.get('cells', 0):,} briefed cells, both Embraer's launch in the rivals-hold column (2045 and 2050), and nothing else; the engine now "
        "counts the full window, and the briefs as played are kept as the record."])
    return T


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "dash_2050_emb.html")
    page = build(out, narrative())
    print("wrote", out, len(page))
