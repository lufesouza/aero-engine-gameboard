"""Game-master briefs for dash-2050: the public rules, the public bulletin, and each player's private brief.

A player's brief holds only (1) public information, identical for everyone, and (2) that player's own position,
projection and payoff grid. No rival's payoff, finances, rationale or covert move is ever written into a brief.
"""
import itertools
import json

import model as M
import rules as R

YEARS_PUBLIC = list(range(2026, 2061))
FIELD_LABEL = {
    "fps": "fps", "fps_engine_code": "fps engine code", "rate_737": "737 rate", "re787": "787 Re-engine",
    "ngsa": "NGSA", "ngsa_engine_code": "NGSA engine code", "rea350": "A350 Re-engine", "delay_tactics": "Delay Tactics",
    "ducted": "Ducted", "open_fan": "Open Fan", "partner_embraer": "Partner Embraer", "lobby_emissions": "Lobby",
    "genx": "GEnx", "gtf2_solo": "GTF2 Solo", "jv_with_rr": "JV with RR", "ultrafan_nb_solo": "UltraFan NB Solo",
    "jv_with_pw": "JV with PW", "ultrafan_wb": "UltraFan WB", "t1000_upgrade": "T1000 upgrade"}
PROG_LABEL = M.PROG_LABEL


def f1(x):
    return "%.1f" % x


def money(x):
    return ("+" if x >= 0 else "−") + "%.2f" % abs(x)


def pct(x):
    return "%.1f%%" % (100 * x)


