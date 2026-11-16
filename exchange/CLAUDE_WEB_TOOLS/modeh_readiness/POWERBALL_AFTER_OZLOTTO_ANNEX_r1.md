# Powerball after Oz Lotto's seal: the expected states (annex r1 to readiness sheet r2d) - DRAFT for focused review; not authorised

Claude web chat, 16 November 2026. Requested by the owner and the reviewer the same evening. US-ASCII, CRLF.

**What this is.** Readiness sheet r2d (blob `7aa8c89c...`) was written before any game was opened, so some of its
"Expect" lines assume an untouched tree. Oz Lotto is now opened, updated and sealed (decision log entries 14-21), and its
deliberate results stay on the owner's PC uncommitted (D5, D6). This annex changes ONLY those expected states for the
Powerball run. **Every command, gate, order, STOP rule and safeguard of r2d stays exactly as written** (r2d section 5
prerequisites 3-6 and section 6 "Powerball"); nothing here authorises anything; each step still needs the owner's own go.

## E0. The Oz Lotto baseline: the exact expected `git status --short`

From the owner's window of 15 November 2026, 22:08 (after the seal), and expected unchanged until Powerball's own steps add
to it. Before starting, the owner commits any OUTLANDISH work by name (`git add GAIS/OUTLANDISH_01/`), so that nothing else
appears:
```
 M results/audit/SEARCH_LOG.csv
 M source_data/OZLOTTO_results_master.csv
 M source_data/OZLOTTO_results_master_ledger.csv
?? results/method_rankings/OZLOTTO/mode_h_OZLOTTO_1694-1703_mh-ba0c301be2fb4c459492697d0137e7ed.csv
?? results/method_rankings/OZLOTTO/mode_h_OZLOTTO_1694-1703_mh-ba0c301be2fb4c459492697d0137e7ed.json
?? results/method_rankings/OZLOTTO/mode_h_OZLOTTO_1694-1703_mh-ba0c301be2fb4c459492697d0137e7ed.txt
?? results/real/holdout/OZLOTTO/MODE_H_BATCH_ID.json
?? results/real/holdout/wf_batches/
```
These eight lines are expected and are never a reason to restore, reset, clean, stash or commit anything (D5, D6; the freeze).
A line not in this list (other than the Powerball additions named below for each step) is a STOP before the next command.

## The adjustments, step by step

**Before step 1 (the freeze's pull rule, r2d section 7).** Instead of a plain pull:
```
git fetch
git diff --stat HEAD origin/main
```
Expect only paths under `exchange/` (Claude's records). Anything else: stop and send it. Then `git pull --ff-only`.

**Prerequisite 3, the page check, Powerball only** (r2d's own Powerball-only form; the same day as Powerball's Approval 1):
the commands of r2d prerequisite 3 with `--games POWERBALL` added to the check's line. Expect: both `git status --short`
outputs exactly E0 (not empty), identical before and after; both blob lines `449b5cd3a974d34488eb1522b5a75809e8d212b1`;
then exactly these four lines and `EXIT 0`:
```
[GOV-SMOKE] POWERBALL: master verified against its ledger (version 1, last draw 1576); read-only
[GOV-SMOKE] POWERBALL: window 2026-01-31..2026-07-31; final address https://www.lotterywest.wa.gov.au; parsed 26 draw(s) 1551-1576, listed newest first; on the weekly date rule 26/26; equal to the master 26/26
[GOV-SMOKE] POWERBALL: PASS
[GOV-SMOKE] PASS: POWERBALL: the installed fetcher and parser read the official page as expected. This check wrote nothing.
```
The two tolerated differences of r2d (a weekly-rule count below 26/26; a "listed" wording other than "newest first") are
still sent to Claude first. The check reads only the Powerball master; Oz Lotto's opened state does not affect it.

**Prerequisite 4, backups:** as on 15 November, to a new folder (`G:\BACKUPS\powerball_modeh_<date>_before_powerball\`);
the same expectations (FAILED 0; copy exit 1; list-only check exit 0).

**Prerequisite 5, the tree check** (same five commands). Expect: the first `git status --short` exactly E0; the
`--ignored src` lines only ending `__pycache__/`; nothing from the `git diff --stat cc0ab73 HEAD -- src "*.bat"
requirements.txt`; **Oz Lotto's master `63e3349333f8aa0485b7b067abe70249e39de81c6d02cda1a5710cf1041a4e9e`** (its version 2,
written by its Approval 2 on 15 November; r2d's version-1 value no longer applies to Oz Lotto); **Powerball's master
`ce0ae7e77e09e5a93389eb98191b455926ec44c0bb38dda0ef721b9f710d66b8`** (version 1, unchanged).

**Prerequisite 6, quiet machine:** unchanged.

**Approval 1:** unchanged (manifest: 40 variants, targets 1577-1586, version 1, 497 files, environment digest `5bf4eb8a36dd`;
then the opening statement).

**The witness push (D3):** the same three `git add` paths as r2d. Expect `git status --short` to show E0 plus
`?? results/real/holdout/POWERBALL/` and `?? source_data/HOLDOUT_OPENED_POWERBALL.json`; `git diff --cached --name-only`
exactly the three paths of r2d and nothing else (in particular no master or ledger of either game, no report). Note: the
staged `results/audit/SEARCH_LOG.csv` now also carries Oz Lotto's later value-free rows (its plan and score); that is
expected. Split into staging-then-check and commit-then-push, as for Oz Lotto.

**Approval 2:** unchanged command. On 16, 17 or 18 November 2026 expect `checked 9 overlapping draws (all matched), added 15
(1577..1591), warnings 0` (from 19 November, after that evening's draw is published, possibly 16, to 1592). Its snapshot
(r2d section 8.2, with `POWERBALL`) will now show ` M` for both games' masters and ledgers; the Oz Lotto lines are E0's.

**Approvals 3 and 4:** unchanged (400 planned pairs; 800 score lines and 400 rank lines if every pair has a forecast, as in
the rehearsal for Powerball; the report names the Powerball-number family and the two exposure flags).

**After the seal:** a backup to a new folder; then E0 grows by Powerball's own report, batch-id and holdout files; none is
committed until the owner decides after both seals (D5, D6).

## Not changed

The freeze (r2d section 7), the STOP rule and section 8.2, D1-D7, the page check's same-day rule, the separate gos, Q7 and the
rule that no AI receives a drawn value, a master, a grab, a backup, a score ledger or a report before both seals.
