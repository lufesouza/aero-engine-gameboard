# fps three years late: business case, Airbus's response and the odds of a third player

**Question.** Using the attached dashboard (*Game.txt* snapshot and *Combined_Game_Board.py*):

- what does a 3-year fps delay do to the business case?
- how would Airbus respond?
- what are the odds that the delay brings Embraer or COMAC in as a third player?

The analysis draws on the two war games we played: fps on time (wg5-2045) and fps three years late (wg5-2045d).

**Delay assumed.** fps entry into service moves from 2041 to 2044. Everything else stays as in the snapshot: NGSA 2037, both Re-engines 2035, and the snapshot's costs, margins, prices and capture speeds.

**How it was done.**
- **Your board, solved headlessly.** Streamlit never runs; a mock harness executes your board's code.
- **Five AI analysts with adversarial checkers.** One each for the Airbus response, Embraer and COMAC, one independent re-derivation of the board numbers, and a completeness critic.
- **Corrections applied.** Every correction the checkers raised has been applied below.

All $ figures are your board's own measure: present value at 2026, $B, against the status quo (Boeing WACC 10.5%, Airbus 8%, debt penalty α = 0.30).

---

## Bottom line

1. **The fps business case flips from "indifferent" to "no".**
   - **Against Do Nothing:** fps (10-year ramp) goes from +$1.1B to −$2.5B.
   - **Against Airbus Delay Tactics:** from −$0.2B to −$3.5B.
   - **fps leaves every equilibrium.** The game moves from 0 pure and 17 near-Nash equilibria to 2 pure ones, and in both Boeing does nothing on the narrowbody.
   - **These are the board's mildest numbers.** They assume the delay is planned and the bill is deferred with it. If the slip is found after the bill is committed, fps is −$6.7B, or −$11.4B with a 30% overrun.
2. **The cause is share, not discounting.**
   - **Share costs $3.3B.** NGSA gets 7 years alone instead of 4, so Boeing re-enters at 20% share instead of 28%. At 1 point a year it never gets back to parity inside the window.
   - **Timing costs $0.3B.**
   - **NGSA's lead is the deciding variable.** fps is a pure equilibrium only when NGSA leads by 3 years or less. Your snapshot (a 4-year lead) is on the knife edge; the delay makes it 7.
3. **Airbus's best response is to do very little.**
   - **NGSA:** keep the 2030 launch and roughly 2037 entry into service. It never pays Airbus to slow down.
   - **Delay Tactics:** drop them. The delay does their job, and against a Boeing that doesn't launch they risk a fine worth about $12B in present value.
   - **Widebody:** the contest moves to widebody Chicken.
   - **Payoff:** Airbus gains $8–11B on the board.
   - **The catch:** almost all of that gain is narrowbody volume beyond what Airbus can build today. Airbus only collects it if it adds capacity. That one decision also sets the odds of a third player.
4. **A third player becomes more likely, but stays the less likely outcome.** These are judgements:
   - **Either Embraer or COMAC entering:** about 15% with fps on time, about 22% with the delay.
   - **Embraer as an independent entrant:** about 6% → 10%.
   - **COMAC as a real exporter:** about 11% → 15%.
   - **The more likely consequences:**
     - Airbus builds more and prices the scarcity.
     - 737 MAX volumes stay higher than the board assumes.
     - COMAC takes a large part of Boeing's share in China (about 45% → 50%). That hurts Boeing more than any exporting entrant.
5. **On the engine side, a Boeing that doesn't launch fps is a large gain for CFM.**
   - **CFM:** about +$38B relative to the snapshot, because the LEAP-powered 737 keeps Boeing's slot.
   - **Rolls-Royce:** loses its narrowbody entry (worth +$17B in the snapshot).
   - **Pratt & Whitney:** about −$4B.
   - **Embraer through CFM:** your engine board has a CFM "Partner Embraer" move but never evaluates it. When it is included, it is in every engine equilibrium.

---

## 0. Your board versus your snapshot

**Your snapshot came from a later build than the file you attached.**
- **Attached file:** charges the full $3B Boeing two-front strain whenever fps and a 787 Re-engine overlap. Solved as uploaded, it gives 1 pure and 13 near-Nash equilibria and misses 4 of your 17 cells.
- **Overlap-aware strain:** scaling the strain by how far the two development windows overlap reproduces the snapshot exactly. That means 0 pure and 17 near-Nash, the same cells, and every rounded yield. Boeing's windows overlap one year in five, so the strain is $0.6B.
- **Another fit:** a flat strain of $1.55B or less would also reproduce the snapshot, but the snapshot prints $3.00B.
- **What this changes:** only the cells where Boeing also re-engines the 787. Both strain rules give the same equilibria at 2044.

