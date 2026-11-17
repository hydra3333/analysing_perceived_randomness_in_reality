# The owner's clarified research model of 18 November 2026: what it changes in the ratified MHUP-B documents

**Status: RECORD OF THE OWNER'S DIRECTION** (decision log entry 84), as set out by the reviewer in EX_234 and EX_235 from
the owner's conversation with it, and confirmed by the owner to Claude on 18 November 2026 (09:34, 09:36 and 09:41
Australia/Adelaide). EX_235 is the latest statement; EX_233 and EX_234 stay in force where it does not supersede them.
This page is the short change note that EX_234 section 0 and EX_235 section 4 ask for. It creates no new approval
step. The ratified files are not edited: the amendments travel with the integrated package's document changes
(code plan v0.3 section 11) and are ratified with it in the ordinary way.

## 1. The model, in the owner's terms

1. **All draws are equal research targets.** The former holdout draws (Powerball 1577 to 1586, Oz Lotto 1694 to 1703) are
   ordinary draws for walk-forward forecasting, scoring and rankings.
2. **The sealed Mode H study is an archive.** It is kept, read-only and unaltered, as separate history. Its seal is not a
   permission gate in any normal workflow, and its scores are never summed again into ordinary scores.
3. **Every method version is a legitimate subject.** A modified method is a new immutable scientific identity. The
   earlier version's forecasts, scores and published rankings stay. Each version is walked forward from its earliest
   eligible draw and ranked separately. Archived code is not run unless an installed, runnable revision exists.
4. **Catch-up is the same walk-forward.** Draws accepted together are processed one target at a time, each from the
   prefix to N-1 only. Evidence labels differ (historical, catch-up, prospective); the computing and the ordinary
   scores do not.
5. **Two clearly labelled OV-1 uses.** (A) The registered formal prospective test: one per game, bar 40, unchanged.
   (B) A retrospective OV-1-style walk-forward diagnostic over history and method versions: descriptive; 40 may be
   drawn as a reference line; no P value, no 2.5% claim; never written to the formal ledger.
6. **Bar 40 is kept.** 5% for the programme, 2.5% a game; by Ville's inequality the bar is 1 / 0.025 = 40.
7. **Science, methods, calculations, scoring and reporting must be right; engineering is proportionate**
   (`WORKING_PRINCIPLE_2026_11_18_MAIN_GAME_PRIORITY.md`).

## 2. What changes in the ratified text

| Where | Ratified text | Now |
|---|---|---|
| Supplement v0.8 section 6.7 | Elsewhere, only retrospective Z values, with no evidence score; nothing of OV-1 for the holdout draws by default | Use (B) above is an approved report view, over all eligible history, the former holdout draws included; labelled "OV-1 RETROSPECTIVE WALK-FORWARD - DESCRIPTIVE, NOT FORMAL PROSPECTIVE" in the text and in the machine-readable headings; implemented in layer L7 (slice 3) |
| Supplement v0.8 section 7.2 rules 1 and 2 | The development cap stays at the Phase 1 cap until the game's `MODE_H_SEALED` record exists; after it the cap is `holdout_last` | One rule: every draw up to `holdout_last` is an ordinary historical draw for a development batch and its report. No record of the Mode H study is a condition |
| Supplement v0.8 section 7.2 rule 3; section 7.1 (b) | Wording that makes the holdout targets a special case allowed after the seal | No special case. The sealed records stay exactly as they are, as separate history |
| Supplement v0.8 section 7.2 rule 2A | Above the holdout: only targets with a weekly freeze line; a routine fill only if frozen before the release instant | UNCHANGED. This is the weekly session's own rule, not a Mode H rule |
| Supplement v0.8 section 6.8; code plan v0.3 L5 | The eligibility line is "durable before C(T)" | Made exact (EX_233 S2-F02): the registration and every eligibility line count only with a CONFIRMED line whose time was read after the record was read back and is before the record's limit; otherwise the stream stops. One more kind of line in the OV-1 ledger |
| Code plan v0.3 L6 (the `DEV_BATCH` gate; the report tool; the outcome reader) | "for a target at or above `holdout_first`, the opening record and the game's `MODE_H_SEALED`" | Removed. The weekly freeze-line conditions for targets above `holdout_last` stay |
| Code plan v0.3 L7 | OV-1 as one part of the report | Two labelled parts: (A) formal, from the OV-1 ledger; (B) retrospective, computed by the same kernel as a derived report with a reproducible cohort, window and input identity. No new formal test, registry or error allocation |
| Design v0.1r7 section 6.7 as slice 1 read it (EX_230 F-230-A) | The weekly readiness check believed a developed record only if it named the game's sealed Mode H score | The developed record is the owner's declaration: well formed, with his fixed sentence. The archive is not consulted |

## 3. What does not change

- Method-facing N-1 isolation; forecast identities; create-only and append-only evidence; no duplicate scoring keys.
- The official source and the owner's updater; the master's version rules; nothing runs on the owner's PC without his go.
- The formal OV-1 test: per game, registered before its first draw, six lambdas with equal weights, the exact
  fair-draw distribution, certified factors, counted / skipped / missed / stop, a stopped stream stays stopped.
- The Mode H study's own tools and readers, which still validate that archive when they read it.
- Plans of the first kind (`WF_BATCH_PLAN_V1`) and their recorded attempts: immutable history.
- Left as installed, because they are validated code with no effect on the real project (both opening records and both
  seals exist and are never altered): the installed reader's condition that a target at or above the former holdout
  needs the game's opening record, and the owner's diagnostic route's conditions (opening record and seal) for such a
  target. They can be removed with the integrated package if the owner or the reviewer wants that.
