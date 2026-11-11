# Rulebook v0.5 and TASK_T016 - drafts for focused review (Route A) - cover note (r2, for RECHECK)

By the Claude web chat (Opus 5.5), 11 November 2026, under the owner's authorisation of 12:13 ("drafting only"). Not an
EX message. US-ASCII, CRLF. **Nothing here is installed, run or frozen:** the live rulebook is still v0.4, the inbox has
no T016, `.claude/settings.json` is unchanged, the package is a draft (base `c48ac3c`, working date 2026-11-10, manifest
`ab71cf22...`), and no install has started.

## 0. Revision r2 (11 November 2026, evening): the reviewer's focused review of 5e1a704

Review recorded byte for byte: `exchange/HO2_2026_11_10/MHUPA_T016_Rulebook_v05_ChatGPT_Focused_Review_2026_11_11.md`. The
reviewer accepted the five approaches of section 6 in principle. The corrections, all wording or task-text only:

| Finding | Where | Change |
|---|---|---|
| T016-C01 | owner sheet | the blanket "neither reads any lottery data" replaced: no drawn outcome value is requested or printed; row 8 can read weekly ticket and forecast ledger metadata if present. Before forwarding output, blank only private parts of command lines; a REFUSED names evidence to investigate, never a process to end |
| T016-C02 | rulebook 2A new A6; task | record each step's command, exit code and output as it ends; on a STOP, note the step and the barrier/record state the outputs showed; never inspect or recover the clone; the report lists them (the clean-up-before-report order is kept) |
| T016-C03 | rulebook 2A, A4 | "no project program is ever run against the main repository's root"; the main venv's python.exe is only the interpreter; the main repository's own process_check.py and install_records.py are never run |
| T016-C04 | rulebook 2A, A5; task steps 10, 19, 27 | an EXPECTED REFUSAL passes only on a non-zero exit code AND a line that begins with the given text AND no traceback; each step names the later steps that prove nothing changed (10: steps 11 and 17; 19: steps 23 and 25; 27: steps 30 and 32) |
| T016-C05 | task header | the freeze list: pinned ZIP and SHA-256, frozen counts, the task's commit named in the go, `check_task_commands.py` rerun on the final file against the then-current settings; F1 stays after T016 |
| J-REVIEW | Appendix J amendments | J-1/J-2 (normal path) separated from J-3/J-4 (exceptional recovery only: never a runner action or automatic; per case, reviewed and owner-approved; CLEAN before any change; U held to the end); `post_pass_utc` keeps its name and schema (no migration) |

Re-checked: `check_task_commands.py` on the r2 task: PASS (47 command lines). The dry run now judges the three refusals
exactly as A5 says (anchored text, non-zero exit, no traceback): all three PASS
(`evidence/PRELIMINARY_T016_dryrun_r2_lf_py315_refusals_anchored_no_step10.txt`; LF clone; step 10 omitted because no
tool changed since the full run of section 4). No production mechanism was added.

## 1. The files (all in `exchange/CLAUDE_WEB_TOOLS/mhupa/t016/`)

| File | What it is |
|---|---|
| `RULEBOOK_v0_5_DRAFT_CLAUDE.md` | the candidate rulebook (LF, as the live file); on approval it replaces `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md` |
| `RULEBOOK_v0_4_to_v0_5_DRAFT.diff` | the change against v0.4, for review |
| `TASK_T016_DRAFT.md` | the task file (CRLF); placeholders `<EX_FOLDER>`, `<ZIP_SHA256>` and the draft counts are fixed at the freeze |
| `make_task_t016.py` | writes the task file from one table of paths (so every path is spelled once) |
| `T016_ENV_HARNESS.py` | rows 6 and 7 (F2-C01); a development check only, not part of the package |
| `OWNER_ROWS_8_9_DRAFT.md` | rows 8 and 9, the owner's own checks at the real root |
| `APPENDIX_J_AMENDMENTS_DRAFT.md` | J-1 to J-4 for ratification, the stricter additions for information, two wording points in 4.3 |
| `t016_dryrun.py` | my Linux dry run of T016's exact sequence (a working tool, not for the runner) |
| `evidence/` | the dry-run outputs and the F1 deny-line check |

## 2. Rulebook v0.5 (diff: 1 new section, 6 short pointers)

