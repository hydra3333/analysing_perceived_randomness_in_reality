# Predictive Randomness - CODE-3 (retirement tooling) and E_1 revision 2, design note v0.1

**Document:** the design of the package that retires E_1 revision 1 into the archive (CODE-3's retirement tooling, used here for the first time) and installs E_1 revision 2, which can run walk-forward on past draws through the contract. E_1's legacy runner moves to revision 2.
**Version:** v0.1 DRAFT for the reviewer's design review (R-3), 31 October 2026. Author: Claude. Ratifier: the project owner.
**Status:**
- **Authority:** it authorises nothing and changes no ratified rule. Where it proposes an exception, the owner decision is listed in section 9.
- **No code yet.**
- **Origin:** owner decision WF1-13 (31 October 2026, option C), made when WF-1A's coding found that E_1 revision 1 refuses real data (EX_082 section 1; `exchange/OWNER_REMINDERS.md` R-005).
- **Base:** `main` at `ef51305` (EX_085). This package installs **after REL-1 and WF-1A (v2, the version that answers EX_083's B01)**, because it edits WF-1A's driver (sections 4.4 and 7).

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
- **The static check** (E2R-R56), a new test:
  - no `.py` file under `src/` or `tests/` imports anything whose module path starts with `archive`;
  - no runner adds `archive` to `sys.path`;
  - `archive/` is in none of the suite's paths.
  The test reads archive files as bytes only.
- **E2R-T15 on a synthetic tree:** a temporary source tree with an invented method E_998 r1, retired by the same builder step to r2, in a copy **without** a `.git` folder. Archived bytes equal the originals, README references resolve, and imports cannot reach the archive.

### 4.2 Paths a successor reuses

E2R-T15 says "the old path is removed". Here revision 2 reuses every path. Five files are byte-identical, and two change by one line each. The rule this package applies, and asks the reviewer to confirm:
- `src/` holds current code only (D-4);
- the archive holds the complete outgoing revision;
- an old path is removed only when the successor does not reuse it.

The verifier proves the archived bytes are the pre-install bytes. Archive copies of unchanged files are deliberate: the archive must hold r1 complete, so that it stands alone if a later revision changes those files.

### 4.3 The archive README (`archive/methods/E_001/r1/README.md`, ASCII)

- **Method:** E_1, Historical Appearance Frequency, revision 1, variant `FULL_HISTORY_RAW_COUNTS_V1` (both games).
- **Retired:** the date of installation, written by the builder as the package's build date; superseded by revision 2.
- **Previous paths:** the seven files' paths under `src/methods/`.
- **Shared helpers used:** `_common/canonical_encoding.py`, `_common/game_profiles.py`, `_common/game_draws_reader.py` (via the bridge) and `_common/experiment_runtime_status_and_resources.py` (the legacy runner's status). All are revision 1 of the shared code. None is revised by this package, and all remain current in `src/methods/_common/`, so the references resolve.
- **Why retired:** the multi-game function's data-kind line (WF1-13).
- **Replay statement:** E2R-R56's wording; exact replay is not promised.
- **No commit ID, no file hash.**

### 4.4 E_1 revision 2

The changes in section 3's table, generated by a script that travels with the package.

## 5. Install and release together (decision ER-2: an exception to E2R-R58's recommended two steps)

**What R58 recommends:** install revision 2 non-runnable (flag present, active entry not `SUPPORTED`), then release it in a second package.

**Why that fails for E_1:** for E_1, that interim state would make **both** revisions unrunnable. The flag is per method folder, and the active entry would no longer be r1's `SUPPORTED`.
- E_1 is the contract's reference workhorse. A probe on the tree with REL-1 and WF-1A applied planted E_1's flag (E_1 unrunnable, as in R58's interim state): **68 of the 321 tests failed** (`test_e2r_runner` 19, `test_e1_standalone` 13, `test_wf1a_walk_forward` 12, `test_multigame_launch_and_manifest` 7, `test_multigame_science_allowlist` 7, `test_e2r_dispatch` 5, `test_multigame_console_and_synthetic_scorer` 4, `test_rel1_release` 1). They would all need editing for the interim, and editing back at release.
- E_1's legacy runner would also refuse in the interim.

**Proposed:** the r2 entries are `SUPPORTED` in this package. Installation and release happen together, as **two separate, named owner actions in the install instructions:**
1. copy `repo_overlay/` (the archive, the code, r2's declarations and the tests), then run the verifier's `post` check, which requires that no r2 entry exists yet;
2. only after that passes, copy `release_overlay/` (the two r2 `entry_0002.json` records only), then run the verifier's `release` check, and then the tests.

The verifier and the instructions list the release entries separately from everything else.

**Why that is acceptable here:** revision 2's computation is proven identical to revision 1's (section 6, tests E1R2-T01 and T02). The only behavioural difference is the data kinds it admits. Admitting real data is the owner's decision WF1-13, and is reviewed in this round.

**The alternative:** follow R58 exactly, and accept a short window in which E_1 cannot run at all, with the test edits that window needs. That costs a second package and a second install.

## 6. Tests (synthetic only)

| ID | Test |
|---|---|
| E1R2-T01 | **Identity:** for both games and several targets on invented masters, E_1 r2's contract forecast equals r1's label for label (scores, ranked groups, ranking, TOP, WORST); only `method_revision`, `declaration_digest` and the content digest differ. r1's output comes from the archived function, loaded by path in the test only, never imported normally. |
| E1R2-T02 | **Real namespace:** on an invented master in a temporary project, through the driver, E_1 r2's `REAL_DEVELOPMENT` forecast equals E_1's legacy function (`build_e1_forecast`) on the same rows with the real-namespace digest (scores, ranking, TOP, WORST). The contract's real-namespace digest already equals the reader's legacy digest (an existing contract test). |
| E1R2-T03 | **Data kinds:** the multi-game function admits `SYNTHETIC_CONTRACT_TEST` and `REAL_DEVELOPMENT`, and refuses `REAL_HOLDOUT`, `FINAL_NEXT_DRAW`, `IN_SAMPLE_DIAGNOSTIC`, `REAL_HISTORICAL_DEVELOPMENT` and anything else. A holdout target is still refused. |
| E1R2-T04 | **Registry:** both games' E_1 chains are r1 `SUPPORTED`, then r2 `SUPPORTED`, linked; r2's declaration equals r1's apart from `method_revision`; a request pinning r1 is refused as `STALE_REGISTRY_ENTRY` (an approval for a retired revision is not one for its successor, E2R-R57). |
| E1R2-T05 | **Legacy runner:** it admits under r2 and refuses with r2's entry withdrawn (a harness copy); its synthetic goldens are byte-identical (the existing E_1 standalone tests, unchanged apart from the revision string). |
| E1R2-T06 | **Driver:** `NOT_REAL_CAPABLE` is empty, and a plan names no method as not in the cohort; the cohort has 40 variants including E_1; in a temporary project, a full batch runs E_1's pairs alongside the others, and E_1's SUCCESS pairs pass the same attempt and record checks (`attempt_state` DONE). |
| E1R2-T07 | **Archive (E2R-R55 and R56):** archived bytes equal the base commit's (verifier, every phase); exact file list; README fields; helper references resolve; the static no-import check; nothing on the suite's paths reaches `archive/`. |
| E1R2-T08 | **E2R-T15** on the synthetic E_998 tree, with and without `.git`. |
| (edits) | `test_e2r_dispatch`'s three `legacy_gate(..., '1')` become `'2'`. WF-1A's tests updated for `NOT_REAL_CAPABLE == {}`. Every other E_1 test reads the active entry, so it follows r2 unchanged. |

**Mutation checks**, each caught:
- r2's data-kind line admitting `REAL_HOLDOUT`;
- the legacy gate left at '1';
- an archived file with one byte changed;
- a README without its helper list;
- an import from `archive`;
- E_1 left in `NOT_REAL_CAPABLE`;
- r2's declaration differing in a field other than the revision;
- the archive missing one file.

## 7. After installation, and how it fits the measurement and ranking scheme

1. **The full-cohort batch (the owner declined ER-6, 31 October 2026).** Since WF-1A v2 (EX_083 B01), a batch never reuses another batch's runs. After installation, the owner plans and runs a new batch over the whole cohort, now 40 variants including E_1, over the same window: for Powerball 1145-1576, about 105 minutes on this estimate. The earlier 39-variant batch stays on record, unchanged and counted in the search log; nothing is deleted.
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

The owner chose ER-1 to ER-4 as recommended on 31 October 2026, before the review, and declined ER-6 on the same day. The reviewer may still raise a finding on any of them; a change would go back to the owner.

- **ER-1 (OWNER-CHOSEN 31 October 2026, before review; was RECOMMENDED): one package for CODE-3's tooling and E_1 revision 2.** CODE-3's tooling has no other use yet, and E_1 r2 is its first, and real, test. The option: CODE-3 alone first (tested only on the synthetic tree), then E_1 r2.
- **ER-2 (OWNER-CHOSEN 31 October 2026, before review; was RECOMMENDED): E_1 r2 installed and released in the same package,** as two named actions (section 5), an exception to E2R-R58's recommended two-step release, for E_1 only. The option: R58's two packages, with E_1 unrunnable in between.
- **ER-3 (OWNER-CHOSEN 31 October 2026, before review; was RECOMMENDED): the archive holds r1 complete, including files that r2 keeps unchanged and the legacy entry file;** an old path is removed only when the successor does not reuse it (section 4.2). The option: archive only the two files that change (then r1 is not complete in the archive).
- **ER-4 (OWNER-CHOSEN 31 October 2026, before review; was RECOMMENDED): the contract adapter's docstring is corrected,** with no code change, and is not archived (it is CODE-2's wrapper, outside E_1's folder). The option: leave the stale sentence, and list it as out of date in the register.
- **ER-5 (RECORDED): WF1-13 itself:** revision 2, and the legacy runner moved to revision 2. No new choice.
- **ER-6 (OWNER-DECLINED 31 October 2026; was RECOMMENDED): a method-restricted batch plan** (`plan --methods ...`), so that E_1 r2, and any method released later, could be run over past draws without rerunning the whole cohort. **Chosen instead:** a full-cohort batch, about 105 minutes for Powerball, of which about 103 minutes repeat runs already done, with every batch holding the complete cohort. The driver and its CLI keep their WF-1A form, apart from `NOT_REAL_CAPABLE`.

## 10. What the reviewer is asked to check (R-3)

1. That revision 2 changes nothing in E_1's counting, ranking or tie order (section 3), and that E1R2-T01 and T02 would prove it.
2. ER-2's exception to R58, and whether the two named actions are enough discipline.
3. ER-3's reading of "the old path is removed" for reused paths, against E2R-R54, R55 and T15.
4. The archive checks, the static no-import check and E2R-T15's synthetic test.
5. The legacy runner's move to revision 2 (D2-3 superseded by WF1-13), and that its goldens stay byte-identical.
6. The driver's change (`NOT_REAL_CAPABLE` becomes empty), and the full-cohort batch after installation (section 7).
