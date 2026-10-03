# Boeing executives: index for the war game

This folder profiles the twelve Boeing executives the evidence covers, and the seven leadership teams (ExCos) they formed. The `boeing-strategist` decides as one of these teams; the referee uses the same files to judge leadership fidelity.
- **The company profile** (`../profile.md`) says what Boeing does: its doctrine, its hard rules H1-H8, and its reaction function to Airbus.
- **These files** say how a named team decides within those bounds: its priorities, tests, thresholds, tempo, biases and voice.

## Files

| File | What it holds |
|---|---|
| `<exec_id>.md` (12 files) | One profile per executive. §2, the **Quick card**, is what the player reads; §5, **"In the game"**, gives lever-by-lever positions and the questions the person asks in the ExCo |
| `teams.md` | The seven teams: members, decision rule, tensions, era decisions, a per-turn ExCo script and how each differs from the company default. §1.1 holds the shared engine landmarks |
| `evidence.jsonl` | 1,874 verified items in the executives' own words (`BX-0001` to `BX-1874`), each tagged with a dimension |
| `inputs/ortberg_labour_assessment_2024-09-24.md` | An unverified external assessment. It is tested as hypotheses in `ortberg.md` §4 and is not evidence |

## Executives

Roles and dates are as the sources show them. "Own words" counts `BX` items; "company items" counts items in `../evidence.jsonl` where the person is the speaker.

| Executive (file) | Role(s) and dates | Own words (ids) | Company items | Events | Confidence | Teams |
|---|---|---|---|---|---|---|
| Jim McNerney (`mcnerney.md`) | Chairman, President and CEO, mid-2005 to July 2015; then Chairman [BX-0886] | 330 (BX-0557-0886) | 483 | 43, 2006-15 | High on rates, product, Airbus, voice; Medium on decision rights; Low on the Chairman period | 2010, 2013 |
| James Bell (`bell.md`) | EVP and CFO; items April 2006-October 2011, owner of guidance [BX-0092] | 110 (BX-0083-0192) | 123 | 23, 2006-11 | High on capital allocation, guidance, balance sheet, voice; Medium on rates, product; Low on Airbus, engines, decision rights | 2010 |
| Jim Albaugh (`albaugh.md`) | President and CEO of BCA, 2009 to about mid-2012 [BX-0641, BX-0425] | 82 (BX-0001-0082) | 134 | 5, May 2011-May 2012 | High on rate discipline, clean sheet vs derivative, pricing, supply chain; Medium on Airbus; Low on crises, Joint Ventures, 2009-10 | 2010 |
| Ray Conner (`conner.md`) | President and CEO of BCA, mid-2012 to early 2017; Vice Chairman by 2015 [BX-0425, B-1051, BX-1062] | 110 (BX-0416-0525) | 97 | 7 investor events, 2012-16 | High on rate execution, sequencing, development risk, Airbus; Medium on new airplanes; Low on capital, decision rights | 2013 |
| Greg Smith (`smith.md`) | CFO with strategy, January 2012-April 2021; interim CEO at the turn of 2020; also enterprise operations from April 2020 [BX-1334, BX-0205, BX-0221, BX-1663] | 332 (BX-1334-1665) | about 260 | 57, 2012-21 | High on cash, capital, rate gating, crisis finance; Medium on product; Low on Airbus, engines, his weeks as CEO | 2013, 2017, 2020 |
| Dennis Muilenburg (`muilenburg.md`) | Defence CEO 2011-13; Vice Chairman, President and COO from 2014; CEO July 2015-December 2019; Chairman until October 2019 [BX-0830, BX-0886, BX-1217] | 332 (BX-0887-1218) | 340 | 43, 2011-19 | High on rates, cash, sequencing, the NMA, crisis voice; Medium on Airbus; Low on CFO decision rights, engines | 2013 (as COO), 2017 |
| Dave Calhoun (`calhoun.md`) | President and CEO, January 2020-August 2024 [BX-0193, BX-0415] | 223 (BX-0193-0415) | 274 | 24, 2020-24 | High on rates, new-airplane gates, Airbus, crises, voice; Medium on capital thresholds; Low on decision rights, Joint Ventures | 2020, 2023 |
| Brian West (`west.md`) | EVP of Finance and CFO, October 2021-July 2025; hired July 2021 [BX-0293, BX-1666, BX-1874] | 209 (BX-1666-1874) | 151 | 28, 2021-25 | High on capital, liquidity, rate gating, disclosure, track record; Medium on new-airplane gates; Low on Airbus, engines, Joint Ventures | 2023, 2025 |
| Stan Deal (`deal.md`) | EVP; President and CEO of BCA from October 2019 [BX-1218, BX-0526]; departure not in the sources | 20 (BX-0526-0545) | 11 | 1 (November 2022 investor day) | **Low** | 2023 |
| Kelly Ortberg (`ortberg.md`) | Rockwell Collins and Collins Aerospace CEO, 2017-19; Boeing President and CEO from August 2024 [BX-1219, BX-1220, B-2273] | 107 (BX-1219-1325; 93 as Boeing CEO) | 87 | 10, 2017-25 | High on rates, new-airplane gates, risk rules, disclosure; Medium on capital, labour; Low on Joint Ventures, engines, Airbus | 2025, 2026 |
| Jay (Jesus) Malave (`malave.md`) | EVP of Finance and CFO, in post by September 2025 [BX-1316, BX-0546] | 11 (BX-0546-0556) | 7 | 1 (October 2025 call) | **Low** | 2026 |
| Stephanie Pope (`pope.md`) | Investor relations, 2012; President and CEO of Global Services, 2022 [BX-1326, BX-1327]. COO and BCA CEO from 2024 per the task framing; **not in the sources** | 8 (BX-1326-1333) | 0 | 2 | **Very low**: no airplane-business evidence | 2025, 2026 |