def public_rules():
    """The rules every player sees (identical text). Rival costs, margins and balance sheets are not in it."""
    P = M.engine_params()
    p = M.af_params()
    return f"""# dash-2050: rules of the game (public; every player has the same text)

**Game master.** The game master (GM) runs the game on the narrowbody/widebody game-theory dashboard. Only the GM sees
the whole board. You see the public record and your own position. You never see another player's payoffs, finances,
orders or reasoning.

**Players.** Boeing and Airbus (airframers); CFM/GE, Pratt & Whitney (P&W) and Rolls-Royce (RR) (engine makers).

**Rounds.** Four decision years: 2030, 2035, 2045, 2050. In each round all five players submit sealed orders at the
same time. The GM adjudicates them and publishes a bulletin before the next round.

**Markets.**
- Narrowbody (NB): {p['NB_PER_YR']:,} aircraft a year. Status quo: Boeing 40%, Airbus 60%.
- Widebody (WB): {p['WB_PER_YR']} aircraft a year. Status quo: Boeing 787 58.8% (100/170), Airbus A350 41.2%.
- NB engines (two per aircraft): status quo CFM 76%, P&W 24%, RR 0%.
- WB engines: status quo CFM/GE (GEnx) 42%, RR (Trent) 58%.

## Moves and timing

| Player | Move (the briefing's wording) | Order field and value | Timing |
|---|---|---|---|
| Boeing | Launch fps with 7-year ramp-up | `fps`: `launch_7yr` | enters service (EIS) 7 years after launch |
| Boeing | Launch fps with 10-year ramp-up | `fps`: `launch_10yr` | EIS 10 years after launch |
| Boeing | Launch fps via Embraer | `fps`: `launch_via_embraer` | EIS 10 years after launch |
| Boeing | Increase 737 production rate by 2030 | `rate_737`: `increase` (2030 round only) | rate up in 2032 |
| Boeing | 787 Re-engine (widebody) | `re787`: `launch` | EIS 5 years after launch |
| Boeing | Do Nothing (737 MAX, 787) | `hold` | |
| Airbus | Launch NGSA | `ngsa`: `launch` | EIS 7 years after launch |
| Airbus | A350 Re-engine (widebody) | `rea350`: `launch` | EIS 5 years after launch |
| Airbus | Delay fps (supply-chain bottleneck), Delay fps (talent poaching) | `delay_tactics` | covert; see below |
| Airbus | Do Nothing (A320neo, A350) | `hold` | |
| CFM/GE | Ducted only / Open Fan only / Open + Ducted | `ducted`, `open_fan`: `launch` | ducted ready 6 years after launch; Open Fan ready 10 years after launch and not before 2045 |
| CFM/GE | Partner with Embraer | `partner_embraer`: `launch` (needs a new CFM engine) | counts 7 years after launch |
| CFM/GE | Lobby governments on emissions | `lobby_emissions`: `launch` | immediate |
| CFM/GE | GEnx upgrade or GEnx investment (widebody) | `genx`: `upgrade_genx9` or `invest_genx` | counts 3 years after launch |
| P&W | Launch GTF2 Solo | `gtf2_solo`: `launch` or `launch_if_selected` | ready 6 years after launch |
| P&W | Joint Venture with Rolls-Royce | `jv_with_rr`: `commit` | see Joint Venture |
| P&W | Do Nothing (continue GTF1) | `hold` | |
| RR | UltraFan narrowbody Solo | `ultrafan_nb_solo`: `launch` or `launch_if_selected` | ready 7 years after launch |
| RR | Joint Venture with P&W | `jv_with_pw`: `commit` | see Joint Venture |
| RR | UltraFan widebody | `ultrafan_wb`: `launch` | ready 6 years after launch; counts only once a re-engined 787 or A350 is in service |
| RR | Trent 1000 upgrade (widebody) | `t1000_upgrade`: `launch` (exclusive with UltraFan WB) | counts 3 years after launch |
| RR | Do Nothing (continue Trent only) | `hold` | |

**Other moves.** You may also propose moves your company has historically made that are not on this list (for example
a pricing campaign, an alliance or a derivative aircraft). Put them in `other_moves` and say whether each is public.
The board does not price them. The GM records them, publishes the public ones, and reports them qualitatively; they
do not change any payoff.

**Launch once, cancel before service.** A launched programme can be cancelled in a later round, until it enters
service (airframes) or is ready (engines). A cancelled programme writes off its spend to date: the bill × years
elapsed ÷ development years, booked in the cancel year. A cancelled programme can be relaunched later as a new one.

## Engines on the new narrowbodies

- When Boeing launches fps or Airbus launches NGSA, it selects an engine code. Until the airframe enters service it
  may change the code in any round. The codes are 1 RR, 2 P&W, 3 CFM, 4 RR & P&W Joint Venture, 5 RR and CFM,
  6 P&W and CFM, 7 all three.
- A code is a request. A maker is fitted only if it has a new NB engine ready by the airframe's EIS: for P&W, GTF2 or
  the Joint Venture engine; for RR, UltraFan NB or the Joint Venture engine. CFM is always available (a LEAP
  derivative if it builds nothing new). A maker that is not ready is dropped. If no one is left, the airframe gets CFM.
- Code 4 needs a formed Joint Venture engine ready by EIS.
- Some code pairs are not allowed together: (1,1), (1,4), (2,2), (2,4), (3,3), (4,1), (4,2), (4,4), (5,5), (6,6),
  listed as (fps, NGSA). If both airframers choose such a pair, the later airframe moves to code 7.
- `launch_if_selected` (P&W GTF2, RR UltraFan NB): the engine launches this round only if a live airframe that is
  not yet in service has selected you this round, and your engine would be ready by its EIS. Otherwise nothing
  happens and nothing is spent.
- **Joint Venture.** P&W (`jv_with_rr: commit`) and RR (`jv_with_pw: commit`) each make a public, standing
  commitment. The Joint Venture forms in the first round in which both are committed. Its engine is ready 6 years
  later, or earlier if a partner folds in a solo programme that is further along. A solo programme folds into the
  Joint Venture when it forms. A commitment can be withdrawn before the Joint Venture forms.
- Before a new airframe enters service, the 737 flies CFM (LEAP-1B) and the A320neo flies P&W and CFM.

## How the board sets market shares

**Narrowbody airframes.**
- Nothing changes until a new airframe enters service.
- If NGSA enters service first, Airbus gains 3 pp a year (cap 80%).
- If fps enters service first, Boeing gains {p['v_ramp7_b_pp']:.1f} pp a year (cap 80%).
- When the second airframe enters service, its maker climbs toward 50% at {p['v_ramp10_b_pp']:.1f} pp a year if it is below
  50%; otherwise shares stay where they are.
- If both enter service in the same year, Boeing climbs from 40% toward 50%.
- **fps 7-year ramp-up:** Boeing gets +{p['v_fps_7yr_advantage']:.0f} pp for 10 years from fps EIS.
- **737 rate increase:** Boeing gets +5 pp in 2032-36, or every year if neither new airframe is ever launched.
- **Delay Tactics:** Boeing loses {p['v_sabotage_share']:.0f} pp for 5 years from fps EIS.

**Widebody airframes.**
- A lone re-engined 787 gains {p['v_wb_b_capture_pp']:.1f} pp a year from its EIS (cap 85%).
- A lone re-engined A350 gains {p['v_wb_a_capture_pp']:.1f} pp a year (cap 60%).
- If both re-engine, the first one's gains stop when the second enters service. If both enter service in the same
  year, nothing changes.

**Engines.**
- Nothing changes until the first new narrowbody enters service; on the widebody, until the first re-engine (or 2035).
- From then on, each airframer's share of the NB market is split equally among the makers fitted to its airframe (the
  737 and A320neo slots as above). The engine moves then shift share:

| Engine move | Effect on engine share |
|---|---|
| CFM ducted | CFM +10 pp NB, taken from P&W (or half each from P&W and RR, if RR has an NB engine) |
| CFM Open Fan | Airframers will not wait for it. If the first new narrowbody enters service before Open Fan is ready, CFM loses 35 pp of NB share to the others (20 pp if CFM lobbies on emissions) |
| Partner Embraer | CFM +5 pp NB |
| GEnx upgrade or investment | CFM +5 pp WB |
| GTF2 Solo | P&W +10 pp NB (5 pp each from CFM and RR) |
| Joint Venture | P&W +5 pp and RR +5 pp NB, CFM −10 pp; P&W and RR then hold equal NB shares |
| UltraFan NB Solo | RR +15 pp NB (CFM −10 pp, P&W −5 pp) |
| UltraFan WB | RR +10 pp WB from CFM |
| Trent 1000 upgrade | RR +5 pp WB from CFM |

Shares are floored at zero and re-normalised to 100%.

**Payoffs.**
- Each player's score is the change in its present value (PV, $B at 2026) against the status quo, and its yield:
  100 + ΔPV ÷ enterprise value × 100.
- Airframers: operating profit on NB and WB aircraft, less programme investment (booked at EIS), a debt penalty,
  two-front strain, rate-increase cost, Delay Tactics spend and fines.
- Engine makers: lifetime value of engines delivered (engine price × a 1.6 lifecycle multiplier, with 2.2% a year
  price inflation), less R&D, strain and write-offs.
- Your own numbers are in your private brief.

## What is public

**Public:**
- launches, cancellations, entry-into-service and engine-ready dates;
- engine selections and the engines actually fitted;
- Joint Venture commitments;
- each player's `public_statement`, and any `other_moves` marked public;
- observed market shares and deliveries, year by year, up to the decision year.

**Private:** everything else: your payoffs, finances, orders not yet public, your rationale and your predictions.

**Delay Tactics** are covert: never published, and revealed only when the game ends.
- Each move (supply-chain bottleneck, talent poaching) costs $1B, spent over the years before fps EIS.
- One or both moves give the same {p['v_sabotage_share']:.0f} pp effect, from fps EIS.
- If Boeing never launches fps, the tactics are "naked" and draw a $48.32B fine.
- They can be ordered in any round before fps enters service.
"""


