"""Builds the MHUP-B design supplement v0.8 (AMENDMENT CANDIDATE) from the ratified v0.7 bytes by counted edits.

Usage: python3 -I make_supplement_v0_8.py V0_7_FILE OUT_FILE
V0_7_FILE is the ratified supplement as stored (CRLF; SHA-256 04c4f68a...3d26). Every old text is asserted to occur
exactly once. The output is US-ASCII with CRLF, like its source. Nothing else is changed.
"""
import hashlib, sys

SRC_SHA = '04c4f68a638fff7d93f06d25084d1454bdfc443e9aab6b0b12ffdfd8b5323d26'
src, out = sys.argv[1], sys.argv[2]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == SRC_SHA, 'not the ratified v0.7 bytes'
s = raw.decode('ascii').replace('\r\n', '\n')
assert '\r' not in s
EDITS = []


def edit(old, new):
    EDITS.append((old, new))


# ---------------------------------------------------------------- header
edit("# MHUP-B design supplement - v0.7 (RATIFICATION CANDIDATE)",
     "# MHUP-B design supplement - v0.8 (AMENDMENT CANDIDATE)")
edit("""**Status: RATIFICATION CANDIDATE, by the Claude web chat (17 November 2026). The reviewer passed draft v0.6 as a design
and recommended ratification with one condition, RC-1 (EX_213). v0.7 is v0.6 with RC-1 written into section 6.8 and
nothing else changed. It is in force only when the project owner ratifies it. Ratifying it approves a design: it
authorises no code, run, rescore, re-forecast or install, each of which needs its own go.** Drafts v0.1 to v0.6 are kept
in the same folder as history. It supplements the ratified design""",
     """**Status: AMENDMENT CANDIDATE, by the Claude web chat (17 November 2026).** A full edition: the supplement v0.7 as the
project owner ratified it on 17 November 2026 (RAT-33; SHA-256 `04c4f68a638fff7d93f06d25084d1454bdfc443e9aab6b0b12ffdfd8b5323d26`)
with the focused amendments listed in section 1A. They answer the reviewer's review of the code plan (EX_223: B01, B02,
B03, B04, C01, C02, C03) and follow the owner's directions OD-1 to OD-4 (decision log entries 69 and 70). Everything not
listed in section 1A is v0.7's text, unchanged; the builder `make_supplement_v0_8.py` makes it from v0.7's bytes by
counted edits. **Until the owner ratifies v0.8, v0.7 is the ratified edition and governs. Ratifying v0.8 approves a
design: it authorises no code, run, rescore, re-forecast or install, each of which needs its own go.** Drafts v0.1 to
v0.6 are kept in the same folder as history. It supplements the ratified design""")
edit("""**Review record:** EX_207 (v0.1), EX_208 (v0.2), EX_209 (v0.4), EX_211 (v0.5), EX_213 (v0.6: focused design pass). **Gates left""",
     """**Review record:** EX_207 (v0.1), EX_208 (v0.2), EX_209 (v0.4), EX_211 (v0.5), EX_213 (v0.6: focused design pass); for
v0.8, EX_223 (the review of the code plan, which asked for these amendments). **Gates left""")

# ---------------------------------------------------------------- section 0
edit("""  reaches its bar in about 190 draws (median; under four years of that game). A 10% tilt takes several times longer. A
  guide only.
""",
     """  reaches its bar in about 190 draws (median; under four years of that game). A 10% tilt takes several times longer. A
  guide only.
- **Amended in v0.8.** A missed week does not end the formal test: a draw for which no forecast set was frozen in time
  counts as neutral, by a rule fixed in advance that cannot see the result. A set that was frozen but whose pre-draw
  entry is missing still stops the test, and a stopped test stays stopped. Any runnable method can be run again over
  past draws for research; such reruns are kept apart and never change the league's totals.
""")

