# MHUP-B design supplement - DRAFT v0.1

**Status: a first draft by the Claude web chat, written unattended on the night of 16 November 2026 (on Fable). Not
reviewed, not ratified, and it authorises nothing.** It applies the owner's inputs of 16 November 2026
(`exchange/DECISIONS/MHUPB_DESIGN_INPUTS_2026_11_16.md`, D-1 to D-10) to the ratified design
(`doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r7.md`, called "the design" below).

## 0. In plain English

- **Most of MHUP-B is already designed and ratified.** Section 6 of the design sets out the weekly session in full: update,
  catch up missed draws in order, score, freeze the next forecast, and write a dated league table. That design went through
  several review rounds. **This supplement does not reopen it.** It adds the parts the owner asked for on 16 November.
- **What it adds:** the league table's layout (every method, an all-draws column, a forward-only column); numbered,
  dated table files with CSV; a history file giving the table after every past draw; and a plain statement of how long
  forward testing takes to show anything.
- **One recommendation the owner should see first (section 7):** every week without MHUP-B turns a forward draw into a
  catch-up draw, and forward draws are the only evidence that can confirm anything. So MHUP-B should carry **no extra scope
  that can wait**. Two wanted items can wait without loss and are proposed as a small follow-on package: a new method's
  back-history, and lifting the report tool's window cap.
- **One sobering fact (section 5):** with weekly draws, confirming that a method beats chance by 10% takes about **15 years**
  under the present 80-track test, or about **6 years** if one overall measure is fixed in advance. A 50% edge shows in under
  a year. This is arithmetic, not pessimism, and it bears on what the project chooses to measure.

## 1. What is already settled (the design, unchanged)

| Topic | Where | In one line |
|---|---|---|
| The weekly command and its three programs | 6.1 | One command per session; forecasting and scoring halves; one launcher each |
| The status block | 6.2 | Per game: last accepted draw, backlog, next target and deadline, active variants |
| Order across weeks and interruptions | 6.3, Appendix F | One target at a time; nothing scored twice; a draw without an accepted result stays open |
| Labels | 6.4, Appendix I | `CATCH_UP`, development and `FINAL_NEXT_DRAW` by a fixed rule; effective class `PROSPECTIVE` or `LATE_PRE_DRAW` |
| The timing proof | 6.5, Appendix G | Forecast and witness ledgers; offline; GitHub an optional witness |
| Scores and the league table | 6.6 | One score ledger; a dated cumulative table each session; full report with N1 monthly or on request |
| FINAL and "developed" | 6.7 | The weekly session is R3's FINAL protocol; the owner's declaration record |
| The owner's checklist | 7 | The update procedure and the session steps |

The labels stay. They are written by the programs and cost the owner nothing. "All draws are treated the same" changes who
may see the data and how the table adds it up; it does not remove the record of when each forecast was frozen.

## 2. S-1: the league table (D-1, and the owner's sketch)

**2.1 Rows.** One row for every method, revision and variant that has at least one scored draw: 40 per game today. Never a
top few. A short roll-up by method (12 lines today) sits above the full table.

**2.2 Columns, main table** (the TOP ticket: the method's seven most favoured numbers):

| Block | Columns | Meaning |
|---|---|---|
| All scored draws | Draws, Hits, Chance, +/- % | Every draw with a routine score for that variant, whatever its label, added up |
| Forward only | Draws, Hits, Chance | Only forecasts frozen before their draw (`PROSPECTIVE`) |
| Last 10 | Hits | Recent form over the ten latest scored draws |

**2.3 A second table, same rows:** the split by kind (development, Mode H, catch-up, forward); the WORST ticket's hits (a
method whose least favoured numbers keep being drawn is as informative as one whose favoured numbers are); for Powerball,
the Powerball-number hits; prize-division counts.

**2.4 Order.** Sorted by hits above chance per draw over all scored draws (a rate, so that variants with different numbers
of draws compare fairly), then by the forward-only rate. The number of draws is always shown beside every figure (design
6.6: "shown, never hidden").