# ─────────────────────────────── public record ───────────────────────────────
def programme_rows(state, year):
    """Every public programme record (live, cancelled, folded), as rows for the public table."""
    rows = []
    for key, r in state["prog"].items():
        base = key
        status = None
        if key.startswith("_cancelled_"):
            base = key[len("_cancelled_"):].rsplit("_", 1)[0]
            status = "cancelled %d" % r["cancel"]
        elif key.startswith("_folded_"):
            base = key[len("_folded_"):]
            status = "folded into the Joint Venture %d" % r["cancel"]
        due = r.get("eis", r.get("ready"))
        if status is None:
            status = ("in service since %d" % due) if due <= year else ("in development; %s %d" % (
                "EIS" if "eis" in r else "ready", due))
        name = PROG_LABEL.get(base, base)
        if base == "fps":
            name += " — " + {"7yr": "7-year ramp-up", "10yr": "10-year ramp-up", "embraer": "via Embraer"}[r["variant"]]
        if base == "cfm_genx":
            name += " — " + {"genx9": "upgrade", "genx_invest": "investment"}[r["kind"]]
        rows.append({"key": base, "name": name, "launch": r["launch"], "due": due,
                     "due_kind": "EIS" if "eis" in r else "ready", "status": status})
    rows.sort(key=lambda x: (x["launch"], x["name"]))
    if state["rate737"]:
        rows.append({"key": "rate737", "name": "737 production-rate increase (Boeing)", "launch": state["rate737"]["launch"],
                     "due": 2032, "due_kind": "rate up", "status": "rate up from 2032"})
    return rows


def observed(state, year):
    """Market history up to the year before the decision year (public)."""
    v = M.value(state, covert=True, series=True)
    af = {r["year"]: r for r in v["_af_series"]["years"]}
    en = {r["year"]: r for r in v["_en_series"]["years"]}
    out = []
    for y in range(2026, year):
        a, e = af[y], en[y]
        out.append({"year": y, "nb_boeing": a["boeing"]["nb_share"], "nb_airbus": a["airbus"]["nb_share"],
                    "wb_boeing": a["boeing"]["wb_share"], "wb_airbus": a["airbus"]["wb_share"],
                    "nb_units_boeing": a["boeing"]["nb_units"], "nb_units_airbus": a["airbus"]["nb_units"],
                    "wb_units_boeing": a["boeing"]["wb_units"], "wb_units_airbus": a["airbus"]["wb_units"],
                    "eng_nb": (e["cfm"]["nb_share"], e["pratt_whitney"]["nb_share"], e["rolls_royce"]["nb_share"]),
                    "eng_wb": (e["cfm"]["wb_share"], e["pratt_whitney"]["wb_share"], e["rolls_royce"]["wb_share"])})
    return out


