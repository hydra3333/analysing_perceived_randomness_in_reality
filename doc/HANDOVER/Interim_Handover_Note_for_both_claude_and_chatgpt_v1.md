# Interim handover note v1 (applies to both AI handovers)

**Date:** 26 October 2026, evening (Adelaide).
**Written by:** Claude (independent reviewer), at the project owner's request. Not separately reviewed.
**Applies to:**
- `doc/HANDOVER/Claude_Reviewer_Handover_Predictive_Randomness_v9.md` (SHA-256 `1c4544ee91dea11b87c89e5cb1e9a2670d9d377026501d634c08b30da3a2dacb`);
- `doc/HANDOVER/Predictive_Randomness_ChatGPT_Coder_Handover_v1_0r1.md` (SHA-256 `07e3728476284aea82da2ef74deb606e9c9bf3fd3a84a5807816615713d04d9a`).

**Status:** INTERIM. Both handovers above **remain in force**. This note records only what has changed since they were committed at `6726963`.
- It is superseded, and may be deleted, once the full replacement handovers are committed: Claude reviewer handover **v10** and ChatGPT coder handover **v1.1**.
- If either AI chat runs out of room before those are written, a fresh chat reads the relevant handover above **plus this note**.

**Repository at writing:** `main` at `ac01678`.

---

## 1. Newly ratified (owner, 26 October 2026; committed at `ac01678`)

| File | SHA-256 (Git blob) | What it is |
|---|---|---|
| `doc/Predictive_Randomness_Method_Ranking_Measures_Proposal_v0_5.md` | `c6ca2cb2174ee2963a6fe33347820c80b92e6dd1eda518a1f0c8e3254d67ab19` | Method ranking measures ("league tables"). **Ratified, pending integration** into the governing documents. |
| `doc/HOLDOUT_EXPOSURE_RECORD_v0_2.md` | `aec833fe031b6d1d73e6acbb81757b50b193425a6899c84d438431d9df4433e2` | Supersedes v0.1. Adds item 6 (ChatGPT's unsolicited search preview) and records that the 1587 paragraph was displayed more than once. |

Proposal versions v0.2-v0.4 are in `doc/` as history. ChatGPT's three reviews are in `review/`.

**What the ranking proposal establishes** (details in the proposal itself):
- **Two modes:**
  - **walk-forward**: "honest test: trained on earlier draws only";
  - **in-sample**: "hindsight fit: trained on all draws, including the ones scored".
  - They are shown side by side, with separate rank columns, and never compete in one ranking. Every report prints these plain meanings word for word.
- **Scope:** all 9 Powerball / 7 Oz Lotto divisions. Measures MR0-MR16; MR17 onward is free for additions.
- **Significance:**
  - the sigma scale (0 wins = 0 excess sigma), with calibration labels on every figure;
  - Bonferroni over predeclared families, plus a search log;
  - the N1 fair-draw simulator: exact only for single-track hit-sequence statistics on a fixed opportunity grid, otherwise a labelled reference.
- **Supplementaries:** Oz Lotto supplementaries are used by the evaluator only, for scoring divisions, never in method inputs or predictions.
- **Rankings never feed forecasts.** Any selection rule built on them is a registered meta-method with strict N-1.
- **Timing:** no ranking code until the **E_2-readiness package** (the method-generic contract required before E_2). That package gains the stage-1 contract fields listed in proposal section 13.

---

## 2. Unchanged (unless the owner says otherwise)

- **Package 2 v0.11 (C1-C6) and its task spec P3 v0.2: no change.** The new ChatGPT coding chat proceeds with v0.11 exactly as in coder handover v1.0r1.
- All 26 October governing documents remain the current editions: Proposal v0.5, R2 v0.4, R3 v0.4, Architecture v0.7, P3 v0.2, register v0.3. So do R1 v0.4 and TIE v0.2.
- Unchanged items:
  - holdout boundaries;
  - the three switches (False);
  - Architecture 5C;
  - the E_1 goldens;
  - the masters;
  - the owner tools;
  - the coordinator.
- **No run, update, Mode H, FINAL, holdout access or destructive test is authorised.**

---

## 3. Owner's foundational points (binding on both AIs)

1. The project is **deliberately and extremely speculative**. It looks for patterns in reality that conventional statistics may have missed. No idea, method or measure is excluded because conventional statistics says it cannot work.
2. The owner **expects the most likely outcome to be that no method works** as hoped. A well-measured null result is a valid outcome.
3. **"Mark, never suppress":** every number the owner asks for is computed and shown. Where it is not a calibrated probability, it carries a plain label saying so.
4. **Statistics is an instrument for telling kinds of pattern apart, not a gate** on what may be investigated. The four pattern origins:
   - unavoidable consequence of the method;
   - effect of fitting;
   - chance, multiplicity or selection;
   - a pattern that persists on genuinely new draws.

   Strict N-1, the sealed holdout and the IS/WF separation are kept precisely so that any surprise can be tested honestly.

---

## 4. Agreed next steps (owner, 26 October 2026)

1. **Full handovers now:** ChatGPT writes coder handover **v1.1** and Claude writes reviewer handover **v10**.
   - Each is a **full** document built from its predecessor's full text, so nothing good is lost, plus everything in this note.
   - The owner commits both together. Claude verifies the commit.
2. **Integration of the ratified proposal**, as new clean editions with no addenda: R3 v0.5, R2 v0.5, Architecture v0.8 (5C untouched), Proposal v0.6, register v0.4.
   - Claude drafts, ChatGPT reviews, the owner ratifies.
   - Done during Package 2 v0.11 coding and review, and **completed before the E_2-readiness task spec is written**.
   - Until then, the ratified proposal v0.5 is the approved record.
3. **Package 2 v0.11** proceeds in the fresh ChatGPT coding chat, unchanged.
4. **After v0.11 is accepted:** the E_2-readiness task spec (method-generic contract plus stage-1 fields), then the E_1 walk-forward runs and scorer with the core ranking measures, then E_2-E_6.

*End of interim note.*
