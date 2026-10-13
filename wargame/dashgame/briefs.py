"""Game-master briefs for dash-2050: the public rules, the public bulletin, and each player's private brief.

A player's brief holds only (1) public information, identical for everyone, and (2) that player's own position,
projection and payoff grid. No rival's payoff, finances, rationale or covert move is ever written into a brief.
"""
import itertools
import json
import os

import model as M
import rules as R

YEARS_PUBLIC = list(range(2026, 2061))
FIELD_LABEL = {
    "fps": "fps", "fps_engine_code": "fps engine code", "rate_737": "737 rate", "re787": "787 Re-engine",
    "ngsa": "NGSA", "ngsa_engine_code": "NGSA engine code", "rea350": "A350 Re-engine", "delay_tactics": "Delay Tactics",
    "ducted": "Ducted", "open_fan": "Open Fan", "partner_embraer": "Partner Embraer", "lobby_emissions": "Lobby",
    "genx": "GEnx", "gtf2_solo": "GTF2 Solo", "jv_with_rr": "JV with RR", "ultrafan_nb_solo": "UltraFan NB Solo",
    "jv_with_pw": "JV with PW", "ultrafan_wb": "UltraFan WB", "t1000_upgrade": "T1000 upgrade",
    "fps_site": "fps site", "a320_plan": "A320 plan"}
PROG_LABEL = M.PROG_LABEL


def f1(x):
    return "%.1f" % x


def money(x):
    return ("+" if x >= 0 else "−") + "%.2f" % abs(x)


def pct(x):
    return "%.1f%%" % (100 * x)


def nb_rules(p):
    """The narrowbody share rule of the board in use, in plain words (public)."""
    if M.H.VERSION == "v2":
        return (f"- Nothing changes until a new airframe enters service.\n"
                f"- If NGSA enters service first, Airbus gains 3 pp a year (cap 80%).\n"
                f"- If fps enters service first, Boeing gains {p['v_ramp7_b_pp']:.1f} pp a year (cap 80%).\n"
                f"- When the second airframe enters service, its maker climbs toward 50% at {p['v_ramp10_b_pp']:.1f} pp a year if it is below\n"
                f"  50%; otherwise shares stay where they are.\n"
                f"- If both enter service in the same year, Boeing climbs from 40% toward 50%.\n"
                f"- **fps 7-year ramp-up:** Boeing gets +{p['v_fps_7yr_advantage']:.0f} pp for 10 years from fps EIS.\n")
    bal = p["boeing_share_pct"]
    return (f"- Nothing changes until a new airframe enters service.\n"
            f"- **Only NGSA launched:** Airbus gains 3 pp a year from NGSA EIS (cap 80%).\n"
            f"- **Only fps launched:** Boeing gains {p['v_ramp10_b_pp']:.1f} pp a year from fps EIS (cap 80%).\n"
            f"- **Both launched, different EIS years:** the first one to enter service gains {p['v_eis_lead_pp']:.1f} pp a year while it\n"
            f"  is alone (cap 80%). From the second EIS, shares move toward a long-run split at {p['v_ramp10_b_pp']:.1f} pp a year\n"
            f"  (Boeing gaining) or {p['v_ramp10_a_pp']:.1f} pp a year (Airbus gaining). The long-run split is {bal}/{100 - bal} (Boeing/Airbus)\n"
            f"  shifted toward the first one by {p['v_eis_lead_pp']:.1f} pp for each year of lead (leader cap 80%), and the leader keeps\n"
            f"  that edge for good. Example: NGSA 2037 and fps 2041 give a long-run split of {bal - 4 * p['v_eis_lead_pp']:.0f}/{100 - bal + 4 * p['v_eis_lead_pp']:.0f}.\n"
            f"- **Both launched, same EIS year:** Boeing climbs from 40% toward {bal}% at {p['v_ramp10_b_pp']:.1f} pp a year; no lead edge.\n"
            f"- The three fps moves (7-year, 10-year, via Embraer) follow the same rule: only the two EIS years matter.\n")


def public_rules():
    """The rules every player sees (identical text). Rival costs, margins and balance sheets are not in it."""
    P = M.engine_params()
    p = M.af_params()
    wb_default = min(M.DEFAULT_EIS["re787"], M.DEFAULT_EIS["rea350"])
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
""" + ("""- **Supply and demand is on in this game:** the narrowbody market is limited by what the factories can build; see the
  last section.
""" if M.SD_ON else "") + f"""
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
  Joint Venture when it forms; what the maker has spent on it beyond its Joint Venture share is written off in the
  fold year. A commitment can be withdrawn before the Joint Venture forms.
- Before a new airframe enters service, the 737 flies CFM (LEAP-1B) and the A320neo flies P&W and CFM.

## How the board sets market shares

**Narrowbody airframes.**
{nb_rules(p)}- **737 rate increase:** Boeing gets +5 pp in 2032-36, or every year if neither new airframe is ever launched.
- **Delay Tactics:** Boeing loses {p['v_sabotage_share']:.0f} pp for 5 years from fps EIS.

**Widebody airframes.**
- A lone re-engined 787 gains {p['v_wb_b_capture_pp']:.1f} pp a year from its EIS (cap 85%).
- A lone re-engined A350 gains {p['v_wb_a_capture_pp']:.1f} pp a year (cap 60%).
- If both re-engine, the first one's gains stop when the second enters service. If both enter service in the same
  year, nothing changes.