def bulletin(state, year, round_no, statements=None, public_other=None, notes=None):
    """Public bulletin at the start of a round (identical for all players)."""
    L = ["# Public bulletin — round %d, decision year %d" % (round_no, year), ""]
    L.append("Published by the game master to all five players. Everything here is public.")
    L.append("")
    if notes:
        L += ["## Game-master notes", ""] + ["- " + n for n in notes] + [""]
    L += ["## Programmes on the public record", ""]
    rows = programme_rows(state, year)
    if rows:
        L += ["| Programme | Launched | Due | Status |", "|---|---:|---:|---|"]
        for r in rows:
            L.append("| %s | %d | %s %d | %s |" % (r["name"], r["launch"], r["due_kind"], r["due"], r["status"]))
    else:
        L.append("No programme has been launched. Everyone is on today's products (737 MAX, 787, A320neo, A350; "
                 "LEAP, GTF, GEnx, Trent).")
    L.append("")
    fit = R.engine_fit(state)
    if fit:
        L += ["## Engines on the new narrowbodies", "", "| Airframe | Engine selection | Fitted if nothing changes | Note |",
              "|---|---|---|---|"]
        for k, f in fit.items():
            L.append("| %s | %s | %s | %s |" % ("fps" if k == "fps" else "NGSA", f["requested"], f["fitted_if_no_change"],
                                             f["note"] or "—"))
        L.append("")
    jc = state["jv_commit"]
    if M.live(state, "jv"):
        j = M.live(state, "jv")
        L += ["**Joint Venture (P&W and Rolls-Royce):** formed %d; engine ready %d." % (j["launch"], j["ready"]), ""]
    elif jc["pratt_whitney"] or jc["rolls_royce"]:
        who = [M.NAMES[s] + " (since %d)" % jc[s] for s in ("pratt_whitney", "rolls_royce") if jc[s]]
        L += ["**Joint Venture commitments standing:** " + ", ".join(who) + ". The Joint Venture forms when both "
              "are committed.", ""]
    if statements and any(statements.values()):
        L += ["## Public statements (last round)", ""]
        for s in M.SIDES:
            if statements.get(s):
                L.append("- **%s:** %s" % (M.NAMES[s], statements[s]))
        L.append("")
    if public_other:
        L += ["## Other moves made public", ""]
        for s, items in public_other.items():
            for it in items:
                L.append("- **%s:** %s%s" % (M.NAMES[s], it.get("move", ""), (" — " + it["detail"]) if it.get("detail") else ""))
        L.append("")
    obs = observed(state, year)
    L += ["## Observed market, %d-%d" % (2026, year - 1), "",
          "Shares of deliveries. Engine shares are of all engines delivered on narrowbody and widebody aircraft.", "",
          "| Year | NB Boeing | NB Airbus | WB Boeing | WB Airbus | NB engines CFM / P&W / RR | WB engines CFM / P&W / RR |",
          "|---:|---:|---:|---:|---:|---|---|"]
    for o in obs:
        L.append("| %d | %s | %s | %s | %s | %s | %s |" % (
            o["year"], pct(o["nb_boeing"]), pct(o["nb_airbus"]), pct(o["wb_boeing"]), pct(o["wb_airbus"]),
            " / ".join(pct(x) for x in o["eng_nb"]), " / ".join(pct(x) for x in o["eng_wb"])))
    L.append("")
    return "\n".join(L)


# ─────────────────────────────── objectives ───────────────────────────────
OBJECTIVES = {
    "boeing": "Hold the 50/50 NB split; defend incumbency",
    "airbus": "Defend the 60/40 edge; protect the A320 family",
    "cfm": "Dominate narrowbody engines; introduce the Open Fan",
    "pratt_whitney": "Restore credibility; capitalise on the GTF investment",
    "rolls_royce": "Enter the narrowbody market; keep widebody dominance",
}


def objective_status(side, state, v):
    af = {r["year"]: r for r in v["_af_series"]["years"]}
    en = {r["year"]: r for r in v["_en_series"]["years"]}
    out = []
    if side == "boeing":
        sh = {y: af[y]["boeing"]["nb_share"] for y in (2030, 2035, 2040, 2045, 2050)}
        w = min(sh[y] for y in (2040, 2045, 2050))
        out.append(("Hold the 50/50 NB split: Boeing NB share ≥ 50% in 2040, 2045, 2050",
                    w >= 0.5 - 1e-9, "worst year %s (%s)" % (pct(w), ", ".join("%d %s" % (y, pct(sh[y])) for y in (2040, 2045, 2050)))))
        w2 = min(sh.values())
        out.append(("Defend incumbency: Boeing NB share ≥ 40% (status quo) in 2030-2050", w2 >= 0.4 - 1e-9,
                    "worst year %s" % pct(w2)))
    elif side == "airbus":
        sh = {y: af[y]["airbus"]["nb_share"] for y in (2030, 2035, 2040, 2045, 2050)}
        w = min(sh[y] for y in (2040, 2045, 2050))
        out.append(("Defend the 60/40 edge: Airbus NB share ≥ 60% in 2040, 2045, 2050", w >= 0.6 - 1e-9,
                    "worst year %s (%s)" % (pct(w), ", ".join("%d %s" % (y, pct(sh[y])) for y in (2040, 2045, 2050)))))
        ngsa = M.live(state, "ngsa")
        yrs = [y for y in sh if not ngsa or y < ngsa["eis"]]
        w2 = min(sh[y] for y in yrs) if yrs else 0.6
        out.append(("Protect the A320 family: ≥ 60% in every listed year before NGSA enters service", w2 >= 0.6 - 1e-9,
                    "worst counted year %s" % pct(w2)))
    elif side == "cfm":
        sh = {y: en[y]["cfm"]["nb_share"] for y in (2040, 2045, 2050)}
        w = min(sh.values())
        out.append(("Dominate NB engines: CFM NB engine share ≥ 50% in 2040, 2045, 2050", w >= 0.5 - 1e-9,
                    "worst year %s" % pct(w)))
        of = M.live(state, "cfm_open_fan")
        out.append(("Introduce the Open Fan: launched and ready by 2050", bool(of and of["ready"] <= 2050),
                    ("Open Fan ready %d" % of["ready"]) if of else "not launched"))
    elif side == "pratt_whitney":
        fitted = [k for k in ("fps", "ngsa") if M.live(state, k) and "PW" in M.effective_code(state, k)[0]
                  and M.live(state, k)["eis"] <= 2050]
        out.append(("Restore credibility: a new P&W engine (GTF2 or Joint Venture) in service on a new airframe by 2050",
                    bool(fitted), ("on " + ", ".join("fps" if k == "fps" else "NGSA" for k in fitted)) if fitted else "none"))
        out.append(("Capitalise on the GTF: ΔPV ≥ 0", v["pratt_whitney"]["pv_delta"] >= 0, money(v["pratt_whitney"]["pv_delta"]) + " $B"))
    elif side == "rolls_royce":
        sh = {y: en[y]["rolls_royce"]["nb_share"] for y in (2045, 2050)}
        out.append(("Enter the NB market: RR NB engine share > 0 in 2045 and 2050", min(sh.values()) > 1e-9,
                    ", ".join("%d %s" % (y, pct(sh[y])) for y in sh)))
        wb = {y: en[y]["rolls_royce"]["wb_share"] for y in (2040, 2045, 2050)}
        out.append(("Keep WB dominance: RR WB engine share ≥ 50% in 2040, 2045, 2050", min(wb.values()) >= 0.5 - 1e-9,
                    "worst year %s" % pct(min(wb.values()))))
    return out


