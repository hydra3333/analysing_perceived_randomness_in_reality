# Claude full review of the consolidated governing documents v0.1, v1

**Reviewer:** Claude (independent reviewer)
**Date:** 25 October 2026 (Adelaide)
**Reviewed:** `Predictive_Randomness_Governing_Documents_CONSOLIDATED_v0_1_CLAUDE_FULL_REVIEW.zip`, SHA-256 `22910d92c6349137cead766267dde012e68b1e2c60015e5a9ce0dca5e30c06b1`
**Checked against:** ratified sources at GitHub HEAD `cf00999`:
- Proposal v0.4;
- R2 v0.3 and its erratum record v0.3;
- R3 v0.3;
- Architecture v0.6;
- P3 v0.1;
- register v0.2;
- the owner decisions of 25 October;
- `Claude_Review_Package2_v0_10_r1_and_Direction_v3.md`;
- the reviewed refresh v0.3 ratification packet.

**Method:** independent. I diffed every document against its own ratified predecessor and ran my own scans: stale wording, protected-block extraction, and requirement-by-requirement searches for every ratified Architecture 0A, R3 0A and erratum item. I did not rely on the supplied matrix or phrase scan.
**Status:** review only. Nothing here authorises any run. Line numbers refer to the candidate files in `review_overlay/doc/`.

No winning, Powerball or supplementary numbers appear in this document.

---

## 1. Verdict

**NOT READY TO RATIFY. Three BLOCKERS.**

The consolidation did not do what the owner chose it for. ChatGPT inserted the new current-rule paragraphs (the former 0B text) into each document and deleted the 0A layers. But the historical bodies of the Proposal, R2 and Architecture were largely kept as they were: 1,178 of the 1,240 Proposal v0.4 lines, about 95%, appear unchanged, and the proportions are similar elsewhere.

So these documents still contain operative-looking text that contradicts the current rules. Some ratified requirements from the deleted 0A layers and erratum record were also lost, and the mapping marks them "INTEGRATED" without a location. The package's own README says any current contradictory requirement is a BLOCKER.

**What is right, verified independently:**
- Architecture section 5C (all of 5C, 9,911 bytes), the R2 section 7 method inventory and mathematics, R2 4.1, and the R3 tie and readout sections 0.4, 2.4 and 3 are byte-identical to the ratified text.
- The new current-rule paragraphs are correct and consistent wherever they appear:
  - boundary, holdouts and the 1577 exception;
  - masters and ledger pinning;
  - assumed order, views and N-1;
  - `int64`/`float64`, dates, upgrades and fresh fitting.
- ERR-R2-02 stays PROVISIONAL.
- The safety summary in Architecture section 14 is complete: no-status/no-kill, the global orphan interlock across games, the failed-group firewall, the exit receipt and the three switches False.
- P3 v0.2 is a good clean rewrite (section 4).

---

## 2. BLOCKERS

### B1. Historical body text still reads as current and contradicts current rules

The examples below are not exhaustive. Every section needs a current-state pass (section 5).

**Proposal v0.5:**
- **Section 0 / 0.1 / 0.2 (lines 24-47).** "Chronology note for the preserved v0.3 body ... historical text retained for audit, not silently updated". "The documentation is deliberately layered, not merged". The table calls this file "Project Proposal v0.3" and R2/R3 "future, no ratified file". "Not performed: a predictor build ...". These are the opposite of a consolidated current charter.
- **Section 0.3 (line 53)** and **line 785:** "all 444 draws"; the two-file 444-row view.
- **Section 3.2 (line 188):** "growing, date-stamped ... `australian_powerball_history_20261021.csv` ..." described as the current record.
- **Line 286:** "The independent acquisition program is now `scrape_..._v0_3.py`".
- **A-08 (line 227):** "Reserve the latest 10 completed draws". The fixed holdout replaced the moving latest-ten rule.
- **A-33 (line 253):** order "supported by Draw 1297 and 1587 evidence". This needs restating as the owner-assumed published order (current rule), with that evidence as history.
- **A-36 (line 256), line 882 and line 903:** one-versus-12-worker bit-identity. This contradicts approved ERR-R2-01.
- **Line 900:** "With the currently reviewed 444-draw archive"; B1 target 1577; B10 targets 1568-1577 (see B3).
- **Line 913:** "installed requests and beautifulsoup4 ... saved requirements.txt".
- **Lines 835-844:** the repository layout lists the removed CSVs and the old scraper as current.
- **Lines 759-765:** scraping prose.
- **Question 17 (line 1163):** "two validated 444-row source views".

