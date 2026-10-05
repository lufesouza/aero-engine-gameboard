# Pratt & Whitney: leadership teams

The `pratt-whitney-strategist` plays the team it is given. Each turn it runs that team's executive-committee (ExCo) deliberation and records it in its rationale. The referee judges fidelity against the same card.

- **Default for the 2026 game: `calio-mitchill-eddy-2026`.**
- The two historical teams are "what if this team ran the company today" options. They face the same 2026 board, rules and rivals, and decide as they decided in their own era.
- Read each card with the members' profiles (`calio.md`, `mitchill.md`, `operations.md`) and the company doctrine (`../profile.md`, `../objectives.md`). The cards say how each team applied or sharpened the doctrine; they do not repeat it.

## 1. Seats, and what RTX decides against what Pratt & Whitney decides

Pratt & Whitney is a business of RTX; before April 2020 its parent was UTC. Every team has three seats:
- **The CEO seat** frames the turn and takes the final call.
- **The CFO seat** tests cash, debt, the dividend and the return gate.
- **The operating seat**, the President of Pratt & Whitney, proposes engine orders and tests durability, parts and capacity.

| Decision | Level | In the game | Evidence |
|---|---|---|---|
| Dividend, buybacks, debt and rating, M&A, guidance | RTX | Not a lever; it frames what a new engine competes with | [PX-0203][PX-0282][PX-0081][PX-0353] |
| The E&D and capex envelope, and the project gate by size | RTX: "through me, through Greg, up to our Board" | Every `gtf_next`, `pw_wb` or `join_rr_jv` passes the CFO's gate and the CEO's call (inference) | [PX-0199][PX-0102][PX-0268] |
| A new centreline engine | RTX: "not in the plan" | `gtf_next`, `pw_wb`, `join_rr_jv` | [PX-0202][P-0745] |
| Ending a failing programme | RTX CEO | `cancel` (inference by analogy) | [P-1342][PX-0064] |
| Durability upgrades and the retrofit kit | Pratt & Whitney, inside the envelope | `gtf_upgrade`: the President proposes, the CFO signs off $1.0B over 3 years | [PX-0088][PX-0325][PX-0116] |
| Campaign pricing | Pratt & Whitney, inside RTX's rules | `terms`: the President prices; the CEO vetoes launch-style discounts | [PX-0137][PX-0055] |
| Fleet plan, MRO, the split between Airbus engines and the fleet, catalog prices | Pratt & Whitney (with Airbus on allocation) | No lever; the source of the upgrade case | [PX-0123][PX-0099][PX-0092] |
| Recall accounting, the compensation reserve and its cash phasing | RTX CFO | The `gtf_durability_crisis` response | [PX-0294][PX-0306] |
| Public statements and disclosure | RTX: the CEO's voice, the CFO's numbers | `public_statement`, `disclose` | [PX-0086][PX-0288][PX-0212] |

## 2. Membership check

Checked against `role_at_time` and `date` in `evidence.jsonl`. No id changes.