# ─────────────────────────────── own options and rival scenarios ───────────────────────────────
def own_options(state, side, year):
    """(label, orders) for each distinct own plan this round. Engine codes are not varied here (they do not change
    an airframer's own payoff on the board)."""
    L = R.legal_options(state, side, year)
    out = []
    if side == "boeing":
        code = state["codes"].get("fps") or 7
        for f, r, w in itertools.product(L["fps"], L["rate_737"], L["re787"]):
            o = {"fps": f, "rate_737": r, "re787": w, "fps_engine_code": code if f.startswith("launch") else None}
            lab = [{"hold": "fps: hold", "launch_7yr": "fps 7-yr", "launch_10yr": "fps 10-yr",
                    "launch_via_embraer": "fps via Embraer", "cancel": "cancel fps"}[f]]
            if r == "increase": lab.append("737 rate up")
            lab.append({"hold": "787: hold", "launch": "787 Re-engine", "cancel": "cancel 787 Re-engine"}[w])
            out.append((" + ".join(lab), o))
    elif side == "airbus":
        code = state["codes"].get("ngsa") or 7
        dts = [d for d in L["delay_tactics"] if d != "poaching"]   # bottleneck and poaching are the same on the board
        for n, a, d in itertools.product(L["ngsa"], L["rea350"], dts):
            o = {"ngsa": n, "rea350": a, "delay_tactics": d, "ngsa_engine_code": code if n == "launch" else None}
            lab = [{"hold": "NGSA: hold", "launch": "NGSA", "cancel": "cancel NGSA"}[n],
                   {"hold": "A350: hold", "launch": "A350 Re-engine", "cancel": "cancel A350 Re-engine"}[a]]
            if d != "none":
                lab.append({"bottleneck": "Delay Tactics (one move)", "both": "Delay Tactics (both moves)"}[d])
            out.append((" + ".join(lab), o))
    elif side == "cfm":
        for du, of, em, lo, gx in itertools.product(L["ducted"], L["open_fan"], L["partner_embraer"], L["lobby_emissions"],
                                                    [g for g in L["genx"] if g != "invest_genx"]):
            has_new = (du == "launch" or (M.live(state, "cfm_ducted") and du != "cancel")) or \
                (of == "launch" or (M.live(state, "cfm_open_fan") and of != "cancel"))
            if em == "launch" and not has_new:
                continue
            has_of = of == "launch" or (M.live(state, "cfm_open_fan") and of != "cancel")
            if lo == "launch" and not has_of:
                continue
            o = {"ducted": du, "open_fan": of, "partner_embraer": em, "lobby_emissions": lo, "genx": gx}
            lab = []
            for k, v in o.items():
                if v != "hold":
                    lab.append({"ducted": "Ducted", "open_fan": "Open Fan", "partner_embraer": "Partner Embraer",
                                "lobby_emissions": "Lobby", "genx": "GEnx upgrade"}[k] + ("" if v in ("launch", "upgrade_genx9") else " (" + v + ")"))
            out.append((" + ".join(lab) or "hold everything", o))
    elif side == "pratt_whitney":
        for g, j in itertools.product(L["gtf2_solo"], L["jv_with_rr"]):
            o = {"gtf2_solo": g, "jv_with_rr": j}
            lab = [{"hold": "GTF2: hold", "launch": "GTF2 Solo", "launch_if_selected": "GTF2 Solo if selected",
                    "cancel": "cancel GTF2"}[g]]
            if j != "hold": lab.append({"commit": "commit to JV", "withdraw": "withdraw JV commitment"}[j])
            out.append((" + ".join(lab), o))
    elif side == "rolls_royce":
        wbs = []
        for u in L["ultrafan_wb"]:
            for t in L["t1000_upgrade"]:
                if u == "launch" and t == "launch":
                    continue
                wbs.append((u, t))
        for s_, j, (u, t) in itertools.product(L["ultrafan_nb_solo"], L["jv_with_pw"], wbs):
            o = {"ultrafan_nb_solo": s_, "jv_with_pw": j, "ultrafan_wb": u, "t1000_upgrade": t}
            lab = [{"hold": "UltraFan NB: hold", "launch": "UltraFan NB Solo", "launch_if_selected": "UltraFan NB if selected",
                    "cancel": "cancel UltraFan NB"}[s_]]
            if j != "hold": lab.append({"commit": "commit to JV", "withdraw": "withdraw JV commitment"}[j])
            if u != "hold": lab.append({"launch": "UltraFan WB", "cancel": "cancel UltraFan WB"}[u])
            if t != "hold": lab.append({"launch": "T1000 upgrade", "cancel": "cancel T1000 upgrade"}[t])
            out.append((" + ".join(lab), o))
    return out