# ---------------------------------------------------------------- section 1: rows, and the new section 1A
edit("""| Owner, entry 53 (new in v0.3) | The holdout draws open to re-forecasting by every variant; the sealed forecasts kept as separate history | 3.2, 4, 6.7, 7 |
""",
     """| Owner, entry 53 (new in v0.3) | The holdout draws open to re-forecasting by every variant; the sealed forecasts kept as separate history | 3.2, 4, 6.7, 7 |
| EX_223 B01; owner OD-2, OD-3 (v0.8) | Every target is one opportunity; a missed week is a neutral factor fixed in advance; the cut-off for the pre-draw entry | 6.5, 6.8 |
| EX_223 C02 (v0.8) | A failure is never a skip; blocked and stop; the factor table sealed before the outcome | 6.8 |
| EX_223 B03 (v0.8) | Back-history by the release instant, not the release date | 7.2 rule 2A |
| EX_223 B04; owner OD-1 (v0.8) | Routine fill and exploratory rerun; canonical and exploratory attempts | 7.1A, 4 rule 2A |
| EX_223 C01, C03, B02 (v0.8) | One writer per ledger; one small source file, with admission inside an approved workflow; a table is logged only when its set is complete | 4 rules 4 and 5, 5.1 |
| Owner OD-4 (v0.8) | A stopped stream stays stopped; no second registration in MHUP-B | 6.8 |

## 1A. What v0.8 changes in the ratified v0.7

Everything else is v0.7's text, byte for byte.

| Where | Change |
|---|---|
| Header, section 0, section 1 | Status and review record; one summary bullet; six table rows; this section |
| 4, after rule 2 | New rule 2A: canonical and exploratory attempts; the first admitted score is the canonical one |
| 4 rule 4 | One sentence replaced: who starts a publication, and the one writer of each ledger |
| 4 rule 5 | Replaced: one small tracked source file; routine admission is part of an approved workflow |
| 5.1 | One sentence added: a set is logged only when both archive files exist |
| 6.5 | What the registration fixes; "every target is one opportunity" |
| 6.8 | The two-lines bullet extended; "who writes" reworded; new: the cut-off, the opportunity rule, failures; "after a stop" replaced |
| 7.1A (new) | Two kinds of development run |
| 7.2 rule 2A | Replaced: by the release instant; exploratory reruns above the holdout |
| 7.3 | One sentence added |
| 11, 12, 13, 14 | The ER-6 note; three alternatives; the decisions O-5 to O-7; the code round's added proofs |
""")

# ---------------------------------------------------------------- section 4
edit("""   key. Nothing here can change a sealed Mode H result.
""",
     """   key. Nothing here can change a sealed Mode H result.
2A. **What the totals count, and what may be run (v0.8; owner OD-1; EX_223 B04).** Rule 2 governs the league's totals, not
   what may be run. A development attempt is either *canonical* (listed in `LEAGUE_SOURCES_<GAME>.json`; its scores enter
   the all-draws column) or *exploratory* (never listed; shown only in separate, labelled comparisons by named
   attempt). A routine-fill attempt (7.1A), or a report attempt over a plan of the first kind, is admitted as canonical
   by its own workflow only if no key it supplies is already supplied by a canonical source or by the weekly score
   ledger; otherwise it is not admitted and the table is unchanged. So the canonical
   score for a key is the first one admitted. It is never replaced because a later run is newer or more favourable. An
   exploratory rerun is never admitted. Replacing a canonical source is a correction: a reviewed, named change on the
   owner's decision.
""")
edit("""the table files under `results/method_rankings/<GAME>/league/` (5.1). The orchestrator, and only it, appends the
   `WEEKLY_TABLE` row to the search log (required, never optional) and the OV-1 lines to their own create-only ledger
   (6.8). The forecasting and scoring halves""",
     """the table files under `results/method_rankings/<GAME>/league/` (5.1). A publication is started only by the
   orchestrator or by the one named publish command it runs, which the owner may also run on its own. One writer, and
   only it, creates the table files and appends their `WEEKLY_TABLE` row to the search log (required for every
   publication, whoever started it). The OV-1 lines are appended to their own create-only ledger by the one OV-1
   recorder, started in the same way (6.8). Nothing else writes either (v0.8; EX_223 C01). The forecasting and scoring halves""")
