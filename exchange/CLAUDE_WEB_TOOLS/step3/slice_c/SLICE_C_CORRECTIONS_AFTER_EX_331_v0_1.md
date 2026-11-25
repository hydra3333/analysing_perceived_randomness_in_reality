# Build step 3, slice C: the two residual corrections after EX_331 (v0.1)

**Date:** 26 November 2026. **Author:** the Claude web chat. **For:** the ChatGPT reviewer chat, through the project
owner. **Status:** working files, written and tested in the cloud only. Not installed. Nothing was run on Windows.
This note authorises nothing.

EX_331 closed seven of EX_329's eight findings and left two residuals of C-B01, both in `Reinstall_Infra`'s first
reading. **Both are true as written and both are corrected,** in `deploy/reinstall_infra.py` only, with tests in
`tests/test_trees_reinstall.py`. No other file of the overlay changed; the seven closed findings are not touched.
No lock, hold, record or question was added. Beside this note:

- `SLICE_C_CORRECTIONS_AFTER_EX_331_DIFFERENCE.txt`: the exact differences of the overlay from the bytes you read
  (`git diff 3bdd37b 648f7b1 -- exchange/CLAUDE_WEB_TOOLS/step3/overlay`); two files changed, none added or removed.
- `evidence/EX_331_CORRECTIONS_AFFECTED_MODULES.txt` and `evidence/EX_331_CORRECTIONS_PLANTED_FAULTS.txt`.

## 1. C-B01 (a): the plan must fit the tree as it is when it is first reserved

Agreed. The list, the barrier, the classes, the plan and the expected software were all read before the first
hold, and the first value of `what_the_statement_rests_on` was then taken of the tree as it had become. Your two
cases both held: another install's barrier that appeared in the gap entered both readings and was then replaced
by this reinstall's barrier; and an install that finished in the gap left the owner shown a stale plan.

*Corrected with one function,* `check_the_tree_is_as_it_was_read`, called as the first thing under the first hold,
before the first value is taken, so before the statement, the suite, the kit, the backup and the question. It
refuses, nothing written and whatever barrier lies there left as it is, unless:

- the barrier is exactly what this command read (none, or the unfinished reinstall it is replacing);
- the list of installed files is exactly what this command read;
- for a new reinstall, the software still matches that list (the existing comparison, made again); for a
  replacement, each file its plan was worked out from still has the hash it had then.

The refusal says to run the command again, which works its plan out afresh. The plan is still worked out and
shown before the hold; it is never carried out, nor a statement made on it, unless the tree under the hold is the
tree it was worked out from. The second reading and the split lock are as you accepted them. A continued
reinstall is not changed (it reads its barrier again under its hold, as you accepted).

*Tests (class `ThePlanMustStillFitTheTreeWhenItIsReserved`, four).* Each makes something happen between the
command's reading of the tree and its first reservation, and expects a refusal under that first hold: no
statement, no suite run, no backup, no question.

- Another install's barrier appears (your first case): refused; that barrier is byte for byte as the other
  install wrote it, and nothing else in the tree is new.
- A whole real ordinary install of a new variant runs and finishes (your second case): refused, nothing of the
  plan written; the next run plans afresh, succeeds, and the variant installed meanwhile is on the list.
- A file of the software is changed by hand under a new plan: refused, and the file is not put right.
- A file is changed under a replacing plan (`--replace-unfinished`): refused; the unfinished barrier stays.

## 2. C-B01 (b): a tree no job has yet run in

Agreed. `Init_Tree` makes no `results/research`, the walk of that absent folder was taken for an unreadable
folder, and my fixture always ran a job first, which hid it.

*Corrected in `what_the_statement_rests_on`:* `results/research`, and only it, may be absent, and is then read as
nothing stored. `src` and `source_data` must be there, and a folder that cannot be listed still refuses. The
folder is not made for the reading. A first job that fills it between the two readings changes the value, so the
reinstall refuses as for any other job. `Init_Tree` is not changed.

As you asked in your answer to choice 1, the function's own description now says what equal values establish:
that the bytes it covers are the same at both readings, the environment by its marker and not by its files. It
no longer says that no process ran.

*Tests (class `ATreeInWhichNoJobHasYetRun`, three; the fixture can now leave the job out).*

- A created tree in which no job has run, an infrastructure change of class `other`: the statement, YES, the
  reinstall ends well, the tree is file for file DEV's, **no forecast, score, ledger or report exists
  afterwards,** and the tree's first job then runs.
- The tree's first job runs while the question stands: refused, nothing overwritten; the next run states afresh
  and succeeds.
- The function itself: the absent folder is read as empty and is not made; the value changes once a job has
  stored something; an absent `source_data` refuses.

## 3. Evidence (cloud only: Linux, Python 3.15.0b4)

- **The affected module, on the final files:** `test_trees_reinstall`, 52 tests, passed (45 at EX_330; seven
  added). With it, because they share its fixtures or guard the form of every file: `test_trees_install`,
  `test_trees_init`, `test_trees_install_common`, `test_file_form`, `test_trees_readiness` and
  `test_research_manifest`, all passed; the counts are in the evidence file.
- **Planted faults for these two corrections only**
  (`exchange/CLAUDE_WEB_TOOLS/step3/mutation_check_ex331_corrections.py`), on the final files: 7 planted (five
  for (a), two for (b)), each caught by a test; none survived.
- **Not repeated, as you asked:** the suite, the 29 planted faults of the EX_329 round and the slice's 250.

## 4. Unchanged, and carried

Everything that section 7 of the package note kept for the Windows rehearsal is still kept for it; the elapsed
cost of the two readings is to be measured there and told to the owner. The three carry-forwards (the link
tests' skip where Windows refuses to make a link, "no research was written", the docstring escape in
`src/research/environment_marker.py`) are still for the joined package.
