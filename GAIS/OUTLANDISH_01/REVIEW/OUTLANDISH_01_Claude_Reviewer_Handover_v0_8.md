# OUTLANDISH_01 - Claude Reviewer Handover (for the successor Claude chat)

**Version:** v0.8
**As at:** 2026-11-16, about 17:15 (Australia/Adelaide)
**From:** The Claude reviewer chat that started 16 Nov 2026 and completed review points A, B and C and the Q5 verification
**To:** Any successor Claude reviewer chat
**Supersedes:** `OUTLANDISH_01_Claude_Reviewer_Handover_v0_7.md` (16 Nov). All of its content is carried forward here, updated for the Q4l housekeeping, the owner's Q5 authorisation, the Powerball REAL scans and their verified null result (memo 007), and the switch reset.
**Authority:** A continuity record, not a decision document. On any conflict, these prevail, in order: the ratified spec v0.2 in the repository; the in-repo living file `OUTLANDISH_01_Living_Decisions_and_Progress.md`; ChatGPT's review briefs (points A, B and C, all 16 Nov). Report conflicts rather than resolving them silently.

---

## 0. What you are walking into

**Project.** OUTLANDISH_01 ("GAIS Outlandish Physical Constants Examination") is a side project of the GitHub project owner (hydra3333). It searches 10-billion-digit expansions of six mathematical constants for patterns matching historical Australian Powerball and Oz Lotto draws, as exploratory research. It is a subordinate component of the repository `hydra3333/analysing_perceived_randomness_in_reality`, confined to `GAIS/OUTLANDISH_01/`. Its methods may later be adapted into the parent project as a new method family, but only through that project's own review route.

**Roles.**
- ChatGPT (an OUTLANDISH-specific chat) is the designer and implementer.
- Claude (you) is the independent technical and scientific reviewer. Read-only by default.
- The owner relays files between chats and decides consequential matters.
- Commits: the owner commits ChatGPT's work. Since 16 Nov the reviewer may also commit its own review documents directly, only under `GAIS/OUTLANDISH_01/`, only when needed (section 1).

**Where things stand.** **Powerball Q5 is complete, verified and null.** On 16 Nov the owner authorised Q5 (`f939652`), scanned all six real constants (phi first; known-answer comparison 227 matched, 0 missing, 0 extra), created six reports and the REAL-only six-constant aggregate, and reset the Q5 switch to False (`8a25667`). The reviewer recomputed every report and the aggregate from the raw events with independent code: identical (memo 007, `931d119`). **Result: no constant shows consecutive-draw positional structure; every Holm-adjusted p, primary and secondary, is 1.0000; match counts sit at the random-digit expectation; zero drawn-order matches.** No review is pending. Open owner decisions are in 6.6.

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
- **Owner can run things locally.** The owner has Claude Code in VS Code and offered to run scripts there to save the reviewer's resources. Use it for anything that must run on his hardware (for example timing on the Ryzen) or that is heavy; give him one exact CMD line and the expected final line.
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
| Q4i shared Powerball production mode, single entry point, Q5 switch | Synthetic PASS | Owner Windows (Q4i 4 / 6 refusals, 4 canaries, 150,000-byte fixture); also run by Claude on Linux at `3a07e8a` |
| Full-size synthetic rehearsal (fabricated 5 GB constant) | PASS on both hosts, identical results | Claude Linux 222 s, 352 MiB; owner Ryzen Windows 363 s (13.8 packed MB/s), 301 MiB, report 2.3 s; 453 events, p = 0.1117 on both |
| Q4j pre-Q5 corrections (N1, N2, W1-W3) | Windows synthetic PASS (owner) | `103d274`; Claude confirmed history SHA-256 `c71039c6...2e54` and Q4i suite PASS (8 refusals) on Linux |
| Read-only receipt preflight, six real files | 6 of 6 PASS (owner, Windows) | ChatGPT reports full-file hashes match the 14 Nov record; Claude has not yet seen the printed lines |
| D4 primary statistic and D5 disclosure (Q4k) | Implemented and checked; Windows synthetic PASS (owner) | `b5f2ada`; memo 006 (`d036859`): no correction; reviewer end-to-end v0.2 identical on owner Windows and reviewer Linux |
| Q4 production readiness | COMPLETE | Q4l housekeeping (`826b045`): living file 17 records D4/D5; phi known-answer comparator |
| Q5 Powerball REAL scans | **COMPLETE, VERIFIED, NULL** | Authorised `f939652`; six scans, six reports, aggregate `REAL_AGGREGATE_powerball_q5_v1`; switch reset False `8a25667`; memo 007 |
| Post-match forecasting | PARKED, unratified | |

