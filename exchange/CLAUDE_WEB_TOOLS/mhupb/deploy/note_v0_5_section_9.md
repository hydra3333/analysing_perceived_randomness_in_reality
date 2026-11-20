## 9. OV-1 after a restore: no special rule, and a plain statement of what a replay gives (EX_253; EX_255 E04)

v0.3's section 9 answered a problem of the ratified rule: OV-1's formal stream counted only forecasts frozen before
their draw by the clock, so a draw counted before a restore could come back as "missed". It proposed restore notices, a
new stop cause and a refusal of a second registration.

The owner has since directed that OV-1 be simplified to one prevailing score per game (EX_253), and the amendment sent
with this note (`ov1_simplify/MHUPB_OV1_SIMPLIFICATION_AMENDMENT_DRAFT_v0_2.md`) proposes the rule: a variant counts at
a draw from the first-draw number in its release record, if it forecast that draw under N-1 isolation, whether before
the draw or afterwards by catch-up. Under that rule:

- **A restore needs no OV-1 rule of its own.** The score's ledger comes back as it was in the snapshot. The ordinary
  session catches up the lost draws and they are counted by the standing rule; each line records that its forecasts
  were caught up. A restored production is fully functional after that catch-up.
- **When the replayed score equals the one that was lost, and when it does not** (EX_255 E04). It equals it when, for
  every replayed draw, the same variants count (the same release records, with their original first-draw numbers), by
  the same code, configuration and seed rule, from the same earlier draws, in an environment that computes the same
  numbers (the amendment's examples 5a and 5b-i). **It is not promised otherwise.** It differs when a later release
  was not put back before the catch-up (5b-ii), when the environment computes differently (5c), or when a revision
  that should have counted can no longer run (6b). Such differences are labelled: each line has its standing,
  supported or qualified, by the amendment's objective rule (2.5A), and each line records the digests of the code and
  the environment that computed it, so a difference can be investigated.
- **The order that keeps the most lines supported:** restore; then `update` to put back each later release from its
  saved record (it keeps its original first-draw numbers: section 4.3); then the results updater and the catch-up.
  `check` prints this when the clone holds a release that production lacks.
- **The environment is not pinned** (the owner, entry 119; the amendment's 2.5B). The restore brings back the
  environment that was running; if the owner then rebuilds it, the replay runs in the new one.
- **Withdrawn from this note:** the restore notices; the stop cause `NOT_ESTABLISHED_AFTER_RESTORE`; the refusal of
  `register` after a lost registration; the look inside the set-aside tree for a registration; any OV-1 purpose of
  `--after-hand-unzip`; the edits to `ov1.py` and `consolidated_report.py` that v0.3 listed; and v0.3's tests of them.
- No science input is ever taken from the set-aside tree. A release is put back from its record in the clone's
  history, not inferred from the old folder.
- The trace made for v0.2 (section 14) stays beside this note as the record of what the old rule did.

**Order of ratification.** This section depends on the amendment. This note is to be ratified with the amendment or
after it, not before. If the amendment were not ratified, v0.3's section 9 would return.

