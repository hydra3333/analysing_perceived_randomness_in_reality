# Claude full review of the consolidated governing documents v0.2, v1

**Reviewer:** Claude (independent reviewer)
**Date:** 25 October 2026 (Adelaide)
**Reviewed:** `Predictive_Randomness_Governing_Documents_CONSOLIDATED_v0_2_CLAUDE_FULL_REVIEW.zip`, SHA-256 `931e8ff474b6a8855a3760fae909b640a7088d4bd5b7e9f33640231e9d8dad6c`
**Checked against:** the ratified sources at GitHub HEAD `ce462be`, which are unchanged since `cf00999`; the owner decisions; my v0.1 review.
**Method:** independent. I ran:
- an ID inventory: every A-, D-, I-, R2-C, R2-D, T-, W-, O-, M-INV- and ERR- identifier in each ratified source, searched for in all eight candidates;
- my own stale-phrase scan;
- a check that each protected-block source file is a byte substring of the ratified original;
- a full read of the new Proposal, R2 (non-inventory parts), Architecture and P3, and the R3 v0.1 to v0.2 changes;
- spot checks of the matrix rows.

**Status:** review only; nothing here authorises any run. No winning, Powerball or supplementary numbers appear in this document.

---

## 1. Verdict

**NOT READY TO RATIFY. Three BLOCKERS, all of the same kind.**

v0.1 changed too little. v0.2 changes too much. The Proposal shrank from 143 KB to 23 KB, the Architecture from 147 KB to 24 KB, and R2 (excluding the method inventory) from about 99 KB to 26 KB. In the process, ratified substance was dropped: not just history, but owner decisions, invariants, contracts and test catalogues.

The matrix marks these items `CURRENT_RESTATED`, but at broad locations ("R2 sections 3-9 (by subject)") with a boilerplate reason. In several cases checked, the substance is not at the cited location. Some ratified catalogues are not in the matrix at all.

**Fixed correctly since v0.1, verified:**
- the stale contradictory text is gone (my scan finds no operative stale hits);
- B3: the benchmarks are B1 1576 and B10 1567-1576;
- the E_1 synthetic and real goldens and the frozen TOP/WORST outputs are now normative in R2 section 5;
- `--game`, process label never ownership evidence, the method-generic contract before E_2, namespaces, value-free auditing, the post-upgrade stop, environment archiving and the R2 OPEN / no-authorisation lists are restored;
- the T-01..T-39 test table is retained and current;
- the ERR-R2 index is in R2 section 0;
- the register lists the out-of-scope documents;
- exposure item 5 is added.

**Protected blocks:** all seven source blocks are byte substrings of the ratified files, and each is present byte-for-byte in its candidate:
- Architecture 5C (all of it);
- the Proposal E_1-E_6 text;
- the R2 method inventory and section 4.1;
- the R3 readout, seed and tie sections.

**R3 v0.4 is in good shape.** P3 is good apart from C3 below.

---

## 2. BLOCKERS

### B1. Proposal: ratified charter substance removed

**Identifiers lost.** None of the 37 owner-decision rows **A-01 to A-37**, or the review dispositions **D1-D5**, appear in any candidate. They are the ratified record of what the owner agreed. Examples whose substance is now missing or thinned:
- **A-07:** a configurable retrospective evaluation count ("last 10" concept). The matrix maps it to "Proposal 8; R2 6", but neither contains it.
- **A-11:** room for up to 100 further candidate methods (to E_106), with no quota.
- **A-15:** combination experiments receive new permanent identifiers, and their criteria evolve only with owner review.
- **A-23:** no earlier-configuration draws even for Powerball-only variants. The new text only says "do not mix eras".
- **A-25:** poor scores or correlation never deprioritise a method as a matter of principle.
- **A-28:** the independent-uniform model calibrates interpretation but is never a gatekeeper.
- **A-32:** the E_57-E_62 origin does not imply quantum physics is acting on lottery equipment.

**Philosophy and principles thinned to a paragraph.** The project's philosophy is binding on the project, and the new section 1 reduces it to a paragraph. The following were dropped:
- the central-premise statement;
- the "Perceived Reality" title;
- old section 2: the assumption-challenging investigation; the precise meaning of "no assumptions"; the independent-draw model as benchmark, not veto; the Monty Hall reminder and its limit; the policy for strange or poor results; and what counts as a claim about reality;
- old section 9: permanent retention details, combination identities, hindsight protection, and correlation never deciding eligibility;
- old section 10.5-10.6: negative or anomalous findings, and synthetic research permitted to inform disclosed design;
- old section 11: data-integrity and leakage principles.

**Required fix.** Keep the ratified charter text, editing only what is stale:
- the central premise, title and philosophy (old section 2) substantially verbatim;
- the A-table with its IDs, each row either current (reworded where superseded, for example A-08 becomes the fixed August holdout and A-34/A-36 become 1-6 workers) or marked "withdrawn: see X";
- old sections 9-11 principles;
- old section 12 design narrative and the risk register can move to Appendix S or be dropped with a one-line pointer.

### B2. Architecture: the ratified test catalogues, wrapper rules and OPEN register were removed and are not mapped

1. **The W-01 to W-25 Windows test suite** is gone and absent from the matrix. Its exact pass criteria cover:
   - argument fidelity;
   - pipe deadlock;
   - exit codes;
   - venv states;
   - `Popen.pid` versus `os.getpid()`;
   - memory self-report;
   - the destructive-gate-only tests (hang timeout, six-worker Ctrl+C, 2 GB ramp, psutil tree);
   - the AutoRun and quoted-path tests;
   - the installer tests;
   - `.bat` CRLF after Git checkout;
   - **W-23** (re-run the W-suite after recreating the venv or upgrading Python/psutil; this is the dependency-upgrade gate on the always-review list);
   - six-way canonical identity.

   Handbacks and test files cite these IDs. The R2 section 8 "mandatory gates" sentence is a summary, not a replacement.
