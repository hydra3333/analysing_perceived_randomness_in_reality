# MHUP-B slice 1 (the live path): PASSED the reviewer's source review (EX_231) - NOT INSTALLED

After EX_231 the small note N-231-1 (a drawn Powerball must be 1 to 20) was applied here, with its test and mutant;
the `evidence/` files are for EX_230's tree, and N-231-1's full-suite evidence comes with slice 2.

EX_228 sent the first edition; EX_229 (the reviewer) asked for four corrections; this folder now holds the corrected
edition (EX_230). `SLICE1_EX228_TO_EX230.diff` shows every line changed between the two.

Code plan v0.3 (RAT-35), slice 1 = the baseline test fixes, L1 (modes and gates), L2 (the forecasting half), L3 (the
scoring half). The owner's go for code: decision log entry 75. Nothing here is installed; the project's `src/` and
`tests/` are unchanged. Layout as MHUP-A's:

- `apply_slice1.py TREE`: counted edits to the installed modules and `.gitignore`.
- `edit_tests_slice1.py TREE`: counted edits to existing tests.
- `slice1_new/`: the new source and test files, by their final paths.
- `build_dev_slice1.sh BASE DEV TOOLS`: makes a dev tree from a clone of `main`.
- `run_suite.py TREE OUT [JOBS] [filter ...]`: the offline suite, one module per process, without E2R-T12.
- `mutations_slice1.py TREE`: one planted defect per rule; each must be caught by its named test.
- `SLICE1_EDITS_TO_INSTALLED_FILES.diff`: every changed line of an installed file.
- `evidence/`: the suite summaries on Python 3.13 and 3.15 and the mutation run, for EX_228's tree and (the files
  named `corrected`) for EX_230's tree.
- `WORKING_NOTES.md`: Claude's notes while coding.