**Engines.**
- Nothing changes until the first new narrowbody enters service; on the widebody, until the first re-engine (or {wb_default}).
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
""" + (sd_rules() if M.SD_ON else "")


def sd_rules():
    """Public rules of the supply-and-demand layer (supply_demand.py)."""
    import supply_demand as SD
    I = SD.inputs()
    b, d = I["boeing"], I["demand"]
    dem = lambda y: "%d" % round(SD.demand(y))
    rep = lambda y: "%d" % round(SD.demand(y) - SD.growth(y))
    gro = lambda y: "%d" % round(SD.growth(y))
    fb = SD.firm_backlog()
    return f"""
## Supply and demand

The board's shares are what customers **want**. Aircraft are delivered only if a factory can build them.

**Demand = replacement + growth.**
- **Replacement:** the retirement of today's 737 MAX, A320neo-family and A220 fleets (Cirium fleet data, October
  2026): {rep(2035)} a year in 2035, {rep(2045)} in 2045, {rep(2050)} in 2050.
- **Growth:** the single-aisle fleet grows about {100 * d['fleet_growth_2025_44']:.1f}% a year to 2044 (Airbus and Boeing 2025 market
  forecasts), easing to {100 * d['fleet_growth_2060']:.0f}% by 2060: {gro(2030)} new aircraft a year for growth in 2030, {gro(2040)} in 2040,
  {gro(2050)} in 2050.
- **Firm backlog:** {fb[0]:,.0f} 737 MAX and {fb[1]:,.0f} A320neo-family aircraft on firm order (October 2026), broadly the
  replacement of the older 737NG and A320ceo fleets. They are delivered first and never switch maker or lapse.
- New demand (replacement + growth, 737/A320 class): {dem(2026)} (2026), {dem(2030)} (2030), {dem(2035)} (2035),
  {dem(2040)} (2040), {dem(2045)} (2045), {dem(2050)} (2050), {dem(2055)} (2055), {dem(2060)} (2060), on top of the firm backlog.

**Who customers want.** Each year's new demand is split by the board's share rules above: the **preference share**. The
fps, NGSA, the 737 rate increase's +5 pp and Delay Tactics all move preference; they move deliveries only where a
factory has the slots. The share objectives in your brief are measured on preference, as in earlier games.

**Factories (public production plans, aircraft a month).**
- **Airbus (Rev. B plan):** A320 family at 85 a month until NGSA enters service. Then, on the base plan, the A320
  lines wind down (72, 52, 42, then 14 a month, and none about five years after NGSA EIS) while NGSA ramps up
  (rate 50 about four years after EIS, 80 about six, 100 about eight). On the **Alt plan** (`a320_plan: alt`) the A320
  lines are kept longer (82, 62, 52, 42, then 14 a month, about eight years in all): about 1,500 more A320s for
  about ${a320_alt_cost():.2f}B. Without NGSA the A320 stays at 85 a month.