def _nb_launch(state, side_key):
    return M.live(state, side_key) is None


def rival_scenarios(state, side, year):
    """(label, orders of the other sides) — a handful of public-information scenarios for this round's rival moves.
    Covert moves appear only as an explicit risk case."""
    sc = [("Rivals hold", {})]
    fps_free, ngsa_free = _nb_launch(state, "fps"), _nb_launch(state, "ngsa")
    fps_dev = M.live(state, "fps") and M.live(state, "fps")["eis"] > year
    if side == "boeing":
        if ngsa_free:
            sc.append(("Airbus launches NGSA", {"airbus": {"ngsa": "launch", "ngsa_engine_code": 6}}))
        if M.live(state, "rea350") is None:
            sc.append(("Airbus launches A350 Re-engine", {"airbus": {"rea350": "launch"}}))
            if ngsa_free:
                sc.append(("Airbus launches NGSA + A350 Re-engine", {"airbus": {"ngsa": "launch", "ngsa_engine_code": 6, "rea350": "launch"}}))
        if fps_free or fps_dev:
            base = {"ngsa": "launch", "ngsa_engine_code": 6} if ngsa_free else {}
            sc.append(("Risk case: %sAirbus Delay Tactics (covert)" % ("NGSA + " if ngsa_free else ""),
                       {"airbus": dict(base, delay_tactics="bottleneck")}))
    elif side == "airbus":
        if fps_free:
            sc.append(("Boeing launches fps 10-yr", {"boeing": {"fps": "launch_10yr", "fps_engine_code": 7}}))
            sc.append(("Boeing launches fps 7-yr", {"boeing": {"fps": "launch_7yr", "fps_engine_code": 7}}))
            sc.append(("Boeing launches fps via Embraer", {"boeing": {"fps": "launch_via_embraer", "fps_engine_code": 7}}))
        if M.live(state, "re787") is None:
            sc.append(("Boeing launches 787 Re-engine", {"boeing": {"re787": "launch"}}))
            if fps_free:
                sc.append(("Boeing launches fps 10-yr + 787 Re-engine", {"boeing": {"fps": "launch_10yr", "fps_engine_code": 7, "re787": "launch"}}))
    else:
        mk = {"cfm": "CFM", "pratt_whitney": "PW", "rolls_royce": "RR"}[side]
        # codes that include / exclude this maker, and the rival makers' conditional launches that go with them
        inc = {"CFM": (6, 7), "PW": (6, 7), "RR": (7, 5)}[mk]
        exc = {"CFM": (2, 1), "PW": (5, 3), "RR": (6, 3)}[mk]
        follow = {"pratt_whitney": {"gtf2_solo": "launch_if_selected"}, "rolls_royce": {"ultrafan_nb_solo": "launch_if_selected"}}
        rivals = {k: v for k, v in follow.items() if k != side}
        if ngsa_free:
            sc.append(("Airbus launches NGSA, selects you (code %d)" % inc[0],
                       dict({"airbus": {"ngsa": "launch", "ngsa_engine_code": inc[0]}}, **rivals)))
            sc.append(("Airbus launches NGSA, does not select you (code %d)" % exc[0],
                       dict({"airbus": {"ngsa": "launch", "ngsa_engine_code": exc[0]}}, **rivals)))
        elif M.live(state, "ngsa")["eis"] > year:
            cur = state["codes"].get("ngsa", 7)
            alt = exc[0] if mk in M.CODE_SETS[cur][0] else inc[0]
            sc.append(("Airbus switches NGSA engines to code %d (%s)" % (alt, M.CODE_LABEL[alt]),
                       dict({"airbus": {"ngsa_engine_code": alt}}, **rivals)))
        if fps_free:
            sc.append(("Boeing launches fps 10-yr, selects you (code %d)" % inc[1],
                       dict({"boeing": {"fps": "launch_10yr", "fps_engine_code": inc[1]}}, **rivals)))
            if ngsa_free:
                sc.append(("Both launch; you are selected on both (codes %d, %d)" % (inc[1], inc[0]),
                           dict({"boeing": {"fps": "launch_10yr", "fps_engine_code": inc[1]},
                                 "airbus": {"ngsa": "launch", "ngsa_engine_code": inc[0]}}, **rivals)))
                sc.append(("Both launch; you are on neither (codes %d, %d)" % (exc[1], exc[0]),
                           dict({"boeing": {"fps": "launch_10yr", "fps_engine_code": exc[1]},
                                 "airbus": {"ngsa": "launch", "ngsa_engine_code": exc[0]}}, **rivals)))
        elif fps_dev:
            cur = state["codes"].get("fps", 7)
            alt = exc[1] if mk in M.CODE_SETS[cur][0] else inc[1]
            sc.append(("Boeing switches fps engines to code %d (%s)" % (alt, M.CODE_LABEL[alt]),
                       dict({"boeing": {"fps_engine_code": alt}}, **rivals)))
        if side in ("pratt_whitney", "rolls_royce") and not M.live(state, "jv"):
            other = "rolls_royce" if side == "pratt_whitney" else "pratt_whitney"
            fld = "jv_with_pw" if other == "rolls_royce" else "jv_with_rr"
            if not state["jv_commit"][other]:
                sc.append(("%s commits to the Joint Venture" % M.NAMES[other], {other: {fld: "commit"}}))
        if side == "rolls_royce" and M.live(state, "re787") is None and M.live(state, "rea350") is None:
            sc.append(("Boeing launches 787 Re-engine and Airbus A350 Re-engine",
                       {"boeing": {"re787": "launch"}, "airbus": {"rea350": "launch"}}))
    return sc


