# OUTLANDISH_01 — Independent Claude Reviewer Brief and Working Protocol v0.1

**Date:** 16 November 2026 (Australia/Adelaide)  
**Project:** `hydra3333/analysing_perceived_randomness_in_reality`  
**Strict OUTLANDISH workspace:** `GAIS/OUTLANDISH_01/`  
**Audience:** Standby Claude chat acting as an **independent technical/scientific reviewer**; ChatGPT acts as the OUTLANDISH implementer; the project owner makes consequential decisions.  
**Status:** Working handover and proposed lightweight review/communication protocol. **Not** a change to ratified science v0.2, a new project-governance regime, or an authorisation for production scans.

## 1. Immediate request to Claude

Please independently examine the current OUTLANDISH_01 Q3/Q4 implementation **as committed**, concentrating on (a) scientific and functional correctness, (b) whether the implementation faithfully follows ratified matching/reporting specification v0.2, and (c) whether we have accumulated avoidable complexity, repeated work, or administrative machinery.

**This is a focused review, not an invitation to redesign the project or implement changes.** Identify substantial faults and propose the smallest defensible corrections. Keep room for unconventional exploratory science while being exact about what does, and does not, constitute qualified evidence. Avoid demands for additional approvals, ledgers, registries, broad audit frameworks, or elaborate testing unless you can demonstrate an important correctness or safety issue they uniquely solve.

Start with a concise **independent findings memo** rather than modifications to code. Use the response format in §7 and the communication rules in §6. If further evidence is necessary, ask only targeted questions; do not infer unseen file contents or silently use unrelated parent-project material.

## 2. Authoritative material and repository checkpoint

Read these directly from GitHub under `GAIS/OUTLANDISH_01/`:

1. `OUTLANDISH_01_Consolidated_Matching_Reporting_Spec_v0_2_RATIFIED.md` — **binding matching/reporting science** (owner ratified 9 Nov 2026; historical proposal wording inside does not reverse that decision).
2. `OUTLANDISH_01_Living_Decisions_and_Progress.md` — especially **§13**, the last in-repository handover; **note that §13 predates the subsequent Q4b–Q4g Windows qualification results described below**. This brief documents the newer owner-provided test outputs but does not replace the living file.
3. `OUTLANDISH_01_Q3_Packed_Matcher_v0_4.py`, `OUTLANDISH_01_Q3_Event_Classifier_v0_1.py`, `OUTLANDISH_01_Q3_Event_Interface_Smoke_v0_1.py` — shared scanner, classifier and event interface.
4. `OUTLANDISH_01_Q4_Published_Source_Guards_v0_1.py`, `OUTLANDISH_01_Q4c_Synthetic_Run_Processing_v0_1.py`, `OUTLANDISH_01_Q4d_Statistical_Core_v0_1.py`, `OUTLANDISH_01_Q4e_Synthetic_Report_Bundle_v0_1.py`, `OUTLANDISH_01_Q4g_Verified_Synthetic_Aggregate_v0_1.py` — main Q4 engineering slices.
5. Their matching Q4 test/qualification Python modules and README files, plus historical Q1/Q2/Q3 qualification material **as necessary to answer a concrete review question**.

**GitHub checkpoint verified by ChatGPT:** `f42ae71ad340bb7db7b5808ac59ebc4f2009bc67` — `OUTLANDISH Q4b-Q4g synthetic qualification and integration`. It adds **17 files, all in `GAIS/OUTLANDISH_01/`**. Previous handover commit `8cdfdb019f4425e5a427b185e5542d50cfb3c53f`; earlier Q3 v0.4/Q4a qualification commit `39d569b`. Review the named snapshot, and report if `main` has advanced rather than silently comparing different revisions.

The parent project's unrelated Oz Lotto/Mode H work has local uncommitted changes and **must not be disturbed**. Do not read parent results, master histories, holdout material, or parent `exchange/` as part of this review. The only authorised project workspace for review artifacts or changes is `GAIS/OUTLANDISH_01/`.

## 3. Purpose, scientific boundaries, and design decisions

OUTLANDISH is an autonomous exploratory investigation of possible structure in the decimal expansions of six mathematical constants, tested retrospectively against Australian Powerball and Oz Lotto draw histories. Unexpected descriptive patterns may be worth investigation; they **do not** by themselves establish predictive power or authorise a parent-project forecasting method.

