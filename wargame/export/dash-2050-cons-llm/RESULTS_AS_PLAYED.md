# dash-2050-cons as played (spoiler: open only after your replay)

The original game, played on 14 October 2026 by twenty AI agents (an executive committee and a Board for each
company) with the game master's engine. Values are ΔPV against the status quo, $B, present value at 2026.

## Final values (after round 4, 2050)

| Company | ΔPV ($B) |
|---|---|
| Boeing | -0.83 |
| Airbus | +14.09 |
| CFM/GE | -28.04 |
| Pratt & Whitney | -1.65 |
| Rolls-Royce | +11.03 |

## Orders each round (non-default fields) and value after the round

| Round | Company | Orders | ΔPV after the round |
|---|---|---|---|
| 1 (2030) | Boeing | hold everything | -0.83 |
| 1 (2030) | Airbus | `ngsa`: `launch`, `ngsa_engine_code`: `7`, `a320_plan`: `alt` | +14.09 |
| 1 (2030) | CFM/GE | `genx`: `upgrade_genx9` | -27.07 |
| 1 (2030) | Pratt & Whitney | `gtf2_solo`: `launch_if_selected` | -0.97 |
| 1 (2030) | Rolls-Royce | `ultrafan_nb_solo`: `launch_if_selected` | +11.77 |
| 2 (2035) | Boeing | hold everything | -0.83 |
| 2 (2035) | Airbus | `ngsa_engine_code`: `7`, `a320_plan`: `alt` | +14.09 |
| 2 (2035) | CFM/GE | `ducted`: `launch`, `partner_embraer`: `launch` | -28.04 |
| 2 (2035) | Pratt & Whitney | `jv_with_rr`: `commit` | -1.65 |
| 2 (2035) | Rolls-Royce | `jv_with_pw`: `commit` | +11.03 |
| 3 (2045) | Boeing | hold everything | -0.83 |
| 3 (2045) | Airbus | `a320_plan`: `alt` | +14.09 |
| 3 (2045) | CFM/GE | hold everything | -28.04 |
| 3 (2045) | Pratt & Whitney | hold everything | -1.65 |
| 3 (2045) | Rolls-Royce | hold everything | +11.03 |
| 4 (2050) | Boeing | hold everything | -0.83 |
| 4 (2050) | Airbus | `a320_plan`: `alt` | +14.09 |
| 4 (2050) | CFM/GE | hold everything | -28.04 |
| 4 (2050) | Pratt & Whitney | hold everything | -1.65 |
| 4 (2050) | Rolls-Royce | hold everything | +11.03 |

## What each company expected and said

### Round 1 (2030)

Events: NGSA (Airbus) launched in 2030; Airbus adopts the Alt plan: A320 lines kept longer through the NGSA ramp-up; NGSA engine selection: RR, PW and CFM; P&W GTF2 (Solo) launched in 2030; pw_solo: conditional launch triggered by ngsa; RR UltraFan NB (Solo) launched in 2030; rr_solo: conditional launch triggered by ngsa; GEnx (CFM/GE) launched in 2030.

**Boeing.** Expected scenario: S2 and S5 at even odds. Airbus launches NGSA, and the odds are about even that it also launches the A350 Re-engine in the same round. Those odds come from doctrine §7, an inference: Airbus re-engines cheaply [B-2446]. My own record is Low on Airbus. I read S6, the risk case, as Malave's slip-leg baseline; for Do Nothing it equals S2 (-0.64). Do Nothing scores -1.95 on the blend. Best grid plan in it: On the S2/S5 even-odds blend, the best plan is fps: hold + 787 Re-engine, at -1.535 against Do Nothing's -1.95. That is +0.41, inside ε, so it is a tie, and Do Nothing wins it on doing less [BX-1239], the higher-confidence plan [BX-0548] and the higher worst column (-3.26 against -5.74). On S2 alone, fps: hold + 787 Re-engine is best at +2.67. Premium: $0.41B. Board: approve.

Public statement: "A few years ago we said we had three jobs to do before anything else: stabilize the factories, finish the airplanes we'd started, and repair the balance sheet. The 777X is in service, the MAX 7 and 10 are delivering, and our net debt is back where it was before the hard years. I'm proud of this team for that. We still work on safety and quality every day, and that doesn't stop.

People ask me whether now is the time for the next airplane. We will do a new airplane when the market and the technology and we're ready. We're ready on our end. The other two aren't there yet, and I'm not going to launch an airplane to win a news cycle. When we do launch, you'll get an entry-into-service date we know we can meet, with room built into it, and not before.

On the 737 we're holding at 57 a month. The line is stable and the data is good, and the demand in front of us doesn't need another step right now. I'd much rather run a steady line than chase a number. On widebodies, the 787 is the most efficient airplane in its class. We'll keep investing in it and in Charleston.

Going slow is what let us go fast. It's so much more important that we do this right than fast."

