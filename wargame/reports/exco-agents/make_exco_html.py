"""Build exco_agents.html: the profiles of the fifteen per-executive agents (one per member of each company's default
ExCo), from data/people.json (evidence counts per person, from the profile evidence files), data/agents/<agent>.json
(each agent's profile, drafted and verified against the evidence) and the evidence files themselves.

Usage: python3 make_exco_html.py [out.html]"""
import collections
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.realpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(HERE, "..", "dash-2050"))
sys.path.insert(0, HERE)
import page_kit as K  # noqa: E402
import check_agents as CA  # noqa: E402
import narrative_exco as NAR  # noqa: E402

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

EV = CA.EV
ITEMS = collections.defaultdict(list)          # each person's own items in their evidence file (not shared JV tags)
for a, p in BY.items():
    for line in open(os.path.join(REPO, p["evidence_file"])):
        if line.strip():
            e = json.loads(line)
            if e.get("exec_id") == p["exec_id"]:
                ITEMS[a].append(e)
PERSP = {"own_words": ("Own words", "s1"), "filing": ("Board Report text", "s2"), "observed_by_boeing": ("Remark by Boeing", "s3"),
         "observed_by_pratt_whitney": ("Remark by RTX / P&W", "s3"), "analyst_question": ("Analyst's question", "s3")}
CITE = {"own_words": "own words", "filing": "Board Report text, not speech", "observed_by_boeing": "as quoted by Boeing",
        "observed_by_pratt_whitney": "as quoted by RTX / Pratt & Whitney", "analyst_question": "an analyst's question",
        "own_behaviour": "company record", "own_behaviour_observed_by_boeing_or_analysts": "observed by Boeing or analysts"}


def depth(a):
    """Depth of the person's record, from the count of items in their own words."""
    n = BY[a]["n_own_words"]
    return "Deep" if n >= 100 else "Moderate" if n >= 25 else "Thin" if n >= 5 else "Filing-based"


DEPTH_NOTE = {"Deep": "100 or more items in own words", "Moderate": "25 to 99 items in own words", "Thin": "fewer than 25 items in own words",
              "Filing-based": "almost nothing in own words; built from the Board Report"}


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


def rich(text):
    """Escape text and render any evidence ids in it as hoverable id chips."""
    t = esc(text or "")
    t = GROUP.sub(lambda m: " " + eids(re.findall(IDS, m.group(1))), t)
    parts = re.split(r"(<span class=\"eids\">.*?</span></span>)", t)
    return "".join(x if x.startswith('<span class="eids">') else BARE.sub(lambda m: eids([m.group(1)]), x) for x in parts)


def ids_html(h):
    """Narrative HTML with its [ID] groups rendered as id chips (the text is already HTML)."""
    return GROUP.sub(lambda m: " " + eids(re.findall(IDS, m.group(1))), h)


def infer(flag):
    return ' <span class="inf">inference</span>' if flag else ""


def year(d):
    return int(d[:4]) + (int(d[5:7]) - 1) / 12 + (int(d[8:10]) - 1) / 365 if d else None


