"""Design v0.1r1 -> v0.1r2 (answers EX_089: C03, O02, and its implementation notes). Counted in-place edits."""
import hashlib, sys
src, out = sys.argv[1:3]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == '933b0a0751a7f88538d03330cc203d9d8e592ff6816f27abdce231996e942b8b'
s = raw.decode('ascii')
n = 0
def r(a, b):
    global s, n
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b); n += 1

r("design note v0.1r1\n", "design note v0.1r2\n")
r("**Version:** v0.1r1 DRAFT for the reviewer's RECHECK, 31 October 2026, answering EX_087 (E1R2-R3-B01, C01, C02 and O01; section 11 maps each change). v0.1 (LF `6cff9f90...e6e8`) was reviewed in EX_087.",
  "**Version:** v0.1r2 DRAFT for the reviewer's focused RECHECK, 31 October 2026, answering EX_089 (E1R2-R3-C03 and O02; section 12). v0.1r1 (LF `933b0a07...942b8b`) answered EX_087 (section 11) and was rechecked in EX_089. v0.1 (LF `6cff9f90...e6e8`) was reviewed in EX_087.")
r("- **Base:** `main` at `cf5b065` (EX_087).", "- **Base:** `main` at `ae190c7` (EX_089).")

r("""**What each interim state does** (proved by E1R2-T09 on synthetic copies, not by running anything during the install):
- **after step 1 or 2:** r1 and r2 requests both refuse with `IN_DEVELOPMENT_FLAG_PRESENT`, through the contract and through the legacy runner. In the walk-forward driver, planning a new batch for either game refuses (`cohort()` treats a `SUPPORTED` method with a flag as an inconsistent installed state), and starting a planned batch whose cohort includes E_1 refuses at its start-of-run check. A batch planned earlier without E_1 is not blocked by the flag, so the install instructions say that no batch is run or resumed between step 0 and the push;
- **after step 3:** the same refusals (the flag is still there); r1 is already stale;
- **after step 4:** only r2 admits; an r1-pinned request refuses as `STALE_REGISTRY_ENTRY`; the data, orphan and owner gates are unchanged.""",
"""**What each state does** (proved by E1R2-T09 on synthetic copies, not by running anything during the install). The gate's check order is unchanged (EX_089 C03): `_admit` checks, in turn, the active entry's status, the pinned entry digest, the revision, the declaration digest, and only then the flag. So **the property** is that nothing admits after steps 1, 2 or 3, and **the reason** depends on the request and the step:
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

**The walk-forward driver** in the same states: planning a new batch for either game refuses after steps 1, 2 and 3 (`cohort()` treats a `SUPPORTED` method with a flag as an inconsistent installed state), and so does starting a planned batch whose cohort includes E_1. A batch planned earlier without E_1 is not blocked by the flag, so the install instructions say that no batch is run or resumed between step 0 and the push. The flag is the gates' application-level safeguard, not an operating-system lock.""")

r("""**On any STOP before step 4,** the owner stops, leaves the flag where it is and sends Claude the output. Recovery is the owner's decision; nothing removes the flag automatically, and no step bypasses it. While the flag exists, E_1 cannot run by either path.""",
"""**On any STOP before step 4,** the owner stops, leaves the flag where it is and sends Claude the output. Recovery is the owner's decision; nothing removes the flag automatically, and no step bypasses it. While the flag exists, E_1 cannot run by either path.

**On any STOP after step 4** (EX_089 O02: the `post` check, the tests, the commit or the `committed` check fails, or the install is interrupted), r2's code and entries are present without the flag, but the install is not complete. Then:
- the owner does not push, runs no E_1 run and no batch of either game, and sends Claude the whole output;
- nothing is undone automatically: no reset, rollback, deletion or process termination;
- if the owner decides to close the gate again while the failure is examined, the owner copies `barrier_overlay/` again and runs the verifier's `release` phase, which accepts exactly that state (r2 installed, the flag present). Removing the flag again is step 4, after the owner's decision.""")

r("""| E1R2-T09 | **The install barrier** (EX_087 B01): on synthetic copies of the installed contract data and method folder, each interim state of section 5 is built in turn (after steps 1, 2, 3 and 4). For each, r1- and r2-pinned contract requests and the legacy gate give exactly the results in section 5's list, planning a batch refuses, and starting a plan that includes E_1 refuses, until step 4. The verifier's six phases are also run against those states and each accepts only its own. |""",
"""| E1R2-T09 | **The install barrier** (EX_087 B01; reasons corrected by EX_089 C03): on synthetic copies of the installed contract data and method folder, the states after steps 0 to 4 of section 5, and the re-barriered state of the STOP-after-step-4 recovery, are built in turn. For each state the test checks **two properties separately:** (1) whether each of the four requests in section 5's table admits, which must be never after steps 1, 2 and 3, and (2) its exact refusal code, cell by cell as in the table, keeping the pinned contract requests apart from the unpinned legacy gate. It also checks that planning a batch refuses, and starting a plan that includes E_1 refuses, until step 4. The verifier's six phases are run against the same states, and each accepts only its own (the re-barriered state passes `release` only). The gate's code and order are not changed. |""")

r("""- E_1's Oz Lotto tie order changed (T02B's oracle);""",
"""- E_1's Oz Lotto tie order changed (T02B's oracle);
- the gate's flag check moved before the pin check (T09's code matrix), and T09 expecting the flag code in a cell where the gate gives another;""")

r("""## 7. After installation, and how it fits the measurement and ranking scheme""",
"""**Implementation commitments (EX_089's notes):**
- **The r1 reference file's provenance** (T01): the package records how it was made (the base commit's r1 files, by path, the builder's command and the inputs), and its review evidence regenerates it from the base tree byte for byte.
- **T15 without Git** compares the archive with pre-install bytes saved by the test before the retirement step, not with a Git operation.
- **T02B's oracle** calls none of E_1's code or the contract's ranking, tie or digest helpers. It implements the count, `TIE_SHA256_V1` and the digest rule in the test, and its published labels are scores, not probabilities.
- **T07's runtime import** imports only a listed inventory of library modules, each checked to have no side effects on import. It never imports an entry-point script (a `Method_*.py`, `E_001_Historical_Appearance_Frequency.py`, the coordinator or a scraper), and it opens no data and no network.

## 7. After installation, and how it fits the measurement and ranking scheme""")

s = s.rstrip('\n') + """

## 12. Changes in v0.1r2 (answering EX_089), and what the focused RECHECK is asked to check

| Finding | Change | Where |
|---|---|---|
| E1R2-R3-C03 (CORRECTION) | Section 5's list is replaced by a table of the exact result for each of four requests (r1 and r2 contract requests, the legacy gate with revision "1" and "2") after each step, matching the gate's unchanged check order. T09 tests the never-admits property and the per-cell refusal codes separately. | 5; 6 (T09, mutations) |
| E1R2-R3-O02 (OPTIONAL) | Adopted: a STOP after step 4 means no push, no E_1 run and no batch, nothing undone automatically, and an owner-controlled way to close the gate again (copy `barrier_overlay/` again; the `release` phase accepts exactly that state). | 5; 6 (T09) |
| EX_089's implementation notes | Recorded as commitments: the reference file's provenance, T15's no-Git comparison, T02B's independence, T07's import inventory. | 6 |

**Please RECHECK:** section 5's table against the gate's order, and T09's two properties. The five-step mechanism (ER-2r1) is unchanged.

Nothing else changed from v0.1r1.
"""
open(out, 'w', encoding='ascii', newline='\n').write(s)
print(n, 'edits;', hashlib.sha256(s.encode()).hexdigest())
