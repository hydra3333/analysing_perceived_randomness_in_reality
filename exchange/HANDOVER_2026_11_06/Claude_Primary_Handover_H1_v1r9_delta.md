# Claude primary handover H-1 v1r9 (DELTA on H-1 v1r8) - the state at 6 November 2026

Written by the Claude web chat (primary designer and coder), 6 November 2026, at the project owner's urgent request, as risk
management: the ChatGPT reviewer chat reached its conversation limit on 6 November 2026 without writing its own handover, and
this Claude chat may also end without warning. This is NOT a full new edition and it has NOT been reviewed (there is no
reviewer chat at present). Read it together with H-1 v1r8:

1. `doc/HANDOVER/Claude_Primary_Handover_H1_v1r8.md` (installed with DOC-11 at 3d4fa3c): the full rules, roles, history and
   working knowledge up to 3-4 November 2026. Still binding, except where this delta records a later ratified change.
2. This delta: everything from the end of HO-2 (4 November 2026) to 6 November 2026.
3. The introductory blurb beside this file (`Claude_Primary_Handover_H1_v1r9_introductory_blurb.md`) is what the owner pastes
   into a new Claude chat.

Where this delta and H-1 v1r8 disagree, the ratified record wins: the register, the ratified design v0.1r5 as amended by A1
(`exchange/MHUP1_design_amendment_A1_RATIFIED.md`), and the owner's decisions recorded in `exchange/`. This delta only points
to them. The owner may install these files into `doc/HANDOVER/` later; Claude commits only in `exchange/` and
`CLAUDE_CODE_WORKING_FOLDER_TREE/`.

US-ASCII, CRLF. The owner is named only as "the project owner" or "hydra3333".

---

## 1. The one-paragraph position (6 November 2026)

MHUP-A (the first MHUP-1 implementation package) is coded and reviewed in two slices, and **both slices have PASSED code review**:
slice 1 in EX_146, and slice 2 (candidate v1r2) in EX_152. **Amendment A1 is RATIFIED by the owner**: the Mode H score ledger is
published whole, once, and the corrective scoring run is deferred to MHUP-B. **Nothing of MHUP-A is installed.** The next work is:

1. the owner's Windows reports for T021 (v1r1) and T022 (v1r2), which are still to come;
2. the **one integrated MHUP-A install package** (slice 1 plus slice 2), which has its own full review.

The reviewer who reviewed both slices has gone. A new ChatGPT reviewer chat must be started with the reviewer handover that
Claude prepared beside this file (H-2 v1r9). It must check it, and accept its role, before it reviews the integrated package.

## 2. What is authorised and what is not (unchanged in kind since H-1 v1r8)

**Authorised:**
- design and code work in Claude's cloud workspace;
- review packages sent through the owner;
- task files for Claude Code, which only rehearses and tests in throw-away clones that cannot push;
- records and handover work in `exchange/` and `CLAUDE_CODE_WORKING_FOLDER_TREE/`.

