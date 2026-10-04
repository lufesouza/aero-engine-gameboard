"""Build plain-text role files from the executive profiles.

For each company, one .txt per executive role (CEO, CFO, operating seat). Each
file holds the role's seat in the ExCo, its holders, and their full profiles
(current holder first), plus a text copy of the leadership teams. The Markdown
profiles stay the source of truth; re-run this after editing them:

    python3 wargame/profiles/build/make_role_txt.py

Output stays inside each company's folder (profiles/<company>/executives/roles/)
so the isolation hook keeps each player away from the other company's files.
"""
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIDTH = 100

# Seat descriptions follow the ExCo order in each company's README.md and teams.md.
SEATS = {
    "ceo": "The CEO frames the turn: is the company ready (stability, balance sheet, technology), what "
           "has the rival done, which levers are in play. The CEO proposes and, under every team's "
           "decision rule, takes the final call; the CEO's Voice lines are used for public statements "
           "and disclosure.",
    "cfo": "The CFO tests cash, debt, the rating and the hurdle: the slip test, capex and strain from the "
           "engine, and whether a plan is fundable in the years it spends. Financial commitments in "
           "public statements use the CFO's register.",
    "ops": "The operating seat tests production, quality and the supply chain: KPI gates for rate "
           "changes, supplier and engine readiness, development risk and concurrency.",
}

ROLES = {
    "boeing": [
        {
            "file": "boeing_ceo.txt",
            "title": "BOEING: CHIEF EXECUTIVE OFFICER (CEO)",
            "label": "Chief Executive Officer (CEO)",
            "seat": "ceo",
            "people": ["ortberg", "calhoun", "muilenburg", "mcnerney"],
            "notes": [
                "Greg Smith, as CFO, was interim CEO at the turn of 2020, before Calhoun [BX-0205]. "
                "His profile is in boeing_cfo.txt.",
            ],
        },
        {
            "file": "boeing_cfo.txt",
            "title": "BOEING: CHIEF FINANCIAL OFFICER (CFO)",
            "label": "Chief Financial Officer (CFO)",
            "seat": "cfo",
            "people": ["malave", "west", "smith", "bell"],
            "notes": [],
        },
        {
            "file": "boeing_coo_bca.txt",
            "title": "BOEING: OPERATING SEAT (COO / PRESIDENT AND CEO, BOEING COMMERCIAL AIRPLANES)",
            "label": "Operating seat (COO / President and CEO of Boeing Commercial Airplanes)",
            "seat": "ops",
            "people": ["pope", "deal", "conner", "albaugh"],
            "notes": [
                "Dennis Muilenburg was Vice Chairman, President and COO from 2014 until he became CEO in "
                "July 2015 [BX-0830, BX-0886]. He holds the COO seat in team mcnerney-smith-conner-2013. "
                "His full profile, including the COO years, is in boeing_ceo.txt.",
                "Team muilenburg-smith-2017 has no BCA head in the evidence. Team calhoun-smith-2020 "
                "gives manufacturing, the supply chain and services to Smith as CFO (from April 2020) "
                "[BX-0221]; see boeing_cfo.txt.",
            ],
        },
    ],
    "airbus": [
        {
            "file": "airbus_ceo.txt",
            "title": "AIRBUS: CHIEF EXECUTIVE OFFICER (CEO)",
            "label": "Chief Executive Officer (CEO)",
            "seat": "ceo",
            "people": ["faury", "historical:enders"],
            "notes": [],
        },
        {
            "file": "airbus_cfo.txt",
            "title": "AIRBUS: CHIEF FINANCIAL OFFICER (CFO)",
            "label": "Chief Financial Officer (CFO)",
            "seat": "cfo",
            "people": ["toepfer"],
            "notes": ["No earlier Airbus CFO is in the sources."],
        },
        {
            "file": "airbus_coo_commercial_aircraft.txt",
            "title": "AIRBUS: OPERATING SEAT (CEO, COMMERCIAL AIRCRAFT)",
            "label": "Operating seat (CEO of Commercial Aircraft)",
            "seat": "ops",
            "people": ["wagner", "historical:scherer", "historical:leahy"],
            "notes": [
                "Airbus's operating seat in the game is the CEO of Commercial Aircraft. No separate Airbus "
                "COO is in the sources. John Leahy (chief commercial officer, sales) is included here as "
                "the historical commercial lead.",
            ],
        },
    ],
}

