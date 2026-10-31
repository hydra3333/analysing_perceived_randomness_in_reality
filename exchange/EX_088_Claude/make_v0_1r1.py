"""Design v0.1 -> v0.1r1 (answers EX_087: B01, C01, C02, O01). Counted in-place edits; every old string once."""
import hashlib, sys
src, out = sys.argv[1:3]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == '6cff9f90be573141e48c532f09cac6d2d0a45d2278f07e1ac4847a033091e6e8'
s = raw.decode('ascii')
E = []
def r(a, b):
    global s
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b); E.append(a[:50])

r("# Predictive Randomness - CODE-3 (retirement tooling) and E_1 revision 2, design note v0.1\n",
  "# Predictive Randomness - CODE-3 (retirement tooling) and E_1 revision 2, design note v0.1r1\n")
r("**Version:** v0.1 DRAFT for the reviewer's design review (R-3), 31 October 2026. Author: Claude. Ratifier: the project owner.",
  "**Version:** v0.1r1 DRAFT for the reviewer's RECHECK, 31 October 2026, answering EX_087 (E1R2-R3-B01, C01, C02 and O01; section 11 maps each change). v0.1 (LF `6cff9f90...e6e8`) was reviewed in EX_087. Author: Claude. Ratifier: the project owner.")
r("- **Base:** `main` at `ef51305` (EX_085).", "- **Base:** `main` at `cf5b065` (EX_087).")

# C01: static check and T15
r("""- **The static check** (E2R-R56), a new test:
  - no `.py` file under `src/` or `tests/` imports anything whose module path starts with `archive`;
  - no runner adds `archive` to `sys.path`;
  - `archive/` is in none of the suite's paths.
  The test reads archive files as bytes only.""",
"""- **The archive is never executed, by production code or by tests** (E2R-R56; EX_087 C01). There is no test-only exception: every test that touches `archive/` reads its files as bytes. Two new checks:
  - **static:** no `.py` file under `src/` or `tests/` has an import whose module path starts with `archive`, and none calls `importlib`, `runpy`, `exec`, `compile`, `spec_from_file_location`, `SourceFileLoader` or `sys.path` changes on a path containing an `archive` folder name. Only the files that compare archived bytes may name `archive/` at all, and they are listed in the test;
  - **runtime:** in a subprocess, the test imports every module under `src/` (as the suite's paths allow) and then the full E_1 contract path for both games on invented data; afterwards, no entry in `sys.modules` has a `__file__` under `archive/`, and `archive` is on no `sys.path` entry.
  - **The r1 output reference does not come from the archive** (see E1R2-T01).""")
r("""- **E2R-T15 on a synthetic tree:** a temporary source tree with an invented method E_998 r1, retired by the same builder step to r2, in a copy **without** a `.git` folder. Archived bytes equal the originals, README references resolve, and imports cannot reach the archive.""",
"""- **E2R-T15 on a synthetic tree** (both kinds of path; EX_087 C01): a temporary source tree with an invented method E_998 r1 of three files, retired by the same builder step to r2, run twice, in a copy **with** and one **without** a `.git` folder. r2 **drops** one file (its old path must be absent afterwards), **reuses** one path with new bytes (the archive holds r1's bytes, the live path holds r2's), and **reuses** one path unchanged (the archive holds r1's bytes, the live path is identical). In every case the archive holds r1 complete, README references resolve, and imports and dispatch cannot reach the archive.""")

# O01
r("- **Retired:** the date of installation, written by the builder as the package's build date; superseded by revision 2.",
  "- **Prepared and retired** (EX_087 O01): the README states the package's preparation date, labelled as such, and says that the retirement takes effect when the owner installs the package. The installation date and commit are recorded in the ratification register, not in the README (D-5: no commit ID, no hash). Superseded by revision 2.")

