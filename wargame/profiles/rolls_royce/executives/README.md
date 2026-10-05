# Rolls-Royce executives and leadership teams

These files let the `rolls-royce-strategist` play Rolls-Royce (RR) as a named leadership team, and let the referee judge whether it did. Each profile describes professional conduct only: what the person said and did as an RR executive, drawn from RR's own calls and investor days. Executive evidence ids are `RX-####` (`evidence.jsonl` here); company evidence ids are `R-####` (`../evidence.jsonl`).

## Executives

| Executive (file) | Role(s) and dates | Own words (ids) | Events | Confidence | Teams |
|---|---|---|---|---|---|
| Tufan Erginbilgic (`erginbilgic.md`) | CEO & Executive Director from January 2023. Evidence from 23 February 2023 [RX-0038] to 31 July 2025 [RX-0138] | 110 (RX-0030 to RX-0139) | 7: six results calls and the November 2023 Capital Markets Day | High on capital allocation, pricing and guidance; medium on UltraFan and narrowbody (words, no launch decision); low on Joint Venture terms and CFM/GE | 2023, 2026 |
| Helen McCabe (`mccabe.md`) | CFO & Director from about November 2023. Evidence from 28 November 2023 [RX-0211] to 31 July 2025 [RX-0263] | 61 (RX-0211 to RX-0271) | 5 | High on the capital frame, guidance and aftermarket economics; low on engine-launch economics | 2026 |
| Panos Kakoullis (`kakoullis.md`) | CFO & Executive Director from about 2021. Evidence from 5 August 2021 [RX-0164] to 3 August 2023 [RX-0206]; served under Warren East, then Erginbilgic | 57 (RX-0154 to RX-0210) | 6 | High on balance-sheet repair, guidance and LTSA mechanics; none on engine launches, UltraFan or partners | 2022, 2023 |
| Chris Cholerton (`operations.md`) | President, Civil Aerospace, from the start of 2018 [RX-0015]; President, Defence Aerospace, in November 2016 [RX-0001]. Last evidence 13 May 2022 | 29 (RX-0001 to RX-0029); 8 of them attributed or probable | 2 | Low to medium | 2022 |
| Rob Watson (`operations.md`) | President, Civil Aerospace, by 28 November 2023 [RX-0277]; head of Rolls-Royce Electrical in June 2021 [RX-0272]. Last evidence 28 November 2023 | 27 (RX-0272 to RX-0298); 4 of them attributed | 2 | Low to medium | 2023, 2026 |
| Eric Schulz (`operations.md`) | President, Civil Aerospace, in 2016; printed as "Former President" at the 16 November 2016 investor day [RX-0140] | 14 (RX-0140 to RX-0153) | 1 | Low; historical reference only | - |
| Warren East (no file; context only) | CEO, mid-2015 to end-2022 [R-0942, R-1561] | 0 RX; 377 company items with him as speaker (R) | 28 | Not profiled | 2022 |

**Attribution.** Twelve Civil items come from transcript turns labelled "Unknown Executive". `operations.md` marks each as attributed **(attr.)** or probable **(prob.)**.

**Evidence base.** 298 own-words items in all: CEO 110, CFOs 118, Civil presidents 70. Nothing is later than July 2025.

## Leadership teams

| Team id | CEO | CFO | President, Civil Aerospace | Era | Status |
|---|---|---|---|---|---|
| `east-kakoullis-cholerton-2022` | Warren East (context only) | Kakoullis | Cholerton | Post-COVID repair: disposals, deleveraging, investment tilted away from Civil [RX-0159, RX-0172] | What-if |
| `erginbilgic-kakoullis-watson-2023` | Erginbilgic | Kakoullis | Watson | The first turnaround year: repricing, investment grade first [RX-0056, R-0865] | What-if; **id changed** from `erginbilgic-kakoullis-cholerton-2023` |
| `erginbilgic-mccabe-watson-2026` | Erginbilgic | McCabe | Watson | The turnaround delivered: net cash, distributions, UltraFan as an option [R-0032, RX-0102] | **DEFAULT** |

**Why the 2023 id changed.** Cholerton's evidence ends in May 2022 [RX-0004]. The only Civil president the evidence shows in 2023 is Watson, at the November 2023 Capital Markets Day [RX-0277]. Kakoullis's last turn (August 2023) comes before Watson's first (November 2023), so this team is a composite; `teams.md` explains.

**The default team's dates.** Erginbilgic's and McCabe's evidence ends in July 2025, and Watson's in November 2023. The 2026 team assumes that all three still hold their seats.

## How the strategist uses these files

1. **Pick the team.** Use the workflow's `leadership` argument (e.g. `{"rolls_royce": "erginbilgic-kakoullis-watson-2023"}`) or tell the referee. With neither, play `erginbilgic-mccabe-watson-2026`. A historical team plays "that team running Rolls-Royce in 2026": the same game and engine, with the team's own thresholds and voice.
2. **Read in this order:**
   - the company doctrine, hard rules and decision procedure (`../profile.md`, §9), and the assigned objective (`../objectives.md`);
   - the team's card in `teams.md`: decision rule, tensions, ExCo script, lever thresholds by round, reactions;
   - each member's Quick card and "In the game" section.
3. **Each turn, run the team's ExCo deliberation** inside the profile's §9 procedure, after `options` and `whatif` and before weighing PV against doctrine. The CEO frames, the CFO tests cash, the hurdle and the downside, the Civil president tests maturity, strain and capacity, and the team rule decides. Keep the shared hard rules and the $3B per-turn cap on doctrine premiums.
4. **Record it** in the rationale: "ExCo (<team id>): CEO …; CFO …; Civil …; decided …; doctrine premium $X B; ids".
5. **Speak in the team's voice.** Public statements use the CEO's voice lines from his Quick card. Disclosures follow the team's style, from "conditional, few and binding" (2026) to "not before 2030" (2023) and "a 2030s opportunity, in partnership" (2022).
6. **Re-run the numbers.** The engine figures in these files are snapshots from a scratch `five-player-2045` run (tag [5p] or [T1]/[whatif]), not evidence. Re-run `options` and `whatif` every turn.

The referee reads the same files to score leadership fidelity: did the orders, the deliberation and the voice match the team given?

## Gaps

- **Thin before 2021.** Only Schulz and Cholerton's Defence turns (November 2016) predate 2021. Nothing covers 2017-2020, so there is no first-hand account of the Trent 1000 crisis or of COVID as they happened.
- **No narrowbody launch decision.** No team has launched or named a partner. Solo against the Joint Venture, the narrowbody hurdle and the reactions to CFM/GE and P&W moves are words plus inference.
- **Seats after the evidence.** The default team's seats after mid-2025 (Watson's after November 2023) are assumed. Kakoullis's exact departure date and the February-August 2023 Civil president are not in the evidence.
- **Warren East is not profiled.** The 2022 team plays his seat from his company-level statements only.
- **Stale id elsewhere.** `erginbilgic.md` (header), `operations.md` (the Cholerton intro) and `../../build/ENGINE_EXEC_SYNTH_ADDENDUM.md` still name `erginbilgic-kakoullis-cholerton-2023`.