**R2 v0.4.** Each of these contradicts approved ERR-R2-01 or the masters:
- **T-13 (line 1031):** "One vs twelve workers".
- **T-37 (line 1055):** "Serial-versus-12-worker".
- **Section 10.2 step 7 (line 986):** "Optional 24-worker trial after the 12-worker ... baseline".
- **Section 12.4 (line 1149):** `--workers 12`.
- **Section 12.1 (from line 1078):** the existing-repository listing still shows the removed CSVs, the scraper and `requirements.txt`.
- **Section 12.3 (line 1137):** versions "recorded in `requirements.txt` or an explicitly named supplementary lock". This contradicts ERR-R2-03.
- **R2-D03 (line 1220):** "joining the two CSV views".
- **Section 14 S0/S1 (lines 1196-1198):** "Commit ratified Proposal v0.3"; "two-view consistency checks".
- **Section 16.1 (line 1260):** the old snapshots listed as observed sources.

**Architecture v0.7:**
- **Section 0.2 (lines 27-36):** the governing documents are listed as Proposal v0.3, R2 erratum v0.2 and Architecture v0.5.
- **Requirements 2-3 (lines 73-74):** Powerball-only (1144, 1-35, PB 1-20), with no Oz Lotto.
- **Requirement 11 (line 82):** "Ratified R2 v0.3 still additionally mandates 1-versus-12-worker evidence; that requirement remains binding until the owner approves an explicit controlled change". The owner approved that change (ERR-R2-01) on 22 October.
- **Requirement 12 (line 83) and O-POL-03 (line 968):** still open reconciliation items for the same, already-approved matter.
- **Line 380 and O-PKG-02 (lines 386, 973):** `requirements.txt` still treated as open.
- **Line 563:** "authorised logical observation view (`UNORDERED_SET`, `DRAWN_ORDER`, or an approved combination)". This uses the old naming and suggests entitlement.

### B2. Ratified requirements lost without a mapped withdrawal

The matrix marks every Architecture 0A subsection and every ERR-R2 item "INTEGRATED ... into current numbered sections", with no section given. I searched all eight candidates for each ratified item. These are missing from every candidate, or survive only in the non-normative numerical reference:

1. **E_1 frozen identities (Architecture 0A.5):**
   - the synthetic goldens `df21871f...` (training), `7ce5ab1b...` (label-3 tie) and `7b43d659...` (canonical);
   - the frozen real draw-1577 TOP/WORST outputs and Powerball outputs.

   The real goldens `d47fbbd6...`/`7f113087...` appear only in the non-normative numerical reference and in P3; no normative document states them. These must be stated in R2 (or Architecture) as normative regression identities.
2. **Architecture 0A.4:**
   - every run supplies `--game`, and commands and STARTED/terminal messages carry game, method, draw key and run ID;
   - the process label/display name is never ownership evidence, and `python.exe`/`cmd.exe` are not renamed for display;
   - before E_2, the E_1-specific runtime conventions are replaced by a method-generic contract (the `e1-` ID prefix, hard-coded E_1/variant/schema constants, Powerball-only filename validation, the 1577 caps).
3. **Architecture 0A.2 / R3 0A.3 / ERR-R2-05, value-free auditing:**
   - per-game separate source, results, synthetic and holdout namespaces;
   - any validator or auditor that reads quarantined rows emits only bounded pass/fail, counts and field names, never values;
   - quarantined values never reach development charts, fixture goldens, tuning, operator output or exception dumps.
4. **ERR-R2-01..03 acceptance gates (erratum section 3):**
   - launcher equivalence: manual and coordinated `Run_Experiment.bat` give identical canonical outputs;
   - the Windows gate list: CMD quoting, exit codes, Ctrl+C, psutil tree termination, no Python-redirector PID assumption;
   - "future extension": more workers, or experiment-created subprocesses, need an owner-approved change;
   - ERR-R2-03: archive the resolved Python/PyPI versions and the installer revision/digest with consequential benchmarks and every FINAL batch.
5. **Holdout integrity:**
   - R2 section 3.4 lost "do not silently shift the holdout" and "after tuning against it the holdout loses its independent designation";
   - R3 lost the same "no longer pristine" rule from its `FINAL_HOLDOUT_10` row and section 6.

   It survives only in Proposal section 5.5; restore it in R2 section 3.4 and R3 section 6.
6. **ERR-R2-05 "decisions intentionally left OPEN":**
   - E_54 external-feed contract;
   - per-method FORMULA_OPEN;
   - the first Oz Lotto real experiment;
   - the start of each game's FINAL track;
   - cross-game features;
   - the walk-forward windows awaiting pre-registration (now Powerball 1145-1576, Oz 1475-1693).

   Its "no authorisation" clause (no Oz method execution, no modifying a frozen Powerball result) is also missing. Several of these appear in P3 section 4, but R2 needs its own OPEN list.
7. **I-07 (R2 line 71)** dropped "any previous holdout use is disclosed; the same data cannot be claimed pristine for a method whose design saw its outcomes". T-17 and R2-D16 still carry "all 1144..L without exclusion", so that part survives.

### B3. Benchmark targets cross the boundary