- Six immutable high-first packed BCD constant files already exist, each **10,000,000,000 logical digits** / **5,000,000,000 bytes**; existing receipts and hashes were owner-verified. Constants: `pi`, `phi`, `e`, `log2`, `gamma`, and lemniscate **half-perimeter**. Generation is finished; no new numerical generation or file replacement is requested.
- The retained converter receipt is a genuine existing artifact, not a new approval or registry record. The packed scan computes a whole-source SHA-256 **as part of its single sequential read**. Comparing this already-computed digest to the receipt is part of ratified integrity checking; **do not propose a compulsory separate 5-GB pre-hash scan** merely for process assurance. The small deterministic receipt readback samples are a preflight check, not a replacement for the scan's full digest.
- Powerball historical era is **draws 1144–1576 inclusive**, cutoff exclusive **1577**, isolated file `POWERBALL_preholdout_only.csv` inside the OUTLANDISH tree; retain operator-drawn order. Oz uses the modern **seven mains plus three supplementaries** rules, but its **approved isolated historical file and exact era/cutoff remain unconfirmed for this adapter**. Do not invent them or access future/holdout outcomes.
- One common streaming packed reader, game-separated canonical families, all valid start positions (including odd offsets), correct per-family EOF, role/overlap handling, stable four-column raw CSV, reproducible classification without packed-data reread, and clear REAL-versus-NULL separation are scientifically important.
- The owner approved a **fixed 4,000,000 packed-byte default chunk** on both 16-GB and 32-GB hosts, with a manual 8,000,000-byte override. No automatic RAM-based switch.
- Proposed primary positional analysis: Powerball `P3_any`, Oz `O3_any`; median minimum absolute W→W+1 gap, deterministic signed-gap ties; **10,000 whole-draw-label permutations including empty draws** and Holm over **exactly six constants within each game**. This primary choice is **owner-vetoable before qualified REAL work**. Descriptive, exploratory views remain available. Do not silently amend these science choices.
- The separately proposed adaptive/post-match forecasting research is **parked and unratified**. No forecasts, parent experiment integration, or holdout access are authorised.

## 4. Actual progress — distinguish synthetic qualification from REAL science

| Stage | Recorded position | Evidence/limitation |
|---|---|---|
| Q1 — historical reconciliation | **PASS** | Exact saved phi 10^8/10^9 comparisons; older 10^9 legacy material subsequently retired with recorded evidence. |
| Q2 — independent reference oracle | **PASS** | Powerball and Oz artificial correctness/adversarial qualification, with preserved historical scanner defect finding. |
| Q3 — packed matcher/classifier | **Synthetic PASS** | Q3 v0.4 streaming/shared PB/Oz qualification, 4 MB default. |
| Q4a — early fixture guards | **Synthetic PASS** | Four isolated test runs, 53 refusals, 51 matcher regressions. |
| Q4b — published-source/receipt/profile guards | **Windows synthetic PASS** | 69 refusals; one optional Windows symlink test can be skipped. Zero production scans/history reads. |
| Q4c — test REAL/NULL-like processing | **Windows synthetic PASS** | Self-test: 10 refusals; integration: four runs/26 refusals; zero production scans/history reads. |
| Q4d — statistics | **Windows synthetic PASS** | 1,025 arithmetic hand checks; 13 refusals; integration four artificial scans/two reports. |
| Q4e — reporting/replay provenance | **Windows synthetic PASS** | Four test runs/four reports/39 refusals; read-only replay tests. |
| Q4f — six-constant/two-game matrix | **Windows synthetic PASS** | 24 artificial runs/24 reports/92 refusals. |
| Q4g — six-constant game aggregation | **Windows synthetic PASS** | 24 artificial runs/24 upstream reports/two game aggregates/23 refusals. |
| Q4 production readiness | **OPEN — current review** | Existing entry points are fixture/synthetic only; no qualified production runner, no approved REAL Oz adapter, no complete production integration sign-off. |
| Q5 — new qualified REAL scans | **NOT AUTHORISED** | Requires remaining Q4 qualification and separate owner decision. |
| Post-match/adaptive forecasting | **PARKED** | No implementation or parent-project admission. |

These are **owner-provided Windows command results** plus the committed source state, not a claim that the reviewer has independently run or inspected genuine 5-GB source files. Do not relabel synthetic evidence as qualified REAL processing.

## 5. The concern: correctness first, but KISS and least administration

The owner has expressly raised the possibility that Q4a–Q4g expanded into **over-admin-engineering**. The implementer agrees that this is plausible. Please review with the following distinctions:

**Keep where needed for science/data integrity:** genuine role and order checks, independent oracle comparisons, drawset cutoff and source identity, once-through whole-file digest verification, typed REAL/NULL isolation, atomic INCOMPLETE→COMPLETE for a new run, meaningful raw-event and historical-source hashes, reproducible arithmetic and exact negative test cases.