# ── charts ──
def evidence_bars(w, label_w, narrow=False):
    rh, gh, top, bot = 24, 22, 8, 34
    x0, x1 = label_w, w - (44 if narrow else 64)
    hi = 450
    sx = lambda v: x0 + v / hi * (x1 - x0)
    h = top + len(SIDES) * gh + len(ORDER) * rh + bot
    out = [K.svg_open(w, h, "Evidence items behind each agent, split by whose words they are", "chart narrow" if narrow else "chart")]
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
            other = tot - own
            lab = SHORT[a] if narrow else f"{SHORT[a]} · {BY[a]['seat'] if BY[a]['seat'] != 'Operating head' else 'Ops head'}"
            out.append(f'<text x="{x0 - 8}" y="{y + 16}" text-anchor="end" class="rowlab sm">{esc(lab)}</text>')
            segs = [(own, "s1")] + [(c.get(k, 0), PERSP[k][1]) for k in PERSP if k != "own_words"]
            segs = [(n, v) for n, v in segs if n]
            start = 0
            for j, (n, var) in enumerate(segs):
                out.append(f'<path d="{K.hbar_path(sx(start), sx(start + n), y + 5, 14, r=3 if j == len(segs) - 1 else 0)}" fill="var(--{var})"/>')
                start += n
            out.append(f'<text x="{sx(tot) + 6:.1f}" y="{y + 16}" class="val sm">{tot}</text>')
            rows = [(str(tot), "evidence items", None)] + [(str(c[k]), PERSP[k][0], f"var(--{PERSP[k][1]})") for k in PERSP if c.get(k)]
            out.append(f'<rect x="0" y="{y}" width="{w}" height="{rh}" class="hit" {K.mark_attrs((BY[a]["name"], "", None), *rows)}/>')
            y += rh
    out.append(f'<text x="{x0}" y="{h - 4}" class="tick">Items in the evidence file</text></svg>')
    return "".join(out)


def evidence_rug():
    w, left, right, top, bot, rh, gh = 760, 150, 16, 8, 34, 24, 22
    lo, hi = 2012, 2026.5
    sx = lambda v: left + (v - lo) / (hi - lo) * (w - left - right)
    h = top + len(SIDES) * gh + len(ORDER) * rh + bot
    out = [K.svg_open(w, h, "When each agent's evidence was said or written: one tick per item", "chart rug")]
    for yr in range(2012, 2027, 2):
        out.append(f'<line x1="{sx(yr):.1f}" x2="{sx(yr):.1f}" y1="{top}" y2="{h - bot}" class="grid"/>'
                   f'<text x="{sx(yr):.1f}" y="{h - bot + 16}" text-anchor="middle" class="tick">{yr}</text>')
    y = top
    for s in SIDES:
        out.append(f'<text x="0" y="{y + 15}" class="grp">{esc(COMPANY[s].upper())}</text>')
        y += gh
        for a in ROSTER[s]:
            out.append(f'<text x="{left - 8}" y="{y + 16}" text-anchor="end" class="rowlab sm">{esc(SHORT[a])}</text>')
            dates = sorted(e["date"] for e in ITEMS[a] if e.get("date"))
            for e in sorted(ITEMS[a], key=lambda e: e.get("perspective") == "own_words"):
                if e.get("date"):
                    x = sx(year(e["date"]))
                    out.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{y + 4}" y2="{y + 20}" stroke="var(--{PERSP.get(e.get("perspective"), ("", "s3"))[1]})" stroke-width="1.4" opacity=".75"/>')
            by_year = collections.Counter(d[:4] for d in dates)
            rows = [(f"{dates[0]} to {dates[-1]}" if dates else "no dated items", "", None)] + \
                   [(str(n), yy, None) for yy, n in sorted(by_year.items())]
            out.append(f'<rect x="0" y="{y}" width="{w}" height="{rh}" class="hit" {K.mark_attrs((BY[a]["name"], "", None), *rows)}/>')
            y += rh
    out.append(f'<text x="{left}" y="{h - 4}" class="tick">Date of the call, conference or filing</text></svg>')
    return "".join(out)


def legend_persp():
    return ('<div class="legend">' + "".join(f'<span><i class="sq" style="background:var(--{v})"></i>{esc(t)}</span>'
                                             for t, v in [("Own words (transcripts)", "s1"), ("Airbus Board Report text", "s2"),
                                                          ("Remarks by others about them, analysts' questions", "s3")]) + "</div>")