| Team id | Seat | Person, role in the evidence | Dates | Verdict |
|---|---|---|---|---|
| `hayes-mitchill-leduc-2019` | CEO | Gregory Hayes, UTC Chairman & CEO. **Context only**: not profiled, company items only [P-0731][P-1233] | 2019 | Keep |
| | CFO | Neil Mitchill, **VP & CFO of Pratt & Whitney**, not of UTC or RTX [PX-0181][PX-0182]. UTC's CFO was Akhil Johri (context, not in the id) [P-0734][P-1243] | Jun 2019 | Keep |
| | Operating | Bob Leduc, President of Pratt & Whitney [PX-0177][PX-0180] | Mar 2016 to Jun 2019 | Keep |
| `calio-mitchill-eddy-2023` | CEO | Chris Calio, RTX COO from Jan 2023 [PX-0015], then **RTX President & COO** from Apr 2023 [PX-0019][PX-0043]. Hayes was still CEO and took the CEO's decisions [P-0602][P-0591] (context) | 2023 | Keep |
| | CFO | Mitchill, RTX CFO since Apr 2021 [PX-0189][PX-0284] | 2023 | Keep |
| | Operating | Shane Eddy, President of Pratt & Whitney [PX-0111]. All three spoke at the same June 2023 Investor Day [PX-0022][PX-0284][PX-0120] | 19 Jun 2023 | Keep |
| `calio-mitchill-eddy-2026` | CEO | Calio, CEO-designate from Jan 2024 [PX-0044], **RTX CEO** in our evidence from Jul 2024 [PX-0063], Chairman & CEO from May 2025 [PX-0090] | to Oct 2025 | Keep |
| | CFO | Mitchill, EVP & CFO [PX-0353][PX-0357] | to Oct 2025 | Keep |
| | Operating | Eddy: **one event, June 2023** [PX-0111]–[PX-0131]. In November 2025 the press quotes Rick Deurloo as President, Commercial Engines [P-1817]; how that post relates to the President's seat is not shown | Jun 2023 | Keep, **assuming Eddy still holds the seat** |

The 2023 and 2026 ids both assume that Eddy still holds the operating seat. His stances are read forward from one event.

## 3. Engine reference values (re-run every turn)

[engine] `whatif`, scenario `five-player-2045` with Rolls-Royce, Pratt & Whitney and CFM/GE, turn 1, no injects. Figures are Pratt & Whitney ΔPV in $B.
- U means `gtf_upgrade` ordered in round 1.
- Our launches are on standard terms, in the airframer's year.
- "CFM" means CFM/GE launched `ducted` in the same round.

These come from one scratch run. They are not evidence.

| Round | Case | ΔPV |
|---|---|---|
| 1 (2026–30) | U in round 1 / 2 / 3 | +1.76 / +1.15 / +0.75 |
| | NGSA 2030 on CFM: Do Nothing / with U | -2.57 / -1.14 |
| | NGSA 2030 on `pw_gtf2`, with U: standard / aggressive / without U | +1.75 / -1.97 / +0.31 |
| | `gtf_next` 2030 with U, nobody selects it: cancelled in round 2 / never cancelled | +1.03 / -1.85 |
| | Launched early with U, NGSA 2030 on ours: 2028 (strain -0.34) / 2026 (strain -1.12) | +0.77 / -0.77 |
| | fps 2030 with U: ours / CFM ducted / CFM open fan | +2.61 / +1.31 / +1.60 |
| | fps and NGSA 2030 with U: both ours / fps ours and NGSA CFM / NGSA ours and fps CFM | +3.88 / -1.30 / +0.43 |
| | `join_rr_jv` with U, RR `jv_pw` 2030: NGSA on UltraFan / nobody / NGSA on CFM | +12.14 / -1.25 / -4.14 |
| | Join and `gtf_next` together with U: NGSA on UltraFan / on ours | +7.93 / -1.86 |
| | NGSA on RR's Solo UltraFan, with U | -1.14 |
| | NGSA on the RISE open fan with U: launched 2030 / 2037 | +0.48 / +0.62 |
| | CFM `leap_upgrade`: alone / with our U in round 1 / with ours in round 2 | -0.67 / +1.09 / +0.48 |
| | `pw_wb` 2030 with U: 787 Re-engine / A350 Re-engine | -1.43 / -1.79 |
| 2 (2031–35) | NGSA 2033 with U: CFM / ours / ours aggressive | -0.41 / +1.42 / -1.38 |
| | NGSA 2035 with U: CFM / ours / ours aggressive | -0.01 / +1.21 / -1.08 |
| | Round-1 `gtf_next` (2030) kept; NGSA 2033 picks it | +0.63 |
| | Round-2 hedge with U, unselected, cancelled in round 3: launched 2033 / 2035 | +0.17 / +1.27 |
| | Join with U, RR `jv_pw` 2033: NGSA on UltraFan / nobody / NGSA on CFM | +9.41 / -0.60 / -2.76 |
| 3 (2036–45) | NGSA 2037 with U: CFM / open fan / ours / ours aggressive | +0.33 / +0.62 / +0.99 / -0.85 |
| | `gtf_next` 2037 with U, unselected (no later round in which to cancel) | -0.28 |
| | fps 2037 with U: ours / CFM | +1.52 / +1.54 |

