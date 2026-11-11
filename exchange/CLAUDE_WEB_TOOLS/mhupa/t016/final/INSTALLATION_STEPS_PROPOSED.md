# MHUP-A: final preparation and the proposed installation steps (11 November 2026)

By the Claude web chat (Opus 5.5), after the project owner's ratification of 11 November 2026
(`exchange/HO2_2026_11_10/MHUPA_Owner_Ratification_Rulebook_v05_AppJ_2026_11_11.md`). Not an EX message. US-ASCII,
CRLF. **Nothing here is installed or run.** Each gate below needs the owner's own go, in this order.

## 1. The final documents, and how they differ from the reviewed r2 drafts (commit 19e45ff)

| Final file (this folder) | From the r2 draft | Differences (all in `R2_TO_FINAL.diff`) |
|---|---|---|
| `CLAUDE_md_rulebook_v0_5_FINAL.md` (LF) | `../RULEBOOK_v0_5_DRAFT_CLAUDE.md` | the version line (draft label removed; ratification stated); W01 (A4's last sentence) |
| `APPENDIX_J_AMENDMENTS_RATIFIED.md` | `../APPENDIX_J_AMENDMENTS_DRAFT.md` | title and status lines only (draft label removed; ratification stated) |
| `OWNER_ROWS_8_9.md` | `../OWNER_ROWS_8_9_DRAFT.md` | title and status lines only |
| `TASK_T016_PREFREEZE.md`, from `make_task_t016.py` | `../TASK_T016_DRAFT.md` | the status line (pre-freeze template); W02 ("five ... items" -> "six ... files", in the purpose and step 37); the optional precision of step 10 ("U remains valid and held by this package") |

`R2_TO_FINAL.diff` has 31 changed lines, every one of them in the table above; nothing else changed. W01 is the
reviewer's suggested wording, word for word. `check_task_commands.py` on the pre-freeze task: PASS (47 command lines).
SHA-256 of the final rulebook: `fa7a5fe229be832880cda4704ed9e7d27af2f4b9462464f7af262e540acd5200` (the file installed
at gate B is byte-identical to it).

## 2. The proposed installation steps

**Gate A - freeze the package (your go).** Claude, in the cloud:
1. Builds the final package on base `c48ac3c` (unchanged, so all evidence stays on the same base) with E_1 revision 3's
   `effective_date` set to the freeze day (C01-EFF), and removes the draft labels from `INSTALL_INSTRUCTIONS.md`.
   No code or test changes from the reviewed draft.
2. Zips it as `MHUPA_Install_v1.zip` (top folder `MHUPA_Install_v1`) and takes its SHA-256.
3. Reruns the evidence on the frozen bytes: the full path, steps 0-18 with step 10, on an LF clone (Python 3.13)
   and a `core.autocrlf=true` clone (Python 3.15); the 88 negatives; the 10 step-10 negatives; the T016 dry run.
4. Completes `TASK_T016.md` from the template (EX folder, SHA-256, frozen counts) and reruns `check_task_commands.py`
   on it against the settings as they are then.
5. Commits the zip, its EX message and the evidence to `exchange/EX_<nnn>_Claude/` (named paths) and pushes.
- **The reviewer:** a short check of the frozen package against the reviewed draft (manifest, SHA-256, evidence, the
  completed T016). Recommended, because the date and the zip are new; no new design.

**Gate B - install rulebook v0.5 and put T016 in the inbox (your go, after A).** Claude makes one commit with exactly two
paths and pushes it:
- `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md` <- `CLAUDE_md_rulebook_v0_5_FINAL.md`, byte for byte (SHA-256 above);
- `CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T016.md` <- the completed task.
You then pull on your PC (with Claude Code closed, or before its next task) and check:
```
cd /d E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality
git pull --ff-only
git log -1 --format=%H
certutil -hashfile CLAUDE_CODE_WORKING_FOLDER_TREE\CLAUDE.md SHA256
```
Expect: the commit Claude names; the SHA-256 above. Section 2A only allows anything once you give T016 its go.

**Gate C - run T016 (your go, after B).** In Claude Code at the repository: `Do inbox\TASK_T016.md`. About 45-60
minutes (the suite is most of it). Claude Code commits `outbox\REPORT_T016.md` and asks you to push; you push; Claude reads
the report from GitHub and reports PASS or the STOP.

**Gate D - the F1 deny lines (your go, after T016 PASS, before the live step 0).** Your own commit. In
`.claude\settings.json`, directly after the line `"Bash(*Method_Rankings_Report*--game*)",` add:
```
      "Bash(*Run_Evaluation*)",
      "Bash(*Method_Mode_H*)",
      "Bash(*mode_h*)",
      "Bash(*process_check*)",
      "Bash(*install_records*)",
```
then:
```
git add .claude/settings.json
git commit -m "settings: deny the MHUP-A evaluator, Mode H, process and records tools to Claude Code (F1, after T016)"
git push
```
Claude then checks the file from GitHub (valid JSON, five lines added, nothing else changed). From then on Claude Code
can never run those tools, even by mistake.

**Gate E - F2 rows 8 and 9 (your go).** Your own checks at the real root, by `OWNER_ROWS_8_9.md`; send Claude the
outputs. Row 9 is optional only in the sense that, without it, its oracle is reported unmet.

**Gate F - the live install (your go, after D and E).** `INSTALL_INSTRUCTIONS.md` from the frozen zip, steps 0 to 19, in
one CMD window, sending Claude the output at any STOP. After the push, Claude verifies the install from GitHub.

**Records (no extra machinery).** The ratification is recorded in `exchange/HO2_2026_11_10/`; the register entry and the
design text follow at the next documentation round (a line in R-025 says so).

## 3. One point to settle before the freeze

The draft instructions still say "Claude's reviewed restore steps for a STOP from step 6 on" will be given. I propose
they stay **per case**, as for J-3 and J-4: on a STOP from step 6, Claude writes the exact restore lines for the state
the output shows; they are reviewed and you approve them. The copy tool already has the `--remove ... --restore` form
they end with. That is simpler than a prewritten restore script for every state, and it matches the ratified restore
rule (E, P and U kept until a fresh `CLEAN`). If you agree, the frozen instructions say exactly that and drop the "Not yet
in this draft" note. No code changes.
