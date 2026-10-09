"""Build exco_agents.html: the profiles of the fifteen per-executive agents (one per member of each company's default
ExCo), from data/people.json (evidence counts per person, from the profile evidence files), data/agents/<agent>.json
(each agent's profile, drafted, verified and audited against the evidence) and the evidence files themselves.
The facts the page text states are checked against the data (checks()); the build stops if any fails.

Usage: python3 make_exco_html.py [out.html]"""
import collections
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.realpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050"))
sys.path.insert(0, os.path.join(REPO, "wargame", "dashgame"))
sys.path.insert(0, HERE)
import page_kit as K  # noqa: E402
import check_agents as CA  # noqa: E402
import narrative_exco as NAR  # noqa: E402
import test_hook as TH  # noqa: E402  (case counts only; the tests run in checks())

esc = K.esc
SIDES = ["boeing", "airbus", "cfm", "pratt_whitney", "rolls_royce"]
COMPANY = {"boeing": "Boeing", "airbus": "Airbus", "cfm": "CFM/GE", "pratt_whitney": "Pratt & Whitney", "rolls_royce": "Rolls-Royce"}
SEATS = ["CEO", "CFO", "Operating head"]
PEOPLE = json.load(open(os.path.join(HERE, "data", "people.json")))
BY = {p["agent_name"]: p for p in PEOPLE}
PROF = {p["agent_name"]: json.load(open(os.path.join(HERE, "data", "agents", p["agent_name"] + ".json"))) for p in PEOPLE}
ROSTER = {s: [p["agent_name"] for p in PEOPLE if p["side"] == s] for s in SIDES}
for s in SIDES:
    ROSTER[s].sort(key=lambda a: SEATS.index(BY[a]["seat"]))
ORDER = [a for s in SIDES for a in ROSTER[s]]
SHORT = {a: BY[a]["name"].split()[-1] for a in ORDER}
PRON = {a: ("her" if a in ("boeing-pope", "rolls-royce-mccabe") else "his") for a in ORDER}

EV = CA.EV
ITEMS = collections.defaultdict(list)          # each person's own items in their evidence file (not shared JV tags)
for a, p in BY.items():
    for line in open(os.path.join(REPO, p["evidence_file"])):
        if line.strip():
            e = json.loads(line)
            if e.get("exec_id") == p["exec_id"]:
                ITEMS[a].append(e)
COMP = {}                                      # items in the company's evidence file where the person is the speaker
for a, p in BY.items():
    f = os.path.join(REPO, "wargame", "profiles", p["side"], "evidence.jsonl")
    n = 0
    if os.path.exists(f):
        for line in open(f):
            if line.strip():
                sp = (json.loads(line).get("speaker") or "").split(",")[0]
                n += bool(re.search(r"\b%s\b" % re.escape(SHORT[a]), sp))
    COMP[a] = n
PERSP = {"own_words": ("Own words", "s1"), "filing": ("Board Report text", "s2"), "observed_by_boeing": ("Remark by Boeing", "s3"),
         "observed_by_pratt_whitney": ("Remark by RTX / P&W", "s3"), "analyst_question": ("Analyst's question", "s3")}
CITE = {"own_words": "own words", "filing": "Board Report text, not speech", "observed_by_boeing": "as quoted by Boeing",
        "observed_by_pratt_whitney": "as quoted by RTX / Pratt & Whitney", "analyst_question": "an analyst's question",
        "own_behaviour": "company record", "own_behaviour_observed_by_boeing_or_analysts": "observed by Boeing or analysts"}


def volume(a):
    """Volume of the person's record: the count of items in their own words."""
    n = BY[a]["n_own_words"]
    return "Deep" if n >= 100 else "Moderate" if n >= 25 else "Thin" if n >= 5 else "Filing-based"


def conf(a):
    return NAR.CONFIDENCE[a][0]


def ids_in(obj):
    return sorted(set(CA.IDRE.findall(json.dumps(obj))))


CITED = sorted({i for a in ORDER for i in ids_in(PROF[a])} | set(CA.IDRE.findall(json.dumps(NAR.FINDINGS))))


def eids(ids):
    ids = [i for i in ids or [] if i]
    if not ids:
        return ""
    return '<span class="eids">' + " ".join(f'<span class="eid" tabindex="0" data-e="{esc(i)}">{esc(i)}</span>' for i in ids) + "</span>"


IDS = r"(?:BX|AX|CX|PX|RX|B|A|C|P|R)-\d{4}"
GROUP = re.compile(r"\s*[\[(]((?:%s)(?:\s*[,;]\s*(?:%s))*)[\])]" % (IDS, IDS))
BARE = re.compile(r"(?<![\w>-])(%s)(?![\w-])" % IDS)
FILES = (r"(?:teams|profile|dashboard_game|objectives|operations|ortberg|malave|pope|faury|toepfer|wagner|culp|ghai|ali|calio|"
         r"mitchill|eddy|erginbilgic|mccabe)\.md")