**The engine board is unchanged by the delay.** It uses the earlier of fps and NGSA (2037) as the narrowbody entry year, so a later fps has no effect. That is a decoupling in the board, not evidence that the engine makers are unaffected; section 4 corrects for it.

---

## 1. Business case

### 1.1 The numbers

| Boeing: fps 10-year Solo minus Do Nothing ($B) | fps 2041 (snapshot) | fps 2044 (delay) |
|---|---:|---:|
| Airbus NGSA + Re-engine A350, Boeing Do Nothing 787 | **+1.06** | **−2.53** |
| …with Airbus Delay Tactics (the slip test) | −0.24 | −3.49 |
| Boeing also re-engines the 787 | +0.24 | −3.13 |
| fps 7-year Solo instead | −0.11 | −3.40 |
| fps via Embraer ($100B, paid by Boeing) instead | −17.05 | −15.95 |

**At 2041 Boeing is indifferent, not committed.** +$1.06B is inside Boeing's tolerance band of 1 yield point, which is $1.3B. Your 2041 board also has no pure equilibrium, because the best responses chase each other in a loop:

1. Boeing launches fps.
2. Airbus answers with Delay Tactics.
3. Boeing switches to Do Nothing.
4. Airbus drops Delay Tactics, because they would now be naked.
5. Boeing launches fps again.

fps 10-year appears in 13 of the 17 near-Nash cells.

**Delay Tactics are what keep Boeing out at 2041. At 2044 the delay does that job by itself.**

| fps entry into service | 2037 | 2038 | 2039 | 2040 | **2041** | 2042 | 2043 | **2044** | 2045 | 2046 | 2047 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| fps 10-year minus Do Nothing | +9.68 | +7.29 | +5.02 | +2.93 | **+1.06** | −0.52 | −1.85 | **−2.53** | −2.29 | −2.07 | −1.87 |
| fps in any equilibrium | yes | yes | yes | yes | yes | yes | no | **no** | no | no | no |

After 2044 the value rises slightly. That is a quirk of the board: its evaluation window runs from 2026 to entry into service + 19, so a later fps is the same losing project, discounted further. On a fixed calendar window most of the rise disappears.

### 1.2 Why it flips

The case loses $3.59B between 2041 and 2044:

| Driver | $B |
|---|---:|
| Narrowbody profit, fps minus Do Nothing: +17.06 → +9.33 | −7.73 |
|   …the same cash, 3 years later | −4.42 |
|   …Boeing re-enters from a deeper hole | **−3.32** |
| The fps bill in present value: 12.36 → 9.16 | +3.20 |
| Debt penalty: 3.64 → 2.70 | +0.94 |
| **Net** | **−3.59** |

**What happens to share.** Under your rule, NGSA takes 3 points of share a year from 2037 until fps arrives, up to an 80% cap. fps then wins back 1 point a year:

| | Boeing share at entry into service | Boeing share at end of window |
|---|---:|---:|
| fps 2041 | 29% (28% before entry) | 48% (2060) |
| fps 2044 | 21% (20% before entry) | 40% (2063) |

Boeing never returns to the 50/50 balance point, so that slider has no effect.

**NGSA's lead decides it.** Holding fps at 2044 and moving NGSA:

| NGSA lead over fps | What happens to fps |
|---|---|
| 5 years | fps returns as a near-Nash equilibrium |
| 4 years | fps beats Do Nothing pairwise, but there is still no pure equilibrium (the snapshot sits here) |
| 3 years or less | fps is in every pure equilibrium |

The delay moves the lead from 4 years to 7.

### 1.3 It depends on what kind of delay this is

Your board books the entire fps bill as one payment in the entry-into-service year. A later fps therefore looks cheaper (+$4.1B). That only holds if the delay is planned and the spending moves with it.

| fps 10-year minus Do Nothing, by reading of the delay | fps 2041 | fps 2044 |
|---|---:|---:|
| Board: bill paid at entry into service (a planned later programme) | +1.06 | −2.53 |
| Slip found after the bill is committed on the 2041 schedule | — | −6.67 |
| …plus a 30% overrun paid at the new date (war-game rule: +10% per year of slip) | — | −11.39 |
| Bill spread over the 6 years before entry into service | −5.96 | −7.73 |
| Bill spread over the 9 years before entry into service | −10.18 | −10.86 |
| Spent over 9 years on the 2041 schedule, then a 3-year slip | — | −17.91 |

