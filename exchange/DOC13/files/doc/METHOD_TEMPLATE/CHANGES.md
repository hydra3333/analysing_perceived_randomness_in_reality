# New-method template: draft 3 to draft 4 (Claude, 1 November 2026)

For review with the snapshot documents. Only README.md and METHOD_SPECIFICATION_TEMPLATE.md change; the code
skeletons (method_folder/, make_contract_data.py.txt, test_template.py.txt) and the two JSON examples are unchanged.

README.md:
- title and status: draft 4, what it adds;
- step 8: a "Windows-safe tests" paragraph (symlink guard and skip, hard-link alternative, allowed-skip list; no
  timing assertions, POSIX-only paths or line-ending reliance) - from WF-1B's TASK_T013 stop;
- step 11: Claude Code's Windows rehearsal before the owner's install, and the deny check of task commands - from
  TASK_T012's stop;
- step 12: the real-development switch is True since WF-1A (was "stays False"); the REL-1 pattern;
- new step 13: full-cohort walk-forward batches, two tracks per variant in the ranking report and the effect on its
  families, a change after release is a new revision archived by CODE-3 (E_1 revision 2), seed policies for
  stochastic methods;
- "Things that bite": three new items (exact arithmetic slow at full size, PERF-1; record files must keep their
  bytes, the Powerball report refusal; no data values in progress lines).

METHOD_SPECIFICATION_TEMPLATE.md:
- section 4: a stochastic fit needs its own approved seed policy (was "does not exist yet");
- section 5: a new question, the run time at full size;
- section 9: the switches as they now stand;
- section 10: joining the walk-forward batches and the report's families;
- section 11: Windows-safe tests.

## Draft 5 (8 November 2026; Claude; for review with the DOC-13 documents)

README.md:
- the status line says DRAFT 5 (draft 4's said DRAFT 3; reminder R-018 (c));
- "How the pieces fit": the release record and the release date once MHUP-A is installed; run modes are the contract's business;
- step 4: never branch on the run mode (E_1 revision 3's lesson);
- step 11: the package manifest's `release_entries` and `retires`; the `released` verifier phase; the task-command checkers;
- step 12: install and release records, the release date, the effective date, rosters that change only through an install;
- step 13: Mode H is a fixed cohort (Q9-E1);
- "Things that bite": a run-mode check is a future revision; text-checked tokens such as `effective_date`.

METHOD_SPECIFICATION_TEMPLATE.md:
- section 10: release entries, the weekly roster, Mode H, and no run-mode check.

The code skeletons are unchanged. Until MHUP-A is installed the draft 4 rules apply.