Results location: `G:\OUTLANDISH_01\large_artifacts\results\REAL_<constant>_q5_v1\` and `...\REAL_AGGREGATE_powerball_q5_v1\` on the owner's Ryzen only (under 1 MB in total); not yet committed to the repository (owner decision, 6.6). Oz Lotto remains blocked on its approved file, era and cutoff.

**Repository checkpoints.**
- `main` when this handover was written: `8a25667` (owner's switch reset to False). This handover is committed on top of it.
- Reviewer memo 007 and recomputation script: `931d119`. Q5 authorisation: `f939652` (code checkpoint `826b045`). Q4l: `826b045`. Handover v0.7: `4b1faac`.
- Q4k (D4/D5 implementation): `b5f2ada`. Handover v0.6: `ca81aeb`.
- Q4j corrections: `103d274`. Ryzen rehearsal recorded in the living file: `43a8a25`. Handover v0.4: `4ec1707`.
- Review C memo and rehearsal script: `d515cd4`. Review C brief and living-file section 15: `0e69b5e` (`148d62d` for section 15 text).
- Q4i scientific code reviewed at point C: `3a07e8aba15cb159e7e0cfc35e41a46bd5558833`.
- Handover v0.3: `dd9b68c`. Point B memo: `677347b`.
- Point B review commit: `b7ce6fd052d65186b7e4d338260aebf054188e45` (Q4h v0.1 and the point B brief).
- Living file recording Review A disposition: `bbdf3f4`.
- Point A review commit: `f42ae71ad340bb7db7b5808ac59ebc4f2009bc67`.
- Earlier handover commit: `8cdfdb019f4425e5a427b185e5542d50cfb3c53f`.
- Q3 v0.4/Q4a commit: `39d569b`.
- Forecasting proposal commit: `c48ac3c393d2eab30014e6200d427b76d90f47ac`.

**Living file:** section 15 (Q4h/Q4i, Review B disposition, D1/D2) and section 16 (Review C, D3, N1/N2, W1 to W5, remaining owner decisions) are both current and checked by the reviewer as accurate (`0e69b5e`, `0f7c6e2`). Section 16 does not yet record the owner's Ryzen rehearsal result; a short paste for ChatGPT was given. Updating it is ChatGPT's job, not the reviewer's.

**Review exchanges so far.**

| # | Document | State |
|---|---|---|
| 001 | ChatGPT's point A brief, `REVIEW/OUTLANDISH_01_Claude_Reviewer_Brief_2026-11-16_v0_1.md` | Committed by the owner (`a333990`). |
| 002 | `REVIEW/OUTLANDISH_REVIEW_002_Claude_to_ChatGPT.md` (point A) | Committed by the owner (`a333990`); relayed; accepted by ChatGPT (living file 14.5). |
| - | `REVIEW/OUTLANDISH_REVIEW_Claude_Independent_Checks_v0_1.py` (point A evidence) | Committed by the owner (`fde9fe3`). |
| - | ChatGPT's point B brief, `REVIEW/OUTLANDISH_01_Q4h_Review_B_Brief_v0_1.md` | Committed by ChatGPT/owner (`b7ce6fd`). Unnumbered. |
| 003 | `REVIEW/OUTLANDISH_REVIEW_003_Claude_to_ChatGPT.md` (point B) | Committed by the reviewer (`677347b`); accepted by ChatGPT with D1/D2 (living file section 15). |
| - | `REVIEW/OUTLANDISH_REVIEW_Claude_Q4h_EndToEnd_Check_v0_1.py` (point B evidence) | Committed by the reviewer (`677347b`). |
| - | ChatGPT's point C brief, `REVIEW/OUTLANDISH_01_Q4i_Review_C_Brief_v0_1.md` | Committed (`0e69b5e`). |
| 004 | `REVIEW/OUTLANDISH_REVIEW_004_Claude_to_ChatGPT.md` (point C) | Committed by the reviewer (`d515cd4`); read by ChatGPT, which recorded it in living file section 16 (`0f7c6e2`). |
| - | `REVIEW/OUTLANDISH_REVIEW_Claude_FullSize_Rehearsal_v0_1.py` (point C evidence) | Committed by the reviewer (`d515cd4`); run by the owner on the Ryzen, PASS. |
| 005 | `REVIEW/OUTLANDISH_REVIEW_005_Claude_to_ChatGPT.md` (primary statistic) | Committed by the reviewer (`8b7eaa2`); implemented in Q4k. |
| - | `REVIEW/OUTLANDISH_REVIEW_Claude_Primary_Statistic_Simulation_v0_1.py` (memo 005 evidence) | Committed by the reviewer (`8b7eaa2`). |
| 006 | `REVIEW/OUTLANDISH_REVIEW_006_Claude_to_ChatGPT.md` (Q4k focused check) | Committed by the reviewer (`d036859`). |
| 007 | `REVIEW/OUTLANDISH_REVIEW_007_Claude_to_ChatGPT.md` (Q5 results) | Committed by the reviewer (`931d119`). |
| - | `REVIEW/OUTLANDISH_REVIEW_Claude_Q5_Powerball_Recompute_v0_1.py` (memo 007 evidence) | Committed by the reviewer (`931d119`). Reads genuine results and history; run only on authorised Q5 output. |
| - | `REVIEW/OUTLANDISH_REVIEW_Claude_Q4h_EndToEnd_Check_v0_2.py` (memo 006 evidence) | Committed by the reviewer (`d036859`); owner Windows run identical to reviewer Linux. Supersedes v0.1 from `b5f2ada` onward. |

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
16. **D1 seed rule (16 Nov, ChatGPT agreed):** primary permutation seed = first 8 bytes, big-endian, of SHA-256 of ASCII `OUTLANDISH_01|<game>|<constant>|PRIMARY_W_TO_W1|V1`. Known case: powerball/pi -> `7cfcc54fcaf4f97f` = 9006290301332289919. R = 10,000. Synthetic regressions keep 271828.
17. **D2 Q5 switch (16 Nov, ChatGPT agreed):** `ENABLE_Q5_PRODUCTION_SCANS = False` in `OUTLANDISH_01_Q4i_Production_Entry_v0_1.py`; the runner checks it before any source or history access. An owner Git commit setting it True, naming the code commit and scope, is the Q5 authorisation record. Guards against accidents, not tampering.
18. **D3 REAL/NULL scope (16 Nov, ChatGPT agreed; living file 16):** for Powerball Q5, the production NULL scan entry point listed in v0.2 B7 Q4 is deferred; it must be implemented and reviewed before any NULL run or any REAL-vs-NULL comparison is reported. REAL/NULL isolation, match definitions and the primary statistic are unchanged; the REAL path must keep refusing NULL-typed and decoy inputs (test W2).
19. **D4 Powerball primary statistic (16 Nov, owner; passed to ChatGPT):** primary = mean over evaluable P3_any adjacent pairs of `log10(g + 1)` (log of the geometric mean of the per-pair minimum absolute gap g); pre-declared secondary = median of g (the former primary), exploratory, own six-constant Holm family. Everything else in v0.2 B5.4 unchanged (events, pairs, gaps, whole-draw-set permutation with empties, R = 10,000, D1 seeds, centred two-sided p, N/A rule, Holm over six constants). Implementation: one permutation loop for both; `math.fsum` over sorted gaps, rounded to 12 decimal places, so results stay byte-identical across hosts. Reason: memo 005 (median nearly blind to sparse effects; geometric mean equal or better everywhere tried). Oz primary not decided; simulate Oz separately when in scope. The owner explicitly rejected keeping a weaker test merely because it was coded first.
20. **D5 legacy-data exposure (16 Nov, owner; ChatGPT agreed; to be recorded in the living file before the Q5 commit):**
   - **Freeze:** nobody computes any W->W+1 or consecutive-draw statistic from saved legacy phi or pi match rows until the qualified REAL Q5 reports exist. Covers the G: phi 10^10 run (227 P3 rows) and the committed `OUTLANDISH_01_results/run_20261105_*` files (phi and pi, 10^6 and 10^9 prefixes).
   - **Known-answer exception:** the first REAL phi scan may be compared with the saved 227 rows as an exact set comparison of (draw, start offset, matched digits), outputting only counts of matched, missing and extra rows and the list of differing rows. No offset differences, gaps, summaries or tests.
   - **Disclosure:** one fixed field, identical text, in each REAL report and the six-constant aggregate (text in 6.4).
   - **No exclusion or re-analysis:** all six constants stay in both Holm families; no phi/pi exclusion, special threshold or post-hoc correction. P1/P2 counts, expectations and matching rules unchanged.
   - **The freeze has now lifted**, because the qualified REAL reports exist (16 Nov).
21. **Q5 Powerball authorisation (16 Nov, owner commit `f939652`):** REAL scans of the six constants, code `826b045`, D4 primary, D5 disclosure, phi first with known-answer comparison. Completed the same day; switch reset to False (`8a25667`). Any further REAL scan needs a new owner authorisation commit.

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

The committed memo 003 still lists D1/D2 as pending; it is the record of what was advised. ChatGPT agreed both; they are recorded in living file section 15 and in section 3 above.

---

### 6.3 Review point C (16 Nov, code `3a07e8a`, record `0e69b5e`, Q4i v0.1)

**What was reviewed.** `OUTLANDISH_01_Q4i_Mode_v0_1.py` (one immutable `PowerballMode`, two constructors), `OUTLANDISH_01_Q4i_Production_Entry_v0_1.py` (single entry: status, scan, report, aggregate; the switch), the three Q4h modules modified in place (runner, report, aggregate), `OUTLANDISH_01_Q4i_Targeted_Qualification_v0_1.py`, the brief and living file section 15.

**Verdict (b):** ready for owner consideration of Q5, subject to N1 and N2 and the D3 decision (since made). No blocker.

**What Claude did.**
- Ran entry `status` (DISABLED) and `scan` (refused), Q4h and Q4i suites, and both earlier reviewer scripts: all PASS on Linux.
- Confirmed the D1 known seed independently; all twelve seeds distinct and below 2^64.
- Scratch-copy checks with a fabricated history (not committed): five NULL-shaped inputs refused by the REAL-path loader; N/A constants keep the Holm family at six; Q4i tests fail if the switch is True (the N2 finding); production mode emulated on Linux with the switch False refused both scan routes with zero source validations, zero history reads and an empty results folder; six forged mode/run-identifier combinations refused; production seed and receipt-preflight branches executed correctly.
- Wrote and committed `REVIEW/OUTLANDISH_REVIEW_Claude_FullSize_Rehearsal_v0_1.py`: one fabricated production-size constant (9,999,999,999 digits, 5,000,000,000 bytes) through the committed path in synthetic mode against 433 fabricated draws. Planted hits at offset 1, across 2^32, across a chunk boundary, at 2^33 - 1 and at the last valid starts were found; all reported events were re-read and rule-checked; chance counts K6S 222, K7 221, K7S 1 against expected 218, 218, 2. Needs about 6 GB scratch outside `G:\OUTLANDISH_01`; removes its sandbox.
- **Owner ran it on the Ryzen** (Windows, `T:\TEMP`): PASS, 363 s (13.8 packed MB/s), 301 MiB, report 2.3 s, results identical to Claude's Linux run (453 events, p = 0.1117). So the scan and statistics give the same answers on both platforms, and Q5 on the Ryzen is about 6 minutes per constant, about 36 minutes for six. The i5 is unmeasured.

**Findings in memo 004.**

| ID | Class | Summary |
|---|---|---|
| N1 | Important, before first REAL scan | The history file's digest depends on git line-ending settings; a re-clone or setting change would make every REAL run refuse to load. Fix: `GAIS/OUTLANDISH_01/.gitattributes` with `POWERBALL_preholdout_only.csv -text`, refresh the file, expect SHA-256 `c71039c6...2e54` everywhere. Must precede the first REAL scan. |
| N2 | Important, before Q5 authorisation | Q4i qualification lines 40 and 54-56 require the committed switch False, so the suite breaks once Q5 is authorised. Fix: set it False in memory inside the test. |
| W1 | Worthwhile | Read-only `preflight` action in the entry (no switch; owner go-ahead to run). |
| W2 | Worthwhile | One test: the REAL path refuses a decoy text identifier and a NULL-typed manifest. |
| W3 | Worthwhile | One Windows test with a real production mode object and zero source/history calls. |
| W4 | Done | Owner ran the full-size rehearsal on the Ryzen (above). |
| W5 | Procedure | Scan phi first and compare its K6S rows with the saved 227 P3 rows (known-answer check); name code commit and scope in the switch commit. |
| O1-O4 | Optional | Production code in `..._Q4h_..._Test_..._v0_1.py` files edited in place; compatibility wrappers; a canary that cannot fail; Review B O1/O2 still deferred. |

Not to add: a NULL framework before needed, resume/parallel scanning, switch tamper-proofing, registries, a second 433-draw test, Q4a-Q4g migration.

**Disposition.** ChatGPT recorded the verdict, N1/N2, W1-W5 and D3 accurately in living file section 16 (`0f7c6e2`), and states no further routine review round is needed.

### 6.4 After review C: preflight and primary statistic (16 Nov)

**Q4j (`103d274`).** ChatGPT implemented N1 (`GAIS/OUTLANDISH_01/.gitattributes` with `POWERBALL_preholdout_only.csv -text`), N2 (Q4i tests force the switch False in memory), W1 (entry action `preflight --constant <name>`, read-only, before the switch check, does not read history), W2 and W3. Claude checked: history SHA-256 `c71039c63f64479b2d83c10e8df3ad5e7525091b3a7f44c5a2680015f4fd2e54`; Q4i `--run` PASS on Linux with 8 refusals; the preflight path and guard code only open files for reading.

**Receipt preflight.** Owner-authorised and run on Windows, one constant at a time: 6 of 6 PASS, all files 5,000,000,000 bytes. ChatGPT compared the printed full-file SHA-256 values with the 14 Nov record (section 2 table): 6 of 6 exact matches. Claude offered an independent comparison and has not yet received the six printed lines. The full 30 GB integrity check remains inside each scan, as designed and tested at review C.

**Primary statistic (memo 005, D4).** Claude's advice ran in two steps, both on Fable:
- First advice was option A+: keep the median primary and pre-declare the geometric mean as secondary, mainly to avoid implementation cost.
- The owner challenged keeping a weaker test because it was coded first. A further simulation of broad effects found no case where the median beat the geometric mean, so Claude changed the recommendation to option B. The owner accepted B.
- Key figures (per constant, Holm threshold 0.05/6): false alarms 0.7% for both (600 sets, nominal 0.83%); about 9 pairs planted within 1,000,000 digits, median 2% against geometric 99%; broad 34 pairs within 10^9, 96.2% against 97.0%; broad 17 pairs, 30.0% against 48.2%.
- About 68 of 432 adjacent pairs are evaluable per constant.
- Two equal primaries (Holm over 12) were rejected: the median adds almost nothing alongside the geometric mean.
- Evidence script: `REVIEW/OUTLANDISH_REVIEW_Claude_Primary_Statistic_Simulation_v0_1.py` (simulated data only, no project code; quick mode about 1 minute, `--full` 30 to 60 minutes).

**Also noted for the owner before Q5.** With six constants and no effect, the chance that at least one RAW p-value falls below 0.05 is about 26%; the Holm-adjusted values are the ones to read.

**Phi/pi blindness, resolved as D5.**
- ChatGPT's assessment: outcome-blind with respect to the chosen P3->P3 test on the available records, but phi match events and smaller examples had been inspected, and private calculations cannot be ruled out.
- The committed legacy runs (`OUTLANDISH_01_results/run_20261105_223116` for 10^6, `run_20261105_231343` for 10^9) hold phi and pi match rows and transition files. Their delta columns are blank, because the old tool measured only from P1 matches (`OUTLANDISH_WSL/wsl_scan_packed_powerball.py`, `closest_pair` from P1 positions).
- **Correction to an earlier reviewer statement.** Claude first told the owner that no P3->P3 distance was ever printed. That was wrong: it had checked only the CSV files. `OUTLANDISH_01_2026-11-05_Historical_Status_and_Draft_Spec_v0_1.md` section 5.2 records hand-computed signed P3->P3 gaps for the five adjacent draw pairs with P3 matches in the 10^9 prefixes: pi 1195->1196, 1470->1471, 1490->1491; phi 1233->1234, 1552->1553. They range from about 67 million to 799 million digits, none small. ChatGPT's first disclosure draft repeated the error and was corrected.
- No median, geometric-mean or permutation test over P3->P3 gaps appears in any project record. Claude had not read that document when recommending D4, which rests on simulation only. D4 therefore keeps its pre-declared status, and D5 adds no test, so there is no multiplicity issue.
- **Never compute anything from those five gaps, or from any legacy rows, before the REAL reports exist** (the D5 freeze).

**D5 disclosure text (fixed, identical in each REAL report and the aggregate):**

> Before the Powerball primary statistic was fixed, legacy match rows had been examined for phi (full 10^10 digits, 227 P3 rows) and for pi and phi (first 10^9 digits). On 5 November 2026 the signed P3->P3 gaps for the five adjacent draw pairs having P3 matches in those 10^9 prefixes (pi 3, phi 2) were computed and recorded in `OUTLANDISH_01_2026-11-05_Historical_Status_and_Draft_Spec_v0_1.md` section 5.2. No median, geometric-mean or permutation test of P3->P3 gaps appears in the reviewed project record. The D4 primary statistic was chosen on simulation evidence (`REVIEW/OUTLANDISH_REVIEW_005_Claude_to_ChatGPT.md`) without reference to these values. These exposures are disclosed; results are not represented as wholly blind.

### 6.5 Focused check of Q4k (16 Nov, commit `b5f2ada`, memo 006)

**What changed in Q4k.** Six files: the Q4d statistics core, the Q4h report and aggregate modules, the Q4h qualification, a new `OUTLANDISH_01_Q4k_D4_Statistics_Qualification_v0_1.py` and a README. The matcher, runner, events module, mode and entry point are unchanged, so the scan path is as reviewed at point C.

**Verdict:** D4 and D5 implemented correctly; no correction required.

**Checked (line numbers at `b5f2ada`):**
- `geometric_mean_log_gap` (Q4d 226-237): mean of `log10(g + 1)`, `fsum` over sorted gaps, rounded to 12 places; N/A on empty input.
- `permutation_test(..., geometric_primary=True)` (Q4d 282 onward): one shuffle loop for both statistics; a trial counts for both or neither (assertion at 339-340); centre rounded to 12 places before tail comparisons (351); same centred two-sided p and N/A rule.
- The median path is byte-identical: the reviewer's recomputed median values match the pre-Q4k ones exactly.
- Oz callers keep the median-only default (`geometric_primary=False`).
- Report schema V3 (report 25-34, 77-81, 124-142) and aggregate schema V3 (aggregate 63-73, 114) record primary and secondary names and the exact D5 text; both loaders refuse mismatches. The aggregate gives two separate six-constant Holm families.
- No code reads legacy result files.

**Reviewer evidence.** `REVIEW/OUTLANDISH_REVIEW_Claude_Q4h_EndToEnd_Check_v0_2.py` recomputes both statistics independently from the same 10,000 shuffles for six fabricated constants and 433 fabricated draws. It checks observed values, centres, p-values, tails, both Holm families, the D5 text against an independent copy, the positive control (primary p 0.0001, Holm 0.0006), audit and corruption refusal. It holds the reviewer's exact Linux values and prints whether a run matches them. **Owner Windows run: identical** ("identical to the reviewer's Linux values: yes"). The log10 path, the one place the platforms could have differed, gives bit-identical results.

v0.1 of the end-to-end check now stops at the aggregate on current code, by design: it tested the median as primary. It remains evidence for `b7ce6fd` to `103d274`.

**Optional, noted to ChatGPT.** In a report's `permutation` block, the top-level `centered_two_sided_p` and `observed_median` are now the SECONDARY (median) result, kept for compatibility; the headline primary is `permutation.geometric_primary.centered_two_sided_p`. The legacy top-level fields can be dropped later. **When reading a REAL report, read the primary from `geometric_primary`.**

### 6.6 Powerball Q5: run, verification and result (16 Nov)

**Run (owner, Ryzen, Windows).** Run IDs `REAL_<constant>_q5_v1`, aggregate `REAL_AGGREGATE_powerball_q5_v1`, all under `G:\OUTLANDISH_01\large_artifacts\results\`. Each scan took about 6.3 minutes with 4,000,000-byte chunks. Phi first; the Q4l known-answer comparison gave matched 227, missing 0, extra 0. Then pi, e, log2, gamma, lemniscate, six reports and the aggregate. No errors or refusals.

**Verification (memo 007, reviewer, on a copy of the owner's results).** `REVIEW/OUTLANDISH_REVIEW_Claude_Q5_Powerball_Recompute_v0_1.py` uses none of the project's matching, classification or statistics modules. All identical:
- Identity: manifests COMPLETE and REAL; 10^10 digits; 5,000,000,000 bytes hashed; in-scan source SHA-256 equals the 14 Nov record for all six; pinned history SHA-256; event, report and aggregate digests; D1 seeds; 10,000 permutations; D4 names; D5 text; recorded code hashes equal the committed files at `f939652`.
- Soundness: all 2,659 events satisfy their family rule against the genuine draw they are attributed to.
- Statistics: category counts, evaluable pairs, both statistics with centres, p-values and tails, and both Holm families.
- Completeness cannot be checked without the constants; the evidence is the phi known-answer result, the rehearsal and counts at expectation.

**Result (expected per constant under random digits: P3_any 218.2, P2_any 218.2, P1_any 2.18).**

| Constant | P1 any | P2 any | P3 any | Pairs | Primary raw p | Primary Holm | Secondary raw p | Secondary Holm |
|---|---|---|---|---|---|---|---|---|
| pi | 2 | 215 | 233 | 71 | 0.2914 | 1.0000 | 0.6487 | 1.0000 |
| phi | 3 | 208 | 227 | 62 | 0.3710 | 1.0000 | 0.8941 | 1.0000 |
| e | 2 | 232 | 228 | 69 | 0.5623 | 1.0000 | 0.5392 | 1.0000 |
| log2 | 2 | 189 | 227 | 72 | 0.2373 | 1.0000 | 0.4383 | 1.0000 |
| gamma | 1 | 198 | 227 | 63 | 0.6747 | 1.0000 | 0.8171 | 1.0000 |
| lemniscate | 0 | 245 | 220 | 67 | 0.3711 | 1.0000 | 0.3640 | 1.0000 |

- Totals: P3_any 1,362 and P2_any 1,287 against 1,309 expected each; P1_any 10 against 13.1; drawn-order matches 0 against about 2.1 expected.
- Smallest adjacent-pair gap 26,289,307 digits (pi); none within 10^7; 13 pairs within 10^8 across the six, about 13 expected.
- Reading: null. The test would very probably have detected about five or more near-coincidences within a million digits, or a broad shift across a third of the pairs (memo 005). It does not rule out other kinds of structure and gives no support for prediction.

**Open owner decisions (raised in memo 007).**
1. Commit a copy of the seven result folders (under 1 MB) under `GAIS/OUTLANDISH_01/`. The reviewer offered to do it from the zip the owner supplied.
2. Any further exploratory analysis of these events: allowed if labelled and with comparisons stated; the reviewer recommends writing it down before running it.
3. NULL decoy runs: the reviewer recommends not building the NULL entry point now.
4. Oz Lotto: approved file, era and cutoff still missing; its primary needs its own simulation.
5. Forecasting: remains parked unless the owner unparks it; these results give no positional structure to build on.

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
| 26 | `REVIEW/OUTLANDISH_01_Claude_Reviewer_Handover_v0_3.md` | Superseded by this handover |
| 27 | `OUTLANDISH_01_Q4i_*_v0_1.py`, `..._Q4i_Shared_Powerball_Mode_v0_1_README.md`, modified Q4h modules | Q4i code reviewed at point C (`3a07e8a`) |
| 28 | `REVIEW/OUTLANDISH_01_Q4i_Review_C_Brief_v0_1.md` | Point C brief |
| 29 | `REVIEW/OUTLANDISH_REVIEW_004_Claude_to_ChatGPT.md` | **Point C findings memo** |
| 30 | `REVIEW/OUTLANDISH_REVIEW_Claude_FullSize_Rehearsal_v0_1.py` | Point C evidence script; owner Ryzen PASS |
| 31 | `REVIEW/OUTLANDISH_01_Claude_Reviewer_Handover_v0_4.md` | Superseded by this handover |
| 32 | `GAIS/OUTLANDISH_01/.gitattributes`, Q4j changes to the entry and Q4i tests | Q4j corrections (`103d274`) |
| 33 | `REVIEW/OUTLANDISH_REVIEW_005_Claude_to_ChatGPT.md` | **Primary statistic memo (D4)** |
| 34 | `REVIEW/OUTLANDISH_REVIEW_Claude_Primary_Statistic_Simulation_v0_1.py` | Memo 005 evidence script |
| 35 | `REVIEW/OUTLANDISH_01_Claude_Reviewer_Handover_v0_5.md` | Superseded by this handover |
| 36 | `OUTLANDISH_01_2026-11-05_Historical_Status_and_Draft_Spec_v0_1.md` section 5.2 | Legacy record of five hand-computed P3->P3 gaps (D5 disclosure) |
| 37 | `REVIEW/OUTLANDISH_01_Claude_Reviewer_Handover_v0_6.md` | Superseded by this handover |
| 38 | Q4k: `OUTLANDISH_01_Q4k_D4_Statistics_Qualification_v0_1.py`, `OUTLANDISH_01_Q4k_D4_D5_Implementation_README_v0_1.md`, changes to Q4d, Q4h report/aggregate/qualification | D4/D5 implementation (`b5f2ada`) |
| 39 | `REVIEW/OUTLANDISH_REVIEW_006_Claude_to_ChatGPT.md` | **Q4k focused check memo** |
| 40 | `REVIEW/OUTLANDISH_REVIEW_Claude_Q4h_EndToEnd_Check_v0_2.py` | Memo 006 evidence; current end-to-end check |
| 41 | `REVIEW/OUTLANDISH_01_Claude_Reviewer_Handover_v0_7.md` | Superseded by this handover |
| 42 | `OUTLANDISH_01_Q4l_Phi_Known_Answer_Compare_v0_1.py`, `OUTLANDISH_01_Q4l_PreQ5_Housekeeping_README_v0_1.md` | Q4l (`826b045`) |
| 43 | `REVIEW/OUTLANDISH_REVIEW_007_Claude_to_ChatGPT.md` | **Q5 results memo** |
| 44 | `REVIEW/OUTLANDISH_REVIEW_Claude_Q5_Powerball_Recompute_v0_1.py` | Memo 007 evidence |
| 45 | `REVIEW/OUTLANDISH_01_Claude_Reviewer_Handover_v0_8.md` (this file) | **Current handover** |

---

## 9. What comes next, and how to start

**Likely next events.**
- Powerball Q5 is complete; no review is pending. ChatGPT should record Q5 and memo 007 in the living file.
- The owner decides the items in 6.6. If asked to commit the results, place an exact copy of the seven folders under a clearly named folder in `GAIS/OUTLANDISH_01/`, verify every digest after copying, and never alter the files.
- Any further analysis on these REAL events is exploratory: insist it is written down first (what, which statistic, how many comparisons), labelled exploratory, and never reported as confirming anything.
- Oz: when its approved file and bounds arrive, simulate the Oz regime (about 50 events per draw) before choosing its primary, then follow the same path (adapter, qualification, preflight, owner authorisation).
- Any new REAL scan needs a new owner authorisation commit; the switch is False.

**If you are a new chat.**
1. Ask the owner which model is selected. Reviews of design or statistics are Fable work; flag and hold.
2. The repository is public. A sparse checkout limited to `GAIS/OUTLANDISH_01/` keeps parent-project folders off disk; the repository's top-level files still arrive and must not be opened.
3. Check whether `main` has moved past this handover's own commit. If so, tell the owner the new commit and review the commit you are asked to review.
4. Read the ratified v0.2 file, the living file (sections 14 to 16 at least) and memos 002, 003 and 004 before any new code.
5. Run the reviewer evidence scripts in `REVIEW/` at the new commit as quick regression checks: the independent checks (core), the Q4h end-to-end check **v0.2** (433 draws; prints whether results match the reviewer's Linux values), and, only if the scan path changed, the full-size rehearsal (about 4 to 6 minutes, 6 GB scratch).
6. Ask the owner for any document not in the repository.
7. Write memos in the point A brief's section 8 format; US-ASCII; verified; end with a paste block for ChatGPT. The next exchange number is 008.

**End of handover.**
