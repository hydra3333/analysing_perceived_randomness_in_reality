# MHUP-1 design v0.1r5 - amendment A1 (RATIFIED): the Mode H score ledger is published whole, once

**Status: RATIFIED by the GitHub project owner (hydra3333), 5 November 2026.** Owner decision, as given: "i hereby authorise and ratify that A1", after the ChatGPT reviewer's favourable focused design review (EX_150 section 2, B01: "ratify A1 as a narrow amendment to design v0.1r5, expressly replacing only the named 5.2, 5.4 and L-H2 rules"). The text below is the reviewed draft of EX_149 (`exchange/EX_149_Claude/MHUP1_design_amendment_A1_draft.md`) unchanged apart from this header, which replaces the draft's opening paragraph (its date, author and draft status).

**Supremacy:** from this ratification, sections 1-5 below replace exactly the words of design v0.1r5 quoted in section 1 (in 5.2, 5.4 and Appendix L item L-H2), and nothing else; every other rule of v0.1r5 stands. Section 6 records the owner's second decision of 5 November 2026 (EX_148 (iii-b)): the corrective scoring run after the Mode H seal is MHUP-B's, by the route stated there, which MHUP-B must separately specify, have independently reviewed and tested, and have the owner approve; no corrective scoring capability exists in MHUP-A. Section 7 is an explanatory note (EX_148 (vi)), not a change. The register and the design document record A1 in the next documentation package; the integrated MHUP-A package cites it.

Author: Claude (the project's primary designer and coder). Asked by: EX_148 B01, route (B).

## 1. The text replaced

Design 5.2, in the paragraph "The lifecycle markers": "-> one score line per planned pair (create-only, in the Mode H
score ledger) -> `SCORE_COMPLETE` (the scorer, after the last pair's line; it holds the ledger's digest)" and "if the
scorer stops after `SCORING_STARTED`, rerunning it finds that marker, re-verifies the same roster digest, skips every
pair that already has a score line (it never re-reads an outcome for a pair already scored), scores the remaining
pairs, then writes `SCORE_COMPLETE` and the seal". Design 5.4, "Scored once": "(5.2: the same attempt id, the same
verified roster, scored pairs skipped, no outcome re-read after `SCORE_COMPLETE`)". Appendix L, L-H2: "scorer crash
after one of ten targets, resume under the same attempt, one score line per pair".

## 2. The replacement

After `SCORING_STARTED`, the scorer reads the outcomes of the plan's targets once, through the outcome reader under the
freeze-before-outcome rule (5.3, unchanged), computes every score record and every MR5 rank-position record of the
attempt from that one read, and publishes the attempt's whole Mode H score ledger (`mode_h_score_ledger.jsonl`) in one
create-only step (`contract_publication.create_only`: the bytes written and synced to a temporary file, then linked to
the final name, so the file either does not exist or exists complete). Before `SCORE_COMPLETE` the scorer validates the
ledger as it stands (EX_148 B04): it must be exactly the lines this scorer writes for the frozen forecasts of the
verified roster, given the drawn numbers the ledger itself records - every expected identity once, nothing missing,
duplicated or foreign, every drawn number of a draw agreeing across its lines, and every line rebuilt byte for byte
(Oz Lotto's supplementary counts, which the ledger never stores the supplementaries for, are checked for range and
against their division). Only then `SCORE_COMPLETE` (with the ledger's digest), the report from the accepted lines (its
three files resumed one by one, EX_148 B02) and `MODE_H_SEALED`.

## 3. The guarantees kept, unchanged

- One routine score attempt per game; the attempt id is fixed by `SCORING_STARTED`; a rerun resumes that attempt and is
  refused after the seal.
- The exact roster: `SCORING_STARTED` holds the roster digest; a resume re-verifies it and refuses a difference.
- Fixed scientific identity: each score line keeps its identity (track, draw, revision, forecast and receipt digests,
  evaluator version), and the ledger's create-only publication and the validation refuse a second line for any identity.
