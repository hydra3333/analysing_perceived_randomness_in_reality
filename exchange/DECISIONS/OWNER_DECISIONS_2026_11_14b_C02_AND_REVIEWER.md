# Owner decisions, 14 November 2026 (evening)

Recorded by the Claude web chat from the project owner's own words in the Claude chat. The project owner is the sole ratifier.

## 1. Replacement reviewer accepted (about 19:35 Australia/Adelaide)

Question (Claude): "The new ChatGPT chat answered all 12 takeover questions correctly (EX_180, pushed at 043adc2). Do you
accept it as the standing independent reviewer under H-2 v2 r1?"
Owner's answer: "Yes, accept it (Recommended)".

## 2. EX_177 C02, the dependency installer's own evidence (19:37 Australia/Adelaide)

Owner's words: "C02 no it's gone. a separate chatgpt did it with me and testing was examined and declared a success so
good enough for me."

As recorded: the installer run's own window output (exit status and any pip messages) is no longer available. The owner
reports that a separate ChatGPT conversation (not the project's reviewer chat, and not in this repository) went through the
installer run with him and judged it successful. The owner accepts that, with TASK_T024 (ENV PASS: every RECORD file present
and matching; 571 tests PASS), as sufficient for C02, and does not ask for a `pip check`. The separate conversation's
examination is the owner's report; it is not evidence held in this repository.

Not decided here: EX_177's B01 (whether T024 plus the default POC rerun is enough for this change as a scoped W-23
acceptance). That stays open; "W-23 PASS" is not to be written.

## 3. Mode H readiness decisions D1 to D7 (about 19:50 Australia/Adelaide)

Question (Claude): "The reviewer (EX_181) agrees with all seven recommendations for D1-D7. Do you want to decide them now,
as recommended, so they're on record for when you come back?"
Owner's answer: "Yes, all seven as recommended (Recommended)".

As decided, in the words of readiness sheet r2c section 9 and EX_181:
- D1: Oz Lotto from manifest to seal, then Powerball; a STOP in Oz Lotto is not permission to go on to Powerball.
- D2: both games, whatever the first shows, barring a technical or safety STOP; four separate gos per game.
- D3: a value-free witness push after each Approval 1 and before Approval 2, each on its own go, commit id recorded.
- D4: the official-page fetch-and-parse check is to be done (prerequisite 3), on its own go, before the first Approval 1.
- D5: updated masters and ledgers left uncommitted until both games are sealed; backups checked after each seal; any
  later push of raw files is its own decision.
- D6: the value-free report files shared together after both games are sealed, where practicable; never the score
  ledger, masters, grabs or backups.
- D7: each prerequisite and each Approval 1 to 4 on its own go, in the sheet's order, outputs inspected between steps.

These decisions authorise nothing to run. EX_177 B01 stays open, to be decided after the POC rerun (EX_181).

## 4. Owner notice: OUTLANDISH_01 work (19:46 Australia/Adelaide)

Owner's words: "I will be doing other development in the "OUTLANDISH" sub-project and "git add -A" committing from time
to time independently of this overarching project."
