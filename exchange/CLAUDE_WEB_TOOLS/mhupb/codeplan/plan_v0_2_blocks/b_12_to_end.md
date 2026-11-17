## 12. Decisions made, and what the recheck is asked

**The owner's directions (decision log entries 69 and 70). Their exact wording is Sup v0.8, for his ratification.**

| | Direction | Where |
|---|---|---|
| OD-1 | A: two kinds of development run, routine fill and exploratory rerun | L6; Sup v0.8 7.1A, 4 rule 2A |
| OD-2 | B, conditionally as the reviewer indicated: a missed week is a neutral factor fixed in advance; else stop | L5; 6.6; Sup v0.8 6.8 |
| OD-3 | B: noon Adelaide time as the last moment for OV-1's pre-draw entry; the owner states that both games close at 7.30pm AEST | L5; Sup v0.8 6.8 |
| OD-4 | A: a stopped stream stays stopped | 6.6; Sup v0.8 6.8 |
| OD-5 | The real score records checked before the install: done (`cc665ce`; section 8) | 8 |
| OD-6 | A: three technical review slices, one integrated review, one install | 4 |

**The reviewer's answers CP-Q1 to CP-Q9 are all adopted** (section 1A). CP-Q7's gap is closed by rule 2A as amended.

**For the focused recheck (the points where this plan goes beyond the exact words of EX_223):**
- **R-1. The cut-off as a fixed instant.** OD-3 says noon Adelaide time. Sup v0.8 6.8 fixes 01:30 UTC on the draw date,
  which is noon in daylight time and 11:00 in standard time: never later than Adelaide's noon, one hour stricter for
  about half the year, and free of any time-zone rule. Is that acceptable as the realisation of OD-3? The owner sees
  the same wording at ratification.
- **R-2. The opportunity rule and its two arguments** (Sup v0.8 6.8; plan 6.6): that "missed" is fixed before the
  outcome, with absence established only from a verified chain; and that a stop can only remove crossings.
- **R-3. The canonical rule:** the first admitted score of a key is the canonical one; routine fills are admitted by
  their own workflow when nothing conflicts; exploratory reruns never (Sup v0.8 4 rule 2A; plan L4).
- **R-4. The publication protocol** (plan L4): manifest first, the search-log row last, an unfinished publication
  finished with identical bytes or marked incomplete.
- **R-5. A second sequencer and launcher for development jobs** (plan L8), so that one go covers one bounded job. It is
  a new launch interface for the Architecture's next edition.
- **R-6. Anything in Sup v0.8's amended text that says more, or less, than EX_223 intended.**

**DECIDED (cited, not reopened):** per game, bar 40, no joint figure (entry 55); the eight layers and the isolation rule
(RAT-33); the deadline (MHUP-R); tickets for official runs (Q11); two commits per install; the full suite after step 18;
OD-1 to OD-6 as directions (entries 69, 70). **RECOMMENDED:** everything else in sections 4 to 10. **OPEN:** R-1 to R-6;
the owner's ratification of this plan and of Sup v0.8.

## 12A. The three everyday jobs (EX_223 Appendix A, the operator experience test)

**1. A new method gets its history, and the all-method ranking is refreshed.** After the method's release package is
installed, the owner types one command per game, `Run_Development_Batch.bat --game G --fill`. The program works out which
(variant, draw) pairs have no canonical score, runs only those, scores them, admits them to the league's sources if
nothing conflicts, and publishes a new league table; the earlier table stays in the archive. One go covers all of it.
If something conflicts or fails, it stops, says what and why in plain words, and changes no table.

**2. A voluntary rerun of anything, for research.** The owner types
`Run_Development_Batch.bat --game G --rerun --variants ... --first S --last L` (or the whole cohort). The program runs
that as a new, separate attempt and writes a report that sets the rerun beside the canonical figures for the same
draws. The league table and its totals do not change. Draws that were once the Mode H holdout are allowed, as
development evidence; the sealed Mode H records are not touched.

**3. A weekly session after missed draws.** The owner runs the updater, then `Run_Weekly_Session.bat --game G`. It catches
up the missed draws oldest first (forecast, freeze, score), freezes the next draw's forecast if at least an hour
remains before midnight, makes OV-1's pre-draw entry, and publishes the league table. A missed week shows in the
formal test as "missed", not as a stop. If something genuinely fails, the status block says which typed stop it is and
what to do; the forecasts and scores already made are safe.

