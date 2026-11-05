# DOC-12 - install the ratified H-2 v1r9 and register v0.25 (owner-run; document-only route)

Prepared by Claude, 6 November 2026, after the owner's ratification RAT-25 ("ok review is ok. Ratify H-2 v1r9 and register v0.25
candidate 3 ratified"). The two documents are candidate 3, reviewed in EX_153 and EX_155, with only their status lines changed
to record the ratification. `diffs/` shows exactly what changed from candidate 3.

## What ends up where

| File (LF content) | Bytes | SHA-256 |
|---|---|---|
| `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r9.md` | 36211 | `99a84910b3333345e1ec5c9497fb77506d9f936e301f3a732897651c130fde69` |
| `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r9_introductory_blurb.md` | 8188 | `2d9744fe47c2e783ac4b7e0f75a81a73874324dea1374423ce1ff8c90f45d664` |
| `doc/RATIFICATION_REGISTER_v0_25.md` | 273221 | `2ef9d17cfbc76c556e00d659677e411686c60aab263e1b0f0ef002930ee6d874` |

Removed from `doc/`, because they are candidate copies whose history is kept in `exchange/`:
- `doc/HANDOVER/HANDOVER_2026_11_06/` (the whole folder);
- `doc/RATIFICATION_REGISTER_v0_25_CANDIDATE.md`.

Unchanged:
- `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r8.md` and `doc/RATIFICATION_REGISTER_v0_24.md` stay, as history.
- Claude's H-1 v1r9 delta was not ratified and stays in `exchange/HANDOVER_2026_11_06/`.

## Steps (Windows CMD, in the repository folder)

1. `git pull`
2. `.venv\Scripts\python.exe exchange\DOC12\install_doc12.py copy`
   Expect `DOC12 COPY PASS`.
3. `git rm -r -q doc/HANDOVER/HANDOVER_2026_11_06 doc/RATIFICATION_REGISTER_v0_25_CANDIDATE.md`
4. `git add doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r9.md doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r9_introductory_blurb.md doc/RATIFICATION_REGISTER_v0_25.md`
5. `git status`
   Expect only those three files added or modified and the candidate copies deleted. Anything else listed: do not commit;
   ask Claude.
6. `git commit -m "DOC-12: H-2 v1r9 and register v0.25 (owner-ratified 6 November 2026, RAT-25)"`
7. `.venv\Scripts\python.exe exchange\DOC12\install_doc12.py verify`
   Expect `DOC12 VERIFY PASS`.
8. `git push`

If step 2 or step 7 prints STOP, stop there and send Claude the output. Rehearsed by Claude on a throwaway clone of main: COPY
PASS, VERIFY PASS.