def evidence_table():
    rows = []
    for a in ORDER:
        c = collections.Counter(e.get("perspective") for e in ITEMS[a])
        dates = sorted(e["date"] for e in ITEMS[a] if e.get("date"))
        rows.append([f"{esc(BY[a]['name'])} <span class=muted>({esc(COMPANY[BY[a]['side']])}, {esc(BY[a]['seat'])})</span>", str(len(ITEMS[a])),
                     str(c.get("own_words", 0)), str(len(ITEMS[a]) - c.get("own_words", 0)), dates[0] if dates else "—", dates[-1] if dates else "—",
                     esc(depth(a))])
    return K.tview("evidence by person", ["Person", "Items", "Own words", "Other", "First", "Last", "Record"], rows, num_cols=[1, 2, 3, 4, 5])


# ── roster, protocol ──
VETO_CHIP = '<span class="chip veto">veto</span>'


def roster():
    head = '<div class="rh"></div>' + "".join(f'<div class="rh">{s}</div>' for s in SEATS)
    cells = []
    for s in SIDES:
        cells.append(f'<div class="rc">{esc(COMPANY[s])}<span class="small muted">{esc(BY[ROSTER[s][0]]["team"])}</span></div>')
        for a in ROSTER[s]:
            p, pr = BY[a], PROF[a]
            lv = depth(a)
            own = p["n_own_words"]
            steps = ", ".join(pr.get("protocol_steps") or []).replace("_", " ")
            cells.append(f'<a class="rcell" href="#{a}"><span class="seat">{esc(p["seat"])}</span><b>{esc(p["name"])}</b>'
                         f'<span class="small muted">{esc(p["title"])}</span>'
                         f'<span class="chips"><span class="chip">{len(ITEMS[a])} items</span>'
                         f'<span class="chip">{own} own words</span><span class="chip lv lv-{lv.lower()}">{esc(lv)} record</span>'
                         f'{VETO_CHIP if pr.get("veto_holder") else ""}</span>'
                         f'<span class="small muted">Steps: {esc(steps)}</span></a>')
    return f'<div class="roster">{head}{"".join(cells)}</div>'


def protocol():
    steps = "".join(f"<li><b>{esc(t)}</b><br>{esc(d)}</li>" for t, d in NAR.STEPS)
    rows = [[esc(COMPANY[s])] + [x for x in NAR.TEAM_RULES[s]] for s in SIDES]
    return (f'<ol class="loop">{steps}</ol>'
            + K.table(["Company", "Frames and decides", "Tests", "Vetoes and how binding"], rows))


# ── cards ──
def lst(items, ordered=False, key="text"):
    tag = "ol" if ordered else "ul"
    return f"<{tag} class=\"facts\">" + "".join(f"<li>{rich(it[key])}{infer(it.get('inference'))} {eids(it.get('ids'))}</li>" for it in items) + f"</{tag}>"


def quote_html(q):
    e = EV.get(q["id"], {})
    persp = q.get("perspective") or e.get("perspective")
    note = CITE.get(persp, persp or "")
    ocr = ' <span class="inf">PDF text as extracted</span>' if re.search(r"[A-Za-z,]{22,}", q["quote"]) else ""
    return (f'<blockquote class="q{"" if persp == "own_words" else " q-other"}"><p>“{esc(q["quote"])}”</p>'
            f'<footer>{eids([q["id"]])} · {esc(q.get("date") or "")} · {esc((q.get("doc") or "")[:70])} · <b>{esc(note)}</b>{ocr}</footer></blockquote>')


