# A reporting part separate from the engine, and the rankings the owner asked for (proposal v0.1)

Date: 28 November 2026. From the Claude web chat, for the owner's reading first, then the reviewer's.
**Status: PROPOSAL. Nothing in it is done, decided or authorised.** Decision log entries 410 and 411.

## 0. In short

- The league table is ordered by one thing only: the TOP ticket's main-barrel hits. The owner's own ranking
  decisions (R3 v0.5 section 17, ratified 26 October 2026) were never built in the living system.
- Proposed: **a reporting part that is separate from the engine.** It reads what the engine has already stored and
  computes no forecast and no score. It makes one table of lines, where **each method's TOP ticket and WORST ticket
  is a line of its own**, and prints that table **once for each ranking criterion, ordered by that criterion**, with
  a column of ranks for every criterion at the right.
- **Every report begins with a plain-English introduction and ends with a legend** that explains every column and
  every criterion, each with a small worked example, and states **the yardstick**: how far the first of N lines gets
  by luck alone.
- The cost is one change to the engine, so one rebuild in each tree, once. After that, a change to any report
  rebuilds nothing: only the reports are made again.

## 1. What arose (the issues)

| # | Issue |
|---|---|
| I1 | The owner's ranking decisions (MRD-01 to MRD-24; R3 section 17: MR0, MR1, his MR1-T and the rest) are not in the living system. Specification v0.6 section 9 left them "on request"; nothing was built, and no handover named it as owed. |
| I2 | The one order of the league uses the main barrel alone. The Powerball barrel and the prize divisions (which need both barrels) are shown as columns but take no part in the order. |
| I3 | TOP and WORST are folded into one line and the order is TOP's. A WORST ticket that leads every TOP ticket is not seen. Luck that runs the wrong way ("anti-luck") is a finding the project looks for on purpose. |
| I4 | The order is by hits a draw. A line with few draws swings further by luck than a line with many, so short histories crowd both ends of the list. No figure allows for the number of draws. |
| I5 | There is no yardstick. Any list has a first line. Nothing says how far ahead the first of N lines would be if every line were luck alone. |
| I6 | The columns are not explained in the file. The reader needs the manual, which has no worked example of a league line (and one wrong figure, to be corrected). |
| I7 | The reports are part of the engine. A change to the wording of a report changes the engine's fingerprint, and every tree then makes everything again (about 49 minutes each). |
| I8 | The one program that ever computed the owner's rankings is the frozen first system's `Method_Rankings_Report.py`, which the tidy is to retire. It reads the first system's files and cannot be used on the trees. |

## 2. The proposal

### 2.1 A reporting part, outside the engine

- **The engine keeps everything that computes and stores:** forecasts, scores, both OV-1 series.
- **The reporting part takes everything that only prints:** the ranking reports (which replace the league table),
  the next-draw reports and the two OV-1 print-outs. The last two move as they are: their bytes are to be the same
  before and after the move, which is the test that the move changed nothing.
- It lives in `src/reporting/`, beside `src/updater/`, and is treated as the updater is (entry 356): **it is not
  part of the engine's fingerprint.** It has a fingerprint of its own, kept beside the reports it made. When that
  differs, the reports are made again, in seconds or a few minutes; no forecast or score is touched.
- It reads through the engine's own reading code, under the tree's lock, and writes only under
  `results/research/<GAME>/reports/`. Nothing it writes is ever read back by the engine. Games are never pooled.
- Every research job ends by making the reports for the latest draw. If the reporting part fails, the job says so;
  the forecasts and scores it made stand.

### 2.2 The lines: TOP and WORST each on its own

- A **line** is one ticket of one method: its TOP ticket or its WORST ticket. With 40 methods a game there are 80
  lines. R3 17.3.4 already calls this a "track"; the simple league folded the two into one line.