# B01: section 5
old5_start = s.index("## 5. Install and release together")
old5_end = s.index("## 6. Tests (synthetic only)")
new5 = """## 5. Install and release together, behind a fail-closed barrier (decision ER-2, revised as ER-2r1: an exception to E2R-R58's recommended two packages)

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
| 4 | delete the flag (`del src\\methods\\E_001\\IN_DEVELOPMENT.txt`) | `post`: as `release`, without the flag; then the tests run |

Then the usual stage, commit (`committed` phase: the commit holds exactly the archive, code, declarations, entries and tests, and no flag), and push.

**What each interim state does** (proved by E1R2-T09 on synthetic copies, not by running anything during the install):
- **after step 1 or 2:** r1 and r2 requests both refuse with `IN_DEVELOPMENT_FLAG_PRESENT`, through the contract and through the legacy runner. In the walk-forward driver, planning a new batch for either game refuses (`cohort()` treats a `SUPPORTED` method with a flag as an inconsistent installed state), and starting a planned batch whose cohort includes E_1 refuses at its start-of-run check. A batch planned earlier without E_1 is not blocked by the flag, so the install instructions say that no batch is run or resumed between step 0 and the push;
- **after step 3:** the same refusals (the flag is still there); r1 is already stale;
- **after step 4:** only r2 admits; an r1-pinned request refuses as `STALE_REGISTRY_ENTRY`; the data, orphan and owner gates are unchanged.

**On any STOP before step 4,** the owner stops, leaves the flag where it is and sends Claude the output. Recovery is the owner's decision; nothing removes the flag automatically, and no step bypasses it. While the flag exists, E_1 cannot run by either path.

**Why one package with a barrier is acceptable here:** revision 2's computation is proven identical to revision 1's (section 6, E1R2-T01, T02 and T02B). The only behavioural difference is the data kinds it admits. Admitting real data is the owner's decision WF1-13, and is reviewed in this round. The barrier gives every intermediate state the property R58 asks for: no code runs under an approval that was not given for it.

**The alternative:** R58's two packages, with a committed interim in which E_1 cannot run and the 68 tests are edited twice.

"""
s = s[:old5_start] + new5 + s[old5_end:]
E.append('section 5')

# C01/C02 tests
r("""| E1R2-T01 | **Identity:** for both games and several targets on invented masters, E_1 r2's contract forecast equals r1's label for label (scores, ranked groups, ranking, TOP, WORST); only `method_revision`, `declaration_digest` and the content digest differ. r1's output comes from the archived function, loaded by path in the test only, never imported normally. |""",
"""| E1R2-T01 | **Identity with r1, both games** (EX_087 C01): for both games and several targets on invented masters, in the synthetic namespace, E_1 r2's contract forecast equals r1's label for label (scores, ranked groups, ranking, TOP, WORST); only `method_revision`, `declaration_digest` and the content digest differ. **r1's side is a frozen reference file,** `tests/fixtures/e1_r1_reference_v1.json`: the package's build tool computes it once from the **base commit's** r1 code, in a temporary copy outside the repository, and the package carries it as an ordinary new test file (listed in the manifest). The test never reads or runs anything under `archive/`. |""")
r("""| E1R2-T02 | **Real namespace:** on an invented master in a temporary project, through the driver, E_1 r2's `REAL_DEVELOPMENT` forecast equals E_1's legacy function (`build_e1_forecast`) on the same rows with the real-namespace digest (scores, ranking, TOP, WORST). The contract's real-namespace digest already equals the reader's legacy digest (an existing contract test). |""",
"""| E1R2-T02 | **Real namespace, Powerball** (scoped by EX_087 C02): on an invented Powerball master in a temporary project, through the driver, E_1 r2's `REAL_DEVELOPMENT` forecast equals E_1's legacy function (`build_e1_forecast`, Powerball's MAIN and POWERBALL scorer) on the same rows with the real-namespace digest (scores, ranking, TOP, WORST). The contract's real-namespace digest already equals the reader's legacy digest (an existing contract test). |
| E1R2-T02B | **Real namespace, Oz Lotto, an independent oracle** (EX_087 C02): on an invented Oz Lotto master in a temporary project, through the driver, E_1 r2's `REAL_DEVELOPMENT` forecast is checked label by label against a test-local oracle written from the specification, not from E_1's code: the MAIN appearance count of each number over exactly the draws before the target in the permitted view; the full ranking with ties ordered by `TIE_SHA256_V1` recomputed in the test from its definition; TOP and WORST; the target, its N-1 boundary, and the permitted-view digest, recomputed from the invented rows by the reader's documented digest rule. The master is invented in the test; no real master is opened or imported. |""")
r("""| E1R2-T03 | **Data kinds:** the multi-game function admits `SYNTHETIC_CONTRACT_TEST` and `REAL_DEVELOPMENT`, and refuses `REAL_HOLDOUT`, `FINAL_NEXT_DRAW`, `IN_SAMPLE_DIAGNOSTIC`, `REAL_HISTORICAL_DEVELOPMENT` and anything else. A holdout target is still refused. |""",
"""| E1R2-T03 | **Data kinds and boundary, both games:** the multi-game function admits `SYNTHETIC_CONTRACT_TEST` and `REAL_DEVELOPMENT`, and refuses `REAL_HOLDOUT`, `FINAL_NEXT_DRAW`, `IN_SAMPLE_DIAGNOSTIC`, `REAL_HISTORICAL_DEVELOPMENT` and anything else. For each game, a target past the permitted development boundary (a holdout target) is refused. |""")
r("""| E1R2-T07 | **Archive (E2R-R55 and R56):** archived bytes equal the base commit's (verifier, every phase); exact file list; README fields; helper references resolve; the static no-import check; nothing on the suite's paths reaches `archive/`. |
| E1R2-T08 | **E2R-T15** on the synthetic E_998 tree, with and without `.git`. |""",
"""| E1R2-T07 | **Archive (E2R-R55 and R56):** archived bytes equal the base commit's (verifier, every phase after `pre`); exact file list; README fields (including the preparation-date wording of 4.3); helper references resolve; the static and runtime no-execution checks of 4.1. |
| E1R2-T08 | **E2R-T15** on the synthetic E_998 tree: a dropped path, a reused path with new bytes and a reused unchanged path, with and without `.git` (4.1). |
| E1R2-T09 | **The install barrier** (EX_087 B01): on synthetic copies of the installed contract data and method folder, each interim state of section 5 is built in turn (after steps 1, 2, 3 and 4). For each, r1- and r2-pinned contract requests and the legacy gate give exactly the results in section 5's list, planning a batch refuses, and starting a plan that includes E_1 refuses, until step 4. The verifier's six phases are also run against those states and each accepts only its own. |""")
r("""- r2's declaration differing in a field other than the revision;
- the archive missing one file.""",
"""- r2's declaration differing in a field other than the revision;
- the archive missing one file;
- the barrier flag left out of `barrier_overlay/`, or removed before step 3 (the `code` or `release` phase accepts a tree without it);
- the verifier's `code` phase accepting an E_1 `entry_0002.json`;
- a test loading an archived file with `importlib` (the static check);
- E_1's Oz Lotto tie order changed (T02B's oracle);
- the r1 reference file edited by one score (T01).""")

