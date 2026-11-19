## Appendix B. Changes in v7

v7 is a full edition made from H-1 v6's ratified bytes (`6dc8185a...0353`, RAT-38) by counted edits, each asserted to occur exactly once, by inserted rows and bullets, and by replacing whole parts (`exchange/CLAUDE_WEB_TOOLS/h1v7/make_h1_v7.py`, with its fragments in `h1v7/frag/`). It was written on 19 November 2026 at the owner's go (decision log entry 105), to fold in what was decided after v6 was written, at his request "at the earliest convenient time".

### B.1 What changed, by section

1. **Header:** v7; status; baseline date; what it replaces.
2. **Section 0:** item 2 names the operative H-2 (v3r4) and register (v0.31) and the v7 blurb; item 3 notes that v6 was ratified with its header reading CANDIDATE.
3. **Section 0B:** its date and the pointer to decision log entries 99 to 105; item 10's note on the reviewer's handover; item 12's rollback bullet points to item 13; **item 13 (new): since v6 (EX_244 governs restore and replay; the restore method; no replay comparison; no monthly restore test; Python 3.15 only; the open questions on formal OV-1 and the orphan marker after a restore; the takeover; RAT-38; the reviewer's handover; the checks of 19 November).**
4. **Section 1.1:** Claude's commit rights include reviewed and ratified documents into `doc/` (as section 1.6 already said).
5. **Section 4:** the register paragraph names v0.31 (the stale v0.29 and v0.30 sentence replaced).
6. **Section 5.3:** E_2 has three variants, not six (the total of 40 per game was right).
7. **Section 7.4:** Python 3.15 only. **Section 7.5:** Claude may read `results/` (the approach of 16 November 2026).
8. **Section 8.3:** one Python 3.15 build. **Section 8.6:** 84 Bash deny patterns and three allow lines (editions to v6 said 87). **Section 8.8:** three lessons added at the end.
9. **Section 10, item 2:** the takeover was accepted; this edition is not a prerequisite. **Section 11:** Claude's `doc/` commits for ratified documents.
10. **Section 12.1:** the EX numbering line and the code round's interpreter. **Sections 12.3, 12.9 and 12.10:** one Python 3.15 build. **Section 12.8:** rewritten for 19 November 2026. **Section 12.11:** revised (what is settled since v6; the ten safeguards of EX_246 Q3 as the design note's checklist; the restore by the owner's method; the "do not" list extended).
11. **Appendix A:** two blurb paths now under `doc/HANDOVER/superseded/`; the settings row (84 and 3); rows for H-1 v6 (RAT-38), the operative H-2 v3r4, the H-2 v3r6 candidate, EX_244, EX_245 and EX_246.
12. **Appendix B:** this appendix.
13. **Section 2A is unchanged, byte for byte** (the builder asserts it).

Deliberately not changed here: the ratified documents (the design's Appendix J, the direction document's section 9, the supplement and the code plan), which are amended with the integrated package; and the reviewer's own H-2, which is its file.

### B.2 Known limits

- Everything B.2 of v6 said still holds: older statements in sections 1 to 9, 11 and 12 that are not listed in B.1 are carried as they were; where they speak of installing by design Appendix J, or of one working clone that is both development and production, read them with section 0B items 12 and 13.
- Section 7 (implementation status) still describes the installed baseline, which has not changed: MHUP-B's code is staged, not installed.
- Section 12.6 describes the owner's clone on E:. The production folder on G: and the backup folder on T: do not exist yet.
- RAT-35 to RAT-38 and the decisions after them are in the decision log and in section 0B, not yet in a register edition (v0.32 travels with the package).
- Test figures quoted "on both Pythons" or "on Python 3.13 and 3.15" are dated history (entry 103).
- This edition is a CANDIDATE until the owner ratifies it. It then goes into `doc/HANDOVER/` as `Claude_Primary_Handover_H1_v7.md` with its blurb, with only its status line changed, and H-1 v6 stays there as history.

### B.3 Integrity

Every fact added here was taken from the repository on 19 November 2026 or from the records named; every hash was computed from the stored bytes by the builder. No file under `src/`, no root `.bat` and no `requirements.txt` has changed since H-1 v4. No design or code was written between v6 and this edition.

**Review:** a documentary look by the reviewer is welcome, not required; the owner ratifies.

