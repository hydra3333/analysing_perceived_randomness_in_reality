# NAMES-1 v0.1 — Independent ChatGPT R-3 HIGH-tier design review

**Date:** 28 October 2026 (Adelaide). **Author:** Claude. **Reviewer:** ChatGPT. **Package:** `NAMES1_Spec_Review_v0_1.zip`. **Base:** `38fc60e03ea0766f72476cbab7c0e1eb5bd59d07`. **Design only**; no owner authorisation to execute source migration, code, or safety-sensitive tests.

## Verdict

**TARGETED REVISIONS REQUIRED BEFORE OWNER RATIFICATION:** **0 BLOCKER / 4 CORRECTION / 1 OPTIONAL / 1 RECONSIDER.** The one-off rename objective and the 27-file map are a reasonable, bounded strategy. This is the **sixth distinct review** under the extended oversight arrangement. The forthcoming implementation necessarily touches always-review reader and coordinator imports: its actual code package is **HIGH tier and must receive an independent RECHECK**, regardless of any trivial-change provision.

## Verified package and limits of evidence

- ZIP SHA-256 **PASS:** `6aab40a1407c4b438ce05b7132ee2d3e183a6feb711d6f5877d9becc3246325f`.
- Specification SHA-256 **PASS:** `88379b2800f0b660242ece361178eff7c0a2ebc70c68a83916cb187d1fa9dce5`.
- Evidence includes the 27-file rename map, 94 whole-word substitution sites in 27 Python files, original/trial logs reporting **79 tests passed in each tree** (60 + 19), and an import/reference inventory. These are **Claude's supplied, author-side trials**, not independently executed project tests by ChatGPT.
- Independently inspected the evidence scripts and substitution-site inventory and compared critical reader-firewall text against the public GitHub source at the submitted base. The proposed transforms are not blanket evidence that all runtime semantics are invariant merely because the edited text mechanically matches the map; particular module paths, string-valued file names, and import-origin checks must receive special attention.
- The accepted E_1 synthetic/golden evidence and frozen v0.6 protected-function AST are appropriate acceptance anchors. Windows execution and protected coordinator lifecycle behaviour were **not** independently tested in this design review.

## Findings

### N1-C01 — CORRECTION — RECHECK — Precisely bound the semantic exceptions to a 'pure rename'

**Locations:** N1-R01 (nothing else changes), N1-T02/T03, §6 and `evidence/substitution_sites.txt`, notably `tests/test_multigame_v011_static_and_timing.py` lines 99 and 102, `src/coordinator_private/multigame_coordinator_exit_receipt_v2.py` line 31, `src/Powerball_Experiment_Coordinator.py` line 1105.

**Failure scenario:** The global replacement changes not only Python imports but literals used as filesystem verification, module-origin identity, and *negative safety assertions*. In particular, the old assertions forbid `_common.game_draws_reader_v1`; changing them to forbid `game_draws_reader` is syntactically a stronger substring test. The *scientific/safety intention* may be correct—prohibit the currently named shared reader from unauthorised method imports—but it is not literally unchanged test logic. Conversely, mechanically preserving the old literal would permit imports from the renamed current reader, defeating the intended boundary. The blanket claim of unaltered test logic cannot stand without this precise semantic distinction.

**Required replacement:** Define a two-column allowlist of filename-coupled references that **must change to preserve their existing intended invariant**, distinguishing (a) imports and correct module/file origins, (b) active-file identity/string comparisons, and (c) *negative firewall assertions*. Prohibit any unrelated replacements. Add explicit mutation/negative cases proving that a new-name reader import is rejected and that removed old-name modules are not importable (fresh interpreter, clean paths). N1-T02 must compare exactly to the narrowly reviewed transformation and report every authorised literal change. Preserve all scientific golden/identity constants. This is not a request to restore versioned filenames.

### N1-C02 — CORRECTION — RECHECK — Windows acceptance must not silently omit 19 relevant tests

**Locations:** N1-T09 versus §6 and README evidence.

**Failure scenario:** The author trial runs **79** tests (60 standard + 19 from `test_e1_standalone` and `test_multigame_windows_lifecycle_review`), but N1-T09 requires the owner's Windows run to achieve only **60**. That leaves the standalone E_1 and lifecycle-review suites unaccounted for on the platform whose import and process-related paths are at risk. A Linux pass does not establish their Windows status.

**Required replacement:** Require the **full applicable renamed 79-test inventory on Windows**, split into the existing 60-test command and the separately named 19-test modules if appropriate. Report each module's test and skip counts and actual environment. Two previously observed symlink skips are *expected possibilities*, not guaranteed test counts; new unexplained skips or failures need examination. No destructive or process-kill tests are authorised merely by adding coverage.

### N1-C03 — CORRECTION — RECHECK — Complete stale-reference and import-origin verification

**Locations:** N1-T01 and N1-T05/T06; `evidence/inventory.py`.