- **The 80 lines are ranked together, by the same rule, with no allowance for which kind they are.** A WORST line
  near the top of a list is hitting more than luck (the method's "least likely" numbers are being drawn). A line of
  either kind at the bottom is hitting less than luck. Both ends of every list are of interest.
- A column says TOP or WORST. The legend says that a method's TOP and WORST come from one ranking and never share a
  number, so the two lines of one method are not two independent pieces of evidence.

### 2.3 The ranking criteria to start with

The codes are R3's (the owner's decision MRD-07), so that the ratified definitions carry over word for word.

| Code | Short title | Barrels | The list is ordered by | Luck figure |
|---|---|---|---|---|
| MR7 | main hits | main | Z of the total main-barrel hits | exact |
| MR7.PB | Powerball hits | Powerball (not Oz Lotto) | Z of the times the Powerball was picked | exact |
| MR4 | prizes won | both | Z of the number of prizes of any division | exact |
| MR0 | best divisions | both | prizes by division, best division first | exact, for the best division |
| MR1 | prize rarity | both | Z of the total "bits of surprise" of the prizes | exact |
| MR1-T | owner's 90/7/3 | both | 0.90 x Division 1 + 0.07 x Division 2 + 0.03 x Division 3, a draw | none (a preference score) |

- For Oz Lotto "both" reads "main and supplementaries": methods never forecast supplementaries (MRD-03); the
  supplementaries drawn count toward the division, as the operator counts them.
- Changed from what Claude first listed in the chat: hits a draw and its Z are one list, not two (the list is
  ordered by Z, with hits a draw beside it), and "prizes won" is added because it is the simplest figure that uses
  both barrels and has an exact luck figure.
- **More criteria are added one at a time later** (R3 has seventeen), each with its legend. None costs a rebuild.
- MR1-T is nought for every line today, as luck expects (Division 3 is about 1 in 686,000 a ticket). It is there for
  the day it is not.

### 2.4 The luck figure "Z", in plain English

One definition serves every criterion that has one.

- **Z says how far a line's total is from what luck alone gives, allowing for how many draws the line has.**
  0 is exactly luck. Plus is more than luck, minus is less. By luck alone about one line in 6 is beyond +1, one in
  44 beyond +2, one in 740 beyond +3, and the same for minus.
- It is worked from the exact chance, under fair draws, of a total at least as high (or at least as low) as the
  line's, and that chance is written on the sigma scale the owner chose (MRD-06; R3 17.5.1). The chance itself is
  in the .csv.
- **Worked example (invented figures):** a line has 300 scored draws and 455 main-barrel hits. Luck gives 1.400 a
  draw, so 420.0 in 300 draws. The line is 35 hits ahead. Luck's own spread over 300 draws is about 16.6 hits. 35 is
  about 2.1 spreads: Z = +2.1.
- **Why the exact chance and not the bell-curve shortcut.** Two cases from the Powerball prize table:
  - A line with 29 draws and no prize. The shortcut gives -0.8, as if it were unlucky. In truth no prize in 29
    draws is what luck gives about half the time: Z is 0.
  - A line that won Division 1 once in 400 draws and nothing else. The chance of that is about 3 in a million
    (+4.5). Yet its prize-rarity total, MR1, is below luck's average (about -1.8), because one great prize weighs
    less in that total than the dozen small ones the line did not win. **So MR1 never stands alone:** MR0 and the
    owner's MR1-T put the best division first, and MR0's luck figure is the chance of the line's best division, or a
    better one, at least once in its draws.
- These exact figures hold for each line by itself, whatever the method does, because a fair draw does not depend
  on what was drawn before (R3 17.5.3: "stay exact under adaptive walk-forward").

### 2.5 The yardstick, stated in every report

- **What it is.** A ranked list always has a first line. The yardstick says how far the first of N lines gets when
  every line is luck alone. The ranking says where to look; the yardstick says whether there is anything to see.