HIST_KEYS = {"enders": "Tom Enders", "leahy": "John Leahy", "scherer": "Christian Scherer"}
ID_PREFIX = {"boeing": ("BX", "B"), "airbus": ("AX", "A")}
DEFAULT_TEAM = {"boeing": "ortberg-malave-pope-2026", "airbus": "faury-toepfer-wagner-2026"}


# --------------------------------------------------------------------------- Markdown to text

def inline(s):
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r"\1 (\2)", s)
    s = s.replace("**", "")
    s = re.sub(r"(?<![\w*])\*(?=\S)([^*\n]+?)(?<=\S)\*(?![\w*])", r"\1", s)
    s = s.replace("`", "")
    return s


def wrap(text, first, rest):
    return textwrap.wrap(text, WIDTH, initial_indent=first, subsequent_indent=rest,
                         break_long_words=False, break_on_hyphens=False) or [first.rstrip()]


def cells(line):
    return [inline(c.strip()) for c in line.strip().strip("|").split("|")]


def table(rows, indent=""):
    head, body = rows[0], rows[1:]
    n = len(head)
    body = [r + [""] * (n - len(r)) for r in body]
    widths = [max(len(r[i]) for r in [head] + body) for i in range(n)]
    if sum(widths) + 3 * (n - 1) + len(indent) <= WIDTH:
        fmt = lambda r: indent + " | ".join(c.ljust(w) for c, w in zip(r, widths)).rstrip()
        out = [fmt(head), indent + "-+-".join("-" * w for w in widths)]
        return out + [fmt(r) for r in body]
    # Too wide: one record per row, first column as the record's heading.
    out = []
    for r in body:
        out += wrap(f"* {head[0]}: {r[0]}" if head[0] else f"* {r[0]}", indent, indent + "  ")
        for h, c in zip(head[1:], r[1:]):
            if c:
                out += wrap(f"{h}: {c}" if h else c, indent + "    ", indent + "      ")
        out.append("")
    return out[:-1]


def md_to_text(md, demote=0):
    """Convert one Markdown profile to wrapped plain text. `demote` shifts heading levels down."""
    out, lines, i = [], md.split("\n"), 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if s.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                if not re.fullmatch(r"\|?[\s:|-]+\|?", lines[i].strip()):
                    rows.append(cells(lines[i]))
                i += 1
            out += table(rows, " " * (len(line) - len(line.lstrip())))
            continue
        if s.startswith("```"):
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                out.append("    " + lines[i].rstrip())
                i += 1
            i += 1
            continue
        m = re.match(r"(#{1,6})\s+(.*)", s)
        if m:
            level, text = len(m.group(1)) + demote, inline(m.group(2))
            if level <= 2:
                out += ["", text.upper(), ("=" if level == 1 else "-") * min(len(text), WIDTH)]
            elif level == 3:
                out += ["", text, "~" * min(len(text), WIDTH)]
            else:
                out += ["", text + ":"]
            i += 1
            continue
        if re.fullmatch(r"-{3,}|\*{3,}", s):
            out += ["", " " * 40 + "* * *"]
            i += 1
            continue
        if not s:
            out.append("")
            i += 1
            continue
        lead = line[: len(line) - len(line.lstrip())]
        m = re.match(r"([-*+]|\d+\.)\s+(.*)", s)
        if m:
            marker = "-" if m.group(1) in "-*+" else m.group(1)
            first = lead + marker + " "
            out += wrap(inline(m.group(2)), first, " " * len(first))
        else:
            out += wrap(inline(s), lead, lead)
        i += 1
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(l.rstrip() for l in out)).strip("\n")
    return text


# --------------------------------------------------------------------------- inputs

