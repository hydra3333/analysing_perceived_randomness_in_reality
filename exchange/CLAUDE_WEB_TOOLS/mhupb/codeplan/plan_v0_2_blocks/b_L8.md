### L8. The two sequencers, their launchers and the rest

- **Both are sequencers in the sense of Des 6.1, not coordinators.** They import neither `methods` nor `evaluation`,
  start each child through its launcher, read its output to the end, stop on a non-zero exit, hold no state, and never
  terminate, poll or look up a process. They share one small child-launching module, so the rules are written once.
- **`Run_Weekly_Session.bat --game G`** (Des Appendix F, with the supplement's additions): status; open or resume; the
  loop of `next` and `score`, with OV-1's `record` after each score; on `FROZE_NEXT`, `record` at once; `close-session`;
  then, and only then, the league table's `publish` (which first repairs any unfinished publication); the status
  block.
- **`Run_Development_Batch.bat --game G --fill`**, or **`--rerun --variants ... --first S --last L`** (new; EX_223 C04):
  plan; run; report; then for a fill, `admit` and `publish`. A third form, `--report --batch B --first S --last L`,
  scores forecasts an existing batch already holds, then `admit` and `publish`: it is how the Powerball 1145-1285
  scores of O-4 are made, with no forecast run again. Rerunning the command with the batch it printed continues
  from the records alone: an unfinished batch is run on, a batch without a report is reported, an unadmitted fill is
  admitted. It opens no weekly record. It is a new launch interface, so the Architecture's next edition names it
  beside the weekly one.
- **Exit statuses, distinct:** 0 complete; one value for "frozen; table not written"; one for "frozen; OV-1 recorder
  failed"; another for a stop of the live path or of a batch, naming the child. A failure after `close-session` never
  reopens, undoes or delays anything before it. Every stop prints what to do next in plain words.
- **Static tests:** neither sequencer imports `methods` or `evaluation`, or has `terminate`, `kill`, `taskkill`, psutil,
  signal, PID or timer; no module of L1 to L3 imports a module of L4 to L7 (the list of both sets is in the test, and
  a new file in `src/` that is in neither list fails the test).