R2 section 3.2 (lines 179-182) and Proposal line 900 keep B1 target **1577** and B10 targets **1568-1577**. Both documents also state "No other boundary crossing follows from this exception", and R2-C07 says the targets come "immediately before the frozen holdout".

**[REVIEWER-DECIDED]** Shift to:
- B1 target 1576, trained on 1144-1575 (432 draws);
- B1, W=100: 1476-1575;
- B10 targets 1567-1576, with 423-432 prior draws.

This is a direct consequence of the owner's August boundary, so no owner decision is needed.

---

## 3. CORRECTIONS

| ID | Finding | Change |
|---|---|---|
| C1 | **Exposure record is incomplete.** Ratified R1 v0.4 (lines 14 and 81) and Proposal v0.3/v0.4 (the Draw 1587 operator-evidence paragraph) quote the published results of Powerball draw **1587**, which is now in the quarantined range (after the first ten). This review's comparison of the old and new Proposal displayed that paragraph in the reviewer chat. The consolidated Proposal removes the paragraph, which is correct. R1 is protected and stays unchanged. | Add item 5, value-free: "Ratified R1 v0.4 and Proposal v0.3/v0.4 quote the published results of Powerball draw 1587 (quarantined range) as drawn-order evidence. These files remain in the repository; R1 is protected and unchanged. Claude's 25 October consolidation review displayed that Proposal paragraph in the reviewer chat." |
| C2 | **Mapping matrix is heading-level, not requirement-level.** 383 of 513 rows say only "PRESERVED_HEADING - text may be locally updated; compare full diff". 0A and ERR rows say "INTEGRATED" with no location. `INTEGRATED_OR_HISTORICAL` and `INTEGRATED_OR_WITHDRAWN` are not dispositions. | Map each ratified requirement (each 0A bullet, each ERR-R2 table row, each A-xx item) to an exact new section, or to "WITHDRAWN: replaced by X". |
| C3 | **ERR-R2 anchors.** Only ERR-R2-04/05 have labelled text. | Add a short R2 index: ERR-R2-01..06, each with its new section, so references in code, tests and handovers resolve. |
| C4 | **Verbatim-block evidence is partial**, and no checker script was supplied. | Add the R3 tie/readout sections, and any restated E_1/TIE identity text, to the block list. Include the checker script so its report can be reproduced. |
| C5 | **Register.** It gives no status for the out-of-scope documents that may mention old rules: `doc/experiments/P3_E1_..._REVIEW_CANDIDATE`, the Windows POC specs v0.1/v0.2, the handovers and the root `README.md`. | One line each: historical, superseded, or to-update-later. |
| C6 | **The same current-rule blocks are pasted verbatim into four documents:** the masters, boundary, "Mode H is not open", N-1, views and dates paragraphs. They agree now, but they will drift. | Give each block one normative home: data, views and N-1 in R2; boundary in R2 and R3; implementation in Architecture. The others should cite it in a sentence. This is the D1 principle already agreed for the numerical rules. |

---

## 4. OPTIONAL

- **O1:** the R3 example JSON (line 674) and the Architecture console example (line 590) use target draw 1588. Use an obviously illustrative number, or a development target such as 1576.
- **O2:** P3 section 4 should add the walk-forward window pre-registration (Powerball 1145-1576, Oz 1475-1693) to its OPEN list, and O2 (owner-supplied real pre-boundary fixtures).
- **O3:** the R2 header still says "Date: 22 October 2026 ... DRAFT FOR USER REVIEW"; update it to the consolidated edition date.

---

## 5. P3 v0.2 (rewritten): acceptable

W1-W6 match the v3 direction exactly:
- C1-C6;
- the ledger-pinned prefix-only reader with `int64` views and the `.base` test;
- the forecast-only 1577 golden from `06f6e0f` with a first-field filter;
- human-speed timing;
- the retirements;
- the gates.

Phases 1-3 and the approval boundaries are correct. Apart from O2, the only missing item is the synthetic E_1 goldens: W2 says "accepted synthetic E_1 vectors" without their hashes, which B2 item 1 fixes in R2.

---

## 6. How to fix (for consolidated v0.2)

1. **Section-by-section current-state pass** of the Proposal, R2 and Architecture. Every section must be either:
   - current text, rewritten where needed; or
   - moved, as a one-line pointer, to Appendix S.

   Text written for a past state must not stay in the body. Protected blocks stay byte-identical.
2. **Restore every B2 item** in its normative home.
3. **Apply B3, then C1-C6.**
4. **Evidence:**
   - re-run the stale-phrase scan with these terms added: `444`, `20261021`, `twelve`, `12-worker`, `requirements.txt`, `scrap`, `layered`, `future` (applied to R2/R3), `v0.3` and `v0.5` (applied to governing-document references). Report zero unexplained hits outside Appendix S;
   - provide the requirement-level matrix (C2) and the checker script (C4).

Claude will repeat the same independent checks on v0.2.

*End of document.*
