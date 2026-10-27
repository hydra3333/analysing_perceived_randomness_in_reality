# Independent ChatGPT review - TH-1 offline test hardening v1r1

**Date:** 27 October 2026 (Australia/Adelaide)  
**Reviewer:** ChatGPT independent technical/scientific reviewer, H-2 v1r2  
**Author:** Claude primary designer/coder  
**Classification:** HIGH (reader-isolation and protected coordinator verification tests)  
**Package:** `TH1_Test_Hardening_v1r1.zip`  
**Package SHA-256 (independently verified):** `e01fd9718de80193484f4c430bc9069f26766ec88e884b141c925a3b8b3cc0a0`  
**Declared base commit:** `997ed46081695c0be68fd5b5db2efa95ce838a8b` (not independently verified against remote Git in this review)  
**Supersedes:** TH-1 v1 `f056d3619a9e7ca4767a34dc515ad928b67ca21090134e746845653414b06fa3`

## Verdict

**0 BLOCKER / 1 CORRECTION / 1 OPTIONAL / 0 RECONSIDER.**

The r1-specific reader-link portability change **PASSES focused review**. The symlink and hardlink tests are now independent `subTest` cases; a simulated inability to create a symlink records a skip and, critically, the hardlink test still executes and verifies rejection. The packaged synthetic test suite reproduced as **59 tests OK, 0 skipped** on Linux, and all **10/10** supplied mutation categories were independently caught. The existing P2-R1-O3 fixture-based AST test remains unskipped and passing.

However, **TH1-C01 from the earlier v1 independent review is still outstanding**. As r1 deliberately preserves the v1 T-05 module byte-for-byte, its longer-suffix fixture continues to create an invalid Powerball numeric field despite the design's assertion that all later rows are valid. Accepting the package without correcting that claim/fixture would lose the earlier finding. It is a focused correction to test data generation, not an objection to the test-hardening design or reader implementation.

## CORRECTION TH1-C01 - unresolved v1 longer-suffix fixture

**Exact location:** `tests/test_p2_r1_t05_hardening_v1.py`, lines 46-52; related claim in `HANDBACK.md`, section 1 ("every row structurally valid" and valid synthetic suffix variants).

**Status:** RETAINED from the v1 review. The file is byte-identical between v1 and v1r1, SHA-256 `7e68542d5f464c910f7c94eccd9aae57089170846fb7224a4727814b88b25278`.

**Failure scenario reproduced independently:** `synthetic_row(..., variant=3)` uses single-digit MAIN values then appends 40 literal spaces after the final field. For the Powerball profile the final field is the separate Powerball number. Building a *fully synthetic* master with that variant and asking the unchanged reader to admit its first mutated row as an eligible prefix raises `ValueError: invalid prefix Powerball`. The same file passes when the target stops before that row, explaining why the full T-05 test can be green although the promised later-row validity is false. For Oz Lotto, the prefix reader ignores supplementary columns, but this is not a substitute for structurally valid synthetic master rows.

**Suggested exact replacement** for the final sequence/line block at lines 48-52, preserving the existing variant-3 MAIN alteration:

```python
    seq = [draw, profile.derived_date(draw).isoformat(), *main, *extra]
    fields = list(map(str, seq))
    if variant == 3:
        # Quoted numeric CSV fields are valid but make suffix rows longer.
        fields[2:] = [f'"{field}"' for field in fields[2:]]
    return ','.join(fields)
```

The independent reviewer re-tested this change **in memory only** (without editing the submitted files): the full new T-05 test passed with this encoding. A separate explicit synthetic-row grammar check is recommended to show that each suffix variant remains parseable even when its first changed row is considered eligible, without ever parsing real target-or-later rows. For the final synthetic development target, a row-level grammar check avoids treating real holdout targets as authorised observations.

**Requested action:** Claude authors a narrow v1r2 fix to the synthetic generator, regenerates hash/evidence and submits a narrow recheck. The owner decides acceptance. No production source change or new scientific authority is requested.

## OPTIONAL TH1-O01 - verifier docstring count

**Exact location:** `VERIFY_TH1_INSTALL.py`, line 11. The `committed` phase description says "exactly those 4 paths (3 added, 2 modified)". Three plus two is **five**, and the verifier's executable checks correctly expect five paths. This is only a documentation typo.

**Suggested replacement:** `after the commit: clean tree; the last commit changed exactly those 5 paths (3 added, 2 modified), all with the expected Git blobs.`

The reviewer recommends correcting it while rebuilding the package; it does not by itself prevent acceptance. No test logic changes are needed.

