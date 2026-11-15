# CONTINUITY NOW - the one page that lets a new chat take over

Living page (P0 and P3, adopted 14 November 2026). Updated in place by the Claude web chat after every milestone; Git
keeps the history. It is a recovery index, not a handover, and grants no permission; the installed handovers and the
durable EX messages are authoritative.

**Last updated:** 15 November 2026, about 19:30 Australia/Adelaide.

## For the owner: NOW

- **Done:** the POC rerun, 14 November about 22:35: PASS (EX_186; window in exchange/RUNS/).
- **Done:** B01 decided: scoped W-23 acceptance (decision log entry 5; EX_187 agreed).
- **Done:** the updater's offline self-test, about 22:43: 13/13 PASS (EX_188; two untracked OUTLANDISH files present,
  benign).
  The reviewer agreed the PASS stands (EX_189). The OUTLANDISH files are committed (657a2c1, merged at a6c2894; no code
  change since cc0ab73).
- **Correction to the order (15 November):** the reviewed sheet requires the official-page check on the day of the first
  Approval 1. So the handover editions come first.
- **Installed:** H-1 v3, its blurb and register v0.30 (RAT-32), at `5b4df41` (15 November, about 18:06; COMMITTED PASS, checked
  by Claude from GitHub). H-2 v2 r1 stays the reviewer's handover.
- **STOP (15 November, about 18:17) at the official-page check:** both games FAIL on the expected draw order (the page
  returned the nine known draws newest-first; every one equal to the master). Nothing written, nothing opened, no approval.
  Decision log entry 9; window in exchange/RUNS/. ROOT CAUSE (EX_194): the check r1 compared draw numbers in page order
  with an oldest-first list; the installed updater does not depend on order (evidence on invented data). Proposed: check r2
  (order-free; 26 draws per game to match the real update's page size) and sheet r2d. REVIEWED: EX_195 PASS (scoped; blobs
  r2 449b5cd3..., sheet r2d 7aa8c89c...). Then prerequisite 3 with r2: PASS (18:50; decision log entry 11). Oz Lotto Approval 1 must be today (15 November)
  or the page check runs again. Backups confirmed (19:01, entry 12; G:\BACKUPS\powerball_modeh_2026-11-15). Tree check PASS (entry 13).
  **Oz Lotto Approval 1 DONE: manifest PASS (entry 14); holdout OPENED 19:19 (entry 15, permanent); witness push 9eb5e33
  (entry 16). THE FREEZE IS ON** until both games are sealed. **Approval 2 DONE 19:23** (entry 17: 15 draws added,
  1694-1708; master v2 63e33493...; master and ledger left uncommitted, D5). **Plan DONE 19:26** (entry 18: batch
  wf-5af149aef7444336a38e469146c95a20). Next: the batch run (Approval 3, part 2), on its own go. No rerun meanwhile. Carried: order-varied pages in the updater's own
  tests, next code package (tests only).
- **Next go (on one chosen day, each on its own go):** the official-page check, the backups, the tree and quiet-machine checks,
  then Oz Lotto's Approval 1.
- **Next after it:** backups confirmed (prerequisite 4).
- **Blocks or STOPs:** the page-check STOP above (Approval 1 waits for it).

## Reviewer status

- Open findings: none. (EX_177 B01 closed 14 November by the owner's scoped W-23 acceptance; never "W-23 PASS".)
- Evidence limits: Windows results (T016, T023, T024) are runner reports, not reproduced by either AI; the live PC state
  (untracked files, running processes, the holdouts being unopened) is owner-reported.
- Latest reviewer messages: EX_181 (D1-D7 advice), EX_183 (P0-P5 advice), EX_185 (POC agreed), EX_187 (POC PASS and B01 wording agreed), EX_189 (self-test PASS stands), EX_191 (H-1 v3 and register v0.30: PASS WITH CORRECTIONS; no H-2 edition needed).

## If a chat ends

- **Claude chat ended:** start a new Claude chat with `doc/HANDOVER/Claude_Primary_Handover_H1_v3_introductory_blurb.md`.
  In its "Since 15 November 2026" line write: "see exchange/CONTINUITY_NOW.md".
- **ChatGPT reviewer chat ended:** start a new ChatGPT chat with
  `exchange/HANDOVER_2026_11_14_REVIEWER/NEW_REVIEWER_START_PASTE.md`, adding: "Then read exchange/CONTINUITY_NOW.md".
  Optional check: blind questions as in EX_178 (Claude writes new ones; the owner holds the key).

## Installed handovers (authoritative)

H-1 v3 (Claude; RAT-32, installed `5b4df41`) and H-2 v2 r1 (reviewer; RAT-31, installed `5a8527b`), with register v0.30.
The next full refresh: after both games are sealed, or earlier if a chat grows long.

## Working approach adopted 14 November 2026 (P0-P6)

EX_182 as modified by EX_183, agreed in EX_184; decision log entry 1. In short: decide by effect (level 1 owner decides
after review: science, safety, `src/`, packages, real data, Mode H; level 2 reviewed, still needs its own go; level 3
cosmetic or routine author choices only); one decisions log; this one NOW page; living drafts, but a procedure used for
a real step is fixed and re-reviewed if changed; an ideas backlog after Mode H; and at each substantial milestone a short
independent "how the process went" note from each AI, with reasoning and alternatives. Reviewer rights unchanged.

## Changes since the installed handovers (all committed)

- Owner dependency change cc0ab73; TASK_T024 PASS (ENV PASS, 571 tests); new environment digest 5bf4eb8a36dd...
  (H-1 v2 still quotes the older 966a2792...; readiness sheet r2c has the new one).
- EX_176-EX_177: PASS WITH CORRECTIONS. C01 applied (sheet r2c). C02 closed by the owner without a pip check. B01 closed (scoped W-23 acceptance).
- The old ChatGPT reviewer chat ended; the replacement took over (EX_178-EX_180: 12 of 12) and was accepted by the owner.
- D1-D7 decided as recommended (exchange/DECISIONS/OWNER_DECISIONS_2026_11_14b_C02_AND_REVIEWER.md); EX_181 agreed.
- Working approach P0-P6 adopted (EX_182-EX_184; exchange/DECISIONS/DECISION_LOG.md).
- OUTLANDISH_01's methods join the method backlog, probably first among the methods still to do, through this project's
  normal route (decision log entry 3).
- The owner works on OUTLANDISH_01 in GAIS/, committing with `git add GAIS/OUTLANDISH_01/`; no further package installs
  planned (he will ask Claude first).

## Mode H state

POC rerun and updater offline self-test COMPLETED (both PASS, 14 November 2026); B01 closed. The official-page check, the
backups, the tree and quiet-machine checks and all Approvals 1-4 NOT RUN. Oz Lotto's holdout OPENED (15 November 19:19); Powerball's UNOPENED. The freeze is ON (from 19:18).

## Full order from here

1. DONE: H-1 v3 and register v0.30 reviewed (EX_191, EX_192), ratified (RAT-32) and installed (`5b4df41`).
2. The official-page check, only when separately approved, on the same day as Oz Lotto's Approval 1; the backups, the tree
   and quiet-machine checks; then Oz Lotto's Approval 1. Each on its own go.
3. Oz Lotto's Approvals 2-4, then Powerball's 1-4, each on its own go and its own safe schedule (a separately approved
   Powerball-only page recheck is allowed after Oz Lotto is sealed and before Powerball's Approval 1). D1-D7 apply.