- **New section 2A, TASK_T016 only** (owner decision R-020(g) option (i), EX_157 section 3 conditions):
  - A1 scope: only T016, after its own go; only in `scratch\T016\`; only the task's exact command lines, which passed
    `check_task_commands.py` (no denial bypassed or edited); no change to the main repository; no other task can use it.
  - A2 programs: the package copies of `process_check.py` (`check-no-runs`, `take-install-lock`, `release-install-lock`;
    never `--game`, never the clear commands), `install_records.py` (`install-record`, `release-record`, `validate`), the
    verifier, the copy tool, the suite runner with `--shadow`, and the harness; every `--root`/`--repo` is the clone.
  - A3 data (F2-C04), exactly: the suite runner copies the six development files (bytes only, never parsed or printed)
    into `%TEMP%\MHUPA_step10_...` and removes it (failure is a STOP); the accepted tests read them there through the
    project's reader; the tools between them create, read (one line) and remove the clone's U, test whether session
    locks exist, and read the weekly ledgers if they exist (they do not); the existence test of `no_pycache_ever`; the
    harness reads the main venv and the base Python, writing only in `scratch\T016\e\`. The runner itself still opens
    nothing in the data folders.
  - A4: everything else in section 2 stays (no real root, launcher, termination, lifecycle test, pip or push).
  - A5: **EXPECTED REFUSAL** steps: pass only with a non-zero exit code and the given refusal text; anything else is a
    STOP. This is the narrow clause that lets T016 check Windows refusals without breaking "a STOP is a STOP".
- Pointers to 2A from rules 2.5, 2.7, 2.9 and 2.10, and the section 2 heading.
- Rule 2.1 names Lotterywest-GOV in R-017's words (used only by the owner's reviewed tools, never by the runner).
- Rule 2.7 adds `create_venv.bat`.

## 3. TASK_T016 (42 steps, then clean-up, report and finish)

How the F2 matrix maps onto it:

| F2 row | T016 |
|---|---|
| 1 package identity | step 4 (`cc_clone.py unzip` with the SHA-256) |
| 2 the suite on the installed bytes | merged into step 18: Appendix J step 10 runs `--shadow` in the FULL clone (N5) |
| 3 Appendix J steps 0-18 | steps 5-36; step 0 as clean tree + HEAD (no pull), step 19 omitted; Git only via `cc_clone.py git` with the package's pathspec lists |
| 4 STOP behaviour | three EXPECTED REFUSAL steps that change nothing: step 10 (take U twice: Windows create-exclusive), step 19 (remove E before the package commit), step 27 (release record while E and P exist) |
| 5 N1/N4/N4b on Windows Git | step 37 (`ls-files --eol`: `i/lf w/lf attr/-text` on six files), step 38 (`validate`) |
| 6 env inventory, real interpreter | step 41 (harness `inventory`) |
| 7 planted orphan | step 42 (harness `orphan`, in `scratch\T016\e`, with a control first) |
| 8, 9 | the owner sheet; not in T016 |
| 10 no byte-code folder | step 40 |

The earlier synthetic data-free clone is dropped: with N5, step 10 needs the six files, and a full clone is simpler.
`check_task_commands.py` on the draft against the current settings: **PASS (47 command lines)**.

## 4. Linux dry run of T016's exact sequence (PRELIMINARY; draft package)

`evidence/PRELIMINARY_T016_dryrun_crlf_py315_WITH_step10.txt`: **DRY RUN PASS.** A full `core.autocrlf=true` clone of
current `main` (`cc2ec7a`, a descendant of the base with exchange-only commits; PRE accepts it), placed at
`.../CLAUDE_CODE_WORKING_FOLDER_TREE/scratch/T016/r`, Python 3.15, the tools run with T016's options:
- steps 5-36 (Appendix J 0-18) each gave the expected line; step 18 (`--shadow`): 571 of 571 in 562 s, the live tree
  barred throughout, the temporary copy removed;
- the three EXPECTED REFUSAL steps refused with exactly the texts the task gives (exit code 1 each), changing nothing;
- step 37: `i/lf w/lf attr/-text` on all six files; step 38 `RECORDS PASS ... 80 released unretired entries`; step 39
  clean, with the two commits on top; step 40 `NO_PYCACHE_EVER ABSENT`;
- steps 41 and 42 (harness, on a venv made by `python -m venv`): `ENV INVENTORY PASS`; `control PASS`, then the planted
  file refused by name, `ORPHAN CHECK PASS`.
This is Linux: it proves the sequence, the expected texts and the harness, not Windows behaviour (that is T016's job).

Found while building the harness: the uv-made test venvs here carry `_virtualenv.pth` and `_virtualenv.py`, which no
RECORD lists, and the inventory refuses them, as designed. A venv made by `python -m venv` (as `create_venv.bat` does)
passes. Row 6 is exactly the check that finds such a file on the owner's real venv before Mode H relies on it.

## 5. F1: the owner's deny lines after T016 (proposed, not applied)

`Bash(*Run_Evaluation*)`, `Bash(*Method_Mode_H*)`, `Bash(*mode_h*)`, `Bash(*process_check*)`,
`Bash(*install_records*)` - added by the owner as his own commit after T016's report and before the live step 0.
Checked with a copy of the settings: with them, `check_task_commands.py` STOPs on 13 of T016's lines (so they must come
after T016, as planned), and they deny no new line of any other task in the inbox (the T011, T012 and T019 lines
they match were already denied); `evidence/F1_deny_lines_check.txt`. Appendix K's names for MHUP-B (`Run_Weekly_Session.bat`, `Method_Weekly_*`,
`Weekly_Session_Orchestrator.py`) are added with MHUP-B.

## 6. Questions for the reviewer and the owner

1. **A5 (EXPECTED REFUSAL).** Accept the narrow clause and the three no-change refusals (recommended), or keep all
   negatives as Linux evidence only and drop steps 10, 19 and 27?
2. **Rows 6 and 7.** The harness hashes the whole base `Lib\` and `DLLs\` trees and the venv (read-only; a few minutes).
   A row 6 STOP is a finding, not a fault of the install: it is reported and fixed by a reviewed step, never by hand. Is
   the scope right?
3. **No further live rehearsal.** T016 rehearses steps 0-18 end to end on Windows with step 10; rows 8 and 9 cover the
   real root. I propose no additional owner rehearsal before the live install. Agree?
4. **The temporary copy in `%TEMP%`.** The six files leave the repository tree for the length of the suite (on the
   owner's own disk; removal checked). Acceptable, or should the runner take a folder inside `scratch\T016\`
   (a small runner option; the live install would keep `%TEMP%`)?
5. **Clean-up after a STOP.** As in T020-T022, the clone is removed even after a STOP (the report holds every output).
   Keep, or leave the clone for inspection on a STOP?

## 7. KISS

No production mechanism is added. The harness, the dry run and the task generator are development-only. Section 2A ends
with T016.

## 8. Next, each needing its own approval

The reviewer's focused check of these drafts; the owner's ratification of the Appendix J amendments; then the package
freeze (final date, base, zip and SHA-256 into the task file); rulebook v0.5 installed and T016 committed to the inbox;
the owner's go for T016; F1; rows 8 and 9; the live install.
