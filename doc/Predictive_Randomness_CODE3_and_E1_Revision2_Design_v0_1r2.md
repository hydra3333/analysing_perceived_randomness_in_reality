# Predictive Randomness - CODE-3 (retirement tooling) and E_1 revision 2, design note v0.1r2

**Document:** the design of the package that retires E_1 revision 1 into the archive (CODE-3's retirement tooling, used here for the first time) and installs E_1 revision 2, which can run walk-forward on past draws through the contract. E_1's legacy runner moves to revision 2.
**Version:** v0.1r2 DRAFT for the reviewer's focused RECHECK, 31 October 2026, answering EX_089 (E1R2-R3-C03 and O02; section 12). v0.1r1 (LF `933b0a07...942b8b`) answered EX_087 (section 11) and was rechecked in EX_089. v0.1 (LF `6cff9f90...e6e8`) was reviewed in EX_087. Author: Claude. Ratifier: the project owner.
**Status:**
- **Authority:** it authorises nothing and changes no ratified rule. Where it proposes an exception, the owner decision is listed in section 9.
- **No code yet.**
- **Origin:** owner decision WF1-13 (31 October 2026, option C), made when WF-1A's coding found that E_1 revision 1 refuses real data (EX_082 section 1; `exchange/OWNER_REMINDERS.md` R-005).
- **Base:** `main` at `ae190c7` (EX_089). This package installs **after REL-1 and WF-1A (v2, the version that answers EX_083's B01)**, because it edits WF-1A's driver (sections 4.4 and 7).

## 1. In plain English

E_1 counts how often each number has come up and ranks by the count. Its revision 1 refuses anything but invented data when run through the method contract. That was deliberate when E_1 was connected to the contract, so that E_1's code would not change then. As a result, E_1 cannot take part in the walk-forward batches.

**The fix,** chosen by the owner, is the textbook one: a **revision 2** of E_1.
- **The same counting,** byte-for-byte.
- **One change:** the line that refuses real data now also accepts past-draw walk-forward runs.

The project's rules say that changing a released method's code makes a new revision. They also say the old revision's code is kept, unchanged, in `archive/`. That archiving step is **CODE-3**, which has not been built yet. This package builds it and uses it first for E_1.

**After it is installed:**
- E_1 runs through the walk-forward driver like any other method. A new batch over the whole cohort, now 40 variants, runs it over the same past draws as the others (section 7).
- E_1's legacy runner checks revision 2's release entry instead of revision 1's. Its outputs do not change.
- E_1's past results stay valid, and its tracks continue across the revision (owner decision D-1).

## 2. What the record fixes

- **E2R-R14A:** a change to a released method's behaviourally relevant implementation needs a successor revision. A revision is never reused after an implementation change merely because outputs did not change. NAMES-1's structural exception and E1-ALIGN's (E1A-D1) are not precedents.
- **E2R-R54 (D-5): the archive.** The package introducing a successor moves the outgoing revision's **unchanged bytes** to `archive/methods/E_<nnn>/r<k>/`, with a `README.md` stating:
  - the method and its revision;
  - the retirement date;
  - the previous paths under `src/`;
  - the shared helpers it used, with their revisions.

  No commit ID and no stored file hash.
- **E2R-R55: package-time checks.** The install verifier compares each archived file with the still-current file in the pre-install `src/` baseline. It also checks naming, case on Windows, unique revision folders, `__init__.py` traversal, and that the README's helper references resolve.
- **E2R-R56: the archive is never imported.** `archive/` is outside every normal import path, and a static check rejects imports from it. Normal runners never dispatch an archived revision. Exact historical replay is not promised.
- **E2R-T15: the retirement test.** On a disposable synthetic tree and successor overlay:
  - archived bytes equal the pre-install bytes;
  - the old path is removed (see 4.2 for paths a successor reuses);
  - README references resolve;
  - imports and dispatch cannot reach `archive/`;
  - the same holds in a tree without Git history.
- **E2R-R57 and R58: release.** R57 (DECIDED): the dispatch gate needs an active `SUPPORTED` entry for the exact revision, and no flag. R58 (RECOMMENDED): a package introducing new or revised code installs it non-runnable, and a separate release package releases it.
- **D2-3:** E_1's legacy runner has the same release check, today pinned to revision 1. The owner's WF1-13 moves it to revision 2.
- **D-1:** a track continues across revisions; every record carries its `method_revision`.

## 3. E_1's files today, and what changes

| File | Role | In revision 2 |
|---|---|---|
| `src/methods/E_001/__init__.py` | package marker | unchanged |
| `src/methods/E_001/e1_historical_appearance_frequency.py` | E_1's accepted counting and tie functions (the legacy goldens) | unchanged |
| `src/methods/E_001/e1_training_view.py` | the legacy runner's training view | unchanged |
| `src/methods/E_001/e1_common_reader_bridge.py` | the legacy digest bridge | unchanged |
| `src/methods/E_001/e1_standalone_contract.py` | the legacy runner's records | unchanged |
| `src/methods/E_001/multigame_e1.py` | the multi-game function the contract adapter calls | **one line:** `data_kind` may be `SYNTHETIC_CONTRACT_TEST` or `REAL_DEVELOPMENT`; every other kind is still refused, and so is a target outside the development boundary |
| `src/methods/E_001_Historical_Appearance_Frequency.py` | the legacy entry file (Powerball, D3 gate) | **one string:** `legacy_gate(..., '1')` becomes `'2'` (WF1-13) |
| `src/methods/contract_adapters/e_001.py` | the contract wrapper (outside E_1's folder) | **docstring only:** "E_1 keeps revision 1 ... real runs stay off there" is corrected; no code change |
| `src/methods/_common/walk_forward.py` | WF-1A's driver | `NOT_REAL_CAPABLE` loses E_1 (it becomes `{}`); nothing else (the owner declined ER-6's restricted plan) |
| declarations `E_1/FULL_HISTORY_RAW_COUNTS_V1/r1.json` (both games) | revision 1's declarations | unchanged (records are never edited) |
| **new** declarations `.../r2.json` (both games) | revision 2 | the same fields as r1, with `method_revision` "2" |
| registry `E_1/FULL_HISTORY_RAW_COUNTS_V1/entry_0001.json` (both games) | r1 `SUPPORTED` | unchanged |
| **new** `entry_0002.json` (both games) | r2 | `SUPPORTED`, revision "2", r2's declaration digest, linked to entry_0001 (see decision ER-2) |

**What stays byte-identical in E_1's output:**
- **Scores, ranking, TOP and WORST** do not change. The counting code is unchanged, and the tie identity (`TIE_SHA256_V1`) names the method and variant, not the revision.
- **What does change:** a contract forecast record carries `method_revision` and `declaration_digest`, so revision 2's records differ in those two fields and in their content digest.
- **The legacy runner's records** carry no revision, so its outputs and goldens do not change.

## 4. The package (one package: CODE-3's tooling and E_1 revision 2; decision ER-1)

### 4.1 CODE-3: the retirement tooling (generic, reused by later successors)

- **The builder's retirement step:** a package declares `RETIRE = {method_id: (old_revision, [src paths])}`. The builder copies those files' **pre-install** bytes into `archive/methods/E_<nnn>/r<k>/`, keeping their paths relative to `src/methods/`. For E_1 that is `E_001/<file>` for the folder, and `E_001_Historical_Appearance_Frequency.py` for the entry file. It also writes the README (4.3).
- **The verifier's archive checks** (E2R-R55), in each phase:
  - **pre:** the archive folder is absent;
  - **post and committed:** every archived file's LF bytes equal the same path's bytes at the **base commit** (`git show BASE:src/...`), which is the pre-install baseline;
  - the archive's file list is exactly the declared list plus `README.md`;
  - folder names are lower-case `r<k>` and unique, case-insensitively;
  - the README's helper references resolve (4.3).
- **The archive is never executed, by production code or by tests** (E2R-R56; EX_087 C01). There is no test-only exception: every test that touches `archive/` reads its files as bytes. Two new checks:
  - **static:** no `.py` file under `src/` or `tests/` has an import whose module path starts with `archive`, and none calls `importlib`, `runpy`, `exec`, `compile`, `spec_from_file_location`, `SourceFileLoader` or `sys.path` changes on a path containing an `archive` folder name. Only the files that compare archived bytes may name `archive/` at all, and they are listed in the test;
  - **runtime:** in a subprocess, the test imports every module under `src/` (as the suite's paths allow) and then the full E_1 contract path for both games on invented data; afterwards, no entry in `sys.modules` has a `__file__` under `archive/`, and `archive` is on no `sys.path` entry.
  - **The r1 output reference does not come from the archive** (see E1R2-T01).
- **E2R-T15 on a synthetic tree** (both kinds of path; EX_087 C01): a temporary source tree with an invented method E_998 r1 of three files, retired by the same builder step to r2, run twice, in a copy **with** and one **without** a `.git` folder. r2 **drops** one file (its old path must be absent afterwards), **reuses** one path with new bytes (the archive holds r1's bytes, the live path holds r2's), and **reuses** one path unchanged (the archive holds r1's bytes, the live path is identical). In every case the archive holds r1 complete, README references resolve, and imports and dispatch cannot reach the archive.

### 4.2 Paths a successor reuses

E2R-T15 says "the old path is removed". Here revision 2 reuses every path. Five files are byte-identical, and two change by one line each. The rule this package applies, and asks the reviewer to confirm:
- `src/` holds current code only (D-4);
- the archive holds the complete outgoing revision;
- an old path is removed only when the successor does not reuse it.

The verifier proves the archived bytes are the pre-install bytes. Archive copies of unchanged files are deliberate: the archive must hold r1 complete, so that it stands alone if a later revision changes those files.

### 4.3 The archive README (`archive/methods/E_001/r1/README.md`, ASCII)

- **Method:** E_1, Historical Appearance Frequency, revision 1, variant `FULL_HISTORY_RAW_COUNTS_V1` (both games).
- **Prepared and retired** (EX_087 O01): the README states the package's preparation date, labelled as such, and says that the retirement takes effect when the owner installs the package. The installation date and commit are recorded in the ratification register, not in the README (D-5: no commit ID, no hash). Superseded by revision 2.
- **Previous paths:** the seven files' paths under `src/methods/`.
- **Shared helpers used:** `_common/canonical_encoding.py`, `_common/game_profiles.py`, `_common/game_draws_reader.py` (via the bridge) and `_common/experiment_runtime_status_and_resources.py` (the legacy runner's status). All are revision 1 of the shared code. None is revised by this package, and all remain current in `src/methods/_common/`, so the references resolve.
- **Why retired:** the multi-game function's data-kind line (WF1-13).
- **Replay statement:** E2R-R56's wording; exact replay is not promised.
- **No commit ID, no file hash.**

### 4.4 E_1 revision 2

The changes in section 3's table, generated by a script that travels with the package.

## 5. Install and release together, behind a fail-closed barrier (decision ER-2, revised as ER-2r1: an exception to E2R-R58's recommended two packages)

**What R58 recommends:** install revision 2 non-runnable (flag present, active entry not `SUPPORTED`), then release it in a second package.

**Why that fails for E_1:** for E_1, that interim state would make **both** revisions unrunnable. The flag is per method folder, and the active entry would no longer be r1's `SUPPORTED`.
- E_1 is the contract's reference workhorse. A probe on the tree with REL-1 and WF-1A applied planted E_1's flag (E_1 unrunnable, as in R58's interim state): **68 of the 321 tests failed** (`test_e2r_runner` 19, `test_e1_standalone` 13, `test_wf1a_walk_forward` 12, `test_multigame_launch_and_manifest` 7, `test_multigame_science_allowlist` 7, `test_e2r_dispatch` 5, `test_multigame_console_and_synthetic_scorer` 4, `test_rel1_release` 1). They would all need editing for a committed interim, and editing back at release.
- E_1's legacy runner would also refuse in the interim.

**The gap in v0.1 (EX_087 B01, accepted).** v0.1's step 1 copied r2's code while r1's entry was still active and no flag existed. Both gates (`contract_dispatch._admit` and `legacy_gate`) check only the active entry and the flag, so an r1-pinned request would have run r2's code under r1's approval until the entries arrived. Reversing the order fails the same way: r2's entries before r2's code would run r1's code under r2's approval.

**Proposed (ER-2r1): one package, and a temporary barrier for the whole install.** The barrier is E_1's own `IN_DEVELOPMENT.txt` flag, which both gates already refuse on. It is created first, kept through every step, and removed last. It is never committed. The install runs as five named steps, each followed by its own verifier phase. Every phase checks the whole working tree against exactly one allowed state, so a skipped or repeated step stops:

| Step | Owner action | Verifier phase: the only state it accepts |
|---|---|---|
| 0 | none | `pre`: clean tree; r1's entries active; no E_1 flag; no archive; no r2 file |
| 1 | copy `barrier_overlay/` (the flag only) | `barrier`: as `pre`, plus the flag with the package's exact bytes |
| 2 | copy `repo_overlay/` (the archive, r2's code and declarations, the driver and the tests) | `code`: the flag; every `repo_overlay` file with the expected bytes; **no** `entry_0002.json` for E_1 |
| 3 | copy `release_overlay/` (the two r2 `entry_0002.json` records only) | `release`: as `code`, plus both entries with the expected bytes; both games' chains end r1 then r2, linked, and each active entry's declaration digest equals r2's declaration |
| 4 | delete the flag (`del src\methods\E_001\IN_DEVELOPMENT.txt`) | `post`: as `release`, without the flag; then the tests run |

Then the usual stage, commit (`committed` phase: the commit holds exactly the archive, code, declarations, entries and tests, and no flag), and push.

**What each state does** (proved by E1R2-T09 on synthetic copies, not by running anything during the install). The gate's check order is unchanged (EX_089 C03): `_admit` checks, in turn, the active entry's status, the pinned entry digest, the revision, the declaration digest, and only then the flag. So **the property** is that nothing admits after steps 1, 2 or 3, and **the reason** depends on the request and the step:
- an **r1 contract request** pins entry_0001's digest, revision "1" and r1's declaration;
- an **r2 contract request** pins entry_0002's digest, revision "2" and r2's declaration;
- the **legacy gate** has no pin, only a revision: "1" from the legacy entry file until step 2 copies r2's file, "2" after. The table also shows the other revision string, for completeness.

| State | r1 contract request | r2 contract request | legacy gate, revision "1" | legacy gate, revision "2" |
|---|---|---|---|---|
| after step 0 (`pre`) | admits (as today) | `STALE_REGISTRY_ENTRY` | admits (the installed legacy file, as today) | `REVISION_MISMATCH` |
| after step 1 (`barrier`) | `IN_DEVELOPMENT_FLAG_PRESENT` | `STALE_REGISTRY_ENTRY` | `IN_DEVELOPMENT_FLAG_PRESENT` (the installed legacy file) | `REVISION_MISMATCH` |
| after step 2 (`code`) | `IN_DEVELOPMENT_FLAG_PRESENT` | `STALE_REGISTRY_ENTRY` | `IN_DEVELOPMENT_FLAG_PRESENT` | `REVISION_MISMATCH` (the installed legacy file) |
| after step 3 (`release`) | `STALE_REGISTRY_ENTRY` | `IN_DEVELOPMENT_FLAG_PRESENT` | `REVISION_MISMATCH` | `IN_DEVELOPMENT_FLAG_PRESENT` (the installed legacy file) |
| after step 4 (`post`) | `STALE_REGISTRY_ENTRY` | admits, subject to the unchanged data, orphan, owner and environment gates | `REVISION_MISMATCH` | admits, subject to the same gates (the installed legacy file) |

**The walk-forward driver** in the same states: planning a new batch for either game refuses after steps 1, 2 and 3 (`cohort()` treats a `SUPPORTED` method with a flag as an inconsistent installed state), and so does starting a planned batch whose cohort includes E_1. A batch planned earlier without E_1 is not blocked by the flag, so the install instructions say that no batch is run or resumed between step 0 and the push. The flag is the gates' application-level safeguard, not an operating-system lock.

**On any STOP before step 4,** the owner stops, leaves the flag where it is and sends Claude the output. Recovery is the owner's decision; nothing removes the flag automatically, and no step bypasses it. While the flag exists, E_1 cannot run by either path.

**On any STOP after step 4** (EX_089 O02: the `post` check, the tests, the commit or the `committed` check fails, or the install is interrupted), r2's code and entries are present without the flag, but the install is not complete. Then:
- the owner does not push, runs no E_1 run and no batch of either game, and sends Claude the whole output;
- nothing is undone automatically: no reset, rollback, deletion or process termination;
- if the owner decides to close the gate again while the failure is examined, the owner copies `barrier_overlay/` again and runs the verifier's `release` phase, which accepts exactly that state (r2 installed, the flag present). Removing the flag again is step 4, after the owner's decision.

**Why one package with a barrier is acceptable here:** revision 2's computation is proven identical to revision 1's (section 6, E1R2-T01, T02 and T02B). The only behavioural difference is the data kinds it admits. Admitting real data is the owner's decision WF1-13, and is reviewed in this round. The barrier gives every intermediate state the property R58 asks for: no code runs under an approval that was not given for it.

**The alternative:** R58's two packages, with a committed interim in which E_1 cannot run and the 68 tests are edited twice.

## 6. Tests (synthetic only)

| ID | Test |
|---|---|
| E1R2-T01 | **Identity with r1, both games** (EX_087 C01): for both games and several targets on invented masters, in the synthetic namespace, E_1 r2's contract forecast equals r1's label for label (scores, ranked groups, ranking, TOP, WORST); only `method_revision`, `declaration_digest` and the content digest differ. **r1's side is a frozen reference file,** `tests/fixtures/e1_r1_reference_v1.json`: the package's build tool computes it once from the **base commit's** r1 code, in a temporary copy outside the repository, and the package carries it as an ordinary new test file (listed in the manifest). The test never reads or runs anything under `archive/`. |
| E1R2-T02 | **Real namespace, Powerball** (scoped by EX_087 C02): on an invented Powerball master in a temporary project, through the driver, E_1 r2's `REAL_DEVELOPMENT` forecast equals E_1's legacy function (`build_e1_forecast`, Powerball's MAIN and POWERBALL scorer) on the same rows with the real-namespace digest (scores, ranking, TOP, WORST). The contract's real-namespace digest already equals the reader's legacy digest (an existing contract test). |
| E1R2-T02B | **Real namespace, Oz Lotto, an independent oracle** (EX_087 C02): on an invented Oz Lotto master in a temporary project, through the driver, E_1 r2's `REAL_DEVELOPMENT` forecast is checked label by label against a test-local oracle written from the specification, not from E_1's code: the MAIN appearance count of each number over exactly the draws before the target in the permitted view; the full ranking with ties ordered by `TIE_SHA256_V1` recomputed in the test from its definition; TOP and WORST; the target, its N-1 boundary, and the permitted-view digest, recomputed from the invented rows by the reader's documented digest rule. The master is invented in the test; no real master is opened or imported. |
| E1R2-T03 | **Data kinds and boundary, both games:** the multi-game function admits `SYNTHETIC_CONTRACT_TEST` and `REAL_DEVELOPMENT`, and refuses `REAL_HOLDOUT`, `FINAL_NEXT_DRAW`, `IN_SAMPLE_DIAGNOSTIC`, `REAL_HISTORICAL_DEVELOPMENT` and anything else. For each game, a target past the permitted development boundary (a holdout target) is refused. |
| E1R2-T04 | **Registry:** both games' E_1 chains are r1 `SUPPORTED`, then r2 `SUPPORTED`, linked; r2's declaration equals r1's apart from `method_revision`; a request pinning r1 is refused as `STALE_REGISTRY_ENTRY` (an approval for a retired revision is not one for its successor, E2R-R57). |
| E1R2-T05 | **Legacy runner:** it admits under r2 and refuses with r2's entry withdrawn (a harness copy); its synthetic goldens are byte-identical (the existing E_1 standalone tests, unchanged apart from the revision string). |
| E1R2-T06 | **Driver:** `NOT_REAL_CAPABLE` is empty, and a plan names no method as not in the cohort; the cohort has 40 variants including E_1; in a temporary project, a full batch runs E_1's pairs alongside the others, and E_1's SUCCESS pairs pass the same attempt and record checks (`attempt_state` DONE). |
| E1R2-T07 | **Archive (E2R-R55 and R56):** archived bytes equal the base commit's (verifier, every phase after `pre`); exact file list; README fields (including the preparation-date wording of 4.3); helper references resolve; the static and runtime no-execution checks of 4.1. |
| E1R2-T08 | **E2R-T15** on the synthetic E_998 tree: a dropped path, a reused path with new bytes and a reused unchanged path, with and without `.git` (4.1). |
| E1R2-T09 | **The install barrier** (EX_087 B01; reasons corrected by EX_089 C03): on synthetic copies of the installed contract data and method folder, the states after steps 0 to 4 of section 5, and the re-barriered state of the STOP-after-step-4 recovery, are built in turn. For each state the test checks **two properties separately:** (1) whether each of the four requests in section 5's table admits, which must be never after steps 1, 2 and 3, and (2) its exact refusal code, cell by cell as in the table, keeping the pinned contract requests apart from the unpinned legacy gate. It also checks that planning a batch refuses, and starting a plan that includes E_1 refuses, until step 4. The verifier's six phases are run against the same states, and each accepts only its own (the re-barriered state passes `release` only). The gate's code and order are not changed. |
| (edits) | `test_e2r_dispatch`'s three `legacy_gate(..., '1')` become `'2'`. WF-1A's tests updated for `NOT_REAL_CAPABLE == {}`. Every other E_1 test reads the active entry, so it follows r2 unchanged. |

**Mutation checks**, each caught:
- r2's data-kind line admitting `REAL_HOLDOUT`;
- the legacy gate left at '1';
- an archived file with one byte changed;
- a README without its helper list;
- an import from `archive`;
- E_1 left in `NOT_REAL_CAPABLE`;
- r2's declaration differing in a field other than the revision;
- the archive missing one file;
- the barrier flag left out of `barrier_overlay/`, or removed before step 3 (the `code` or `release` phase accepts a tree without it);
- the verifier's `code` phase accepting an E_1 `entry_0002.json`;
- a test loading an archived file with `importlib` (the static check);
- E_1's Oz Lotto tie order changed (T02B's oracle);
- the gate's flag check moved before the pin check (T09's code matrix), and T09 expecting the flag code in a cell where the gate gives another;
- the r1 reference file edited by one score (T01).

**Implementation commitments (EX_089's notes):**
- **The r1 reference file's provenance** (T01): the package records how it was made (the base commit's r1 files, by path, the builder's command and the inputs), and its review evidence regenerates it from the base tree byte for byte.
- **T15 without Git** compares the archive with pre-install bytes saved by the test before the retirement step, not with a Git operation.
- **T02B's oracle** calls none of E_1's code or the contract's ranking, tie or digest helpers. It implements the count, `TIE_SHA256_V1` and the digest rule in the test, and its published labels are scores, not probabilities.
- **T07's runtime import** imports only a listed inventory of library modules, each checked to have no side effects on import. It never imports an entry-point script (a `Method_*.py`, `E_001_Historical_Appearance_Frequency.py`, the coordinator or a scraper), and it opens no data and no network.

## 7. After installation, and how it fits the measurement and ranking scheme

1. **The full-cohort batch (the owner declined ER-6, 31 October 2026).** Since WF-1A v2 (EX_083 B01), a batch never reuses another batch's runs. No batch is run or resumed during the install (an instruction, section 5); while the barrier flag exists, planning a new batch refuses, and so does starting one whose cohort includes E_1. After installation, the owner plans and runs a new batch over the whole cohort, now 40 variants including E_1, over the same window: for Powerball 1145-1576, about 105 minutes on this estimate. The earlier 39-variant batch stays on record, unchanged and counted in the search log; nothing is deleted.
2. **The scorer reads E_1 like every other method.** E_1 r2's forecasts are ordinary `METHOD_FORECAST_V1` records, made by the same runner, under the same pins, and checked by the same batch evidence. WF-1B's scorer reads them exactly as it reads the other 39 variants', with the same grids, measures, labels and fair-draw references. Nothing about E_1 is special in the measurement or ranking scheme. Because the new batch holds all 40 variants under one plan and one set of pins, WF-1B can score one complete batch per game, so the batches are not mixed in one report. Whether WF-1B also reports the earlier 39-variant batch, and how, is a WF-1B design point.
3. **Families (EX_083's point).** A predeclared family must not be rewritten after its first use. With a full 40-variant batch, WF-1B can register its MR7 families once, with M = 80 as designed, before that batch is scored. If WF-1B scores the 39-variant batch first, its 78-track family is a separate, predeclared family and is not rewritten. This is the owner's choice at WF-1B's design.
4. **The old runner** keeps working for Powerball past draws under D3, now checked against revision 2.

## 7A. Offline operation (the owner's principle, 31 October 2026)

Once installed, nothing here depends on GitHub:
- **The runs read only local files:** the installed registry, the method folders and the local masters. They write only under `results/` and `transitory_data/`.
- **The archive needs no Git history:** it is a plain copy of revision 1's files with a README, holding no commit ID and no hash (E2R-R54), and E2R-T15 is tested in a tree with no `.git` folder.
- **The install verifier uses only the local repository:** it compares the archive with the local base commit. GitHub is used only for the owner's `pull` and `push`, which are optional when working offline.
- **E_1 r2 introduces no network access** and no new dependency.

## 8. Not in scope

Not in scope:
- any other method's revision;
- WF-1B;
- the handovers;
- a change to E_1's counting;
- a promise of exact replay of r1.

## 9. Owner decisions

The owner chose ER-1 to ER-4 as recommended on 31 October 2026, before the review, and declined ER-6 on the same day. EX_087 accepted ER-1, ER-3 and ER-4 in principle, and required a fail-closed procedure for ER-2 (B01). ER-2r1 is that procedure; the owner chose it on 31 October 2026, before the RECHECK.

- **ER-1 (OWNER-CHOSEN 31 October 2026, before review; was RECOMMENDED): one package for CODE-3's tooling and E_1 revision 2.** CODE-3's tooling has no other use yet, and E_1 r2 is its first, and real, test. The option: CODE-3 alone first (tested only on the synthetic tree), then E_1 r2.
- **ER-2 (OWNER-CHOSEN 31 October 2026, before review): E_1 r2 installed and released in the same package,** as two named actions, an exception to E2R-R58's recommended two-step release, for E_1 only. EX_087 B01 found that its interim was not fail-closed.
- **ER-2r1 (OWNER-CHOSEN 31 October 2026, after EX_087 and before the RECHECK; replaces ER-2's procedure): one package, installed in five steps behind a temporary barrier** (E_1's own flag, created first and removed last, never committed; section 5). The option: R58's two packages, with a committed interim in which E_1 cannot run.
- **ER-3 (OWNER-CHOSEN 31 October 2026, before review; was RECOMMENDED): the archive holds r1 complete, including files that r2 keeps unchanged and the legacy entry file;** an old path is removed only when the successor does not reuse it (section 4.2). The option: archive only the two files that change (then r1 is not complete in the archive).
- **ER-4 (OWNER-CHOSEN 31 October 2026, before review; was RECOMMENDED): the contract adapter's docstring is corrected,** with no code change, and is not archived (it is CODE-2's wrapper, outside E_1's folder). The option: leave the stale sentence, and list it as out of date in the register.
- **ER-5 (RECORDED): WF1-13 itself:** revision 2, and the legacy runner moved to revision 2. No new choice.
- **ER-6 (OWNER-DECLINED 31 October 2026; was RECOMMENDED): a method-restricted batch plan** (`plan --methods ...`), so that E_1 r2, and any method released later, could be run over past draws without rerunning the whole cohort. **Chosen instead:** a full-cohort batch, about 105 minutes for Powerball, of which about 103 minutes repeat runs already done, with every batch holding the complete cohort. The driver and its CLI keep their WF-1A form, apart from `NOT_REAL_CAPABLE`.

## 10. What the reviewer was asked to check (R-3, v0.1; answered in EX_087)

1. That revision 2 changes nothing in E_1's counting, ranking or tie order (section 3), and that E1R2-T01 and T02 would prove it.
2. ER-2's exception to R58, and whether the two named actions are enough discipline.
3. ER-3's reading of "the old path is removed" for reused paths, against E2R-R54, R55 and T15.
4. The archive checks, the static no-import check and E2R-T15's synthetic test.
5. The legacy runner's move to revision 2 (D2-3 superseded by WF1-13), and that its goldens stay byte-identical.
6. The driver's change (`NOT_REAL_CAPABLE` becomes empty), and the full-cohort batch after installation (section 7).

## 11. Changes in v0.1r1 (answering EX_087), and what the RECHECK is asked to check

| Finding | Change | Where |
|---|---|---|
| E1R2-R3-B01 (BLOCKER) | The install is five steps behind a temporary barrier (E_1's flag: created first, removed last, never committed), each with its own verifier phase that accepts exactly one state; a STOP leaves the barrier in place; the interim states are proved on synthetic copies (E1R2-T09). ER-2's procedure becomes ER-2r1 (owner-chosen 31 October 2026). | 5; 6 (T09, mutations); 7 item 1; 9 |
| E1R2-R3-C01 (CORRECTION) | Nothing executes archived code, tests included: T01's r1 side is a frozen reference file computed by the build tool from the base commit, outside the repository; static and runtime no-execution checks; T15 covers a dropped path, a reused changed path and a reused unchanged path, with and without `.git`. | 4.1; 6 (T01, T07, T08, mutations) |
| E1R2-R3-C02 (CORRECTION) | T02 is scoped to Powerball; new T02B checks Oz Lotto's `REAL_DEVELOPMENT` forecast label by label against an independent test-local oracle on an invented master; T03 checks both games' boundary refusal. | 6 (T02, T02B, T03, mutations) |
| E1R2-R3-O01 (OPTIONAL) | Adopted: the README states the preparation date, labelled as such, and that retirement takes effect at the owner's installation, recorded in the register. | 4.3 |

**Please RECHECK:**
1. That section 5's five steps and six phases leave no interim state in which E_1 code runs under an approval not given for it, and that E1R2-T09 would prove it.
2. That C01's reference file and the static and runtime checks keep `archive/` unexecuted, and that T15's three path cases test ER-3's reading.
3. That T02B is an independent oracle for Oz Lotto's real namespace.

Nothing else changed from v0.1.

## 12. Changes in v0.1r2 (answering EX_089), and what the focused RECHECK is asked to check

| Finding | Change | Where |
|---|---|---|
| E1R2-R3-C03 (CORRECTION) | Section 5's list is replaced by a table of the exact result for each of four requests (r1 and r2 contract requests, the legacy gate with revision "1" and "2") after each step, matching the gate's unchanged check order. T09 tests the never-admits property and the per-cell refusal codes separately. | 5; 6 (T09, mutations) |
| E1R2-R3-O02 (OPTIONAL) | Adopted: a STOP after step 4 means no push, no E_1 run and no batch, nothing undone automatically, and an owner-controlled way to close the gate again (copy `barrier_overlay/` again; the `release` phase accepts exactly that state). | 5; 6 (T09) |
| EX_089's implementation notes | Recorded as commitments: the reference file's provenance, T15's no-Git comparison, T02B's independence, T07's import inventory. | 6 |

**Please RECHECK:** section 5's table against the gate's order, and T09's two properties. The five-step mechanism (ER-2r1) is unchanged.

Nothing else changed from v0.1r1.