FILE_NAME = {"teams": "the team rules", "profile": "the company profile", "dashboard_game": "the board notes", "objectives": "the objectives"}
# Plain words for display only: order-field names, file references and rule shorthand. Quotes are never touched.
PLAIN = [
    (r"`", ""),
    (r"\b(%s)(?:\s*§\s?[\d.]+(?:\s*(?:and|,)\s*§?\s?[\d.]+)*)?" % FILES, lambda m: FILE_NAME.get(m.group(1)[:-3], "the personal profile")),
    (r"\s*§\s?\d+(?:\.\d+)?", ""),
    (r"\bstep-4 veto\b", "veto at the veto check"), (r"\bstep-4\b", "veto-check"), (r"\bveto_check\b", "veto check"),
    (r"\blaunch_if_selected\b", "launch if selected"), (r"\bjv_with_pw\b", "Joint Venture with P&W"),
    (r"\bjv_with_rr\b", "Joint Venture with Rolls-Royce"), (r"\bcfm_jv\b", "CFM Joint Venture"),
    (r"\bpremium_b\b", "declared premium"), (r"\bexpected_pv_b\b", "expected value"),
    (r"\bpratt_whitney\b", "Pratt & Whitney"), (r"\brolls_royce\b", "Rolls-Royce"),
    (r"within ε", "within the tie margin"), (r"ε", "the tie margin"),
    (r"\b([a-z0-9]+(?:_[a-z0-9]+)+)\b", lambda m: m.group(1).replace("_", " ")),
]
PLAIN = [(re.compile(p), r) for p, r in PLAIN]


def plain(text):
    t = text or ""
    for p, r in PLAIN:
        t = p.sub(r, t)
    return t


def rich(text):
    """Plain words, escape, then evidence ids as hoverable chips and '(inference)' as the inference tag."""
    t = esc(plain(text))
    t = GROUP.sub(lambda m: " " + eids(re.findall(IDS, m.group(1))), t)
    parts = re.split(r"(<span class=\"eids\">.*?</span></span>)", t)
    t = "".join(x if x.startswith('<span class="eids">') else BARE.sub(lambda m: eids([m.group(1)]), x) for x in parts)
    t = re.sub(r"\s*\*{0,2}\((inference(?:[^()]|\([^()]*\))*?)\)\*{0,2}", lambda m: ' <span class="inf">' + m.group(1) + "</span>", t)
    return t.replace("**", "")


def ids_html(h):
    """Narrative HTML with its [ID] groups rendered as id chips (the text is already HTML)."""
    return GROUP.sub(lambda m: " " + eids(re.findall(IDS, m.group(1))), h)


def infer(flag):
    return ' <span class="inf">inference</span>' if flag else ""


def year(d):
    return int(d[:4]) + (int(d[5:7]) - 1) / 12 + (int(d[8:10]) - 1) / 365 if d else None


def short_doc(d, n=70):
    d = re.sub(r"Airbus SE Report of the Board of Directors 2025 \(issued 18 February 2026\)", "Airbus Board Report 2025", d or "")
    return d if len(d) <= n else d[:n].rsplit(" ", 1)[0] + "…"


def span(first, last):
    if not first:
        return "—"
    return f"all on {first}" if first == last else f"{first} to {last}"


# ── vetoes: what a member can block, red lines it flags, rules on a CEO's own decision ──
RED = re.compile(r"^(A company red line|Company red line|Five pillars|Hard-rule flags|Red line)", re.I)


def veto_kind(a, v):
    if not PROF[a]["veto_holder"]:
        return "own"
    return "red" if RED.match(v["ground"]) else "veto"


def veto_label(v):
    b = v["binding"]
    if b == "formal":
        return "binding (right inferred)" if re.search(r"itself inferred|an inference|team rule[^.;]*inferred", v["ground"]) else "binding"
    return {"soft": "soft", "inference": "by inference", "none": "advice only"}.get(b, b)


def veto_class(lab):
    return {"binding": "b-binding", "soft": "b-soft", "by": "b-inference", "advice": "b-none"}.get(lab.split()[0], "b-none")


def veto_summary(a):
    """Roster/header label: how hard this member can block."""
    pr = PROF[a]
    if not pr["veto_holder"]:
        return "decides; holds no veto"
    labs = [veto_label(v) for v in pr["vetoes"] if veto_kind(a, v) == "veto"]
    for key, out in (("binding", "binding veto"), ("soft", "soft veto"), ("by inference", "veto by inference")):
        if any(lab.startswith(key) for lab in labs):
            return out
    return "advice only"


def first_clause(t, n=150):
    t = plain(t)
    t = re.split(r"(?<=[a-z\)])[;.] ", t)[0]
    t = re.sub(r"\s*\[[^\]]*\]", "", t)
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + "…"


# ── charts ──
def evidence_bars(w, label_w, narrow=False):
    rh, gh, top, bot = 24, 22, 8, 34
    x0, x1 = label_w, w - (44 if narrow else 64)
    hi = 450
    sx = lambda v: x0 + v / hi * (x1 - x0)
    h = top + len(SIDES) * gh + len(ORDER) * rh + bot
    out = [K.svg_open(w, h, "Items behind each agent, split by whose words they are", "chart narrow" if narrow else "chart")]
    for t in range(0, hi + 1, 100 if not narrow else 200):
        out.append(f'<line x1="{sx(t):.1f}" x2="{sx(t):.1f}" y1="{top}" y2="{h - bot}" class="grid"/>'
                   f'<text x="{sx(t):.1f}" y="{h - bot + 16}" text-anchor="middle" class="tick">{t}</text>')
    y = top
    for s in SIDES:
        out.append(f'<text x="0" y="{y + 15}" class="grp">{esc(COMPANY[s].upper())}</text>')
        y += gh
        for a in ROSTER[s]:
            c = collections.Counter(e.get("perspective") for e in ITEMS[a])
            own = c.get("own_words", 0)
            tot = len(ITEMS[a])
            lab = SHORT[a] if narrow else f"{SHORT[a]} · {BY[a]['seat'] if BY[a]['seat'] != 'Operating head' else 'Op. head'}"
            out.append(f'<text x="{x0 - 8}" y="{y + 16}" text-anchor="end" class="rowlab sm">{esc(lab)}</text>')
            segs = [(own, "s1")] + [(c.get(k, 0), PERSP[k][1]) for k in PERSP if k != "own_words"]
            segs = [(n, v) for n, v in segs if n]
            start = 0
            for j, (n, var) in enumerate(segs):
                out.append(f'<path d="{K.hbar_path(sx(start), sx(start + n), y + 5, 14, r=3 if j == len(segs) - 1 else 0)}" fill="var(--{var})"/>')
                start += n
            out.append(f'<text x="{sx(tot) + 6:.1f}" y="{y + 16}" class="val sm">{tot}</text>')
            rows = [(str(tot), "items in own file", None)] + [(str(c[k]), PERSP[k][0], f"var(--{PERSP[k][1]})") for k in PERSP if c.get(k)]
            if COMP[a]:
                rows.append((str(COMP[a]), "more as speaker in the company file (not in the bar)", None))
            out.append(f'<rect x="0" y="{y}" width="{w}" height="{rh}" class="hit" {K.mark_attrs((BY[a]["name"], "", None), *rows)}/>')
            y += rh
    out.append(f'<text x="{x0}" y="{h - 4}" class="tick">Items in the person\'s evidence file</text></svg>')
    return "".join(out)