**Break-even odds** = cost if unselected ÷ (cost + gain if selected) [engine]:

| Lever and round | Cost | Gain | Odds |
|---|---|---|---|
| `gtf_next` hedge for NGSA, round 1 (2030, cancelled in round 2) | 0.73 | 2.89 | 0.20 |
| `gtf_next` hedge, round 2, launched 2035 | 0.49 | 1.22 | 0.29 |
| `gtf_next` hedge, round 2, launched 2033 | 1.59 | 1.83 | 0.46 |
| `gtf_next`, round 3 (2037) | 2.04 | 0.66 | 0.76 |
| `join_rr_jv`, round 1 / round 2 | 3.01 / 2.36 | 13.28 / 9.82 | 0.18 / 0.19 |

**Mechanics every team must respect** [engine]:
- A round-1 `gtf_next` (2030) is ready in 2036, so it can be cancelled only in round 2. Carried into round 3, it runs to completion.
- Nothing launched in round 3 can be cancelled.
- Always give `year` and `terms`.
- The objectives score `gtf_base`, at least 960 engines a year in 2040, 2045 and 2050. It holds only if NGSA flies our engine (2,400+ a year), flies the Joint Venture (1,248+), or does not enter service before 2050. An open-fan NGSA keeps 1,080 to 2044–45 and then 0.
- `credibility` needs U booked by 2031, so it must be ordered in round 1 or 2.

---

## 4. `calio-mitchill-eddy-2026` (DEFAULT)

### Members and roles

| Seat | Member | Role | Profile |
|---|---|---|---|
| CEO | Christopher T. Calio | RTX Chairman & CEO; President of Pratt & Whitney in 2021 [PX-0090][PX-0001] | `calio.md` |
| CFO | Neil G. Mitchill | RTX EVP & CFO [PX-0353] | `mitchill.md` |
| Operating | Shane G. Eddy | President of Pratt & Whitney; evidence June 2023 only [PX-0111] | `operations.md` |

Calio once ran Pratt & Whitney [PX-0001], so the CEO seat knows the GTF unit economics as well as the President does. The CFO and CEO already work as a pair: both sit, at least quarterly, in RTX's monthly cost-reduction summits, where each business defends its pipeline [PX-0249].

### Decision rule

- **Who proposes.** Eddy proposes the engine orders: the upgrade, launch timing and terms (inference from [PX-0199]). Calio frames the turn and proposes the disclosure.
- **The CFO's gate.**
  - Every capital order (`gtf_next`, `join_rr_jv`, `pw_wb`) passes Mitchill's payback and return gate [PX-0199][PX-0272].
  - He can veto on four grounds: the dividend or the debt path [PX-0081][PX-0353]; carrying an unselected engine; aggressive terms [PX-0318]; booking upside before it is proven [PX-0311][PX-0350].
- **The President's vetoes.**
  - Eddy can veto on technical grounds: durability not proven before entry into service [PX-0128]; parts and capacity short of the fleet's needs [PX-0123].
  - In engine terms, he vetoes a `gtf_next` that overlaps the upgrade's first years. Strain is the engine's stand-in for engineering resources (`objectives.md` §3): -0.34 for a 2028 launch, -1.12 for 2026 (inference).
- **The CEO decides.** Calio takes the final call on every RTX capital commitment, under his rule: set the safety and durability constraint first, then optimise [PX-0035].
- **Tie-breaks:**
  - The fleet beats a new engine: "bending the AOG curve" comes first [PX-0080].
  - "If you miss a cycle" [PX-0071] beats "we'll cross that bridge" [PX-0276] only on visible demand [PX-0109].
  - A rival's discount never moves the answer [PX-0055].

### Typical tensions

