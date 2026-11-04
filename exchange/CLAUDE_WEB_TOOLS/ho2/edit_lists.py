"""Counted edits to the owner's two lists (CRLF, US-ASCII). Every old string must occur exactly once."""
import sys, pathlib
repo = pathlib.Path(sys.argv[1])

def apply(path, edits):
    p = repo / path
    t = p.read_bytes().decode("ascii").replace("\r\n", "\n")
    for old, new in edits:
        n = t.count(old)
        assert n == 1, (path, n, old[:70])
        t = t.replace(old, new)
    t.encode("ascii")
    p.write_bytes(t.replace("\n", "\r\n").encode("ascii"))
    print(path, len(edits), "edits")

# ---------------- reminders ----------------
R016_OLD = """- Status: OPEN. Step 1 and Step 1.1 done (EX_133 to EX_136; owner-ratified 4 November 2026; DOC-11
  installed at 3d4fa3c and verified from GitHub, EX_138). Next: Step 2, the owner starts the new Claude chat."""
R016_NEW = """- Status: OPEN for the later ChatGPT reviewer handover only. The staged Claude handover is DONE (4 November
  2026): DOC-11 installed at 3d4fa3c (EX_138); the replacement Claude chat's first reply, the reviewer's
  questions Q1-Q9 answered blind, all PASS; the owner declared HO-2 complete and authorised normal work
  (option (a)); recorded in EX_139 and EX_140. The current reviewer stays in role through at least MHUP-A's
  first substantive code review."""

R017_OLD = """- When: the Claude Code rulebook's rule 1 with MHUP-A's rulebook change (register v0.24, future action 1);
  the design and the direction document at their next editions (future action 6); H-2 with the later
  reviewer handover (R-016)."""
R017_NEW = """- When: the Claude Code rulebook's rule 1 with MHUP-A's rulebook change (register v0.24, future action 1);
  the design at its next edition (future action 6); H-2 with the later reviewer handover (R-016). The
  direction document is DONE: v0.3r1 (installed at dfc2d13, 4 November 2026) uses the name."""

R018 = """
## R-018  The owner's decisions of 4 November 2026, to be recorded and carried into the work

- Asked: the owner, 4 November 2026, during the staged handover (EX_139, EX_140).
- Status: OPEN until each is recorded and carried into its place.
- What, and where each goes:
  (a) Retrying after a STOP (the first results update in particular): a STOP is always a STOP; Claude
      reports it, diagnoses the cause and proposes the recovery; the owner explicitly authorises each retry.
      A retry may proceed under the existing Approval 2 only if the refusal came before admission (master and
      ledger unchanged) and the cause is positively identified as within the original operation (for
      example an insufficient window, fixed with --months-back). If the cause is uncertain, there is partial
      transaction state, or the retry would go beyond the approval, STOP for separately reviewed recovery
      steps and the owner's approval. Goes into: register v0.25, the next H-1 edition, MHUP-B's checklist.
  (b) The direction document aligned to the release-record date: DONE (v0.3r1, installed at dfc2d13).
  (c) The template README's draft number ("DRAFT 3" in the status line of draft 4): at the next authorised
      template edition.
  (d) Interrupted sessions: MHUP-B's operator checklist says an interrupted session must be safely resolved
      before any code-changing install, and that a session cannot be resumed after the code closure has
      changed. Goes into: MHUP-B's documents, under normal review.
  (e) E1, complete historical coverage: a deferred objective. Every method eventually gets retrospective
      forecasts for every applicable past draw, including the ten holdout draws; a later method's holdout
      forecasts only through a separately designed, reviewed and owner-approved process, as development
      evidence only, never part of the sealed Mode H study. Raise with roadmap 21b's back-history design.
  (f) E2, one consolidated owner-facing report, with development, Mode H, CATCH-UP and PROSPECTIVE kept
      separate, sample sizes shown, comparisons on common draws, no pooled score. Design with the
      cross-batch report, after WF-1C (roadmap 21b).
  (g) E3: recalculating a development report's quantities is not a second accepted score; accepted
      records are never altered. Check the actual WF-1B behaviour in the cross-batch report's design.
  (h) E4: after the owner's GOAL-1 declaration and the required installs and approvals, his deliberate run
      of Run_Weekly_Session.bat is that week's authorisation; no weekly approval round. Not for unattended
      scheduling, unusual recovery, a STOP, or anything outside the approved scope; the updater stays a
      separate operation. Goes into: register v0.25, the next H-1 edition (section 10.8), MHUP-B's checklist.
  (i) The direction document v0.3r1 ratified (dfc2d13): register v0.25.
- When: register v0.25 records all of them (with MHUP-A's round); each "goes into" item at its document's
  next authorised edition.
"""
STANDING_OLD = "\n## Standing reminders\n"

