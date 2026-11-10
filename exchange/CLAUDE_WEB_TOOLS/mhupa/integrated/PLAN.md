# MHUP-A integrated install package - plan and checkpoint (Claude)

Started on 8 November 2026 after the owner's "go". If this chat ends, a new Claude chat continues from this file, from H-1 v1r8
plus the H-1 v1r10r3 delta (RAT-29), and from register v0.26. US-ASCII, CRLF. The owner is named only as "the project owner".

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
- 2026-11-08 20:50 Adelaide: DOC-13 ratified (RAT-27) and installed at 52b6de8 (verified); H-1 v1r10r2 ratified (RAT-28). The owner
  starts a new Claude chat on Tuesday 10 November 2026 from the H-1 v1r10r2 blurb; this plan continues there unchanged.
- 2026-11-10 18:30 Adelaide: **R-020 (g) DECIDED by the owner: option (i)** (the narrow rulebook v0.5 allowance for T016, with
  the reviewer's EX_157 section 3 conditions). Nothing else changed since 8 November. Next: item 2 (the package builder), Opus,
  in a fresh Claude chat started from the H-1 v1r10r3 blurb.
- 2026-11-10 20:38 Adelaide: **HO-2 closed** (the owner's GO, `exchange/HO2_2026_11_10/`): the new Claude chat (Opus 5.5)
  accepted; items 1 and 2 authorised; E2R-T12 approved for this cloud context only; Route A favoured; the predecessor's F1-F9
  are design inputs. Item 3 is NOT authorised yet.
- 2026-11-10 about 23:30 Adelaide (Opus 5.5): **items 1 and 2 done, PRELIMINARY/DRAFT.** Base `c48ac3c` (main unchanged
  since). DEV equals the reviewed overlay's 70 paths (65 identical; `.gitignore`, the three date files and the pinned test
  differ only as expected). Preliminary suites 570/570 PASS, 0 skips, on Linux Python 3.13.18 and 3.15.0b4 (working date
  2026-11-10). The builder `build_mhupa_pkg.py` and its templates: the gate closure computed (15 files, 10 changed: exactly
  the list), 570 tests in 45 modules counted by the loader, the draft package `MHUPA_Install_v1` (manifest SHA-256
  `fa034f33...7df1`), the verifier's `released` phase a refusing stub. Smoke steps 0-18 PASS on a synthetic root, LF and
  CRLF; 11/11 negatives STOP. **New finding N1:** the install/release records refuse after Git rewrites them with CRLF
  (reproduced); proposed fix: `.gitattributes` `src/methods/_common/contract_data/install_records/** -text` (needs the
  reviewer and the owner). N2 (`--no-renames` at step 12) fixed in the draft; N3 (synthetic root needs empty
  `source_data/` and `results/`). Full report: `ITEMS_1_2_REPORT_2026_11_10.md`. **Next: item 3 on Fable, after the owner's
  go.**
- 2026-11-10 23:24 Adelaide: the owner's decisions after the reviewer's focused review of items 1-2
  (`exchange/HO2_2026_11_10/MHUPA_Owner_Decisions_After_Items1_2_Review_2026_11_10.md`; the review beside it): D01 item 3
  AUTHORISED on Fable (High); D02 N1 approved in principle for the draft; D03 F1 timing approved in principle (not for
  execution); D04 Route A; D05 F2 NOT approved as submitted (F2-C01 the real Windows inventory at T016, F2-C02 both process
  oracles exactly, F2-C03 a full oracle matrix); D06 F4 accepted in principle; D07 S1 (the smoke script continued past the
  refusing `released` stub) to be corrected; D08 F5-F9 carried. No T016, rulebook install, settings edit or MHUP-A install.
- 2026-11-10 about 23:50 Adelaide (Opus 5.5, the packaging part before the switch to Fable): **N1 applied to the draft.**
  `build_dev_integrated.sh` appends `src/methods/_common/contract_data/install_records/** -text` to `.gitattributes` (and now
  refuses relative paths); the builder expects 37 new, 34 modified, 1 deleted (71 overlay files + 1 deletion = 72 changed
  paths; the staging list 73 with the install record). `records_eol_oracle.sh`: N1 ORACLE PASS (written and committed;
  fresh clone; re-checkout; full index reset; later ff pull: worktree = blob, LF, RECORDS PASS; the override negative STOPs;
  only the 3 records gain -text). Scope scan: no other unprotected byte-canonical file in the package. Next: item 3 on Fable.
- 2026-11-11 about 00:30 Adelaide (Opus 5.5): **new finding N4 (PRELIMINARY; not applied).** The full suite in a FRESH
  core.autocrlf=true clone of the installed draft tree (every text file CRLF, as a Windows clone after the install): 568/570;
  two tests fail on line endings, not on logic: `test_mhupa_process_check.Statics.test_imports_and_no_terminating_call`
  (asserts no CR in src/package_tools/process_check.py) and `test_mhupa_updater_v0_2.UpdaterV02Identity.
  test_reference_is_the_base_v0_1_and_v0_1_is_gone` (raw-byte SHA-256 of tests/fixtures/results_master_v0_1_reference.py.txt).
  T022 could not see it (the overlay is copied in LF); T017 or any fresh Windows clone after the install would. Same class as
  N1; proposed separately (D02): either -text for those two paths or CRLF-tolerant tests; the reviewer and the owner decide.
  Evidence: evidence_2026_11_10/N4_PRELIMINARY_suite_fresh_autocrlf_clone_py315.txt.
- 2026-11-11 about 02:30 Adelaide (Fable 5.2): **item 3 built; checkpoint `ITEM_3_CHECKPOINT_2026_11_11.md`.** The verifier's
  `released` and `staged` phases, barrier state in every phase, barrier order enforced by the copy tool, STOP-aware
  `rehearse_mhupa.py` (88 negatives, 0 failed; positive steps 0-18 PASS on LF and CRLF with step 10 omitted), a cold read
  (17 findings; tooling ones fixed). **N5 (BLOCKER for Appendix J step 10): the reviewed suite fails with U, E and P in place
  (21 modules); a barrier-free byte copy passes 570/570; option A (suite on a barrier-free copy) recommended; undecided.**
  N4 (two line-ending-sensitive tests) proposed, not applied. F2 oracle matrix written. Next: the reviewer and the owner on
  N5, N4 and F2; then rulebook v0.5 and the T016 task (Opus). Item 3's Fable work is finished.
- 2026-11-11 about 10:30 Adelaide (Opus 5.5): owner's yes (08:21) to N5 option A in principle and N4. Done in the DRAFT
  (`ITEM_3_FOLLOWUP_2026_11_11.md`): step 10 `--shadow` runner (barrier-free byte copy; only the six development master files
  as data, found by a no-data run); N4 plus N4b (a third -text line, awaiting the owner's yes); the release-record guard (U
  held, E absent; suite 571). Evidence `evidence_2026_11_11b/`: full positive 0-18 WITH step 10 PASS on LF/3.13 and
  CRLF/3.15; 571/571 in a fresh autocrlf clone; 88 + 9 negatives, 0 failed; N1 oracle PASS. Proposed: abandon-and-rebuild
  recovery for a fix after step 13/17; corrected F2 rows 8-9. Next: the owner on N4b, B, rows 8-9; then rulebook v0.5 and
  the T016 task (Route A).
- 2026-11-11 afternoon (Opus 5.5; owner away, draft work only): the reviewer's follow-up on fadd2b9 addressed (section 6 of
  `ITEM_3_FOLLOWUP_2026_11_11.md`): N4b owner-approved (09:32); N5-C01 cleanup failure is a STOP (10 step-10 negatives, 0
  failed); N5-C02 each of the six data files needed; a Windows defect fixed (the escape check now allows the project's own
  .venv inside the tree; proven with a venv inside the clone, 571/571); REC-C01 STOP texts for steps 13 and 17; the
  Appendix J deviations tabled. Final draft evidence `evidence_2026_11_11c/`: positive 0-18 WITH step 10 PASS on LF/3.13 and
  CRLF/3.15; 88 negatives 0 failed. Next: the owner and reviewer; rulebook v0.5 and T016 not started.