edit("""5. `LEAGUE_SOURCES_<GAME>.json` is changed only by a reviewed step on the owner's go (for example after the Powerball
   1145-1285 report run of section 8).
""",
     """5. `LEAGUE_SOURCES_<GAME>.json` is one small tracked file. It is changed only by the reviewed admission step of a
   workflow the owner has approved. Admitting a routine-fill attempt that conflicts with nothing (rule 2A) is part of
   that workflow's go and needs no separate one (for example the Powerball 1145-1285 report run of section 8).
   Anything that conflicts refuses; resolving it is a separately reviewed, named change on the owner's decision. Every
   published table names the file's digest and the exact sources it used; Git keeps the file's history (v0.8; EX_223
   C03).
""")

# ---------------------------------------------------------------- section 5.1
edit("""Each table set (the `.txt` and `.csv` of one publication) is logged in the search log (`WEEKLY_TABLE`).
""",
     """Each table set (the `.txt` and `.csv` of one publication) is logged in the search log (`WEEKLY_TABLE`). A set is logged,
and counts as published, only when both of its archive files are durable and verified. An interrupted publication is
finished with exactly the same bytes and identity, or is marked incomplete; it is never logged as complete, never
overwritten and never abandoned silently (v0.8; EX_223 B02).
""")

# ---------------------------------------------------------------- section 6.5
edit("""formula of 6.1, the six lambdas and their equal weights, the bar, the pair and V = 0 rules, the freeze-time eligibility
  rule and the error budget. It is created""",
     """formula of 6.1, the six lambdas and their equal weights, the bar, the pair and V = 0 rules, the freeze-time eligibility
  rule, the opportunity rule and the cut-off of 6.8, the scoring policy whose lines are read, the numerical kernel's
  version, and the error budget. It is created""")
edit("""was known when this statistic was chosen, can ever enter it.** From the start, every eligible forward draw is included
  exactly once, including skipped (V = 0) draws with factor 1; none is dropped, repeated or recomputed.""",
     """was known when this statistic was chosen, can ever enter it.** From the start, every target is one opportunity, taken
  in draw order exactly once: counted, skipped (V = 0) or missed (6.8), the last two with factor 1; none is dropped,
  repeated or recomputed (amended in v0.8).""")

# ---------------------------------------------------------------- section 6.8
edit("""- **Two create-only lines per counted draw** in a small ledger of its own. The *eligibility line* is written when the
  freeze line closes, before the outcome exists: game, target, the registered test's identity, the freeze line's identity,
  the eligible variants' count and digest, the weights' digest, V and whether the draw will be skipped. The *factor line*
  is written at scoring: the eligibility line's identity, the outcome pin (master version and SHA-256), X, Z, the six
  log-factors and the running score. A factor line without its earlier eligibility line refuses.""",
     """- **Two create-only lines per counted draw** in a small ledger of its own. The *eligibility line* is written when the
  freeze line closes, before the outcome exists: game, target, the registered test's identity, the freeze line's identity,
  the eligible variants' count and digest, the weights' digest, V and whether the draw will be skipped. The *factor line*
  is written at scoring: the eligibility line's identity, the outcome pin (master version and SHA-256), X, Z, the six
  log-factors and the running score. A factor line without its earlier eligibility line refuses. (v0.8: the eligibility
  line also holds the weight of every number and the digest of the draw's sealed factor table; a missed target has one
  line of its own, written after its cut-off; see below.)""")
