# OUTLANDISH_01 - Claude Reviewer Handover (for the successor Claude chat)

**Version:** v0.3
**As at:** 2026-11-16, about 09:35 (Australia/Adelaide)
**From:** The Claude reviewer chat that started 16 Nov 2026 and completed review points A and B
**To:** Any successor Claude reviewer chat
**Supersedes:** `OUTLANDISH_01_Claude_Reviewer_Handover_v0_2.md` (16 Nov). All of its content is carried forward here, updated for review point B, the owner's decisions after it, and the reviewer's new commit permission.
**Authority:** A continuity record, not a decision document. On any conflict, these prevail, in order: the ratified spec v0.2 in the repository; the in-repo living file `OUTLANDISH_01_Living_Decisions_and_Progress.md`; ChatGPT's review briefs (point A and point B, both 16 Nov). Report conflicts rather than resolving them silently.

---

## 0. What you are walking into

**Project.** OUTLANDISH_01 ("GAIS Outlandish Physical Constants Examination") is a side project of the GitHub project owner (hydra3333). It searches 10-billion-digit expansions of six mathematical constants for patterns matching historical Australian Powerball and Oz Lotto draws, as exploratory research. It is a subordinate component of the repository `hydra3333/analysing_perceived_randomness_in_reality`, confined to `GAIS/OUTLANDISH_01/`. Its methods may later be adapted into the parent project as a new method family, but only through that project's own review route.

**Roles.**
- ChatGPT (an OUTLANDISH-specific chat) is the designer and implementer.
- Claude (you) is the independent technical and scientific reviewer. Read-only by default.
- The owner relays files between chats and decides consequential matters.
- Commits: the owner commits ChatGPT's work. Since 16 Nov the reviewer may also commit its own review documents directly, only under `GAIS/OUTLANDISH_01/`, only when needed (section 1).

**Where things stand.** Review points A and B are complete, both on 16 Nov. Both memos and both reviewer evidence scripts are committed in `GAIS/OUTLANDISH_01/REVIEW/`. ChatGPT accepted Review A in full (living file section 14.5). The point B memo and the owner's two decisions after it (section 6.2) were sent to ChatGPT with a request to agree; its reply had not arrived when this handover was written. The next reviewer task is that reply, then review point C.

---

## 1. Working rules with this owner (apply throughout)

