# Claude primary handover H-1 v1r10r3 (DELTA on H-1 v1r8) - the state at 10 November 2026 (after DOC-13 and R-020 (g))

Written by the Claude web chat (primary designer and coder), 8 November 2026, at the project owner's request, because this chat
has become very long and may end. **r1 (same evening) applies the reviewer's focused documentary check EX_157: corrections C01-C03
and optional O01-O04; the exact changes are in EX_158; r1 was ratified as a working supplement to H-1 v1r8 (RAT-26). r2 (later
the same evening) only updates the pointers after DOC-13 (section 4.8; the newest register, the design's edition, the exchange
row, the section 2 pointer of EX_159 O05) and adds the model guidance for the new chat (section 9, item 5); nothing else
changes. r2 was OWNER-RATIFIED on 8 November 2026 (RAT-28) as a working supplement to H-1 v1r8, replacing r1. r3 (10 November
2026, at the owner's instruction, RAT-29) records the owner's decision R-020 (g) = option (i) and the state on 10 November
(section 4.9); nothing else changes.** It supersedes v1r10 and the 6 November delta (`Claude_Primary_Handover_H1_v1r9_delta.md`), which
stays beside it as history.** It is a working document, not reviewed and not ratified; the ratified handover is still
`doc/HANDOVER/Claude_Primary_Handover_H1_v1r8.md`. Read H-1 v1r8 in full first (its sections 2, 2A and 12 are the rules and the
working knowledge), then this file. Where this delta and a ratified record disagree, the record wins: register v0.25,
the design v0.1r5 as amended by A1, H-2 v1r9, and the owner's decisions in `exchange/`.

US-ASCII, CRLF. The owner is named only as "the project owner" or "hydra3333".

---

## 0. Read this first: the two things that trip a new chat

1. **Commit IDs changed on 6 November 2026.** A history clean-up renumbered the 27 commits of 5-6 November 2026 (section 4.5).
   Any record that cites one of those 27 commits uses its OLD ID (commits outside the 27 were not renumbered); such records include H-1 v1r8's successor documents, register v0.25,
   H-2 v1r9, EX_153-EX_156 and the T022 report. `git show <old id>` fails on them. Translate with
   `exchange/HISTORY_CLEANUP_2026_11_06/commit-map.txt` (old in column 1, new in column 2), which is authoritative and has all 27.
   A selection, 24 of the 27, in short form (the other three are the owner's GAIS commits 442597a -> 129cf32, 456cefd -> a8dc010,
   ece780a -> 8e2c214):

   | old | new | old | new | old | new |
   |---|---|---|---|---|---|
   | 534af84 (EX_149) | a0ebb1f | c498103 (EX_150, A1) | a74fb97 | 8b5acaa (EX_151) | b8db732 |
   | f7d90da (EX_152) | 9605ba7 | 54d161f (y-cruncher added) | 64d5474 | 43dd069 | e25ed7f |
   | c84e2dc | edd4477 | 957a452 | b335dad | 2660e46 | bdcc539 |
   | dbde41f | c907e69 | aa3adbb | ddaf172 | 8e8c1af | e061f12 |
   | 929eff5 | 030a389 | 5a0bb9a | a79def8 | 0432b7f (EX_153/154) | 8e1d74d |
   | b20f2c0 | 95bcb77 | b913e51 (EX_155/156) | bffa962 | 3e0d15d | 2253703 |
   | 8841e62 (DOC12 prep) | 7d3e164 | 377e27a (DOC-12 install) | fafa1ba | 2eb9abb (REPORT_T022) | e963e0e |
   | cbf29bb | 4dac77d | 6eb1fbd | f99de9f | 6b99029 (GAIS move) | 9d28b9f |

   Every **file** hash (SHA-256 of content) in every record is unchanged: the files were not touched. Only commit IDs moved.
   Commits from `cf1c6d9` (6 November, 11:25) onward are unaffected.
2. **The cloud workspace is gone.** Nothing of the previous chat's scratch survives: not the base and development trees, not
   the Python 3.15 venv, not the rehearsal mirrors. Everything needed to rebuild them is committed (section 5). Budget about an
   hour for the rebuild and the first full suite run (H-1 v1r8 section 12.3 and 12.9).

## 1. The position in one paragraph (8 November 2026)

MHUP-A, the first MHUP-1 code package, is **coded, reviewed in two slices (both PASS) and tested on Windows (T022 PASS), and
nothing of it is installed.** Design amendment A1 is ratified. A **new ChatGPT reviewer chat** took over on 6 November after the
previous one ended; the owner accepted it and ratified **H-2 v1r9 and register v0.25** (installed as DOC-12). The owner moved his
GAIS experiments out of `src/` and a history clean-up removed 153 MB of accidentally committed binaries. On 8 November the owner
said "go" for the **one integrated MHUP-A install package**, and the first step is done: the reviewed code was rebuilt on the current
`main`, and the pre-correction run of all 570 tests on each Python had exactly one expected failure (the test that pins
E_1 r3's date; the build now sets it); **the full 570-test suite on the final, date-frozen package is still to be run**
(EX_157 C01). The package itself (manifest, copy tool, verifier with a `released` phase, the
owner's Appendix J instructions, LF/CRLF rehearsals, the Windows rehearsal T016, and the review message, whose number is the
next free one: EX_157 is now the reviewer's check of this handover) is **not yet built**. Section 7 is the exact work list.

## 2. Roles, chats and models (changes since H-1 v1r8)

- **The ChatGPT reviewer:** a **new chat since 6 November 2026**, started from the H-2 v1r9 blurb. It accepted the role on H-2
  v1r8, verified the rights region, found five documentation corrections (EX_153), passed Claude's 19 blind verification
  questions (EX_155; Claude's sealed key and comparison in EX_156). It has **not** executed the project's tests itself for any
  MHUP-A round; its reviews are static plus diff reproduction plus Claude's logs. It has said (EX_155 Q15) it intends R-2
  reproduction and R-4 oracles for the integrated review and listed what it needs (section 7, item 7).
- **Claude:** the same cloud chat since HO-2 (4 November). It commits only in `exchange/` and `CLAUDE_CODE_WORKING_FOLDER_TREE/`.
  **Model:** the owner switched this chat to **Fable 5.1 on 8 November 2026 at about 19:00** for the handover work; the
  commit attribution line is therefore `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>` from then on (Opus 5.5 before).
  A new chat uses whatever model the owner selects and cannot see it; MC-1 still applies (recommend Opus or Fable per step, one
  line; Fable for HIGH core, BLOCKER findings, unexplained STOPs, cold reads).
- **Claude Code:** unchanged role (local runner only). Rulebook v0.4; `cc_clone.py` v0.4. Tasks T018, T020 and T022 PASSED; T019
  STOPPED correctly (deny list); T021 was withdrawn unrun.
- **The owner's own commits:** since 5 November the owner has made many commits of his own outside the reviewed line (his GAIS
  "OUTLANDISH" thought experiments, now under the top-level `GAIS/`; `.gitignore` lines; `create_venv.bat`; the
  `pyahocorasick` dependency line). They are owner material, unreviewed, and recorded as facts only. An OUTLANDISH ChatGPT chat
  works with the owner on that; it is not part of this project's review process.

## 3. The hard rules (unchanged; H-1 v1r8 sections 2 and 2A are the text)

Data folders never opened; no outcome of Powerball >= 1577 or Oz Lotto >= 1694 displayed or computed with; the one results
source is Lotterywest-GOV (`www.lotterywest.wa.gov.au`, HTTPS) and Claude never contacts any lottery site; the orphan marker is
never cleared; the science switches stay as they are; Claude commits only in `exchange/` and `CLAUDE_CODE_WORKING_FOLDER_TREE/`
with named paths; US-ASCII, CRLF for EX/task/roadmap/reminder/handover files, LF for code; never the owner's name; a STOP is a
STOP (R-018 (a)); no install, real-data run, holdout opening, Mode H, updater run, weekly session or dependency change without the
owner's separate go. **Checkpoint often**: commit tools and a checkpoint note before every review message.

## 4. Events since 6 November 2026 (the v1r9 delta covered 4-6 November; both are summarised in the register v0.25 section)

### 4.1 The reviewer takeover (EX_153-EX_156, 6 November)
- EX_153: the new reviewer's takeover assessment; TAKEOVER-C01 to C05 (documentation errors in Claude's candidates: C01 was the
  order of A1's ledger publication and validation, which Claude had reversed) and O01 (CRLF copies from `git archive`).
- EX_154: all five applied (candidate 2); clarifications; Claude's verification questions Q1-Q19 with a sealed answer key.
- EX_155: C01 RECHECK PASS; C06 (wording) and O02 (editorial); the 19 answers, blind, with sources.
- EX_156: the key published (hash matched); all 19 agree; C06 and O02 applied (candidate 3).
- **RAT-25 (owner, 6 November, about 01:53):** "ok review is ok. Ratify H-2 v1r9 and register v0.25 candidate 3 ratified."
- **DOC-12 (owner, `377e27a` = new `fafa1ba`):** `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r9.md` (+ blurb) and
  `doc/RATIFICATION_REGISTER_v0_25.md` installed; the candidate copies removed from `doc/`; Claude verified from GitHub
  (`exchange/DOC12/install_doc12.py verify`: PASS).

### 4.2 Windows evidence
- **T022 PASS** (REPORT_T022, old `2eb9abb` = new `e963e0e`): slice 2 candidate v1r2 (the reviewed one), 570 tests, 4 allowed
  symlink skips, 24 min 37 s, in a task clone of `main` with the owner's `src/GAIS` files present. One recorded deviation: the
  runner started step 8 detached with output redirected, to time it; command and arguments unchanged. Claude accepted it; future
  task files say "run in the foreground" and the runner prints its own elapsed time.
- **T021 withdrawn** (v1r1; T022 covers the later candidate).

### 4.3 The owner's decisions of 6 November
- **DEP-1:** `pyahocorasick` is installed in the project venv and approved as a dependency ("we keep it"). The environment freeze
  records it at Approval 1. To go into register v0.26.
- **GAIS-1:** GAIS moved from `src/GAIS/` to the top-level `GAIS/` (owner commit, now `9d28b9f`), outside MHUP-A's code closure;
  y-cruncher untracked by `.gitignore`. To go into register v0.26.
- **The reviewer's bundle-restore test:** waived by the owner (recorded in CLOSEOUT.md).
- **Loss of 15 commit signatures** in the history clean-up: accepted by the owner (recorded by the reviewer in its Gate A
  recheck).

### 4.4 The reviewer's process documents on the clean-up
`exchange/HISTORY_CLEANUP_2026_11_06/`: the reviewer's proposal, assessment (B01-B03, C01-C05) and Gate A RECHECK (PASS); Claude's
Gate A evidence package; `commit-map.txt`; `CLOSEOUT.md`.

### 4.5 The history clean-up (6 November, 11:00-11:30), led by Claude at the owner's choice
- Removed from all history: `src/GAIS/OUTLANDISH_01/y-cruncher v0.8.7.9547b/` (246 files), the `ycruncher_digits` placeholder and
  two 1 MB `.bin` files. Tool: `git filter-repo --refs 54d161f^..main --invert-paths ...` on a fresh mirror.
- `main` 6b99029 -> **9d28b9f**; tree `e8be598...` identical; 389 commits unchanged; 27 renumbered; fresh clone 45.6 MiB (from
  82.8). Gates B-E run by the owner exactly as written (one pinned `--force-with-lease`; `reset --soft`; no file touched). The
  owner's local `.git` then cleaned (983 -> 48.6 MiB; `fsck` clean), with a copy of `.git` kept in `E:\TEMP\git_backup_before_gc`
  and the pre-cleanup bundle `E:\TEMP\repo_before_cleanup.bundle` (the only copy of the old history).
- **Any clone made before 6 November 11:25 must be re-cloned, never merged back.** Claude's own workspace clone was replaced.

### 4.6 The owner's later commits (6-8 November)
19 owner commits of OUTLANDISH work under `GAIS/`, plus `.gitignore` lines (`/GAIS/OUTLANDISH_01/large_artifacts/` and
config-file patterns) and a new root file **`create_venv.bat`** (creates the venv if absent; never overwrites; installs nothing).
No change under `src/`, `tests/`, `doc/` or the data folders. Main was `009c985` at 15:49 on 8 November.

### 4.7 The integrated package started (8 November, 18:13 "please check the github repo and then go")
- The development tree was rebuilt on `009c985` with the committed tools: identical to the reviewed v1r2 overlay in 66 of 70
  files; the four differences are `.gitignore` (the MHUP-A block now appended after the owner's new lines) and the three files
  carrying E_1 revision 3's date (C01-EFF).
- **Pre-correction suite on the rebuilt tree, Linux, Python 3.13.18 and 3.15.0b4: 570 ran, 569 passed, 0 skips, on each.** The one
  failure on each is `test_e1r3_revision3`, which pins the `effective_date` to the candidates' 2026-11-04, an expected consequence
  of C01-EFF. `integrated/build_dev_integrated.sh` sets that test's date to the package date by a counted edit; **only that module
  (8 tests) was rerun** after the correction, passing on both Pythons. **The full 570-test suite on the final, date-frozen package
  has not yet been run**; it is part of the final evidence (section 7, item 6). The original logs are kept unaltered:
  `exchange/CLAUDE_WEB_TOOLS/mhupa/integrated/evidence/` (labelled preliminary). These Linux runs are on 3.15.0b4; the owner's
  Windows evidence (T022, Python 3.15.2) is separate.
- Commits `4bae8f4` (PLAN.md) and `1fe7b02` (checkpoint).

### 4.8 After this delta was first written: RAT-26, DOC-13 and RAT-27 (8 November 2026, 19:40 to 20:45)
- **RAT-26:** the owner ratified H-1 v1r10r1 (this delta's previous revision) and its blurb as working supplements to H-1 v1r8,
  after the reviewer's EX_157 (corrections) and EX_159 (recheck PASS).
- **DOC-13**, a documentation round at the owner's request (EX_160; the reviewer's EX_161: three corrections, applied in EX_162;
  the reviewer's further check of EX_162: PASS, no EX_163 needed), **ratified by the owner (RAT-27)** and **installed at `52b6de8`**
  (Claude verified it from GitHub: `exchange/DOC13/install_doc13.py verify` PASS). It installed:
  - `doc/RATIFICATION_REGISTER_v0_26.md`: **the newest register**; its new section records everything from DOC-12 to DOC-13
    (T022, DEP-1, GAIS-1, the history clean-up, RAT-26, RAT-27, the integrated package's preliminary state, R-020 (g) open);
  - `doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r6.md`: **the design's current edition**, v0.1r5 with A1 folded
    into 5.2, 5.4 and L-H2, Lotterywest-GOV named, section 8's tool list updated; A1 stays the ratified record of the amendment;
  - `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r10_delta.md` and blurb: the reviewer's working supplement to H-2 v1r9;
  - the new-method template **draft 5** (`doc/METHOD_TEMPLATE/`): what MHUP-A changes for a new method once installed;
  - the root `README.md` (a `GAIS/` row);
  - 34 superseded editions moved into `superseded/` folders (`exchange/DOC13/MOVES.txt`; H-2 v1r4 stays because H-2 v1r8 sends
    reviewers to it).
- **Then decided:** R-020 (g), option (i) (section 4.9). The integrated MHUP-A work list (section 7) is otherwise unchanged.

### 4.9 The state on 10 November 2026
- Nothing on the main project changed between 8 and 10 November: no new EX message (the newest is EX_162), no task file or
  report. The owner installed H-1 v1r10r2 at `06c26a6` (Claude verified it: `install_h1_v1r10r2.py verify` PASS) and committed
  OUTLANDISH material only (`fe13d31`, under `GAIS/` and `doc/GASI_thought_experiments/`; owner material, unreviewed; OUTLANDISH
  is nearly parked).
- **R-020 (g) DECIDED (owner, 10 November 2026, about 18:30): option (i).** Claude Code's rulebook v0.5 allows `process_check.py`
  and `install_records.py` ONLY inside T016's synthetic, non-pushing task clone, ONLY run from the package's staging folder, ONLY
  under the T016 task file, with the reviewer's EX_157 section 3 conditions: every other safeguard unchanged; `.claude/settings.json`
  denials not bypassed; `check_task_commands.py` passing on the actual task; no change to the main repository; the rulebook
  change reviewed with the package; and T016 still needs the owner's own separate go.
- **The next step is Claude's: section 7, item 2 (the package builder), on Opus.** No reviewer input is needed before it; the
  reviewer's turn is the integrated package's review request (at the next free EX number, EX_163 if nothing intervenes).

## 5. Where everything is (all committed; paths from the repository root)

| What | Where |
|---|---|
| The reviewed MHUP-A candidate (slice 1 + slice 2, v1r2) | `exchange/EX_151_Claude/MHUPA_Slice2_Review_v1r2.zip` (SHA-256 `67701220...`); its `overlay/` = 70 files against base `2061055`; `REMOVED_FILES.txt` = `src/results_master_v0_1.py` |
| The build tools (slice 1 then slice 2) | `exchange/CLAUDE_WEB_TOOLS/mhupa/`: `build_dev_slice1.sh`, `build_dev_slice2.sh`, `apply_slice*.py`, `edit_tests_slice*.py`, `make_e1r3.py`, `make_updater_v0_2.py`, `slice1_new/`, `slice1_edited/`, `slice2_new/`, `slice2_edited/` |
| **The integrated build** | `exchange/CLAUDE_WEB_TOOLS/mhupa/integrated/build_dev_integrated.sh BASE DEV TOOLS DATE` (BASE = `git archive HEAD` of current main; TOOLS = `exchange/CLAUDE_WEB_TOOLS/mhupa`; DATE = the package date, C01-EFF). `PLAN.md` beside it is the work list and checkpoint log |
| The suite runner (570 tests, expected counts) | `exchange/CLAUDE_WEB_TOOLS/mhupa/slice2_checkpoint/RUN_MHUPA_SLICE2_SUITE.py --repo <tree>`; about 25 min per Python on Linux |
| Mutation tools | `mhupa_slice1_mutations.py TREE [--only N]` (90 mutants) and `mhupa_slice2_mutations.py TREE [--only N]` (103); a full chain is about three hours; run new mutants alone first |
| Earlier package templates to adapt | `exchange/CLAUDE_WEB_TOOLS/wf1/verifier_template.py` (pre/post/committed), `wf1/suite_template.py`, `wf1b/build_wf1b_pkg.py`, `wf1b/e2e_wf1b.sh` (LF/CRLF rehearsal with negatives), `wf1b/make_t01N.py` (task-file generators) |
| Claude Code | `CLAUDE_CODE_WORKING_FOLDER_TREE/tools/cc_clone.py` v0.4 (`make`, `unzip`, `overlay --plan`, `verify-overlay`, `git`, `remove`, `commit-report`); rulebook `CLAUDE.md` v0.4; task files and plan files in `inbox/`; reports in `outbox/`; **always** run `python3 -I exchange/CLAUDE_WEB_TOOLS/check_task_commands.py <repo> <task>` before sending a task |
| The ratified records | `doc/RATIFICATION_REGISTER_v0_26.md` (newest register; its new sections are just before "Interpretation and verification"); `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r9.md` with its v1r10 delta; `exchange/MHUP1_design_amendment_A1_RATIFIED.md`; the design `doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r6.md` (A1 folded in; Appendix J = the install procedure) |
| The exchange | when r2 was written the newest message was EX_162; **always check `exchange/` for the highest number in use and
take the next one** |
| Owner lists | `exchange/OWNER_ROADMAP.md` (NOW line), `exchange/OWNER_REMINDERS.md` (R-019, R-020 (a)-(g), R-023 open) |
| History clean-up | `exchange/HISTORY_CLEANUP_2026_11_06/` (CLOSEOUT.md, commit-map.txt) |
| DOC-12 | `exchange/DOC12/` (installer script, README, diffs) |
| Handover folder | `exchange/HANDOVER_2026_11_06/` (this file, its blurb, the superseded v1r9 delta, the H-2 v1r9 candidate history, README) |

## 6. Decisions and obligations the integrated package must carry (consolidated)

1. **A1 (ratified 5 Nov):** the Mode H score ledger: read outcomes once; compute; **publish whole, create-only; then validate
   the published ledger**; then `SCORE_COMPLETE` (digest); report resumed file by file; seal. Three recovery states (A1 s.4). A
   refused published ledger is a STOP. The corrective scoring run is MHUP-B's (A1 s.6). Cite A1; never rely on design 5.2/5.4/L-H2's
   superseded text.
2. **C01-EFF:** E_1 r3's `effective_date` = the integrated package's preparation date, set when the package is frozen for review
   (the DATE argument); it changes the two `entry_0003.json` files, `archive/methods/E_001/r2/README.md` and the pinned test;
   rebuild and rerun everything after setting it. The release record alone dates a release.
3. **R-020 (a):** the manifest's `release_entries` = E_1 revision 3 for POWERBALL and OZLOTTO (`retires` empty); released set
   after install = 39 baseline + E_1 r3 = 40 per game. **(b):** the environment freeze refuses an orphan file in site-packages;
   the fix is a reviewed step. **(c):** the owner chooses, at approval, to rerun the Windows POC suite after the
   `Run_Experiment.bat` change or accept it unrun. **(d):** rebased onto current main; the owner's `.gitignore` lines survive
   (done in the rebuild). **(e) DEP-1** and **(f) GAIS-1** decided (section 4.3). **(g), DECIDED option (i)** (section 4.9); see section 7, item 6 (the
   T016/rulebook conflict).
4. **R-019:** (a) complete-first-update and study-version-advance rule, (d) the date, (e) real-emitted-bytes reconciliation: check
   again in the assembled behaviour; (b) `FREEZE_LINE_V1`'s full shape and (c) the FINAL/CATCH_UP mutant: MHUP-B.
5. **EX_152 s.5 and EX_155 Q12:** the integrated review assesses the **assembled** behaviour: integration, records, installer and
   verifier, release gating, LF/CRLF reproducibility, Windows and safety rehearsals (T016), the outstanding Windows evidence;
   **(ix) COMMITTED PASS** proves both commits, the barrier order (U, then E and P, then the gate) and record/repository agreement.
6. **MHUP-B timing (design 4.4):** installed before Approval 1, or only after a game's Mode H seal, never between; the owner
   chooses and the integrated install plan states it.
7. **R-018 (a), (d), (h):** retries after a STOP; interrupted sessions; the weekly session's authorisation (Q9-E4): into MHUP-B's
   checklist and register v0.26.
8. **Register v0.26 must record:** T022 PASS and T021 withdrawn; DEP-1; GAIS-1; the history clean-up and the crosswalk; the
   owner's `create_venv.bat` and OUTLANDISH commits as facts; the integrated package's review and install; R-018; the model
   switch is not a register matter.
9. **Q7 (OPEN):** the display restriction on holdout draws after Mode H: decide before Approval 2; recommendation: keep it.
10. **The owner's backup** of `results/` and `source_data/` (R-015): to confirm at MHUP-A's approval.

## 7. The work list for the integrated MHUP-A package, in order (the detail is `integrated/PLAN.md`)

Model guidance per MC-1 is given in brackets; the owner may switch the chat at any time. **The order follows EX_157 C03: every
piece of final evidence (suites, mutations, LF/CRLF rehearsals, T016) is produced on the date-frozen final candidate, after the
owner's R-020 (g) decision; anything run earlier is preliminary and labelled so.**

1. **Rebuild the trees** [any model]: `git archive HEAD | tar -x -C BASE` (main at or after `1fe7b02`), then
   `build_dev_integrated.sh BASE DEV exchange/CLAUDE_WEB_TOOLS/mhupa <DATE>`. Python 3.15 venv: H-1 v1r8 section 12.3 (`uv`;
   install the `DIRECT_PACKAGES` of `install_upgrade_dependencies_into_venv.bat`, which now include `pyahocorasick`; nothing of
   the project imports it, so the suite does not need it). A preliminary full-suite run on both Pythons is worth doing (expect
   570/570 with the date fix), but the evidence that counts is item 6's.
2. **The package builder** `integrated/build_mhupa_pkg.py` [Opus]: from BASE and DEV it writes `repo_overlay/`
   (the 70 files, LF), the **package manifest** (JSON: `package` = `MHUP_A`; `base_commit`; `new`, `modified`, `deleted`
   paths with LF SHA-256; `gate_files` = the 10 of section 7a; `release_entries` and `retires` and
   `registry_entries_added` in the shape `install_records.load_manifest` reads; the SHA-256 of the package's
   `process_check.py`), the **copy tool** (`copy --part gate|rest --manifest M --repo R`, standard library, refuses any path
   not listed, checks each written file), the **verifier** (from `wf1/verifier_template.py`: `pre`, `post`, `committed`, plus a
   new **`released`** phase), the suite runner, and `INSTALL_INSTRUCTIONS.md` = Appendix J steps 0-19 as exact CMD lines.
   - 7a. **The step 6 gate files: ten** (computed from `contract_dispatch.py`'s import closure, restricted to files the package
     changes or adds; all under `src/methods/_common/`; EX_157 C02 corrected an earlier count of eleven). Eight changed: `contract_dispatch.py`, `contract_forecast.py`, `contract_receipts.py`,
     `contract_records.py`, `contract_runner.py`, `contract_task.py`, `contract_vocab.py`, `game_draws_reader.py`. Two new:
     `master_versions.py`, `owner_records.py`. The builder recomputes this closure and asserts it equals the manifest's list.
   - 7b. The tools the instructions call, all run from the **staging folder** with the venv's Python `-I -B
     -X pycache_prefix=<never-existing folder>`: `process_check.py check-no-runs --root R --install MANIFEST`,
     `take-install-lock --root R --package MHUP_A`, `release-install-lock --root R --package MHUP_A`;
     `install_records.py install-record|release-record --root R --package MHUP_A --manifest MANIFEST`.
3. **The `released` phase and the two-commit proof** [Fable], and the verifier's negatives: the release commit's only parent is the package commit; it adds
   exactly `RELEASE_MHUP_A_V1.json`; the record names E_1 r3 for both games, the install record's digest, a local date not before
   the install record's; E and P absent; U's content; the records agree with the repository (EX_148 (ix)). Plus the verifier's
   own negatives (missing or wrong-byte file at POST; a wrong install record; an extra file in the release commit; the wrong
   parent) and a **cold read** of the instructions against Appendix J by a fresh helper.
4. **The owner's R-020 (g) decision: DONE, option (i)** (section 4.9), before the rulebook change or the T016 task file is written.
5. **The rulebook v0.5 and the deny lines** [Opus], written to the owner's choice (option (i)): rule 7 gains `create_venv.bat` and
   the narrow T016 allowance of section 4.9; rule 1 names Lotterywest-GOV (R-017); the owner's `.claude/settings.json` deny lines
   are the owner's edit (register v0.24 future action 1).
6. **Freeze the date (C01-EFF), build the final candidate, and produce ALL final evidence on it** [Opus; Fable for an
   unexplained failure]: the full 570-test suite on both Pythons; both mutation chains; LF and CRLF end-to-end rehearsals on a
   frozen mirror (steps 0-18; step 19 omitted), each negative STOPping; then T016 on Windows under the owner's go. Any change
   to the package after this point means a new candidate and the evidence is redone.
   **About T016 (R-020 (g)):** Appendix J's steps 2, 3, 12, 16 and 18 run
   `process_check.py` and `install_records.py`, and **rulebook v0.4 rule 7 forbids the runner from running either in any
   command.** Options: (i) rulebook v0.5 allows those two tools **only inside a task clone, only from the package's staging
   folder, only under a task file**, reviewed with the package; or (ii) the owner runs T016's steps himself, Claude Code only
   preparing the clone. Also: `Bash(git -C *)`, `git add*`, `git commit*` and `git rm*` are denied, so every Git step in the clone
   goes through `cc_clone.py git`; `*results_master*` is denied, so the updater file is copied by the copy tool from the
   manifest, never named on a command line; `check_task_commands.py` checks all of it. The reviewer (EX_157 section 3) prefers
   (i) under conditions: explicit owner approval; only those two tools, only in T016's synthetic clone, from the staging folder;
   every other safeguard unchanged; the settings denials not bypassed; `check_task_commands.py` passing; no change to the main
   repository; T016 still needs its own owner go. If (i) cannot be done cleanly, choose (ii).
7. **The review message, at the next free EX number** [Opus], with: the ZIP and manifests; base and target identities; the test and mutant inventories
   with logs; T022 and T016 evidence; DEP-1 and GAIS-1; A1 cited; MHUP-B's timing route stated; and **an explicit statement of
   which offline tests the owner authorises the reviewer to execute** (EX_155 Q15 asked for it). Expect a full R-2/R-4 review,
   possibly with the reviewer's own reproduction. If T016 has to follow the review instead, say so: the review is then
   provisional as to Windows, and a follow-up evidence RECHECK comes before any install.
8. **After PASS and the owner's separate approval:** the install by Appendix J (two commits), Claude's verification from GitHub,
   register v0.26 and the full H-1 and H-2 editions in a documentation package.
9. **Then:** MHUP-B (design section 6; the A1 s.6 route; `FREEZE_LINE_V1`; R-018), WF-1C, the method waves (the roadmap).

**Planning dates:** ST-5's target (Mode H and the weekly session installed by about 13-15 November 2026) is now unlikely; FB-1
applies (the schedule slips, no review or rehearsal is cut). Say so to the owner when the package goes to review.

## 8. Working lessons (add to H-1 section 12 at the next full edition; the v1r9 delta's lessons are repeated here)

- The deny list matches command **text** (`*.bat*`, `*results_master*`, `*lottery*`, `*unlink*`, `*rmtree*`, `git -C *`, `git
  add*`, `git rm*` ...): denied paths go in plan files; Git in a clone goes through `cc_clone.py git`; check every task file.
- The `test_e1r3` guard refuses the token `effective_date` in unexpected source text (keep it out of comments and docstrings);
  the same test pins E_1 r3's date, so the build sets it (section 4.7).
- Counted edits only (assert an anchor occurs exactly once). Diffs between candidates exclude removed files on both sides.
- Mutation honesty: "no test plants it" is non-detection, not equivalence; print each equivalent's reason.
- An invalid record is a refusal (`ModeHRefused`), never an escaping `ValueError`. Oz Lotto's ledger never stores supplementaries.
- Token economy: new mutants alone with `--only`, then one final chain; rerun only the changed module after a one-line change and
  say so.
- When the reviewer checks your documents, expect real catches (TAKEOVER-C01 reversed A1's order). State A1's order exactly.
- Hashes: Git stores these markdown files LF; `git archive` on Windows gives CRLF copies; A1 and the EX messages are stored CRLF;
  always say which bytes a hash identifies.
- A long-running Windows step in a task file: say "run in the foreground" and have the tool print its elapsed time.
- History rewrites: rehearse on a fresh `--mirror`; limit `--refs` to the affected range; prove tree identity and reachability;
  pinned `--force-with-lease`; `reset --soft` locally; a bundle holds reachable history only.
- The owner commits often and outside the reviewed line (GAIS, `.gitignore`, root `.bat` files): **always `git fetch` and look
  at what changed outside `exchange/` before building on main**, and check `.gitignore` and the root files every time.

## 9. The first hour in a new chat (replaces H-1 v1r8 section 12.9's tail)

1. Clone; read H-1 v1r8, this delta, register v0.25's new section, A1, H-2 v1r9 sections 0 and 6, EX_152-EX_156,
   `integrated/PLAN.md`, the roadmap and the reminders. Check the hashes this delta quotes with a tool (translate commit IDs
   with the crosswalk).
2. Give the owner the first-reply summary HO-2 asks for (H-1 v1r8 section 0): implemented / designed / ratified / reviewed-not-
   installed / open; what you are and are not authorised to do; discrepancies.
3. Do not build, run tests, write task files or commit until the owner has your reply checked by the reviewer and says go
   (the reviewer may ask questions; answer blind).
4. Then rebuild (section 7, item 1) and continue the work list from where `integrated/PLAN.md`'s checkpoint log stops.
5. **Models (the owner plans to start the new chat on Opus):** stay on Opus for the takeover and for section 7 items 1 and 2; at
   item 3 (the `released` phase, the two-commit and barrier-order proofs, the cold read), and for any BLOCKER-level finding or
   unexplained STOP, say "Suggest switching to Fable (High) for this" and wait for the owner's "go"; say when the Fable work is
   done. The owner's R-020 (g) decision is made (option (i); section 4.9).

## 10. Integrity

Every fact above was checked against the repository at `1fe7b02` (8 November 2026) or taken from the records named, and the
reviewer checked v1r10 against the repository at `b38bd0a` (EX_157: crosswalk, A1 order and boundaries PASS; C01-C03 applied
here). T016 is not run; the final full suite is not run; the integrated package is not built; nothing is installed. The previous chat's unfinished thought is nowhere else: what is
not in this file, in `integrated/PLAN.md`, in the reminders or in the roadmap does not exist.

End of H-1 v1r10r3 delta.
