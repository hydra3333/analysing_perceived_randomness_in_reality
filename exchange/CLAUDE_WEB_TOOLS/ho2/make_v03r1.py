import sys
p = sys.argv[1]
t = open(p, encoding='ascii').read()
R = []
R.append(("# Direction for the operational procedures, v0.3 (CANDIDATE)",
          "# Direction for the operational procedures, v0.3r1 (CANDIDATE)"))
R.append(("ratification register hold the exact rules, and they prevail wherever this file is looser.\n\n**Status and authority:** CANDIDATE v0.3, for the ChatGPT reviewer chat's content check and the owner's",
          "ratification register hold the exact rules, and they prevail wherever this file is looser. **v0.3r1** (4 November\n2026) applies the reviewer's focused RECHECK of v0.3 (C01 to C03, O01, O02).\n\n**Status and authority:** CANDIDATE v0.3r1, for the ChatGPT reviewer chat's focused recheck and the owner's"))
R.append(("  Oz Lotto 1694-1703), each from the draws before its target; every planned run finishes and is frozen; then\n  the ten are scored once, and the study is sealed. (ratified: MHUP-Q1 option A, MHUP-R)",
          "  Oz Lotto 1694-1703), each from the draws before its target. Every planned pair reaches DONE, including a run\n  that fails and is counted as missing; every successfully published forecast is frozen create-only. Only once\n  the whole batch is complete are the ten targets scored once and the study sealed. (ratified: MHUP-Q1 option A,\n  MHUP-R; design 5.2)"))
R.append(("6. If a session is interrupted, running the same command again resumes it where its records left off; nothing\n   accepted is redone. An interrupted",
          "6. If a session is interrupted, running the same command again resumes it where its records left off, but only\n   when the project's checks admit a safe resume (no project process still running, the session's lock, an\n   unchanged code closure and a fresh resume token); otherwise it STOPs and the reviewed recovery procedure is\n   followed, so an interruption is never permission to retry. Nothing accepted is redone. An interrupted"))
R.append(("""  - the ten holdout draws: never in the weekly session, because Mode H is a one-time study of the cohort
    released before it; any later forecasts on them would need a separately reviewed extension (design 6.3;
    open: whether the owner wants this).
  Until 21b exists, a method released after Mode H has a gap in its record over those draws; every ranking
  shows each method's number of draws, and methods are compared on the draws they share.""",
"""  - the ten holdout draws: never in the weekly session, and not by roadmap 21b either, because Mode H is a
    one-time study of the cohort released before it (design 6.3). Forecasts by a later method for those draws
    would need a later, separately reviewed extension, if the owner keeps that objective (open); they could
    only ever be retrospective development evidence: never added to the sealed Mode H family, never given
    pre-draw standing, and never counted as part of the original holdout cohort.
  So a method released after Mode H has two gaps in its record: the post-holdout draws before its release
  (until 21b exists) and the ten holdout draws (unless a later extension is approved). Every ranking shows each
  method's number of draws, and methods are compared on the draws they share."""))
R.append(("""  change) and MHUP-B (the weekly session and the owner's one-page checklist). The updater is not run in any form
  before MHUP-A is installed and the first update is separately approved. (ratified: MHUP-R)""",
"""  change) and MHUP-B (the weekly session and the owner's one-page checklist). (ratified: MHUP-R)
- Before MHUP-A is installed, the updater is not run in any form. After its installation and before Approval 2,
  the owner runs the required offline `--self-test` under Python 3.15. No real results update is permitted until
  the owner grants Approval 2 for that game; a STOP is reported and no retry occurs without the owner's new
  explicit instruction. (ratified: MHUP-R, design 4.4 step 3 and section 7; owner, 4 Nov 2026)"""))
R.append(("""- Deferred, each its own package and the owner's decision, after WF-1C (roadmap 21b): a report that ranks
  across batches by reusing frozen records; a back-history batch for a later method over post-holdout draws;
  the retired index.""",
"""- Deferred, each its own package and the owner's decision, after WF-1C (roadmap 21b): a consolidated
  owner-facing report that ranks across batches by reusing frozen records; a back-history batch for a later
  method over the post-holdout draws before its release; the retired index. A consolidated report holds the
  separate evidence families (development, Mode H, CATCH-UP, PROSPECTIVE) as separately labelled views, with
  sample sizes, exposure windows and matched-draw comparisons; it does not pool them into one score, and no
  combined statistic is specified here."""))
R.append(("*End of direction v0.3 (candidate).*",
"""## Changes in v0.3r1 (the reviewer's focused RECHECK of v0.3, 4 November 2026)

1. C01, section 4: every planned pair reaches DONE, a failed run counted as missing; scoring only once the whole
   batch is complete (design 5.2); the primary statement in the next bullet unchanged.
2. C02, section 10: the updater is not run before MHUP-A is installed; the offline self-test under Python 3.15
   after its installation and before Approval 2; no real update without Approval 2; a STOP is reported and no
   retry occurs without the owner's explicit instruction.
3. C03, section 7: roadmap 21b covers only the post-holdout draws before a method's release; the ten holdout
   draws need a later, separately reviewed extension, and could only ever be retrospective development evidence.
4. O01, section 11: a consolidated report keeps the evidence families separate; no pooled score.
5. O02, section 5 step 6: a session resumes only when the checks admit a safe resume; otherwise STOP and the
   reviewed recovery procedure.
No other line changed.

*End of direction v0.3r1 (candidate).*"""))
for old, new in R:
    n = t.count(old)
    assert n == 1, (n, old[:60])
    t = t.replace(old, new)
t.encode('ascii')
open(p, 'w', encoding='ascii', newline='\n').write(t)
print("applied", len(R), "counted replacements")