**Airbus.** Expected scenario: S1, rivals hold. Boeing's own stated preconditions for a new airplane (a 20-30% gain, 'not before 2035', a repaired balance sheet) and our prior of no fps before the next round point to a hold this round [profile §7]. Working weights: S1 55%, S2 10%, S3 5%, S4 10%, S5 5%, S6 10%, S7 5%. A 737 Rate Increase is possible but is not a grid column, and we would not react to it. The ordered row is the best survivor in every column, so the call does not change the orders. Best grid plan in it: Raw best in S1: NGSA (A320 Alt plan) + A350 Re-engine at +15.83. It is deleted on rule 6 (two launches, a 5-year overlap), on peak cash ($6.674B against $5.2B) and on the Board's veto. Best surviving plan in S1, and the one ordered: NGSA (A320 Alt plan) + A350: hold, no Delay Tactics, at +14.09. It is also the best survivor in S2 to S7. Premium: $0.00B. Board: approve.

Public statement: "Our core principles of safety, quality, integrity, compliance and security will remain at the heart of all we do. Today Airbus launches its next-generation single-aisle aircraft, with entry into service planned in the second half of the 2030s. This is how we prepare the Airbus of the 2030s: on the clock of technology maturity, with a disciplined and controlled ramp-up. To serve our customers through the transition, we will keep the A320 family in production for longer on our proven lines while the new aircraft ramps up. We have invited CFM, Pratt & Whitney and Rolls-Royce to power the new aircraft, because robust, multi-source engine supply matters to our customers and to the ramp. We will fund the programme from our own cash generation, within our financial framework, and preserve our financial flexibility and a strong balance sheet. The A350 family, including the A350F, remains our widebody focus. Together with our European industrial base, our suppliers and our partners worldwide, we will continue to work with the whole industry for a tariff-free, zero-for-zero regime for civil aviation."

**CFM/GE.** Expected scenario: S1: rivals hold. On the public record, no programme is launched, no airframe has an engine code, and no rival NB engine or Joint Venture commitment exists. If anyone moves, S2 is the likeliest next column (an Airbus NGSA with CFM alongside a rival), but I'm not planning on selections nobody has made. Best grid plan in it: GEnx upgrade alone (genx: upgrade_genx9): S1 +0.78, the best row in S1, against 0.00 for hold. It is also the best plan in S3, S4 and S6. In S2 and S5 the best plan is Ducted + Partner Embraer + GEnx upgrade (-13.02 and -30.22). Premium: $0.00B. Board: approve.

Public statement: "Safety, quality, delivery and cost, always in that order. That's how we run this business, and it's how we made this call.

Here's what we know. The LEAP is flying on every 737 MAX and on the A320neo, and our job today is to deliver those engines on time and support that fleet. We'll keep at it with our suppliers, and with our partners at Safran.

Here's what we don't know: when the airframers will launch their next single-aisle, and what they'll want under the wing. That's really not for us to say. We don't have a birthright on that next order. So CFM will offer our engines to both airframers, and we will commit a new engine alongside a committed airframer.

RISE remains a technology programme we're all in on with Safran. The airframers will set the date for that architecture.

On the widebody, we're investing in a GEnx upgrade so the 787 fleet stays competitive for our customers.

It's that simple. Ain't that hard."

**Pratt & Whitney.** Expected scenario: S1: rivals hold in 2030. This is the modal column at 0.30 on my weights. My incrementalism bias puts the next single-aisle in the 'mid-next decade' [PX-0093], and I have discounted it, not relied on it. There is still about a 50% chance that NGSA launches this round (S2, S3, S5, S6). That is exactly why `hold` is not acceptable and `launch_if_selected` is. Best grid plan in it: In S1, `GTF2: hold` and `GTF2 Solo if selected` tie at 0.00, because `launch_if_selected` does not trigger and nothing is spent. Our order is a best plan in the expected column. It is also the best plan across all columns on my weights, Mitchill's and equal weights: expected −2.49 against hold's −9.99 on mine. Premium: $0.00B. Board: approve.

Public statement: "Control what you can control. The last few years on the GTF fleet were hard on our customers, and we own that. Time on wing and getting aircraft back in the air come first, ahead of any new engine.

Here is our commitment. In any round an airframer selects Pratt & Whitney for a new single-aisle, as sole source or alongside a partner, we will launch our next-generation geared turbofan that same round. It is planned to be ready six years from launch, so 2036 for a commitment made this year. Its durability will be proven before it enters service. That means time on wing ahead of fuel burn in the specification, life-limited parts at full life at entry into service, and no testing compressed to hold a date. We have learned our lesson from the prior iterations of the GTF.

We will offer it on standard terms, priced for value. We are not in the early entry phase. We are continuing the GTF Advantage hot-section durability kit across the A320neo fleet, also at standard terms. The dates and rates of any new aircraft are the airframer's to give, not ours."

**Rolls-Royce.** Expected scenario: S1, rivals hold (weight 0.30), is the single most likely column. More broadly I expect no Rolls-Royce selection this round: S1, S3, S6, S7, S8 and S9 together carry 0.90 on base weights. An airframer that launches in 2030 most likely goes to CFM or P&W, and the selection weight is 0.10 because nothing is announced. Best grid plan in it: In S1, 'UltraFan NB: hold' and 'UltraFan NB if selected' tie at +0.00 as the best grid plans. launch_if_selected weakly dominates hold across S1-S9: equal in six columns and +12.53 / +9.52 / +23.13 in S2 / S4 / S5. It is therefore the best plan on expected value (+1.37 base, +2.89 at selection 0.2), with a worst column of 0. Premium: $0.00B. Board: approve.