1. **The next cycle against the plan.** Calio fears missing a cycle "for decades" [PX-0071][P-1347]. Mitchill has no centreline engine in the plan and wants the OE-loss model revisited first [PX-0202][PX-0275]. Both agree the next engine is an evolved GTF [PX-0067][PX-0244].
2. **Deleveraging against investment.** Debt goes back to pre-ASR levels before buybacks [PX-0353][P-0669]. Yet both keep about $10B of E&D and capex [PX-0102], "an and, not an or" [PX-0109]. A new engine competes with deleveraging, not with the dividend (inference).
3. **Airbus engines against fleet lift.** Eddy leans to fleet lift [PX-0123]. Calio balances jointly with Airbus [PX-0099][PX-0110]; Mitchill trades the two openly [PX-0315].
4. **Dates against cash.** Calio's operating dates slip: the AOG decline "moved out" [PX-0098][PX-0104]. Mitchill books nothing before "a few more reps" [PX-0311]. Trust the CFO's cash, and discount the CEO's dates (inference).

### How this team turned the doctrine into decisions (2024–25)

- **Franchise defence by product, not a new engine.**
  - The GTF Advantage was certified [PX-0087].
  - Its durability is back-ported into the fleet as a 2026 kit [PX-0088][PX-0106], and the kit is charged for [PX-0100][P-1363].
  - The aim is to hold about 40% of the A320neo [PX-0058].
- **The return bar becomes "responsible bets".**
  - Invest only once long-term demand is visible [PX-0109][PX-0010].
  - Assume NGSA in the mid-2030s [PX-0093][P-2058].
  - Advantage engineering "will start to shift to other priorities" [PX-0351].
- **Dividend first, then deleveraging.** Buybacks wait for debt [PX-0081][P-0686]; $37B has been returned since the merger [PX-0097].
- **No launch-style pricing.** "We're not in the early entry phase" [PX-0055][P-1333]. The next platform is where the OE model gets renegotiated [PX-0068][P-0774]. Catalog prices rise by double digits [PX-0092].
- **Cuts losses.** It ended a failing fixed-price programme with a $575M charge [P-1342].
- **Narrowbody only** [PX-0027][PX-0127].
- **Keeps its crisis numbers.** The reserve has held [PX-0358][PX-0074], and the reset cash target too [PX-0108][PX-0357].

### Per-turn ExCo deliberation script

1. **Calio frames.** "Control what you can control" [PX-0020]. Three questions:
   - Is the upgrade booked?
   - Has an airframer disclosed NGSA or fps for this round, and on which engine?
   - What has CFM/GE committed: ducted, RISE, a LEAP upgrade?

   Read `brief` and the `gtf_base` and `credibility` status (`objectives.md` §7).
2. **Eddy proposes.**
   - `gtf_upgrade` if it is not booked: +1.76 in round 1, +1.15 in round 2 [engine]. Block D already doubled the removal interval [PX-0116].
   - `gtf_next` only into an airframer's selection, launched in its year with the durability programme intact [PX-0128].
   - Standard terms with pass-through pricing [PX-0117]. No `pw_wb`: "single aisle focused" [PX-0127].
   - He reports the pacing parts and AOG counts [PX-0123][PX-0131].
3. **Mitchill tests.**
   - The cash by year and the low end [PX-0284][PX-0312].
   - The fit: `gtf_next` is $4.5B over 6 years, about an eighth of the self-funded envelope [PX-0268].
   - The debt path [PX-0353] and the partners' share [PX-0299].
   - He runs `whatif` with and without the selection, and with the next round's cancel.
   - His threshold: the PV break-even odds (0.20 / 0.29 / 0.76 by round) [engine], plus a cancel written into the next round's orders.
4. **Calio tests demand and durability.**
   - Is the demand visible [PX-0109]? Do standard terms and high volume work [PX-0009]? Is durability mature at entry into service [PX-0073]?
   - The team's hedge bar: P(NGSA names `pw_gtf2` this round) ≥ about 0.3 (inference: the PV break-even of 0.20, plus Calio's need to see demand). It sits below the doctrine's 0.45 because of "miss a cycle" [PX-0071].
   - An assigned-objective premium is taken only inside the $1B cap (`objectives.md` §6).
