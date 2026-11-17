# MHUP-B slice 2 (layers L5 and L6) - cloud workspace copy, NOT INSTALLED

Status: SUBMITTED FOR REVIEW (see the EX message that names this folder). Nothing here is installed; `src/` and `tests/`
on `main` are as at `cc0ab73`. Slice 2 is built ON TOP of slice 1's tree (`../slice1/`, passed in EX_231).

Governing documents: `doc/Predictive_Randomness_MHUPB_Code_Plan_v0_3.md` (section 5 L5 and L6; sections 6, 7, 9),
`doc/Predictive_Randomness_MHUPB_Design_Supplement_v0_8.md` (sections 6 and 7), and the working principle
`exchange/DECISIONS/WORKING_PRINCIPLE_2026_11_18_MAIN_GAME_PRIORITY.md`.

## What is here

- `build_dev_slice2.sh BASE DEV SLICE1_TOOLS SLICE2_TOOLS`: makes the tree that was tested: slice 1 first, then
  `apply_slice2.py` (counted edits to installed modules and to slice 1's `score_identities.py`), `edit_tests_slice2.py`
  (one line of the static firewall), then the files of `slice2_new/` by their final path.
- `slice2_new/src/evaluation/ov1_numeric.py`: OV-1's numerical kernel (whole numbers only; the proofs are in its
  docstring). `ov1.py`, `Method_OV1.py`: the registration, the ledger, `record`, `stop`, `status`, `verify`.
  `reforecast_compare.py`: named forecast content compared (supplement 7.2 rule 7).
- `slice2_new/tests/`: `test_mhupb_ov1_numeric.py`, `test_mhupb_ov1.py`, `test_mhupb_dev_batch.py`.
- `mutations_slice2.py TREE [name ...]`: one planted defect per rule, each caught by a named test; the equivalent
  mutants are listed in its docstring. `ov1_bruteforce_evidence.py TREE`: every 7-subset of both barrels enumerated.
- `SLICE2_EDITS_TO_SLICE1_TREE.diff`: every changed line of a file that slice 1's tree already had.
- `evidence/`: the suite summaries on Python 3.13 and 3.15, the mutation run and the brute-force run.
- `WORKING_NOTES.md`: the working log.

## Rebuild and test (cloud, from the repository root)

    git clone <repo> base
    sh exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/build_dev_slice2.sh base dev exchange/CLAUDE_WEB_TOOLS/mhupb/slice1 exchange/CLAUDE_WEB_TOOLS/mhupb/slice2
    python3 -I exchange/CLAUDE_WEB_TOOLS/mhupb/slice1/run_suite.py dev OUT 2
    cp -a dev mut && python3 -I exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/mutations_slice2.py mut
    python3 -I exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/ov1_bruteforce_evidence.py dev

Run the mutation tool on a separate copy: it edits files in place and restores them.
