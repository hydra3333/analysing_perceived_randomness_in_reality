# MHUP-A integrated install package - plan and checkpoint (Claude)

Started on 8 November 2026 after the owner's "go". If this chat ends, a new Claude chat continues from this file, from H-1 v1r8
plus the ratified H-1 v1r10r1 delta (RAT-26), and from register v0.25. US-ASCII, CRLF. The owner is named only as "the project owner".

## Where things stand

**Base.** The base is current main, `009c985` on 8 November 2026. The base is new because of three earlier changes:
- the GAIS move out of `src/`;
- the history clean-up (`main` 6b99029 -> 9d28b9f; crosswalk in `exchange/HISTORY_CLEANUP_2026_11_06/`);
- the owner's OUTLANDISH commits, which touch only `GAIS/`, `.gitignore` and the new `create_venv.bat`.

The reviewed candidate's base was `2061055`.

**Rebuild.** The development tree was rebuilt on `009c985`:
- build command: `build_dev_slice2.sh BASE DEV TOOLS DATE`, with BASE = `git archive HEAD` of `009c985`;
- result: identical to the reviewed v1r2 overlay (`exchange/EX_151_Claude/MHUPA_Slice2_Review_v1r2.zip`) in 66 of 70 files;
- the other four differ only as expected:
  - `.gitignore`: the MHUP-A block is appended after the owner's new lines, by `apply_slice2.py`;
  - E_1 revision 3's two registry `entry_0003.json` files and `archive/methods/E_001/r2/README.md`: the date argument
    (2026-11-08 here, 2026-11-04 in the candidate).
- **C01-EFF:** the final date is set when the package is frozen for review. Then rebuild and rerun everything.

**Suite.** The full suite runs on both Pythons on the rebuilt tree: `suite_integ_py313` and `suite_integ_py315` in the scratch
logs (see the checkpoint lines below).

## What the integrated package needs (design Appendix J; EX_152 section 5; R-019; R-020)

1. **The package manifest** (JSON, inside the package):
   - base commit;
   - NEW, MODIFIED and DELETED paths with their LF SHA-256;
   - the step 6 gate list: `contract_dispatch.py` and the changed modules it imports;
   - the step 8 rest;
   - `release_entries`: E_1 revision 3 for POWERBALL and OZLOTTO (R-020 (a));
   - the SHA-256 of the package's `process_check.py`;
   - roster-changing = true.
2. **A copy tool** (standard library): `copy --part gate|rest`, from the staging folder into the repository. It refuses outside
   the listed paths and checks each written file's SHA-256.
3. **The verifier** (standard library; from `wf1/verifier_template.py`), with phases:
   - `pre`: clean tree; HEAD = base or a descendant; base bytes; `process_check.py` in staging matches the manifest;
   - `post`: exactly the overlay changes, `src/results_master_v0_1.py` deleted;
   - `committed`: the package commit has exactly the overlay plus `INSTALL_MHUP_A_V1.json`, whose fields name the package and
     the manifest digest;
   - `released`: the release commit's only parent is the package commit; it adds exactly `RELEASE_MHUP_A_V1.json`; that record
     names E_1 r3 for both games, the install record's digest and a date not earlier than the install record's; E and P absent;
     the record agrees with the repository (EX_148 (ix)).
4. **The owner's install instructions:** Appendix J steps 0-19 as exact CMD lines. They use `process_check.py` from staging
   (`take-install-lock`, `check-no-runs --install`, `release-install-lock`), the copy tool, the verifier, the suite runner and
   `install_records.py`. Each STOP is handled as Appendix J's table says. Each line is checked with `check_task_commands.py`
   where Claude Code rehearses it.
5. **Rehearsals:**
   - LF and CRLF checkouts on Linux, end to end in scratch clones;
   - **T016** for Claude Code on Windows: the whole install in a task clone. Step 19 (push) is impossible there, and steps 3
     and 18 use a synthetic `source_data` lock path in the clone.
6. **The negative tests Appendix J lists:** most already exist in slice 2 (`test_mhupa_process_check`,
   `test_mhupa_install_records`). The integrated package adds the verifier's own negatives: a missing or wrong-byte file at
   POST; a wrong install record; a release commit with an extra file; the wrong parent.
7. **Rulebook rule 7 additions:** `create_venv.bat` (it changes the venv the freeze records), and the owner's settings deny lines
   for the MHUP-A programs.