- **What is printed**, for the N lines of that list, and the same with minus for the other end:
  - "By luck alone the first of 80 lines is typically near +2.4." (Approximate: it treats the lines as
    independent, which they are not quite.)
  - "Beyond +3.2 would be unusual: by luck, once in 20 such lists." (Guaranteed however the lines depend on each
    other: R3 17.5.3, Bonferroni over exact figures.)
  - "Across every list of both games, at both ends: beyond about +4.0." (The same guarantee over all of them.)
- The words that stay: "A descriptive order. It selects nothing." A line beyond the yardstick is a reason to look
  and to wait for new draws; it is not a result of the project.

### 2.6 One table, ordered several ways

- **Every report of a draw holds the same lines and the same columns.** Only the order differs: one report for
  each criterion, ordered by it. At the right is a column of ranks for every criterion (1 to 80; ties share a rank).
  A line that is high in one list and nowhere in the others is what luck looks like; the rank columns show it at a
  glance.
- **Column headings carry the code and the short title,** for example "MR7 main hits Z" and "rank MR7".
- The columns of the present league are kept, now for the one ticket of the line: draws, hits, hits a draw, luck's
  figure, the difference, the last ten draws, Powerball hits, divisions won, first scored draw, forecasts made
  before and after the result, first draw in the prevailing OV-1, NO_FORECAST counts, the retirement note.
- **Files** (names for discussion), under `results/research/<GAME>/reports/rankings/d<draw>/`:

      rank_POWERBALL_d01593_MR7_main_hits.txt
      rank_POWERBALL_d01593_MR7PB_powerball_hits.txt
      rank_POWERBALL_d01593_MR4_prizes_won.txt
      rank_POWERBALL_d01593_MR0_best_divisions.txt
      rank_POWERBALL_d01593_MR1_prize_rarity.txt
      rank_POWERBALL_d01593_MR1T_owner_90_7_3.txt
      rank_POWERBALL_d01593.csv        (the same lines and columns once, under full names, for a spreadsheet)

### 2.7 A plain-English introduction and a legend in every report

Because one part makes every report, one rule covers them all, the next-draw reports and OV-1 print-outs included
(theirs can follow the rankings; no rebuild is needed for it).

- **At the top:** what the report is, in three or four plain lines; the game and the draw it runs to; which tree
  made it; the yardstick; the standing words ("A descriptive order. It selects nothing.").
- **Under the table, a legend:**
  - every column, one by one: what it is and how to read a number in it;
  - every criterion: its code, its short title, what it measures in plain words, what its Z means, and **a worked
    example taken from the first line of that very report**, so the arithmetic can be followed with the table;
  - what TOP and WORST are, and what a WORST line at the top or at the bottom means;
  - the divisions of the game with their odds, and how "7x1 8x4 9x9" is read (Division 7 once, 8 four times, 9
    nine times);
  - what the report does not say.
- A sketch (invented figures; a real report is wider):

      RANKING - POWERBALL - through draw 1593 - ordered by MR7: main-barrel hits against luck
      Each line is one ticket of one method: its TOP seven (most likely) or its WORST seven (least likely).
      Plus Z = more hits than luck; minus = fewer. 80 lines. A descriptive order. It selects nothing.
      By luck alone the first of 80 is typically near +2.4; beyond +3.2 would be unusual. The same, minus, at the foot.

      #   line                         draws  main hits  luck   MR7 main hits Z  ...  rank MR7  rank MR4  rank MR0
      1   E_901/INVENTED_A_V1  WORST   300    455        420.0  +2.1             ...  1         33        13
      2   E_902/INVENTED_B_V1  TOP     240    364        336.0  +1.9             ...  2         23        54

      LEGEND
      MR7 main hits Z   How far the line's main-barrel hits are from luck, allowing for its number of draws.
                        Line 1: 300 draws, 455 hits; luck gives 1.400 a draw = 420.0; 35 ahead; luck's spread
                        over 300 draws is about 16.6; so Z = +2.1.

