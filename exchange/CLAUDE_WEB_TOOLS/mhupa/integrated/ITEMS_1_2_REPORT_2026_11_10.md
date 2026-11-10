# MHUP-A integrated package - items 1 and 2 report (10 November 2026)

Written by the Claude web chat (primary designer and coder) for the project owner, under the owner's GO of 10 November 2026
(`exchange/HO2_2026_11_10/HO2_Closure_Owner_GO_Items1-2_For_NewClaude_v0_1.md`). Not an EX message. US-ASCII, CRLF.
Model: Opus 5.5 throughout. Nothing was installed; no data folder was opened; no real-data run; nothing outside `exchange/`
was committed. Everything below is **PRELIMINARY / DRAFT**: no part of it is final evidence or installation-ready.

## 1. Base and what changed

- **Current `main`:** `c48ac3c393d2eab30014e6200d427b76d90f47ac` (checked again at the end of the work: unchanged; no
  commit after it). This is the base of the rebuilt trees and of the draft package.
- **Since `c48ac3c`:** nothing.
- **Since the 8 November rebuild base `009c985`,** outside `exchange/`, `GAIS/`, `doc/` and the Claude Code folder: only the
  root `README.md` (not a package file).
- **Since the reviewed candidates' base `2061055`,** outside those folders: `.gitignore` (the owner's 16 GAIS lines),
  `README.md`, the new root `create_venv.bat`, and `install_upgrade_dependencies_into_venv.bat` (DEP-1's `pyahocorasick`).
  `src/GAIS/` is gone (GAIS-1).
- **None of the 33 files the package replaces, nor the deleted `src/results_master_v0_1.py`, changed since `2061055`,**
  except `.gitignore`, which the build handles (below).

## 2. Item 1: the rebuilt trees (done)

- BASE = `git archive c48ac3c`, data folders removed. DEV = `build_dev_integrated.sh BASE DEV TOOLS 2026-11-10`.
  **The date 2026-11-10 is a working date only; the final date is set at the freeze (C01-EFF).**
- **DEV against BASE:** 37 new, 33 modified, 1 deleted; the changed set equals the reviewed v1r2 overlay's 70 files exactly.
- **DEV against the reviewed v1r2 overlay** (`EX_151_Claude/MHUPA_Slice2_Review_v1r2.zip`): 65 of 70 identical. The five that
  differ differ only as expected:
  - `.gitignore`: the owner's current file followed by the reviewed MHUP-A block. The block is byte-identical to the reviewed
    one, and the reviewed file is exactly its base (`2061055`) plus the same block, so the owner's 16 GAIS lines survive
    (R-020 (d)).
  - the two `entry_0003.json` files and `archive/methods/E_001/r2/README.md`: the date only (2026-11-04 to 2026-11-10).
  - `tests/test_e1r3_revision3.py`: the pinned date only (one line).
- **Root files:** `create_venv.bat` and `install_upgrade_dependencies_into_venv.bat` are not package files and stay as the
  owner has them. Both are inside the Mode H closure at Approval 1 (every root `.bat`), and `create_venv.bat` joins rulebook
  rule 7 with v0.5 (delta 7 item 5).

## 3. Item 1: preliminary suites (PRELIMINARY; not final evidence)

Full disposable clones of a frozen mirror of `main` at `c48ac3c`, with DEV's changes applied; the reviewed slice 2 runner;
E2R-T12 included (owner-approved for this cloud context).

| Python | Environment | Result |
|---|---|---|
| 3.13.18 | Linux 6.18.44, uv venv: numpy 2.5.4, scipy 1.18.1, psutil 7.2.2 (+ the other five direct packages) | **570 ran, 570 passed, 0 skips; SUITE PASS** (module time 862 s) |
| 3.15.0b4 | the same, uv-managed CPython 3.15.0b4 | **570 ran, 570 passed, 0 skips; SUITE PASS** (module time 809 s) |

Logs: `evidence_2026_11_10/PRELIMINARY_suite_c48ac3c_date20261110_py313.txt` and `_py315.txt`. This closes the 8 November
date-pinning failure at the preliminary level. The final suites run on the date-frozen candidate (item 6). The Windows evidence
(T022, Python 3.15.2) is separate and is of the reviewed candidate, not of this tree.

## 4. Item 2: the builder and the draft package (built; scaffold where marked)

**Tools, committed in `exchange/CLAUDE_WEB_TOOLS/mhupa/integrated/` (SHA-256 of the committed LF files):**

| File | What | Status |
|---|---|---|
| `build_mhupa_pkg.py` | the builder (`BASE DEV OUT BASE_COMMIT DATE`) | complete for item 2 |
| `mhupa_copy_tool.py` (becomes `MHUPA_COPY.py`) | copy `--part gate|rest`, barrier `--create|--remove E|P` | complete for item 2 |
| `mhupa_verifier_template.py` (becomes `VERIFY_MHUP_A.py`) | `pre`, `post`, `committed` built; **`released` a refusing stub** | scaffold: item 3 adds `released` and the barrier-order proof |
| `mhupa_suite_template.py` (becomes `RUN_MHUP_A_SUITE.py`) | per-module counts from the unittest loader | complete for item 2 |
| `mhupa_install_instructions_template.md` (becomes `INSTALL_INSTRUCTIONS.md`) | Appendix J steps 0-19 as CMD lines | **DRAFT**, says "do not run"; step 17 STOPs until item 3 |
| `smoke_steps.sh`, `neg_smoke.sh`, `apply_dev.py` | the smoke run, the negatives, applying DEV to a clone | working tools |

The current hashes are in the commit; the builder writes `BUILD_REPORT.txt` with every package member's hash.

**What the builder asserts, and STOPs on:**
- the changed set is exactly 37 + 33 + 1;
- the step 6 gate files, computed from the static import closure of `contract_dispatch.py` (every import, including those
  inside functions and relative ones, followed through `src` and `src/methods`; a name found in both refuses), equal the ten
  listed: **computed closure 15 project files, of them changed by the package exactly the ten** (eight changed:
  `contract_dispatch`, `contract_forecast`, `contract_receipts`, `contract_records`, `contract_runner`, `contract_task`,
  `contract_vocab`, `game_draws_reader`; two new: `master_versions`, `owner_records`);
- E_1 revision 3's date equals DATE in both registry entries, the r2 archive README and the pinned test;
- `release_entries` derive from the two new `entry_0003.json` (E_1 revision 3, both games), `retires` is empty, and
  `registry_entries_added` is exactly those two;
- the tests are counted by the unittest loader (nothing run): **570 in 45 modules**, identical module by module to the
  reviewed runner.

**The draft package `MHUPA_Install_v1`** (built in the cloud workspace; not committed, because it is rebuilt at the freeze):
- `repo_overlay/` (70 files);
- `PACKAGE_MANIFEST_MHUP_A.json`, SHA-256 `fa034f33e11963e4932a2669c0593732d025c805072024144dd6f18877e17df1`. It is the one
  manifest: `install_records.py` and `process_check.py` read its `package`, `release_entries`, `retires` and
  `registry_entries_added`; the copy tool and verifier read the file lists, `gate_files`, `rest_files`, `tool_sha256`,
  `barriers` and the record paths; `status` says DRAFT;
- `VERIFY_MHUP_A.py`, `MHUPA_COPY.py`, `RUN_MHUP_A_SUITE.py`;
- `STAGE_PACKAGE_COMMIT.txt` (72 paths) and `STAGE_RELEASE_COMMIT.txt` (1): pathspec files for `git add`, so no denied
  filename is ever typed (F4);
- `INSTALL_MANIFEST_SHA256.txt`, `INSTALL_INSTRUCTIONS.md` (DRAFT), `BUILD_REPORT.txt`.
- Copies for reading: `evidence_2026_11_10/DRAFT_INSTALL_INSTRUCTIONS.md` and `DRAFT_PACKAGE_MANIFEST_MHUP_A.json`.

**Smoke test of steps 0-18** (`smoke_steps.sh`; PRELIMINARY): on a synthetic root (a scratch clone with `source_data/`,
`results/` and `transitory_data/` removed by a local, unpushed commit, and empty `source_data/` and `results/` placeholder
folders), with the tools run from a separate staging copy exactly as the instructions do:
- LF clone (Python 3.13) and CRLF clone (`core.autocrlf=true`, Python 3.15): every step PASS;
- step 10 (the suite) omitted: it needs the real masters, which the synthetic root lacks; the suite ran separately above;
- step 17's `released` phase STOPs as designed (item 3);
- after the run: `transitory_data/no_pycache_ever` never created; no `__pycache__` in the staging folder or under `src/`.
Logs: `evidence_2026_11_10/PRELIMINARY_smoke_steps_lf_py313.txt` and `_crlf_py315.txt`.

**Negatives** (`neg_smoke.sh`): **11 of 11 STOPped as required:**
- a damaged package file (copy tool and PRE), with nothing written;
- an untracked file at PRE;
- a missing new file at POST, named as MISSING (R-008);
- an extra file at POST, named as UNEXPECTED;
- wrong bytes at POST;
- a second gate copy;
- removing a P with foreign content (it stays);
- creating P when present;
- a path traversal in the manifest (caught by the manifest-shape check before the path check);
- an altered manifest.
Log: `evidence_2026_11_10/PRELIMINARY_negatives_py315.txt`.

**Reminders folded in:** R-008 (missing versus unexpected paths named apart) and R-010 (the failure-output label). R-007
(the seed record's reader names) needs a source change to `src/evaluation/seed_policies.py`; that is not in the reviewed
overlay, so it is not done (section 6).

## 5. Findings from items 1 and 2 (new; each needs the reviewer and, where marked, the owner)

**N1 - CORRECTION, found by test: the MHUP-A install and release records break on a CRLF checkout.**
- **What happens:** `src/methods/_common/release_records.py` refuses any record that is not byte-for-byte canonical (LF)
  JSON. `.gitattributes` protects `results/**` and `source_data/**` from line-ending conversion, but not
  `src/methods/_common/contract_data/install_records/`. On the owner's `core.autocrlf=true` checkout, Git writes those three
  records with CRLF whenever it writes them out: a fresh clone (including every Claude Code task clone after the install), a
  pull that changes them, a checkout or a rebase.
- **Reproduced** in the CRLF smoke clone:
  - as written by the tools: `RECORDS PASS`;
  - after Git rewrites them: `VALIDATE STOP: INSTALL_MHUP_A_V1.json is not its canonical bytes`.
  Evidence: `evidence_2026_11_10/FINDING_records_crlf_reproduction.txt`.
- **Consequence if unfixed:** the Mode H manifest, the release-record tool and every later reader of the records would refuse
  after such a rewrite. T017 (MHUP-B's rehearsal) would meet it first. The slice reviews and T022 could not see it, because
  the overlay's copies were never rewritten by Git.
- **Proposed fix** (the R-011 pattern): one line in `.gitattributes`,
  `src/methods/_common/contract_data/install_records/** -text`, as a 34th modified package file, with a test that checks the
  attribute and a CRLF rewrite negative in the rehearsal.
- **Why I have not applied it:** it changes the reviewed overlay, and `.gitattributes` is a root file. It needs the reviewer
  (RECHECK) and the owner's yes. I recommend it.

**N2 - DONE in the draft: `git status --short` shows the updater swap as a rename.** At step 12, Git shows the deleted
`results_master_v0_1.py` and the new `results_master_v0_2.py` as one `R` line, so "every line starts A, M or D" would wrongly
STOP. The instructions now use `git status --short --no-renames`: 72 lines, all A/M/D (smoke test). The verifier's
`committed` phase already uses `--no-renames`.

**N3 - for F2: `process_check.py` needs `source_data/` and `results/` to exist.** Its project-root test requires the folders
`src`, `source_data`, `results` and `.git`. A synthetic root for T016 therefore needs empty placeholder folders, which hold
no data and are invisible to `git status`. The smoke test used exactly that.

## 6. The approach to F1-F4 (proposals for review; nothing here is decided)

**F1 - settings-deny timing.**
- Proposal: the owner's `.claude/settings.json` deny lines for MHUP-A's tools are committed **after T016 and before Appendix
  J step 0 of the live install**, as their own reviewed, owner-made commit. They are not part of steps 0-19.
- That commit advances `main` but touches neither `src/` nor `tests/` nor any package path. PRE already allows a descendant
  of the base and lists other changes for information, so the frozen base and evidence stay valid. This needs one rehearsal
  negative: PRE on a base plus a settings-only commit passes; plus a package-path change STOPs.
- Proposed deny lines (to be checked with `check_task_commands.py` against real T016 commands and against negative examples):
  `Bash(*Run_Evaluation*)`, `Bash(*Method_Mode_H*)`, `Bash(*mode_h*)`, `Bash(*process_check*)`, `Bash(*install_records*)`.
  `*results_master*` already exists. **Open point:** whether `*process_check*`/`*install_records*` go in at all, given
  rulebook v0.5's T016 allowance. After T016 they can, because no later task needs the two tools until T017 (F9: a new
  decision then).

**F2 - T016's data and lifecycle boundaries (HIGH).** Proposed mapping, for review before T016 is written:

| Design-required check | Where it runs | Why it is equivalent or not |
|---|---|---|
| Appendix J steps 0-18 (barriers, copies, PRE/POST/COMMITTED, records, U) | T016, Claude Code, in a **synthetic root**: a task clone with the data folders removed by a local commit and empty `source_data/` and `results/` placeholders (N3) | the tools only test existence and write U and the records; no data is present to read (rule 2.5 holds) |
| The suite (step 10) | T016 as a **separate, earlier step in a normal task clone** (as T018-T022 did, rule 2.5's test allowance) | the tests read the masters through the project's reader, as before; Claude Code opens nothing |
| `check-no-runs` CLEAN on the ordinary desktop (Claude Code and a console open at the root) | T016 itself gives this naturally: Claude Code's own process is not Python, and the check runs from inside it | equivalent; it is literally that desktop |
| Detection of a live `Run_Experiment.bat` child (6.1 / Appendix L) | **owner-run, outside Claude Code, separately approved**: one console runs a synthetic contract run via `Run_Experiment.bat` (or `python -c "import time; time.sleep(60)"` started from the project root); a second console runs `check-no-runs` and must print REFUSED listing it | Claude Code may not launch it (rule 7, rule 9 and the denials); a launcher-started synthetic run is the real case; the bare sleeper is weaker (it proves rules (b)/(c) only) |
| Windows environment-freeze branch (`python.exe`, DLLs, `Lib/`, the orphan refusal) | the suite's existing synthetic tests on Windows; the first real inventory is Approval 1's | Approval 1 is owner-run anyway; no earlier real-venv inventory is proposed |

Nothing in this mapping overrides rules 2.5 or 9, and no design-required check is dropped: the live-child check moves to the
owner, and is said to.

**F3 - Route A prerequisites** (the owner's preferred order):
1. Item 3 (the `released` phase, the barrier-order proof, the verifier's own negatives, the cold read) on Fable.
2. Rulebook v0.5 and the T016 task file and plan files written. `check_task_commands.py` PASS on the task. The F2 mapping and
   the N1 fix decided.
3. A focused review of rulebook v0.5 and the T016 task (a separate EX message).
4. The owner installs rulebook v0.5 by his own commit. **This advances `main`.** It touches only
   `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md`, so the frozen base stays valid by the F1 argument; if it ever touched a package
   path, the candidate would be re-frozen and its evidence redone.
5. The final candidate frozen and all final evidence produced (item 6). T016 under its own go.
6. The integrated review with the Windows evidence (item 7).

**F4 - staging and step 0 in a task clone.**
- **Staging:** both commits stage from pathspec files (`git add --pathspec-from-file=...`), so `*results_master*` never
  appears on a command line. In T016 the same `add` runs through `cc_clone.py git <clone> add --pathspec-from-file=<file>`.
  Whether `cc_clone.py git` accepts that form, and whether the denials match its text, is checked with
  `check_task_commands.py` when T016 is written.
- **Step 0:** a task clone has no remote, so `git pull --ff-only` is replaced in T016 only by a read-only identity check: HEAD
  equals the commit named in the task, and the tree is clean. The live install keeps the real step 0.

**F5 - F9 noted.** The instructions follow Appendix J's order exactly (F5). F6 and F7 go into the owner's reminders and are
said again at freeze time. F8: E2R-T12's approval is used only in this cloud workspace. F9: T017 gets its own decision.

## 7. What is next, and what it needs from the owner

- **Item 3 (needs your "go"; Fable):** the verifier's `released` phase, the two-commit and barrier-order proofs, the
  verifier's own negatives, the cold read of the instructions against Appendix J. **"Suggest switching to Fable (High) for
  this."**
- **Decisions for you, best taken with the reviewer:**
  1. N1: add the `.gitattributes` line to the package (recommended).
  2. F1: the deny lines after T016 (recommended).
  3. F2: the mapping above, including the one owner-run live-child check.
- **Then, on Opus:** rulebook v0.5 and the T016 task file for their own focused review (Route A), the freeze, and the final
  evidence.
- **Not done and not authorised:** item 3, rulebook v0.5, any settings edit, T016, any install, R-007's source change.