def evidence_rug(narrow=False):
    """One tick per evidence item by date. Wide: names on the left. Narrow (phones): each name above its row."""
    if narrow:
        w, left, right, top, bot, rh, gh = 360, 6, 10, 8, 34, 36, 22
    else:
        w, left, right, top, bot, rh, gh = 760, 150, 16, 8, 34, 24, 22
    lo, hi = 2012, 2026.5
    sx = lambda v: left + (v - lo) / (hi - lo) * (w - left - right)
    h = top + len(SIDES) * gh + len(ORDER) * rh + bot
    out = [K.svg_open(w, h, "When each agent's evidence was said or written: one tick per item", "chart narrow" if narrow else "chart")]
    for yr in range(2012, 2027, 2):
        out.append(f'<line x1="{sx(yr):.1f}" x2="{sx(yr):.1f}" y1="{top}" y2="{h - bot}" class="grid"/>')
        if not narrow or yr % 4 == 0 or yr == 2026:
            anchor = "start" if narrow and yr == lo else "end" if narrow and yr == 2026 else "middle"
            out.append(f'<text x="{sx(yr):.1f}" y="{h - bot + 16}" text-anchor="{anchor}" class="tick">{yr}</text>')
    y = top
    for s in SIDES:
        out.append(f'<text x="0" y="{y + 15}" class="grp">{esc(COMPANY[s].upper())}</text>')
        y += gh
        for a in ROSTER[s]:
            if narrow:
                out.append(f'<text x="{left}" y="{y + 11}" class="rowlab sm">{esc(SHORT[a])}</text>')
                t0, t1 = y + 15, y + 31
            else:
                out.append(f'<text x="{left - 8}" y="{y + 16}" text-anchor="end" class="rowlab sm">{esc(SHORT[a])}</text>')
                t0, t1 = y + 4, y + 20
            dates = sorted(e["date"] for e in ITEMS[a] if e.get("date"))
            for e in sorted(ITEMS[a], key=lambda e: e.get("perspective") == "own_words"):
                if e.get("date"):
                    x = sx(year(e["date"]))
                    out.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{t0}" y2="{t1}" stroke="var(--{PERSP.get(e.get("perspective"), ("", "s3"))[1]})" stroke-width="1.4" opacity=".75"/>')
            by_year = collections.Counter(d[:4] for d in dates)
            rows = [(span(dates[0], dates[-1]) if dates else "no dated items", "", None)] + \
                   [(str(n), yy, None) for yy, n in sorted(by_year.items())]
            out.append(f'<rect x="0" y="{y}" width="{w}" height="{rh}" class="hit" {K.mark_attrs((BY[a]["name"], "", None), *rows)}/>')
            y += rh
    out.append(f'<text x="{left}" y="{h - 4}" class="tick">{"Date of the item" if narrow else "Date of the call, conference or filing"}</text></svg>')
    return "".join(out)


def legend_persp():
    return ('<div class="legend">' + "".join(f'<span><i class="sq" style="background:var(--{v})"></i>{esc(t)}</span>'
                                             for t, v in [("Own words (transcripts)", "s1"), ("Airbus Board Report text", "s2"),
                                                          ("Remarks by others about them, analysts' questions", "s3")]) + "</div>")