**Not authorised** (each needs the owner's separate, explicit go, after its review):
- installing anything into `src/`, `tests/` or `doc/`;
- disabling a development or interlock flag;
- any real-data run;
- opening or using a holdout outcome (Powerball draw 1577 or later, Oz Lotto draw 1694 or later);
- Mode H opening or scoring;
- any results-update run;
- a dependency change;
- MHUP-B;
- clearing the orphan marker;
- turning any science switch on.

EX_152 section 5 restates these limits.

## 3. The hard rules, as they bind the next chat (summary; H-1 v1r8 sections 2 and 2A are the full text)

- **Data:** never open anything under `source_data/`, `results/` or `transitory_data/`. Never display, paste or compute with an
  outcome of Powerball draw 1577 or later, or Oz Lotto draw 1694 or later. Tests use invented masters in temporary folders.
- **Results source:** the one results source is Lotterywest-GOV: HTTPS, exact hostname `www.lotterywest.wa.gov.au`. Never
  `oz.lotterywest.com`, The Lott, an API or a new scraper. Claude never contacts any lottery website at all.
- **Commits:** Claude commits only in `exchange/` and `CLAUDE_CODE_WORKING_FOLDER_TREE/`. It stages named paths only (never
  `git add -A` or `git add .`) and pushes only its own commits. The owner commits everything else.
- **Text format:**
  - US-ASCII;
  - CRLF for EX messages, task files, `OWNER_ROADMAP.md`, `OWNER_REMINDERS.md` and handover documents;
  - LF for repository code (the repository's `.gitattributes` governs).
- **Names:** never write the owner's personal name in a file. Write "the project owner" or "hydra3333".
- **Stops and flags:** a STOP is a STOP (R-018(a) states the retry rule). The orphan marker is never cleared by Claude or Claude
  Code. The science switches stay `False` and the allowlist stays empty.
- **Commit attribution lines** (the session link changes with each chat):
  ```
  Co-Authored-By: Claude <model> <noreply@anthropic.com>
  Claude-Session: <this chat's session link>
  ```
  Commit as `git -c user.name="Claude (web chat)" -c user.email="noreply@anthropic.com" commit ...`.
- **Model rationing** (owner, 5 November 2026, until the weekly reset on Tuesday 10 November 2026): Fable only for critical core
  work (a new HIGH design, the core of a HIGH code module, a BLOCKER-level finding, an unexplained STOP); Opus for everything else.
  The core functionality comes first; administrative controls can be simplified later. The owner plans a KISS (simplicity) review
  after implementation (R-014). Ratified requirements remain binding meanwhile. MC-1 (register v0.24): say which model you
  recommend at each step, in one line.
- **Checkpoints:** take them often. Commit a checkpoint note and every working tool to `exchange/CLAUDE_WEB_TOOLS/` before each
  review message. The cloud workspace is lost when a chat ends; only the repository survives.

## 4. Events since H-1 v1r8 (in order; each is recorded in `exchange/`)

| Date | Event | Record |
|---|---|---|
| 4 Nov | DOC-11 installed at 3d4fa3c; HO-2: the replacement Claude chat verified (Q1-Q9 PASS); the owner declared HO-2 complete and authorised normal work; direction document v0.3r1 installed at dfc2d13 | EX_138-EX_140, R-016, R-018 |
| 4 Nov | The owner chose two review slices, then one integrated MHUP-A install package | roadmap 10c |
| 4 Nov | Slice 1 v1 sent (version-2 master rules, E_1 revision 3, one data kind, binding and ticket gates, barrier P; 506 tests) | EX_141 (32cc0e3) |
| 4 Nov | ChatGPT RECHECK: three blockers (frozen-pin binding, fail-closed evidence, the full ledger grammar for every ledger), C01-C03 | EX_142 |
| 4 Nov | Owner decision C01: E_1 revision 3's `effective_date` is the integrated package's preparation date; the release record alone dates a release | EX_143, R-019(d) |
| 4-5 Nov | Slice 1 v1r1 (507 tests; 87 mutants: 80 caught, 7 equivalent) and v1r2 (blank JSONL lines, strict CSV quoting; 90 mutants: 81 caught, 9 equivalent, 0 survived) | EX_143 (5573035), EX_144, EX_145 (3d825b3) |
| 5 Nov | **Slice 1 PASS** (review checkpoint only) | EX_146 (8aa16c3) |
| 5 Nov | T018: slice 1's 507 tests on Windows in a task clone: PASS; the committed real ledgers pass the full ledger grammar | REPORT_T018 (110eb41) |
| 5 Nov | Slice 2 v1 sent: the Mode H batch kind and families, `Method_Mode_H.py`, the closure and environment freeze, the records tool, `process_check.py`, updater v0.2, the launchers, the freeze-before-outcome rule, rulebook v0.4; 561 tests | EX_147 (2eb6dfb) |
| 5 Nov | T019 STOPPED correctly at step 5: its command lines named paths that `.claude/settings.json` denies (`*.bat*`, `*results_master*` and others). Fixed by `cc_clone.py` v0.4 (`overlay --plan`, `verify-overlay`) and by `exchange/CLAUDE_WEB_TOOLS/check_task_commands.py`; T020 replaced it | REPORT_T019, d2c5a18 |
| 5 Nov | T020: slice 2 v1's 561 tests on Windows: PASS | REPORT_T020 (cba73e5) |
| 5 Nov | ChatGPT RECHECK of slice 2 v1: B01 (the per-pair ledger against design 5.2), B02-B04, C01, (iii-b) | EX_148 and its evidence supplement (b45cb0d) |
| 5 Nov | Owner decisions: B01 by route (B), the one-step atomic ledger by design amendment A1; (iii-b) corrective scoring run deferred to MHUP-B with its route named | EX_149, A1 section 6 |
| 5 Nov | Slice 2 v1r1 (569 tests) and the A1 draft sent | EX_149 (534af84), TASK_T021 |
| 5 Nov | ChatGPT: B02-B04 and C01 PASS, A1 favourable, one new blocker B05 (the resumed scorer's plan and completion bindings) | EX_150 |
| 5 Nov | **The owner RATIFIED A1** ("i hereby authorise and ratify that A1") | `exchange/MHUP1_design_amendment_A1_RATIFIED.md` (c498103), R-021 |
| 5 Nov | Slice 2 v1r2 (B05 corrected; 570 tests; 5 targeted mutants caught) | EX_151 (8b5acaa), TASK_T022 |
| 5 Nov | **Slice 2 PASS** (v1r2): the integrated package may be prepared for its own review; not an install authorisation | EX_152 (f7d90da) |
| 5 Nov | Owner's own commits outside the reviewed process: `src/GAIS/` and `doc/GASI_thought_experiments/` (the "outlandish" thought experiments), `.gitignore` lines for GAIS `.bin` files, and **`pyahocorasick` added to `DIRECT_PACKAGES` in `install_upgrade_dependencies_into_venv.bat`** (f1883df) | 456cefd, ece780a, f1883df, 43dd069 |
| 6 Nov | The ChatGPT reviewer chat reached its conversation limit with no handover. On the owner's instruction Claude writes this delta, the reviewer handover H-2 v1r9 and both blurbs | this folder |

## 5. Where the work is (exact locations)

- **Candidate:** the reviewed, cumulative candidate is `exchange/EX_151_Claude/MHUPA_Slice2_Review_v1r2.zip`
  (SHA-256 `67701220d761924cc9ee1703c613cb3bf48b8f978050115de9ef242d60b751bc`, verified by the reviewer in EX_152).
  - Its `overlay/` holds every file of the development tree that differs from the base tree, **main at 2061055**: 70 files,
    slice 1 and slice 2 together.
  - `REMOVED_FILES.txt` lists the one file it removes (`src/results_master_v0_1.py`, replaced by v0.2).
  - Its `tools/` and `evidence/` hold the build scripts and the Linux suite and mutation logs.
- **Tools to rebuild the development tree:** `exchange/CLAUDE_WEB_TOOLS/mhupa/`, checked on 6 November 2026 to be byte-identical
  to the working copies this chat used.
  - Build command: `sh build_dev_slice2.sh BASE DEV TOOLS DATE`, where:
    - `BASE` is a checkout of 2061055;
    - `TOOLS` is that folder;
    - `DATE` is the `effective_date` written into E_1 revision 3 by `make_e1r3.py`.
  - The build runs slice 1 (`build_dev_slice1.sh`, `apply_slice1.py`, `edit_tests_slice1.py`, `slice1_new/`,
    `slice1_edited/`), then slice 2 (`slice2_edited/`, `slice2_new/`, `apply_slice2.py`, `edit_tests_slice2.py`), with
    `make_updater_v0_2.py` for the updater.
- **Test runner:** `slice2_checkpoint/RUN_MHUPA_SLICE2_SUITE.py --repo <tree>` runs all 570 tests module by module against the
  expected counts. For scale: the owner's T020 ran 561 tests on Windows in 16 minutes 55 seconds, and the Mode H module alone
  takes about two minutes.
- **Mutation tool:** `mhupa_slice2_mutations.py TREE [--only N]` (103 mutants), plus `mhupa_slice1_mutations.py`. The agreed
  practice is to run new mutants alone first with `--only N`, then one final full run. A full run takes about three hours.
- **Checkpoint and working records:** `slice2_checkpoint/` holds `CHECKPOINT_slice2.md`, the work-item card v7, the A1 draft,
  the bodies of EX_147, EX_149 and EX_151, and the logs.
- **Message assemblers:** `assemble_ex141.py` ... `assemble_ex151.py`. Each EX folder holds the message, the reviewer's previous
  message unchanged, the ZIP, a members list with SHA-256 as stored and after CRLF to LF, and diffs.
- **Claude Code:**
  - `CLAUDE_CODE_WORKING_FOLDER_TREE/tools/cc_clone.py` v0.4, with the commands `make`, `unzip`, `overlay --plan`,
    `verify-overlay`, `git`, `remove` and `commit-report`;
  - the rulebook `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md` v0.4, whose rule 7 names the MHUP-A programs it must never run;
  - task files and their plan files in `inbox/`;
  - reports in `outbox/`.
  - **Before sending any task file**, run `python3 -I exchange/CLAUDE_WEB_TOOLS/check_task_commands.py <repo> <task file>`.
    The deny list matches command *text*, so a denied path goes in a plan file and never on a command line.

## 6. The decisions and records the next chat must carry

- **A1 (RATIFIED, 5 November 2026):**
  - The Mode H score ledger is written in full in a temporary file, synced, and published once by create-only link
    (`contract_publication.create_only`). It replaces the per-pair provisions of design v0.1r5 sections 5.2 and 5.4 and
    Appendix L-H2, and nothing else.
  - The ledger is fully validated (`mode_h._verify_ledger`) before `SCORE_COMPLETE`.
  - A resumed scorer is bound to the scoring plan that `SCORING_STARTED` froze, and to a `SCORE_COMPLETE` naming this game,
    attempt, plan, ledger digest and line count (B05).
  - A1 section 6 is the MHUP-B route for a corrective scoring run. The integrated documentation must cite A1 and must not rely
    on the superseded text (EX_152 section 3).
- **C01 (owner, 4 November 2026):** E_1 revision 3's `effective_date` is the integrated package's preparation date. It is set
  before the package's final review freezes the registry bytes and digests. It is never the admission or release date. The
  release record alone dates a release.
- **R-020** (the integrated package must carry):
  - (a) the package manifest's `release_entries` names E_1 revision 3 for both games (Appendix J step 16), so the released set
    is the 39 baseline variants plus E_1 revision 3 = 40 per game;
  - (b) the environment freeze refuses an orphan file in site-packages, and the fix is a reviewed step;
  - (c) the owner chooses either to rerun the Windows POC suite after the install or to accept it unrun with the reason recorded.
- **R-019:**
  - (a), (d) and (e) were carried in slice 2 and are checked again in the integrated review;
  - (b), the full shape of `FREEZE_LINE_V1` for weekly writers, stays open for MHUP-B;
  - (c), the `FINAL_NEXT_DRAW`/`CATCH_UP` binding mutant, is re-run when MHUP-B makes those modes producible.
- **EX_152's conditions for the integrated review:**
  - assess the assembled behaviour, not the separate slice approvals;
  - integration, records, installer and verifier, release gating, LF/CRLF reproducibility, Windows and safety rehearsals
    including T016, and the outstanding Windows evidence;
  - (ix) COMMITTED PASS: the verifier must prove both commits, the barrier order and that the records agree with the repository.
- **R-018** (the owner's decisions of 4 November 2026, notably (a) the retry rule after a STOP and (h) the weekly session run as
  that week's authorisation): to go into register v0.25, the next full H-1 edition, and MHUP-B's checklist.
- **The register:** v0.24 is the newest installed edition. Register v0.25 is still to be written. It records:
  - MHUP-A's review round (EX_141-EX_152);
  - A1;
  - C01;
  - R-018;
  - the direction document v0.3r1;
  - the reviewer change of 6 November 2026.

## 7. What to do next, in order

1. **Read the Windows reports** when the owner has run and pushed them: `outbox/REPORT_T021.md` (v1r1, 569 tests) and
   `REPORT_T022.md` (v1r2, 570 tests).
   - Never claim either as passed before reading it.
   - A Windows failure is fixed before integration. If its cause is unexplained, it is Fable work.
2. **Start the new reviewer.**
   - The owner starts a new ChatGPT chat with `ChatGPT_Reviewer_Handover_H2_v1r9_introductory_blurb.md` (this folder).
   - Its takeover check (read and verify, a first reply in its own words) must be favourable, and the owner must accept it,
     before the integrated package is sent.
   - Claude answers its questions blind, as in HO-2.
3. **Build the integrated MHUP-A install package** (Opus for packaging; Fable only for a HIGH core problem). It contains:
   - design Appendix J steps 0-19: the installer and the verifier, including the verifier's `released` phase;
   - the LF and CRLF rehearsals, and T016 on Windows;
   - the package manifest with `release_entries` (R-020(a));
   - E_1 revision 3's `effective_date` set to the preparation date (C01), which changes the registry bytes and digests, so
     rebuild and rerun everything after setting it;
   - A1 cited;
   - **the base rebased from 2061055 onto the current main**:
     - the owner's `.gitignore` lines must survive (the candidate's `overlay/.gitignore` is a whole-file replacement made from
       the old base);
     - account for `install_upgrade_dependencies_into_venv.bat` now adding `pyahocorasick`, which changes the venv's
       environment freeze and the closure, if installed;
     - account for the owner's new folders `src/GAIS/` and `doc/GASI_thought_experiments/`.
     - Ask the owner whether `src/GAIS/` should move out of `src/` before Approval 1. A code closure over `src/` that takes in
       experimental work, with very large ignored files beside it, is a risk. Offer this as a question; do not decide it.
4. **Write register v0.25 and the next full H-1 and H-2 editions** in a documentation package for the owner to install, once the
   integrated package is reviewed.
5. **Later:** MHUP-B (the weekly writers, catch-up, `FREEZE_LINE_V1`, the corrective scoring route in A1 section 6, R-018(d) and
   (h)), WF-1C, then wave 3 onward (the roadmap).

## 8. Working lessons from this cycle (add to H-1 section 12 at the next full edition)

- **The `.claude/settings.json` deny list matches text**, including `*.bat*`, `*Run_Experiment*`, `*Run_Results_Updater*`,
  `*results_master*`, `*unlink*`, `*rmtree*`, `*lottery*` and `git rm*`. Task files name such paths only inside plan files. Check
  every task file with `check_task_commands.py`.
- **Guards inside the tests:** slice 1's `test_e1r3` refuses the token `effective_date` in unexpected source text. A docstring
  that named it broke the suite. Keep that token out of comments and docstrings.
- **Generators:** use counted edits (assert that an anchor occurs exactly once). Several anchor mistakes were caught that way.
- **Diffs between candidates:** exclude removed files on both sides. The v1 to v1r1 diff once wrongly showed
  `results_master_v0_1.py`.
- **Mutation honesty** (the reviewer's point on mutant [55]): "no test plants it" is test non-detection, not equivalence.
  Mark a mutant equivalent only for a demonstrated semantic reason, printed in the log.
- **Errors:** an invalid record must become a refusal (`ModeHRefused`), never an escaping `ValueError`.
- **Oz Lotto:** the ledger never stores supplementaries (R2 2.5). Validate `supplementary_matches` by range and against its
  division.
- **Token economy:** run new mutants alone, then one final full chain; rerun only the changed module and the affected mutant
  after a one-line test change, and say so in the message.

## 9. Integrity of this delta

Every fact above was taken from the repository at 43dd069 (origin/main, 6 November 2026) and from the records it names. Where
memory and the records differ, the records win. Anything not checkable from the repository is marked as the owner's or as
pending. T021 and T022 are pending. The ChatGPT reviewer's handover of 6 November 2026 was not written by the reviewer: H-2
v1r9 is Claude's reconstruction, and the new reviewer must verify it.

End of H-1 v1r9 delta.
