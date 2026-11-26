# Step 2 of the simple scheme: the engine simplified, and compared with the frozen engine

Version v0.1, 26 November 2026. From the Claude web chat (primary designer and coder), for the project owner and
for the reviewer's one reading. Short on purpose (the lighter process, decision log entry 335).

## 1. The result

The engine inside `a_p_r_i_r_DEV\` is simplified as the simple scheme v0.2 says, and committed there
(`aedda2e`; 124 files changed, 2349 insertions(+), 6404 deletions(-)). Nothing at the top level of the repository was touched, and
nothing was run on the owner's PC.

**From the same accepted results, the simplified engine and the frozen engine give the same forecasts, the same
scores, the same OV-1 numbers and the same reports.** Evidence class: the cloud only (Linux, Python 3.15.0b4).
The same comparison on the owner's PC is step 5.

## 2. What was compared, and what the tool printed

Two trees were made in the cloud workspace from the same four files of accepted results: `ref` (a clone of `main`,
the frozen engine at the top level) and `new_DEV` (a copy of `a_p_r_i_r_DEV\src`, checked afterwards to be file for
file the committed one). Each engine ran its own full fill in its own Python process
(`--game BOTH --no-update`; about 30 minutes each here). Then `align` gave the methods of both trees the same
spread of starting draws for the second OV-1 series, both jobs ran again, and `trees` compared what the two
trees hold:

```
SAME       POWERBALL: the methods that have results (40 and 40)
SAME       POWERBALL: every forecast and every score of every method (15118 forecast lines: 15118 forecasts and 0 no-forecasts; 15078 scores)
SAME       POWERBALL: the second OV-1 series, line by line (41 and 41 lines; draws 1551 to 1591)
SAME       POWERBALL: the names of the report files (901 and 901)
SAME       POWERBALL: every report file, byte for byte (league, next draw, both OV-1 print-outs, README)
SAME       OZLOTTO: the methods that have results (40 and 40)
SAME       OZLOTTO: every forecast and every score of every method (6598 forecast lines: 6598 forecasts and 0 no-forecasts; 6558 scores)
SAME       OZLOTTO: the second OV-1 series, line by line (41 and 41 lines; draws 1668 to 1708)
SAME       OZLOTTO: the names of the report files (475 and 475)
SAME       OZLOTTO: every report file, byte for byte (league, next draw, both OV-1 print-outs, README)
RESULT: SAME: the frozen engine at /home/claude/work/ref and the simplified engine at /home/claude/work/new_DEV
```

The series over all draws is compared through its print-out (the frozen engine stores no file of it); that
print-out is among the report files compared byte for byte. The same whole comparison on **invented** results
with the 40 real methods (`invented`, 5,678 forecasts a game) also ends `RESULT: SAME`, all eleven lines.

The tool's `code` command lists every source file by how it differs from the frozen one:

```
the same bytes: 17 engine files, 119 method and helper files
    evaluation/__init__.py
    evaluation/divisions.py
    methods/_common/__init__.py
    methods/_common/canonical_encoding.py
    methods/_common/contract_forecast.py
    methods/_common/contract_records.py
    methods/_common/contract_task.py
    methods/_common/contract_vocab.py
    methods/_common/game_profiles.py
    research/__init__.py
    research/forecast_engine.py
    research/job_lock.py
    research/method_api.py
    research/ov1_numeric.py
    research/readout.py
    research/reports.py
    research/settings.py
the same program (comments and docstrings differ): 3 engine files, 0 method and helper files
    research/reader.py
    research/scoring.py
    research/windows_text.py
changed: 7 engine files, 0 method and helper files
    research/code_identity.py
    research/game_state.py
    research/ov1_ledger.py
    research/research_job.py
    research/variant_folders.py
    research/variant_lists.py
    research_command.py
only in the simplified engine: 1 engine files, 0 method and helper files
    research/method_flags.py
only in the frozen tree (of the engine): research/derived_check.py, research/results_step.py,
    research/status_file.py, research/withdraw.py