8. **The review message (at the next free EX number; not EX_157, which is the reviewer's handover check)** to the reviewer, with:
   - the assembled ZIP and manifests;
   - base and target identities;
   - the test and mutant inventories;
   - T022 and later T016 evidence;
   - the owner's decisions DEP-1 and GAIS-1;
   - an explicit list of the offline tests the owner authorises the reviewer to run (EX_155 Q15).

**Model split (owner's rationing, MC-1):** Opus for items 1, 2, 4, 5, 7 and 8 and the template parts of 3. Fable (after the
Tuesday 10 November reset) for the `released` phase, the two-commit and barrier-order proofs, and a cold read of the install
instructions against Appendix J.

## Handover pointer

If you are a new Claude chat: read `exchange/HANDOVER_2026_11_06/Claude_Primary_Handover_H1_v1r10r1_delta.md` first (section 7 is
this plan in order, with the model split and the T016/rulebook question, R-020 (g)). The previous chat's scratch trees are gone;
rebuild with `build_dev_integrated.sh` (section 7, item 1 there).

## Checkpoint log

- 2026-11-08 18:15 Adelaide: rebuild done and checked (above); suites started.
- 2026-11-08 18:45 Adelaide: **PRELIMINARY: the full suite on the rebuilt tree, on Linux Python 3.13.18 and 3.15.0b4: 570 ran, 569
  passed, 0 skips.** (Final evidence is produced on the date-frozen candidate; EX_157 C01.)
  - **The one failure on each Python:** `test_e1r3_revision3`, which pins E_1 r3's `effective_date` to the candidates'
    2026-11-04. This is the C01-EFF consequence, not a code fault.
  - **The fix:** `integrated/build_dev_integrated.sh` wraps `build_dev_slice2.sh` and makes one counted edit setting that
    test's expected date to DATE. The test keeps checking the exact date.
  - **Recheck:** with the fix, that module passes on both Pythons (8/8). The other 562 tests are unaffected by the edit.
  - **Evidence:** `integrated/evidence/suite_rebuild_009c985_py313.txt` and `_py315.txt` (before the fix).
  - **Still to come:** the full 570-test suite and both mutation chains on the final frozen tree; nothing else counts as evidence.
- **Step 6 gate list** (from `contract_dispatch.py`'s import closure, restricted to files the package changes or adds): **10 files**
  (an earlier line here said 11; EX_157 C02). The builder must recompute the closure and assert it equals this list.
  - Changed: `contract_dispatch.py`, `contract_forecast.py`, `contract_receipts.py`, `contract_records.py`,
    `contract_runner.py`, `contract_task.py`, `contract_vocab.py`, `game_draws_reader.py`.
  - New: `master_versions.py`, `owner_records.py`.
  - All under `src/methods/_common/`.
- **The manifest schema** the tools already read (`install_records.load_manifest`, `process_check.load_install_manifest`):
  - `package` = `MHUP_A`;
  - `release_entries` (E_1 r3 for both games);
  - `retires` (empty);
  - `registry_entries_added` (the two `entry_0003.json`).

  The verifier and copy fields are added beside them.
- **Next:** `integrated/build_mhupa_pkg.py`, which builds the manifest, the copy tool, the verifier (from
  `wf1/verifier_template.py`, adding the `released` phase) and the owner's instructions.
- 2026-11-08 19:30 Adelaide: the reviewer's EX_157 checked the v1r10 handover: C01 (suite status overstated), C02 (gate count),
  C03 (order: freeze the date and assemble first, then all final evidence on that candidate; the R-020 (g) decision before the
  rulebook change), O01-O04. All applied (v1r10r1; EX_158). **The order of work in the handover's section 7 replaces the list in
  "What the integrated package needs" above where they differ.** The integrated package's review message takes the next free EX
  number, not EX_157.
- 2026-11-08 19:45 Adelaide: the reviewer's EX_159: focused recheck of EX_158, **PASS** (C01-C03, O01-O04 resolved), with one
  non-blocking editorial point O05 (stale pointers; tidied here and in the handover README; the delta's own "section 7, item 8"
  in its section 2 should read "item 7", left for the next full H-1 edition). **RAT-26 (owner, 8 November 2026, about 19:43):
  H-1 v1r10r1 delta and blurb ratified as working supplements to H-1 v1r8**; installed by the owner in `doc/HANDOVER/` at
  `b866e42` (v1r10 copies removed). R-020 (g) remains OPEN.
