# Claude checkpoint v4 - Predictive Randomness project - 28 October 2026

**Purpose:** a running checkpoint, as H-1 v1r2 section 0 item 5 asks, so no state lives only in a chat. It records events and owner decisions since H-1 v1r2 and register v0.6 were installed at `be185485693f29cf9ab28292dc6eebad00bbc32c`.
**Authority:** none. The ratified documents and the register prevail. Owner decisions listed here become authoritative when the next register edition records them.
**Author:** Claude (primary designer and coder). **Date:** 28 October 2026 (Adelaide).
**Holdout statement:** no draw outcome appears here.
**Numbering:** checkpoint v3 was a working file in Claude's own workspace and was never committed. This file follows `doc/HANDOVER/Claude_Checkpoint_v2.md`.

## 1. Where things stand

- **Current records:** H-1 v1r2, H-2 v1r3 and register v0.6, installed at `be18548` (DOC-1; verified by Claude).
- **Work in progress: E2R-1, the E_2-readiness method-generic contract specification.**
  - Under independent design review (R-3) by the ChatGPT reviewer chat. No code.
  - Latest draft: **v0.3r3**, `0a73c92d757f9adbe1e6933e95778e10e27532b31a755f2453afca9895b3a954`, in `E2R_Spec_Recheck_v0_3r3.zip` (`d198966c04fd990fa58f8d41d226f786efbe04a3cb8fa68f9f534dc1f1cf6f6c`).
  - Review history: v0.2 reviewed (3 BLOCKER, 10 CORRECTION, 2 OPTIONAL, 1 RECONSIDER; all resolved in v0.3r1). Recheck of v0.3r1: 1 BLOCKER and 4 CORRECTION, resolved in v0.3r2. Recheck of v0.3r2: 2 CORRECTION (seed roots; a version label), resolved in v0.3r3.
  - **Recheck of v0.3r3: PASS, 0 BLOCKER / 0 CORRECTION / 0 OPTIONAL / 0 RECONSIDER** (`Independent_ChatGPT_E2R_v0_3r3_Focused_Recheck_v0_1.md`, `3b69f540c637f400c503092daef9072c0069a857b9450cc91355e48e7c7d6646`). The reviewer recommends v0.3r3 for owner ratification, and requests no further design recheck. Claude agrees.
  - The reviewer counts all E2R rechecks as continuations of review 4 of 6. Claude found no reason to raise any of its REVIEWER-DECIDED items (E2R-RD-01..21) with the owner.
  - **Carried forward to the future seed-policy package (the reviewer's implementation-stage observation, not a condition):** keep a checkable, dated copy of each provisional pulse-selection rule as evidence that it was written before the pulse was published. This need not be a Git commit. A future implementation must also reject any beacon response for a different pulse, including a nearby pulse returned by a time-based query.
  - **Status:** awaiting owner ratification of v0.3r3.
- **Next:** owner ratification of the specification, then its installation with the next register edition; then NAMES-1; then the E_2-readiness code.

## 2. Owner decisions of 28 October 2026 (to be recorded in the next register edition)

E2R specification decisions (spec section 14):
- **D-1:** `track_id` excludes the method revision. A track continues across revisions, every record carries `method_revision`, and each report uses one declared revision per track (E2R-R40A).
- **D-2:** synthetic and benchmark records get the evidence tier `NOT_EVIDENCE`.
- **D-3:** the plain-English method texts (name, one-liner, explanation) are written for E_1 and E_2 in the E_2-readiness code package. Later methods' texts are written with their own specifications.
- **D-4:** `src/` holds current code only, with stable names (no version in file names), one folder per method (`src/methods/E_<nnn>/`, zero-padded locator; scientific identity stays `E_n`).
- **D-5:** a superseded revision moves to `archive/methods/E_<nnn>/r<k>/` (shared helpers to `archive/common/<name>/r<k>/`), with a README. There are no commit IDs and no stored file hashes, and there is no run-time code-identity recording. Exact historical replay is not promised.
- **D-6:** a method runs only if its active registry entry is SUPPORTED for its current revision **and** no `IN_DEVELOPMENT.txt` flag is present. Release is the owner's two deliberate actions (remove the flag; add the SUPPORTED registry entry), in a separate small package.
- **D-7:** NAMES-1, the one-off rename of existing versioned file names to stable names, comes before the E_2-readiness code, as its own HIGH-tier package with RECHECK.
- **D-8:** prospective results are shown both "as published" (revision named on each draw) and "current methods" (single revision).
- **D-9:** a seed policy's root comes from a pre-announced NIST Randomness Beacon pulse, fetched once by hand and verified independently. Runs never fetch.
- **D-10:** roots may be switched ("another universe") as a new revision or variant. Every root tried is logged and counted in reports, which is not a limit on trying.
- **D-11:** a root published after historical targets may be used for retrospective development runs, labelled as randomness chosen for the experiment. A real forecast made before a draw needs a root that is already approved.

Process decisions:
- **Oversight reporting:** Claude still checks every REVIEWER-DECIDED item. From 28 October 2026 it reports one to the owner only if Claude disagrees with it, or thinks it would interest the owner. (The owner extended the oversight instruction to six reviews on 28 October 2026; the reviewer counts the E2R rechecks as continuations of review 4.)
- **One review for handovers:** handover documents get one review only (owner, 28 October 2026).
- **Git history:** the owner does not plan to remove Git history before the code base is stable and in production. Before any clean-up, Claude records which commit IDs the register and handovers rely on.

## 3. Files to look at

- The latest E2R draft, with its exact diffs and builder scripts, inside the review ZIPs committed in `review/`.
- The reviewer's E2R reviews in `review/`:
  - `E2R_R3_Review_Commit_Independent.md` (`17087f57...b2b2`);
  - `Independent_ChatGPT_E2R_v0_3r1_Focused_Recheck_v0_1.md` (`866974a7...e392`);
  - `Independent_ChatGPT_E2R_v0_3r2_Focused_Recheck_v0_1.md` (`865edd97...def2`);
  - `Independent_ChatGPT_E2R_v0_3r3_Focused_Recheck_v0_1.md` (`3b69f540...6646`, PASS).
- `review/REVIEWER_FIX-and-PROCEED_RECHECK_PROCEDURE_v1.md` (dispositions; FIX AND PROCEED never applies to always-review code).

## 4. Gates unchanged

No real-data scientific run, holdout access, Mode H, FINAL, switch change, allowlist entry, master update, dependency upgrade, lottery-results search, Windows lifecycle or destructive test, or orphan-marker clearance by any chat. The three switches stay False and the allowlist stays empty.

*End of checkpoint v4.*