def readme_rows(company):
    """Index rows from the company's executives README, keyed by exec_id."""
    md = (ROOT / company / "executives" / "README.md").read_text()
    rows, header = {}, None
    for line in md.split("\n"):
        if not line.startswith("|"):
            header = None
            continue
        if re.fullmatch(r"\|[\s:|-]+\|?", line.strip()):
            continue
        c = cells(line)
        if header is None:
            header = c
            continue
        rec = dict(zip(header, c))
        if company == "boeing" and "Executive (file)" in rec:
            m = re.search(r"\((\w+)\.md\)", rec["Executive (file)"])
            if m:
                rec["Name"] = re.sub(r"\s*\(\w+\.md\)$", "", rec["Executive (file)"])
                rows[m.group(1)] = rec
        elif company == "airbus" and "exec_id" in rec:
            rows[rec["exec_id"]] = rec
        elif "Team id" in rec:
            rows.setdefault("_teams", []).append(rec["Team id"])
    teams = rows.pop("_teams", [])
    for key, rec in rows.items():
        if company == "boeing":
            years = {t.rsplit("-", 1)[1]: t for t in teams}
            rec["Teams"] = re.sub(r"\b(20\d\d)\b", lambda m: years.get(m.group(1), m.group(1)), rec.get("Teams", ""))
        elif key in DEFAULT_TEAM["airbus"].split("-"):
            rec["Teams"] = DEFAULT_TEAM["airbus"]
        if DEFAULT_TEAM[company] in rec.get("Teams", ""):
            rec["Teams"] = rec["Teams"].replace(DEFAULT_TEAM[company], DEFAULT_TEAM[company] + " (DEFAULT)")
    return rows


def historical_parts(company):
    md = (ROOT / company / "executives" / "historical.md").read_text()
    parts = re.split(r"\n(?=## )", md)
    preface = parts[0].split("\n", 1)[1].strip()
    preface = re.sub(r"\n-{3,}\s*$", "", preface).strip()
    sections = {}
    for p in parts[1:]:
        title = p.split("\n", 1)[0][3:]
        body = re.sub(r"\n-{3,}\s*$", "", p).strip()
        for key, name in HIST_KEYS.items():
            if title.startswith(name):
                sections[key] = (title, body)
        if title.startswith("Gaps common"):
            sections["gaps"] = (title, body)
    return preface, sections


def person_block(company, person, idx, total, current, team_rows):
    rule = "#" * WIDTH
    if person.startswith("historical:"):
        key = person.split(":")[1]
        preface, sections = historical_parts(company)
        title, body = sections[key]
        label = f"PROFILE {idx} OF {total}: {inline(title).upper()} (HISTORICAL, OUTSIDE VIEW)"
        md = ("### About the historical cards\n\n" + preface + "\n\n" + body.split("\n", 1)[1]
              + "\n\n" + sections["gaps"][1].replace("## ", "### ", 1))
        src = f"historical.md, section \"{inline(title)}\""
        text = md_to_text(md)
    else:
        md = (ROOT / company / "executives" / f"{person}.md").read_text()
        title = md.split("\n", 1)[0].lstrip("# ").strip()
        status = "CURRENT HOLDER" if idx == 1 and current else "PREVIOUS HOLDER"
        label = f"PROFILE {idx} OF {total}: {inline(title).upper()} ({status})"
        src = f"{person}.md"
        text = md_to_text(md.split("\n", 1)[1], demote=0)
    head = [rule, *wrap(label, "", ""), *wrap(f"Source: wargame/profiles/{company}/executives/{src}", "", "  ")]
    teams = team_rows.get(person.split(":")[-1], {}).get("Teams")
    if teams:
        head += wrap(f"Teams (see {company}_leadership_teams.txt): {teams}", "", "  ")
    return "\n".join(head + [rule, "", text, ""])


def roster(company, people, team_rows):
    out = []
    for p in people:
        key = p.split(":")[-1]
        r = team_rows.get(key, {})
        name = r.get("Name") or HIST_KEYS.get(key, key)
        if company == "boeing":
            fields = [("Role(s) and dates", "Role(s) and dates"), ("Own-words items", "Own words (ids)"),
                      ("Company items", "Company items"), ("Events", "Events"),
                      ("Confidence", "Confidence"), ("Teams", "Teams")]
        else:
            fields = [("Role", "Role"), ("Dates in the sources", "Dates shown in the sources"),
                      ("Evidence items", "AX items"), ("Own words", "Own words"), ("Confidence", "Confidence")]
        out += wrap(f"- {name}", "", "  ")
        for label, col in fields:
            if r.get(col):
                out += wrap(f"{label}: {r[col]}", "    ", "      ")
        out.append("")
    return out