**The direction holds under every reading. Only the size changes.**
- **The positive 2041 case:** it exists only under the board's pay-at-entry rule.
- **If the board's own caption is right:** a stale caption in the board says the bill is spread over 9 years. If it were, fps would already be a no-go on time.

### 1.4 What would bring fps back at 2044

Each lever moves on its own. All levels are solved on the board.

| Lever (snapshot value) | Beats Do Nothing | Beats Do Nothing by $1B | Back in a **pure** equilibrium |
|---|---:|---:|---:|
| fps margin (25.64%) | 31.2% | 33.4% | **34.1%** |
| fps 10-year bill ($55.25B) | $45.0B | $40.7B | **$40.8B** |
| fps price ($55M) | $66.9M | $71.7M | **$73.0M** |
| Boeing's share recovery after entry (1 point/yr) | 1.85 | 2.30 | **2.28** |
| "fps via Embraer" bill paid by Boeing ($100B) | $45.0B | — | — |

**Breaking even is not enough.** Between "beats Do Nothing" and the pure-equilibrium level, the board cycles with no pure equilibrium. fps settles only once it beats Do Nothing even against Delay Tactics.

**"fps via Embraer" differs from the 10-year Solo only in its bill.** Its break-even is therefore the same $45B, less than half of the $100B the slider is set to.

### 1.5 What the game becomes

| 2044 equilibrium | Airbus | Boeing | Airbus $B | Boeing $B |
|---|---|---|---:|---:|
| A | NGSA + Re-engine A350 | Do Nothing 737 + Do Nothing 787 | +50.12 | −6.05 |
| B | NGSA + Do Nothing A350 | Do Nothing 737 + Re-engine 787 | +47.68 | −0.47 |
| *Snapshot, typical cell* | *NGSA + Delay Tactics + Re-engine A350* | *fps 10-year + Do Nothing 787* | *+39.21* | *−6.17* |

**Boeing's own payoff hardly moves** (−6.17 → −6.05). Do Nothing was already almost as good as fps. What the delay destroys is the option: the fps path back into the narrowbody market. Boeing is left at 20% narrowbody share from 2043.

**Boeing's best remaining move is to re-engine the 787 first** (equilibrium B). Winning the widebody Chicken is worth +$5.6B to Boeing and only +$2.4B to Airbus.

**Our war game reached the same end state.** In wg5-2045d, fps three years late:
- Boeing failed its own go/no-go test: −0.73 against a +$1B hurdle, and −4.71 in the slip test.
- Boeing re-engined the 787 instead.
- Airbus shelved the A350 Re-engine.

That is equilibrium B. The war-game calibration differs (NGSA 2035, a $30B fps bill), but measured as NGSA lead it also crosses the knife edge, going from 3 years to 6.

---

## 2. How Airbus would respond

The board solves for what pays. Airbus's behavioural profile and both war games show what Airbus actually tends to do. Probabilities are judgements; the board values are solved.