2. **The A-01 to A-26 architecture acceptance tests** (for example A-24, real and synthetic queued together) are gone.
3. **Wrapper rules settled by the owner are gone:**
   - `SETLOCAL`/`ENDLOCAL` restoration;
   - forwarding with `%*`;
   - never rebuilding arguments from `%1..%9` (CMD splits at `= , ;`);
   - the restricted argument character set (`SAFE_ARG`);
   - the AutoRun check by registry instead of `cmd /D /C`;
   - the old 5A.1 and 5A.3 wrapper acceptance criteria;
   - the 5B monitoring contract (child self-reported metrics, compatibility as an observable contract).
4. **The O-register (34 OPEN items, O-ARCH-01 .. O-WRAP-03)** is gone, apart from a one-line OPEN list. Each needs a disposition: resolved (cite the decision), still OPEN, or withdrawn.

   Note: protected 5C still refers to "5B.2/14.2", which no longer exist. Add a note outside the protected block saying those references point to the predecessor.

**Required fix.** Restore the W- and A-test tables and the wrapper rules, with their IDs, updated where needed: Option F stays provisional, the installer defaults to install-and-upgrade, and W-23 also covers package upgrades. Give every O-item a disposition.

### B3. R2: the ratified invariant and contract identifiers were removed

**I-01 to I-17, R2-C01 to C20 (plus C07A and C11A) and R2-D01 to D28** no longer appear. These items lost their substance as well as their label:
- **R2-C07A:** labelled `HISTORICAL_EVALUATION` and `FINAL_NEXT_DRAW` workflows, with `training_last_draw` derived from draw numbers.
- **R2-C11A:** TOP and WORST shown side by side in the same E-method row, frozen together.
- **R2-C15:** switching view creates a versioned variant, not a new E-number, without owner approval.
- **Old section 5:** the supported output types and `ForecastResult` fields.
- **Old section 6:** the method lifecycle and registry fields.
- **Old section 9.4 / R2-C20:** failure semantics and the benchmark status vocabulary (`SUCCESS`, `TIMEOUT`, `ERROR`, `INSUFFICIENT_HISTORY`, `BLOCKED_DEPENDENCY`, `NUMERIC_INVALID`).
- **Old section 10.3-10.4:** the benchmark report schema and environment fingerprint.
- **Old section 13.2:** the three owner-agreed reporting components, which must be frozen before the first FINAL. T-39 covers only the block.

Items labelled [PROPOSED] inside ratified R2 should remain as RECOMMENDED with their IDs, not disappear. Whether to promote or withdraw them is the owner's decision, not the consolidation's.

**Required fix.** Keep every I-, R2-C and R2-D ID as an anchor with current text, or as "withdrawn: replaced by X". The T-table shows the right pattern.

---

## 3. CORRECTIONS

| ID | Finding | Change |
|---|---|---|
| C1 | **Path typo in three documents** (Proposal section 2, R2 section 2, Architecture section 1): `source_data/_results_master_ledger.csv` and `source_data/_results_master_init_verification.json`. The `<GAME>` placeholder was lost. | Use `source_data/<GAME>_results_master_ledger.csv` and `<GAME>_results_master_init_verification.json`. |
| C2 | **Exposure record.** Item 4 says "apart from item 1, no values were displayed", but item 5 now records a second display. | Change to "apart from items 1 and 5". |
| C3 | **P3 dropped the M-INV-01..07 invariants.** These are the ratified P3 invariant set, and M-INV-03 still carries the old holdout. I missed this in my v0.1 review. | Restore them as current invariants: M-INV-03 updated to the August boundary, M-INV-01 to the master-based goldens. |
| C4 | **Matrix quality.** Locations are ranges ("R2 sections 3-9 (by subject), Architecture section 9") with a boilerplate reason. The W-, O- and M-INV items and the old Proposal sections 2/9-11 have no rows. | For each row: one exact section, and a one-line statement of where the substance now sits or why it was withdrawn. |
| C5 | **Proposal structure.** Section 6 is missing (the numbering jumps 5 to 7). The title lost "Perceived Reality". | Fix both as part of B1. |
| C6 | **R3 line 680** still uses target draw 1588 in the example JSON. This was optional item O1 in the v0.1 review and was reported as covered. | Use a development target (for example 1576) or a clearly fictitious one. |

---

## 4. OPTIONAL

- **O1:** add to the stale scan the IDs that must survive (the A-, I-, R2-C, R2-D, W- and M-INV- lists), as a "must be present" check. That would have caught B1-B3 mechanically.

---

## 5. Recommended method for v0.3: edit in place, do not rewrite

1. **Start from each ratified file.**
2. **Change only what is stale.** Make each change a minimal edit, keep every ID, and preserve the surrounding text.
3. **Remove only pure history** (chronology and superseded proposals), each with a one-line Appendix S entry.
4. **Keep the new current-rule sections from v0.2.** They are good. Their wording does not need to be reworked; they need to be placed into the preserved structure.
5. **Expected result:** documents close to the ratified size, with diffs that read as a list of targeted changes. That makes the full review tractable and the mapping verifiable.

Claude will repeat the same independent checks on v0.3, including the "must be present" ID inventory.

*End of document.*
