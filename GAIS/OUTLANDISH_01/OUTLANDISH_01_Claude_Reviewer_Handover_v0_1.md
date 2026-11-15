# OUTLANDISH_01 - Claude Reviewer Handover (for the successor Claude chat)

**Version:** v0.1
**As at:** 2026-11-16 (Australia/Adelaide)
**From:** The Claude reviewer chat active 8-16 Nov 2026 (now too long to continue)
**To:** The successor Claude reviewer chat
**Supersedes:** `OUTLANDISH_01_Claude_Chat_Record_for_ChatGPT_Recovery_v0_1.md` (14 Nov). Its content is carried forward here, with later corrections applied.
**Authority:** A continuity record, not a decision document. On any conflict, these prevail, in order: the ratified spec v0.2 in the repository; the in-repo living file `OUTLANDISH_01_Living_Decisions_and_Progress.md`; ChatGPT's reviewer brief of 16 Nov. Report conflicts rather than resolving them silently.

---

## 0. What you are walking into

**Project.** OUTLANDISH_01 ("GAIS Outlandish Physical Constants Examination") is a side project of the GitHub project owner (hydra3333). It searches 10-billion-digit expansions of six mathematical constants for patterns matching historical Australian Powerball and Oz Lotto draws, as exploratory research. It is a subordinate component of the repository `hydra3333/analysing_perceived_randomness_in_reality`, confined to `GAIS/OUTLANDISH_01/`. Its methods may later be adapted into the parent project as a new method family, but only through that project's own review route.

**Roles.**
- ChatGPT (an OUTLANDISH-specific chat) is the designer and implementer.
- Claude (you) is the independent technical and scientific reviewer. Read-only by default.
- The owner relays files between chats, decides consequential matters, and alone stages, commits and pushes.

**Your first task.** Review point A from `OUTLANDISH_01_Claude_Reviewer_Brief_2026-11-16_v0_1.md`: an independent scientific and KISS ("keep it simple") audit of the Q3/Q4 implementation at commit `f42ae71ad340bb7db7b5808ac59ebc4f2009bc67`. The owner suspects the project has drifted back into over-administration (brief section 5). Section 6 below gives this chat's preliminary view, based on the brief only, before any code was read.

---

## 1. Working rules with this owner (apply throughout)

- **Model choice.** Before statistical design or validity work, root-cause investigations, or a cold-read review of a design or code before it goes to ChatGPT, say "Suggest switching to Fable (High) for this" and wait for "go". Everything else proceeds on Opus without asking. When a Fable task finishes, say so. You cannot see which model is selected, so flag and hold. The owner's Fable allowance is limited.
- **Documents for the repo:** US-ASCII, CRLF line endings, verified mechanically after writing. Filenames carry their version.
- **Never name the owner** in anything that may be committed. Use "the GitHub project owner" or hydra3333.
- **End anything to be relayed to ChatGPT with a short paste-ready block.**
- **Plain English to the owner.** Decisions as question / why / recommendation / options. Show reasoning, alternatives and uncertainties.
- **Distrust assertion.** Verify against source (file:line). Never present an owner-reported Windows test result as independently verified.
- **Simplicity over administration.** No registries, approval layers, allowlist catalogues, rule languages or ceremonies. Effort goes to correct science, correct code and meaningful tests.
- **Handovers.** At each stage, judge whether a handover update is due, and say so. Handovers are comprehensive "as at" documents.
- **Process notes.** At each substantial milestone, give a short independent note on how the process went.
- **Repository fence.** Read and write only under `GAIS/OUTLANDISH_01/`. Never read parent-project results, master histories, holdout material or the parent `exchange/` folder.

---

## 2. Current state (as at 16 Nov)