def role_file(company, role, team_rows, today):
    people = role["people"]
    lines = ["=" * WIDTH, *wrap(role["title"], "", ""),
             "Role profile for the Boeing vs Airbus war game", "=" * WIDTH, ""]
    own, co = ID_PREFIX[company]
    lines += wrap(
        f"Plain-text copy of the executive profiles in wargame/profiles/{company}/executives/, built "
        f"{today} by wargame/profiles/build/make_role_txt.py. The Markdown files are the source of "
        f"truth. Bracketed ids ([{own}-0123], [{co}-0456]) point to verified evidence in "
        f"wargame/profiles/{company}/executives/evidence.jsonl and wargame/profiles/{company}/evidence.jsonl. "
        "Section numbers (§) and file names inside a profile refer to that person's Markdown profile; the "
        "same sections appear below under the person's name.", "", "")
    lines.append("")
    lines += wrap("Scope: professional conduct only, from the executives' own words and the company "
                  "record. Inferences are labelled (inference).", "", "")
    lines += ["", "THE SEAT IN THE EXCO", "-" * 20]
    lines += wrap(SEATS[role["seat"]], "", "")
    title = f"HOLDERS ({len(people)}, current first)"
    lines += ["", title, "-" * len(title)]
    lines += roster(company, people, team_rows)
    for n in role["notes"]:
        lines += wrap(f"Note: {n}", "", "      ")
        lines.append("")
    lines.append("")
    blocks = [person_block(company, p, i, len(people), not p.startswith("historical:"), team_rows)
              for i, p in enumerate(people, 1)]
    return "\n".join(lines) + "\n" + "\n\n".join(blocks)


def teams_file(company, today):
    md = (ROOT / company / "executives" / "teams.md").read_text()
    head = ["=" * WIDTH, f"{company.upper()}: LEADERSHIP TEAMS (EXCO CARDS)",
            "Companion to the role files in this folder", "=" * WIDTH, ""]
    head += wrap(f"Plain-text copy of wargame/profiles/{company}/executives/teams.md, built {today} by "
                 "wargame/profiles/build/make_role_txt.py. The Markdown file is the source of truth.", "", "")
    return "\n".join(head) + "\n\n" + md_to_text(md) + "\n"


def readme(company, roles, rows, today):
    lines = [f"{company.upper()} EXECUTIVE ROLE PROFILES (PLAIN TEXT)", "=" * 40, ""]
    lines += wrap(f"Built {today} from the Markdown profiles in wargame/profiles/{company}/executives/ by "
                  "wargame/profiles/build/make_role_txt.py. Re-run it after editing the profiles.", "", "")
    lines += ["", "Files:"]
    for r in roles:
        names = ", ".join(rows.get(p.split(":")[-1], {}).get("Name") or HIST_KEYS.get(p.split(":")[-1], p)
                          for p in r["people"])
        lines += wrap(f"- {r['file']}: {r['label']}. "
                      f"Holders, current first: {names}.", "", "  ")
    lines += wrap(f"- {company}_leadership_teams.txt: the leadership teams, their decision rules and the "
                  "per-turn ExCo deliberation scripts.", "", "  ")
    return "\n".join(lines) + "\n"


def main():
    import datetime
    today = datetime.date.today().isoformat()
    for company, roles in ROLES.items():
        rows = readme_rows(company)
        outdir = ROOT / company / "executives" / "roles"
        outdir.mkdir(exist_ok=True)
        for role in roles:
            (outdir / role["file"]).write_text(role_file(company, role, rows, today).rstrip() + "\n")
        (outdir / f"{company}_leadership_teams.txt").write_text(teams_file(company, today))
        (outdir / "README.txt").write_text(readme(company, roles, rows, today))
        print(company, sorted(p.name for p in outdir.iterdir()))


if __name__ == "__main__":
    main()