| Decision | Most likely response (probability) | Board value | Profile and war-game evidence |
|---|---|---|---|
| **NGSA timing** | Keep the plan: 2030 launch, ~2037 entry into service (65%). Slip for technology reasons (25%). Pull earlier (10%). A deliberate slowdown to save cash is unlikely. | Each year of NGSA slip costs Airbus $2.6–3.3B against a Boeing that does nothing, and $4.7–5.3B against fps. At a 5-year lead or less fps returns. Each year earlier pays about $3.8–4.1B. | Profile rule "own clock": don't wait for Boeing. Its default is the technology-ready year, entry 2035. Both war games launched NGSA in 2028 for 2035; the late-fps game noted "a delayed fps does not change it". Public plan, Farnborough July 2026: launch 2030, entry in the second half of the 2030s. |
| **Delay Tactics** | Drop them (95%, if NGSA holds). | Worth +$1.16B only if Boeing actually launches fps. Against a Boeing that does nothing they cost −$12.5B: the $48.3B naked fine is about $12.1B in present value, plus about $0.4B of operating cost. They pay only if Boeing launches with more than about 91% probability. | The war-game Airbus never used them in either game; they always fell below its $1B test and ran against its integrity pillar. The profile says stop Delay Tactics once fps is off. |
| **Widebody Chicken** (now the main contest) | Stay out once Boeing re-engines the 787 first (50%). Pre-empt with an A350 Re-engine (30%). Both re-engine (10%). Neither (10%). | A350 Re-engine alone +50.12; stay out +47.68; both +45.36. Pre-empting gains +1.8 if Boeing stays out but loses −2.3 if Boeing re-engines anyway. That fails Airbus's own test of beating Do Nothing by $1B against every plausible Boeing move. | Late-fps war game: Boeing, freed from fps, moved first (787 Re-engine in 2031); Airbus deferred, then shelved, which was worth +$0.33B. On-time game: Airbus pre-empted while Boeing was busy with fps. |
| **Price** (not on the board) | Sell the scarcity: hold or raise prices, with targeted campaigns at Boeing strongholds and at customers COMAC is courting. Broad price war unlikely. | +1 point of NGSA margin is worth about $3.8B. | Airbus priced up on slot scarcity before (neo premium) and is paid on EBIT and free cash flow; July 2026 brought a €5B buyback over 3 years. |
| **Capacity** (not on the board) | Hold rate 75 and price the scarcity (~40%). Add 5–10% timed to NGSA, with engine deals (~30%). Size NGSA's production system for about 100 a month (~20%). Absorb or partner (A220-500, the CSeries precedent) (~10%). | See below: the delay's whole gain to Airbus is volume above its current capacity. | Stated plan: 70–75 a month by end-2027, "stabilising at rate 75", gated by engines. 2026 reports: NGSA being prepared for about 100 a month (Aviation Week, June 2026; Air Data News, 7 Oct 2026; seen in search snippets only), and rate 83 under study for the A320neo (Leeham, August 2026). Airbus historically out-ramped Boeing and opened new lines in 2025–26. |

**These branches depend on each other.** If NGSA slips to 2039–2041, fps comes back, and Delay Tactics come back with it. The 95% "drop" assumes NGSA holds.

### The capacity decision links Airbus's response to the third-player question

The board gives Airbus 80% of a 2,000-a-year market from 2043. That is about 1,600 aircraft a year, against 900 a year at rate 75 or 1,200 at rate 100.

On the board, the delay is worth +$8.4B to Airbus against a launched fps (39.21 → 47.60). NGSA margin on volume above 1,200 a year rises by the same +$8.4B. **Every dollar of Airbus's delay gain is volume it cannot build today.**

| If Airbus… | Airbus captures the delay gain? | The gap left for others |
|---|---|---|
| Holds rate 75 and prices the scarcity | No: it earns price, not volume | Large: queues lengthen, the 737 sells more, an entrant has a case |
| Builds NGSA for ~100 a month, as the 2026 reports suggest | Yes, largely | Small: little demand is left unserved after about 2040 |

---

## 3. Odds of a third player

**Definition.** A third player is a company other than Boeing or Airbus that, by 2045, delivers a 150–210 seat single-aisle at 100 or more a year (5% of the board's market) to customers outside its home country, or that has committed funding to such a programme by 2035.

Entering as Boeing's partner (the board's "fps via Embraer" Joint Venture) does **not** create a third player.

### 3.1 How big is the gap, and can an entrant make money in it?

**The size of the gap depends on Airbus's capacity.** Board aircraft are treated as real aircraft a year: 2,000 a year is close to the OEMs' 2040s forecasts.

| Unserved demand 2037–2056 (aircraft) | fps 2041 | fps 2044, launched | Boeing Do Nothing (the 2044 equilibrium) |
|---|---:|---:|---:|
| Airbus at rate 75 (900/yr) | 7,720 | 11,040 | 12,860 |
| Airbus at ~100/month (1,200/yr) | 1,920 | 5,040 | 6,860 |
| Airbus at ~110/month (1,320/yr) | 480 | 2,700 | 4,520 |

- **The board overstates the gap.** In the late-fps war game Boeing still holds 32% in 2045, so the 2045 gap above 1,200 a year is about 150 aircraft, not 400.
- **The 737 already exceeds the board's Boeing slot.** Boeing built 447 737s in 2025 and is cleared to 47 a month, above the 400 a year the board allows Boeing.
- **Part of the overflow becomes queues.**

**Entrant economics, on the board's conventions** ($48M price, 12% margin, 10% WACC, a $15B programme; NPV in $B):

| Case | fps 2041 | fps 2044 | Boeing Do Nothing |
|---|---:|---:|---:|
| Bill paid at entry in 2038, Airbus capped at 1,200 a year | −2.78 | −0.51 | +0.42 |
| Embraer-realistic timing (entry 2042), bill paid at entry | −2.44 | −0.49 | — |
| Same, but bill spread over 2034–41 | −4.31 | −2.36 | −1.44 |
| The 737 at rate 47 absorbs part of the overflow | — | −1.45 | −1.35 |
| Airbus capped at rate 75 (900 a year) | +1.68 | +4.03 | +4.95 |