def stack_table(head, rows, num_cols=(), cls=""):
    """A table that becomes stacked label/value rows on phones."""
    th = "".join(f'<th scope="col"{" class=n" if i in num_cols else ""}>{h}</th>' for i, h in enumerate(head))
    body = "".join("<tr>" + "".join((f'<th scope="row">{c}</th>' if j == 0 else
                                     f'<td data-label="{esc(re.sub("<[^>]+>", "", head[j]), quote=True)}"{" class=n" if j in num_cols else ""}>{c}</td>')
                                    for j, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="scroll"><table class="stk {cls}"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'


def evidence_table():
    rows = []
    for a in ORDER:
        c = collections.Counter(e.get("perspective") for e in ITEMS[a])
        dates = sorted(e["date"] for e in ITEMS[a] if e.get("date"))
        rows.append([f"{esc(BY[a]['name'])}<br><span class='muted small'>{esc(COMPANY[BY[a]['side']])}, {esc(BY[a]['seat'])}</span>",
                     str(len(ITEMS[a])), str(c.get("own_words", 0)), str(len(ITEMS[a]) - c.get("own_words", 0)), str(COMP[a]),
                     dates[0] if dates else "—", dates[-1] if dates else "—", esc(volume(a)), esc(conf(a))])
    return ('<details class="tv"><summary>Table view: evidence by person</summary>'
            + stack_table(["Person", "Items", "Own words", "Other", "As speaker in company file", "First", "Last", "Volume", "Confidence"],
                          rows, num_cols=(1, 2, 3, 4, 5, 6)) + "</details>")


# ── roster, protocol, glossary ──
def roster():
    head = '<div class="rh"></div>' + "".join(f'<div class="rh">{s}</div>' for s in SEATS)
    cells = []
    for s in SIDES:
        cells.append(f'<div class="rc">{esc(COMPANY[s])}</div>')
        for a in ROSTER[s]:
            p, pr = BY[a], PROF[a]
            lv, cf = volume(a), conf(a)
            steps = ", ".join(pr.get("protocol_steps") or []).replace("_", " ")
            cells.append(f'<a class="rcell" href="#{a}"><span class="seat">{esc(p["seat"])}</span><b>{esc(p["name"])}</b>'
                         f'<span class="small muted">{esc(p["title"].replace(" (COO seat)", ""))}</span>'
                         f'<span class="chips"><span class="chip">{p["n_own_words"]} own-words items</span>'
                         f'<span class="chip lv-{lv.lower()}">Volume: {esc(lv.lower())}</span>'
                         f'<span class="chip{" warn" if cf in NAR.LOW_CONFIDENCE else ""}">Confidence: {esc(cf)}</span>'
                         f'<span class="chip veto">{esc(veto_summary(a))}</span></span>'
                         f'<span class="small muted">Steps: {esc(steps)}</span></a>')
    return f'<div class="roster">{head}{"".join(cells)}</div>'


def protocol():
    steps = "".join(f"<li><b>{esc(t)}</b><br>{esc(d)}</li>" for t, d in NAR.STEPS)
    rows = [[esc(COMPANY[s])] + [esc(x) for x in NAR.TEAM_RULES[s]] for s in SIDES]
    return f'<ol class="loop">{steps}</ol>' + stack_table(["Company", "Frames and decides", "Tests", "Vetoes and how binding"], rows, cls="rules")


def glossary():
    return ('<details class="gloss-box panel"><summary>Board terms used on the cards</summary><dl class="gl">'
            + "".join(f"<dt>{esc(t)}</dt><dd>{esc(d)}</dd>" for t, d in NAR.GLOSSARY) + "</dl></details>")


# ── cards ──
def lst(items, ordered=False, key="text"):
    tag = "ol" if ordered else "ul"
    return f"<{tag} class=\"facts\">" + "".join(f"<li>{rich(it[key])}{infer(it.get('inference'))} {eids(it.get('ids'))}</li>" for it in items) + f"</{tag}>"


def quote_html(q):
    e = EV.get(q["id"], {})
    persp = q.get("perspective") or e.get("perspective")
    note = CITE.get(persp, persp or "")
    if persp == "own_words" and (e.get("speaker") or "").startswith("Unknown"):
        note = "attributed: an unnamed speaker in the transcript"
    ocr = (' <span class="inf">PDF spacing as extracted</span>'
           if persp == "filing" or re.search(r"[a-z][A-Z]|[a-z],[A-Za-z]|[A-Za-z]{18,}", q["quote"]) else "")
    return (f'<blockquote class="q{"" if persp == "own_words" else " q-other"}"><p>“{esc(q["quote"])}”</p>'
            f'<footer>{eids([q["id"]])} · {esc(q.get("date") or "")} · {esc(short_doc(q.get("doc")))} · <b>{esc(note)}</b>{ocr}</footer></blockquote>')


def vetoes_html(a):
    pr = PROF[a]
    vs = pr["vetoes"]
    if not pr["veto_holder"]:
        items = "".join(f"<li>{rich(v['ground'])} {eids(v.get('ids'))}</li>" for v in vs)
        return (f'<p class="label">Red lines and rules on {PRON[a]} own decisions ({PRON[a]} seat decides and holds no veto)</p>'
                f'<ul class="facts">{items}</ul>')
    can = [v for v in vs if veto_kind(a, v) == "veto"]
    red = [v for v in vs if veto_kind(a, v) == "red"]
    out = f'<p class="label">What {esc(SHORT[a])} can block at the veto check</p><ul class="facts">'
    out += "".join(f'<li><span class="chip {veto_class(veto_label(v))}">{esc(veto_label(v))}</span> {rich(v["ground"])} {eids(v.get("ids"))}</li>'
                   for v in can) or "<li>Nothing.</li>"
    out += "</ul>"
    if red:
        out += (f'<p class="label">Red lines {esc(SHORT[a])} flags to the CEO</p><ul class="facts">'
                + "".join(f'<li><span class="chip b-red">red line</span> {rich(v["ground"])} {eids(v.get("ids"))}</li>' for v in red) + "</ul>")
    return out


def card(a):
    p, pr = BY[a], PROF[a]
    ev = pr["evidence"]
    lv, cf = volume(a), conf(a)
    thin_flag = lv in ("Thin", "Filing-based") or cf in NAR.LOW_CONFIDENCE
    conf_items = "".join(f'<li><b>{esc(c["area"])}:</b> {rich(c["level"])}</li>' for c in ev.get("confidence_by_area") or [])
    tests = stack_table(["Test", "Threshold or rule", "Evidence"],
                        [[rich(t["test"]) + infer(t.get("inference")), rich(t["threshold"]), eids(t.get("ids"))] for t in pr["tests"]])
    levers = stack_table(["Lever", "Position", "Evidence"],
                         [[rich(l["lever"]) + infer(l.get("inference")), rich(l["position"]), eids(l.get("ids"))] for l in pr["lever_positions"]])
    coll = "".join(f'<li><b>{esc(c["name"])}.</b> {rich(c["relation"])}</li>' for c in pr["colleagues"])
    voiced = pr.get("dash2050_voiced") or {}
    vrows = "".join(f'<li><b>Round {r["round"]}.</b> {rich(r["line"])}</li>' for r in voiced.get("by_round") or [])
    gaps = "".join(f"<li>{rich(g)}</li>" for g in pr["thin"]["gaps"])
    extra = p.get("extra_items_same_person_other_tag") or 0
    extra_txt = f" Plus {extra} items tagged to the CFM Joint Venture in {PRON[a]} own words." if extra else ""
    quotes = pr["voice"]["quotes"]
    q_main, q_more = quotes[:4], quotes[4:]
    more_q = (f'<details class="moreq"><summary>More quotes ({len(q_more)})</summary><div class="quotes">'
              + "".join(quote_html(q) for q in q_more) + "</div></details>") if q_more else ""
    if pr["veto_holder"]:
        block = "; ".join(f"{veto_label(v)}: {first_clause(v['ground'], 110)}" for v in pr["vetoes"]
                          if veto_kind(a, v) == "veto" and veto_label(v) != "advice only") or "nothing; advice only"
    else:
        block = "nothing: " + ("he" if PRON[a] == "his" else "she") + " frames and decides, within the colleagues' vetoes"
    comp = f'<span class="chip">+{COMP[a]} as speaker in the company file</span>' if COMP[a] else ""
    return f'''<article class="pcard panel" id="{a}">
<header class="ph"><p class="label"><span>{esc(COMPANY[p["side"]])} · {esc(p["seat"])}</span><a class="back" href="#roster">Back to the roster</a></p>
<h4>{esc(p["name"])}</h4><p class="muted small">{esc(p["title"].replace(" (COO seat)", ""))}. {rich(pr["role_dates"])}</p>
<p class="chips"><span class="chip">{len(ITEMS[a])} items in {PRON[a]} file</span><span class="chip">{p["n_own_words"]} in own words</span>{comp}
<span class="chip">{esc(span(ev.get("first"), ev.get("last")))}</span><span class="chip lv-{lv.lower()}">Volume: {esc(lv.lower())}</span>
<span class="chip{" warn" if cf in NAR.LOW_CONFIDENCE else ""}">Confidence: {esc(cf)}</span><span class="chip veto">{esc(veto_summary(a))}</span>
<span class="chip">Steps: {esc(", ".join(pr.get("protocol_steps") or []).replace("_", " "))}</span></p>
<p class="mandate">{rich(pr["mandate"])}</p>
<dl class="glance"><dt>Protects first</dt><dd>{rich(pr["objective_ranked"][0]["text"])}</dd>
<dt>Can block</dt><dd>{esc(block)}</dd>
<dt>When the record is silent</dt><dd>{esc(first_clause(pr["thin"]["fallback"], 220))}</dd></dl></header>
<div class="grid2"><div><p class="label">What {esc(SHORT[a])} is paid to protect</p>{lst(pr["objective_ranked"], ordered=True)}</div>
<div><p class="label">How {esc(SHORT[a])} decides</p>{lst(pr["decision_style"])}</div></div>
<p class="label">Tests (applied whenever the brief has the data)</p>{tests}
{vetoes_html(a)}
<p class="label">Voice</p><p class="small">{rich(pr["voice"]["style"])}</p><div class="quotes">{"".join(quote_html(q) for q in q_main)}</div>{more_q}
<div class="thin{" warn" if thin_flag else ""}"><p class="label">Where the record is thin</p><ul class="facts">{gaps}</ul>
<p class="small"><b>When the record is silent:</b> {rich(pr["thin"]["fallback"])}</p></div>
<details class="more"><summary>Lever positions, rivals, colleagues, biases, evidence base, dash-2050 role-play</summary>
<p class="label">Positions on the game's levers</p>{levers}
<div class="grid2"><div><p class="label">How {esc(SHORT[a])} reads the rivals</p>{lst(pr["rivals"])}</div>
<div><p class="label">Colleagues</p><ul class="facts">{coll}</ul></div></div>
<div class="grid2"><div><p class="label">Biases the agent displays</p>{lst(pr["biases"])}</div>
<div><p class="label">Evidence base</p><p class="small">{rich(ev["sources_note"])}{esc(extra_txt)}</p><p class="small"><b>Confidence, in the profile's words:</b> {rich(ev["confidence_overall"])}</p><ul class="facts small">{conf_items}</ul></div></div>
<p class="label">As voiced in dash-2050 (the single company agent's role-play, not evidence)</p><p class="small">{rich(voiced.get("summary", ""))}</p><ul class="facts small">{vrows}</ul>
</details><p class="small muted agentfile">Agent file: <code>.claude/agents/{esc(a)}.md</code></p></article>'''


def cards():
    out = []
    for s in SIDES:
        names = ", ".join(SHORT[a] for a in ROSTER[s])
        out.append(f'<h3 class="co" id="co-{s}">{esc(COMPANY[s])} <span class="muted small">2026 ExCo: {esc(names)}</span></h3>')
        out.append('<div class="stack">' + "".join(card(a) for a in ROSTER[s]) + "</div>")
    return "".join(out)


def tiles():
    n_items = sum(len(ITEMS[a]) for a in ORDER)
    n_own = sum(1 for a in ORDER for e in ITEMS[a] if e.get("perspective") == "own_words")
    thin = [SHORT[a] for a in ORDER if volume(a) in ("Thin", "Filing-based")]
    quotes = sum(len(PROF[a]["voice"]["quotes"]) for a in ORDER)
    t = [("Agents", "15", "Three per company: the CEO, the CFO and the operating head of each default 2026 ExCo"),
         ("Items in the executives' files", f"{n_items:,}", f"{n_own:,} in the person's own words; Airbus mostly Board Report text"),
         ("Cited in the profiles", f"{len(CITED):,} ids", f"every id resolves to an evidence item; {quotes} signature quotes checked word for word"),
         ("Thin or filing-based", f"{len(thin)} of 15", ", ".join(thin) + ": each falls back on the company profile or a named colleague"),
         ("Game", "Not run", "The agents are set up and kept apart from each other's files; the round procedure has been tried only with "
                             "placeholder agents")]
    return '<div class="tiles">' + "".join(f'<div class="panel tile"><div class="k">{esc(k)}</div><div class="v">{esc(v)}</div><div class="d">{esc(d)}</div></div>'
                                           for k, v, d in t) + "</div>"


EXTRA_CSS = """
:root { --tip-bg: var(--surface); --tip-line: var(--line); }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --tip-bg: #253041; --tip-line: #56637a; } }
:root[data-theme="dark"] { --tip-bg: #253041; --tip-line: #56637a; }
.tip { background: var(--tip-bg); border-color: var(--tip-line); }
.roster { display: grid; grid-template-columns: 150px repeat(3, minmax(0, 1fr)); gap: 8px; }
.roster .rh { font: 500 .72rem/1.3 var(--font-mono); letter-spacing: .1em; text-transform: uppercase; color: var(--muted); padding: 0 4px; }
.roster .rc { font: 700 1.25rem/1.1 var(--font-display); display: flex; flex-direction: column; gap: 4px; padding: 10px 4px; }
.rcell { display: flex; flex-direction: column; gap: 3px; background: var(--surface); border: 1px solid var(--line); border-radius: var(--r);
  padding: 10px 12px; text-decoration: none; min-width: 0; }
.rcell:hover, .rcell:focus-visible { border-color: var(--fg); }
.rcell b { font-weight: 600; font-size: 1rem; }
.rcell .seat { display: none; font: 500 .7rem/1.3 var(--font-mono); letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }
.chips { display: flex; flex-wrap: wrap; gap: 4px 6px; margin: 4px 0; }
.chip { font: 500 .74rem/1.2 var(--font-mono); padding: 2px 7px; border-radius: 999px; background: var(--sunk); color: var(--muted); border: 1px solid var(--line); }
.chip.lv-deep, .chip.lv-moderate { color: var(--fg); }
.chip.lv-thin, .chip.lv-filing-based, .chip.warn { color: var(--fg); border-color: var(--s2); }
.chip.veto { color: var(--fg); border-color: var(--fg); }
.chip.b-binding { color: var(--fg); border-color: var(--fg); } .chip.b-soft { border-style: dashed; color: var(--fg); }
.chip.b-inference { border-style: dotted; color: var(--fg); } .chip.b-none { opacity: .85; }
.chip.b-red { color: var(--fg); border-color: var(--s2); }
.pcard { scroll-margin-top: 12px; }
.pcard h4 { font: 700 1.7rem/1.1 var(--font-display); margin: 2px 0 4px; letter-spacing: .01em; }
.pcard .label { margin-top: 16px; }
.pcard header .label { margin-top: 0; display: flex; justify-content: space-between; gap: 10px; flex-wrap: wrap; }
.pcard header .label .back { font: 500 .8rem var(--font-body); letter-spacing: 0; text-transform: none; color: var(--muted); }
.mandate { font-size: 1.02rem; margin-top: 6px; max-width: 90ch; }
dl.glance { display: grid; grid-template-columns: 11rem 1fr; gap: 4px 14px; margin: 10px 0 0; padding: 10px 12px; background: var(--sunk);
  border-radius: 6px; font-size: .92rem; }
dl.glance dt { font: 500 .72rem/1.6 var(--font-mono); letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }
dl.glance dd { margin: 0; }
.inf { font: italic 500 .72rem/1.5 var(--font-mono); color: var(--muted); border: 1px dotted var(--faint); border-radius: 4px; padding: 0 4px; }
.eids { white-space: normal; }
.eid { font: 500 .72rem/1.2 var(--font-mono); color: var(--muted); border-bottom: 1px dotted var(--faint); cursor: help; white-space: nowrap; }
.eid:focus-visible { outline: 2px solid var(--fg); outline-offset: 1px; border-radius: 2px; }
td .eids { display: inline-block; max-width: 13rem; }
.quotes { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 10px; }
details.moreq { margin-top: 8px; } details.moreq summary { cursor: pointer; color: var(--muted); font-size: .9rem; margin-bottom: 8px; }
blockquote.q { margin: 0; padding: 10px 12px; border-left: 3px solid var(--s1); background: var(--sunk); border-radius: 0 6px 6px 0; }
blockquote.q.q-other { border-left-color: var(--s2); }
blockquote.q p { margin: 0 0 6px; font-size: .93rem; overflow-wrap: anywhere; }
blockquote.q footer { font-size: .76rem; color: var(--muted); margin: 0; border: 0; padding: 0; }
blockquote.q footer b { color: var(--fg); font-weight: 500; }
.thin { margin-top: 14px; padding: 10px 12px; border: 1px solid var(--line); border-radius: 6px; }
.thin.warn { border-color: var(--s2); }
.thin .label { margin-top: 0; }
details.more { margin-top: 14px; border-top: 1px solid var(--line); padding-top: 10px; }
details.more summary { cursor: pointer; font-weight: 600; }
.agentfile { margin: 12px 0 0; }
h3.co { font-size: 1.6rem; margin: 30px 0 10px; scroll-margin-top: 12px; }
.gloss-box { margin-bottom: 8px; } .gloss-box summary { cursor: pointer; font-weight: 600; }
dl.gl { display: grid; grid-template-columns: 13rem 1fr; gap: 6px 14px; margin: 10px 0 0; font-size: .92rem; }
dl.gl dt { font-weight: 600; } dl.gl dd { margin: 0; }
.loop li b { font-weight: 600; }
code { font: .86em var(--font-mono); }
table.rules th[scope=row] { white-space: nowrap; }
@media (max-width: 760px) {
  .roster { grid-template-columns: 1fr; }
  .roster .rh { display: none; }
  .roster .rc { padding: 14px 0 2px; }
  .rcell .seat { display: block; }
  .quotes { grid-template-columns: 1fr; }
  .chip, .eid, .inf { font-size: .8rem; } .label { font-size: .76rem; }
  dl.glance, dl.gl { grid-template-columns: 1fr; gap: 2px; } dl.glance dd, dl.gl dd { margin-bottom: 8px; }
  table.stk thead { display: none; }
  table.stk, table.stk tbody, table.stk tr, table.stk th, table.stk td { display: block; width: auto; }
  table.stk tr { border-bottom: 1px solid var(--line); padding: 6px 0; }
  table.stk tbody tr:last-child { border-bottom: 0; }
  table.stk th[scope=row] { font-weight: 600; border: 0; padding: 4px 10px 2px; white-space: normal; }
  table.stk td { border: 0; padding: 2px 10px; text-align: left; white-space: normal; }
  table.stk td::before { content: attr(data-label); display: block; font: 500 .7rem/1.4 var(--font-mono); letter-spacing: .06em;
    text-transform: uppercase; color: var(--muted); }
  table.stk td.n { font-family: var(--font-body); }
  td .eids { max-width: none; }
}
"""

EV_JS = r"""
(() => {
  const EV = JSON.parse(document.getElementById('evdata').textContent);
  document.querySelectorAll('.eid').forEach(el => {
    const e = EV[el.dataset.e]; if (!e) return;
    const rows = [{v: el.dataset.e, l: [e.date, e.doc, e.p].filter(Boolean).join(' · ')}, {v: '', l: e.s}, {v: '', l: '“' + e.q + '”'}];
    el.dataset.tip = JSON.stringify(rows);
    el.setAttribute('aria-label', el.dataset.e + ': ' + e.q);
  });
})();
"""


def checks():
    """Facts the narrative states, checked against the data; also the hook tests and the agent checker. Stops on failure."""
    n = {a: len(ITEMS[a]) for a in ORDER}
    dates = {a: sorted({e["date"] for e in ITEMS[a]}) for a in ORDER}
    yrs = collections.Counter(e["date"][:4] for a in ORDER for e in ITEMS[a])
    ortberg_collins = [e["date"] for e in ITEMS["boeing-ortberg"] if e.get("source") == "rtx_transcripts"]
    airbus_feb = [e for a in ("airbus-toepfer", "airbus-wagner") for e in ITEMS[a]]
    faury_br = [e for e in ITEMS["airbus-faury"] if e.get("source") == "airbus_fy2025"]
    watson = ITEMS["rolls-royce-watson"]
    C = [("min is Wagner 2", min(n, key=n.get) == "airbus-wagner" and n["airbus-wagner"] == 2),
         ("max is Culp 425", max(n, key=n.get) == "cfm-culp" and n["cfm-culp"] == 425),
         ("JV extras 51/7/7", [BY[a].get("extra_items_same_person_other_tag") for a in ("cfm-culp", "cfm-ghai", "cfm-ali")] == [51, 7, 7]),
         ("Airbus one own-words line, Faury", [a for a in ROSTER["airbus"] for e in ITEMS[a] if e.get("perspective") == "own_words"] == ["airbus-faury"]),
         ("six in ten 2023-2025", 0.55 <= sum(yrs[y] for y in ("2023", "2024", "2025")) / sum(yrs.values()) < 0.65),
         ("Malave one call 2025-10-29", dates["boeing-malave"] == ["2025-10-29"] and n["boeing-malave"] == 11),
         ("Eddy one day 2023-06-19", dates["pratt-whitney-eddy"] == ["2023-06-19"] and n["pratt-whitney-eddy"] == 21),
         ("Pope eight, 2012-2022", n["boeing-pope"] == 8 and dates["boeing-pope"][0][:4] == "2012" and dates["boeing-pope"][-1][:4] == "2022"),
         ("Ali 13 from four events 2022-2024", n["cfm-ali"] == 13 and len(dates["cfm-ali"]) == 4 and dates["cfm-ali"][0][:4] == "2022"
          and dates["cfm-ali"][-1][:4] == "2024"),
         ("Watson 26 of 27 on 2023-11-28, 4 unnamed", len(watson) == 27 and sum(e["date"] == "2023-11-28" for e in watson) == 26
          and sum((e.get("speaker") or "").startswith("Unknown") for e in watson) == 4),
         ("McCabe 61, Watson 27", BY["rolls-royce-mccabe"]["n_own_words"] == 61 and BY["rolls-royce-watson"]["n_own_words"] == 27),
         ("Ortberg 14 Collins items 2017/2019", len(ortberg_collins) == 14 and {d[:4] for d in ortberg_collins} == {"2017", "2019"}),
         ("Toepfer/Wagner all 2026-02-18", {e["date"] for e in airbus_feb} == {"2026-02-18"}),
         ("Faury 47 Board Report lines 2026-02-18", len(faury_br) == 47 and {e["date"] for e in faury_br} == {"2026-02-18"}),
         ("volume counts 6/2/4/3", collections.Counter(volume(a) for a in ORDER) == {"Deep": 6, "Moderate": 2, "Thin": 4, "Filing-based": 3}),
         ("Airbus all filing-based", [volume(a) for a in ROSTER["airbus"]] == ["Filing-based"] * 3),
         ("narrative ids exist", set(CA.IDRE.findall(json.dumps(NAR.FINDINGS))) <= set(EV)),
         ("deep six named", [SHORT[a] for a in sorted((a for a in ORDER if volume(a) == "Deep"), key=lambda a: -BY[a]["n_own_words"])]
          == ["Culp", "Mitchill", "Calio", "Erginbilgic", "Ghai", "Ortberg"]),
         ("confidence labels match the profiles", all(NAR.CONFIDENCE[a][1] in PROF[a]["evidence"]["confidence_overall"].lower() for a in ORDER)),
         ("Airbus once per game in Faury's file", "at most one override per game" in open(os.path.join(REPO, ".claude/agents/airbus-faury.md")).read())]
    for t, x in NAR.FINDINGS:
        for q, i in re.findall(r'"([^"]+)" \[([A-Z]+-\d{4})\]', x):
            C.append((f"finding quote {i} verbatim", CA.verbatim(q, EV[i].get("quote", ""))))
    hook = subprocess.run([sys.executable, os.path.join(REPO, "wargame", "dashgame", "test_hook.py")], capture_output=True, text=True)
    C.append(("hook tests pass", hook.returncode == 0))
    agents = subprocess.run([sys.executable, os.path.join(HERE, "check_agents.py")], capture_output=True, text=True)
    C.append(("agent checker passes", agents.returncode == 0))
    bad = [c for c, ok in C if not ok]
    if bad:
        sys.exit("NARRATIVE CHECKS FAILED: %s" % bad)
    print("checks passed:", len(C))


def build(out_path):
    checks()
    css = K.CSS + EXTRA_CSS
    ev = {}
    for i in CITED:
        e = EV[i]
        q = e.get("quote") or e.get("finding") or ""
        src = (e.get("speaker") or "")[:80] if e.get("quote") else "Finding from an analyst model (not a quote)"
        ev[i] = {"date": e.get("date"), "doc": short_doc(e.get("doc"), 60), "s": src, "q": q if len(q) <= 420 else q[:417] + "…",
                 "p": CITE.get(e.get("perspective"), (e.get("perspective") or "").replace("_", " "))}
    evjson = json.dumps(ev, ensure_ascii=False).replace("</", "<\\/")
    comp = ", ".join(f"{SHORT[a]} {COMP[a]}" for a in sorted(ORDER, key=lambda a: -COMP[a]) if COMP[a])
    iso = NAR.ISOLATION.format(cases=len(TH.CASES), new=TH.N_EXEC, paths=TH.N_PATHS)
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ExCo Agent Profiles</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{css}</style></head><body><div class="wrap">
<header class="top"><p class="eyebrow">Boeing Product Development · war game agents · BOEING PROPRIETARY</p>
<h1>{esc(NAR.TITLE)}</h1><p class="lede">{NAR.LEDE}</p>
<nav class="toc"><a href="#summary">Summary</a><a href="#roster">Roster</a><a href="#protocol">How a round runs</a><a href="#evidence">Evidence</a>
{"".join(f'<a href="#co-{s}">{esc(COMPANY[s])}</a>' for s in SIDES)}<a href="#isolation">Isolation</a><a href="#method">Method</a></nav></header>

<section id="summary"><h2>Summary</h2>{tiles()}
<div class="bl">{"".join(f'<div class="panel"><div><b>{esc(t)}</b>{ids_html(x)}</div></div>' for t, x in NAR.FINDINGS)}</div></section>

<section id="roster"><h2>The fifteen agents</h2><p class="lede">{NAR.ROSTER_LEDE}</p>{roster()}</section>

<section id="protocol"><h2>How a round will run</h2><p class="lede">{NAR.PROTOCOL_LEDE}</p><div class="panel">{protocol()}<p class="cap">{NAR.PROTOCOL_CAP}</p></div></section>

<section id="evidence"><h2>What each agent is built on</h2><p class="lede">{NAR.EVIDENCE_LEDE}</p><div class="stack">
<div class="panel"><p class="ctitle">{esc(NAR.BARS_TITLE)}</p>{legend_persp()}<div class="only-wide">{evidence_bars(760, 170)}</div><div class="only-narrow">{evidence_bars(360, 84, narrow=True)}</div>
<p class="cap">{NAR.BARS_CAP.format(comp=comp)}</p></div>
<div class="panel"><p class="ctitle">{esc(NAR.RUG_TITLE)}</p>{legend_persp()}<div class="only-wide">{evidence_rug()}</div><div class="only-narrow">{evidence_rug(narrow=True)}</div>
<p class="cap">{NAR.RUG_CAP}</p>{evidence_table()}</div></div></section>

<section id="agents"><h2>The agents</h2><p class="lede">{NAR.CARDS_LEDE}</p>{glossary()}{cards()}</section>

<section id="isolation"><h2>Isolation</h2><div class="panel stack">{iso}</div></section>

<section id="method"><h2>Method</h2><div class="panel stack">{NAR.METHOD}</div></section>
<footer>{NAR.FOOTER}</footer></div>
<script type="application/json" id="evdata">{evjson}</script>
<script>{EV_JS}</script><script>{K.JS}</script></body></html>'''
    with open(out_path, "w") as f:
        f.write(page)
    print("wrote", out_path, len(page))


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "exco_agents.html"))