## r1-specific positive findings and independent reproduction

1. **Package integrity:** SHA-256 matched exactly. Five overlay file hashes match the handback and install verifier; there are three new repository paths and two modified test modules, plus wrapper/instructions/evidence kept outside the repository overlay.
2. **Change isolation:** Compared the actual v1 and v1r1 archives. The original T-05 source, protected-AST test source, coordinator-v0.6 fixture and transition verification record are byte-identical. The only additional repository test-code change is `tests/test_multigame_v011_reader_contracts.py`; its unified diff independently reconstructs `evidence/reader_test_change.diff` byte-for-byte. Supporting handback, verifier, staging instructions and mutation evidence changed consistently with five overlaid paths.
3. **Reader-link design:** The symlink target is now a real file and symlink and hardlink cases are separate subtests. The `finally` clause restores the ordinary master after a failed symlink creation, permitting the hardlink check. An inability to create a link is a recorded skip, not a pass.
4. **Failure-path probe:** In a disposable isolated tree, mocked `Path.symlink_to` to raise `PermissionError` (a cross-platform proxy for the Windows privilege refusal). The symlink subtest registered exactly **one skip**, with no error/failure; an independently instrumented spy confirmed the hardlinked master was still presented to the reader, with rejection required by the assertion. This validates the intended continuation, not actual Windows behaviour.
5. **Ordinary suite:** Reconstructed an isolated offline tree from earlier supplied repository/source overlays plus the r1 five-file overlay. Linux Python **3.13.5**, NumPy **2.3.5**, psutil **7.2.2**. Ran the seven specified `unittest` modules. **59 tests ran, 0 errors/failures/skips, exit 0.** The new T-05 and protected-AST tests pass as before.
6. **Mutation tests:** Inspected and ran r1's author-supplied `evidence/mutation_checks.py` in disposable copies only. All **10/10** mutants were detected; importantly the two additions (reader accepts hardlinks and reader follows symlinks) both failed their targeted link test. A green test suite or mutants does not imply exhaustive correctness.
7. **Windows evidence:** Inspected `owner_windows_run_20261027_before_TH1.txt`. The *pre-TH-1* suite recorded the symlink privilege exception `WinError 1314` before the hardlink assertion, 58 tests with one error and two skips. It supports the motivation for r1. It is **not** a post-r1 Windows reproduction. The dependency-check transcript reports no installed-version changes.
8. **Scope and safeguards:** No production reader, coordinator, golden, safety switches, result allowlist, governing document or actual master is included in the overlay. The install verifier is statically read-only, uses `git --no-optional-locks` and `GIT_OPTIONAL_LOCKS=0`, and guards the three sensitive existing files. Its staging script is a distinct write-capable owner action. Neither verifier nor staging script was executed by this reviewer.

## Limits and safety

- The isolated test tree is reconstructed from previously provided packages, not an independently fetched Git checkout at base `997ed46`. The author's Windows environment and NTFS link behaviour were **not independently tested**; Windows results after r1 remain outstanding.
- The ordinary existing offline test suite reads only the previously supplied accepted development-prefix masters. The new T-05 test creates entirely synthetic data. No quarantined/holdout outcomes were inspected, printed or used.
- No remote Git operations, dependency upgrades, installation/staging, Windows process/lifecycle tests, coordinator launch, real scientific evaluation, lottery-result acquisition or safety-switch modifications were performed.
- All execution authorisation and repository acceptance remain with the project owner.

## REVIEWER-DECIDED entries (first-three-review owner reporting)

**TH1-RD-01 (carried forward):** Treat TH1-C01 as a narrowly scoped synthetic fixture correction rather than a redesign or permission to modify the production reader. The prior v1 finding remains binding for acceptance because r1 left its exact source unchanged.

**TH1-RD-02 (new routine disposition):** Accept the r1 symlink/hardlink test separation as a correct high-risk, tests-only design improvement; no additional design-stage round or platform-dependent hard failure is required where the symlink-creation privilege is unavailable, provided the skip is explicit and the hardlink subtest proceeds.

Both reviewer decisions are routine review dispositions, not authorisation to change ratified science/safety/process rules. Claude should list both in its required first-three-reviews report to the project owner. No apparent departure from ratified safety or process policy was found.

## Next action

Claude should submit a narrowly revised package correcting TH1-C01 (and optionally the verifier's four/five typo), with regenerated package/file hashes and focused offline evidence. A focused ChatGPT reviewer recheck is sufficient; the project owner then decides acceptance and installation. No live or scientific gates open.
