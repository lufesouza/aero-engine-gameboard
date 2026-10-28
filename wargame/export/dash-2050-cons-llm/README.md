# dash-2050-cons: the Boeing vs Airbus war game, packed for any LLM

**Start with `GAME_SCRIPT.md`.** It is the whole game as one script: the game master's instructions, the rules, the
round protocol, each company's doctrine and the twenty personas.

| File or folder | What it is | Who gets it |
|---|---|---|
| `GAME_SCRIPT.md` | The full script (sections 1-8) | The game master; in a one-chat game, the one chat |
| `kits/COMPANY_<company>.md` | One company's kit: how its chat works, its decision rule, the nine steps, output formats, rules, doctrine and its four full persona definitions | That company's chat only (six-chat set-up) |
| `engine/` | The game engine (Python 3.9+, numpy, pandas) with the 2030 starting position and `play.py` | The game master (needs code execution) |
| `engine/reference/` | The original game: briefs, bulletins, orders, every step's notes | The game master only, and only as section 1.6 of the script allows |
| `personas/` | The twenty persona cards (also in the script, section 8) | |
| `personas_full/` | The twenty original agent definitions, adapted to this pack (file paths point into `companies/`) | |
| `companies/<company>/` | Each company's source files: behavioural profile, objectives, game doctrine, 2026 analyst-model baseline, executive and Board profiles, evidence | That company only |
| `RESULTS_AS_PLAYED.md` | What the original players did (spoiler) | Nobody until the replay ends |

## Quick start

**One chat with code execution** (ChatGPT, Gemini or Claude with file upload and code): upload the zip and say:

> Unzip this pack. Read GAME_SCRIPT.md in full: you are the game master and you will also play every seat by section
> 1.4. Run `python3 engine/play.py selftest`, then start a game and play round 1 by the script.

**Six chats (closest to the original):** in one chat, upload the pack and say "You are the game master: read
GAME_SCRIPT.md section 1 and run the engine". In five more chats, give each company its kit
(`kits/COMPANY_boeing.md` etc.) and say "Read this kit; you are this company. Wait for the game master's brief." Then
carry each round's brief from the GM chat to each company chat, and each company's final orders block back.

**No code execution:** give the one chat `GAME_SCRIPT.md` and the five round-1 briefs
(`engine/reference/briefs/round1_*.md`) only, and follow section 1.6 of the script. Later rounds' original briefs
show what the original players did: give them to the chat only when section 1.6 says they apply.

## Notes

- The engine's self-test replays the original orders and checks that every brief and every value comes out exactly as
  played (`python3 play.py selftest`).
- The company folders and the original briefs contain extracts from company filings, earnings-call transcripts and
  analyst models (Goldman Sachs, Morgan Stanley, S&P Capital IQ). Check that your licences and your organisation's
  rules allow sharing them with the LLM provider you use.
- Built by `wargame/export/build_llm_pack.py` from the repository's game files.