**Challenge unless they have demonstrated scientific value:** additional approval layers, SHA allowlists or registries, elaborate review ceremonies, redundant hash passes, repeated recomputation of expensive Monte Carlo work simply to open an old report, excessive implementation-source hash gating, duplicated validators, numerous interdependent manifest formats, or mandatory NULL processing before ordinary REAL reporting.

Specific **audit hypotheses** (not predetermined verdicts):

1. **Full-source hashing:** Verify it is performed during the **same scan read**, not in a separate compulsory 5-GB pass. Preflight receipt samples are acceptable and cheap. Do not call this requirement "administrative" in itself: it is ratified v0.2 data integrity.
2. **Historical code hashes:** Q4e/Q4g record code-file SHA-256 and currently refuse historical report replay if the *present installed code* differs. That may unnecessarily make trustworthy old reports unreadable after normal maintenance. Can we preserve provenance while allowing archived reports to be viewed or explicitly reanalysed using an appropriate implementation?
3. **Repeated recomputation:** Q4e/Q4g recompute analytical reports, including permutations, when verifying/reading aggregates. Determine the concrete computational cost and whether simple digest checks + source/event provenance are sufficient for ordinary loading, reserving full recomputation for an explicit audit/reanalysis operation.
4. **Unnecessary REAL/NULL coupling:** Q4g currently requires six REAL-like **and** six NULL-like reports simultaneously. Ratified v0.2 allows REAL research first and optional, later, separately labelled NULL comparisons. Production REAL aggregation should not be blocked by absent NULL data.
5. **Too many wrappers:** Q4a, Q4b, Q4c, Q4e and Q4g each carry overlapping identity, path, digest, replay and manifest checks. Identify opportunities to consolidate into a **small number of shared scientific/IO boundaries** without weakening meaningful refusal tests.
6. **Hard production gates:** Recheck game era/cutoff, exact source role semantics, genuine six-constant identity, create-only run isolation, no parent holdout leakage, and no ability to spoof test roots as REAL. Prioritise actual correctness failures above aesthetic simplification.
7. **Statistical correctness:** Check category expectations/nesting, same-draw physical overlaps, signed tie order, zero-match chronological draws, valid versus undefined Monte Carlo permutations, the specified two-sided p convention and within-game six-constant Holm. Identify science-altering discrepancies explicitly; they require owner decisions rather than quiet refactors.
8. **Production performance feasibility:** Avoid an unnecessarily materialised multi-gigabyte intermediate or a compulsory extra constant-file pass. Benchmark-driven changes only; no speculative framework optimisation.

Please distinguish **verified bug**, **design incompatibility with ratified v0.2**, **simplification opportunity**, and **optional improvement**. The owner particularly wants the scientific core protected against administrative noise. A real defect must not be waved away in the name of KISS, but speculative edge-case scaffolding should not dictate the architecture.

### Preferred destination architecture (subject to review)

A small shared matcher and pure classifier/statistics core; a straightforward fixed-root **REAL** runner; a distinctly isolated **NULL** runner/adapter; one minimal run manifest with the relevant receipts, source/drawset and result digests; reports generated from validated events without re-reading the packed constant; optional separate NULL comparisons and game-wise six-constant aggregation. No project-wide registry, extra signing or approval service, unrelated parent integration, or sprawling "qualification platform". Keep existing passing synthetic suites as regression evidence even if production internals are simplified.

## 6. Communication protocol — strict OUTLANDISH-only tree and owner relay

**Hard GitHub scope fence:** All OUTLANDISH review communications and any proposed files, scripts, changes, test fixtures or evidence must be **within `GAIS/OUTLANDISH_01/` and its subdirectories, and nowhere else**. In particular **do not write to** the repository's top-level `exchange/`, `review/`, `results/`, `source_data/`, `src/`, or any parent-project documents. Do not read held-out or non-OUTLANDISH parent data for this review. Do not edit published 5-GB constants, old saved evidence or other projects' working files.

**Lightweight route:**

