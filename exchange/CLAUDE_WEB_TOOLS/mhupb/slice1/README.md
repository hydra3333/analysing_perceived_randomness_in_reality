# MHUP-B slice 1 (the live path): WORK IN PROGRESS - not yet sent for review

Code plan v0.3 (RAT-35), slice 1 = the baseline test fixes, L1 (modes and gates), L2 (the forecasting half), L3 (the
scoring half). The owner's go for code: decision log entry 75. Nothing here is installed; the project's `src/` and
`tests/` are unchanged. Layout as MHUP-A's:

- `apply_slice1.py TREE`: counted edits to the installed modules and `.gitignore`.
- `edit_tests_slice1.py TREE`: counted edits to existing tests.
- `slice1_new/`: the new source and test files, by their final paths.
- `build_dev_slice1.sh BASE DEV TOOLS`: makes a dev tree from a clone of `main`.
- `run_suite.py TREE OUT [JOBS] [filter ...]`: the offline suite, one module per process, without E2R-T12.
- `WORKING_NOTES.md`: Claude's notes while coding (decisions to put to the reviewer).

Until an EX message sends this slice to the reviewer, treat every file here as unfinished.