- **Model choice.** Before statistical design or validity work, root-cause investigations, or a cold-read review of a design or code before it goes to ChatGPT, say "Suggest switching to Fable (High) for this" and wait for "go". Everything else proceeds on Opus without asking. When a Fable task finishes, say so. You cannot see which model is selected, so flag and hold. The owner's Fable allowance is limited. For a large review, offer a split: locating and measuring on Opus, statistics and the final cold read on Fable. The owner chose Fable for the whole of points A and B.
- **Model switch advice (owner request, 16 Nov).** Tell the owner plainly each time to switch: to Fable when a Fable task starts, and back to Opus when it ends. Packaging, handovers, paste blocks and commits are Opus work. Note: the session tells you which model is running, so check it rather than assuming.
- **Documents for the repo:** US-ASCII, verified mechanically after writing. Filenames carry their version. Line endings: the owner wants CRLF on his Windows disk. The repository stores OUTLANDISH files with LF (the owner's git converts on checkout), so files the reviewer commits are stored with LF; files handed to the owner directly are CRLF.
- **Never name the owner** in anything that may be committed. Use "the GitHub project owner" or hydra3333.
- **End anything to be relayed to ChatGPT with a short paste-ready block.**
- **Plain English to the owner.** Decisions as question / why / recommendation / options. Show reasoning, alternatives and uncertainties.
- **Distrust assertion.** Verify against source (file:line). Never present an owner-reported Windows test result as independently verified.
- **Simplicity over administration.** No registries, approval layers, allowlist catalogues, rule languages or ceremonies. Effort goes to correct science, correct code and meaningful tests.
- **Handovers.** At each stage, judge whether a handover update is due, and say so. Handovers are comprehensive "as at" documents.
- **Process notes.** At each substantial milestone, give a short independent note on how the process went.
- **Repository fence.** Read and write only under `GAIS/OUTLANDISH_01/`. Never read parent-project results, master histories, holdout material or the parent `exchange/` folder.
- **Reviewer commits (owner permission, 16 Nov).** The reviewer may commit directly into the `GAIS/OUTLANDISH_01/` tree only, only when needed. In practice: only the reviewer's own memos, evidence scripts and handovers, in `REVIEW/`. Never ChatGPT's code, the living file, or anything outside the tree. Stage by explicit path; before committing, check every staged path starts `GAIS/OUTLANDISH_01/`, otherwise STOP. No force-push. Report the commit ID to the owner and remind him to pull. Push access comes from the session's `add_repo` with push access; a sparse clone limited to `GAIS/OUTLANDISH_01/` keeps parent folders off disk.
- **Repository CLAUDE.md.** The repository's top-level `CLAUDE.md` says that a cloud reviewer session is not the local runner and that its rulebook is reference material only. It does not change the reviewer's role.
- **Misdirected pastes.** The owner sometimes pastes a block meant for ChatGPT into the Claude chat. If a request is the implementer's job (for example updating the living file), say so rather than doing it.

---

## 2. Current state (as at 16 Nov)

**Constants: generation finished.**
- Six immutable packed files, each 10,000,000,000 logical digits (integer digit at offset 0), 5,000,000,000 bytes, format `OUTLANDISH_PACKED_BCD_HIGH_FIRST_V1`, each with a `.wsl-receipt.json`. Owner-verified. Location `G:\OUTLANDISH_01\large_artifacts\digits\` on the owner's Ryzen 3900X.
- Constants: pi, phi, e, log2, gamma, lemniscate half-perimeter.
- Filenames and SHA-256 values, from `OUTLANDISH_01_Operational_Handover_2026-11-14_v0_8.md` section 1 (owner-reported, not verified by Claude):

| Constant | Filename | Packed SHA-256 |
|---|---|---|
| pi | `digits_pi_10_to_10.packed.bin` | `62ab5b9a511eb0fcf5d09717df9ee51f8bd29ea09acf379e6f1045c537ababe2` |
| phi | `digits_golden_ratio_10_to_10.packed.bin` | `dd80be0c3fdb330fe4e1780c2d53bf03bde297a5dea83b5785cd3349838ad36d` |
| e | `digits_e_10_to_10.packed.bin` | `522f088b013432f775098df863b851ad87a4f5d0f0296b54cb00d6f13f72720f` |
| log2 | `digits_log2_10_to_10.packed.bin` | `6993b8b6c6f46ae13b5e213aae0d46e784c8acae510f10e6862aecde83a15694` |
| gamma | `digits_gamma_10_to_10.packed.bin` | `68e4a47d27759632dd8c608af973fa5bd22fb2aa7290d5e92f59e485ceb85e6a` |
| lemniscate | `digits_lemniscate_10_to_10.packed.bin` | `958210dcda823fd1951b8487fbfe3cb98aeda9748c2b0dea4db9684608d21369` |

- The legacy 10^9 byte-per-digit files have been retired, with evidence recorded.

**Powerball history.** `GAIS/OUTLANDISH_01/POWERBALL_preholdout_only.csv` is in the tree at the review commit. Its SHA-256 there is `c71039c63f64479b2d83c10e8df3ad5e7525091b3a7f44c5a2680015f4fd2e54`. The Q4b drawset gate accepts it: 433 rows, draws 1144 to 1576.

**Qualification stages.**

| Stage | Status | Evidence |
|---|---|---|
| Q1 historical reconciliation of saved phi results | PASS | Owner Windows result |
| Q2 independent reference oracle | PASS | Owner Windows result |
| Q3 packed matcher/classifier (v0.4, 4 MB chunks) | Synthetic PASS | Owner Windows result; also Claude's own brute-force check on Linux |
| Q4a-Q4g guards, processing, statistics, reporting, six-constant matrix and aggregation | Synthetic PASS (each) | Owner Windows results; also all seven suites run by Claude on Linux at `f42ae71` |
| Q4h minimal Powerball production-shaped slice | Synthetic PASS | Owner Windows result (5 refusals; 6 runs, 6 reports, 1 aggregate, 27 refusals, 10,000 permutations per report); also run by Claude on Linux at `b7ce6fd`, plus Claude's own 433-draw end-to-end check |
| Q4 production readiness | OPEN | Review points A and B complete; production mode switch (K1), three tests, seed rule and Q5 switch to implement (section 6.2) |
| Q5 qualified REAL scans | NOT AUTHORISED | |
| Post-match forecasting | PARKED, unratified | |

Missing for production: the production entry point built on Q4h with the mode switch, an approved REAL Oz Lotto adapter, the read-only receipt preflight of the six real files, review point C, and owner Q5 authorisation.

**Repository checkpoints.**
- `main` when this handover was written: `677347b2a9e62e1b9d96dc6bd494adab61f3a241` (the reviewer's point B commit). This handover is committed on top of it.
- Point B review commit: `b7ce6fd052d65186b7e4d338260aebf054188e45` (Q4h v0.1 and the point B brief).
- Living file recording Review A disposition: `bbdf3f4`.
- Point A review commit: `f42ae71ad340bb7db7b5808ac59ebc4f2009bc67`.
- Earlier handover commit: `8cdfdb019f4425e5a427b185e5542d50cfb3c53f`.
- Q3 v0.4/Q4a commit: `39d569b`.
- Forecasting proposal commit: `c48ac3c393d2eab30014e6200d427b76d90f47ac`.

**Living file:** current to Review A (section 14, with 14.5 recording ChatGPT's acceptance of F1 to F10), checked by the reviewer at `bbdf3f4` and found accurate. It does not yet record Q4h, Review B or the owner's decisions D1/D2. Updating it is ChatGPT's job, not the reviewer's.

**Review exchanges so far.**

| # | Document | State |
|---|---|---|
| 001 | ChatGPT's point A brief, `REVIEW/OUTLANDISH_01_Claude_Reviewer_Brief_2026-11-16_v0_1.md` | Committed by the owner (`a333990`). |
| 002 | `REVIEW/OUTLANDISH_REVIEW_002_Claude_to_ChatGPT.md` (point A) | Committed by the owner (`a333990`); relayed; accepted by ChatGPT (living file 14.5). |
| - | `REVIEW/OUTLANDISH_REVIEW_Claude_Independent_Checks_v0_1.py` (point A evidence) | Committed by the owner (`fde9fe3`). |
| - | ChatGPT's point B brief, `REVIEW/OUTLANDISH_01_Q4h_Review_B_Brief_v0_1.md` | Committed by ChatGPT/owner (`b7ce6fd`). Unnumbered. |
| 003 | `REVIEW/OUTLANDISH_REVIEW_003_Claude_to_ChatGPT.md` (point B) | Committed by the reviewer (`677347b`); relayed with the owner's decisions; ChatGPT reply pending. |
| - | `REVIEW/OUTLANDISH_REVIEW_Claude_Q4h_EndToEnd_Check_v0_1.py` (point B evidence) | Committed by the reviewer (`677347b`). |

---

## 3. Owner decisions (fixed; do not reopen)

1. **Matching/reporting spec v0.2 RATIFIED on 9 Nov 2026** (`OUTLANDISH_01_Consolidated_Matching_Reporting_Spec_v0_2_RATIFIED.md`). Its header still carries pre-ratification wording; that does not reverse ratification.
2. **Sequencing.** All six constants first (done), then Q1-Q5 qualification, then separately authorised scans. Each Q5 REAL scan needs owner authorisation.
3. **Engine.** Canonical-key families with post-hoc classification (ratified in v0.2).
4. **Decoys** approved. Non-contamination of REAL results is release-blocking. Synthetic-digit null worlds are optional.
5. **O2.** Both any-slot and supplementary-last views; supplementary-last is the provisional primary headline.
6. **Oz Lotto.** Modern 7 mains + 3 supplementaries from 47 only, from the first draw of that format; own drawset and own holdout, never Powerball's cutoff. **The approved isolated Oz file and its exact era start and cutoff are NOT yet confirmed for the adapter.** Do not invent them.
7. **Draw data.** Drawn-order provenance is settled and verified. Adapter-fidelity tests are fine; source audits are not.
8. **Not wanted:** an ascending-order flag; a Powerball six-mains-without-PB category.
9. **Simplicity:** no new registry, approval workflow, allowlist catalogue or rule language.
10. **Powerball history:** draws 1144-1576 inclusive, exclusive cutoff 1577, file `POWERBALL_preholdout_only.csv` inside the OUTLANDISH tree.
11. **Forecasting** (when unparked): use ALL known pre-holdout draws, strict walk-forward, no discovery/confirmation split.
12. **Only approved draw source:** Lotterywest-GOV (`www.lotterywest.wa.gov.au`).
13. **Chunk size:** fixed 4,000,000 packed bytes by default on both hosts, with a manual 8,000,000 override; no automatic RAM-based switch.
14. **Lighter working approach** (agreed with ChatGPT, about 14 Nov). The AI makes routine implementation choices and explains them afterwards. One living decisions document. The owner decides consequential matters. Calculations run only on the owner's PCs.
15. **Full-file digest** computed during the scan's single read is ratified data integrity, not administration. No separate 5 GB pre-hash pass.

---

## 4. Ratified v0.2: Claude's summary (now checked against the file)

- **Families**, each with its own index: K7 (7 mains; PB 1-35 / Oz 1-47; 14 digits), K7S (PB 7 mains + trailing PB; 16), K6S (PB 6 mains + trailing PB; 14), K6 (Oz 6 mains; 12), K7mix (Oz 6 mains + 1 supplementary in any slot; 14).
- **Role rules.** Distinctness over mains only. PB 1-20 may equal a main. P2's seventh field is a main 1-35. FIXED2 encoding; every digit offset is a possible start, including odd ones.
- **End of file.** Per-family eligibility `k + L_F <= N` via explicit masks.
- **Classification** is post-hoc. P1 = K7S AND drawn order; P2 = K7 AND drawn order; P3 = K6S; O1 = K7 AND drawn order. O2 nesting: drawn-subsequence (subset of) supplementary-last (subset of) any-slot.
- **Raw REAL events:** `draw_number, family, start_digit_offset, matched_digits` (text, leading zeros kept) + `run_manifest.json`. Sorted `(start_digit_offset, family, draw_number)`. Writer aborts on a duplicate identity.
- **Overlaps.** Same-draw overlaps computed by interval intersection. Shifted nestings include `P1_any@k => P3_any@k+2` and `O1@k => O3@k and @k+2`. PB-equals-main P2/P3 pairs. Overlaps do not change expectations. Three units always distinguished: events, distinct offsets, distinct draws.
- **REAL/NULL.**
  - Separate runs. One NULL run MAY index K decoys together (permitted, not mandated). K = 19 / 99 are benchmark defaults.
  - NULL is complementary and optional. v0.2 B7 Q5: "Optional separate NULL runs and reports follow."
  - REAL packed input via the existing receipt (path, size, streamed SHA before completion).
  - REAL drawset fixed in the profile, with a complete integer range `[era_first, cutoff)` exactly once.
  - Fixture IDs 1-999; decoy IDs are text.
  - Drawset SHA checked against the manifest.
  - Old-scanner fixture output kept outside the REAL root.
  - `results_null\` beside `results\`.
  - B4 item 5 and B7 Q4 ask for guard-removal mutation tests.
- **Statistics.**
  - Expectation `E = D x S x (N-L+1) / 10^L`. Conditional order test `Binomial(n, q)`.
  - Empirical decoy tail `(1+b)/(K+1)`.
  - Primary W->W+1 test: P3_any (PB) / O3_any (Oz), median per-pair minimum absolute gap, tie `(abs(b-a), b-a, a, b)`, 10,000 draw-label permutations over all draws including empty ones, `(1+b)/(R_valid+1)` centred on the median of valid permuted medians, two-sided, Holm over the six constants within each game. **Owner-vetoable before qualified REAL runs.**
  - v0.2 fixes no permutation seed rule and does not say how Holm treats an undefined p-value.

---

## 5. Parked: post-match forecasting

- **Status:** a proposal (document 13 below), not owner-ratified, parked.
- **Agreed between the two AIs on 10 Nov:**
  - Nine pilots plus an optional tenth (B01, N1, N2, M1, XA, N4, M2, M3, N7, XB).
  - Decoders: D1, plus D2-core with no sliding.
  - Rank convention: colex.
  - Primary ticket from a rotating constant: `draw_number mod 6`.
  - M2: 38 PB / 32 Oz experts, chance expert included.
  - M3-3 primary.
  - Controls L1-L7 (the stop rule was removed). Stages S0-S4.
- **Document 13 also proposes:**
  - An N2 prefix of 2,000,000,000 digits.
  - Strict N4 overlap exclusion.
  - An M3 cap of 100.
  - Per-origin fixed-panel nulls, with a sequential e-process across origins.
- **Evidence label:** "pre-specified retrospective walk-forward", not independent confirmation.
- Do not work on this unless the owner unparks it.

---

## 6. Review outcomes

### 6.1 Review point A (16 Nov, commit `f42ae71`)

**Verdict.** No scientific defect found. The owner's over-administration suspicion is confirmed in the Q4e and Q4g layers. Nothing committed can run on REAL data, so nothing is a blocker today.

**What Claude did.**
- Read in full: the ratified spec, the living file, matcher v0.4, the classifier, the event-interface smoke file, and the Q4a, Q4b, Q4c, Q4d, Q4e and Q4g modules.
- Ran all seven Q4 `--run` suites on Linux (Python 3.13.18, NumPy 2.5.3) with the committed code. All passed. The Q4b refusal count was 70 against 69 on Windows; one symlink test is optional on Windows.
- Wrote an independent brute-force oracle and compared it with matcher v0.4 and the classifier: 60 random planted cases, both games, six chunk sizes each, 604 events, all equal.
- Re-implemented the tie rule, permutation p, Holm, expectations and the binomial test independently. All equal.
- Timed one 10,000-permutation test: about 2 seconds for Powerball; about 61 to 75 seconds for Oz at illustrative draw counts of 200 and 250.
- The checks are kept as `REVIEW/OUTLANDISH_REVIEW_Claude_Independent_Checks_v0_1.py` (synthetic only, temp folder, no REAL inputs; expected line `REVIEWER INDEPENDENT CHECKS PASS: matcher-trials=60 events=604 classified=604 stats=PASS`). It still passed at `b7ce6fd`.

**Not validated.** The six 5 GB files and receipts on `G:`; anything Windows-specific; the owner's Windows PASS lines; any REAL scan or report; any Oz REAL profile; Q1/Q2 material; matcher versions v0.1 to v0.3; the internals of the test harnesses.

**Findings in the memo.**

| ID | Severity | Type | Summary | Where |
|---|---|---|---|---|
| F1 | IMPORTANT | Binding-spec conflict | Q4g cannot aggregate REAL reports without six NULL reports | Q4g lines 77-79, 133-134, 149-161, 187 |
| F2 | IMPORTANT | Operational integrity / KISS | Reports and aggregates refuse to open if any code file hash differs | Q4e lines 256-257; Q4g lines 256-257 |
| F3 | IMPORTANT | Operational integrity / KISS | Every open, and creation, recomputes the full analysis and demands byte-identical output | Q4e lines 215, 232-234, 259-265; Q4g lines 221, 237-239, 260 |
| F4 | IMPORTANT | Scientific correctness | Permutation count and seed are caller-supplied, default 64; v0.2 fixes 10,000 | Q4e lines 113-114, 121-123, 209-210; Q4g lines 158, 187-190 |
| F5 | MINOR (KISS-important) | KISS | The same checks are implemented several times; Q4a is imported only by its own test | Inventory table in the memo |
| F6 | MINOR | KISS | The only event reader lives in the "smoke" test aid; the classifier imports record classes from matcher v0.2 | Smoke lines 42-92; classifier line 17 |
| F7 | MINOR | Operational integrity | The sandbox check does not refuse a test root nested under the production tree, although its comment says it does | Q4b lines 84-91 |
| F8 | MINOR | Binding-spec gap | Q4 suites mutate data only; guard-removal mutation tests are missing | v0.2 B4 item 5, B7 Q4 |
| F9 | OPTIONAL | Operational integrity | The NULL path will not scale to K=99 as written | Q4e lines 175-178; Q4c lines 158-192 |
| F10 | OPTIONAL | KISS | The permutation loop re-sorts its inputs on every call | Q4d lines 199-204 |

**Notes behind the findings.**
- F2: the hashed list omits matcher v0.2 and the Python and NumPy versions, so the gate is incomplete as well as obstructive.
- F3: the cost is minutes, not hours. The larger problem is fragility: byte-identical replay depends on floating-point library results and on `random.Random.shuffle` staying the same. Shuffle output was identical on Python 3.11, 3.12 and 3.13. No mismatch was demonstrated.
- The Q4e and Q4g README files say ChatGPT's own local tests used stand-ins for the Q3 scanner and classifier. The owner's Windows runs and Claude's Linux runs used the committed code.

**Answers to the brief's eight hypotheses.** 1 confirmed correct; 2 confirmed (F2); 3 confirmed (F3); 4 confirmed (F1); 5 confirmed (F5, F6); 6 sound for Powerball, Oz correctly blocked, one loose end (F7); 7 no discrepancy, one unpinned parameter (F4); 8 REAL path feasible, NULL at K=99 unmeasured (F9).

**Recommended next slice (in the memo).** Build the minimal production REAL path for Powerball small: one events module, one REAL runner, one reporter, one aggregator. Leave the synthetic slices untouched as regression evidence. Must-fix before adoption: F1 to F4. No extra review before review point B.

**Disposition.** ChatGPT accepted F1 to F4 as essential corrections in new production code, F5 to F8 as targeted production work, and deferred F9/F10 (living file 14.5, `bbdf3f4`). ChatGPT then built Q4h.

**Open inputs and owner choices raised.**
1. Oz approved isolated file, column layout, era start and cutoff.
2. Owner veto on the primary W->W+1 statistic.
3. A permutation seed rule, to be fixed in code before the first REAL report. (Decided after point B: see 6.2, D1.)
4. Holm convention: an undefined p-value stays in the family of six and counts as 1 when adjusting the others (Q4d lines 315-321). Conservative; not stated in v0.2.
5. A read-only receipt preflight of the six real files on the Ryzen (12 samples of 4,096 bytes each, nothing written). Needs the owner's go-ahead because it touches the production digits folder.
6. NULL K (19 or 99), only when a NULL run is planned.

**Small errors noticed in the brief.** Its section 1 points to section 7 for the response format; the format is in section 8. It lists eight audit hypotheses; handover v0.1 mentioned five.

### 6.2 Review point B (16 Nov, commit `b7ce6fd`, Q4h v0.1)

**What was reviewed.** Q4h v0.1: four new modules (`OUTLANDISH_01_Q4h_Events_v0_1.py`, `..._Powerball_Test_Runner_v0_1.py`, `..._Powerball_Test_Report_v0_1.py`, `..._Powerball_Test_Aggregate_v0_1.py`, 421 lines in total), a qualification harness and a README. It reuses matcher v0.4, the classifier, Q4b guards and Q4d unchanged. Everything is TEST-only; no REAL entry point exists.

**Verdict.** Suitable as the basis for the minimal Powerball production path. No blocking correctness or safety issue. F1 to F4 all resolved:
- F1: six REAL-like reports alone give Holm; `null_comparison` recorded as not run (Aggregate lines 28-63).
- F2: code hashes recorded, mismatch returned as `code_matches_current`, not refused (Report lines 27-30, 98-100).
- F3: ordinary load checks digests and identities; `audit_test_report` is separate and tolerance-based (Report lines 73-120).
- F4: 10,000 permutations is a constant; any other count is refused on load (Report lines 18, 54-55, 90, 95).

**What Claude did.**
- Ran Q4h `--self-test` and `--run` on Linux: PASS, matching the owner's Windows counts.
- Reran the point A independent checks at `b7ce6fd`: PASS.
- Wrote and committed `REVIEW/OUTLANDISH_REVIEW_Claude_Q4h_EndToEnd_Check_v0_1.py`. It runs Q4h at realistic Powerball shape (433 fabricated draws, six fabricated 300,000-digit constants, about 200 planted events each, 10,000 permutations) and compares with Claude's own calculation. All events, category counts, expectations, evaluable pairs, median gaps, p-values and Holm values agreed. Expected final line starts `REVIEWER Q4H END-TO-END PASS: constants=6 draws=433 permutations=10000`. About 20 seconds on Linux.
- Positive control: planted adjacency in constant `e` gave p = 0.0001, Holm 0.0006; the other five gave Holm 0.46 to 0.98.
- Corruption test: on a 150,000-byte fixture, 48,912 bytes are sampled by the receipt plan. Changing one unsampled byte passed the preflight; the scan refused with "full packed SHA-256 mismatch", the run stayed INCOMPLETE and no event file was left.
- Timing: about 1.7 seconds per report at 433 draws; ordinary aggregate load 0.04 seconds.

**Findings in memo 003.**

| ID | Class | Summary | Where |
|---|---|---|---|
| K1 | Worthwhile KISS | Reach production by passing one small mode value (roots, profile, run type, digits) into the four modules, with two constructors (synthetic; production Powerball). Do not write REAL-named copies, or the tests stop covering the code that runs on REAL data. | TEST identity hard-coded at Runner 33-47, 69, 72, 102-103, 107; Report 40, 62, 77, 83; Aggregate 22-25, 57, 87 |
| K2 | Worthwhile KISS | Aggregate load rebuilds the whole aggregate and byte-compares; any layout change would lock out old aggregates. Compare the six stored report digests instead. | Aggregate 91-96 |
| K3 | Worthwhile KISS | Aggregates use a new `reports_test_aggregate` root; reuse the existing run-location guard instead. | Aggregate 21-25 |
| O1 | Optional | One fixed `report.json` per run; a later report on another statistic cannot sit beside it. | Report 63-66 |
| O2 | Optional | Scanner code hash recorded only at report time, not at scan time. | Report 27-30 |
| O3 | Optional | Audit compares integers with a relative tolerance; fine at N = 10^10, not beyond. | Report 103-105 |
| O4 | Optional | Q4h harness imports three older modules for fixture setup. | Qualification 17-19 |

Not warranted: loading the event file in memory (about 440 events per constant for Powerball REAL); re-validating the run on report load; a digest for the run manifest; changing the classifier's record-class import.

**Tests recommended.** (1) Corruption outside the sampled blocks on a fixture of at least 100 KB; the standard 5,001-byte fixture is fully sampled, so the in-scan digest guard is never the one tested. (2) One 433-draw realistic-shape run. (3) Mode separation once K1 exists. Guard-removal canaries via the harness's existing replace-one-function pattern (Qualification lines 95-111); duplicate identity by a data test instead.

**Owner decisions after point B (16 Nov), both subject to ChatGPT's agreement.**
- **D1 seed rule:** derived per game and constant. Claude's proposed formula, sent to ChatGPT for confirmation or adjustment: seed = first 8 bytes, big-endian, of SHA-256 of the ASCII text `OUTLANDISH_01|<game>|<constant>|PRIMARY_W_TO_W1|V1`. Fits the Q4d bound 0 <= seed < 2**64. Each report records the label and the seed.
- **D2 Q5 switch:** one true/false constant in the single production entry-point file, default false. The owner's commit setting it true is the authorisation record. Only starting a scan needs the switch; reading existing results does not.

The committed memo 003 still lists D1/D2 as pending; it is the record of what was advised. The living file should record the decisions once ChatGPT agrees.

---

## 7. Earlier non-design findings (for reference)

- **y-cruncher on Windows, 9 Nov.** Swap mode needs elevation. Since v0.8.3, swap files get a permission list of Everyone = delete only and Administrators = full access (`RawFile_Windows.ipp`, lines 130-223 and 355, at the v0.8.7.9547 commit). The rename-and-reopen therefore fails with errno 13 under a standard account. SeManageVolumePrivilege does not help. Resuming must also run elevated. The owner ran elevated, and generation is now finished.
- **Lemniscate:** the converter halves y-cruncher's full perimeter before packing.
- **Converter agreement, 16 Nov.** The Q4b guard's receipt fields, filename stems and sample plan are identical to `OUTLANDISH_WSL/wsl_format.py` and `wsl_convert.py`. Gamma and lemniscate were produced on the i5 with a native Windows copy of the converter; its receipts have not been seen by Claude.

---

## 8. Document trail

All are under `GAIS/OUTLANDISH_01/` on GitHub unless noted. Handovers v0.1 and v0.2 were committed under `REVIEW/` by the owner.

| # | Document | Status |
|---|---|---|
| 1 | `OUTLANDISH_01_Common_Matching_Engine_Claude_Review_v0_1.md` (in `OUTLANDISH_WSL/doc/`) | History |
| 2 | `OUTLANDISH_01_Common_Matching_Engine_Claude_Review_Response_v0_1.md` (`OUTLANDISH_WSL/doc/`) | History |
| 3-6 | ChatGPT reconciliations and spec candidate (old ChatGPT file library only) | History, superseded by 8 |
| 7 | `OUTLANDISH_01_Claude_Single_Review_of_Consolidated_Spec_v0_1.md` (C1-C20) | History |
| 8 | `OUTLANDISH_01_Consolidated_Matching_Reporting_Spec_v0_2_RATIFIED.md` | **Binding** |
| 9-12 | Forecasting brainstorm, Claude round 1, ChatGPT round 2, Claude round-2 reply | History |
| 13 | `OUTLANDISH_01_PostMatch_Adaptive_Forecasting_Proposed_Spec_v0_1_FOR_OWNER_REVIEW-2026.11.10.md` | Proposal, parked |
| 14 | `OUTLANDISH_01_Claude_Chat_Record_for_ChatGPT_Recovery_v0_1.md` (14 Nov) | Superseded |
| 15 | `OUTLANDISH_01_ChatGPT_Recovery_Reconciliation_20261114.md` (14 Nov) | Superseded |
| 16 | `OUTLANDISH_01_Living_Decisions_and_Progress.md` | **Operational status record** (current to Review A; Q4h/Review B not yet recorded) |
| 17 | `REVIEW/OUTLANDISH_01_Claude_Reviewer_Brief_2026-11-16_v0_1.md` | Point A brief |
| 18 | `REVIEW/OUTLANDISH_01_Claude_Reviewer_Handover_v0_1.md` | Superseded |
| 19 | `REVIEW/OUTLANDISH_REVIEW_002_Claude_to_ChatGPT.md` | **Point A findings memo** |
| 20 | `REVIEW/OUTLANDISH_01_Claude_Reviewer_Handover_v0_2.md` | Superseded by this handover |
| 21 | `REVIEW/OUTLANDISH_REVIEW_Claude_Independent_Checks_v0_1.py` | Point A evidence script |
| 22 | `REVIEW/OUTLANDISH_01_Q4h_Review_B_Brief_v0_1.md` | Point B brief |
| 23 | `OUTLANDISH_01_Q4h_*_v0_1.py` and `..._Minimal_Powerball_Test_v0_1_README.md` | Q4h v0.1 code under review at point B |
| 24 | `REVIEW/OUTLANDISH_REVIEW_003_Claude_to_ChatGPT.md` | **Point B findings memo** |
| 25 | `REVIEW/OUTLANDISH_REVIEW_Claude_Q4h_EndToEnd_Check_v0_1.py` | Point B evidence script |
| 26 | `REVIEW/OUTLANDISH_01_Claude_Reviewer_Handover_v0_3.md` (this file) | **Current handover** |

---

## 9. What comes next, and how to start

**Likely next events.**
- ChatGPT replies to memo 003 and to D1/D2. Review only what is disputed or consequential; routine implementation of K1 to K3 and the tests needs no review. If ChatGPT changes the seed formula, check only that it is deterministic, fixed in code before any REAL report, within 0 <= seed < 2**64, and recorded in each report.
- ChatGPT implements the production entry point (K1 mode switch, D2 Q5 constant), the three tests and the canaries, and updates the living file.
- Owner may authorise the read-only receipt preflight of the six real files.
- **Review point C:** final Q4, before the first Q5 REAL scan. Scope: the actual production path and entry point; the Q5 switch is off by default and cannot be bypassed by the synthetic mode; the in-scan digest test on a large fixture; the canaries; the seed rule in code; receipt preflight results if run; open limitations and compute cost. The owner then decides Q5 separately.

**If you are a new chat.**
1. Ask the owner which model is selected. Reviews of design or statistics are Fable work; flag and hold.
2. The repository is public. A sparse checkout limited to `GAIS/OUTLANDISH_01/` keeps parent-project folders off disk; the repository's top-level files still arrive and must not be opened.
3. Check whether `main` has moved past `677347b` (or this handover's own commit). If so, tell the owner the new commit and review the commit you are asked to review.
4. Read the ratified v0.2 file, the living file and memos 002 and 003 before any new code.
5. Run the two reviewer evidence scripts in `REVIEW/` at the new commit; they are quick regression checks of the shared core and of Q4h.
6. Ask the owner for any document not in the repository.
7. Write memos in the point A brief's section 8 format; US-ASCII; verified; end with a paste block for ChatGPT. The next exchange number is 004.

**End of handover.**
