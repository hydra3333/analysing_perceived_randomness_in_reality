# Claude review of Package 2 v0.11, v1

**Reviewer:** Claude (independent reviewer).
**Date:** 26 October 2026 (Adelaide).

**Reviewed:** `Predictive_Randomness_MultiGame_Package2_v0_11_CLAUDE_REVIEW_ONLY.zip`, SHA-256 `0e00e231c46dafd01df52fb6f50db6ceaf399ea27be40efb318529101611d74c` (ChatGPT coding chat).

**Baseline:** `618fe48` (verified earlier from a clean clone). The scratch tree was built as `git archive 618fe48` plus `repo_overlay/`. The retired list was checked: none of the 21 paths exists at HEAD.

**Status:** review only.
- No installation, Windows run, real-science run, holdout access or network was used.
- Tests were run offline in Claude's Linux sandbox: Python 3.13.16, NumPy 2.5.3, psutil 7.2.2.
- No draw results appear here.

## 1. Verdict

**One BLOCKER, one CORRECTION, a few OPTIONAL items.** The package is careful and close to acceptable.
- C1, C3, C4, C5 (real-data part) and C6 are met.
- C2 is met for reading.
- The blocker concerns what the method-facing view carries, not how the master is read. Its fix is small and local.

## 2. What I verified independently

| Check | Result |
|---|---|
| ZIP SHA-256 | matches the value above |
| 26 overlay files against `SHA256_MANIFEST.json` | all match |
| Offline suite (the six modules in README) | **56 tests, OK.** 1 skipped: `test_protected_v06_ast_mechanically_equal_when_baseline_available`, which needs a baseline path not present in my tree; covered by my own AST check below |
| `evidence/COORDINATOR_V06_TO_V011_EXACT.diff` applied to committed v0.6 (`2e23d550...`) | reproduces the shipped coordinator **byte for byte** (`bc8380b5...b822`) |
| Protected functions (own AST comparison, all 11) | **all identical** |
| Changed unprotected functions | `arguments`, `capture_owned_tree`, `coordinator_main`, `drain`, `read_lines`; added `receive_messages`. Reviewed in section 4 |
| Switches | `ENABLE_PROCESS_TERMINATION`, `ENABLE_SCIENTIFIC_COORDINATION`, `ENABLE_SYNTHETIC_WINDOWS_LIFECYCLE` all `False` |
| Scientific allowlist | `_COORDINATED_SCIENCE_ALLOWLIST = MappingProxyType({})` |
| Real E_1 goldens | asserted in tests: view `d47fbbd6...4339`, forecast `7f113087...164e` |
| R2 5.5 synthetic goldens | **reproduced by committed `e1_historical_appearance_frequency_v0_3.py` on `tests/p3_e1_synthetic_v0_3.json`:** `df21871f...`, `7ce5ab1b...`, `7b43d659...`. Not asserted by any test (correction C1 below) |

## 3. BLOCKER

### B1. The method-facing `DrawView` exposes the whole-master SHA-256

**Where:** `game_draws_reader_v1.py`:
- `load_pinned_draw_view` builds `order_evidence = {'record': evidence_name, 'master_sha256': sha}`;
- `DrawView.order_evidence` stores it for the `OPERATOR_DRAWN_ORDER` and `PAIRED_DIAGNOSTIC` views;
- `test_dates_opt_in_schema_digest_and_order_evidence` asserts it (line ~143).

**Why it is a blocker:** the whole-master hash depends on every row, including rows at and after the target. A method holding the `DrawView` therefore holds a value derived from future rows.
- **Concrete channel:** at the last development target (Powerball 1576; Oz Lotto 1693), the only row after the prefix is the target draw itself. A method could enumerate the target's possible outcomes and recompute the file hash until it matches, which recovers the target outcome exactly:
  - Powerball: the row is stored in drawn order, so about 6.6 x 10^11 ordered rows. That is feasible: precompute the hash state over the prefix, then hash only the last row of about 40 bytes for each candidate.
  - Oz Lotto: about 1.9 x 10^16 ordered rows, impractical. The value still breaks T-05 and must still go.
- **T-05 consequence:** changing target-and-later rows changes `DrawView.order_evidence`, so the method's inputs are not identical. That breaks R2 T-05 and the rule that the master SHA is provenance only, never available to a predictor.
- **What is already right:** excluding the hash from the view digest is correct, and keeping it in the run manifest is correct. Only its presence inside the method-facing object is wrong.

**Required change:**
1. Remove `master_sha256` from `DrawView` entirely. `order_evidence` may carry only outcome-independent identifiers, such as the evidence record's file name and the status label `OPERATOR_DRAWN_ORDER_ASSUMED_OWNER_DECISION`.
2. Keep the full SHA, ledger version and INIT record identity in the orchestration-side run manifest and receipt only.
3. **New test** (for each of the three view kinds): with a fixture ledger re-pinned to a master whose rows at and after N were changed, every `DrawView` field, every array byte and the view digest are identical. A static check that no `DrawView` attribute holds any 64-hex value equal to the master, ledger or INIT-record file hash.
4. Update the test at line ~143, and the closure note's C2/C3 wording ("separately bound SHA metadata").

## 4. Coordinator changes (C4/C6): reviewed, acceptable

