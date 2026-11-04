# Embraer profile: how it was built and checked

Built November 2026 for run `dash-2050-emb`, where Embraer is a sixth player. Sources are the repo's own:
`Embraer Transcripts 2010-2020 (1).pdf` (despite the name it runs from 2011 to the 8 May 2026 call, read as text),
the four Embraer S&P Capital IQ workbooks, and the earlier research file
(`wargame/reports/dash-2050-phaseout/data/embraer_research.json`, used only with its verdicts).

| File | Seat | Built from | Adversarial check |
|---|---|---|---|
| `profile.md`, `teams.md` | company doctrine; the team and its decision rule | 204 company items, 162 transcript items 2011-2026, 13 financial, 29 research | 204 quotes checked, 3 fixed, 21 claims removed or relabelled |
| `.claude/agents/embraer-gomes-neto.md` | CEO (frame, decide, revise, Board revise) | 160 items in his own words, 27 events, 2019-08 to 2026-05 | 203 quotes checked, 2 fixed, 24 relabelled |
| `.claude/agents/embraer-santana.md` | CFO (test, veto check) | 25 items in his own words (the 8 May 2026 call), plus Garcia's record cited as inherited | 97 quotes checked, 0 fixed, 18 relabelled |
| `executives/garcia.md` | not seated: the CFO doctrine Santana inherits (Garcia, CFO 2020 to March 2026) | 138 items in Garcia's own words, 21 events | 161 quotes checked, 3 fixed, 28 relabelled |
| `.claude/agents/embraer-meijer.md` | operating head (test, veto check) | 57 answers in his own words, 3 events to November 2024 | 202 quotes checked, 0 fixed, 24 relabelled |
| `.claude/agents/embraer-board.md` | Board (guidance, review, confirm) | 117 items; no director speaks in the sources, so it is role-based | 136 quotes checked, 5 fixed, 40 relabelled |

**Integration.** The six evidence files were merged into `evidence.jsonl` (881 items). Ids that collided between
builders were renumbered (company EB-0200..0204 to EB-0400..0404, the CEO's EB-0250..0293 to EB-0600..0643, Garcia's
EB-0300..0321 to EB-0800..0821) and every citation was remapped by its own file first; none was left ambiguous or
unresolved. The CFO seat was then moved from Garcia to Santana across the files, and two independent checkers (the
decision rule across files; citations and attribution) found 30 issues, then 13, then 9, all fixed. Every id cited in
the seven files resolves; no file carries a game dollar figure or a gendered pronoun outside a quote.

**Caveats.**
- The decision rule and both vetoes are inferences from calls; there are no Board papers.
- The Board's composition is not in the sources (one director is named); its culture scores are judgements.
- Meijer last appears in November 2024; Santana's own record is one call.
- One builder (Garcia's) read the round-1 Embraer brief's layout to match its column labels. No figure from it is in
  any file; the CFO's leverage line comes from Garcia's own "below 2x" and the workbooks' EV/EBITDA.
- In this session the agent types could not be loaded, so the seats ran as general-purpose agents with these files
  passed as their text, and the game master audited their tool calls instead of the hook.
