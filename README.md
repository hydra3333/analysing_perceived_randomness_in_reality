# Analysing perceived randomness in reality

A speculative research project. It asks whether the published results of two Australian lotteries, **Powerball** and
**Oz Lotto**, contain any structure that a forecasting method could use better than chance. The working expectation
is that none will be found: the point is to test "perceived randomness" carefully and honestly, with every method
measured against fair draws, rather than to win anything. Nothing here is betting advice.

## The safety rules, in one paragraph

No automation of The Lott or of any lottery website, no use of any site's API, no browser impersonation and no
bypassing of bot protection. The newest draws are a sealed **holdout** (Powerball draws 1577-1586, Oz Lotto draws
1694-1703, and everything after them, the quarantined range): no chat, tool or person acting for the project
displays, quotes or computes with them until the owner opens them in Mode H. Methods see only the draws before
the draw they forecast. Every code change goes through a written design, an independent review, the owner's
ratification and a checked install. The full rules are in the ratification register and the handover documents.

## Who does what

- **The project owner** (GitHub `hydra3333`) is the sole ratifier and run authoriser, and the only one who installs
  code and commits data.
- **The Claude web chat** is the primary designer and coder; it also commits the exchange messages.
- **The ChatGPT reviewer chat** is the independent reviewer.
- **Claude Code** is a local runner on the owner's PC: it rehearses installs in throw-away clones and reports.

## Where things are

| Folder | What it holds |
|---|---|
| `doc/` | The specifications and designs, the **ratification register** (`RATIFICATION_REGISTER_v0_NN.md`, the record of every decision), the architecture, and `doc/HANDOVER/` (the handovers that let a new chat take over). |
| `exchange/` | The numbered messages between Claude and the reviewer (`EX_NNN_...`), the owner's roadmap and reminders (`OWNER_ROADMAP.md`, `OWNER_REMINDERS.md`), and Claude's working tools (`CLAUDE_WEB_TOOLS/`). |
| `src/` | The code: `methods/` (the forecasting methods and their shared contract), `evaluation/` (the scorer and ranking report), the coordinator and the results-data tools. |
| `tests/` | The test suite (run module by module by each install package's runner). |
| `review/` | Review copies and each install package's evidence. |
| `archive/` | Retired method revisions, kept complete. |
| `source_data/`, `results/`, `transitory_data/` | Data and run records. Some of their contents are restricted by the rules above. |
| `CLAUDE_CODE_WORKING_FOLDER_TREE/` | Claude Code's task files, reports and tools; its rulebook is the `CLAUDE.md` there. |
| Root `.bat` files | The owner's launchers; each checks and uses the project's own Python environment (`.venv`). |

## Where to start reading

1. `exchange/OWNER_ROADMAP.md`: where the project is up to, in plain English.
2. The latest `doc/RATIFICATION_REGISTER_v0_NN.md`: every decision and install.
3. The latest handovers in `doc/HANDOVER/` (H-1 for the Claude chat, H-2 for the reviewer).

Licence: see `LICENSE`.
