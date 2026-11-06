# GAIS history clean-up - close-out record (6 November 2026)

Written by Claude, the lead (owner's decision, 6 November 2026), after the cutover. US-ASCII, CRLF.

## What was done

Git's history was rewritten to remove a third-party program that had been committed by accident, together with two small
generated files. **No file in the current tree changed.**

**Removed from all history:**
- `src/GAIS/OUTLANDISH_01/y-cruncher v0.8.7.9547b/` (246 files, mostly executables);
- `src/GAIS/OUTLANDISH_01/ycruncher_digits/` (one placeholder file);
- `src/GAIS/OUTLANDISH_01/digits_golden_ratio_10_to_6.bin` and `src/GAIS/OUTLANDISH_01/digits_pi_10_to_6.bin` (1 MB each).

**Kept:** `GAIS/OUTLANDISH_01/Pi - Dec - Chudnovsky.txt` (0.95 MB), which is tracked in the current tree. It is the owner's to
untrack later if wanted.

## Identities

| Item | Value |
|---|---|
| Old `main` | `6b9902968b6f97faffa8c3d4d38b6ea5edb9e389` |
| New `main` (the rewrite) | `9d28b9f51bab150ae5c8f9ccf62388b4853c4d0f` |
| Tree, old and new | `e8be5988e18f79d13cd1e34bbbf461f3659cca2c` (identical) |
| Commits | 416; 389 unchanged; 27 rewritten (5-6 November 2026), mapped in `commit-map.txt` and in the evidence file's section 4 |
| Signatures | 15 rewritten commits, all Claude's, lost their signatures (accepted by the owner); 212 other signed commits unchanged |
| Fresh clone from GitHub after cutover | `main` = `9d28b9f...`; 416 commits; removed paths reachable: 0; `git fsck` clean; packed 45.61 MiB (82.84 MiB before, same mirror method) |
| GitHub refs after cutover | `HEAD` and `refs/heads/main` only, both `9d28b9f...`; the temporary `history-cleanup` branch was deleted |

**Old commit IDs in project records.** Records written before the cutover cite some of the 27 old IDs:
- register v0.25;
- H-2 v1r9;
- EX_154 to EX_156;
- `exchange/DOC12/`;
- the roadmap and the reminders;
- `REPORT_T022`.

They are **not edited**. Use `commit-map.txt`: the old ID is in the first column, the new one in the second. For example, EX_152
`f7d90da` is now `9605ba7`, DOC-12 `377e27a` is now `fafa1ba`, and REPORT_T022 `2eb9abb` is now `e963e0e`. Every document SHA-256
quoted in any record still holds, because no file changed. The rewritten commits' own messages had their abbreviated IDs updated
by the tool. Register v0.26 will cite this folder.

## The gates and the decisions

| Gate | Result |
|---|---|
| Proposal | ChatGPT's proposal v0.1, recommending an audit first |
| Lead | The owner chose Claude to lead |
| Rehearsal | Claude rehearsed on a mirror of GitHub. A whole-history rewrite was rejected (it would renumber every commit); a narrower variant was rejected (it was wrong) |
| Assessment | ChatGPT's assessment v0.1: method PASS in principle; B01-B03 and C01-C05 to meet |
| Gate A | Claude's evidence package (this folder), delivered to the owner outside the repository before any change. ChatGPT's focused recheck: **PASS** |
| C01 | **The owner accepted the loss of the 15 signatures** (recorded in ChatGPT's recheck, section 1) |
| Gate B | The owner made a bundle backup of all refs (`E:\TEMP\repo_before_cleanup.bundle`, 87.75 MiB) and confirmed a clean tree. **The owner waived the reviewer's independent bundle-restore test** ("I am unfussed by testing the restore. I have my own independent download zip of the latest git head and that is good enough for me"). Note: a ZIP of the files holds no history; the bundle remains the only copy of the old history |
| Gate C | Claude pushed `9d28b9f...` to `history-cleanup` only. The owner verified it: the expected SHA, both trees `e8be598...`, an empty diff |
| Gate D | The owner rechecked that remote `main` was still `6b99029...`, then ran one pinned `--force-with-lease` update to `9d28b9f...` (accepted as a forced update), deleted `history-cleanup`, and checked `ls-remote` (main only, `9d28b9f...`) |
| Gate E | The owner confirmed a clean tree, fetched, verified the SHA and both trees, ran `git reset --soft origin/main`, confirmed a clean tree again, and `HEAD` = `9d28b9f...`. Claude then verified from a fresh clone (above) and replaced its own working clone with a fresh one |

## Still open (none of it urgent)

- **Gate F (optional, owner):** clearing the owner's local `.git` of leftover unreachable objects (about 900 MiB on the owner's
  PC; not on GitHub). Copy the `.git` folder first, then `git reflog expire --expire=now --all` and `git gc --prune=now`. This is a
  separate decision.
- **GitHub:** it may keep the old objects for a while. No purge is claimed.
- **Other clones:** any other existing clone of the old history must be re-cloned, never merged back. None is known: Claude Code
  makes a fresh clone per task, and the ChatGPT reviewer has none.
- **Follow-on:** a handover to the owner's OUTLANDISH (GAIS) ChatGPT chat. It covers the relocation of `src/GAIS/` to `GAIS/`,
  the ignore rules, this clean-up, and a recommended ignored folder for large generated files under `GAIS/OUTLANDISH_01/`, with a
  check for oversized output elsewhere. It is not a precondition of anything.

## Files in this folder

| File | What it is |
|---|---|
| `GAIS_Git_History_Cleanup_Proposal_v0_1_ChatGPT.md` | ChatGPT's proposal, as relayed |
| `GAIS_Git_History_Cleanup_Reviewer_Assessment_v0_1_ChatGPT.md` | ChatGPT's assessment, as relayed |
| `GAIS_history_cleanup_GateA_evidence.md` | Claude's Gate A evidence package, as delivered to the owner |
| `commit-map.txt` | git-filter-repo's commit map: old ID, then new ID, for each of the 27 |
| `GAIS_History_Cleanup_GateA_RECHECK_ChatGPT_v0_1.md` | ChatGPT's Gate A recheck: PASS |
| `CLOSEOUT.md` | This file |
