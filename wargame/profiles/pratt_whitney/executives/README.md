# Pratt & Whitney: executives and leadership teams

These files let the `pratt-whitney-strategist` decide as a named Pratt & Whitney leadership team, and let the referee judge whether it did.

Each executive is profiled from their own words on UTC and RTX calls and investor days:
- `evidence.jsonl` holds the quotes (PX-####), each with its `role_at_time` and `date`;
- the company file `../evidence.jsonl` holds the context items (P-####).

Pratt & Whitney is a business of RTX (before April 2020, of UTC), so the seats split by level:
- **RTX level, the CEO and CFO:** capital allocation, the balance sheet, the dividend and buybacks, and the gate every new engine passes [PX-0199][PX-0081].
- **Pratt & Whitney level, the President:** the fleet plan, durability upgrades, MRO, campaign pricing and the split between Airbus engines and the fleet [PX-0123][PX-0099].

`teams.md` §1 maps each game lever to its level.

## Executives

| Executive (file) | Role(s) and dates | Own words (ids) | Events | Confidence | Teams |
|---|---|---|---|---|---|
| Christopher T. Calio (calio.md) | President, Pratt & Whitney (in our evidence May 2021); RTX COO (Jan 2023), then President & COO (Apr 2023), CEO-designate from Jan 2024; RTX CEO (in our evidence from Jul 2024); Chairman & CEO (May–Oct 2025) | 110 (PX-0001 to PX-0110) | 20 (2021, then 2023 to Oct 2025; none from 2022) | High on crisis handling, capital order, pricing and durability-first; Medium on new-engine launches; Low on a Rolls-Royce Joint Venture, widebody and the open fan | 2023, 2026 |
| Neil G. Mitchill (mitchill.md) | VP & CFO, Pratt & Whitney (Jun 2019); UTC Acting CFO (Jan 2020); RTX VP FP&A and IR (2020); RTX CFO from Apr 2021, EVP & CFO to Oct 2025 | 180 (PX-0181 to PX-0360) | 34 (Jun 2019 to Oct 2025) | High on capital allocation, guidance, GTF economics and recall finance; Medium on launches; none on the Joint Venture, widebody or CFM | 2019, 2023, 2026 |
| Robert F. (Bob) Leduc (operations.md) | President, Pratt & Whitney (in our evidence Mar 2016 to Jun 2019; in the seat to about 2019) | 49 (PX-0132 to PX-0180) | 4 | Medium-high on the ramp, supply chain, crisis handling and pricing; Low on launches (only the NMA bid) | 2019 |
| Shane G. Eddy (operations.md) | President, Pratt & Whitney (in our evidence 19 Jun 2023 only; start and end dates not shown) | 21 (PX-0111 to PX-0131) | 1 | Low: one event, before the powder-metal recall | 2023, 2026 |

**Context only (not profiled):**
- Gregory J. Hayes, UTC then RTX CEO to 2024. He holds the CEO seat in the 2019 team and was CEO above Calio in 2023 [P-0731][P-0602].
- Akhil Johri, UTC's CFO in 2019 [P-0734].
- Rick Deurloo, quoted as President, Commercial Engines in November 2025 [P-1817].

## Teams

| Team id | CEO seat | CFO seat | Operating seat | Status |
|---|---|---|---|---|
| `calio-mitchill-eddy-2026` | Calio, RTX Chairman & CEO | Mitchill, RTX EVP & CFO | Eddy, President of Pratt & Whitney (assumed still in the seat) | **DEFAULT** for the 2026 game |
| `calio-mitchill-eddy-2023` | Calio, RTX President & COO under Hayes (context) | Mitchill, RTX CFO | Eddy (assumed in the seat beyond June 2023) | Historical: "what if this team ran the company today" |
| `hayes-mitchill-leduc-2019` | Hayes, UTC Chairman & CEO (context only) | Mitchill, **Pratt & Whitney's** CFO (UTC's was Johri) | Leduc | Historical: "what if this team ran the company today" |

**One line per team:**
- **2026 (default).** Durability first and a lower NGSA hedge bar (about 0.3), driven by the CEO's "miss a cycle". The CFO's gate makes it cancel in round 2, and it deleverages before buybacks.
- **2023.** Crisis-mode recovery: the fleet first, and `gtf_next` only on a disclosed selection, since it planned for a late NGSA. It held capital returns and is prone to reassurance before the facts.
- **2019.** Offence on its own terms: sole-source offers to both airframers, no launch-mode pricing and capacity discipline. It protects E&D, is the least crisis-scarred, and carries the most durability optimism at entry into service.

`teams.md` §2 checks membership dates against the evidence; no team id changed.

## How the strategist uses these files

1. **Load the team** named in the `leadership` argument, or the default. Read its card in `teams.md` (members, decision rule, tensions, script, round table, reactions) and each member's Quick card and "In the game" section.
2. **Each turn, run the ExCo script.**
   - The CEO frames the turn.
   - The President proposes the upgrade, launches and terms.
   - The CFO tests cash, the envelope and the break-even odds from `whatif`.
   - The CEO decides by the team's rule.

   Record each seat's view, the numbers asked for and the tie-break used in the rationale.
3. **Use the engine as the finance team.** Re-run the `teams.md` §3 reference cases with `whatif` every turn, since injects and other players' orders move them.
4. **Keep the company red lines** (`../profile.md`) and the objective weighing (`../objectives.md` §6–7). A team never trades a red line. Doctrine and objective premiums share the $1B cap.
5. **Speak in the team's voice.**
   - The CEO's lines are for the public statement.
   - The CFO's ranges are for any figure.
   - Disclose conditional, dated offers; never speak for an airframer [PX-0062].

## Gaps

- **Eddy:** one event. Both Calio-Mitchill-Eddy teams assume he still holds the operating seat, and the role of the 2025 President of Commercial Engines is unexplained [P-1817].
- **Hayes and Johri** are not profiled. The 2019 card's CEO and group-CFO calls rest on company items. Mitchill has only two items from 2019, as Pratt's CFO [PX-0181].
- **Nobody in any team speaks on:**
  - joining Rolls-Royce's UltraFan Joint Venture;
  - CFM's RISE open fan;
  - a widebody engine beyond the 2019 NMA bid;
  - a hurdle rate after 2019.

  Those thresholds are inference from engine payoffs.
- **Coverage:** no Calio events from 2022, and nothing after October 2025 (November 2025 press only).
- **Engine values** in the cards come from one scratch run and are not evidence.