def card(a):
    p, pr = BY[a], PROF[a]
    ev = pr["evidence"]
    lv = depth(a)
    thin_flag = lv in ("Thin", "Filing-based")
    conf = "".join(f'<li><b>{esc(c["area"])}:</b> {rich(c["level"])}</li>' for c in ev.get("confidence_by_area") or [])
    tests = K.table(["Test", "Threshold or rule", "Evidence"],
                    [[rich(t["test"]) + infer(t.get("inference")), rich(t["threshold"]), eids(t.get("ids"))] for t in pr["tests"]])
    vetoes = "".join(f'<li><span class="chip b-{esc(v["binding"])}">{esc(v["binding"])}</span> {rich(v["ground"])} {eids(v.get("ids"))}</li>'
                     for v in pr["vetoes"]) or "<li>None.</li>"
    levers = K.table(["Lever", "Position", "Evidence"],
                     [[rich(l["lever"]) + infer(l.get("inference")), rich(l["position"]), eids(l.get("ids"))] for l in pr["lever_positions"]])
    coll = "".join(f'<li><b>{esc(c["name"])}.</b> {rich(c["relation"])}</li>' for c in pr["colleagues"])
    voiced = pr.get("dash2050_voiced") or {}
    vrows = "".join(f'<li><b>Round {r["round"]}.</b> {rich(r["line"])}</li>' for r in voiced.get("by_round") or [])
    gaps = "".join(f"<li>{rich(g)}</li>" for g in pr["thin"]["gaps"])
    extra = p.get("extra_items_same_person_other_tag") or 0
    extra_txt = f" Plus {extra} items tagged to the CFM Joint Venture that he also said." if extra else ""
    return f'''<article class="pcard panel" id="{a}">
<header class="ph"><p class="label">{esc(COMPANY[p["side"]])} · {esc(p["seat"])} · agent <code>{esc(a)}</code></p>
<h3>{esc(p["name"])}</h3><p class="muted small">{esc(p["title"])}. {rich(pr["role_dates"])}</p>
<p class="chips"><span class="chip">{len(ITEMS[a])} evidence items</span><span class="chip">{p["n_own_words"]} in own words</span>
<span class="chip">{esc(ev.get("first") or "—")} to {esc(ev.get("last") or "—")}</span><span class="chip lv lv-{lv.lower()}">{esc(lv)} record</span>
{"<span class='chip veto'>holds a veto</span>" if pr.get("veto_holder") else ""}<span class="chip">Steps: {esc(", ".join(pr.get("protocol_steps") or []).replace("_", " "))}</span></p>
<p class="mandate">{rich(pr["mandate"])}</p></header>
<div class="grid2"><div><p class="label">What {esc(SHORT[a])} is paid to protect</p>{lst(pr["objective_ranked"], ordered=True)}</div>
<div><p class="label">How {esc(SHORT[a])} decides</p>{lst(pr["decision_style"])}</div></div>
<p class="label">Tests applied every round</p>{tests}
<p class="label">Vetoes and red lines</p><ul class="facts">{vetoes}</ul>
<p class="label">Voice</p><p class="small">{rich(pr["voice"]["style"])}</p><div class="quotes">{"".join(quote_html(q) for q in pr["voice"]["quotes"])}</div>
<div class="thin{" warn" if thin_flag else ""}"><p class="label">Where the record is thin</p><ul class="facts">{gaps}</ul>
<p class="small"><b>When the record is silent:</b> {rich(pr["thin"]["fallback"])}</p></div>
<details class="more"><summary>Lever positions, rivals, colleagues, biases, evidence base, dash-2050 role-play</summary>
<p class="label">Positions on the game's levers</p>{levers}
<div class="grid2"><div><p class="label">How {esc(SHORT[a])} reads the rivals</p>{lst(pr["rivals"])}</div>
<div><p class="label">Colleagues</p><ul class="facts">{coll}</ul></div></div>
<div class="grid2"><div><p class="label">Biases the agent displays</p>{lst(pr["biases"])}</div>
<div><p class="label">Evidence base</p><p class="small">{rich(ev["sources_note"])}{esc(extra_txt)}</p><p class="small"><b>Overall:</b> {rich(ev["confidence_overall"])}</p><ul class="facts small">{conf}</ul></div></div>
<p class="label">As voiced in dash-2050 (the single company agent's role-play, not evidence)</p><p class="small">{rich(voiced.get("summary", ""))}</p><ul class="facts small">{vrows}</ul>
</details></article>'''


