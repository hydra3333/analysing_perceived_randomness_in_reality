### L6. The window contract and the two kinds of development run (always-review: holdout access, N-1)

- **A second plan schema, `WF_BATCH_PLAN_V2`,** beside the first, which is left exactly as it is. A V2 plan fixes its
  kind, its cohort and its explicit (variant, target) pairs; its runs carry tickets (`TICKET_V1`, scope `DEV_BATCH`)
  and a `DEV_BATCH` binding, and publish under the development run root only. Both kinds go through the same driver,
  the same gate, the same N-1 isolation and the same record contracts (Sup v0.8 7.1A; EX_223 B04).
  - **`ROUTINE_FILL`:** the driver works out the pairs itself: for every released variant, its eligible targets that no
    canonical source covers (`score_identities.canonical_coverage`, identities only). Eligible means the game's first
    target to `holdout_last` (after the seal), and, above the holdout, only the targets of rule 2A. The owner names
    nothing but the game.
  - **`EXPLORATORY_RERUN`:** the owner names the variants (or the whole released cohort) and the window. Any target up
    to `holdout_last` (after the seal) and any later accepted target that already has a weekly freeze line may be
    included, whether or not it was scored before.
- **The `DEV_BATCH` branch of the dispatch gate** (value-free records, fixed roots): the plan exists with that digest
  and its search-log row and lists the pair; the request pins the plan's pin; an open ticket, and no DONE ticket for
  the pair in the batch; for a target at or above `holdout_first`, the opening record and the game's `MODE_H_SEALED`
  (Sup 7.2 rules 1 and 2); for a target above `holdout_last`, a weekly freeze line for the target must exist, and
  - for a routine fill (rule 2A as amended, EX_223 B03): that freeze line's time is before the variant's release
    instant (`released_utc` of its release record), the line does not name the variant, and no session ledger holds a
    ticket for the pair;
  - for an exploratory rerun: nothing more.
  A target that is still open in the weekly session is never a batch's.
- **The report tool:** a V2 batch is reported on its own pairs; the window may reach `holdout_last` once the seal exists,
  and the targets above it that the plan lists; the outcome reader releases those draws to a development report only
  under the same conditions, after the search-log row and the scoring plan are written (the existing order,
  unchanged); families are loaded by window **and tier** (CF-5); every table of a V2 report is `EXPLORATORY_COHORT`.
- **After the report:** a routine fill's attempt is admitted (L4) and the league table is published. An exploratory
  rerun's report carries the comparison with the canonical figures for the same keys, and with any named earlier
  attempt, and changes nothing else.
- **The comparison with the sealed forecasts** (Sup 7.2 rule 7), as a section of the batch's report: for each pair, the
  preconditions and whether each holds; the ranking with scores and ties, and the TOP and WORST sets, compared; every
  difference listed with the inputs' identities. It reads the sealed run folders and writes nothing under any sealed
  path.
- **Gates:** no write under any sealed Mode H path and no freeze line or weekly ledger touched (a test snapshots every
  such file's bytes before and after each L6 command); every refused window refuses, including a holdout target
  before the seal, a routine-fill target with a weekly ticket, and the same-day cases of rule 2A (frozen before the
  release instant: admitted; frozen after it: refused; across a daylight-saving change); every forecast's tier is
  development; T-05 on the extended windows; a repeated run of a covered key is a separate attempt, is never summed,
  and never becomes canonical; a retired revision is not runnable; the two kinds give identical forecast content for
  the same pair, pin and revision.