apply("exchange/OWNER_REMINDERS.md", [
    (R016_OLD, R016_NEW),
    (R017_OLD, R017_NEW),
    (STANDING_OLD, R018 + STANDING_OLD),
])

# ---------------- roadmap ----------------
HDR_OLD = """Last updated: 3 November 2026 (evening): the MHUP-1 design ratified (MHUP-R); DOC-11, the Claude handover
package, prepared for ChatGPT's Step 1.1 review under your staged handover (HO-2); the code paused.
Plain-English direction: exchange/Direction_for_operational_procedures_v0_2r1.md (into doc/ with DOC-11);"""
HDR_NEW = """Last updated: 4 November 2026 (afternoon): the staged Claude handover (HO-2) COMPLETE; the replacement Claude
chat accepted and normal work authorised (option (a)); the direction document v0.3r1 installed at dfc2d13.
Plain-English direction: doc/Direction_for_operational_procedures_v0_3r1.md (v0.2r1 kept as history);"""

NEXT_OLD = """           (Lotterywest-GOV); ChatGPT's recheck EX_136 PASS; you ratified DOC-11 on 4 November 2026
           and installed it at 3d4fa3c (verified from GitHub, EX_138). NEXT: you start the new Claude
           chat with the blurb in doc/HANDOVER/; ChatGPT checks its first replies and suggests
           targeted questions, which the new chat answers blind; then, ONLY after that check and your
           explicit go-ahead, MHUP-A code (Fable for the core). A ChatGPT reviewer handover is
           considered later, separately. The planning dates above are unchanged; FB-1 applies."""
NEXT_NEW = """           (Lotterywest-GOV); ChatGPT's recheck EX_136 PASS; you ratified DOC-11 on 4 November 2026
           and installed it at 3d4fa3c (verified from GitHub, EX_138). DONE (4 November 2026): the new
           Claude chat started; ChatGPT checked its first reply and asked Q1-Q9, answered blind, all
           PASS; Q9 led to the direction document v0.3r1 (ChatGPT RECHECK, then PASS; ratified and
           installed by you at dfc2d13); your decisions on retrying after a STOP, interrupted sessions
           and Q9's E1-E4 (reminder R-018); you declared HO-2 complete and authorised normal work
           (EX_139, EX_140). NOW: Claude's workspace and the Linux suite, then MHUP-A code (Fable for
           the core), up to ChatGPT's code review; installing it, its Windows rehearsal and MHUP-B each
           wait for your separate go. A ChatGPT reviewer handover is considered later, separately. The
           planning dates above are unchanged; FB-1 applies."""

R21B_OLD = """21b. LATER - After WF-1C, two efficiency items from the stock-take (ratified 2 November 2026, not
           before Mode H): a report that ranks across batches by reusing the frozen run records, so
           adding a method no longer needs every other method re-run; and the index for a retired
           revision's records."""
R21B_NEW = """21b. LATER - After WF-1C, two efficiency items from the stock-take (ratified 2 November 2026, not
           before Mode H): a report that ranks across batches by reusing the frozen run records, so
           adding a method no longer needs every other method re-run; and the index for a retired
           revision's records. Added 4 November 2026 (your E1-E3, reminder R-018): the same design
           gives you one consolidated report with development, Mode H, CATCH-UP and PROSPECTIVE kept
           separate (no pooled score), checks how the WF-1B report recomputes its figures, and plans a
           later method's back-history over the post-holdout draws; forecasts by a later method for the
           ten holdout draws need their own reviewed design and count only as development evidence."""

apply("exchange/OWNER_ROADMAP.md", [
    (HDR_OLD, HDR_NEW),
    (NEXT_OLD, NEXT_NEW),
    (R21B_OLD, R21B_NEW),
])
