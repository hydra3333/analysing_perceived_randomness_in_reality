# CHECKPOINT - MHUP-A slice 2 recheck after EX_148 (the next handback is EX_149), 5 November 2026

For a continuing session (any model). S = the session scratchpad (lost if the session ends); this folder in the repository
is the durable copy. EX_147 (slice 2 candidate v1) was answered by EX_148 (RECHECK: B01-B04, C01, (iii-b)).

Owner decisions (5 November 2026, already relayed to ChatGPT): B01 route (B) - approve the one-step atomic score ledger
by a focused design amendment (Claude writes it for review, then the owner's final approval); (iii-b) - the corrective
scoring run is deferred to MHUP-B, with the route named in EX_149.

DONE in slice2_new/ (this folder; build with build_dev_slice2.sh BASE DEV TOOLS 2026-11-04):
- B02 mode_h.py: the three report files resumed one by one (existing verified first, missing created, never overwritten).
- B04 mode_h.py: _verify_ledger before SCORE_COMPLETE (exact rebuild from the frozen forecasts and the ledger's own drawn
  numbers; Oz Lotto supplementary counts checked for range and division); _ledger_lines turns validator errors into refusals.
- B03 new src/methods/_common/release_records.py (the one reader; released_variants drops entries whose registry chain's
  active entry is another revision or not SUPPORTED); install_records.py delegates to it; mode_h.manifest refuses unless
  the cohort equals the game's released set (_check_release_authority). test_wf1b_static ALLOWED_COMMON gains it (edit script).
- C01 process_check.read_table reads every process (non-Python: command line only) so a cmd.exe ancestor is seen.
- New oracles: test_mhupa_mode_h (+4: cohort/release set, superseding entry at the manifest, bad ledger x9, report resume),
  test_mhupa_install_records (+2), test_mhupa_process_check (+1). All pass on Python 3.13.

TODO, in order: (1) mutants for each new rule in tools/mhupa_slice2_mutations.py, run with --only N first (survivors found
before the full run); (2) the B01 amendment note (guarantees kept, states removed, failure model) and the (iii-b) route and
the (vi) note, as members of EX_149; (3) RUN_MHUPA_SLICE2_SUITE.py counts: 561 + 7 = 568; one full chain (both suites, then
mutations); (4) assemble EX_149 (copy assemble_ex147.py: NAME v1r1, the EX_147 overlay as the "previous" side of the
v1->v1r1 diff, EX_148 and the supplement as members); (5) TASK_T021 for the Windows run (copy TASK_T020 + its plan; check it
with exchange/CLAUDE_WEB_TOOLS/check_task_commands.py); (6) commit, push, paste block for ChatGPT asking for EX_150.