- ChatGPT prepares a focused Markdown request. The owner relays the file or its contents to Claude. Claude reads the relevant **GitHub OUTLANDISH tree at the stated commit** and returns a Markdown findings memo to the owner. The owner relays it back to ChatGPT. No direct AI-to-AI channel, automatic background collaboration or shared-worktree assumptions are implied.
- Put any **committed** review exchanges in **`GAIS/OUTLANDISH_01/REVIEW/`** (new in-tree subdirectory, if the owner elects to keep them). Suggested names: `OUTLANDISH_REVIEW_001_ChatGPT_to_Claude.md`, `OUTLANDISH_REVIEW_002_Claude_to_ChatGPT.md`, with increasing sequence numbers within this OUTLANDISH conversation. This is **not** the parent project's `EX_NNN` sequence. A short single file per meaningful exchange is preferred; avoid ZIPs, duplicate logs and multi-file paperwork unless technical attachments are truly needed.
- Each exchange should include: source revision/commit SHA, subject/specific question, relevant file paths and line locations, finding and severity, minimal recommended correction, and any decision explicitly reserved for the owner. Do not cite local Windows-only test claims as independently verified unless Claude actually ran them.
- **Reviewer is read-only by default.** Claude should not modify/push GitHub code or create PRs without the owner's separate explicit instruction. ChatGPT remains implementer. The **owner controls relaying, staging, commits and pushes**. Before each commit, verify that all staged paths begin `GAIS/OUTLANDISH_01/`; other staged entries mean STOP. Existing unrelated local changes stay untouched. Use explicit path-scoped staging; no `git add .`, `git commit -a`, force-push or cleanup of unrelated files.
- We can keep minor conversational clarifications in chat. Only consequential findings, decisions or a meaningful review checkpoint need a stored Markdown exchange. The living decisions/progress file remains the **one principal operational status record**; this reviewer protocol is not a second decisions register.
- If an OUTLANDISH file to inspect is unavailable at the named commit, state the gap and ask the owner for that exact file. Never silently broaden scope to parent folders to find an alternative.

## 7. When to seek the reviewer — limited, consequential checkpoints

**Review point A — NOW: independent scientific/KISS audit.** Review the Q3/Q4 implementation at `f42ae71` and return ranked, concrete findings. ChatGPT/owner then decide a short correction list. Routine refactors may proceed without repeated review; substantive v0.2 science changes go to the owner.

**Review point B — BEFORE authorising the production design/run interface.** After ChatGPT drafts the minimal fixed-root production-runner approach (and resolves or explicitly blocks REAL Oz profile), ask Claude to review **only consequential** matters: data/holdout firewall, REAL/NULL separation, single-pass full digest, durability/status boundary, report loader and genuine science compatibility. Do this before an irreversible or expensive production interface is adopted; **do not request approval for every implementation detail**.

**Review point C — FINAL Q4 / BEFORE first Q5 REAL scan.** Present the implemented production path, compact test evidence, all open limitations, planned compute costs, and remaining scientific decisions for one focused independent preflight review. The owner decides whether findings must be fixed and separately **authorises or rejects Q5**. Claude's review is advisory, not an independent approval authority or compulsory sign-off ceremony.

**Ad hoc exception:** Request review promptly for an unexpected scientific contradiction, an unreconciled REAL-versus-null contamination risk, missing historical profile/holdout boundary evidence, risk of irreversible loss, or a significant change to the ratified statistical proposal. Do **not** interrupt implementation for trivial naming/style choices or merely to increase test/refusal counts.

If independent review is unavailable, record the limitation openly; do not invent assent or silently promote Q5.

## 8. Requested response format from Claude for point A

Please return one Markdown memo (suggested in-tree filename `OUTLANDISH_REVIEW_002_Claude_to_ChatGPT.md` if the owner stores the exchange), with:

1. **Snapshot and scope:** exact commit reviewed; exact OUTLANDISH files examined; what you did not independently validate.
2. **Highest-priority findings first:** for each, `Severity: BLOCKER / IMPORTANT / MINOR / OPTIONAL`, and `Type: scientific correctness / binding-spec conflict / operational integrity / KISS simplification`. Give a specific file, function and line range, the reason, a reproducible test/example where possible, and the **smallest** proposed fix.
3. **KISS verdict:** which checks are essential, duplicated, expensive or obstructive; how to simplify without loss of scientific validity. Pay special attention to §5 hypotheses.
4. **Missing factual inputs/owner choices:** particularly Oz approved modern-era isolated source/cutoff and the owner-vetoable primary W→W+1 choice. Do not invent either.
5. **Recommended next code slice and whether a second focused review is justified before implementing it.** Separate must-fix from nice-to-have. A clear "no consequential issues found" is a valid outcome if supported by the inspection.

**Please do not:** run real production scans; modify any published source or historical result; read or touch parent-project data/work; create a broad governance program; automatically implement your findings; classify exploratory retrospective coincidences as predictive evidence; or assume all currently passing synthetic tests prove production readiness.

---

**Owner/implementer note:** This is a proposal for efficient technical cooperation, not a replacement for established owner authority or the ratified v0.2 science. If the owner wants a different communication route, adjust the path/protocol **while keeping every review artifact and every write strictly within `GAIS/OUTLANDISH_01/`**.