### 2.8 Which draws, and never a stale report

- **LAST** (the default, and what every job does at its end): the reports through the latest scored draw.
- **DRAW n:** the reports through draw n.
- **ALL:** the reports through every scored draw (some thousands of files; minutes).
- Specification v0.6 section 9 says no report made by old code or from old records is left in the active folder.
  That is kept: the reporting part notes what its reports were made from (its own fingerprint, the engine's, the
  methods, and the lists as they stood). When any of that has changed for earlier draws, it removes the earlier
  draws' reports and says so; the owner asks for ALL or DRAW n again if he wants them. A new draw alone changes
  nothing earlier, so earlier reports stay.

### 2.9 The commands

- `Run_Research.bat` as now; it ends by making LAST.
- A new launcher in every tree, `Run_Reports.bat [LAST | ALL | DRAW <n>] [--game POWERBALL|OZLOTTO|BOTH]`, for the
  reports alone. It computes nothing but reports and can be run at any time the tree is not busy.

## 3. How it fits the architecture (read in the code)

- **Everything needed is already stored.** For every method and scored draw, `forecasts.jsonl` holds the whole
  ranking of each barrel with the TOP and WORST sets, and `scores.jsonl` holds the matches in each barrel for each
  set, the division each set would have won and, for Oz Lotto, the supplementary matches
  (`src/research/scoring.py`). The reporting part asks the engine for nothing new.
- **The precedent exists.** `src/research/code_identity.py` already leaves `src/updater/` out of the engine's
  fingerprint and gives it one of its own. The reporting part is a second case of the same rule.
- **Reports are already "print-outs, never read back by the job"** (`src/research/reports.py`, its first lines).
- **What changes in the engine, once:** `reports.py` leaves `src/research/`; the fingerprint leaves
  `src/reporting/` out; the job ends by starting the reporting part instead of making reports itself. Nothing that
  computes a forecast, a score or an OV-1 series is touched.
- **Installing:** the reporting part goes with the infrastructure, under the same `I_AM_INSTALLABLE` flag. An
  install that changes only the reporting part makes nothing again but the reports. (The install message that says
  "only the updater or the launchers differ" is widened at the same time; it was already owed.)

## 4. How each issue is answered

| Issue | Answer |
|---|---|
| I1 rankings never built | 2.3: MR0, MR1 and MR1-T first, under R3's codes and definitions; the rest of R3 section 17 one at a time. |
| I2 one barrel in the order | 2.3: a list for each barrel, and four lists that use both through the prize divisions. |
| I3 WORST hidden; anti-luck | 2.2: TOP and WORST lines ranked together; both ends of every list read. |
| I4 short histories | 2.4: lists ordered by Z, which allows for the number of draws, from the exact chance. |
| I5 no yardstick | 2.5: stated at the top of every report, for both ends. |
| I6 columns unexplained | 2.7: an introduction and a legend with worked examples in every report. |
| I7 report changes rebuild all | 2.1 and 3: the reporting part is outside the engine's fingerprint. |
| I8 the old program retires | The living system gets its own. The tidy's list names the old one as the past implementation; R3 stays in `doc/`. |

## 5. What does not change

- Method-facing N-1 isolation; the forecasts and scores and how they are made; TOP and WORST from one ranking.
- Both OV-1 series and what they claim. **OV-1 stays main-barrel only**, as ratified; that is named here because the
  owner raised the barrels, and is not proposed for change.
- Games are never pooled. The sealed Mode H records are not touched. The updater is not touched.
- Everything the reports say stays exploratory and descriptive. The exact figures hold draw by draw, but the
  methods were designed with the history in view and their early forecasts were computed afterwards, so no figure
  here is a finding. That is what new draws after a method's establishment are for.

## 6. Related changes

- **Specification v0.6 section 9** is amended (the league report replaced by the ranking reports; the reporting
  part; LAST, ALL and DRAW), to be ratified with this proposal's final form.