def cards():
    out = []
    for s in SIDES:
        out.append(f'<h3 class="co" id="co-{s}">{esc(COMPANY[s])} <span class="muted small">{esc(BY[ROSTER[s][0]]["team"])}</span></h3>')
        out.append('<div class="stack">' + "".join(card(a) for a in ROSTER[s]) + "</div>")
    return "".join(out)


def tiles():
    n_items = sum(len(ITEMS[a]) for a in ORDER)
    n_own = sum(1 for a in ORDER for e in ITEMS[a] if e.get("perspective") == "own_words")
    thin = [SHORT[a] for a in ORDER if depth(a) in ("Thin", "Filing-based")]
    quotes = sum(len(PROF[a]["voice"]["quotes"]) for a in ORDER)
    t = [("Agents", "15", "Three per company: the CEO, the CFO and the operating head of each default 2026 ExCo"),
         ("Evidence items", f"{n_items:,}", f"{n_own:,} in the person's own words; Airbus mostly Board Report text"),
         ("Cited in the profiles", f"{len(CITED):,} ids", f"every id resolves to an evidence item; {quotes} signature quotes checked word for word"),
         ("Thin or filing-based", f"{len(thin)} of 15", ", ".join(thin) + ": each falls back on the company profile or a named colleague"),
         ("Game", "Not run", "Agents installed and isolated; the round script is written and dry-run with stub agents only")]
    return '<div class="tiles">' + "".join(f'<div class="panel tile"><div class="k">{esc(k)}</div><div class="v">{esc(v)}</div><div class="d">{esc(d)}</div></div>'
                                           for k, v, d in t) + "</div>"


