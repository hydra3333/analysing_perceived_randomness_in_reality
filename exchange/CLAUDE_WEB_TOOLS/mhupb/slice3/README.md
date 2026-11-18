# MHUP-B slice 3 (layers L4, L7 and L8) - cloud workspace copy, NOT INSTALLED

Status: CORRECTED EDITION, sent as EX_241 on 18 November 2026 for the reviewer's focused recheck. The first edition
was EX_239; the reviewer's source review is EX_240 (three narrow corrections, F3-01 to F3-03; the five questions of
EX_239 answered and the choices kept). The owner's go for this slice: 18 November 2026, 14:33 (decision log entry 88).
Nothing here is installed; `src/` and `tests/` on `main` are as at `cc0ab73`. Slice 3 is built ON TOP of slice 2's tree
(`../slice2/`, passed in EX_237), which is built on slice 1's (`../slice1/`, passed in EX_231).

What the correction changed (`SLICE3_EX239_TO_EX241.diff` shows every line): admission also binds each score's method
revision and freeze receipt to the frozen forecast it scores and checks its prize division against its own matches
(F3-01); a lost source blanks only the (method, revision, variant) identities it supplies (F3-02); a publication
counts as logged only if its search-log row holds the digest of the manifest as read (F3-03).

Governing documents: `doc/Predictive_Randomness_MHUPB_Code_Plan_v0_3.md` (section 5 L4, L7, L8; sections 7, 8, 9, 12A),
`doc/Predictive_Randomness_MHUPB_Design_Supplement_v0_8.md` (sections 3, 4, 5, 8), both as changed by the owner's
clarification of 18 November 2026 (`exchange/DECISIONS/OWNER_CLARIFICATION_2026_11_18_EQUAL_DRAWS_AND_OV1_USES.md`),
EX_235 section 2 (the two labelled OV-1 uses), EX_237 section 5 (slice 3's obligations), and the working principle
`exchange/DECISIONS/WORKING_PRINCIPLE_2026_11_18_MAIN_GAME_PRIORITY.md`.

## What is here

- `build_dev_slice3.sh BASE DEV SLICE1_TOOLS SLICE2_TOOLS SLICE3_TOOLS`: makes the tree that was tested: slice 1, then
  slice 2, then `apply_slice3.py` (counted edits to modules slice 2's tree already has), `edit_tests_slice3.py` (one line
  of one slice 2 test), then the files of `slice3_new/` by their final path.
- `slice3_new/src/evaluation/` (L4): `league_sources.py` (the three read-only adapters, the pins, the publication
  manifests' reader, what an attempt must show to be admitted), `league_table.py` (pure: rows, columns, order, labels),
  `league_publish.py` (the ONE league writer: publish, repair, admit, history, reconstruction), `Method_League_Table.py`.
- `slice3_new/src/evaluation/` (L7): `ov1_retrospective.py` (the retrospective OV-1 view: descriptive, not the formal
  test), `consolidated_report.py` (the weekly report's seven parts and the retired-revision index),
  `Method_Weekly_Report.py`.
- `slice3_new/src/` (L8): `sequencer_children.py` (how a child is started: written once), `Weekly_Session_Orchestrator.py`,
  `Development_Batch_Orchestrator.py`; `slice3_new/Run_Weekly_Session.bat`, `slice3_new/Run_Development_Batch.bat` (CRLF).
- `slice3_new/tests/`: `test_mhupb_league.py`, `test_mhupb_league_real.py` (reads the committed real score records;
  kept apart), `test_mhupb_weekly_report.py`, `test_mhupb_sequencers.py`.
- `mutations_slice3.py TREE [name ...]`: one planted defect per rule, each caught by a named test; the equivalent
  mutants are listed in its docstring.
- `SLICE3_EDITS_TO_SLICE2_TREE.diff`: every changed line of a file that slice 2's tree already had (seven files).
- `SLICE3_EX239_TO_EX241.diff`: every changed line of this folder's sources, tests and mutation tool since EX_239.
- `evidence/`: the suite summaries on Python 3.13 and 3.15 and the mutation run, for EX_239 and (`*_corrected_*`) EX_241.
- `WORKING_NOTES.md`: the build log, with the times read from the clock.

## Rebuild and check (Linux; nothing is installed and no real data is written)

    git clone <the repository> base            # or a clean checkout of main
    T=base/exchange/CLAUDE_WEB_TOOLS/mhupb
    sh $T/slice3/build_dev_slice3.sh base dev $T/slice1 $T/slice2 $T/slice3
    (cd dev && find . -type f \( -path './src/*' -o -path './tests/*' -o -name '.gitignore' \
        -o -path './Run_Weekly_Session.bat' -o -path './Run_Development_Batch.bat' \) ! -name '*.pyc' -print0 \
        | sort -z | xargs -0 sha256sum | sha256sum)                      # the tree digest quoted in EX_241
    python3 -I $T/slice1/run_suite.py dev out 2                          # the offline suite, one module per process
    python3 -I $T/slice3/mutations_slice3.py dev                         # on a copy of the tree

The digest recipe is slice 2's with the two new launchers at the tree's root added (they are outside `src/` and `tests/`; `-path`, not `-name`, so that the copies under `exchange/` in a full checkout are not taken). The launchers
are CRLF in a checkout that follows the repository's `.gitattributes` (`*.bat text eol=crlf`); the digest is of such a
checkout.

## What the cloud cannot test (it is T017's, or the first use on the owner's PC)

- The Windows launch chain: a `.bat` child started from a Python parent, the two new launchers, the process check.
  In the tests the sequencers' one child-starting function is replaced by a stand-in that runs the same tool's
  `main()` in-process.
- The admission of the two real report attempts: its check of every score against its frozen forecast needs the batch's
  run folders, which are on the owner's PC only. The adapters themselves do read the committed real ledgers here.
- Anything on real data: no league table, report, batch or session has been run on the real project.