- **The operations manual:** section 2 is rewritten for the new reports (the wrong Oz Lotto chance figure goes with
  the old table; 49/47 = 1.043 is the right one); most of the explaining moves into the reports' own legends.
- **The tidy** follows this work and is unchanged by it, except for the line of I8.

## 7. Cost, proof and order of work

- **Work:** this proposal agreed; a short code plan; the code and its tests in DEV (reviewer reads the commit); the
  section 9 amendment and the manual; one install.
- **Proof that the engine's one change altered nothing:** DEV makes everything again; every `forecasts.jsonl`,
  `scores.jsonl` and OV-1 series file must then have the same bytes as in the backup made just before, and the
  next-draw and OV-1 print-outs the same bytes too.
- **Installing, two routes (the owner's choice at the time; neither needs new code):**
  - **A, the usual order:** DEV, then `Install.bat QA`, then `Install.bat PROD`. Three rebuilds of about 49 minutes,
    all unattended. QA tries the change before PROD has it.
  - **B, the owner's suggestion:** DEV, then `Install.bat PROD`, then `Copy_From_PROD.bat both QA`. Two rebuilds;
    QA takes PROD's software and data and has nothing to make again. It works as the commands stand. PROD is backed
    up before the install as always. What is given up: QA as a separate trial of this one change, and QA's results
    as a third independent computation (DEV and PROD remain two).
  - Claude's view: B is sound for this change if the proof above passes in DEV, since the engine computes nothing
    new; A costs only unattended time. Either.

## 8. Tests (permanent, on invented draws)

- Each criterion's figures on a small invented history, worked by hand in the test; ranks and ties.
- The exact chances against a brute-force count on a small invented game, and against R3's own examples (for one:
  no Powerball Division 9 win in 291 draws is 2.29 deficit sigma, R3 17.5.1).
- Every report has its introduction, its yardstick and a legend entry for every column and criterion it prints.
- LAST, DRAW n and ALL; an earlier report is removed when what it was made from has changed, and kept otherwise.
- A change to the reporting part changes no forecast, score or OV-1 file and not the engine's fingerprint.
- The next-draw and OV-1 print-outs have the same bytes after the move as before it.

## 9. Uncertainties, and questions for the reviewer

- **Q1. Scope of the move.** All printing leaves the engine at once (proposed), or the league alone now and the
  next-draw and OV-1 print-outs later (a second rebuild then)?
- **Q2. MR1's luck figure.** R3 foresaw a simulation (N1). An exact figure is possible, because under fair draws
  the division won at each draw has the same fixed chances whatever the ticket: a prototype computed it in about a
  minute, unoptimised. Proposed: exact, brought to seconds in the code plan; else the simulation as R3 has it. Is
  exact acceptable in place of N1 for this one figure?
- **Q3. One signed Z for display** (plus above luck, minus below, from whichever exact chance is the smaller),
  with R3's two figures (excess and deficit) and both chances in the .csv. Acceptable, or two columns?
- **Q4. The yardstick's three lines** (2.5): is the "typically near" line, which treats lines as independent,
  acceptable when labelled approximate, beside the guaranteed line?
- **Q5. The lines of one method** (TOP and WORST) are dependent, and several methods are near copies of each other.
  The guaranteed line allows for any dependence; is a note in the legend enough, or should near copies be marked?
- **Q6. Staleness** (2.8): is "remove earlier draws' reports when what they were made from has changed" the right
  reading of section 9, in place of making every draw's reports again at every job?
- **Q7. Anything in R3 section 17 that this simple form would contradict** and that Claude has missed.

## 10. What is asked

- **Of the owner:** read this; say what is wrong or missing; then relay it to the reviewer.
- **Of the reviewer:** agreement or corrections, and answers to Q1 to Q7.
- **Then:** the owner's decision; Claude's code plan. Nothing is built before that, and nothing is installed or
  run without the owner's separate go.
