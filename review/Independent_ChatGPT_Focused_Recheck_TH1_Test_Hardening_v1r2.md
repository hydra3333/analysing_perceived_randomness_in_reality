# Independent ChatGPT focused recheck - TH-1 v1r2

**Date:** 27 October 2026 (Adelaide)  
**Role:** Independent reviewer (H-2 v1r2)  
**Author:** Claude primary development chat  
**Review subject:** `TH1_Test_Hardening_v1r2.zip`  
**Package SHA-256:** `47d6e5a67eb60b045c9b3c1b0930f0ced2ad082cee47dbdd93caaa74196c3015` - VERIFIED  
**Declared base:** `997ed46081695c0be68fd5b5db2efa95ce838a8b`  
**Disposition:** **PASS - 0 BLOCKER / 0 CORRECTION / 0 OPTIONAL / 0 RECONSIDER.** Recommend owner acceptance consideration and owner-controlled installation; this review is not acceptance or permission to run anything further.

## 1. Scope and provenance

This is a **focused recheck of v1r2 against reviewed v1r1**, not a fresh general review of Package 2 or its scientific rules. It addresses outstanding TH1-C01 (synthetic longer-suffix row invalid under the Powerball numeric grammar) and TH1-O01 (verifier path-count typo), and confirms that the v1r1 Windows link-test change remains intact.

The supplied r1 and r2 ZIPs were compared byte-for-byte in an isolated workspace. Of five `repo_overlay/` payload files, **only** `tests/test_p2_r1_t05_hardening_v1.py` changes. The coordinator-v0.6 fixture, both existing test modules, and the transition verification record are byte-identical to r1. Packaging support files (handback, instructions, verifier, mutation script/results and suite evidence) appropriately changed, and `evidence/t05_module_v1r1_to_v1r2.diff` was added. The supplied module diff **exactly** equals an independently generated unified diff from the two archived module versions, including its headers.

The revised T-05 module SHA-256 is `c3341ce2fa7409335f6232c0f65b2d9b5a1b2d03fde6ee863e4fe4e30c8b9e58` (VERIFIED). The revised verifier uses this same hash and correctly describes five installation paths. Existing fixture and test hashes match the verifier's expected map.

In the isolated reproduction tree, the unchanged production reader SHA-256 was `e06e0cca7edc298aadf5298ae860d6093467f6460fcbf9839928b1e4fdb342b5`; coordinator SHA-256 was `bc8380b5f20a704c0f47d5f76eeb86156237142b5639e5b9770b8314db3bb822`. The verifier statically protects both and register v0.5. No change to those sources is requested or delivered.

## 2. Findings and reproduction

### TH1-C01 - CLOSED

**Location:** `tests/test_p2_r1_t05_hardening_v1.py`, `synthetic_row()` (roughly lines 35-57), and new `T05HardeningTests.test_every_suffix_variant_row_is_a_valid_row()` (roughly lines 152-173).

Variant 3 now quotes all numeric CSV fields instead of appending invalid trailing spaces to the last numeric field. It remains a *longer* synthetic suffix and is valid when the changed row is intentionally moved inside the eligible prefix. The added grammar test exercises both game profiles, four variants, three view kinds and both date settings (**48 subtests**), loading the first changed row through the real reviewed reader. This closes the precise deficiency identified in v1/v1r1, without exposing actual results.

### TH1-O01 - CLOSED

**Location:** `VERIFY_TH1_INSTALL.py`, module docstring around line 11. The previous contradictory `4 paths (3 added, 2 modified)` now correctly states `5 paths`. The verifier's expected new test-module hash was updated; no installation logic change was identified in the v1r1-to-v1r2 verifier comparison beyond these changes and the revision label.

### Independent R-2 reproduction

Used a separate, previously reconstructed offline repository tree with the v1r2 test overlay applied. This is an independent Linux reproduction, **not** a fresh checkout or Git-blob verification of base HEAD. Environment: Python **3.13.5**, NumPy **2.3.5**, psutil **7.2.2**.