# ER-2 decision and section 7 Q6 note
r("""- **ER-2 (OWNER-CHOSEN 31 October 2026, before review; was RECOMMENDED): E_1 r2 installed and released in the same package,** as two named actions (section 5), an exception to E2R-R58's recommended two-step release, for E_1 only. The option: R58's two packages, with E_1 unrunnable in between.""",
"""- **ER-2 (OWNER-CHOSEN 31 October 2026, before review): E_1 r2 installed and released in the same package,** as two named actions, an exception to E2R-R58's recommended two-step release, for E_1 only. EX_087 B01 found that its interim was not fail-closed.
- **ER-2r1 (OWNER-CHOSEN 31 October 2026, after EX_087 and before the RECHECK; replaces ER-2's procedure): one package, installed in five steps behind a temporary barrier** (E_1's own flag, created first and removed last, never committed; section 5). The option: R58's two packages, with a committed interim in which E_1 cannot run.""")
r("The owner chose ER-1 to ER-4 as recommended on 31 October 2026, before the review, and declined ER-6 on the same day. The reviewer may still raise a finding on any of them; a change would go back to the owner.",
  "The owner chose ER-1 to ER-4 as recommended on 31 October 2026, before the review, and declined ER-6 on the same day. EX_087 accepted ER-1, ER-3 and ER-4 in principle, and required a fail-closed procedure for ER-2 (B01). ER-2r1 is that procedure; the owner chose it on 31 October 2026, before the RECHECK.")
r("""1. **The full-cohort batch (the owner declined ER-6, 31 October 2026).** Since WF-1A v2 (EX_083 B01), a batch never reuses another batch's runs. After installation,""",
"""1. **The full-cohort batch (the owner declined ER-6, 31 October 2026).** Since WF-1A v2 (EX_083 B01), a batch never reuses another batch's runs. No batch is run or resumed during the install (an instruction, section 5); while the barrier flag exists, planning a new batch refuses, and so does starting one whose cohort includes E_1. After installation,""")

# Section 10 and new 11
r("## 10. What the reviewer is asked to check (R-3)\n",
  "## 10. What the reviewer was asked to check (R-3, v0.1; answered in EX_087)\n")
s = s.rstrip('\n') + """

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
"""
open(out, 'w', encoding='ascii', newline='\n').write(s)
print(len(E), 'edits;', hashlib.sha256(s.encode()).hexdigest())
