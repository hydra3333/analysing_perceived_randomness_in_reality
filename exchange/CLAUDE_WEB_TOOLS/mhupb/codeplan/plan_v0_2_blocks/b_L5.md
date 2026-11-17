### L5. OV-1 (section 6 has the arithmetic; Sup v0.8 6.5 and 6.8 have the rules)

- **The registration** (`register --game G --statement "..."`, owner-run, create-only, one per game, a search-log row):
  the game; the first eligible target T0 = `last_draw + 1` at that moment, which must have no freeze line and a
  deadline still ahead; the formula; the six lambdas as exact fractions with equal weights; the bar 40; the pair rule
  and the V = 0 rule; the opportunity rule and the cut-off; the owner's statement that both games close at 7.30pm
  AEST; the scoring policy whose lines are read; the kernel's precision, margin and version; the error budget (this
  game's 2.5% of the programme's 5%, and RC-1). It refuses without the developed record. **No command makes a second
  registration for a game, and none recovers a stopped stream (OD-4).**
- **The cut-off** C(T) is 01:30 UTC on T's derived draw date: noon in Adelaide in daylight time, 11:00 in standard time,
  eight hours before 7.30pm AEST. It is a fixed instant, so the code has no time-zone rule to get wrong. A test checks,
  for every Tuesday and Thursday to the end of 2045, that it is 11:00 or 12:00 in Adelaide on the same date and never
  after noon. It moves no forecast deadline: a ticket counts only if frozen before midnight (Des 6.4).
- **The ledger** (`OV1_LEDGER_<GAME>_V1.jsonl`, tracked, chained from the registration's digest), four kinds of line:
  - *eligibility*, for a target with a pre-cut-off freeze line: the registration's identity, the freeze line's digest,
    the eligible variants (count and digest), the weight of every number, V as an exact fraction, whether the draw is
    a V = 0 skip, the digest of the sealed factor table with its certificate result, the time, and the master pin then
    in force;
  - *factor*: the eligibility line's digest, the outcome pin copied from the score lines, X, Z to a fixed number of
    digits for display, the six stored log-factors as exact fixed-point integers, the six running sums, the proved
    lower bound of the score, and `crossed`;
  - *missed* (`MISSED_NO_FREEZE`), for a target with no pre-cut-off freeze line: written after C(T), from the verified
    forecast ledger, naming that ledger's length and digest as read, and labelled as recorded after the cut-off;
  - *stop*: the target and the cause.
- **One idempotent command, `record --game G`,** run by the sequencer after every `score` and after the loop, and safe
  for the owner to run again at any time. It takes the targets from T0 in order and writes whatever is due, nothing
  twice and nothing out of order: an eligibility line (before C(T) only); a missed line (after C(T) only); a factor
  line once the eligibility line and the eligible variants' score lines are there; a stop line. It reads the frozen
  tickets, the forecast ledger and the score ledger, and never the master. A failure of `record` never changes the
  live path's exit. It is the one writer of this ledger (EX_223 C01).
- **`stop --game G --statement "..."`** records an owner stop (the operator's schedule changed). **`verify`** rebuilds
  every line from the eligibility lines, the forecast ledger and the score ledger and compares bytes. A later kernel
  version must reproduce a frozen fixture ledger byte for byte, or it is a reviewed amendment.
- **Gates** (Sup 2 row L5; Sup v0.8 14): section 6's; every target classified as counted, skipped, missed or a stop from
  the records alone, with the cut-off tested one second before, at, and one second after; a missed line refused when
  the forecast ledger's chain is broken or its times run backwards; a freeze line appended after the cut-off never
  counted; incomplete pairs excluded; changing rosters and history-dependent weights; an interruption exactly between
  the freeze line and the eligibility line, resumed before and after the cut-off; each stop cause of 6.6 planted
  once, with no factor line after it; restart giving the same bytes; no OV-1 figure for a holdout, catch-up or
  development draw in the formal stream (Sup 6.7).

