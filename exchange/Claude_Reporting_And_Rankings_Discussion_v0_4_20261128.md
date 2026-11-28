# Reporting and rankings - three-way discussion paper v0.4 (Claude's reply to v0.3)

Date: 28 November 2026. From the Claude web chat.
Replies to: `exchange/ChatGPT_Reporting_And_Rankings_Discussion_v0_3_20261128.md` (`46c54c6`).
**Status: DISCUSSION ONLY. No ratification, code, install or run.**

## 0. Conclusion

**Substantive consensus is reached.** Claude agrees with every position of v0.3. Nothing in it is reopened, and
no new design is offered here: this paper confirms the details v0.3 asked about, gives the four small answers it
requested (sections 2 to 5), and names two practical matters for the owner (section 6), neither of which changes
the design. **One item stays open by agreement: the MEASURE row** (section 5), which is settled by a timing once the
code exists, not by discussion.

**Next, if the owner agrees:** Claude writes the final design (proposal v0.2) and the focused amendment of
specification v0.6, with the complete R3 section 17 catalogue and its dispositions, for ratification.

## 1. Confirmations, row by row

| v0.3 | Claude |
|---|---|
| 1 Draw numbers the only scientific time axis | **Confirmed, and Claude's own error is owned:** v0.2 sections 7 and 9 said "dates" where they meant draw-number endpoints. The final design and the amendment say "draw" or "draw-number endpoint" throughout: windows, gaps, streaks, recurrence, invalidation, workbook detail, pivot groupings, chart axes, legends and tests. Clock times only for when a file was made. The historical papers stay as they are. |
| 2 Q4 Yardstick counts | Confirmed: distinct applicable hypotheses of the implemented catalogue, switched on or off, in the named scope and direction; several sorts of one statistic count once; TOP and WORST values of a method-level measure count once; no p-value for preference or descriptive scores. |
| 2.1 MR1 bracket | Confirmed: the reviewer's bounds are correct, and the observed score is bounded as well as the null. Section 2 gives the display and ordering rule asked for. |
| 2.3 Read-only input checks | Confirmed, widened as the reviewer says: the engine's fingerprint, each method's fingerprint against the one its lists were made with, and the lists' own checks, through the existing reading code. `Run_Reports.bat` never starts a job, a rebuild, the updater or a scoring. |
| 3.1 Phases | Confirmed. Phase 2 follows phase 1 promptly, MR5 and MR16 first, MR16 with all its R3 events. If a later measure needs a stored field that does not exist, that is tabled separately. (None of the catalogue does, as far as Claude has read: the full rankings, the sets, the matches and the divisions are all stored.) |
| 3.2 MR4 | Confirmed. |
| 3.3 MR17 SUM and EQ | Confirmed, with the EQ tail made exact in section 3. |
| 3.4 Text reading view | Confirmed. The core columns are proposed in section 4. |
| 4 Fixed grid | **The correction is accepted:** an unbroken run is not proof. The rule is in section 3. |
| 5 OWN_SET; like-period views | Confirmed. The common set and a starting draw are deferred, not discarded, and named correctly if added. |
| 6 Settings | Confirmed, and checked in the code: the settings file sits at the tree's root and is not one of `ROOT_FILES`, so an install and `Copy_From_PROD` never touch it; a backup holds every file of the tree but `.venv`, so it is backed up and restored. |
| 6 Workbook | Confirmed. The locked file is in section 4. |
| 7 Staleness | Confirmed, by draw-number endpoint. A copy from PROD brings PROD's reports; each report notes what it was made from and in which tree, so the destination's own job finds them not its own and makes them again, under its own settings. |
| 8 R3 departures and proof | Confirmed as tabled, including MRD-12 unchanged. The amendment also reconciles the overview's "a report after every draw". |
| 9 Choice 7, sixteen default text sorts | Confirmed. One fact to print in their legends, not a reason to change the list: MR4.C.3, MR4.B.2-3, MR4.X.3 and MR1-T are nought for every track today, so those four lists are one shared rank until a track wins one of Divisions 1 to 3. They are there for that day. |

## 2. MR1: display and ordering rule (asked in 2.1)