- Author-specified seven-module nondestructive offline `unittest` suite: **60 tests, OK, 0 skipped; exit code 0**.
- Two T-05 hardening tests, including the 48-subtest grammar test: PASS.
- Non-skipping coordinator v0.6 protected-function AST check: PASS.
- Independently invoked supplied mutation-check driver on disposable copies: **11/11 mutations caught**, including the specific regression mutant restoring v1's invalid trailing padding; that mutant produces the expected six Powerball errors, while the unmutated test passes.
- Diff matching: the supplied r1-to-r2 T-05 module diff and the independently reconstructed diff are **exactly identical**.

The tests ran on local synthetic temporary masters and the already approved development-prefix offline regression inputs. No test performed network acquisition, science execution, process termination, lifecycle probes, dependency upgrades, or holdout scoring. The project files in the user's working tree were not edited.

## 3. Limitations / what was not tested

- **No Windows 11/Python 3.14.8 run of v1r2 by this reviewer.** The owner's reported previous Windows suite was for the pre-TH-1 tests. Windows symlink creation remains privilege-dependent; a skipped symlink subtest is not treated as a PASS, and the hardlink subtest must still run when hardlink creation succeeds.
- Did not execute the installer, staging `.cmd`, or installation verifier against the owner's Git repository. The supplied verifier was statically inspected; it uses `git --no-optional-locks` and `GIT_OPTIONAL_LOCKS=0`.
- No claim of live operational, Windows lifecycle, scientific, Mode H, FINAL, or holdout acceptance.

## 4. Reviewer decisions / owner oversight

**REVIEWER-DECIDED TH1-RD-03:** Close TH1-C01 after verifying both the valid quoted-field fixture and the independently run grammar regression/mutation. **REVIEWER-DECIDED TH1-RD-04:** Close TH1-O01; issue a focused **PASS** for TH-1 v1r2 within the authorised offline test-hardening scope. These are routine review decisions, not changes to ratified rules or safety gates. Claude should include them in the owner's first-three-reviews reporting, without treating that reporting as authority to override the review.

**Recommendation:** Present the exact v1r2 ZIP/hash and this PASS to the project owner for acceptance and an owner-controlled installation decision. No revision is requested. Maintain normal before/after Git-blob verification; continue to treat Windows evidence and operational gates as separate matters.

## 5. Paste-ready handoff to Claude

```text
For: Claude primary development chat
Subject: TH-1 v1r2 - ChatGPT focused independent recheck

VERDICT: PASS
0 BLOCKER / 0 CORRECTION / 0 OPTIONAL / 0 RECONSIDER.

Package SHA-256 VERIFIED:
47d6e5a67eb60b045c9b3c1b0930f0ced2ad082cee47dbdd93caaa74196c3015

TH1-C01 CLOSED: the longer variant uses valid quoted numeric CSV
fields. The new 48-subtest grammar check passes with the
rewritten row included in the eligible prefix.
TH1-O01 CLOSED: verifier now says 5 paths.

Only the new T-05 module changed among the five overlay files;
all four other overlay payloads are byte-identical to v1r1.
The r1-to-r2 module diff reproduces exactly.

R-2 independent Linux reproduction (Python 3.13.5,
NumPy 2.3.5, psutil 7.2.2):
- Full authorised offline suite: 60 OK, 0 skipped.
- Mutations: 11/11 caught, including old invalid padding.
- Coordinator protected v0.6 AST test: PASS, no skip.
- Production reader/coordinator hashes unchanged.

REVIEWER-DECIDED TH1-RD-03: close TH1-C01.
REVIEWER-DECIDED TH1-RD-04: close TH1-O01 and PASS v1r2.
Please report these under the owner's first-three-reviews
oversight procedure. No departure from ratified rules found.

No owner-Windows v1r2 acceptance, installation, operational
or scientific permission is implied.
Recommend owner acceptance consideration and controlled install.
```

*End of focused recheck.*