**2.5 Where the numbers come from.** Hits add up, so the all-draws total is the sum of the per-draw matches already held
in three places: the development score records (the reports of 1 November 2026), the sealed Mode H score ledgers, and the
weekly score ledger. The table reads them; it rescores nothing and changes nothing. One canonical source per kind is named
in the table's header, with each source's identity.

**2.6 What the all-draws column is not.** It carries **no P value and no significance mark**. It mixes kinds of evidence, so
it is a description. The formal comparison with chance stays where the design puts it: N1 and the family tables over the
forward and catch-up records, in the full report. This is the reviewer's condition (EX_203) built into the layout.

**2.7 A plain yardstick line under the table**, so the percentages are not over-read. Example wording: "Over 448 draws one
method's hits vary by about 3% either way from luck alone; among 40 methods the luckiest is usually further out than that."
The first figure is exact arithmetic from the fair-draw distribution (Powerball: 21.7% at 10 draws, 9.5% at 52, 6.7% at
104, 4.3% at 260, 3.2% at 448; Oz Lotto: 26.6%, 11.7%, 8.3%, 5.2%, 4.0%). The second comes from the N1 replay when the
full report is run.

## 3. S-2: files, names and archive (D-2, D-3)

- **Name:** `league_<GAME>_d<draw, 5 digits>_v<version, 5 digits>_<UTC date-time>.txt`, and the same with `.csv`.
  Example: `league_POWERBALL_d01592_v00001_20261119T131500Z.txt`.
- **Never overwritten** (create-only, as R3 17.10.1 already requires of report files). A second table for the same draw, for
  example after a new method is released, takes the next version number. The newest file is the current ranking; every
  earlier one stays as its own archived file. The date-time keeps several in one day apart.
- **Folder:** `results/method_rankings/<GAME>/league/`. Tracked in Git.
- **Each table is logged** in the search log (`WEEKLY_TABLE`, design 6.6).
- **History on request:** one command joins the tables, newest first, into one dated file. It reads the files; it
  recomputes nothing.
- **CSV:** one header row; one row per variant; the same columns as the two tables; plain numbers; UTF-8.

## 4. S-3: the table after every past draw (D-4)

One CSV per game, written on request: one row per draw and variant, with that draw's matches, the running total, the
running chance figure and the rank after that draw, each row carrying its kind. About 18,000 rows for Powerball today.
From it the owner can see the ranking as it stood after any draw, chart a method's course, or filter in a spreadsheet.
It is descriptive and logged. This closes the gap "no table after every draw over the history" without one file per past
draw.

## 5. S-4: how long forward testing takes (D-10)

Planning arithmetic for a single ticket rule, from the exact fair-draw mean and spread per draw and a normal approximation
(to be checked by the reviewer; a proper calculation belongs in the code round):

| True edge over chance | Draws for an 80% chance of passing the 80-track family test | Draws if one measure is fixed in advance |
|---|---|---|
| Powerball 50% | 32 (0.6 years) | 12 |
| Powerball 20% | 195 (3.7 years) | 73 (1.4 years) |
| Powerball 10% | 780 (15 years) | 291 (5.6 years) |
| Powerball 5% | 3,117 (60 years) | 1,164 (22 years) |
| Oz Lotto 20% | 294 (5.6 years) | 110 (2.1 years) |
| Oz Lotto 10% | 1,176 (23 years) | 439 (8.4 years) |

What follows from it:
1. Forward evidence is slow for small edges whatever the software does. The league table should say so in plain words.
2. Testing 80 tracks at once costs a factor of about 2.7 in time against one predeclared measure. This is the case for
   fixing **one overall measure in advance** (EX_201's suggestion 3; D-1's neighbour): for example the total TOP minus WORST
   main matches over all current variants, calibrated by N1. **Proposed as a design question, not adopted here.**
3. Catch-up draws do not shorten these times as confirmation: they are retrospective. They do add description.

## 6. Smaller items

- **D-7, the HX-2 flag** (Powerball 1587 and 1588): **keep it as ratified.** It is already specified, it is automatic, and
  removing it is a design change that would itself need review. Keeping costs nothing.