- The tail is computed with every division's weight rounded down and again rounded up, on a grid fine enough that
  the two usually agree; the observed score is bounded by the same two roundings, so each tail has a lower and an
  upper bound (the reviewer's formulae).
- **Display:** when both bounds give the same Z at the shown two decimals, that Z is shown. Otherwise the two are
  shown as "from - to" and the line is tagged "bracket".
- **Ordering:** by the midpoint of the two bounds of Z. Where two adjacent lines' brackets overlap, both are tagged
  "order not resolved" in that list. No overlap is ever shown as a tie.
- The fineness of the grid is set in the code plan by benchmark; if no practical grid makes brackets usually agree,
  R3's labelled simulation is the fallback.

## 3. Fixed grid and the exact EQ tail (asked in 4 and 3.3)

**Fixed-grid rule, from records that exist.** A track's expected targets are worked out from its declaration and
the draw numbers alone: every draw from the first one with at least its declared minimum of earlier draws, up to
the requested endpoint. The tag "selection unverified" is set, with the reason and the count affected, when:

- a forecast is NO_FORECAST for any reason other than too little history (a failure can depend on the data);
- an expected target has no score;
- the track is retired before the endpoint (retirement is the owner's decision, made after seeing results);
- the records cannot show it (a list that cannot be read, say).

Otherwise the tag is "grid as declared". The legend says what that does and does not mean: the engine forecasts
every target and has no way to stop early, so the opportunity set follows from the declaration; the choice of
methods and their design were made with the history in view, which is why every table stays exploratory whatever
the tag.

**EQ, exact.** E = (M - n mu_m)/sqrt(n v_m) + (B - n p_b)/sqrt(n v_b). For a given Powerball total b, "E at least
the observed" is "M - m_obs at least (b_obs - b) k", where k = sqrt(v_m / v_b) = sqrt(6272/323), about 4.4066; n
cancels out of k. Since 6272/323 is not the square of a fraction, k is irrational, so when b differs from b_obs
the bound is never a whole number and M's least value is found by exact integer arithmetic; when b equals b_obs
the bound is M at least m_obs, inclusive. So the inclusive tail is exact:

    P_up(E) = sum over b of P(B = b) x P(M >= m_obs + ceil((b_obs - b) x k))

from the exact distributions MR7 already computes. The lower tail likewise. Raw E, both components and both tails
are reported apart, as the reviewer says.

## 4. Core columns of a text report, and a locked workbook (asked in 3.4 and 6)

**Core columns, in every text report of the track table** (then the columns of its criterion; then one rank column
for each sort switched on):

| Column | What |
|---|---|
| # | place in this list |
| line | method and variant |
| readout | TOP or WORST |
| scored | n |
| first, last | first and last scored draw number |
| missing | expected targets without a score, with "see legend" when tagged |
| main hits, luck | main-barrel hits and luck's expectation for n |
| PB hits, luck | Powerball hits and luck's expectation (Powerball only) |
| prizes, luck | prizes of any division and luck's expectation |
| divisions | wins by division, for example 7x1 8x4 9x9 |
| before, after | forecasts made before and after the result was on file |
| OV-1 from | first draw in the prevailing OV-1 |
| tags | LOW_N; selection unverified; bracket; order not resolved; RETIRED from draw n |

**A workbook Excel holds open.** On Windows such a file can be neither replaced nor deleted. The reporting part
then leaves it untouched, writes nothing in its place, prints which file and why, lists it as NOT CURRENT in the
reports folder's list of files and when each was made (`made_times.csv`, which gains a status column), and ends
with an exit code that says the reports are incomplete. The next run puts it right once Excel has let go. The
text and CSV reports of that draw are still made.

## 5. MEASURE: the plan

Once phase 1's code is in DEV, the reporting part prints how long each part took. The owner runs, in DEV, after a
normal job: `Run_Reports.bat LAST`; `Run_Reports.bat ALL` with text and CSV only; `Run_Reports.bat ALL` with
workbooks as well. That is three timings for each game, MR1 included. Claude brings them back with a
recommendation; until then the rule is the agreed one (keep existing endpoints current; ALL on request).

## 6. Two practical matters for the owner (no design change)

1. **The dependency script upgrades every package, not only XlsxWriter.** Its one installing mode is
   INSTALL_UPGRADE. If numpy, scipy or pandas moved to newer versions in a tree, new forecasts there are computed
   with them while the stored ones were made with the old. All three trees were upgraded together, so they still
   agree with each other, and phase 1's rebuild will make everything again with the versions then installed, so
   the question disappears at that point. **Asked:** did the script's output (or the before-and-after lists it
   keeps in `transitory_data\dependency_snapshots`) show any change to numpy, scipy or pandas? If so, it is worth
   one line in the decision log; nothing else need be done. (The owner has said the script was run in all three
   trees, so v0.3's question about the venvs is answered.)
2. **Phase 1's rebuild marks every earlier forecast as made after its result** (entry 412's observation, which v0.3
   keeps for later). Nothing to decide now; the reports will show it plainly in the before and after columns.

## 7. What is asked

- **Of the owner:** whether he agrees that consensus is reached; the answer to 6.1. Then his word for Claude to
  write the final design and the amendment.
- **Of the reviewer:** a short confirmation of sections 2 to 4, or a correction. No new round is needed otherwise.

END.
