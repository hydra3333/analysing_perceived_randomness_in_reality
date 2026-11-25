# Build step 3, slice C (creating a tree, the installs, verifying a tree): plan and working notes

**Date:** 25 November 2026. **Author:** the Claude web chat (on Fable, the owner's go: decision log entry 301).
**Status:** working notes, kept up to date as the slice is written. Not reviewed, not ratified. It authorises nothing.
**If a chat resumes or a new one starts:** read this file, then the files it names under `overlay/`, then go on from
section 4 ("Where it stands"). Slices A and B are reviewed (EX_321, EX_327) and lie in the same overlay (34 files).

## 1. What governs the slice (all ratified; nothing here is a new design)

- Deployment design v0.12: section 3 (what can be installed; what every install checks), 4 (`Init_Tree`), 5
  (`Install`), 6 (`Reinstall_Infra`), 7 (`Verify_Tree`), 8 (an operation stopped half-way), 9 (the process rules of
  the install tools: "the existing rule of design 6.1, applied to the target tree, the tool's own chain excepted"),
  2 (the install tools live in DEV; with RAT-56, psutil for the process rule only).
- Specification v0.6: section 12.1 to 12.6 (12.3 the checks and the smoke case; 12.4 the question of an
  infrastructure reinstall, in full), 13 (the environment), 3.4 and 3.5 (variants and the status file).
- The build plan v0.1r1 sections 4 and 6; EX_301.
- Out of this slice: `Correct_Shared_Code`, the QA software replacement, the reseeding, the rerun (build step 4);
  the updater (slice D). Their states of design section 8 are recognised and refused, not carried out.
- The working principle: the smallest thing that carries out those clauses. "The same command again" is the only
  resumption; no repair; no new record.

## 2. The parts, in the order they are written

**C1. The checks that travel with the installed software** (design 3.3 items 4, 6, 7; specification 12.3 items 2, 4,
5). New infrastructure in every tree, run with the tree's own Python: the smoke case of a variant for a game (an
invented results table from a fixed seed, long enough for the variant's declared minimum history; the ordinary
engine; passes only on a complete FORECAST; writes only under `<tree>/scratch/`; removed on success, left and named
on failure); the fixed sample of stored forecasts recomputed and compared by content; the derived results in full
(the existing check of specification 5.8). One entry point that a tool in DEV can start with the target's Python
and read the result of. **And `Verify_Tree.bat`** (design 7), which is those checks, the environment's marker, and a
backup attempted before and after.

**C2. What every install shares** (new `deploy/` module): the plan (every file to copy with its hash, from the
markers and the manifest); copying a file (temporary name, hash, rename; no existing file opened for writing); the
barrier `records/INSTALL_IN_PROGRESS.json` holding the plan, and the comparison of a barrier found with the plan now
(design 8); the reservation of the target (its job lock by exclusive create, then the process check under it; the
updater's lock; `SNAPSHOT_DUE`); the recovery kit and the backup attempted, and the one question with their results
said exactly; `INSTALLED_FILES.json`; the log line in `records/INSTALL_LOG.jsonl`; the suite on a temporary copy with
the target's Python when the target's infrastructure is file for file DEV's.

**C3. `Init_Tree.bat QA|PROD`** (design 4, nine steps; it stops at step 6 for the owner to build `.venv`, and the
same command goes on).

**C4. `Install.bat QA|PROD [--only ...]`** (design 5, eleven steps; add-only).

**C5. `Reinstall_Infra.bat QA|PROD [--replace-unfinished]`** (design 6, eleven steps; refuses any forecast-class
file; says what it would change before it asks; the cutoff file when a change from draw X was accepted).

## 3. Readings taken (for the reviewer; RECOMMENDED unless marked)

(none yet)

## 4. Where it stands

- 25 November 2026: the ratified clauses read (design 2 to 8; specification 12.3); this plan written; no code yet.
  Next: C1. Before coding C1, read what the engine already offers: `src/research/derived_check.py` (the full
  check), `forecast_engine.py` and `reader.py` (how one forecast is computed from a view), `variant_lists.py` (how a
  stored forecast is read), `variant_folders.py` (a variant's declared minimum history and games).

## 5. Costs on the owner's PC, to be told plainly when the slice is put to him

- `Init_Tree` and `Reinstall_Infra` run the whole suite with the target's Python on a temporary copy (about ten
  minutes in the cloud; the owner's own figure on Windows is in his install reports).
- Every install is preceded and followed by a whole backup of the target (slice B's cost, twice).
- An infrastructure reinstall recomputes every score and the whole prevailing ledger twice (before the question, and
  after the overwrite).
