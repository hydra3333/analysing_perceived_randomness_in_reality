# CHECKPOINT - MHUP-A slice 2, 5 November 2026 (before EX_151)

EX_150 (reviewer): B02, B03, B04, C01 PASS; A1 favourable; new narrow blocker B05. The owner RATIFIED A1 the same day
(exchange/MHUP1_design_amendment_A1_RATIFIED.md; reminder R-021 DONE). B05 is corrected in slice2_new (mode_h.py:
plan_for, _resumed_scoring_plan, the fuller SCORE_COMPLETE check) with the test
Pipeline.test_a_resume_binds_the_frozen_scoring_plan_and_completion (570 tests); four B05 mutants added (99-102).

Running when written: both suites (S/suite_slice2r2_py31{3,5}.log) then mutants 99-102 and 50 alone
(S/mutations_slice2r2_targeted_py313.txt). Then: python3 S/tools/assemble_ex151.py S R; fill t022_lf.md's
@@SHA@@/@@SHA8@@ from exchange/EX_151_Claude/MHUPA_Slice2_Review_v1r2.zip (and its file count in "UNZIP PASS: n files"),
write inbox/TASK_T022.md (CRLF) and inbox/TASK_T022_overlay_plan.txt, run check_task_commands.py; commit, push; paste
block asking for EX_152 and reminding the owner to attach exchange/EX_151_Claude.zip. T021's report was not yet in the
repository; do not claim it.
