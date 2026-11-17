# MHUP-B slice 2 (layers L5 and L6) - cloud workspace copy, NOT INSTALLED

Status: CORRECTED EDITION, sent as EX_236 on 18 November 2026. The first edition was EX_232; the reviewer's review is
EX_233 (kernel proofs accepted; S2-F02 to fix; S2-F01 later withdrawn); the owner's clarified research model is recorded in
EX_234 and EX_235 and in decision log entry 84. Nothing here is installed; `src/` and `tests/` on `main` are as at
`cc0ab73`. Slice 2 is built ON TOP of slice 1's tree (`../slice1/`, passed in EX_231).

What the correction changed (`SLICE2_EX232_TO_EX236.diff` shows every line): the archived Mode H study's seal and opening
record are no longer conditions of any normal path staged here (weekly readiness, development plan, gate, report); OV-1's
registration and every eligibility line now need a CONFIRMED line, read after the record, before they are used (S2-F02).

Governing documents: `doc/Predictive_Randomness_MHUPB_Code_Plan_v0_3.md` (section 5 L5 and L6; sections 6, 7, 9),
`doc/Predictive_Randomness_MHUPB_Design_Supplement_v0_8.md` (sections 6 and 7), both as changed by the owner's
clarification of 18 November 2026 (`exchange/DECISIONS/OWNER_CLARIFICATION_2026_11_18_EQUAL_DRAWS_AND_OV1_USES.md`), and
the working principle `exchange/DECISIONS/WORKING_PRINCIPLE_2026_11_18_MAIN_GAME_PRIORITY.md`.

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
- `SLICE2_EX232_TO_EX236.diff`: every changed line of this folder's tools, sources and tests since EX_232.
- `evidence/`: the suite summaries on Python 3.13 and 3.15, the mutation run and the brute-force run.
- `WORKING_NOTES.md`: the working log.

## Rebuild and test (cloud, from the repository root)

    git clone <repo> base
    sh exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/build_dev_slice2.sh base dev exchange/CLAUDE_WEB_TOOLS/mhupb/slice1 exchange/CLAUDE_WEB_TOOLS/mhupb/slice2
    python3 -I exchange/CLAUDE_WEB_TOOLS/mhupb/slice1/run_suite.py dev OUT 2
    cp -a dev mut && python3 -I exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/mutations_slice2.py mut
    python3 -I exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/ov1_bruteforce_evidence.py dev

Run the mutation tool on a separate copy: it edits files in place and restores them.