edit("""- **Who writes them, and when** (EX_211 F01). The orchestrator calls the OV-1 recorder as soon as a freeze line closes,
  before the session ends and so before the outcome exists; the recorder needs only the frozen tickets. It is not part
  of table publication: a failed league table never prevents it, and its own failure never undoes or delays a freeze.
- **A missing eligibility line stops the primary stream, openly** (F01). The stream is a strict sequence. If, for a frozen
  prospective target, the eligibility line cannot be written and made durable before the outcome is known, the session
  record and every report say **"OV-1 eligibility NOT VERIFIED - PRIMARY STREAM STOP"** for that game from that target. No
  factor line is appended for that target or any later one; the target is not skipped, a later draw is not treated as the
  next, and nothing is back-filled with hindsight. The genuine forecast, its scores and the failure evidence are kept, and
  forecasting and scoring continue as normal.
- **After a stop** (EX_213 RC-1). Every new registration has a distinct test identity and must receive an explicit,
  reviewed error-budget allocation across all confirmatory registrations; there is no automatic reset and no reuse of
  the earlier per-game 2.5% allowance. A recovery after the outcome may continue the original stream only under a
  reconstruction rule fixed in advance and independent of the outcome, which accounts for every eligible draw; the
  owner's decision to recover may not depend on whether the resulting factor would be favourable. Building a line after
  the outcome is never assumed to be equivalent to the pre-outcome record.""",
     """- **Who writes them, and when** (EX_211 F01; EX_223 C01). The orchestrator starts the OV-1 recorder as soon as a freeze
  line closes, before the session ends and so before the outcome exists; it is attempted at once and is never held back
  until the cut-off. The recorder needs only the frozen tickets. It is the one writer of this ledger. It is not part of
  table publication: a failed league table never prevents it, and its own failure never undoes or delays a freeze.
- **The cut-off (v0.8; owner OD-3; EX_223 B01).** For target T the cut-off C(T) is 01:30 UTC on T's derived draw date.
  That is 12:00 noon in Adelaide during daylight saving and 11:00 in Adelaide standard time: never later than noon in
  Adelaide, and with no time-zone data to depend on. It is at least seven hours before a result can exist, on the
  owner's statement, recorded in the registration, that both games close at 7.30pm AEST. An eligibility line counts
  only if it is durable before C(T) and T's result is not then in the master; otherwise the recorder refuses to write
  one. **The cut-off moves no forecast deadline:** a ticket counts only if its own freeze time is before the design's
  midnight deadline (design 6.4), exactly as before, and nothing frozen later is promoted. If the operator's schedule
  changes so that a result could exist before C(T), the owner stops the stream by a recorded stop before the first
  affected draw; and a counted draw whose date in the master is not its derived date stops the stream.
- **Every target is one opportunity, classified by a rule fixed at registration (v0.8; owner OD-2; EX_223 B01).** From
  the first eligible target on, the targets are taken in draw order, each exactly once. A *pre-cut-off freeze line* for
  T is the freeze line of a next-draw set for T whose own freeze time is before C(T).
  - *Counted:* T has a pre-cut-off freeze line and a valid eligibility line. Its factor is that of 6.5, or 1 if the
    line records V = 0.
  - *Missed (`MISSED_NO_FREEZE`):* T has no pre-cut-off freeze line. Its factor is 1. The program decides this, never
    a person. After C(T) it records the fact from the forecast ledger, whose whole chain it has first verified, and
    labels the line as recorded after the cut-off from the records, which is a weaker witness than a pre-outcome line.
  - *Stop:* T has a pre-cut-off freeze line and no valid eligibility line at C(T). **"OV-1 eligibility NOT VERIFIED -
    PRIMARY STREAM STOP"** (F01), in the session record and in every report for that game from that target. It is
    never treated as missed.
  Which of the three applies is fixed by what existed before C(T), and so before T's result existed. Recording it
  later reads that fact and cannot choose it: a freeze line appended later carries its own later time and can never
  become a pre-cut-off line. If the ledger's chain does not verify, or its times do not run forward, absence is not
  established and nothing is recorded: an absence of evidence is never evidence of absence. The genuine forecasts,
  their scores and the failure evidence are always kept, and forecasting and scoring continue as normal.
- **Failures (v0.8; EX_223 C02).** A failure is never a skip.
  - *Blocked:* an input is not yet there or cannot be verified (the result not yet accepted; a score line not yet
    written; a ledger that does not verify). Nothing is written for that target or any later one until it resolves. No
    target is passed over.
  - *Stop:* the F01 case above; a recorded owner stop; or a contradiction about a counted target between what was
    sealed and what came later: the factor table rebuilt at scoring is not the one whose digest the eligibility line
    sealed; X is not a value the frozen weights can produce, or its two derivations disagree; an eligible variant's
    score line does not carry the frozen record's digest and the registered scoring policy; the draw's date is not its
    derived date. After a stop no factor line is appended for that target or any later one.
  - *Sealed before the outcome:* the factor table of a counted draw (every possible X, for each lambda) and its
    certificate are computed when the eligibility line is written, and the table's digest is in that line. The factor
    line only looks up the observed X. If the table cannot be computed and certified then, no eligibility line is
    written, which is the F01 case and is decided before the outcome. The scoring policy whose lines are read is fixed
    in the registration; a corrective score never enters OV-1.
  - *Why a stop can never manufacture a crossing:* a stop ends the stream at its last value, and no later factor is
    ever applied. Every crossing the software can declare is therefore a crossing of the whole registered process at
    that same draw. Stopping can only remove crossings. What would break the guarantee is passing over a draw and
    carrying on; outside the missed rule above, which is fixed before the outcome, the software never does that.
- **After a stop** (EX_213 RC-1; owner OD-4, v0.8). The stream stays stopped. MHUP-B provides no second registration, and
  no reconstruction rule is registered, so there is no recovery after an outcome. A retry of the recorder before C(T)
  is ordinary operation, not a recovery. For any future design, RC-1 stands: a new registration has a distinct test
  identity and must receive an explicit, reviewed error-budget allocation across all confirmatory registrations; there
  is no automatic reset and no reuse of the earlier per-game 2.5% allowance; and building a line after the outcome is
  never assumed to be equivalent to the pre-outcome record.""")