Public statement: "So, plainly. Rolls-Royce will launch UltraFan for a new narrowbody that selects us, in the round it selects us, where seven years of development fit before its entry into service. Entry into service no earlier than seven years from launch. We don't compress maturity for anyone. Partnership is our preference, not our need: the Joint Venture is open to Pratt & Whitney, and we commit the round they do. UltraFan widebody launches in the round a 787 or A350 Re-engine is announced, if it pays. Widebody is our core, and our Trent durability work continues. We won't do anything not profitable. I will say that categorically."

### Round 2 (2035)

Events: Pratt & Whitney commits to the Joint Venture; Rolls-Royce commits to the Joint Venture; P&W GTF2 (Solo) folded into the Joint Venture; RR UltraFan NB (Solo) folded into the Joint Venture; P&W-RR Joint Venture NB engine launched in 2035; Joint Venture engine ready 2036 (inherits a folded solo programme's schedule); CFM ducted engine launched in 2035; CFM-Embraer partnership launched in 2035.

**Boeing.** Expected scenario: S1 (rivals hold) for the narrowbody: S1, S2 and S4 differ by at most $0.49B on every non-Re-engine row. For the 787 Re-engine: S1 blended with S3 at 40% odds of an A350 Re-engine this round (Malave's finance read; Low confidence). On that blend, Do Nothing scores -1.41. S4 stays the buffer baseline, and for Do Nothing it equals S1 (-0.83). S2 is upside, and I don't plan on it. Best grid plan in it: On S1 alone, the best plan is fps: hold + 787 Re-engine (+1.17 against Do Nothing's -0.83). On my S1/S3 60/40 blend it scores -0.87 against Do Nothing's -1.41: +0.54, inside ε, about +0.18 after Malave's haircut. The tie goes to Do Nothing: doing less [BX-1239], the higher-confidence plan [BX-0548], the higher worst column (-2.29 against -3.93) and the smaller debt penalty. The Board's Downside rule (S3 -1.64 against -1.00) would veto the Re-engine anyway. Every fps row trails Do Nothing by $4.24B or more in every column. Premium: $0.54B. Board: approve.

Public statement: "Five years ago I said we'd do a new airplane when the market and the technology and we're ready. That's still the test, and I'll give you a straight read on it.

We're ready on our end. The factories are stable, the 777X and the MAX 7 and 10 are flying with customers, and the balance sheet is where it should be. The technology is moving too. There will be good new engines out there. The market case for us isn't there yet. So we are not launching a new airplane this year, and I'm not going to give you a date for one. Another company's schedule doesn't set ours. When we do launch, you'll get an entry-into-service date we know we can meet, with room built into it. We'll share the development risk sensibly with our partners. We won't take a fixed-price bet on it.

We turned the big ship. The job now is to keep it steady, not to swing the wheel to chase a headline.

On the 737 we're holding at 57 a month, on the gates we agreed with the FAA. Our customers want more airplanes than we're building, and I understand that. I'd rather give a customer an honest delivery date than run an unstable line.

On widebodies, the 787 is the most efficient airplane in its class. We'll keep making it better with our partners at GE, and we'll keep growing Charleston.

The financials will follow our production performance. I'd much rather be a month late than go a month early."

**Airbus.** Expected scenario: S1, rivals hold.  Why I expect a hold: - Boeing says it is 'ready on our end', but the market and the technology are not. - It promises an EIS 'with room built into it'. - It holds the MAX at 57 with idle slots, and it is investing in the current 787 at Charleston rather than a Re-engine.  Working weights: S1 55%, S2 15%, S3 5%, S4 10%, S5 5%, S6 5%, S7 5%. All seven columns stay plausible.  The ordered row is the best survivor in every column, so the call does not change the orders. Best grid plan in it: Raw best in S1: NGSA hold (A320 Alt plan) + A350 Re-engine, at +15.63. It fails Toepfer's peak-cash test ($6.674B against $5.2B in 2035-36), a binding soft veto, and the Board would veto it on liquidity. No override is available: the Board's review fails at -1.21 in S7, and I hold none against the Board.  The best surviving plan in S1, and the one ordered, is NGSA hold (Alt) + A350 hold, with no Delay Tactics and code 7, at +14.09. It is also the best survivor in S2-S7. Premium: $0.00B. Board: approve.

Public statement: "Our core principles of safety, quality, integrity, compliance and security will remain at the heart of all we do. Our next-generation single-aisle aircraft remains on track for entry into service in the second half of the 2030s. We are taking it through certification on the clock of maturity: no test will be compressed to hold a date, and no engine will enter service before it is mature. Our engine partners CFM, Pratt & Whitney and Rolls-Royce are maturing their engines for the aircraft, because robust, multi-source engine supply matters to our customers and to the ramp-up. That ramp-up will be disciplined and controlled. Through the transition, the A320 family continues to serve our customers on our proven lines, and we are securing the engines, structures and materials our own ramp-up needs. This is how we prepare the Airbus of the 2030s. We continue to fund the programme from our own cash generation, within our financial framework, and to preserve our financial flexibility and a strong balance sheet. The A350 family, including the A350F, remains our widebody focus. Together with our European industrial base, our suppliers and our partners worldwide, we will continue to work with the whole industry for a tariff-free, zero-for-zero regime for civil aviation."

**CFM/GE.** Expected scenario: S1, rivals hold. Airbus keeps code 7 on the NGSA (entry into service 2037), with CFM, P&W and RR all fitted. GTF2 is ready in 2036 and UltraFan NB in 2037. No Boeing fps this round, and no P&W-RR Joint Venture commitment. This is the column the public record supports. It does not count on any selection not yet made. Best grid plan in it: Ducted + Partner Embraer: -25.03 in S1 (yield 84.4%), against hold at -27.07. It is also the best plan in S3 (-30.91). Hold is best only in S2 (-38.62). Premium: $0.00B. Board: approve.

Public statement: "Safety, quality, delivery and cost, always in that order. That's how we run this business, and it's how we made this call.

Five years ago we said we'd commit a new engine alongside a committed airframer. Airbus has committed, and so have we. Together with our partners at Safran, CFM is launching a new single-aisle engine. It builds on the hot section and the durability lessons of the LEAP fleet, and it enters service when the testing says it's ready, not before. The dates and rates for that aircraft are Airbus's to give, not ours.

We're also teaming up with Embraer. It's open, it's not exclusive, and there are no terms to talk about today. CFM's engines stay on offer to every airframer. We don't have a birthright on anybody's next order. We have to earn it.

Here's what we know. Our first job is still the LEAP fleet flying today. We'll keep shop-visit material and time-on-wing kits ahead of the new-engine delivery rate, and we don't trade durability for fuel burn. Airbus has asked for long-term engine supply, and we'll work that through with them, jointly with Safran.

Here's what we don't know: how the next decade's market plays out, or when the airframers will want the next architecture. RISE remains a technology programme we're all in on with Safran, and the airframers will set the date for it.

It's that simple. Ain't that hard."

**Pratt & Whitney.** Expected scenario: S1, rivals hold (p 0.55). NGSA stays on code 7 and GTF2 is fitted alongside CFM and Rolls-Royce if it is ready by NGSA's EIS. No fps launches this round. Rolls-Royce does not match this round; on my reading it matches, if at all, after our commitment is on the public record (2045). In S1, hold + commit ties hold at −0.97. Best grid plan in it: In S1, `GTF2: hold` and `GTF2: hold + commit to JV` tie at −0.97. I submit hold + commit (row B). It equals hold in S1, S2 and S3 and is +2.35 ahead in S4, so it is weakly dominant on the grid and never below hold. Cancel rows are −18.62 in S1. Premium: $0.00B. Board: approve.

Public statement: "Control what you can control. The GTF fleet is still not where our customers need it to be, and we own that. Time on wing and getting aircraft back in the air come first, ahead of any new engine. We are continuing the GTF Advantage hot-section kit across the A320neo fleet at standard terms, and we will report progress as the share of the fleet in the latest configuration.

Our next-generation geared turbofan, launched in 2030 for the new Airbus single-aisle, is planned to be ready in 2036. Its durability will be proven before it enters service: time on wing ahead of fuel burn, life-limited parts at full life at entry into service, and no testing compressed to hold a date. If the test data tell us something we don't like, you will hear it from us first. We have learned our lesson from the industrial gaps on the GTF.

Today Pratt & Whitney commits to a narrowbody Joint Venture with Rolls-Royce. This adds to our engine on the new Airbus aircraft; it is not a hedge against it. The Joint Venture forms only when Rolls-Royce commits, and Rolls-Royce has not done so. The terms are these: risk, investment and revenue shared, and both partners on one new engine. Each partner keeps its own technology. Our gear and our core stay ours, in work-share and in intellectual property. What each side brings counts in the share split and is not licensed. Nothing changes in the engine we are certifying.

Our next-generation engine is available to any other new single-aisle whose entry into service it can meet, on standard terms, priced for value. We are not in the early entry phase. The dates and rates of any new aircraft are the airframer's to give, not ours."

**Rolls-Royce.** Expected scenario: S1: rivals hold (my weight 0.55). NGSA keeps code 7 and flies CFM + P&W + RR from 2037. P&W continues GTF2 Solo without joining the Joint Venture. Boeing launches no fps, and no widebody Re-engine is announced. Weights S1-S6: 0.55 / 0.15 / 0.05 / 0.10 / 0.10 / 0.05. Best grid plan in it: 'UltraFan NB: hold' and 'UltraFan NB: hold + commit to JV' tie at +11.77 in S1. Hold + commit is chosen: it equals hold in five columns and beats it by +2.29 in S4, so it is the best expected plan on every weight set (+9.86 on mine, +10.64 on the Board's). Premium: $0.00B. Board: approve.

Public statement: "So, plainly. UltraFan narrowbody is in development for NGSA, ready in 2037, seven years from launch. We pace it to maturity and we don't compress it for anyone. If maturity needs longer, we will say so. Support through partner shops is being built now, in place before entry into service. Partnership is our preference, not our need. NGSA already carries Pratt & Whitney and Rolls-Royce, so our Joint Venture commitment is now on the record. It forms when Pratt & Whitney joins, on terms that credit the technology each side brings. There is no change of strategy. Widebody is our core, and our Trent durability work continues. Any UltraFan widebody or Trent upgrade comes to the Board in the round a Re-engine is on the record, and only if it pays after the cost of running two programmes. We won't do anything not profitable. I will say that categorically."

### Round 3 (2045)

Events: none.

**Boeing.** Expected scenario: S1 (rivals hold) for the narrowbody. S3 equals S1 on rows with no fps and sits $0.10-0.15B below it on fps rows.  For the 787 Re-engine: S1 blended with S2 (an A350 Re-engine) at Malave's 35% odds (Low confidence). On that blend Do Nothing scores -0.95.  S3, the risk case, stays the buffer baseline and is not blended in. Best grid plan in it: The best plan is fps: hold + 787 Re-engine, at -0.75 against Do Nothing's -0.95 (+0.19 at 35% odds; about +0.01 after Malave's haircut). That is inside ε. The tie goes to Do Nothing on four counts: - doing less [BX-1239]; - the higher-confidence plan [BX-0548]; - the higher worst column (-1.16 against -1.97); - no added penalty. The Board's Business case test would veto the Re-engine anyway.  The best fps row, 10-year at Renton + Re-engine, scores -2.78 expected, which is -1.83 against Do Nothing. The 10-year at Renton alone is -1.78. Premium: $0.19B. Board: approve.

Public statement: "I've said for a long time that we'll do a new airplane when the market and the technology and we're ready. That's still the test, and you'll get the same straight read on it.

We're ready on our end. The factories are stable. The 777X and the MAX 7 and 10 have been flying with customers for years. The balance sheet is where it should be. The technology is ready too: there are good, mature engines out there from more than one maker. The market case for our next airplane isn't there yet. On paper it looks closer than it was. I've looked hard at why, and I'm not going to tell you something has turned when it hasn't. So we're not launching a new airplane this year, and I'm not going to give you a date for one. Another company's schedule doesn't set ours.

When we do launch, you'll get an entry-into-service date we know we can meet, with room built into it. We'll share the development risk sensibly with our partners, and we won't take a fixed-price bet on it. In the meantime we're keeping our engineering teams and our suppliers ready, because readiness doesn't keep by itself.

On the 737 we're holding at 57 a month, on the gates we agreed with the FAA. We'll keep giving customers honest delivery dates rather than push the line.

On widebodies, the 787 is the most efficient airplane in its class. We'll keep making it better with our partners at GE, and we'll keep investing in Charleston.

We'd rather do fewer things and do them well. The financials will follow our production performance."

**Airbus.** Expected scenario: S1, rivals hold. Boeing says it is 'ready on our end' but 'the market case for us isn't there yet', and gives no date. The MAX holds at 57 a month, and its widebody growth comes from the current 787 at Charleston with the GEnx upgrade, which is not a Re-engine.  Working weights: S1 50%, S2 15%, S3 5%, S4 15%, S5 5%, S6 5%, S7 5%. All seven columns stay plausible.  The order does not turn on the call. The default is the only survivor in every column, and the Re-engine item keeps its sign unless a 787 Re-engine is more than about 64% likely. Best grid plan in it: Raw best in S1: NGSA hold (A320 Alt plan) + A350 Re-engine, at +14.98. That is +0.89 over the default, and +0.75 at my weights. It fails two binding soft vetoes: - Toepfer: the added-move $1B test; - Wagner: no mature widebody engine for a 2050 EIS. It also sits inside my within-$1B default band, and no override is possible.  The best survivor, and the one ordered, is NGSA hold (A320 Alt plan) + A350 hold, with no Delay Tactics. It scores +14.09 in S1, and about +13.91 at my weights; its worst column is S4 at +13.29. It is the only survivor in every column. Premium: $0.00B. Board: approve.

Public statement: "Our core principles of safety, quality, integrity, compliance and security will remain at the heart of all we do. Our next-generation single-aisle aircraft is in service, and its ramp-up is completing in a disciplined and controlled way. It flies on robust, multi-source engine supply from CFM and from the Pratt & Whitney-Rolls-Royce Joint Venture. We brought it into service on the clock of maturity, and we will keep running it on that clock. This is how we prepared the Airbus of the 2030s, and it is how we will serve our customers into the next decade. To the end of the transition, the A320 family continues to serve our customers on our proven lines, and we keep the in-service fleet fully supported. We are securing the engines, structures and materials our own production needs. The A350 family, including the A350F, remains our widebody focus. We continue to fund our programmes from our own cash generation, within our financial framework, and to preserve our financial flexibility and a strong balance sheet. Together with our European industrial base, our suppliers and our partners worldwide, we will continue to work with the whole industry for a tariff-free, zero-for-zero regime for civil aviation."

**CFM/GE.** Expected scenario: S1, rivals hold. No Boeing fps this round: Boeing said 'we are not launching a new airplane this year' and gave no date, holding the MAX at 57 a month. Airbus keeps code 7 on the NGSA (CFM, P&W and RR fitted). The Joint Venture stays formed, and its effect is already in the row. No widebody Re-engine, so the GEnx keeps counting from 2042. No Embraer volume agreed. This is the column the public record supports, and it is also the low column for hold (-28.04, $0.09B below S2). Best grid plan in it: Hold everything (Do Nothing): -28.04 in S1 (yield 82.47%). It is also best in S2 (-27.95). The next-best row, Open Fan + Lobby, is -45.52 / -45.40, which is $17.48B / $17.45B worse. The submitted plan is the best grid plan. Premium: $0.00B. Board: approve.

Public statement: "Safety, quality, delivery and cost, always in that order.

Our first job is the fleet flying today: the LEAP fleet and our new single-aisle engine, now flying with our customers. We'll tell you what we're seeing in the field, and we'll tell you what we don't know yet. Shop-visit material and time-on-wing kits stay ahead of the OE delivery rate through the ramp, and we don't trade durability for fuel burn.

Airbus asked for long-term engine supply, and we're working that through with them, jointly with Safran. CFM's engines stay on offer to every airframer. We don't have a birthright on anybody's next order. We have to earn it, one engine at a time.

On the 787, we'll keep making the GEnx better for Boeing's customers.

RISE stays a technology programme we're all in on with Safran, and the airframers will set its date.

No new programme this round. We're running the business we've got, and running it well. It's that simple. Ain't that hard."

**Pratt & Whitney.** Expected scenario: S1, rivals hold (p 0.75). Boeing does not launch an fps this round. Its latest words on the record are 'not launching a new airplane this year', and it has passed two rounds. NGSA stays in service on code 7 with CFM, P&W and Rolls-Royce fitted. Our row scores −1.65. Best grid plan in it: `GTF2: hold` (gtf2_solo hold, jv_with_rr hold) scores −1.65 in S1. It is the only row on the grid, so it is also best in S2 (−1.68). Premium: $0.00B. Board: approve.

Public statement: "Control what you can control. The hard part first. The GTF fleet on the A320neo is still not where our customers need it to be, and we own that. A large fleet is coming through the shops, so the fleet's spare parts and shop material come ahead of new-engine deliveries. We are continuing the GTF Advantage hot-section kit at standard terms, and we report progress as the share of the fleet in the latest configuration.

The Pratt & Whitney and Rolls-Royce Joint Venture engine grew out of our next-generation geared turbofan. It has been ready since 2036 and has flown on the new Airbus single-aisle since 2037, alongside CFM. We will report its durability as the fleet data show it, by operating environment, hot and sandy included, and claim no more than that. If the data tell us something we don't like, you will hear it from us first. We have learned our lesson from the industrial gaps on the GTF.

The competition is strong, and it should be. We answer it with time on wing and with product, not with price. The Joint Venture's terms stand as published: risk, investment and revenue are shared, and our gear and our core stay ours, in work-share and in intellectual property.

Our engine is available, as certified, to any new single-aisle whose entry into service it can meet, on standard terms, priced for value. We are not in the early entry phase. The dates and rates of any new aircraft are the airframer's to give, not ours."

**Rolls-Royce.** Expected scenario: S1: rivals hold, weight 0.65. Boeing launched no airplane, gave no date and took no fixed-price bet. Its 787 work with GE is 'not a 787 Re-engine order'. Airbus keeps the A350 as its widebody focus. S2 is 0.10, S3 0.15 and S4 0.10. Best grid plan in it: 'UltraFan NB: hold': all four fields at hold. It is +11.03 in S1 and the best plan in every column (+11.03 / +10.99 / +11.03 / +11.28), +11.05 expected on my weights and on the Board's. Against it, the upgrade is −6.48 and UltraFan WB is −9.00 in S1. Premium: $0.00B. Board: approve.

Public statement: "So, plainly. The Joint Venture engine with Pratt & Whitney is in service on NGSA. Our job now is to deliver what flies: time on wing, support, durability. Support through our partner shops, alongside Pratt & Whitney's network, is in place and scaling with the fleet. Any Rolls-Royce content that enters that engine goes in as an engineering change with its own test evidence. We don't compress it for anyone. If the in-service data tell us something we don't like, we will say so first. The engine is on offer to any new single-aisle on standard terms. Widebody is our core, and our Trent durability work continues inside our existing budget. Any UltraFan widebody or Trent upgrade comes to the Board only in the round a Re-engine is on the record, and only if it pays after the cost of running two programmes. We are not after market share. We won't do anything not profitable. I will say that categorically."

### Round 4 (2050)

Events: none.

**Boeing.** Expected scenario: I plan the narrowbody on S1 (rivals hold). With no fps, S3 equals S1; on fps rows it sits $0.06-0.09B below.  For the 787 Re-engine, S1 is blended with S2 (an A350 Re-engine) at Malave's 30% odds (range 20-40%, Low confidence). On that blend Do Nothing scores -0.86.  S3 (Airbus Delay Tactics, covert) stays the buffer baseline and is not blended in. Do Nothing's S3 is -0.83, $2.00B clear of the -2.83 limit. Best grid plan in it: THE BEST PLAN: fps hold + 787 Re-engine - -0.73 expected against Do Nothing's -0.86: +0.13 at 30% odds, +0.08 at 35%. - Best in S1 and S3 (-0.39); worst column -1.53. - That is inside ε. The tie goes to Do Nothing on four counts:   - doing less [BX-1239];   - the higher-confidence plan [BX-0548];   - the higher worst column (-0.93 against -1.53);   - no added penalty. - The Board would veto the Re-engine on Business case anyway.  THE BEST fps ROWS - 10-year at Renton: -1.72 expected (-0.86 against Do Nothing). - 10-year at Renton + Re-engine: -1.73 (-0.87). - Both are inside ε but behind Do Nothing, with worst columns of -1.78 and -2.53. - No fps row is ahead of Do Nothing in any column.  THE SUBMITTED ROW Do Nothing: -0.83 / -0.93 / -0.83. Premium: $0.13B. Board: approve.

Public statement: "I've said for a long time that we'll do a new airplane when the market and the technology and we're ready. That's still the test, and I owe you a straight read on it.

We're ready on our end. The factories are stable. The 777X and the MAX 7 and 10 have been flying with customers for years. The balance sheet is where it should be. The technology is ready too: there are good, mature engines out there from more than one maker. The market case for our next airplane moved our way this year, for the first time in a while. I think it's turning. I don't think it's turned. So we're not launching a new airplane this year, and I'm not going to give you a date for one. I'd rather tell you plainly that the case isn't there than launch an airplane to avoid saying so. Another company's schedule doesn't set ours.

When we do launch, you'll get an entry-into-service date we know we can meet, with room built into it. We'll share the development risk sensibly with our partners, and we won't take a fixed-price bet on it.

One correction from me on the 737. I've been saying we're holding at 57 a month. That's our capacity, on the gates we agreed with the FAA. We build to demand, and this year that's about 43 a month. As demand comes down, we'll bring the rate down in steps on those same gates, never off a cliff, and we'll keep our suppliers and our people ready through it. Customers will keep getting honest delivery dates.

On widebodies, the 787 is the most efficient airplane in its class. We'll keep making it better with our partners at GE, and we'll keep investing in Charleston.

We'd rather do fewer things and do them well. The financials will follow our production performance."

**Airbus.** Expected scenario: S1, rivals hold. Boeing says the market case for its next airplane 'isn't there yet', gives no date, and would 'rather do fewer things and do them well'. On widebodies it is improving the current 787 with GE and growing Charleston; the GEnx upgrade is 'not a 787 Re-engine order'.  Working weights are unchanged: S1 50%, S2 15%, S3 5%, S4 15%, S5 5%, S6 5%, S7 5%. All seven columns stay plausible. On the default row an fps (S2-S5) no longer moves our number; only a 787 Re-engine (S6 / S7) does.  The order does not turn on the call. The default is the only survivor in every column, and the Re-engine item would keep its sign unless a 787 Re-engine were more than about 58% likely. Best grid plan in it: Raw best in S1: NGSA hold (A320 Alt plan) + A350 Re-engine, at +14.66. That is +0.57 over the default, and +0.47 at my weights. It fails two binding soft vetoes: - Toepfer: the added-move $1B test; - Wagner: no mature widebody engine for a 2055 EIS. It also sits inside my within-$1B default band, and its worst column (+13.64) trails the default's.  The best survivor, and the one ordered, is NGSA hold (A320 Alt plan) + A350 hold, with no Delay Tactics. It scores +14.09 in S1-S5 and +14.06 in S6 / S7, about +14.09 at my weights; its worst column is S6 / S7 at +14.06. It is the only survivor in every column and the best plan in S6 and S7. Premium: $0.00B. Board: approve.

Public statement: "Our core principles of safety, quality, integrity, compliance and security will remain at the heart of all we do. Our next-generation single-aisle aircraft is at full rate, and we run it in a disciplined and controlled way. It flies on robust, multi-source engine supply from CFM and from the Pratt & Whitney-Rolls-Royce Joint Venture, and we will report its in-service performance as the fleet data show it. We brought it into service on the clock of maturity, and that is the clock we keep. A320 family production has completed, and we keep the in-service fleet fully supported, with its sustaining engineering fully staffed. We are securing the engines, structures and materials our own production needs, on standard terms. The A350 family, including the A350F, remains our widebody focus and competes on product and value. We keep preparing the technologies for the generation after this one, on the clock of their maturity. We continue to fund our programmes from our own cash generation, within our financial framework, and to preserve our financial flexibility and a strong balance sheet. Together with our European industrial base, our suppliers and our partners worldwide, we will continue to work with the whole industry for a tariff-free, zero-for-zero regime for civil aviation."

**CFM/GE.** Expected scenario: S1, rivals hold. This is the column the public record supports: - No Boeing fps this round. Boeing said "we're not launching a new airplane this year, and I'm not going to give you a date", and it holds the MAX at 57 a month on the FAA gates. - Airbus keeps code 7 on the NGSA (CFM, P&W and RR fitted) and extends its long-term engine slot agreements. - The Joint Venture stays formed, and its effect is already in the row. - There is no widebody Re-engine, so the GEnx keeps counting. - No Embraer volume is agreed. Hold is -28.04 in S1, identical to S2, so the low column and the expected column coincide. Best grid plan in it: Hold everything (Do Nothing): -28.04 in S1 (yield 82.47%), and also the best in S2 (-28.04). The next-best row, Open Fan + Lobby (-41.26), is $13.22B worse, and the Open Fan alone (-42.01) is $13.97B worse. The submitted plan is the best grid plan. Premium: $0.00B. Board: approve.

Public statement: "Safety, quality, delivery and cost, always in that order.

Our first job is still the fleet flying today: the LEAP fleet and our new single-aisle engine, flying with our customers. We'll tell you what we're seeing in the field, and we'll tell you what we don't know yet. Shop-visit material and time-on-wing kits stay ahead of the OE delivery rate as the fleet ages, and we don't trade durability for fuel burn.

Airbus is extending its long-term engine supply agreements, and we're working that through with them, jointly with Safran. CFM's engines stay on offer to every airframer. We don't have a birthright on anybody's next order. We have to earn it, one engine at a time.

On the 787, we'll keep making the GEnx better for Boeing's customers.

RISE stays a technology programme we're all in on with Safran, and the airframers will set its date.

No new programme this round. We're running the business we've got, and running it well. It's that simple. Ain't that hard."

**Pratt & Whitney.** Expected scenario: S1, rivals hold. Boeing again says it is not launching a new airplane this year and gives no date. CFM says it has no new programme this round. Weights: S1 0.75, S2 0.25. Best grid plan in it: GTF2: hold (`gtf2_solo: hold`, `jv_with_rr: hold`) at −1.65 in S1. It is the only row on the grid, and it is also best in S2 at −1.65. Premium: $0.00B. Board: approve.

Public statement: "Control what you can control. The hard part first. A large GTF fleet on the A320neo is coming through the shops, and until every one of those engines flies in the latest configuration, that fleet is not where our customers need it to be. We own that. The fleet's spare parts and shop material come ahead of new-engine deliveries, and we are continuing the GTF Advantage hot-section kit at standard terms. We will report progress as the share of the fleet in the latest configuration when we have the data to report it.

The Pratt & Whitney and Rolls-Royce Joint Venture engine grew out of our next-generation geared turbofan. It has been ready since 2036 and has flown on the new Airbus single-aisle since 2037, alongside CFM. We claim no more for its durability than the fleet data show, and we will report those data by operating environment, hot and sandy included. If the data tell us something we don't like, you will hear it from us first. We have learned our lesson from the prior iterations of the GTF.

The competition is strong, and it should be. We answer it with time on wing and with product, not with price. The Joint Venture's terms stand as published: risk, investment and revenue are shared, and our gear and our core stay ours, in work-share and in intellectual property.

Our engine is available, as certified, to any new single-aisle whose entry into service it can meet, on standard terms, priced for value. Any change a new airframe needs goes in with its own test evidence. We are not in the early entry phase. Our capital order doesn't change: the dividend comes first. The dates and rates of any new aircraft are the airframer's to give, not ours."

**Rolls-Royce.** Expected scenario: S1: rivals hold. Boeing launches no new airplane and gives no date. Its 787 work with GE is 'not a 787 Re-engine order'. Airbus keeps the A350 family as its widebody focus. CFM/GE launches no new programme. Weights 0.75 / 0.10 / 0.10 / 0.05 (S1-S4). S2 equals S1 on the hold row, so the 0.10 on S2 moves nothing. Best grid plan in it: UltraFan NB: hold (all four fields at hold). It scores +11.03 in S1 and is also best in S2 (+11.03), S3 (+11.03) and S4 (+11.37). Expected +11.05 on my weights and the Board's, +11.10 on the Re-engine stress. The two alternatives are hold + T1000 upgrade (+4.30 in S1, -6.73 against hold) and hold + UltraFan WB (+2.03 in S1, -9.00 against hold). Premium: $0.00B. Board: approve.

Public statement: "So, plainly. The Joint Venture engine with Pratt & Whitney is in service on NGSA, and we pace it on durability. Our job is to deliver what flies: time on wing, support, durability. Support through our partner shops, alongside Pratt & Whitney's network, scales with the fleet. Any Rolls-Royce content that enters that engine goes in as an engineering change with its own test evidence. We don't compress it for anyone. If the in-service data tell us something we don't like, we will say so first. The engine is on offer to any new single-aisle on standard terms. Widebody is our core. Our Trent durability work continues inside our existing budget. Any UltraFan widebody or Trent upgrade comes to the Board only once a Re-engine is on the record, and only if it pays after the cost of running two programmes. We are not after market share. We won't do anything not profitable. I will say that categorically."

The full record of every step (Board guidance, frames, test memos, decisions, veto checks, Board reviews) is in
`engine/reference/played_decisions.json`; the briefs and bulletins the players saw are in `engine/reference/briefs/`.
