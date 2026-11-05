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

DONE since: all corrections and oracles (569 tests); 15 new mutants + 5 retargeted, run alone first (all caught or
equivalent with reasons); amendment A1 draft (MHUP1_design_amendment_A1_draft.md); EX_149 body (ex149_body.md, with
@@SUITE@@/@@MUT@@/@@CONTENTS@@/@@TABLE@@ filled by the assembler); tools/assemble_ex149.py; TASK_T021 draft (t021_lf.md, with
@@SHA@@/@@SHA8@@ = the v1r1 zip's SHA-256) and its plan (TASK_T021_overlay_plan.txt: 33 REPLACE, 1 REMOVE, 37 new); card v6.
Final chain started on the final tree (both suites -> S/suite_slice2r1_py31{3,5}.log, then 99 mutants -> S/mutations_slice2r1_py313.txt).

TODO: (1) when the chain ends with SUITE PASS x2 and "0 survived": python3 S/tools/assemble_ex149.py S R; (2) fill t021_lf.md's
@@SHA@@ / @@SHA8@@ from exchange/EX_149_Claude/MHUPA_Slice2_Review_v1r1.zip, write inbox/TASK_T021.md (CRLF) and
inbox/TASK_T021_overlay_plan.txt, run exchange/CLAUDE_WEB_TOOLS/check_task_commands.py on it; (3) reminders/roadmap lines
(EX_149 sent; T021; A1 awaiting review then owner approval); (4) commit, push; paste block asking ChatGPT for EX_150 and
reminding the owner to attach exchange/EX_149_Claude.zip directly. If the session is lost: rebuild S/DEV with
build_dev_slice2.sh from a git archive of 2061055 (BASE, minus data folders), overlay onto a clone (dev_clone), rerun the chain.