# ---------------------------------------------------------------- section 7
edit("""**7.2 The window contract** (an R3 17.3.6 amendment, not a bound edit).""",
     """**7.1A Two kinds of development run (v0.8; owner OD-1, decision log entry 69; EX_223 B04).** Both use the one driver, the
same N-1 isolation and the same record contracts, and both give development evidence only.
- *Routine fill:* when a variant is released, or a gap exists, only the missing pairs are run: each released variant's
  eligible targets for which no canonical score exists. Records that exist are reused. Its report attempt is admitted
  to the league's sources if nothing conflicts (section 4 rule 2A), and a new league table is published.
- *Exploratory rerun:* on the owner's request, any currently runnable variants, or the whole released cohort, over any
  eligible targets, whether or not they were scored before: any target up to `holdout_last` (after the seal), and any
  later accepted target whose weekly freeze line exists. It is a new, separate attempt. It is never admitted to the
  league's sources and never changes a canonical figure; it is shown in labelled comparisons by named attempt.
- Neither kind alters or reopens a sealed Mode H record, a weekly record, a frozen forecast or an earlier attempt.
  Neither can make a known draw prospective or holdout evidence. Repeated runs of a draw are never added together or
  treated as independent observations. A retired revision is run only if an installed, released revision makes it
  runnable; archived code is never executed.
- The kind, the cohort and the targets are fixed in the attempt's plan. For plans of this new kind this is a recorded
  exception to the full-cohort choice of 31 October 2026 (ER-6 declined); plans of the first kind are unchanged. Once
  this is ratified, choosing another eligible window needs no new design decision; each run on the owner's PC still
  needs his go.

**7.2 The window contract** (an R3 17.3.6 amendment, not a bound edit).""")
edit("""2A. **Beyond the holdout, for a variant released later:** a development batch may also cover any accepted target dated
   before that variant's release for which the variant has no weekly record of any kind. It is read-only towards the
   weekly records: it opens no freeze line and writes nothing to the weekly ledgers. It has its own source identity in
   `LEAGUE_SOURCES_<GAME>.json`, and section 4's one-score rule stops any overlap with a weekly record.""",
     """2A. **Beyond the holdout (amended in v0.8; EX_223 B03, B04):** a routine fill may also cover an accepted target whose
   weekly freeze line was written before the variant's release instant (the `released_utc` of its release record),
   provided no weekly ticket or record exists for that pair. A target still open when the variant joined the session
   roster is the weekly session's, never a batch's. An exploratory rerun (7.1A) may cover any accepted target whose
   weekly freeze line exists. Either is read-only towards the weekly records: it opens no freeze line and writes
   nothing to the weekly ledgers. A routine fill has its own source identity in `LEAGUE_SOURCES_<GAME>.json`, and
   section 4's one-score rule stops any overlap with a weekly record.""")
edit("""untouched, and the reconstruction file marks where a variant's history is back-filled (5.3).
""",
     """untouched, and the reconstruction file marks where a variant's history is back-filled (5.3). An exploratory rerun (7.1A)
adds no row and changes no figure in this ranking (v0.8).
""")