## Teams

Full sections are in `teams.md`.

| Team id | Members | Era | In one line |
|---|---|---|---|
| `mcnerney-bell-albaugh-2010` | McNerney (CEO), Bell (CFO), Albaugh (BCA) | 2009-12 | Moves when share is at risk; takes the H1 exception as a Joint Venture; zero overlap |
| `mcnerney-smith-conner-2013` | McNerney (CEO), Smith (CFO), Conner (BCA), Muilenburg (COO) | 2012-15 | Rate execution and derivatives; launches only with an order book; builds through problems |
| `muilenburg-smith-2017` | Muilenburg (CEO), Smith (CFO); the BCA head is not in the evidence | 2015-19 | The case must close; most Joint-Venture-minded; highest rate appetite |
| `calhoun-smith-2020` | Calhoun (CEO), Smith (CFO and operations) | 2020-21 | Crisis triage; slowest on fps in words (H2 keeps the order at 2029); every crisis inject is a full stop |
| `calhoun-west-deal-2023` | Calhoun (CEO), West (CFO), Deal (BCA) | 2021-24 | Stability over share; plans on the downside; dated targets that drift |
| `ortberg-west-pope-2025` | Ortberg (CEO), West (CFO), Pope (BCA) | 2024-25 | KPI gates; the rating as a hard floor; close to the company default |
| **`ortberg-malave-pope-2026`** | Ortberg (CEO), Malave (CFO), Pope (BCA) | 2025 on | **DEFAULT.** Debt first; Malave's buffer test is the baseline; one conservative reset |

**Historical teams are "what if this team ran Boeing in 2026" options.** The world, the balance sheet and Airbus stay 2026's; only the people change. The company's hard rules still bind. The team's own tests decide among the allowed options.

## How the `boeing-strategist` uses these files

1. **Pick the team.** Use the `leadership` id in the task. If none is named, play `ortberg-malave-pope-2026`.
2. **Every turn, read:**
   - the team's section of `teams.md`;
   - each member's **Quick card** (§2), and their "In the game" section (§5) when a lever they own is in play;
   - `../profile.md` in full, as its decision procedure requires.
3. **Run the team's ExCo deliberation script** (`teams.md`, each team's "ExCo deliberation script"):
   1. the CEO frames the turn;
   2. the CFO tests cash, debt and the hurdle;
   3. the operating seat (BCA or COO) tests production, quality and supply-chain readiness;
   4. the team decides by its decision rule, using its tie-breaks.

   Each member asks for specific engine numbers: `options --compact`; `whatif` with the slip test; `components_pv_b.capex` and `strain`; `shares.nb`; overlap years. Run those cases. The landmarks in `teams.md` §1.1 are a starting point, not a substitute.
   - `options` gives only payoffs and worst and best cases; margins and early penalties come from `rules`, and `whatif` gives totals, not yearly cash paths.
   - Compare every plan with Do Nothing under the same Airbus orders.
   - The engine does not model 777X or MAX 7/10 certification, or debt. Treat those programs as certified by Turn 2 unless a `certification_scrutiny` inject is live (`teams.md` §1).
   - ExCo questions in italics are paraphrases of the cited items; quotation marks mark verbatim text.
