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