- **Boeing:** 737 MAX at {b['max_rate']['2026']}, {b['max_rate']['2027']}, {b['max_rate']['2028']:.0f} and {b['max_rate']['2029']} a month in 2026-2029, then {b['max_rate_after']:.0f} from 2030
  (Renton's three lines at {b['renton_rate']:.0f} plus the Everett North Line); the 737 rate increase adds {b['rate_increase_per_year']:.0f} aircraft a year from
  {b['rate_increase_from']} while the MAX is built. The fps ramps on the same shape as NGSA (rate 50 about four years after EIS, 100
  about eight). Boeing's single-aisle total is capped at {b['total_rate_cap']:.0f} a month: as the fps fills it, the MAX gives way,
  down to an Everett tail of {b['max_tail_rate']:.0f} a month. On the **new-site plan** (`fps_site: new_site`, the default) the fps is
  built at new sites and the MAX carries on at Renton and Everett. On the **Renton plan** (`fps_site: renton`) Renton is
  reassigned to the fps: its MAX lines (with the rate increase that rides on them) wind down as the fps ramps up, like
  the A320 base plan, and only the Everett North Line carries on (up to {b['everett_rate']:.0f} a month); Boeing avoids about
  ${b['renton_saving_b']:.1f}B of new-site capex, in full if Renton is chosen at least three years before the fps enters service
  (pro-rated if later). After {b['max_last_year']} the MAX builds only what the fps cannot yet: it tops Boeing up to the fps's full
  rate while the fps ramps. Without an fps the MAX carries on.

**Deliveries each year.**
- Each maker delivers its firm backlog first, then what its new customers want plus its waiting backlog, up to its
  capacity.
- Customers its factories cannot serve: the flexible ones ({100 * d['flex_share']:.0f}%: airlines flying both types, lessors and
  unannounced customers) take the other maker's free slots, this year or in any later year when slots open; the rest
  wait in the backlog for their first choice.
- A tenth of the waiting backlog (not the firm backlog) drops out each year (keeps old aircraft longer, defers growth
  or cancels).
- New types are delivered first, up to their line's capacity; the rest are 737 MAX or A320neo, at today's price and
  margin.
- Market share in the observed tables is the share of deliveries. Profit is earned on aircraft delivered, at the
  board's prices and margins for each type.
- The status quo runs the same rules with today's plans (A320 at 85 a month, the MAX path above), the same demand and
  firm backlog, and the 40/60 preference.
- Engine makers sell engines on the aircraft actually delivered (two per aircraft). The 737 MAX keeps CFM (LEAP-1B)
  and the A320neo keeps CFM 60% / P&W 40%; the engine moves in the table above shift share only on the new types (fps
  and NGSA), starting from the makers fitted to each.

**Your supply plan** (`fps_site` for Boeing, `a320_plan` for Airbus) is public. It applies to your new airframe once
launched (you can choose it in the launch round) and can change in any round until that airframe enters service. A
field you leave out keeps your current plan. Supply-plan costs and savings are valued at your cost of capital (no debt
penalty).
"""


def a320_alt_cost():
    import supply_demand as SD
    return SD.inputs()["airbus"]["alt_cost_b"]


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
            status = (("in service since %d" if "eis" in r else "ready since %d") % due) if due <= year else (
                "in development; %s %d" % ("EIS" if "eis" in r else "ready", due))
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
    if M.SD_ON:
        import supply_demand as SD
        a3, site = SD.plans(state)
        L += ["## Production plans (public)", "",
              "- **Airbus:** A320 %s plan (%s)." % (a3, "lines kept longer through the NGSA ramp-up" if a3 == "alt" else
                                                    "lines wind down as NGSA ramps up") +
              ("" if M.live(state, "ngsa") else " It applies once NGSA is launched; until then the A320 runs at 85 a month."),
              "- **Boeing:** fps %s%s." % ("at Renton (the Renton MAX lines wind down as the fps ramps up)" if site == "renton" else
                                          "at new sites (the MAX carries on at Renton and Everett)",
                                          "" if M.live(state, "fps") else "; it applies once the fps is launched"), ""]
    sf = unexplained_shortfall(state, year)
    if sf:
        L += ["**Market observation.** In %d-%d Boeing's narrowbody deliveries ran %s below what the published rules "
              "give for the programmes on record (shares in the table below). The game master does not attribute causes." % (
                  sf[0][0], sf[-1][0], " / ".join(sorted({"%.0f points of market share" % (100 * (p_ - a)) for _, a, p_ in sf}))), ""]
    obs = observed(state, year)
    L += ["## Observed market, %d-%d" % (2026, year - 1), "",
          "Shares of deliveries. Engine shares are of all engines delivered on narrowbody and widebody aircraft.", "",
          "| Year | NB Boeing | NB Airbus | NB deliveries Boeing / Airbus | WB Boeing | WB Airbus | NB engines CFM / P&W / RR | WB engines CFM / P&W / RR |",
          "|---:|---:|---:|---:|---:|---:|---|---|"]
    for o in obs:
        L.append("| %d | %s | %s | %d / %d | %s | %s | %s | %s |" % (
            o["year"], pct(o["nb_boeing"]), pct(o["nb_airbus"]), round(o["nb_units_boeing"]), round(o["nb_units_airbus"]),
            pct(o["wb_boeing"]), pct(o["wb_airbus"]),
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
# Control's additions (set "control2" in runs/<run>/objectives.txt; runs without the file keep the base set):
# Boeing repairs its balance sheet; Boeing and Airbus gain an engine-supply enabler; Rolls-Royce protects its
# widebody cash cow while it weighs the narrowbody.
OBJECTIVES_CONTROL2 = {
    "boeing": "Hold the 50/50 NB split; defend incumbency; repair the balance sheet (debt back to historical levels). "
              "Enabler: a stable engine supply (dual or triple engine sources; three NB engine makers)",
    "airbus": "Defend the 60/40 edge; protect the A320 family. "
              "Enabler: a stable engine supply (dual or triple engine sources; three NB engine makers)",
    "rolls_royce": "Enter the narrowbody market; keep widebody dominance; protect the widebody cash cow "
                   "(bounded narrowbody risk)",
}


def objective_set():
    run = os.environ.get("DASH_RUN")
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "runs", run, "objectives.txt") if run else None
    if p and os.path.exists(p):
        with open(p) as f:
            return f.read().strip()
    return "base"


def objective_text(side):
    if objective_set() == "control2":
        return OBJECTIVES_CONTROL2.get(side, OBJECTIVES[side])
    return OBJECTIVES[side]


# ── engine supply (Control's enabler for the airframers) ──
INCUMBENT = {"boeing": ("737 MAX", ["CFM"]), "airbus": ("A320neo family", ["CFM", "P&W GTF"])}
SOURCE_NAME = {"CFM": "CFM", "PW": "P&W GTF2", "RR": "RR UltraFan NB", "JV": "P&W-RR Joint Venture"}


def engine_sources(state, key, year=None):
    """Independent engine sources fitted to a live new airframe (at its EIS, or in `year` if given). The Joint
    Venture's engine is one source however many of its partners an airframer names. A solo engine that was ready
    by EIS and later folded into the Joint Venture counts as itself until the fold year, then as the JV's engine."""
    r = M.live(state, key)
    if not r:
        return []
    makers, jv, _ = M.effective_code(state, key)
    eis = r["eis"]
    src = ["CFM"] if "CFM" in makers else []
    jv_used = bool(jv)
    for m, solo in (("PW", "pw_solo"), ("RR", "rr_solo")):
        if m in makers and not jv:
            s_ = M.live(state, solo) or state["prog"].get("_folded_" + solo)
            if s_ and s_["ready"] <= eis and (s_.get("cancel") is None or (year is not None and year < s_["cancel"])):
                src.append(m)
            elif M.jv_available_by(state, eis) or M.live(state, "jv"):
                jv_used = True
    if jv_used:
        src.append("JV")
    return [SOURCE_NAME[x] for x in src]


def nb_sources(state, side, year):
    """(airframe in production, its engine sources) for `side`'s narrowbody in `year`: the new airframe once it
    is in service, else the incumbent."""
    key = "fps" if side == "boeing" else "ngsa"
    r = M.live(state, key)
    if r and r["eis"] <= year:
        return ("fps" if key == "fps" else "NGSA"), engine_sources(state, key, year)
    return INCUMBENT[side]


def nb_engine_makers(v, year):
    en = {r["year"]: r for r in v["_en_series"]["years"]}
    return [s for s in ("cfm", "pratt_whitney", "rolls_royce") if en[year][s]["nb_share"] > 1e-9]


# ── Rolls-Royce narrowbody risk ──
def rr_nb_exposure(state):
    """Rolls-Royce's own narrowbody development money ($B, undiscounted, as the board charges it): live UltraFan NB
    Solo or its Joint Venture share, plus write-offs of NB programmes it stopped or folded."""
    x = 0.0
    if M.live(state, "rr_solo"):
        x += M.en_rd("rr_solo")
    if M.live(state, "jv"):
        x += M.en_rd("jv", "rolls_royce")
    x += sum(d["sunk_nom"] for d in state["dead"] if d["side"] == "rolls_royce" and d["key"] in ("rr_solo", "jv"))
    return x


def objective_status(side, state, v, covert=True):
    af = {r["year"]: r for r in v["_af_series"]["years"]}
    en = {r["year"]: r for r in v["_en_series"]["years"]}
    out = []
    if side == "boeing":
        sh = {y: af[y]["boeing"].get("nb_pref_share", af[y]["boeing"]["nb_share"]) for y in (2030, 2035, 2040, 2045, 2050)}
        w = min(sh[y] for y in (2040, 2045, 2050))
        out.append(("Hold the 50/50 NB split: Boeing NB share ≥ 50% in 2040, 2045, 2050",
                    w >= 0.5 - 1e-9, "worst year %s (%s)" % (pct(w), ", ".join("%d %s" % (y, pct(sh[y])) for y in (2040, 2045, 2050)))))
        w2 = min(sh.values())
        out.append(("Defend incumbency: Boeing NB share ≥ 40% (status quo) in 2030, 2035, 2040, 2045 and 2050", w2 >= 0.4 - 1e-9,
                    "worst year %s" % pct(w2)))
    elif side == "airbus":
        sh = {y: af[y]["airbus"].get("nb_pref_share", af[y]["airbus"]["nb_share"]) for y in (2030, 2035, 2040, 2045, 2050)}
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
    if objective_set() == "control2":
        out += control2_status(side, state, v, covert)
    return out


def control2_status(side, state, v, covert=True):
    out = []
    if side == "boeing":
        import finance as FIN
        F = FIN.inputs()
        m = FIN.debt_metrics(state, v, F, covert=covert)
        H = m["H"]
        by = {r["year"]: r for r in m["rows"]}
        out.append(("Repair the balance sheet: net debt back to historical levels (≤ $%.0fB, %s) by end-%d" % (
            H, F["historical_label"], m["target_year"]), m["reached_by_target"],
            ("reached in %d" % m["first_year"] if m["first_year"] else "not reached by %d" % M.REPORT_END) +
            "; net debt end-%d $%.1fB; with no new programme it would be reached in %s" % (
                m["target_year"], by[m["target_year"]]["debt"],
                m["first_year_no_programme"] or "never")))
        out.append(("Keep it repaired: net debt ≤ $%.0fB at end-%s" % (H, ", ".join(str(y) for y in m["held"])), m["held_ok"],
                    ", ".join("%d $%.1fB" % (y, d) for y, d in m["held"].items()) +
                    ("; highest after repair $%.1fB in %d" % (m["peak_after_first"][1], m["peak_after_first"][0])
                     if m["peak_after_first"] else "")))
        ms = FIN.debt_metrics(state, v, F, stress=True, covert=covert)
        out.append(("Keep it repaired in the stress case (free cash flow one-third below consensus): net debt back to "
                    "≤ $%.0fB by end-%d and held at end-%s" % (H, ms["target_year"], ", ".join(str(y) for y in ms["held"])),
                    ms["reached_by_target"] and ms["held_ok"],
                    ("reached in %d" % ms["first_year"] if ms["first_year"] else "not reached") + "; " +
                    ", ".join("%d $%.1fB" % (y, d) for y, d in ms["held"].items()) +
                    ("; highest after repair $%.1fB in %d" % (ms["peak_after_first"][1], ms["peak_after_first"][0])
                     if ms["peak_after_first"] else "")))
    if side in ("boeing", "airbus"):
        yrs = (2040, 2045, 2050)
        src = {y: nb_sources(state, side, y) for y in yrs}
        out.append(("Enabler, stable engine supply: dual or triple engine sources on your narrowbody in production "
                    "in 2040, 2045 and 2050", all(len(src[y][1]) >= 2 for y in yrs),
                    "; ".join("%d %s: %s (%d)" % (y, src[y][0], " + ".join(src[y][1]), len(src[y][1])) for y in yrs)))
        mk = {y: nb_engine_makers(v, y) for y in (2045, 2050)}
        nm = {"cfm": "CFM", "pratt_whitney": "P&W", "rolls_royce": "RR"}
        out.append(("Enabler, stable engine supply: three narrowbody engine makers in the market in 2045 and 2050",
                    all(len(x) == 3 for x in mk.values()),
                    "; ".join("%d %s" % (y, ", ".join(nm[s] for s in x) or "none") for y, x in mk.items())))
    if side == "rolls_royce":
        x = rr_nb_exposure(state)
        out.append(("Protect the widebody cash cow, bounded NB risk: RR's own NB development money ≤ $4B. The Joint "
                    "Venture share is $4B and UltraFan NB Solo $8B; a Solo cancelled or folded into the Joint Venture "
                    "counts its spend to date (a Solo launched in 2030 and folded in 2035 is $5.7B)", x <= 4.0 + 1e-9,
                    "$%.2fB committed or written off" % x))
        _, strain, _, _ = M.engine_costs(state)
        out.append(("Protect the widebody cash cow, WB never starved: never hold an NB engine programme (UltraFan NB "
                    "Solo or the Joint Venture) and a WB programme (UltraFan WB or Trent 1000 upgrade) at the same time. "
                    "The board charges a one-off $5B strain whenever both are on record, whatever their dates and even "
                    "after one is ready; only cancelling one before it is ready removes it", strain["rolls_royce"] <= 1e-9,
                    "strain charged $%.1fB" % strain["rolls_royce"]))
    return out


def sees_covert(state, side, year):
    """Airbus always values its own covert moves. Another player's valuation includes them only once their market
    effect is entirely in the past (observed deliveries); its cause is never disclosed."""
    if side == "airbus":
        return True
    fps = M.live(state, "fps")
    if not (state["dt"]["bottleneck"] or state["dt"]["poaching"]) or not fps:
        return False
    return fps["eis"] + 5 <= year


def unexplained_shortfall(state, year):
    """Public market observation: years before `year` in which Boeing's NB deliveries ran below what the published
    rules give for the programmes on record. Returns [(year, actual, rule)]."""
    va = M.value(state, covert=True, series=True)["_af_series"]["years"]
    vp = M.value(state, covert=False, series=True)["_af_series"]["years"]
    out = []
    for a, p_ in zip(va, vp):
        if a["year"] < year and abs(a["boeing"]["nb_share"] - p_["boeing"]["nb_share"]) > 1e-9:
            out.append((a["year"], a["boeing"]["nb_share"], p_["boeing"]["nb_share"]))
    return out


# ─────────────────────────────── own options and rival scenarios ───────────────────────────────
def own_options(state, side, year):
    """(label, orders) for each distinct own plan this round. Engine codes are not varied here (they do not change
    an airframer's own payoff on the board)."""
    L = R.legal_options(state, side, year)
    out = []
    if side == "boeing":
        code = state["codes"].get("fps") or 7
        sites = L.get("fps_site", [None])
        for f, r, w, site in itertools.product(L["fps"], L["rate_737"], L["re787"], sites):
            fps_on = f.startswith("launch") or (M.live(state, "fps") and f != "cancel")
            if site is not None and site != sites[0] and not fps_on:
                continue                                   # the site only matters with an fps
            o = {"fps": f, "rate_737": r, "re787": w, "fps_engine_code": code if f.startswith("launch") else None}
            if site is not None:
                o["fps_site"] = site
            lab = [{"hold": "fps: hold", "launch_7yr": "fps 7-yr", "launch_10yr": "fps 10-yr",
                    "launch_via_embraer": "fps via Embraer", "cancel": "cancel fps"}[f]]
            if site is not None and fps_on and (site == "renton" or site != sites[0]):
                lab[-1] += {"renton": " at Renton", "new_site": " at new sites"}[site]
            if r == "increase": lab.append("737 rate up")
            lab.append({"hold": "787: hold", "launch": "787 Re-engine", "cancel": "cancel 787 Re-engine"}[w])
            out.append((" + ".join(lab), o))
    elif side == "airbus":
        code = state["codes"].get("ngsa") or 7
        dts = [d for d in L["delay_tactics"] if d != "poaching"]   # bottleneck and poaching are the same on the board
        plans_ = L.get("a320_plan", [None])
        for n, a, d, pl in itertools.product(L["ngsa"], L["rea350"], dts, plans_):
            ngsa_on = n == "launch" or (M.live(state, "ngsa") and n != "cancel")
            if pl is not None and pl != plans_[0] and not ngsa_on:
                continue                                   # the A320 plan only matters with NGSA
            o = {"ngsa": n, "rea350": a, "delay_tactics": d, "ngsa_engine_code": code if n == "launch" else None}
            if pl is not None:
                o["a320_plan"] = pl
            lab = [{"hold": "NGSA: hold", "launch": "NGSA", "cancel": "cancel NGSA"}[n],
                   {"hold": "A350: hold", "launch": "A350 Re-engine", "cancel": "cancel A350 Re-engine"}[a]]
            if pl is not None and ngsa_on and (pl == "alt" or pl != plans_[0]):
                lab[0] += {"alt": " (A320 Alt plan)", "base": " (A320 base plan)"}[pl]
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
            if M.SD_ON:
                sc.append(("Airbus launches NGSA on the A320 Alt plan", {"airbus": {"ngsa": "launch", "ngsa_engine_code": 6, "a320_plan": "alt"}}))
        ng = M.live(state, "ngsa")
        if M.SD_ON and ng and ng["eis"] > year:
            import supply_demand as SD
            if SD.plans(state)[0] == "base":
                sc.append(("Airbus switches to the A320 Alt plan", {"airbus": {"a320_plan": "alt"}}))
            else:
                sc.append(("Airbus returns to the A320 base plan", {"airbus": {"a320_plan": "base"}}))
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
            if M.SD_ON:
                sc.append(("Boeing launches fps 10-yr at Renton", {"boeing": {"fps": "launch_10yr", "fps_engine_code": 7, "fps_site": "renton"}}))
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
        if side == "rolls_royce" and M.live(state, "re787") is None:
            sc.append(("Boeing launches 787 Re-engine", {"boeing": {"re787": "launch"}}))
        if side == "rolls_royce" and M.live(state, "re787") is None and M.live(state, "rea350") is None:
            sc.append(("Boeing launches 787 Re-engine and Airbus A350 Re-engine",
                       {"boeing": {"re787": "launch"}, "airbus": {"rea350": "launch"}}))
    return sc


def payoff_grid(state, side, year, metrics_out=None):
    """Own ΔPV and yield for every own plan × rival scenario, assuming no moves after this round. With
    `metrics_out` (a dict), also fills {(plan index, scenario index): objective metrics} for Control's objectives."""
    opts = own_options(state, side, year)
    scen = rival_scenarios(state, side, year)
    covert = sees_covert(state, side, year)
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
            if metrics_out is not None:
                cv = covert or slab.startswith("Risk case")
                m = plan_metrics(side, s1, v, cv)
                if side in ("boeing", "airbus"):          # engine makers follow a selection in the same round
                    of = dict(orders)
                    of.setdefault("pratt_whitney", {})
                    of.setdefault("rolls_royce", {})
                    of["pratt_whitney"] = dict(of["pratt_whitney"], gtf2_solo="launch_if_selected")
                    of["rolls_royce"] = dict(of["rolls_royce"], ultrafan_nb_solo="launch_if_selected")
                    sf, _ = R.adjudicate(state, year, of)
                    vf = M.value(sf, covert=cv, series=True)
                    m["sources_2050_follow"] = len(nb_sources(sf, side, 2050)[1])
                    m["makers_2050_follow"] = len(nb_engine_makers(vf, 2050))
                metrics_out[(len(grid), len(row) - 1)] = m
        grid.append((olab, o, row))
    return grid, scen


def plan_metrics(side, state, v, covert=True):
    """Control's objective metrics for one grid cell (a plan against a scenario)."""
    if side == "boeing":
        import finance as FIN
        m = FIN.debt_metrics(state, v, covert=covert)
        ms = FIN.debt_metrics(state, v, stress=True, covert=covert)
        by = {r["year"]: r for r in m["rows"]}
        bys = {r["year"]: r for r in ms["rows"]}
        return {"repaired": m["first_year"], "debt_2035": by[2035]["debt"], "debt_2040": by[2040]["debt"],
                "held_ok": m["held_ok"], "stress_ok": ms["reached_by_target"] and ms["held_ok"],
                "stress_peak": max(r["debt"] for r in ms["rows"] if r["year"] >= 2030),
                "sources_2050": len(nb_sources(state, side, 2050)[1]), "makers_2050": len(nb_engine_makers(v, 2050))}
    if side == "airbus":
        return {"sources_2050": len(nb_sources(state, side, 2050)[1]), "makers_2050": len(nb_engine_makers(v, 2050))}
    if side == "rolls_royce":
        en = {r["year"]: r for r in v["_en_series"]["years"]}
        _, strain, _, _ = M.engine_costs(state)
        af = {r["year"]: r for r in v["_af_series"]["years"]}
        return {"nb_exposure": rr_nb_exposure(state), "strain": strain["rolls_royce"],
                "wb_2050": en[2050]["rolls_royce"]["wb_share"], "nb_2050": en[2050]["rolls_royce"]["nb_share"],
                "airbus_wb_2050": af[2050]["airbus"]["wb_share"]}
    return None


def code_sources_section(state, side, year):
    """Independent engine sources each engine code would give on your new narrowbody, with the engine programmes
    on record now (a maker whose engine is not ready by your EIS drops out; CFM always fits)."""
    import copy
    key = "fps" if side == "boeing" else "ngsa"
    r = M.live(state, key)
    if r and r["eis"] <= year:
        return []
    if r:
        eis_txt = "your %s's EIS %d" % ("fps" if key == "fps" else "NGSA", r["eis"])
    else:
        dev = M.af_dev(key, "10yr") if key == "fps" else M.af_dev(key)
        eis_txt = "an EIS of %d (a launch this round%s)" % (year + dev, ", 10-year ramp" if key == "fps" else "")
    rows, notes = [], []
    other = "ngsa" if key == "fps" else "fps"
    ro = M.live(state, other)
    for c in range(1, 8):
        if ro and ro["eis"] > year:
            pair = (c, state["codes"].get(other, 7)) if key == "fps" else (state["codes"].get(other, 7), c)
            if pair in M.FORBIDDEN:
                notes.append("- Code %d is not allowed together with the %s's current code %d: the airframe entering "
                             "service later is moved to code 7 (all three)." % (c, "NGSA" if other == "ngsa" else "fps",
                                                                                 state["codes"].get(other, 7)))
        s2 = copy.deepcopy(state)
        if not r:
            s2["prog"][key] = {"launch": year, "eis": year + dev, "cancel": None, "variant": "10yr" if key == "fps" else None}
        s2["codes"][key] = c
        src = engine_sources(s2, key)
        rows.append([c, M.CODE_LABEL[c], " + ".join(src), len(src)])
    eng = []
    for k, lab in (("pw_solo", "P&W GTF2"), ("rr_solo", "RR UltraFan NB"), ("jv", "P&W-RR Joint Venture")):
        e = M.live(state, k)
        eng.append("%s %s" % (lab, ("ready %d" % e["ready"]) if e else "not launched"))
    L = ["", "**Engine sources by engine code** at %s, with the engine programmes on record now (%s). A maker whose "
         "engine is not ready by your EIS drops out. CFM is always ready: it is fitted when your code names it, or "
         "alone if no maker you named is ready by your EIS. The engine makers' own moves this round can change this "
         "(P&W and Rolls-Royce can launch an engine when an airframer selects them)." % (eis_txt, "; ".join(eng)), ""]
    L += table(["Code", "Makers named", "Fitted sources", "Count"], rows)
    if notes:
        L += [""] + notes
    return L


def debt_section(state, v, covert=False):
    """Boeing's debt path from the GM's balance-sheet tracker (Boeing's brief only)."""
    import finance as FIN
    F = FIN.inputs()
    rows = FIN.debt_path(state, v, F, covert=covert)
    stress = {r["year"]: r for r in FIN.debt_path(state, v, F, F["stress_fcf_scale"], covert=covert)}
    show = set(range(2027, 2043)) | {2045, 2050, 2055, 2060}
    L = ["", "**Your net-debt path** if nobody moves again (the GM's balance-sheet tracker; constant 2026 $B, year end). " +
         F["method_short"], ""]
    L += table(["Year", "Base free cash flow", "Profit vs game baseline (pre-tax)", "Programme cash spend",
                "Interest on added debt", "Free cash flow", "Net debt", "Net debt with no new programme",
                "Net debt, stress case"],
               [[r["year"], f1(r["base_fcf"]), money(r["profit_vs_baseline"]), f1(r["spend"]) if r["spend"] else "—",
                 f1(r["interest"]) if r["interest"] > 0.05 else "—", money(r["fcf"]), f1(r["debt"]),
                 f1(r["debt_no_programme"]), f1(stress[r["year"]]["debt"])] for r in rows if r["year"] in show])
    return L


def metric_cell(side, m):
    if side == "boeing":
        return "%s / %s / %s ($%.1fB) / %d (%d)" % (m["repaired"] or "never", "yes" if m["held_ok"] else "no",
                                                    "yes" if m["stress_ok"] else "no", m["stress_peak"],
                                                    m["sources_2050"], m["sources_2050_follow"])
    if side == "airbus":
        return "%d / %d (%d / %d)" % (m["sources_2050"], m["makers_2050"], m["sources_2050_follow"],
                                      m["makers_2050_follow"])
    return "$%.1fB / $%.0fB / %s / %s / %s" % (m["nb_exposure"], m["strain"], pct(m["wb_2050"]), pct(m["nb_2050"]),
                                              pct(m["airbus_wb_2050"]))


METRIC_KEY = {
    "boeing": "Each cell: year net debt first reaches the historical level / held at or below it at end-2035, 2040, "
              "2045 and 2050 / the same in the stress case (free cash flow one-third below consensus), with its highest "
              "net debt from 2030 / engine sources on your narrowbody in production in 2050 if the engine makers hold "
              "this round (in brackets: if P&W and Rolls-Royce both launch an engine when selected, in the same round). "
              "Airframer payoffs do not depend on engine-maker moves.",
    "airbus": "Each cell: engine sources on your narrowbody in production in 2050 / narrowbody engine makers in the "
              "market in 2050, if the engine makers hold this round (in brackets: if P&W and Rolls-Royce both launch an "
              "engine when selected, in the same round). Airframer payoffs do not depend on engine-maker moves.",
    "rolls_royce": "Each cell: your own NB development money (committed or written off) / NB+WB strain ($5B if you hold "
                   "both an NB and a WB programme, whatever their dates) / your WB engine share in 2050 / your NB engine "
                   "share in 2050 / Airbus's widebody airframe share in 2050 (the A350 fleet you power alone; the "
                   "board's WB engine shares do not move with the 787/A350 split).",
}


# ─────────────────────────────── private brief ───────────────────────────────
OWN_KEYS = {"boeing": ("fps", "re787", "rate737"), "airbus": ("ngsa", "rea350"),
            "cfm": ("cfm_ducted", "cfm_open_fan", "cfm_embraer", "cfm_lobby", "cfm_genx"),
            "pratt_whitney": ("pw_solo", "jv"), "rolls_royce": ("rr_solo", "jv", "rr_uf_wb", "rr_t1000")}
BRIDGE_LABEL = {"nb_profit_vs_sq": "Narrowbody operating profit vs status quo", "wb_profit_vs_sq": "Widebody operating profit vs status quo",
                "programme_investment": "Programme investment (booked at EIS)", "rate_hike": "737 rate increase",
                "delay_tactics_spend": "Delay Tactics spend", "write_offs": "Cancellation write-offs",
                "debt_penalty": "Debt penalty (α)", "two_front_strain": "Two-front strain", "naked_fine": "Naked Delay Tactics fine",
                "engine_value_vs_sq": "Engine value vs status quo", "r_and_d": "R&D (undiscounted, as the board)",
                "strain": "Strain (concurrent programmes)",
                "supply_demand": "Supply and demand: aircraft your factories can deliver, against the board's market",
                "supply_plan": "Supply plan cost or saving (your plan)"}
SUPPLY_PLAN_LABEL = {"boeing": "Supply plan: new-site capex avoided at Renton", "airbus": "Supply plan: A320 Alt plan cost"}


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


SD_YEARS = [2026, 2028, 2030, 2032, 2033, 2034, 2035, 2036, 2037, 2038, 2039, 2040, 2041, 2042, 2043, 2044, 2045, 2047, 2050, 2053, 2055, 2060]


def sd_outlook(side, state, v):
    """Supply and demand for an airframer if nobody moves again: demand, what customers want from you, your backlog,
    your factories (public plans), deliveries and the other maker's capacity (also a public plan)."""
    import supply_demand as SD
    pre, other = ("b", "a") if side == "boeing" else ("a", "b")
    a3, ng = SD.plans(state)
    plan = ("fps site: %s" % {"new_site": "new sites", "renton": "Renton"}[ng]) if side == "boeing" else (
        "A320 plan: %s" % a3)
    L = ["", "**Supply and demand if nobody moves again** (aircraft a year; your %s; capacities are the public "
         "production plans):" % plan, ""]
    rows = []
    for r in v["_af_series"]["years"]:
        y = r["year"]
        if y not in SD_YEARS:
            continue
        x, o = r[side], r["airbus" if side == "boeing" else "boeing"]
        cap = (r["sd"]["cap_max"], r["sd"]["cap_fps"]) if side == "boeing" else (r["sd"]["cap_a320"], r["sd"]["cap_ngsa"])
        rows.append([y, "%d" % round(r["sd"]["demand"]), "%d" % round(x["sd"]["firm_in"]), "%d" % round(x["sd"]["wanted"]), "%d" % round(x["sd"]["backlog_in"]),
                     "%d + %d" % (round(cap[0]), round(cap[1])), "%d" % round(x["nb_units"]), "%d" % round(x["sd"]["spill_in"]),
                     pct(x["nb_pref_share"]), pct(x["nb_share"]), "%d" % round(o["sd"]["capacity"]), "%d" % round(x["sd"]["sq_delivered"])])
    L += table(["Year", "New market demand", "Your firm backlog", "New demand for you (preference)", "Your waiting backlog",
                "Your capacity (%s)" % ("MAX + fps" if side == "boeing" else "A320 + NGSA"),
                "You deliver", "of which the rival's flexible customers", "Preference share", "Delivered share",
                "Rival capacity", "You deliver in the status quo"], rows)
    L += ["", "Status quo: nobody launches anything (A320 at 85 a month, the MAX path, 40/60 preference); your payoff "
          "is measured against it."]
    return L


def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---:" if i else "---" for i in range(len(head))) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return out


def private_brief(state, side, year, round_no, last_orders=None, gm_notes=None):
    name = M.NAMES[side]
    v = M.value(state, covert=sees_covert(state, side, year), series=True)
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
    L += table(["Component", "$B (PV at 2026)"], [[SUPPLY_PLAN_LABEL.get(side, BRIDGE_LABEL[k]) if k == "supply_plan" else BRIDGE_LABEL[k],
                                                  money(x)] for k, x in me["bridge"].items() if abs(x) > 1e-12])
    if M.SD_ON and side in ("boeing", "airbus") and "supply_demand" in me["bridge"]:
        L += ["", "The narrowbody line is the board's (2,000 a year, every aircraft delivered); the supply-and-demand line "
              "corrects it to the aircraft your factories can deliver, net of the same correction in the status quo."]
    if M.SD_ON and side not in ("boeing", "airbus"):
        L += ["", "Supply and demand is on: your narrowbody engine volumes follow the aircraft actually delivered (two "
              "engines each), not the board's 2,000 a year. The 737 MAX keeps CFM and the A320neo CFM 60% / P&W 40%; "
              "engine moves shift share only on the fps and NGSA, from their fitted makers. While MAX and A320neo are "
              "still built alongside a slowly ramping new type, your moves reach fewer engines. See the last section "
              "of rules.md."]
    L += ["", ("Year by year ($B at 2026 prices: the airframer board does not escalate; shares of the market's "
               "deliveries):" if side in ("boeing", "airbus") else
               "Year by year (nominal $B; shares of the market's deliveries):"), ""]
    head, prow = projection_rows(side, v)
    L += table(head, prow)
    if side in ("boeing", "airbus") and M.SD_ON:
        L += sd_outlook(side, state, v)
    if side in ("boeing", "airbus"):
        L += ["", "The board counts each programme's market for 20 years from its EIS (unlaunched programmes use the "
              "snapshot dates fps %d, NGSA %d, Re-engines %d), so years after that window add nothing to ΔPV." % (
                  M.DEFAULT_EIS["fps"], M.DEFAULT_EIS["ngsa"], M.DEFAULT_EIS["re787"])]
    else:
        t = v["_engine_timing"]
        L += ["", "The board counts the narrowbody engine market to %d and the widebody to %d." % (
            t["nb_window_end"], t["wb_window_end"])]
    L += ["", "## 2. Your objective", "", "Briefing goal: **%s**." % objective_text(side), ""]
    for lab, ok, det in objective_status(side, state, v, sees_covert(state, side, year)):
        L.append("- %s — **%s** (%s)" % (lab, "met" if ok else "not met", det))
    if objective_set() == "control2" and side == "boeing":
        L += debt_section(state, v, sees_covert(state, side, year))
    if objective_set() == "control2" and side in ("boeing", "airbus"):
        L += code_sources_section(state, side, year)
    L += ["", "## 3. Your options this round", ""]
    legal = R.legal_options(state, side, year)
    for k, opts in legal.items():
        L.append("- `%s`: %s" % (k, ", ".join("`%s`" % o for o in opts)))
    mets = {} if (objective_set() == "control2" and side in METRIC_KEY) else None
    grid, scen = payoff_grid(state, side, year, metrics_out=mets)
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
    if mets:
        L += ["", "**Your objective metrics by plan** (Control's objectives in section 2; same plans and scenarios as "
              "the payoff grid). " + METRIC_KEY[side], ""]
        L += table(head, [[g[0]] + [metric_cell(side, mets[(i, j)]) for j in range(len(scen))]
                          for i, g in enumerate(grid)])
    L += ["", "## 4. What to return", "",
          "Return your sealed orders as the JSON object your task specifies: one value for each order field above, "
          "plus `other_moves`, `public_statement`, `rationale` (with your ExCo deliberation), `predictions` and "
          "`expected_pv_b`. Fields you leave out are read as `hold`%s." % (
              " (a supply-plan field you leave out keeps your current plan)" if (M.SD_ON and side in ("boeing", "airbus")) else "")]
    return "\n".join(L), grid, scen