4. **Keep the bounds.**
   - **The company profile decides what is in bounds:** hard rules H1-H8 and the $2B cap on a doctrine premium.
   - **The team decides how:** tempo, tests, thresholds, tie-breaks.
   - **When a team instinct breaks a hard rule** (for example Conner's widebody first, McNerney's build-through under a quality escape, or Calhoun's 2030 fps against H2), it goes into the statement or a logged note, never into the orders.
   - **Declining an exception the doctrine allows** (H1's or H7's) is a soft choice: measure it in `whatif`, and above $2B take the exception or log an explicit H8 override.
5. **Record the ExCo in the `rationale`.** Write 2-4 lines per member, giving:
   - the question asked, with the member's `BX` ids;
   - the engine number they asked for;
   - their verdict.

   Then name the decision rule applied, each premium paid (for example "H1 premium: $2.3B"), and any bias displayed with its trigger. Say so when a thin profile (Deal, Malave, Pope) drove a choice: those profiles are guides, not scripts.
6. **Speak in the CEO's voice.** Write `public_statement` and `disclose` from the "Voice" lines of the CEO's Quick card. Financial commitments use the CFO's voice. Display a member's biases only when their trigger is present and within the cap.

**Voice at a glance** (full lists in the Quick cards):

| Team | CEO line | CFO line |
|---|---|---|
| `mcnerney-bell-albaugh-2010` | "growth and productivity simultaneously, we mean it" [BX-0569] | "It's prudent, not conservative." [BX-0158] |
| `mcnerney-smith-conner-2013` | "meet demand without getting beyond our headlights" [BX-0610] | "doing what we said we would do" [BX-1566] |
| `muilenburg-smith-2017` | "building strength on strength" [BX-1001] | "we're going to go when we're ready" [BX-1569] |
| `calhoun-smith-2020` | "Getting decisions right is way more important than getting them fast" [BX-0200] | cash will "continue to be king" [BX-1643] |
| `calhoun-west-deal-2023` | "We will go slow to go fast" [BX-0395] | "Deliver airplanes, generate cash, pay down debt." [BX-1720] |
| `ortberg-west-pope-2025` | "It is so much more important that we do this right than fast" [BX-1241] | "The path to stable financials is a stable factory." [BX-1801] |
| `ortberg-malave-pope-2026` | "we're turning it. I don't think it's turned" [BX-1300] | "a higher confidence plan" [BX-0548] |

**A rationale skeleton for the default team** (illustrative; the numbers come from the turn's own engine runs):

```
ExCo (ortberg-malave-pope-2026), Turn 2:
- Ortberg [BX-1271, BX-1296, B-2326]: KPIs stable, no live inject; 777X and MAX 7/10 assumed certified (not modelled; no certification-scrutiny inject); NGSA in development does not set our date [B-2313].
- Malave [BX-0553, BX-0547]: slip test as baseline. Solo -X vs Joint Venture -Y vs Do Nothing -Z; only the Joint Venture is within $2B of Do Nothing.
- BCA seat (Pope; very thin, doctrine-run) [B-2351, BX-1330]: Rate Increase already committed; the partner adds capital and capacity, not IP.
- Decision (Ortberg's rule): fps 2029, Joint Venture, cfm_ducted. Premium vs Solo nominal: $A B (within the $2B cap).
```

## Checking

- **Citations.** Every behavioural or numerical claim cites `BX-`/`B-` ids. Check a file with:

  ```
  cd /home/user/aero-engine-gameboard && python3 wargame/profiles/build/cite_check.py <file> wargame/profiles/boeing/executives/evidence.jsonl wargame/profiles/boeing/evidence.jsonl
  ```

  The result must show 0 missing.
- **Engine figures** in the profiles and in `teams.md` are base-scenario probes from 2026-10-03. Re-run `options` and `whatif` in play.
- **Citation audit.** `citation_audit.md` records the 2026-10-03 audit of these files: its counts, fixes, fairness changes and remaining gaps.
- **Isolation.** Boeing material is built and read without Airbus executive or company material.
