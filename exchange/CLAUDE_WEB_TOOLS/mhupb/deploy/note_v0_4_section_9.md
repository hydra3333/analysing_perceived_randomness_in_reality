## 9. OV-1 after a restore: nothing special (EX_253; the OV-1 simplification amendment; entry 116)

v0.3's section 9 answered a problem of the ratified rule: OV-1's formal stream counted only forecasts frozen before
their draw by the clock, so a draw counted before a restore could come back as "missed". It proposed restore notices, a
new stop cause and a refusal of a second registration.

The owner has since directed that OV-1 be simplified to one prevailing score per game (EX_253), and the amendment sent
with this note (`ov1_simplify/MHUPB_OV1_SIMPLIFICATION_AMENDMENT_DRAFT_v0_1.md`) proposes the rule: a variant counts at
a draw if it was released before that draw and forecast it under N-1 isolation, whether before the draw or afterwards
by catch-up. Under that rule:

- **A restore has no OV-1 side effect.** The score's ledger comes back as it was in the snapshot. The ordinary session
  catches up the lost draws; they are counted by the standing rule; each line records that its forecasts were caught
  up. The amendment's invented example 5 shows the replayed lines equal to the lost ones.
- **Withdrawn from this note:** the restore notices; the stop cause `NOT_ESTABLISHED_AFTER_RESTORE`; the refusal of
  `register` after a lost registration; the look inside the set-aside tree for a registration; any OV-1 purpose of
  `--after-hand-unzip`; the edits to `ov1.py` and `consolidated_report.py` that v0.3 listed; and v0.3's tests of them.
- **The one thing left to say is about conduct, not machinery** (the amendment's section 8, condition 4): which
  backup to restore is never chosen in order to move a score.
- The trace made for v0.2 (section 14) stays beside this note as the record of what the old rule did.

**Order of ratification.** This section depends on the amendment. This note is to be ratified with the amendment or
after it, not before. If the amendment were not ratified, v0.3's section 9 would return.

