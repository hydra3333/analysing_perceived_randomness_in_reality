# DOC-13 - install the documents ratified on 8 November 2026 (RAT-27). Owner-run; re-runnable.

What it does: copies 8 ratified files into place (overwriting, so it can be re-run), moves 34 superseded editions into
`superseded/` folders with `git mv` (already-moved ones are skipped), and checks every file's SHA-256 before and after the commit.
Rehearsed by Claude twice in a row on a throwaway clone: COPY PASS, MOVE PASS (34 then 0), CHECK PASS, VERIFY PASS.

Files written (from `exchange/DOC13/files/`):
- `README.md`
- `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r10_delta.md`
- `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r10_introductory_blurb.md`
- `doc/METHOD_TEMPLATE/CHANGES.md`
- `doc/METHOD_TEMPLATE/METHOD_SPECIFICATION_TEMPLATE.md`
- `doc/METHOD_TEMPLATE/README.md`
- `doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r6.md`
- `doc/RATIFICATION_REGISTER_v0_26.md`

Moves: `exchange/DOC13/MOVES.txt` (34 lines). H-2 v1r4 stays in `doc/HANDOVER/` (EX_161 C02).

## Steps (Windows CMD, in the repository folder)

```
git pull
git status --short
.venv\Scripts\python.exe exchange\DOC13\install_doc13.py copy
.venv\Scripts\python.exe exchange\DOC13\install_doc13.py move
.venv\Scripts\python.exe exchange\DOC13\install_doc13.py check
git add README.md doc/RATIFICATION_REGISTER_v0_26.md doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r6.md doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r10_delta.md doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r10_introductory_blurb.md doc/METHOD_TEMPLATE/README.md doc/METHOD_TEMPLATE/METHOD_SPECIFICATION_TEMPLATE.md doc/METHOD_TEMPLATE/CHANGES.md
git status --short
git commit -m "DOC-13: register v0.26, H-2 v1r10 delta and blurb, design v0.1r6, template draft 5, README, 34 superseded editions moved (owner-ratified 8 November 2026, RAT-27)"
.venv\Scripts\python.exe exchange\DOC13\install_doc13.py verify
git push
```

- The first `git status --short` must print nothing; if it lists anything, stop and ask Claude.
- `copy`, `move` and `check` must each end with PASS. Any of them can be re-run safely.
- The second `git status --short` must show exactly: 4 lines `A` (register v0.26, design v0.1r6, the two H-2 v1r10 files),
  4 lines `M` (README.md and the three template files) and 34 lines `R` (the moves). Anything else: do not commit; ask Claude.
- `verify` must end with `DOC13 VERIFY PASS`.

If any step prints STOP, stop there and send Claude the output.