**The delay improves an entrant's case by about $2B, but Airbus's capacity moves it more than the delay does.** With realistic spending, an entrant needs either Airbus to stay at rate 75 or a protected home market.

COMAC's case doesn't hinge on this: its development spending is sunk and its capital comes from the state.

### 3.2 Embraer

**Capability.**
- **Size:** market value about $13B (August 2026). FY2025 revenue $7.6B, adjusted operating profit $0.66B.
- **Investment today:** about $0.4B a year.
- **Track record:** the E2 cost $1.7B and came in under budget.
- **What a clean sheet would cost:** a 150–210 seat aircraft costs $10–25B, so partners would have to fund roughly two-thirds to four-fifths.
- **Credit:** Fitch upgraded Embraer to BBB in September 2026.

**What it says and does.**
- **Studies under way:**
  - "Studies for a new cycle of products… commercial jet or business jet" (May 2026).
  - Leeham (January 2026) reports a 180–240 seat design being explored, and Embraer's research and technology director said in June 2026 that a single-aisle is "one of our potential products".
  - The CEO said in October 2025 that the market has room for "three or four" manufacturers (FT, via secondary sources).
- **Partners:** talks reported with Saudi Arabia's PIF, Korea, Japan, Turkey and India, all at an early stage; nothing is funded.
- **History of waiting for Boeing:** in 2011 Embraer waited for Boeing's choice before deciding, then built the E2. Boeing walked away from the Joint Venture in 2020, and arbitration settled in 2024.
- **Airbus's warning:** Faury told Embraer in June 2026 to "think twice".
- **No delay trigger:** Embraer's 2016 rule of entering only if the incumbents leave the segment applies to aircraft of 104–150 seats, and a Boeing that does nothing keeps the 737 there. That rule is not a trigger for the delay.

| Embraer path | fps 2041 | fps 2044 |
|---|---:|---:|
| Independent 180–210 seat clean sheet with sovereign or industrial partners, launched by 2035 (**third player**) | ~5% | ~8% |
| Smaller 150–170 seat step above the E195-E2 (counts only above 150 seats) | ~1–2% | ~2–3% |
| **Embraer becomes a third player** | **~6%** | **~10%** |
| Boeing's partner: Joint Venture or buy-back (not a third player) | ~10% | ~12% |

**Money is the binding constraint, not demand.** The delay roughly doubles the opportunity but not the ability to fund it.

### 3.3 COMAC

**Where it stands.**
- **The aircraft:** the C919 (158–192 seats) has been in service since 2023 on Chinese certification only.
- **Output, well below plan:**
  - Deliveries were 10–13 in 2024 and 15 in 2025, against a 2025 target cut to 25.
  - 2026 is tracking at about 25–28.
  - COMAC targets 150 a year by 2027–28 and 200 by 2029, backed by about $6B of new state capital.
- **Orders:** over 1,000, almost all Chinese. AirAsia confirmed purchase talks in September 2025, and Malaysia Airlines is evaluating the aircraft.
- **European validation:** EASA expects 2028–31, and test flying reportedly found no major hardware issues (July 2026).
- **Exposure to US parts:**
  - The US suspended LEAP-1C engine licences from May to July 2025.
  - In October 2026 Reuters reported, citing unnamed sources, that the US is capping the parts licences it issues to COMAC.
  - China's own CJ-1000A engine is expected around 2027–28.

| COMAC path | fps 2041 | fps 2044 |
|---|---:|---:|
| EASA-validated C919 exported at 100+ a year outside China by 2045 (**third player**) | ~7–11% | ~9–15% |
| Funded, export-oriented new single-aisle by 2035 (**third player**; no study is cited, C929 widebody competes for engineers) | ~5% | ~7% |
| **COMAC becomes a third player (either path; the two paths overlap)** | **~11%** | **~15%** |
| COMAC supplies 40% or more of China's single-aisle deliveries by 2045 (**not** a third player, but the bigger effect) | ~45% | ~50% |

**What binds COMAC is production, US parts, and certification, not demand.** The delay mostly gives Beijing a stronger reason to steer Chinese orders to COMAC and Airbus Tianjin.

### 3.4 Combined, and who bears the risk