def payoff_grid(state, side, year):
    """Own ΔPV and yield for every own plan × rival scenario, assuming no moves after this round."""
    opts = own_options(state, side, year)
    scen = rival_scenarios(state, side, year)
    covert = (side == "airbus")
    grid = []
    for olab, o in opts:
        row = []
        for slab, so in scen:
            orders = {k: dict(v) for k, v in so.items()}
            orders[side] = dict(orders.get(side, {}), **o)
            s1, _ = R.adjudicate(state, year, orders)
            # the risk case is the only one that values Airbus's covert move for another player
            v = M.value(s1, covert=(covert or slab.startswith("Risk case")), series=True)
            row.append((v[side]["pv_delta"], v[side]["yield"]))
        grid.append((olab, o, row))
    return grid, scen


# ─────────────────────────────── private brief ───────────────────────────────
OWN_KEYS = {"boeing": ("fps", "re787", "rate737"), "airbus": ("ngsa", "rea350"),
            "cfm": ("cfm_ducted", "cfm_open_fan", "cfm_embraer", "cfm_lobby", "cfm_genx"),
            "pratt_whitney": ("pw_solo", "jv"), "rolls_royce": ("rr_solo", "jv", "rr_uf_wb", "rr_t1000")}
BRIDGE_LABEL = {"nb_profit_vs_sq": "Narrowbody operating profit vs status quo", "wb_profit_vs_sq": "Widebody operating profit vs status quo",
                "programme_investment": "Programme investment (booked at EIS)", "rate_hike": "737 rate increase",
                "delay_tactics_spend": "Delay Tactics spend", "write_offs": "Cancellation write-offs",
                "debt_penalty": "Debt penalty (α)", "two_front_strain": "Two-front strain", "naked_fine": "Naked Delay Tactics fine",
                "engine_value_vs_sq": "Engine value vs status quo", "r_and_d": "R&D (undiscounted, as the board)",
                "strain": "Strain (concurrent programmes)"}


def projection_rows(side, v):
    rows = []
    if side in ("boeing", "airbus"):
        nr = v["_af_series"]["nonrecurring"][side]
        for r in v["_af_series"]["years"]:
            x = r[side]
            y = r["year"]
            if y > M.REPORT_END:
                continue
            rows.append([y, pct(x["nb_share"]), pct(x["wb_share"]), "%d" % round(x["nb_units"]), "%d" % round(x["wb_units"]),
                         f1(x["nb_revenue"] + x["wb_revenue"]), f1(x["nb_profit"] + x["wb_profit"]),
                         f1(x["sq_nb_profit"] + x["sq_wb_profit"]), f1(sum(nr.get(y, {}).values())) if nr.get(y) else "—"])
        head = ["Year", "NB share", "WB share", "NB deliveries", "WB deliveries", "Revenue $B", "Operating profit $B",
                "Status-quo profit $B", "Non-recurring $B"]
    else:
        nr = v["_en_series"]["nonrecurring"][side]
        for r in v["_en_series"]["years"]:
            x = r[side]
            y = r["year"]
            if y > M.REPORT_END:
                continue
            rows.append([y, pct(x["nb_share"]), pct(x["wb_share"]), "%d" % round(x["nb_units"]), "%d" % round(x["wb_units"]),
                         f1(x["nb_value"] + x["wb_value"]), f1(x["sq_nb_value"] + x["sq_wb_value"]),
                         f1(sum(nr.get(y, {}).values())) if nr.get(y) else "—"])
        head = ["Year", "NB engine share", "WB engine share", "NB engines", "WB engines", "Engine lifecycle value $B",
                "Status-quo value $B", "R&D and write-offs $B"]
    return head, rows


