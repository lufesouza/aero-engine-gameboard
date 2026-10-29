# dash-2050-cons: the Boeing vs Airbus war game, packed for any LLM

**Start with `GAME_SCRIPT.md`.** It explains the four ways to play, the game, its rules and its round protocol.

| File or folder | What it is | Who gets it |
|---|---|---|
| `GAME_SCRIPT.md` | The full script: set-ups, the runner, the operator's and game master's steps, rules, protocol, known inconsistencies | The operator and the game master |
| `engine/run_game.py` | The automated runner: plays all twenty seats through any OpenAI-compatible API | The operator (set-up 1) |
| `engine/play.py` | The engine's commands: new, brief, orders-template, check, adjudicate, undo, status, reveal, save, load, env, selftest | The game master |
| `kits/COMPANY_<company>.md` | One company's kit: how its chat works, its decision rule, what each seat is told and receives, the nine steps, formats, orders, rules, doctrine and its four full agent definitions | That company only |
| `companies/<company>/` | That company's source files: behavioural profile, objectives, game doctrine, 2026 analyst-model baseline, executive and Board profiles, role cards, evidence | That company only |
| `personas_full/`, `personas/` | All twenty agent definitions (full, and condensed cards) | Never a company (each company's four are in its kit); the runner uses them |
| `RESULTS_AS_PLAYED.md`, `engine/reference/` | The original game: orders, values, statements, every step's notes, the briefs and bulletins (full pack only) | Nobody until the replay ends; the operator for the self-test and set-up 4 |

Two zips: `dash-2050-cons-llm.zip` (everything, for the operator) and `dash-2050-cons-llm-players.zip` (the same
without the original game's record: for the runner, the GM chat and set-up 3; a company chat gets only its own kit and
its own `companies/<company>/` folder, never a zip). Each unzips to a folder `dash-2050-cons-llm/`: unzip them into
separate folders, and run every command from inside one.

## Quick start

1. Unzip the full pack into its own folder, `cd dash-2050-cons-llm`, install the engine's needs
   (`pip install -r engine/requirements.txt`) and run `python3 engine/play.py selftest`. It prints PASS or FAIL per
   round and nothing about the original game.
2. **Automated (recommended):** unzip the players' pack into another folder and, with an API key,
   `python3 engine/run_game.py --game mygame --base-url <endpoint> --model <model>` (GAME_SCRIPT.md section 2).
3. **In chat apps:** follow GAME_SCRIPT.md section 3 (six chats and an operator; one chat; or no code execution).

## Notes

- The pack contains extracts from company filings, earnings-call transcripts and analyst models (Goldman Sachs,
  Morgan Stanley, S&P Capital IQ) in `companies/`, the kits and the briefs. Check that your licences and your
  organisation's rules allow sharing them with the LLM provider you use.
- Sizes: `GAME_SCRIPT.md` is about 20k tokens; a company kit about 35-40k; a brief 4-9k. A full automated game is
  roughly 400-1,000 API requests and 20-60 million input tokens.
- Built by `wargame/export/build_llm_pack.py` from the repository's game files.
