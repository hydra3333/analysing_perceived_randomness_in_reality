# MHUP-B design inputs gathered on 16 November 2026

**Status: notes for the MHUP-B design. Not a design, not reviewed, and nothing here is authorised or in force.**
Kept so that no input is lost if a chat ends. The owner's exact words are in decision log entries 42 to 46.

## 1. What the owner asked for

1. The missing code is to be fixed "asap": the sealed holdout draws and every later draw are processed like any other draw.
2. A league table after every new draw, including after a small catch-up of missed weeks.
3. He is most interested in the **latest** ranking and performance against chance, based on each method's hits over all
   draws scored so far.
4. Earlier rankings may be kept as separate files (by game, draw number and a five-digit version) and joined into one report
   on request; neat columns or CSV; laid out for a non-specialist reader.
5. All draws are treated the same; no holdout for future method development; a new method re-ranks all draws to the latest.
6. Added 22:58, on seeing the sketch of section 4: "I like the sketch as a starting point for your design , it could
   include all methods not only the top "n"." So the table lists **every method and every variant** (40 rows per game
   today), never only a top few. The ".." in the sketch only shortens the sample.

## 2. What already exists (checked 16 November 2026)

- The ranking is already cumulative and hit-based: for each method, the matches of its TOP seven picks added over every
  scored draw of the window, beside what fair draws give (MR7), with the Powerball-number hits, the prize-division scores
  (MR1, MR1-T, MR16) and the average rank position of the drawn numbers (MR5). The owner's recollection is right.
- The ratified design (Mode H, update and prospective design v0.1r7, section 6.6) already has each weekly session write a
  dated cumulative league table, with the kinds of evidence in separate columns, and a full report with N1 monthly or on
  request. This is MHUP-B's scope, marked HIGH.
- The report tool ranks over one chosen window. It has no table after each draw and refuses any window beyond 1576
  (Powerball) or 1693 (Oz Lotto) (R3 17.3.6, Phase 1). The Powerball development report starts at 1286 (R3's default start,
  the first draw of 2021); targets 1145 to 1285 are forecast and frozen but not in a report.

## 3. Items for the MHUP-B design to settle (each needs the reviewer's review and the owner's decision)

| # | Item | Note |
|---|---|---|
| D-1 | An "all scored draws" column in the league table: one cumulative figure per method over every draw scored, whatever its kind. Every variant of every method is a row; a short per-method roll-up may sit above it | New. The design today has only the separate columns. The forward-only column stays beside it: only forecasts frozen before their draw can confirm anything |
| D-2 | Numbered table files, never overwritten: `league_<GAME>_d<draw>_v<5 digits>_<date-time>.txt` and the same as `.csv`. Each superseded ranking stays as its own archived file | The owner's naming idea, with his 23:07 addition: the date and time in the name, so several in one session or day never collide |
| D-3 | A history report on request: the numbered tables joined, newest first | The owner's idea |
| D-4 | One CSV per game with a row per draw and method (cumulative hits and rank after that draw) | Gives the table after every draw for the whole past from the score records, without one file per past draw |
| D-5 | Raise the report window cap (R3 17.3.6) so the sealed holdout and later draws are ordinary history | Code and an R3 edition |
| D-6 | Powerball targets 1145 to 1285 in the all-history view | Already forecast; scoring them is a new logged run |
| D-7 | The HX-2 flag (Powerball 1587, 1588): keep or drop | Catch-up evidence is already labelled retrospective |
| D-8 | The runner's rulebook rules 4 and 5 reworded to read-only inside MHUP-B's rulebook edition | Owner agreed 22:51, on condition the runner never interferes with data |
| D-9 | Whether roadmap item 21b (the consolidated report; a new method's back-history) comes forward to sit with or right after MHUP-B | A roadmap change: the owner's decision |
| D-10 | A proper power statement for the league table's "against chance" figures | From EX_203: thresholds are not power |
| D-11 | A `current` folder holding only the newest table set, with every table kept for ever in an archive folder | Owner, 17 November 2026 (decision log entry 58): the archive is create-only and never moves; `current` is a replaceable copy |

## 4. Sketch of the latest league table (layout only; the numbers are invented)

```
POWERBALL league table after draw 1592          file: league_POWERBALL_d01592_v00001.txt

                         ----- all scored draws -----    --- forward only ---   last 10
Rank  Method / variant   Draws   Hits  Chance   +/- %    Draws  Hits  Chance      Hits
   1  Method A / v2        448    671     627    +7.0        1     2     1.4        16
   2  Method C / v1        448    655     627    +4.4        1     1     1.4        13
  ..
  40  Method F / v3        448    590     627    -5.9        1     0     1.4        11
```

- **Hits:** how many of the method's seven top picks were drawn, added over the draws. **Chance:** what random picks get.
- **Forward only:** draws whose forecast was frozen before the draw. **Last 10:** recent form.
- Below it in the real file: the Powerball-number hits, the prize divisions, the split by kind of evidence, and a plain
  note that a lead of a few per cent is what luck produces among 40 methods. The formal statistics stay in the full report.

End of notes.
