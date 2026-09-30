# Drafter brief: one theme of the Boeing behavioural profile

We are building an independent Boeing strategy agent for a Boeing vs Airbus war game. It must decide the way Boeing has actually decided. First read `SYNTH_BRIEF.md` in the same scratchpad folder: it describes the game, the levers and the final profile structure.

You draft ONE theme. An integrator will merge five theme drafts into the final `profile.md`.

## Input

`wargame/profiles/build/work/profiles/boeing/evidence.jsonl` holds verified evidence items. Every quote has been machine-checked against its source page. Each item carries:
- `id` (B-0001…), `category`, `date`, `doc`, `page`, `speaker`, `quote`, `finding`;
- `trigger`, `response`, `lag`, `numbers`;
- `perspective`: `own_behaviour`, or `intel_on_rival` for what Boeing said about Airbus.

Filter the file to your categories with a short Python or jq script. It is too large to read whole: about 2,500 items. Read every item in your categories; you may skim other categories for context. Period summaries are in `.../scratchpad/evidence/*.summary.md` (tr01 = 2024-25 … tr15 = 2006-08; tk1-4 are 10-Ks; `rival` is the Airbus action/reaction timeline).

Speaker names tell you which era of Boeing leadership said what:
- McNerney, CEO to 2015;
- Muilenburg, 2015-2019;
- Calhoun, 2020-2024;
- Ortberg, 2024-.

Doctrine shifted across these eras. **Track the eras explicitly**, and make clear which behaviour is **current (2024-25)** versus historical.

## Output

Write `.../scratchpad/profiles/boeing/draft_<theme>.md`: 1,200-2,500 words, dense and specific.
- Every claim cites ids, like [B-0123].
- Every number comes from the evidence.
- Label any inference **(inference)**.
- Separate what Boeing SAID from what it DID. Where the two diverge, that divergence is itself a behavioural fact; flag it.
- Give **decision rules** the agent can apply: thresholds, gates, lags, priorities. Not vague adjectives.
- End with a short "For the war game" section. It translates your theme into concrete guidance for the levers:
  - fps timing, and Solo vs Joint Venture;
  - 787 Re-engine;
  - Rate Increase;
  - cancellation;
  - engine choice;
  - how to react to NGSA, A350 Re-engine, Delay Tactics and Poaching.

Final reply: five lines at most.