- No second accepted score: the ledger is create-only, and `SCORE_COMPLETE` binds its digest.
- No outcome re-read after accepted scoring: once the ledger exists, no outcome is read for it again (its lines are
  validated from their own recorded drawn numbers); after `SCORE_COMPLETE` the outcome reader refuses every holdout
  target (5.3).
- The report from the accepted lines only; the seal after the report.

## 4. The recovery states that disappear, and the bounded failure model

With per-pair lines there were three states between `SCORING_STARTED` and `SCORE_COMPLETE`: no line, some lines, all
lines. With one publication there are two: **no ledger** (a crash at any point before the link, including a crash
while computing or writing the temporary file) and **the complete ledger** (a crash after the link). "Some lines" no
longer exists, so L-H2's "crash after one of ten targets" has no state to test and the skip-scored-pairs logic is not
needed. Failure model:
- crash before publication: the rerun finds `SCORING_STARTED` and no ledger, re-verifies the roster, and reads the
  outcomes again - permitted, because no outcome of this attempt has been accepted (no ledger, no `SCORE_COMPLETE`) and
  the release rule (5.3) still holds; the leftover temporary file, if any, is never read;
- crash after publication, before `SCORE_COMPLETE`: the rerun reads no outcome; it validates the ledger as section 2
  says and writes `SCORE_COMPLETE`, or refuses if the ledger is not exactly the scorer's (a refused ledger is a STOP for
  the owner and the reviewer; nothing is completed);
- crash after `SCORE_COMPLETE`: as ratified (no outcome read; the report resumed; the seal).
The one new cost is that a crash before publication repeats the whole outcome read rather than part of it; the read is
of the same ten targets at the same pinned version, so its result is identical.

## 5. Oracles (in the slice 2 candidate v1r1)

`test_mhupa_mode_h`: crash before publication (the outcome read fails; the rerun scores), crash after publication and
before `SCORE_COMPLETE` with the outcome reader mocked to fail (no read), crash after `SCORE_COMPLETE` and after the
report's `.txt` and `.csv` (B02), the twin-project byte identity of the resumed and uninterrupted attempts (in place of
L-H2), and nine invalid ledgers refused before `SCORE_COMPLETE` (B04), plus Oz Lotto's two.

## 6. The corrective scoring run (EX_148 (iii-b); owner decision: deferred to MHUP-B)

Design 5.2 and 5.4 allow, after the seal, a separately identified scoring run beside the first, to correct a scorer
fault or add a measure, under its own scoring policy id with `amendment_of`. MHUP-A does not provide it; its `score`
command refuses after the seal and names this route. The route, for MHUP-B's weekly scorer (design 6.6), is:
`Method_Weekly_Score.py diagnostic-score`'s sibling command for Mode H corrections, run by the owner after a reviewed
reason, which (a) requires `MODE_H_SEALED`; (b) writes its own attempt folder `results/real/holdout/scores/<GAME>/<batch>/
<new attempt id>/` with a scoring plan naming the new scoring policy id and `amendment_of` = the sealed attempt id and
ledger digest; (c) reads the outcomes only under a release rule extended for it (the seal present, the policy id
registered by a reviewed package, the sealed attempt's records unchanged by digest); (d) publishes its ledger and report
create-only beside the first, never touching the first ledger, `SCORE_COMPLETE` or the seal; (e) appears in every later
report as an amendment, beside and never instead of the sealed score. Its design is part of MHUP-B's review.

## 7. Refusal (1) and the study version advance (EX_148 (vi), for the record)

Design 4.1 says refusal (1) and the other checks "read that record and, when its named rows are exactly the rows beyond
`v_a`, use `v_a'` in its place". The updater v0.2's refusal (1) admits a write only while the ledger's last row is `v_f`
(the one permitted first update); every other state of an opened, unsealed game is refused. So the advance record can
only ever replace `v_a` where `v_a` is the admitted version - in the plan, every `run` check and the scorer - and never
in the updater, where admitting `v_a'` would mean admitting a second update. The updater reads the advance record so
that an inconsistent one refuses and its message names `v_a'`. Synthetic evidence: the updater's
`t_refusal_unsealed_window` and `test_mhupa_mode_h.Pipeline.test_an_advance_after_the_plan_moves_the_admitted_pin`.
