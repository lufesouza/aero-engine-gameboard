**Completeness critique of the four analyses, in priority order**

Note: my input was cut off partway through the COMAC caveats, and the board-verification analysis text never arrived. I judged those two from the scratch outputs instead (wf/verify/*, wf/adv2/*, wf/adv_comac/*). The COMAC board re-run is byte-identical to the original solve. SCRATCH = /tmp/claude-0/-home-user-aero-engine-gameboard/95fa875c-ca9d-5564-a6e5-4c9b461d7e56/scratchpad. The new arithmetic is in SCRATCH/wf/critic/cap900.py and cap900.json.

**P1 – fix before writing the answer**

1. **The analyses read the board's units differently, and that decides the vacuum.**
   - Fact: the brief and vacuum.json treat 1,200/yr as "100/month". The Airbus analysis maps 1,200 to rate 75. The COMAC analysis compares real 737 output (447 in 2025) with board units. The Embraer and COMAC analyses set the third-player bar at "100/yr = 5% of 2,000".
   - Fact: if 1,200 means 100/month, then rate 75 (900/yr) leaves $39.7B of Airbus's +$50.1B Boeing-Do-Nothing gain above capacity. On the Airbus mapping the figure is $20.0B (critic/cap900.json; airbus_cells.json).
   - Fact: on the Airbus mapping, Airbus's reported NGSA plan of about 100/month (Aviation Week 9 Jun 2026, Air Data News 7 Oct 2026; snippets only) equals 1,600 board units. That is the board's full 80% share, so the vacuum after 2043 would be zero.
   - Fix: pick one mapping and say so. My judgement is that board units are close to real 2040s units, because 2,000/yr is near the OEM average forecast of about 1,680-1,710/yr cited in the COMAC analysis. Show the vacuum at 900, 1,200 and 1,600, and re-run the opportunity stages of both the Embraer and COMAC odds on that basis.

2. **The Airbus response and the third-player odds are one question, but nobody links them.**
   - Fact: all of Airbus's board gain from the delay is volume above capacity. Against fps with Delay Tactics, the gain is +8.39 (39.21 → 47.60, BRIEF). Volume above 1,200 rises by +8.38 (7.95 → 16.33, airbus_cells.json). Without Delay Tactics the gain is +8.69, and volume above 900 rises by exactly +8.69 (27.36 → 36.05, cap900.json).
   - Judgement: if Airbus keeps to rate 75 and prices the scarcity (its modal 50-60%), it captures none of the delay's volume, and that unserved demand is the opening for an entrant. If it builds, it captures about $8.4B and closes the gap.
   - Fix: present a joint table of Airbus capacity branch × third-player odds. Drop the Airbus headline that says holding capacity "is enough to keep an entrant negative". The check refuted it: the modal "hold 75" branch leaves the entrant at +0.42.

3. **Capex timing (one lump at entry into service) is the board's biggest limitation, and it is applied unevenly.**
   - Fact, fps 10-year minus Do Nothing:

     | Spending pattern | fps 2041 | fps 2044 |
     |---|---|---|
     | Lump at entry into service (board) | +1.06 | −2.53 |
     | Spread over 9 years | −10.18 | −10.86 |
     | Spread over 6 years | −5.96 | −7.73 |

     Source: adv2/a4.json.
   - Fact: if the slip happens after launch, with money already spent on the 2041 schedule, the result is −17.91. With a 30% overrun it is −24.15 (a4.json; verify/check_misc.json).
   - Fact: the entrant NPVs in the Airbus analysis and vacuum.json use the lump convention. The Embraer check used spread spending and got −2.36 at fps 2044 and −1.44 with Boeing Do Nothing (adv/entrant_spread.json).
   - Fix: tell the user the snapshot's +1.06 "knife-edge go" exists only under the lump convention. Separate "planned later programme" (−2.53) from "slip after launch" (−17.9 / −24.1). Apply one realistic-spending sensitivity to both fps and the entrants.

4. **The business case uses a widebody setting the other analyses say is unlikely.**
   - Fact: the table assumes Boeing does nothing on the 787. The Airbus analysis (50%) and the delayed war game (787 Re-engine in 2031) both predict Boeing re-engines.
   - Fact: in that setting fps 10-year minus Do Nothing is +0.24 (2041) and −3.13 (2044) with overlap strain. With flat $3B strain it is −0.33 and −3.69 (dash/run_all.log lines 24, 39, 69, 94).
   - Fix: add this row.

5. **The fps via Embraer break-even is wrong in four places.**
   - Fact: $52.9B came from a straight-line extrapolation between $90B and $100B (analysis2.py lines 82-83). The board solve gives −1.94 at $52.93B and 0.00 at $44.96B (check_misc.json). That matches the fps 10-year capex break-even of $44.96B (adv2/a2.json), as it should, because the two moves differ only in capex.
   - Fix: change it to about $45B in BRIEF, report_part1 (which says "≈$53B"), and the Embraer and COMAC analyses.

6. **The third-player odds are on different bases and are never combined, though the user asked "Embraer or COMAC".**
   - Fact: Embraer's 6 → 11% is the probability of an independent launch by 2035; on the exports test it is about 1 → 2%. COMAC's 7 → 9% is exports. COMAC's 17 → 23% is mostly its new-programme prong (13 → 18%).
   - Fix: one table, combined assuming independence (judgement; the true figure is lower because the two compete for the same overflow):

     | Test | fps 2041 | fps 2044 |
     |---|---|---|
     | Material exporter, ≥100/yr by 2045 (lead with this) | ≈8% | ≈11% |
     | Funded new programme by 2035 (leading indicator) | ≈18% | ≈26-28% |

     Source: cap900.json. The delay effect is about +3pp on the exports test.

**P2 – probabilities that do not follow from the evidence**

7. **COMAC's new-programme prong (13 → 18%) has no supporting evidence.**
   - No COMAC next-generation single-aisle study is cited. The C929 takes engineering until 2035, there is no next-generation engine, the C919 is not EASA-validated, and it delivered 15 aircraft in 2025.
   - It still scores above Embraer, which does have single-aisle studies (Embraer R&T director, 12 Jun 2026) and partner talks.
   - Fix: lower it (judgement: about 5-10%) or justify it, since it drives the 17 → 23% headline.

8. **COMAC's China share (45 → 52%) contradicts itself.** The text says the gain happens "largely regardless of fps timing", then assigns +7pp to the delay. Make the two consistent.

9. **Boeing's decision timing is wrong in both entrant analyses.**
   - Fact: on the board, a 10-year programme with fps 2041 launches in 2031. With fps 2044 it launches in 2034 if planned, or in 2031 with a slip, which is how the war game modelled it (wg5-2045d/drivers.md line 3).
   - Fix: Boeing's no-go is visible before 2035 either way. Remove Embraer's stage-4 cut (0.65 → 0.55), its engine-stage rise (P&W cancelled its next-generation GTF in both war games), and the 2036-37 rationale behind COMAC's +5pp.

10. **The Joint Venture is treated two ways.**
    - Fact: the Embraer analysis re-prices it on war-game terms: +2.21 (2041) and −0.83 (2044), against Solo at +1.06 and −2.53 (emb_jv.json). On those terms it beats Solo at 2041 too, so the delay is not what creates the preference.
    - Fact: the COMAC analysis calls it "dominated" at $100B. That figure is a slider set at its maximum (range 20-100, board.py line 843).
    - Fix: use one treatment, and soften the 10 → 12% Joint Venture path.

11. **No odds are conditioned on Airbus's own branches.**
    - Fact: an NGSA slip to 2039-41 (Airbus gives it 25%) brings fps back (analysis2.json) and shrinks the vacuum.
    - Fact: the Airbus capacity split (50/25/10/15) is contradicted by the 2026 rate-100 reports.
    - Fix: at minimum, state which way each branch moves the odds.

**P3 – war-game use, the vacuum, and consistency**

12. **The war games say nothing about third players, and their dates differ from the board's.**
    - Fact: neither game had COMAC. The CFM "Embraer partnership" was "not committed" in both (final_report.md lines 71-72).
    - Fact: war-game fps was 2038 on time and 2041 late, with NGSA in 2035, LEAP-derivative engines on both aircraft, and $30B fps capex. The board has fps 2041 → 2044 and NGSA 2037.
    - Fix: reconcile in years of NGSA lead. The war game goes from 3 to 6 years and the board from 4 to 7, so both cross the knife edge.
    - Fact: the delayed war game kept Boeing at 38.4% (2040), 32.3% (2045) and 25.0% (2050), with Airbus at 67.7% in 2045 (wg5-2045d/final_report.md lines 84-86). The board has Airbus at 78-80%. On the war-game path the 2045 overflow above 1,200 is about 154/yr, against 360-400 on the board (2000 × 0.677 − 1,200). Show this as a sensitivity.

13. **The "vacuum" comes from the share rule, not from real lost demand.**
    - Fact: if Boeing's 737 can deliver 564/yr, the entrant NPV falls from −0.51 to −1.45 at fps 2044, and from +0.42 to −1.35 with Boeing Do Nothing (adv2/a4.json).
    - Fix: tell the user the real-world result is longer queues, higher prices and more 737s. Use realistic entrant timing (entry into service 2042-43, not 2038) across all three analyses.

14. **Window and count inconsistencies.**
    - Airbus capacity value at fps 2044: use 16.33 (Airbus's own 2037-2056 window), not 16.82 (airbus_overflow.json, which runs to 2063).
    - On a common horizon the delay costs Boeing −3.9 to −4.8, not −3.59 (check_misc.json, common_horizon). The verdict holds for any horizon up to 2089.
    - Snapshot near-Nash count: 13 cells with fps 10-year (8 alone, 5 with a 737 rate increase), 1 with fps 7-year and 3 with Do Nothing (Game.txt lines 118-205). This replaces "12" in BRIEF and "12 + 2" in the Airbus check.

15. **The strain rule cannot be identified from the snapshot.**
    - Fact: flat strain anywhere from $0 to $1.55B also reproduces the snapshot exactly (adv2/a1.json, flat_strain_ok). The 2044 equilibria are the same under flat and overlap strain.
    - Fix: drop "only overlap reproduces". Say the conclusions hold either way; only the 787 Re-engine rows depend on the strain rule.

**Still missing for the user**

16. **Business case.**
    - Boeing's board value barely moves (yield 95.44 → 95.34, verify/check2.json). What it loses is the option and a 20% share.
    - Its best move after the delay is a 787 Re-engine first (−0.47 against −6.05).
    - Break-even is not the same as fps returning to equilibrium. fps only becomes a pure equilibrium again at a margin of 34.1% or more, or capex of $40.8B or less (a2.json). The 31.2% break-even margin is not enough.

17. **Who bears the risk of a third player.** An entrant exporting at scale mostly fills Airbus overflow that Airbus cannot build (the Embraer analysis). COMAC taking China hits Boeing: losing 6.2% of the market erases the 2041 case (comac/board_comac.json). Say both in one sentence.

18. **Missing non-third-player path.** Airbus absorbing an entrant (the CSeries precedent; 15% in the Airbus analysis) is not among the Embraer paths. The A220-500 also overlaps Embraer's 150-170 seat option.

19. **Weak sourcing to flag.** These come from snippets or single sources:
    - NGSA at about 100/month
    - Commerce capping COMAC parts licences (Reuters, 1 Oct 2026, unnamed sources)
    - no C919 deliveries in September 2026 (Forecast International)
    - "about 60% of FCF", which is a J.P. Morgan estimate, not an Airbus commitment
    - the Morgan Stanley note on the "75 thereafter" wording, which could not be verified
    - afm.aero's ">1,100 deliveries by 2029"
    - 44bn yuan of state investment in COMAC (Bloomberg)
    - Embraer CEO's "three or four" manufacturers (FT, via secondary sources)

    The Airbus analysis's "Boeing's free balance sheet" claim is judgement with no Boeing evidence behind it.

20. **Model limitations to state together.**
    - capex paid as one lump at entry into service
    - a window of entry into service + 19 years
    - no third player, capacity, price or move order
    - a 20% share floor for Boeing
    - 2,000/yr is above OEM forecasts
    - the $48.32B naked fine and the $100B Joint Venture price are slider settings
    - CFM's Embraer move is never evaluated
    - NGSA's entry year is an input, not a choice
    - the uploaded build is not the build that produced the snapshot

    Naming: no "Milk_787", "Sabotage" or "Delay fps Bottleneck/Poaching". Write "Delay Tactics (supply bottleneck / talent poaching)".