**Constants: generation finished.**
- Six immutable packed files, each 10,000,000,000 logical digits (integer digit at offset 0), 5,000,000,000 bytes, format `OUTLANDISH_PACKED_BCD_HIGH_FIRST_V1`, each with a `.wsl-receipt.json`. Owner-verified. Location `G:\OUTLANDISH_01\large_artifacts\digits\` on the owner's Ryzen 3900X.
- Constants: pi, phi, e, log2, gamma, lemniscate half-perimeter.
- Known SHA-256 values: phi `dd80be0c3fdb330fe4e1780c2d53bf03bde297a5dea83b5785cd3349838ad36d`; e `522f088b013432f775098df863b851ad87a4f5d0f0296b54cb00d6f13f72720f`; gamma `68e4a47d27759632dd8c608af973fa5bd22fb2aa7290d5e92f59e485ceb85e6a`. Others are in their receipts.
- The legacy 10^9 byte-per-digit files have since been retired, with evidence recorded (per the brief).

**Qualification stages (from ChatGPT's 16 Nov brief; owner-provided Windows results, not independently verified by Claude):**

| Stage | Status |
|---|---|
| Q1 historical reconciliation of saved phi results | PASS |
| Q2 independent reference oracle | PASS |
| Q3 packed matcher/classifier (v0.4, 4 MB chunks) | Synthetic PASS |
| Q4a-Q4g guards, processing, statistics, reporting, six-constant matrix and aggregation | Windows synthetic PASS (each) |
| Q4 production readiness | OPEN: under review now |
| Q5 qualified REAL scans | NOT AUTHORISED |
| Post-match forecasting | PARKED, unratified |

Missing for production: a qualified production runner, an approved REAL Oz Lotto adapter, and production integration sign-off.

**Repository checkpoints.**
- Review commit: `f42ae71ad340bb7db7b5808ac59ebc4f2009bc67`.
- Previous handover commit: `8cdfdb019f4425e5a427b185e5542d50cfb3c53f`.
- Q3 v0.4/Q4a commit: `39d569b`.
- Forecasting proposal commit: `c48ac3c393d2eab30014e6200d427b76d90f47ac`.

**Living file:** its section 13 predates Q4b-Q4g. ChatGPT has been asked (via the owner) to bring it up to date.

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

## 4. Ratified v0.2: Claude's summary (verify against the file)

- **Families**, each with its own index: K7 (7 mains; PB 1-35 / Oz 1-47; 14 digits), K7S (PB 7 mains + trailing PB; 16), K6S (PB 6 mains + trailing PB; 14), K6 (Oz 6 mains; 12), K7mix (Oz 6 mains + 1 supplementary in any slot; 14).
- **Role rules.** Distinctness over mains only. PB 1-20 may equal a main. P2's seventh field is a main 1-35. FIXED2 encoding; every digit offset is a possible start, including odd ones.
- **End of file.** Per-family eligibility `k + L_F <= N` via explicit masks.
- **Classification** is post-hoc. P1 = K7S AND drawn order; P2 = K7 AND drawn order; P3 = K6S; O1 = K7 AND drawn order. O2 nesting: drawn-subsequence (subset of) supplementary-last (subset of) any-slot.
- **Raw REAL events:** `draw_number, family, start_digit_offset, matched_digits` (text, leading zeros kept) + `run_manifest.json`. Sorted `(start_digit_offset, family, draw_number)`. Writer aborts on a duplicate identity.
- **Overlaps.** Same-draw overlaps computed by interval intersection. Shifted nestings include `P1_any@k => P3_any@k+2` and `O1@k => O3@k and @k+2`. PB-equals-main P2/P3 pairs (about 6 per constant). Overlaps do not change expectations. Three units always distinguished: events, distinct offsets, distinct draws.
- **REAL/NULL.**
  - Separate runs. One NULL run MAY index K decoys together (permitted, not mandated). K = 19 / 99 are benchmark defaults.
  - REAL packed input via the existing receipt (path, size, streamed SHA before completion).
  - REAL drawset fixed in the profile, with a complete integer range `[era_first, cutoff)` exactly once.
  - Fixture IDs 1-999; decoy IDs are text.
  - Drawset SHA checked against the manifest.
  - Old-scanner fixture output kept outside the REAL root.
  - `results_null\` beside `results\`.
- **Statistics.**
  - Expectation `E = D x S x (N-L+1) / 10^L`. Conditional order test `Binomial(n, q)`.
  - Empirical decoy tail `(1+b)/(K+1)`.
  - Primary W->W+1 test: P3_any (PB) / O3_any (Oz), median per-pair minimum absolute gap, tie `(abs(b-a), b-a, a, b)`, 10,000 draw-label permutations over all draws including empty ones, `(1+b)/(R+1)`, two-sided, Holm over the six constants within each game. **Owner-vetoable before qualified REAL runs.**

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

## 6. Preliminary view on the 16 Nov brief (this chat; brief only, no code read)

**Protocol (sent to ChatGPT 16 Nov).**
- Agreed:
  - The read-only reviewer.
  - `GAIS/OUTLANDISH_01/REVIEW/` with `OUTLANDISH_REVIEW_NNN_<From>_to_<To>.md`.
  - The living file as the single status record.
  - Review points A and C, plus prompt review for genuine surprises.
- Suggested:
  - Make point B optional.
  - A one-line simplicity rule: every new check must name the wrong result or data loss it prevents, or it is omitted.
  - Stop reporting refusal and test counts as progress; report what was proved.

**Likely drift, to verify in code at `f42ae71` (the brief's own section 5 hypotheses agree):**
1. **Q4g requires six NULL reports before aggregating REAL ones.** If true, this conflicts with v0.2: REAL comes first, NULL is optional and separate. Classify as a binding-spec conflict, not just KISS.
2. **Old reports refuse replay when installed code hashes differ.** Record the code hash for provenance; do not gate reading on it.
3. **Opening or verifying a report recomputes the permutations.** Ordinary loading should check digests; recomputation should be an explicit audit or reanalysis action. Quantify the cost.
4. **Seven Q4 slices with overlapping identity, path, digest, replay and manifest checks.** Likely consolidatable into: matcher; classifier/statistics core; REAL runner; NULL runner; one manifest; one reporter.
5. **Single-pass digest.** Confirm the full SHA-256 is computed in the scan's own read, not in a separate pass.

**Correctness checks the drift must not distract from** (brief section 5, items 6 and 7):
- Expectations and nesting.
- Same-draw physical overlaps.
- Signed tie order.
- Zero-match draws included in permutations.
- The two-sided p convention.
- Holm over exactly six constants within each game.
- Era/cutoff enforcement.
- Create-only run isolation.
- No way to spoof a test root as REAL.

**Response format required:** brief section 8. Findings ranked BLOCKER / IMPORTANT / MINOR / OPTIONAL, each typed scientific correctness / binding-spec conflict / operational integrity / KISS simplification, with file, function and line range, and the smallest fix. Suggested filename `OUTLANDISH_REVIEW_002_Claude_to_ChatGPT.md`.

---

## 7. Earlier non-design findings (for reference)

- **y-cruncher on Windows, 9 Nov.** Swap mode needs elevation. Since v0.8.3, swap files get a permission list of Everyone = delete only and Administrators = full access (`RawFile_Windows.ipp`, lines 130-223 and 355, at the v0.8.7.9547 commit). The rename-and-reopen therefore fails with errno 13 under a standard account. SeManageVolumePrivilege does not help. Resuming must also run elevated. The owner ran elevated, and generation is now finished.
- **Lemniscate:** the converter halves y-cruncher's full perimeter before packing.

---

## 8. Document trail

All are under `GAIS/OUTLANDISH_01/` on GitHub unless noted. Numbers 1-13 match the recovery record.

| # | Document | Status |
|---|---|---|
| 1 | `OUTLANDISH_01_Common_Matching_Engine_Claude_Review_v0_1.md` (in `OUTLANDISH_WSL/doc/`) | History |
| 2 | `OUTLANDISH_01_Common_Matching_Engine_Claude_Review_Response_v0_1.md` (`OUTLANDISH_WSL/doc/`) | History |
| 3-6 | ChatGPT reconciliations and spec candidate (old ChatGPT file library only) | History, superseded by 8 |
| 7 | `OUTLANDISH_01_Claude_Single_Review_of_Consolidated_Spec_v0_1.md` (C1-C20) | History |
| 8 | `OUTLANDISH_01_Consolidated_Matching_Reporting_Spec_v0_2_RATIFIED.md` | **Binding** |
| 9-12 | Forecasting brainstorm, Claude round 1, ChatGPT round 2, Claude round-2 reply | History |
| 13 | `OUTLANDISH_01_PostMatch_Adaptive_Forecasting_Proposed_Spec_v0_1_FOR_OWNER_REVIEW-2026.11.10.md` | Proposal, parked |
| 14 | `OUTLANDISH_01_Claude_Chat_Record_for_ChatGPT_Recovery_v0_1.md` (14 Nov) | Superseded by this handover |
| 15 | `OUTLANDISH_01_ChatGPT_Recovery_Reconciliation_20261114.md` (14 Nov) | Superseded; its corrections are folded into sections 2-5 |
| 16 | `OUTLANDISH_01_Living_Decisions_and_Progress.md` | **Operational status record** (section 13 stale until updated) |
| 17 | `OUTLANDISH_01_Claude_Reviewer_Brief_2026-11-16_v0_1.md` | **Current task brief** |

---

## 9. Before you start

1. Ask the owner which model is selected. The point-A review is Fable work.
2. Obtain read access to `hydra3333/analysing_perceived_randomness_in_reality` and check out `f42ae71`. If `main` has moved, say so and review the named commit.
3. Read the ratified v0.2 file and the living file (section 13 onwards) before the code.
4. Read only what each review question needs. Keep within `GAIS/OUTLANDISH_01/`.
5. Write the memo in brief section 8 format; US-ASCII CRLF; end with a paste block for ChatGPT.

**End of handover.**