**Failure scenario:** N1-T01's proposed `*.py` scan is necessary but not sufficient for non-Python launch references or dynamically composed imports. The inventory records `.bat` references but the acceptance rule does not explicitly assert that relevant wrappers/configuration/launch templates contain no stale references. N1-T05 may pass in a process that has already imported the old name (from `sys.modules`) or still has stale paths on `sys.path`.

**Required replacement:** At package-install verification, check all live launch scripts and relevant package/configuration paths in addition to the source/test AST scan, with an exact expected-reference allowlist. Run a *fresh interpreter* for new-name import-origin assertions and old-name import refusals; demonstrate original old file paths are absent in installed `src/`. Historical `review/` and frozen fixtures remain deliberately exempt and unmodified. Ensure the coordinator's exit-receipt file-origin check matches the new filename without relaxing issuer restrictions.

### N1-C04 — CORRECTION — RECHECK — Narrow the git-dependent rollback promise

**Location:** N1-T10: “A single owner `git revert` of the NAMES-1 commit restores every old path.”

**Failure scenario:** This is valid only while the introducing commit remains reachable and the working tree/revert has no conflicts. The owner has expressly reserved the right to rewrite repository history later. A timeless rollback guarantee that depends on surviving commit history conflicts with that policy.

**Required replacement:** State explicitly that N1-T10 is an **immediate installation-recovery check while the recorded commit still exists**, carried out only in an isolated/disposable clone. This is not a guarantee of historical replay or rollback after Git-history cleanup. Do not add per-file historical hashes, archive commit IDs or runtime attestations merely for rollback.

### N1-O01 — OPTIONAL — Simplify names without destabilising legacy-owner tools

**Location:** §4 OPEN-N2. Retaining the current owner-run data utility names and legacy tests outside NAMES-1 is prudent. The later separate tidy-up is an *option*, not a commitment to change data acquisition. Avoid calling existing owner tools 'superseded' until the owner explicitly decides their disposition and verifies no wrapper still depends on them. Do not run, import, rename or retire these tools under NAMES-1.

### N1-REC01 — RECONSIDER (owner decision requested, nonblocking as a finding) — Per-method folder model

**Location:** §4 N1-R05 / OPEN-N1, read against owner-approved E2R D-4 and the unchanged Option F wrapper.

**Issue:** D-4 says “folder per method”, whereas the proposed refinement deliberately keeps entry files flat under `src/methods/` and creates only method-specific module/flag subfolders from E_2 onwards. For E_1, even that subfolder is postponed. The rationale is technically credible and avoids a broader, riskier wrapper/reader migration, but this is a genuine clarification/refinement of a ratified design—not an implementation detail the author can unilaterally reinterpret.

**Recommendation:** Owner explicitly choose either **A** (accept N1-R05's flat executable entry files plus method folders for future-specific modules/flags, postponing E_1 restructuring) or **B** (keep D-4's literal folder-per-method layout and authorise a separately reviewed wrapper/reader rework first). I recommend **A** for the *bounded NAMES-1 package*. Record the decision in the next register edition. NAMES-1 must not claim to have implemented per-method folders if no folders were created. Nothing here waives the `SUPPORTED AND no IN_DEVELOPMENT.txt` admission rule when implemented in the separately approved E2R code.

## Outstanding owner choices

- **OPEN-N1:** explicitly resolve the D-4 layout refinement in N1-REC01 before ratifying this design.
- **OPEN-N2:** keep owner data tools and legacy tests out of scope; any later tidy-up requires separate owner scope and independent protection as applicable.
- **OPEN-N3:** stable test filenames in §3 are acceptable as design choices, provided all 79 applicable tests and their call sites are updated and proven.

## REVIEWER-DECIDED — sixth review, list all

- **N1-RD-01:** Support the bounded 27-file rename plan and keep its implementation HIGH tier with mandatory independent RECHECK of always-review code.
- **N1-RD-02:** Require N1-C01/C03 exact semantic-reference and fresh-process import/firewall proofs; no silent code/test-logic scope expansion.
- **N1-RD-03:** Require N1-C02 full applicable Windows coverage (60 + 19) with explicit skips; no Windows test claim is inferred from the author's Linux trial.
- **N1-RD-04:** Require N1-C04 Git-history-conditional rollback wording, preserving owner's freedom to rewrite history.
- **N1-RD-05:** Raise N1-REC01 for owner resolution; recommend Option A but do not unilaterally narrow ratified D-4.
- **N1-RD-06:** Keep N1-O01 optional; authorisation for data acquisition, protected coordinator process action, scientific runs and retired module replay remains closed.

**No scientific code, tests, migration, process termination or holdout data were executed or read for this review.** No NAMES-1 implementation is authorised. Claude should return a targeted corrected specification with exact diff and hash, and collect the owner's OPEN-N1..N3 decisions. The subsequent *implementation* is a separate, owner-authorised HIGH-tier package requiring its own independent RECHECK.