EXTRA_CSS = """
.roster { display: grid; grid-template-columns: 150px repeat(3, minmax(0, 1fr)); gap: 8px; }
.roster .rh { font: 500 .72rem/1.3 var(--font-mono); letter-spacing: .1em; text-transform: uppercase; color: var(--muted); padding: 0 4px; }
.roster .rc { font: 700 1.25rem/1.1 var(--font-display); display: flex; flex-direction: column; gap: 4px; padding: 10px 4px; }
.roster .rc .small { font: 400 .78rem/1.3 var(--font-mono); }
.rcell { display: flex; flex-direction: column; gap: 3px; background: var(--surface); border: 1px solid var(--line); border-radius: var(--r);
  padding: 10px 12px; text-decoration: none; min-width: 0; }
.rcell:hover, .rcell:focus-visible { border-color: var(--fg); }
.rcell b { font-weight: 600; font-size: 1rem; }
.rcell .seat { display: none; font: 500 .7rem/1.3 var(--font-mono); letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }
.chips { display: flex; flex-wrap: wrap; gap: 4px 6px; margin: 4px 0; }
.chip { font: 500 .74rem/1.2 var(--font-mono); padding: 2px 7px; border-radius: 999px; background: var(--sunk); color: var(--muted); border: 1px solid var(--line); white-space: nowrap; }
.chip.lv-deep, .chip.lv-moderate { color: var(--fg); }
.chip.lv-thin, .chip.lv-filing-based { color: var(--fg); border-color: var(--s2); }
.chip.veto { color: var(--fg); border-color: var(--fg); }
.chip.b-formal { color: var(--fg); border-color: var(--fg); } .chip.b-soft { border-style: dashed; color: var(--fg); }
.chip.b-inference { border-style: dotted; } .chip.b-none { opacity: .8; }
.pcard { scroll-margin-top: 12px; }
.pcard h3 { font-size: 1.7rem; margin: 2px 0 4px; }
.pcard .label { margin-top: 16px; }
.pcard header .label { margin-top: 0; }
.mandate { font-size: 1.02rem; margin-top: 6px; max-width: 90ch; }
.inf { font: italic 500 .72rem/1 var(--font-mono); color: var(--muted); border: 1px dotted var(--faint); border-radius: 4px; padding: 1px 4px; white-space: nowrap; }
.eids { white-space: normal; }
.eid { font: 500 .72rem/1.2 var(--font-mono); color: var(--muted); border-bottom: 1px dotted var(--faint); cursor: help; white-space: nowrap; }
.eid:focus-visible { outline: 2px solid var(--fg); outline-offset: 1px; border-radius: 2px; }
td .eids { display: inline-block; max-width: 13rem; }
.quotes { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 10px; }
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
h3.co { font-size: 1.6rem; margin: 30px 0 10px; scroll-margin-top: 12px; }
.loop li b { font-weight: 600; }
code { font: .86em var(--font-mono); }
@media (max-width: 760px) {
  .roster { grid-template-columns: 1fr; }
  .roster .rh { display: none; }
  .roster .rc { padding: 14px 0 2px; }
  .rcell .seat { display: block; }
  .quotes { grid-template-columns: 1fr; }
  td .eids { max-width: 8rem; }
  .chart.rug { min-width: 720px; }
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
    """Facts the narrative states, checked against the data."""
    n = {a: len(ITEMS[a]) for a in ORDER}
    dates = {a: sorted({e["date"] for e in ITEMS[a]}) for a in ORDER}
    yrs = collections.Counter(e["date"][:4] for a in ORDER for e in ITEMS[a])
    ortberg_collins = [e["date"] for e in ITEMS["boeing-ortberg"] if e.get("source") == "rtx_transcripts"]
    airbus_feb = [e for a in ("airbus-toepfer", "airbus-wagner") for e in ITEMS[a]]
    faury_br = [e for e in ITEMS["airbus-faury"] if e.get("source") == "airbus_fy2025"]
    C = [("min is Wagner 2", min(n, key=n.get) == "airbus-wagner" and n["airbus-wagner"] == 2),
         ("max is Culp 425", max(n, key=n.get) == "cfm-culp" and n["cfm-culp"] == 425),
         ("JV extras 51/7/7", [BY[a].get("extra_items_same_person_other_tag") for a in ("cfm-culp", "cfm-ghai", "cfm-ali")] == [51, 7, 7]),
         ("Airbus one own-words line, Faury", [a for a in ROSTER["airbus"] for e in ITEMS[a] if e.get("perspective") == "own_words"] == ["airbus-faury"]),
         ("six in ten 2023-2025", 0.55 <= sum(yrs[y] for y in ("2023", "2024", "2025")) / sum(yrs.values()) < 0.65),
         ("Malave one call 2025-10-29", dates["boeing-malave"] == ["2025-10-29"] and n["boeing-malave"] == 11),
         ("Eddy one day 2023-06-19", dates["pratt-whitney-eddy"] == ["2023-06-19"] and n["pratt-whitney-eddy"] == 21),
         ("Pope eight, 2012-2022", n["boeing-pope"] == 8 and dates["boeing-pope"][0][:4] == "2012" and dates["boeing-pope"][-1][:4] == "2022"),
         ("Ortberg 14 Collins items 2017/2019", len(ortberg_collins) == 14 and {d[:4] for d in ortberg_collins} == {"2017", "2019"}),
         ("Toepfer/Wagner all 2026-02-18", {e["date"] for e in airbus_feb} == {"2026-02-18"}),
         ("Faury 47 Board Report lines 2026-02-18", len(faury_br) == 47 and {e["date"] for e in faury_br} == {"2026-02-18"}),
         ("depth counts 6/2/4/3", collections.Counter(depth(a) for a in ORDER) == {"Deep": 6, "Moderate": 2, "Thin": 4, "Filing-based": 3}),
         ("Airbus all filing-based", [depth(a) for a in ROSTER["airbus"]] == ["Filing-based"] * 3)]
    nar_ids = set(CA.IDRE.findall(json.dumps(NAR.FINDINGS)))
    C.append(("narrative ids exist", nar_ids <= set(EV)))
    deep = sorted((a for a in ORDER if depth(a) == "Deep"), key=lambda a: -BY[a]["n_own_words"])
    C.append(("deep six named", [SHORT[a] for a in deep] == ["Culp", "Mitchill", "Calio", "Erginbilgic", "Ghai", "Ortberg"]))
    C.append(("Ali 13, Eddy 21", n["cfm-ali"] == 13 and n["pratt-whitney-eddy"] == 21))
    bad = [c for c, ok in C if not ok]
    if bad:
        print("NARRATIVE CHECKS FAILED:", bad)
    return bad


def build(out_path):
    checks()
    css = K.CSS + EXTRA_CSS
    ev = {}
    for i in CITED:
        e = EV[i]
        q = e.get("quote") or e.get("finding") or ""
        src = (e.get("speaker") or "")[:80] if e.get("quote") else "Finding from an analyst model (not a quote)"
        ev[i] = {"date": e.get("date"), "doc": (e.get("doc") or "")[:60], "p": CITE.get(e.get("perspective"), (e.get("perspective") or "").replace("_", " ")),
                 "s": src, "q": q if len(q) <= 420 else q[:417] + "…"}
    evjson = json.dumps(ev, ensure_ascii=False).replace("</", "<\\/")
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ExCo Agent Profiles</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{css}</style></head><body><div class="wrap">
<header class="top"><p class="eyebrow">Boeing Product Development · war game agents · BOEING PROPRIETARY</p>
<h1>{esc(NAR.TITLE)}</h1><p class="lede">{NAR.LEDE}</p>
<nav class="toc"><a href="#summary">Summary</a><a href="#roster">Roster</a><a href="#evidence">Evidence</a><a href="#protocol">How a round runs</a>
{"".join(f'<a href="#co-{s}">{esc(COMPANY[s])}</a>' for s in SIDES)}<a href="#isolation">Isolation</a><a href="#method">Method</a></nav></header>

<section id="summary"><h2>Summary</h2>{tiles()}
<div class="bl">{"".join(f'<div class="panel"><div><b>{esc(t)}</b>{ids_html(x)}</div></div>' for t, x in NAR.FINDINGS)}</div></section>

<section id="roster"><h2>The fifteen agents</h2><p class="lede">{NAR.ROSTER_LEDE}</p>{roster()}</section>

<section id="evidence"><h2>What each agent is built on</h2><p class="lede">{NAR.EVIDENCE_LEDE}</p><div class="stack">
<div class="panel"><p class="ctitle">{esc(NAR.BARS_TITLE)}</p>{legend_persp()}<div class="only-wide">{evidence_bars(760, 170)}</div><div class="only-narrow">{evidence_bars(360, 84, narrow=True)}</div>
<p class="cap">{NAR.BARS_CAP}</p></div>
<div class="panel"><p class="ctitle">{esc(NAR.RUG_TITLE)}</p>{legend_persp()}<div class="cw" data-focus="560">{evidence_rug()}</div>
<p class="cap">{NAR.RUG_CAP}</p>{evidence_table()}</div></div></section>

<section id="protocol"><h2>How a round will run</h2><p class="lede">{NAR.PROTOCOL_LEDE}</p><div class="panel">{protocol()}<p class="cap">{NAR.PROTOCOL_CAP}</p></div></section>

<section id="agents"><h2>The agents</h2><p class="lede">{NAR.CARDS_LEDE}</p>{cards()}</section>

<section id="isolation"><h2>Isolation</h2><div class="panel stack">{NAR.ISOLATION}</div></section>

<section id="method"><h2>Method</h2><div class="panel stack">{NAR.METHOD}</div></section>
<footer>{NAR.FOOTER}</footer></div>
<script type="application/json" id="evdata">{evjson}</script>
<script>{EV_JS}</script><script>{K.JS}</script></body></html>'''
    with open(out_path, "w") as f:
        f.write(page)
    print("wrote", out_path, len(page))


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "exco_agents.html"))