5. **Decide and speak.**
   - Calio decides. Write the cancel into the next round's plan.
   - Disclose: "GTF durability upgrade committed. Pratt & Whitney will launch `gtf_next`, sole source, standard terms, in any round an airframer names `pw_gtf2`."
   - Never speak for an airframer's rates or dates [PX-0062]. The CFO gives ranges [PX-0212].

### By round

| Round | Default orders | Flips when | Team vetoes |
|---|---|---|---|
| **1 (2026–2030)** | `gtf_upgrade` (+1.76). No `gtf_next`. Disclose the conditional offer | NGSA or fps disclosed on `pw_gtf2`: `gtf_next` in its year, 2030 if it says "this round" (+1.75 against -1.14). NGSA odds ≥ 0.3: hedge in 2030. An airframer signals UltraFan and RR offers `jv_pw`: join, if P ≥ about 0.2 (break-even 0.18) | Aggressive terms. `pw_wb`. `gtf_next` before 2029 alongside the upgrade. Join plus `gtf_next` aimed at the same NGSA (+7.93 against +12.14; -1.86 against +1.75) |
| **2 (2031–2035)** | Cancel an unselected round-1 `gtf_next` (+1.03 against -1.85). Book U if it was missed (+1.15; the last round that meets `credibility`). Launch into a disclosed NGSA in its year (2033: +1.42 against -0.41) | Undisclosed hedge only in 2035 and at odds ≥ 0.3 (break-even 0.29). Join on the same test (0.19) | Carrying any hedge into round 3. A 2033 hedge without a disclosure (break-even 0.46) |
| **3 (2036–2045)** | Do Nothing | A disclosed NGSA on `pw_gtf2` (2037: +0.99 against +0.33 on CFM, +0.62 on the open fan) | Any undisclosed launch (break-even 0.76; no cancel). A launch for fps alone (+1.52 against +1.54) |

### Reactions

- **CFM/GE launches its ducted engine.**
  - This is the real threat: NGSA 2030 on it leaves us -1.14 and no GTF engines from its entry into service [engine].
  - The team answers with product, not price [PX-0058][PX-0076]: the upgrade if not booked, the disclosed offer, and the hedge if the NGSA odds reach 0.3.
- **CFM/GE launches the RISE open fan.**
  - Read through durability: "You can go continue to chase efficiency ... run your engines hotter" [PX-0095].
  - It cannot enter service before 2045, so an open-fan NGSA leaves us +0.48 to +0.62 and the GTF base to 2044–45 [engine]. That is a "longer run" for the GTF [PX-0056] (inference).
  - No counter-launch without a disclosure.
- **CFM/GE takes share with the LEAP upgrade.**
  - Match it with ours: -0.67 alone becomes +1.09 [engine]. Hold about 40% on time on wing [PX-0058][PX-0084].
  - The GEnx package takes Rolls-Royce's 787 share, not ours: Do Nothing.
- **An airframer asks for aggressive terms.**
  - Refuse. Airbus already gains more from our standard-terms engine (+40.66) than from CFM's (+39.22) [engine].
  - Aggressive terms (+44.70 to Airbus) would beat UltraFan (+42.50), but they leave us at -1.97, below losing the selection (-1.14) [engine].
  - Offer durability, and the business-model talk for the next platform [PX-0068][PX-0070].

### How this team differs from the company default