def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---:" if i else "---" for i in range(len(head))) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return out


def private_brief(state, side, year, round_no, last_orders=None, gm_notes=None):
    name = M.NAMES[side]
    v = M.value(state, covert=(side == "airbus"), series=True)
    me = v[side]
    L = ["# %s — private brief, round %d (decision year %d)" % (name, round_no, year), "",
         "From the game master, for %s only. It holds the public record (in the bulletin) and your own position. "
         "No other player's payoff, finances, orders or reasoning is in it." % name, ""]
    if gm_notes:
        L += ["## Game-master notes to you", ""] + ["- " + n for n in gm_notes] + [""]
    L += ["## 1. Your position now", ""]
    rows = [r for r in programme_rows(state, year) if r["key"] in OWN_KEYS[side]]
    if rows:
        L += table(["Your programme", "Launched", "Due", "Status"],
                   [[r["name"], r["launch"], "%s %d" % (r["due_kind"], r["due"]), r["status"]] for r in rows])
    else:
        L.append("You have launched nothing. You are on today's products.")
    if side == "airbus" and (state["dt"]["bottleneck"] or state["dt"]["poaching"]):
        L.append("")
        L.append("Covert (known only to you and the game master): Delay Tactics ordered — " + ", ".join(
            "%s %d" % (k, y) for k, y in state["dt"].items() if y) + ".")
    if side in ("boeing", "airbus"):
        key = "fps" if side == "boeing" else "ngsa"
        f = R.engine_fit(state).get(key)
        if f:
            L += ["", "Engines on your %s: you selected %s; fitted if nothing changes: %s%s." % (
                "fps" if key == "fps" else "NGSA", f["requested"], f["fitted_if_no_change"], ("; " + f["note"]) if f["note"] else "")]
    L += ["", "**If nobody moves again** (the board's valuation of today's state%s):" % (
        "; your covert moves included" if side == "airbus" else ""), "",
          "- ΔPV against the status quo: **%s $B** (PV at 2026, your WACC %.1f%%). Yield **%.2f%%** (enterprise value $%.0fB)." % (
              money(me["pv_delta"]), 100 * me["wacc"], me["yield"], me["ev"]), ""]
    L += table(["Component", "$B (PV at 2026)"], [[BRIDGE_LABEL[k], money(x)] for k, x in me["bridge"].items() if abs(x) > 1e-12])
    L += ["", "Year by year (nominal $B; shares of the market's deliveries):", ""]
    head, prow = projection_rows(side, v)
    L += table(head, prow)
    if side in ("boeing", "airbus"):
        L += ["", "The board counts each programme's market for 20 years from its EIS (unlaunched programmes use the "
              "snapshot dates fps 2041, NGSA 2037, Re-engines 2035), so years after that window add nothing to ΔPV."]
    else:
        t = v["_engine_timing"]
        L += ["", "The board counts the narrowbody engine market to %d and the widebody to %d." % (
            t["nb_window_end"], t["wb_window_end"])]
    L += ["", "## 2. Your objective", "", "Briefing goal: **%s**." % OBJECTIVES[side], ""]
    for lab, ok, det in objective_status(side, state, v):
        L.append("- %s — **%s** (%s)" % (lab, "met" if ok else "not met", det))
    L += ["", "## 3. Your options this round", ""]
    legal = R.legal_options(state, side, year)
    for k, opts in legal.items():
        L.append("- `%s`: %s" % (k, ", ".join("`%s`" % o for o in opts)))
    grid, scen = payoff_grid(state, side, year)
    L += ["", "**Your payoff grid.** Your ΔPV in $B (yield in brackets) for each plan (rows) against what the others "
          "might do this round (columns), assuming nobody moves after this round. %s" % (
              "Engine codes do not change your own payoff on the board." if side in ("boeing", "airbus") else
              "Your payoff depends heavily on which engines the airframers select."), ""]
    head = ["Your plan"] + ["S%d" % (i + 1) for i in range(len(scen))]
    rows = []
    for olab, o, row in grid:
        rows.append([olab] + ["%s (%.1f%%)" % (money(a), b) for a, b in row])
    L += table(head, rows)
    L += [""] + ["- **S%d:** %s" % (i + 1, s[0]) for i, s in enumerate(scen)]
    best = []
    for j, (slab, _) in enumerate(scen):
        i = max(range(len(grid)), key=lambda i: grid[i][2][j][0])
        best.append("- Best plan against S%d: %s (%s)" % (j + 1, grid[i][0], money(grid[i][2][j][0])))
    L += [""] + best
    L += ["", "## 4. What to return", "",
          "Return your sealed orders as the JSON object your task specifies: one value for each order field above, "
          "plus `other_moves`, `public_statement`, `rationale` (with your ExCo deliberation), `predictions` and "
          "`expected_pv_b`. Fields you leave out are read as `hold`."]
    return "\n".join(L), grid, scen