| | fps 2041 | fps 2044 |
|---|---:|---:|
| **Embraer or COMAC becomes a third player** (judgement; they compete for the same gap, so slightly lower than independent odds) | **~15%** | **~22%** |
| COMAC takes a large share of Boeing's China business | ~45% | ~50% |

**An exporting entrant mostly fills demand Airbus cannot build.** It is chiefly an Airbus risk and a check on Airbus's delay gain.

**COMAC taking China hits Boeing.** China is about 20% of global single-aisle demand. Losing about 6% of the board's 2,000-a-year market wipes out the 2041 fps case (+1.06 → 0); that is about 30% of China. At 2044 it deepens the loss: −2.53 becomes −3.46 at 10%.

**Signals to watch.** Each one moves the odds:
- **Airbus:** an NGSA production-rate decision, and a line or engine deal above rate 75.
- **Embraer:** money signed with PIF, Korea or Japan; an engine selection; investment stepping up above about $0.4B a year rather than share buybacks.
- **COMAC:** C919 deliveries above 60 in 2028 and 100 in 2030; EASA validation; firm orders outside China; whether the US formalises the parts caps.
- **Boeing:** whether a narrowbody launch shows up around 2031–34, or Boeing stays silent. Boeing's CEO said in 2026 that the next narrowbody is "moving to the right".

---

## 4. Engine makers

The engine board ignores whether Boeing launches fps. To represent the delay's end state, Boeing's slot is set to the 737 on LEAP at 20% share.

| Engine board, pure equilibrium ($B) | CFM/GE | Pratt & Whitney | Rolls-Royce |
|---|---:|---:|---:|
| Snapshot (fps 2041, fps engines from all three, Boeing 50%) | −62.65 | +18.34 | +17.25 (UltraFan NB Solo) |
| fps launched late, Boeing at ~30% of the new-generation market | −57.56 | +22.29 | +9.35 |
| Boeing Do Nothing: 737 stays on LEAP at 20% | **−24.97** | +14.30 | **0** (Do Nothing on narrowbody) |

**CFM gains about $38B from Boeing not launching fps.** Rolls-Royce loses its narrowbody entry, and Pratt & Whitney gives up about $4B.

**CFM's "Partner Embraer" move.** It exists in your code but is never among the 16 CFM moves the board evaluates, because the board keeps only the first four combinations for each base move.
- **When it is included:** it enters every pure engine equilibrium, as Ducted + Partner Embraer + a GEnx upgrade.
- **Its value:** +$2.5B to CFM in the snapshot, and +$0.6B if Boeing does nothing.
- **What it doesn't show:** it is a fixed +5 points of share, so it says nothing about the delay. It does show that your board would favour an engine maker backing Embraer.

In both war games, Pratt & Whitney cancelled its next-generation geared turbofan in 2031, and CFM never used its Embraer lever.

---

## 5. Limits to keep in mind

- **Bill timing.** The board pays the whole programme bill in the entry-into-service year (§1.3). This drives both the positive 2041 case and the "cheaper delay".
- **Evaluation window.** The window runs from 2026 to entry into service + 19.
  - It moves Boeing's Do Nothing payoff with the fps slider (−$0.13B between 2041 and 2044).
  - On a common calendar horizon the delay costs Boeing $3.9–4.8B, not $3.6B. The verdict holds for any horizon up to 2089.
- **No third player, capacity, price, or move order.** The board lets Airbus build 1,600 a year and has no Embraer or COMAC. Who moves first in the widebody Chicken is taken from the war game.
- **The naked fine and the "fps via Embraer" bill are slider settings.** The fine is $48.3B and is discounted to the fps date. "fps via Embraer" is $100B, which is the slider's maximum.
- **Board build.** The uploaded build is not the one that produced the snapshot (§0). The engine board doesn't read Boeing's launch decision, and CFM's Embraer move is never evaluated.
- **War games.** Each is one run, calibrated differently (NGSA 2035, a $30B fps bill), and neither had a third airframer.
- **Web evidence.** Some 2026 facts were seen only in search snippets: NGSA at about 100 a month, the October 2026 parts-licence caps, and some Embraer quotes. They are flagged where used.

---

## Files

- `inputs/`: your dashboard and snapshot, as received.
- `analysis/`: the headless solver (`harness.py`) and one script per result. `run_all.sh` reproduces every number above; results are in `analysis/results/`.
- `review/`: the full outputs of the four analysts and their adversarial checks, with all citations, plus the critic's notes. File paths inside them point to a scratch area that is not kept.