```

So the forecast engine, the readout and its tie order, the OV-1 arithmetic, the divisions, the reports and the
shared contract modules are the same bytes; the reader, scoring and the text helper differ in docstrings only;
all 119 method and helper files are the same bytes. **The science could only have moved in the seven changed
files and the one new file,** and the comparison says it did not.

That "SAME" means the same is tested: `tests\test_research_compare.py` plants one difference of each kind (a
forecast's sets, whether it was made before its result, a score, an OV-1 line, a report, a missing method, a
missing report) and the tool names each. 161 tests pass in the tree; all run on invented draws and toy methods.

## 3. What changed, in a few lines

- **`research_job.py`:** one job, the same in every tree. It deletes what is out of date and only that, then
  fills and catches up (the next draw included), then makes the league, the reports and both OV-1 series again,
  then adds one line to `records\JOB_LOG.jsonl` (time, Python and every package version, what was rebuilt and
  why, what failed). `--rebuild <method>`, `--rebuild-all`; `--game` now defaults to BOTH; `--only` is gone.
- **`method_flags.py` (new):** the three small files beside a method, plain `key = value` text.
- **`variant_lists.py`:** plain CRLF line records; no link to the line before; the first line names the
  fingerprint of the method's software that made the list.
- **`code_identity.py`:** one fingerprint over every file under `src\` outside the method families, kept in
  `results\research\INFRASTRUCTURE`. The manifest is gone.
- **`ov1_ledger.py`, `game_state.py`:** both OV-1 series are made afresh by every job; nothing is "held",
  "foreign" by fingerprint, or "not current".
- **Removed:** the derived check, the status file, the results-copy step, the withdrawal command, and the first
  system's files that only three old comparison tests used (those tests stay with the frozen engine).
- **Size:** the engine's own code went from 4,511 lines to 3,733; its tests from 3,880 to 2,877.

## 4. Choices I made while writing it (say if any should be otherwise)

1. **A corrected draw.** Each forecast holds the digest of the draws it was computed from. Per method, the job
   finds the first forecast whose digest no longer matches and drops it and every later one, with their scores.
   Separately, **every stored score is worked out again from its forecast and the result on file at the start of
   every job**, and the first that comes out otherwise is dropped with every later one. This is what the old
   "derived check" did, turned from a refusal into "make that part again".
2. **A method whose calculation fails** writes no line, is reported, and is passed over for the rest of that job;
   the other methods go on. Such a job ends with exit code 1 and says so, so that nothing reads it as clean.
3. **`I_AM_RETIRED` made by hand, even empty,** retires the method from the tree's next draw: the job writes the
   draw into the file. A method retired from an earlier draw loses what it held from that draw on (its forecast
   for that very draw stays, unscored, as today's reports already show it).
4. **Results of a method the tree has no software for** are left alone, even by `--rebuild-all`, and count in no
   report and in neither OV-1 series (the job says so each time).
5. **A changed engine deletes the results of both games,** even when the job works one; the other game is filled
   by the next job that works it.
6. **`IN_PLACE_SINCE`** is kept when the engine changes or `--rebuild` is used, and written afresh only when the
   method's own fingerprint changes. Git ignores it (it is each tree's own bookkeeping).
7. **One behaviour differs from the frozen engine, in a case the frozen engine could never reach:** in the second
   OV-1 series a method does not count before its own first target. (The frozen engine would have stopped the
   series there; it never gave a method a counting draw before it had a line.)
8. **The content digest of a forecast** is still written, because a score names its forecast by it; nothing
   checks it on reading.
9. **Scores must be in draw order with no gap,** as before: a gap means a line was lost, and the method is made
   again.

## 5. Known and left for later

- **The reports' wording is unchanged** ("withdrawn", "variant", the "at most 2.5%" claim of the second series,
  the README's mention of reports set aside), on purpose: with `reports.py` the same bytes, the reports compare
  byte for byte. A small wording change follows, as its own commit.
- **The settings file, the lock and the first system's orphan-marker check** are still the first form; step 4
  replaces them. **The updater** is step 3: until then the job works on the results the tree holds and says so.
- **A question for step 4:** whether `I_AM_INSTALLABLE` and `I_AM_RETIRED` in DEV are kept in Git.
- A job with nothing to do takes about two minutes here for both games, because every league report is made
  again each time. It can be shortened later; it does not matter for a weekly job.

## 6. For the reviewer: where to look

One reading, where the science is: in `a_p_r_i_r_DEV\src\research\`, `research_job.py` (what is dropped and
when: `settle_infrastructure`, `open_game`, `drop_what_results_no_longer_support`, `drop_beyond_retirement`),
`ov1_ledger.py` (`prevailing_series`), `game_state.py` (`load_variant_state`), `variant_lists.py`
(`check_lists`, `keep_below`) and `method_flags.py`. The question that matters: can any path leave a stored
forecast, score or OV-1 line that is not what the engine would compute from the results on file and the software
in the tree? And for the tool, `a_p_r_i_r_DEV\deploy\compare_with_frozen.py`: is anything that should be
compared left out?

## 7. What I think the owner should do next

1. Paste the short block of my message to the reviewer for its one reading. Nothing waits on it.
2. Nothing on the PC. A `git pull` is harmless whenever convenient.
3. Give the go for **step 3** (the updater with every Mode H state removed, the same in every tree) when ready.