- **Constants:** match the owner-decided values (1.0/0.5/5.0, 5.0, 0.5/15), and `--poll-seconds` is bounds-checked. The 0.12 and 0.05 literals are named; the 3.0 and 3 waits stay inside protected `terminate_owned_tree`.
- **Capture throttle:** equals the poll interval, with a forced capture at launch.
- **Waiting:** `drain(block=True)` replaces the 40 ms sleep, giving human-speed waits that wake on output. The main loop still checks exit, timeout and capture every iteration, at most one poll interval apart.
- **Exit timing:** `exit_observed_utc` is set at the coordinator's first observation of the Popen exit.
- **Console record cap of 8** (`reader_error` beyond that): existing probes print at most 4 such lines (BEGIN, RESULT, DIGEST, FINISH), so ordinary POC runs are unaffected.
- **Scientific receipt branch:** unreachable while the switch is False (any populated identity with the gate off gives FAIL). When reachable, it fails closed: it checks the trusted issuer path, rechecks for orphans, requires a run-matched status PID with creation time, and issues create-only receipts.
- **`--synthetic-contract-test`:** refuses unless its source gate is True, with no CLI override.
- **Return code:** follows `final['success']`, so a failed receipt path can no longer exit 0.

## 5. Reader (C1-C3): otherwise sound

- **C1:** each array is backed by its own freshly created `bytes`, is read-only and int64, and dates are `datetime64[D]`. Shapes are checked. `simple_rows` returns plain Python ints. The 47 x 47 = 2209 test is present.
- **C2:**
  - The manifest's key set is exact. Ledger version 1 / INIT / SHA / first-last / count are all bound, as are the master SHA over all bytes and the INIT record identity.
  - Symlinks and hard links are refused, and the file is checked for change during the read.
  - Rows are read one line at a time, with a raw first-field digit check before decoding, and **no line at or beyond N is read**.
  - Error messages are value-free.
  - Target 1577 is allowed only for the E_1 legacy forecast-only case.
- **C3:** dates are opt-in and checked against the profile's derived weekly date (a mismatch halts with a value-free error); a new schema is used with dates. The E_1 legacy digest is unchanged. New schemas bind game, era, profile version, method, variant, target, view kind, dates and order assumption. Oz supplementaries are never converted or stored.

## 6. CORRECTION

### C1. Assert the ratified R2 5.5 synthetic goldens

`C1_C6_CLOSURE_AND_REVIEW_REQUEST.md` (C5 row) describes `3851fa46...` / `8a7f917a...` as the synthetic goldens. Those belong to the later standalone runner's synthetic test. That is useful, but it is not the ratified set.

R2 5.5 (and the TIE contract v0.2) ratify `df21871f...` (training view), `7ce5ab1b...` (MAIN label-3 tie) and `7b43d659...` (canonical forecast), from `tests/p3_e1_synthetic_v0_3.json` at target 1152. No test in the repository or package asserts them.

**Fix:**
- Add a test asserting all three, using the committed v0.3 module. It passes today; I reproduced all three.
- Keep the standalone-runner assertions.
- Relabel the closure note to list both sets, distinguished.

## 7. OPTIONAL

- **O1:** `_trusted_file_bytes` checks only the final path component for a symlink. Optionally also confirm that the resolved path lies under `repo_root/source_data`, which would catch a symlinked parent folder.
- **O2:** add to the Windows TO-TEST list that `os.fstat().st_nlink` reports hard links correctly on the owner's NTFS checkout.
- **O3:** `coordinator_private/multigame_windows_lifecycle_v1.py` (gated False, not executed) was checked only for its timing constants this round. A full review is due before any Windows synthetic-lifecycle gate is proposed.
- **O4:** the `requirements.txt` header marking it historical satisfies the earlier O3. No objection.

## 8. Next step

ChatGPT fixes B1 and C1 as v0.11-r1, a small local delta with tests. Claude then does a focused check of that delta. No Windows run is implied by either.

```text
Claude review of Package 2 v0.11 (0e00e231...d74c): ONE BLOCKER, ONE
CORRECTION; otherwise C1, C3, C4, C5-real, C6 met and C2 met for reading.
Verified independently: 26 manifest files; scratch 618fe48+overlay; 56/56
offline tests OK (1 skip = baseline-path AST test, covered by Claude's own
AST check); exact v0.6->v0.11 diff reproduces shipped coordinator bc8380b5;
11/11 protected ASTs identical; 3 switches False; allowlist empty; real E_1
goldens asserted; coordinator edits reviewed and acceptable.
B1 BLOCKER: DrawView.order_evidence carries master_sha256 (whole-master hash,
depends on rows >= N) into the method-facing object for OPERATOR_DRAWN_ORDER
and PAIRED_DIAGNOSTIC views. At the last dev target (PB 1576 / Oz 1693) the
only post-prefix row is the target itself, so a method could brute-force the
outcome by matching the file hash; also breaks T-05 (inputs change when
suffix rows change). Excluding it from the view digest was right; keeping it
in the run manifest is right; it must not be in DrawView at all. Fix: remove
master_sha256 from DrawView/order_evidence (record name + status label only);
keep full SHA/ledger/INIT identity orchestration-side; add a T-05 test per view
kind (re-pinned fixture ledger, changed rows >= N -> every DrawView field,
array byte and digest identical) and a static check that no DrawView attribute
equals a master/ledger/INIT file hash; update test ~line 143 and closure text.
C1: the closure note calls 3851fa46/8a7f917a "the synthetic goldens" - those
are the standalone runner's. Add a test asserting the RATIFIED R2 5.5 /
TIE v0.2 vectors df21871f / 7ce5ab1b / 7b43d659 (tests/p3_e1_synthetic_v0_3.json,
target 1152, committed v0.3 module - Claude reproduced all three); relabel.
Optional: resolved-path check under source_data; Windows TO-TEST for
st_nlink; full review of the lifecycle module before any lifecycle gate.
Please deliver v0.11-r1 as a small delta; Claude does a focused check.
```

*End of document.*