In none of the three does the owner edit a ledger, a hash, the source list or a version number.

| EX_223 Appendix A area | How this plan meets it |
|---|---|
| Historical walk-forward reruns | both kinds through one V2 driver; one canonical score per key (L6; L4) |
| Adding results to league tables | admission and publication are steps of the job; conflicts refuse (L4; L8) |
| Source-list versioning | one small tracked file, digest-bound to each publication; no extra chain (L4) |
| Owner approvals | one go per bounded job (section 13) |
| Three review slices | technical checks only (section 4) |
| OV-1 safeguards | kept and automated: the pre-draw entry, the sealed table, the certificate, the stop rules (L5; 6) |

## 13. Which gate belongs where

| Stage | What is judged | By whom |
|---|---|---|
| This plan's recheck | that B01-B04 and C01-C04 are met; R-1 to R-6; the kernel's method and proof plan; the release rules of CF-4; the `DEV_BATCH` gate; the fault and interruption matrices | the reviewer |
| Ratification | this plan and Sup v0.8, together | the owner |
| Implementation acceptance | the tests on both Pythons; mutants; the proofs written out; oracles reproduced (R-2, R-4); adapters on writer-made and on real records; the cloud rehearsals; T017's report read step by step | the reviewer, in three slices and one integrated review; Claude's evidence |

**The owner's gos, each covering one bounded job and all of its named steps (P1; EX_223 C04):**

| Go | Covers | How often |
|---|---|---|
| Start the code | the code round, to the integrated package | once |
| T017 | the baseline, the install rehearsal, both suites, the timings, the launch chain, the dress rehearsal | once (again only after a STOP) |
| The install | Appendix J's steps, both commits; his settings lines first | once |
| The documents | ratifying each amended document before it goes into `doc/` | once each |
| `declare-developed`; OV-1's registration | one per game | once each |
| A weekly session | the update, then for each game: catch-up, freeze, score, OV-1's entry, the table and any repair | his own deliberate weekly run is that week's go (R-018) |
| A development job | plan, run, report, and for a fill the admission and the new table | one per job he asks for |

A step outside a job's named scope, a retry after a STOP, and anything that changes a binding rule still need their
own go. The E2R-T12 run context is asked once for the cloud suite.

## 14. Not tested, uncertainties, alternatives

- **Not tested:** everything in the plan. The only things run were the existing suite (section 3), the probe (section
  6.4) and the census (section 8).
- **Size:** twenty new Python source files and two launchers, about twelve edited files, about fifteen new test
  modules. Larger than MHUP-A's code. v0.2 adds three source files to v0.1 (the identities reader, and the second
  sequencer with the shared child launcher) and removes the chain of source-list versions.
- **Uncertainties:** the cost of the environment digest at every `next`; the local time of midnight around a
  daylight-saving change for the forecast deadline (tested with fixed zones; the owner's zone is the one that
  matters; OV-1's cut-off no longer depends on it); the reviewer's view of R-1 to R-5.
- **Alternatives considered:**
  - `decimal` at high precision for OV-1, with a margin: shorter code, but it leans on a library's rounding of `exp` and
    `ln`, and on two implementations of `decimal` giving the same digits. Kept as a cross-check only.
  - Exact fractions throughout: no rounding to argue about, but the denominators grow without limit.
  - Reading X from the master in L5: rejected; the score lines already hold it (CF-8), and L5 then needs no outcome
    access at all.
  - Extending the first plan schema in place: rejected; committed version-1 plans must stay verifiable byte for byte.
  - Writing the eligibility line inside the forecasting half, in the same step as the freeze line: it would close the
    gap between the two, but L2 would then import L5, against the isolation rule.
  - A chain of numbered source-list versions (v0.1): dropped; Git and the publication manifests already give the
    history and the identity (EX_223 C03).
  - The search-log row before the archive files (v0.1): dropped; a crash could leave a permanent row with no files
    (EX_223 B02).
  - Noon by Adelaide's own clock: needs time-zone data and a rule for the daylight-saving change; the fixed instant is
    never later and has neither.
  - No second sequencer, the owner typing four commands per development job with identifiers copied by hand: fewer
    files, but exactly the administration the owner asked to avoid.
  - One big review instead of slices: fewer rounds, but faults in the live path would be found late.

End of draft v0.2.