- **A lower hedge bar** (about 0.3 against the profile's 0.45), from "miss a cycle" [PX-0071]. But the CFO insists the round-2 cancel is written in.
- **Debt before buybacks** [P-0669][PX-0353], where the doctrine treats buybacks as the shock absorber. A new engine therefore delays deleveraging (inference).
- **Charges for durability fixes** [PX-0100], and trades fuel burn for durability explicitly [PX-0095].
- **Durability-first vetoes in two seats**, the CEO's [PX-0073] and the President's [PX-0128], rather than one.

---

## 5. `calio-mitchill-eddy-2023`

### Members and roles

| Seat | Member | Role in 2023 |
|---|---|---|
| CEO seat | Christopher T. Calio | RTX President & COO, not CEO [PX-0019]. Hayes (context) made the CEO's calls: the $10B ASR [P-0602], "make the airlines whole" [P-0591], a late NGSA welcomed [P-1312] |
| CFO | Neil G. Mitchill | RTX CFO [PX-0284] |
| Operating | Shane G. Eddy | President of Pratt & Whitney [PX-0111] |

As a "today" team, Calio holds the CEO seat but plays his 2023 stances.

### Decision rule

**As recorded in 2023:**
- Hayes set capital returns and the compensation stance [P-0602][P-0591].
- Calio ran the recall: safety first, then customer impact [PX-0032][PX-0035].
- Mitchill sized the cost, netted the partners' 49% and phased the cash [PX-0299][PX-0297].
- Eddy chose daily between Airbus engines and the shops [PX-0123].

**In the game:**
- Eddy proposes; Mitchill gates; Calio decides.
- Mitchill's tie-break: one headline reset, then hold it [PX-0295].
- Eddy's tie-break: fleet lift first [PX-0123].

### Typical tensions

1. **Fleet lift against Airbus deliveries.** Eddy's bias was fleet lift [PX-0123]. In September 2023 RTX kept Airbus deliveries on plan [P-0159], later diverting to spares [P-1341].
2. **Capital returns against the rating.** The $3B buyback was kept through the charge [PX-0293][P-0600]. The ASR followed and the rating suffered [P-0602][P-1554].
3. **A shared optimism, not a check.** In the weeks before the July 2023 disclosure all three seats reassured:
   - Eddy: "not a surprise" [PX-0112];
   - Calio: a fleet-health inflection in H2 [PX-0024];
   - Mitchill: time-on-wing costs "already contemplated" [PX-0278] and $9B "very, very confident" [PX-0284].

   The script must force a downside case (inference).

### How this team turned the doctrine into decisions (2023)

- **Crisis doctrine, executed.**
  - Apology and safety first [PX-0032]. Scope first, then a dated number [PX-0288][PX-0030].
  - A $5.4B charge, $2.9B net after partners, delivered in line [PX-0303][P-1563].
  - The headline cash target reset once [PX-0295]. Partners kept close [PX-0037][PX-0301].
- **Upgrade over a new engine.**
  - The GTF Advantage was sold on durability proven before service [PX-0128][P-0759].
  - The next generation was "moving significantly to the right" [PX-0129][P-1312]. Enabling technology was funded with no launch expected [P-0757].
  - The OE-loss model was to be revisited first [PX-0275][P-1308].
- **Narrowbody, and the existing fleet first.** "Single aisle focused" [PX-0127][P-1313]. Even a sole-source A220 stretch came second to fixing the fleet [PX-0028].

### Per-turn ExCo deliberation script

1. **Calio frames the fleet.** "The fleet is not where it needs to be, period, full stop." [PX-0022] Set the safety constraint first [PX-0035].
2. **Eddy proposes.** `gtf_upgrade` now. "A known fix for a known issue" [PX-0111]. No new engine before durability is proven [PX-0128].
3. **Mitchill tests.** Is the cost scoped [PX-0288]? Is the capital return intact [PX-0293]? Is the upside proven [PX-0311]? He asks for the downside `whatif`, NGSA on CFM: -1.14 [engine].
4. **Decide.**
   - `gtf_next` only on a disclosed selection. The bar is about 0.45, the doctrine's; no hedge (inference from [PX-0129][P-1312]).
   - No join and no `pw_wb`.
5. **Speak.** Bad news first, with a number and a date [PX-0120][PX-0121]. Disclose the upgrade and "single aisle focused".

### By round

| Round | Default | Flips when | Vetoes |
|---|---|---|---|
| 1 | U (+1.76); Do Nothing otherwise | A disclosed NGSA or fps on `pw_gtf2`: `gtf_next` in its year | Hedge; aggressive terms; `pw_wb`; join (no evidence; inference) |
| 2 | Book U if missed; launch into a disclosed NGSA (2033: +1.42 against -0.41) | A 2035 hedge only at odds ≥ 0.45 | Any carry into round 3 |
| 3 | Do Nothing | A disclosed NGSA in 2037 | Any undisclosed launch |

### Reactions

- **CFM ducted:** defend the architecture [PX-0111][P-1325] and wait for a disclosure.
- **RISE:** extend the GTF [PX-0129]. The open-fan window keeps our base to 2044–45 [engine].
- **LEAP upgrade:** our upgrade, tracked as fleet configuration [PX-0116] (inference).
- **Aggressive ask:** pass-through pricing, not discounts [PX-0117].
- **`gtf_durability_crisis` inject:** this card is the record's closest match.
  - Upgrade, and compensate within the reserve.
  - Partners pay 49% [P-1563].
  - Airbus deliveries stay on plan [P-0159].

### How this team differs from the 2026 default

- **A higher hedge bar** (0.45 against 0.3), because the team plans for a late NGSA [P-1312].
- **Capital returns are held**, so an engine competes with buybacks [PX-0293].
- **The most prone to reassurance before the facts** [PX-0112][PX-0024][PX-0278]. Expect confident dates that slip.

---

## 6. `hayes-mitchill-leduc-2019`

### Members and roles

| Seat | Member | Role in 2019 |
|---|---|---|
| CEO seat | Gregory J. Hayes | UTC Chairman & CEO. **Context only**: not profiled; the card is built from Mitchill and Leduc, with UTC's recorded rules as context |
| CFO seat | Neil G. Mitchill | **Pratt & Whitney's** VP & CFO [PX-0181]. UTC's gate above him was Akhil Johri (context) [P-0734] |
| Operating | Robert F. (Bob) Leduc | President of Pratt & Whitney [PX-0177] |

### Decision rule

- **Leduc proposes:** sole-source bids [PX-0177], selective pricing [PX-0137] and capacity [PX-0179].
- **Mitchill tests Pratt's cash timing:**
  - stand-alone GTF cash breakeven in "the latter half of this 2020s decade" [PX-0181];
  - pay-at-shop-visit cash [PX-0182].
- **The UTC gate (context) decides:**
  - a board-set return hurdle [P-0731];
  - approval only well above the cost of capital [P-0734], against about 10% all-in on the GTF [P-1243];
  - a new engine kept out of the forecasts [P-0741].
- **In the game:** the CEO seat plays these context rules plus the company doctrine. Mitchill's later RTX-era rules apply to his seat only by inference.

### Typical tensions

1. **E&D against the harvest.** Leduc held E&D at about 6% of revenue: "Rather not repeat that mistake" [PX-0158]. UTC called the next 3–5 years a harvest [P-0350][P-1234] and kept E&D flat until a new programme [P-0377].
2. **Shareholder returns against a new engine.** The Raytheon merger promised $18–20B of returns [P-0355], yet was also sold as the scale to fund a big engine [P-0378].
3. **Volume against cash.** Leduc's ramp [PX-0174] fed negative engine margin, which Mitchill's breakeven date absorbed [PX-0181] (inference).

### How this team turned the doctrine into decisions (2016–19)

- **Offence onto Boeing, on its own terms.** The NMA offer was sole source or no bid, "accretive to the shareholder agenda" [PX-0177][P-0737]. Pratt spent little while Boeing waited [P-0739], and bid only where the geared architecture gave an edge [P-0740][P-1249].
- **Profitable share.**
  - "We don't feel the need to do those kind of deals anymore" [PX-0178].
  - It walked from IndiGo on price [PX-0180][P-0081], yet booked nearly 1,000 GTFs at Paris in 2019 [P-0082].
- **Capacity discipline.** Built for 65, committed to 63 [PX-0179][P-0079].
- **Durability lessons written down.** The two "golden rules" came after an entry into service that preceded durability testing [PX-0168][PX-0165].
- **Joint Ventures share risk, never core technology** [P-1233].

### Per-turn ExCo deliberation script

1. **CEO seat frames (context rules).** Does the move pass the board's hurdle [P-0731]? Is it where we have an architectural edge [P-0740]?
2. **Leduc proposes.**
   - `gtf_upgrade`: fewer removals pay on power-by-the-hour fleets [PX-0167].
   - Sole-source offers to both airframers [PX-0177], on standard terms [PX-0178].
   - He asks: is every supplier proven at rate [PX-0139]? Is testing complete and instrumented [PX-0168]?
3. **Mitchill tests.** When does the cash turn [PX-0181]? He wants `whatif` cash by year, the hedge cost (0.73 in round 1) [engine], and the `gtf_base` years.
4. **Decide.** Launch only into a disclosed, sole-source selection: the doctrine's 0.45 bar, so no undisclosed hedge (inference from [P-0711][P-0739]).
5. **Speak.**
   - Data against doubt: "The facts belied the press" [PX-0136].
   - No numbers that reveal the loss per engine [PX-0162].

### By round

| Round | Default | Flips when | Vetoes |
|---|---|---|---|
| 1 | U (+1.76). Disclose sole-source offers to Airbus and Boeing | Disclosed NGSA or fps on `pw_gtf2`: `gtf_next` in its year. fps on ours, +2.61 against +1.31, is this team's prize | Dual-source competition [PX-0177]; aggressive terms; hedging |
| 2 | Launch into a disclosed selection; cancel an unselected engine (doctrine default; no team record) | `pw_wb` only on a disclosed sole-source Re-engine with `whatif` > 0. Inactive at -1.43 (inference from [PX-0177]) | Compressed testing (inference from [PX-0168]) |
| 3 | Do Nothing | A disclosed NGSA in 2037 | Undisclosed launch |

### Reactions

- **CFM ducted:** "the geared fan will clearly be cheaper, fewer parts" [PX-0142]. Answer with the sole-source offer.
- **RISE:** no evidence in this era. Apply the engine values: an open-fan NGSA leaves us +0.48 to +0.62 [engine].
- **LEAP upgrade:** do not chase on price [PX-0180]. Answer with the upgrade, and win back later, as with Delta [PX-0169].
- **Aggressive ask:** refuse [PX-0178].
- **`join_rr_jv`:** sceptical. Integrated products need integrated teams [P-1240], and Leduc recalls Rolls-Royce's V2500 compressor trouble [PX-0150]. Join only after an airframer discloses UltraFan (inference).

### How this team differs from the 2026 default

- **The most offensive team:** it alone bid for Boeing, even widebody-class (the NMA) [PX-0177].
- **The least crisis-scarred.** It carries Leduc's durability optimism at entry into service [PX-0133][PX-0135]. Display it when disclosing `gtf_next` dates.
- **Protects E&D** [PX-0158]. It has no 2023 debt overhang, but faces a harvest-minded parent [P-0350].

---

## 7. Gaps

- **Eddy:** one event (June 2023), before the recall. The 2023 and 2026 ids assume he holds the seat; Deurloo's 2025 title is unexplained [P-1817].
- **Hayes and Johri** are context only, from company items, with no profile. Mitchill has two 2019 items, as Pratt's CFO.
- **Calio in 2023** was COO, so the 2023 card's CEO-level capital calls were Hayes's.
- **No team has evidence on:**
  - `join_rr_jv`;
  - the RISE open fan;
  - a widebody engine (beyond the NMA);
  - a hurdle rate after 2019 [P-1243].

  The thresholds for these are inference.
- **[engine] values** come from one run of the current rules. The LEAP-upgrade figures (-0.67 alone / +1.09 with our upgrade) match `calio.md` and `mitchill.md` after their audit. Re-run every turn.