- **D-8, the local runner's rules 4 and 5:** proposed wording for MHUP-B's rulebook edition: "4. (withdrawn 2026: draw values
  are no longer hidden.) 5. You may read files under `source_data`, `results` and `transitory_data` when a task says so. You
  never create, change, move or delete anything there." The rulebook's write limit (its section 3) and rules 6 to 10 stay.
- **The first session's catch-up list**, from the design's rule (6.4) and the weekly calendar, to be confirmed by the
  program: Oz Lotto 1704 to 1708 and Powerball 1587 to 1591. For each variant, a draw dated before the variant's release
  date in the install and release records is development evidence, and a later one is catch-up (E_1 revision 3's release
  date is 13 November 2026). The programs decide this and print it in the status block; nobody labels by hand.

## 7. Recommendation on scope and order (D-5, D-6, D-9)

**Keep MHUP-B to the ratified section 6 plus sections 2 to 4 of this supplement.** Reason: each week without the weekly
session is a forward draw lost for good (it can only be caught up, and catch-up cannot confirm). Oz Lotto 1709 is drawn on
17 November 2026 and Powerball 1592 on 19 November; neither will be forward evidence. Nothing recovers a missed week, so
the package that starts the forward record should not wait for anything that can follow it.

**A small follow-on package ("MHUP-C" as a working name)**, needed only when the next method is released:
- a new method's **back-history**: one development walk-forward batch over every draw from the first to the latest
  accepted, the sealed holdout draws included, labelled development evidence; this is what makes "a new method re-ranks all
  draws" true (roadmap item 21b);
- **the report tool's window cap** (R3 17.3.6, Phase 1) lifted once a game's `MODE_H_SEALED` marker exists;
- the consolidated report across kinds (roadmap item 21b).

**D-6, Powerball targets 1145 to 1285:** no new code. The installed report tool accepts that window today. One owner-run
report (logged; under half an hour on the last timing) gives their scores, and the all-draws column then starts at the first
target. Proposed as an owner's go after MHUP-B's design review, not before.

## 8. Alternatives considered

- **One combined total only, no labels:** simplest to read, but it would hide which results were frozen before their draw,
  and that is the only part that can ever confirm an edge. Rejected; the sketch the owner liked already shows both.
- **One file per past draw for the history:** thousands of files for no gain over one CSV. Rejected in favour of section 4;
  the numbered files of section 3 still exist for every table actually published.
- **Put the back-history and the cap into MHUP-B:** one package instead of two, but it delays the forward record by the
  time it takes to design, review and test them. Rejected for the reason in section 7.
- **Drop the HX-2 flag for simplicity:** a change to a ratified design to remove something automatic. Rejected.

## 9. For the reviewer and the owner

**Questions for the reviewer**
- R-1. Section 2.6: is "no P value on the all-draws column, formal tests on forward and catch-up only" the right line?
- R-2. Section 2.4: is hits above chance per draw the right sort key, given variants with different numbers of draws?
- R-3. Section 5: please check the arithmetic and say whether one predeclared overall measure should be designed now.
- R-4. Section 7: do you agree MHUP-B should carry no scope that can wait, with the follow-on package as described?
- R-5. Anything in sections 2 to 4 that conflicts with the design's sections 6.4 to 6.6 or Appendix I?

**Decisions for the owner (after the reviewer's view)**
- O-1. The table layout of section 2 and the file names of section 3.
- O-2. MHUP-B's scope as section 7 recommends, with the follow-on package.
- O-3. Whether one overall measure is fixed in advance (section 5, point 2).
- O-4. A go, later, for the one report run of D-6.

## 10. What comes next

1. The owner reads section 0 and says whether the direction is right.
2. This draft, corrected, goes to the reviewer with the agreed approach.
3. On the owner's decisions: the code plan (the design's section 8 lists MHUP-B's members), then code, review, the Windows
   rehearsal and the owner's install, each on its own go.

End of draft v0.1.