# ---------------------------------------------------------------- sections 11 to 14
edit("""the Architecture's next edition; the runner's rulebook; the design itself, by a short amendment naming this supplement.
""",
     """the Architecture's next edition; the runner's rulebook; the design itself, by a short amendment naming this supplement;
and (v0.8) a note beside the record of ER-6 that plans of the new kind may name their variants (7.1A).
""")
edit("""- **Total TOP minus WORST matches without the variance per draw:** its luck band would have to be estimated or simulated.
""",
     """- **Total TOP minus WORST matches without the variance per draw:** its luck band would have to be estimated or simulated.
- **Stopping the formal test at the first missed week** (v0.8): the strictest reading, and simple; but over years one
  missed week is close to certain, so it would almost surely end the test early for no scientific reason. Replaced by
  the opportunity rule of 6.8, which the reviewer accepts only because the missed status is fixed before the outcome.
- **Noon by Adelaide's own clock** (v0.8): needs time-zone data and a rule for the daylight-saving change. The fixed
  instant of 6.8 is never later than Adelaide's noon and has neither.
- **Full-cohort batches only** (the choice of 31 October 2026) (v0.8): no restricted plans to review; but every new
  method would repeat every earlier run, rule 2A could not work at all, and the owner's wish to rerun any method over
  any eligible draws would be unmet. Kept unchanged for plans of the first kind.
""")
edit("""**The reviewer's recommendation (EX_213):** ratify, with RC-1 (now in 6.8).

**The owner's decisions** (his position is in decision log entry 59):
- O-1. The table and files of sections 3 and 5.
- O-2. OV-1 as the one confirmatory forward test for each game, by the evidence score of 6.5 with a bar of 40, everything
  else secondary.
- O-3. The window contract and re-forecasting rules of section 7.
- O-4. The objective of scoring Powerball targets 1145-1285; the run itself needs a separate go once its command is reviewed.
""",
     """**The reviewer's recommendation (EX_213):** ratify, with RC-1 (now in 6.8). **For v0.8:** EX_223 asked for the amendments
of section 1A; the owner gave his directions on 17 November 2026 (decision log entries 69 and 70).

**The owner's decisions** (his position is in decision log entry 59). O-1 to O-4 were approved with v0.7 (RAT-33) and
are unchanged:
- O-1. The table and files of sections 3 and 5.
- O-2. OV-1 as the one confirmatory forward test for each game, by the evidence score of 6.5 with a bar of 40, everything
  else secondary.
- O-3. The window contract and re-forecasting rules of section 7.
- O-4. The objective of scoring Powerball targets 1145-1285; the run itself needs a separate go once its command is reviewed.

**New in v0.8, for the owner's ratification:**
- O-5. The opportunity rule, the cut-off and the failure rules of 6.5 and 6.8 (his directions OD-2, OD-3 and OD-4).
- O-6. The two kinds of development run and the canonical rule (7.1A, 7.2 rule 2A, section 4 rule 2A; his direction OD-1).
- O-7. The writer, source-file and publication wording (section 4 rules 4 and 5; 5.1).
""")
edit("""and a session interrupted at every step with the table layer made to fail.
""",
     """and a session interrupted at every step with the table layer made to fail.

For v0.8 the code round must also show: every target classified as counted, skipped, missed or a stop from the records
alone, with the cut-off tested at its exact second and across both daylight-saving changes; the missed status refused
when the forecast ledger's chain is broken or its times run backwards; each stop cause planted once, with no factor
line after it; the sealed factor table equal to the one rebuilt at scoring; both kinds of development run through the
one driver, with no key counted twice and no exploratory attempt in a canonical total; and an interrupted publication
finished with the same bytes or marked incomplete, never logged as complete.
""")
edit("End of v0.7.", "End of v0.8.")

for old, new in EDITS:
    assert s.count(old) == 1, ('anchor not found exactly once', s.count(old), old[:70])
    s = s.replace(old, new)
assert all(ord(c) < 128 for c in s)
assert s.count('v0.7 (RATIFICATION CANDIDATE)') == 0
open(out, 'wb').write(s.replace('\n', '\r\n').encode('ascii'))
print(f'{len(EDITS)} counted edits; {s.count(chr(10))} lines; longest line {max(len(l) for l in s.split(chr(10)))}')
