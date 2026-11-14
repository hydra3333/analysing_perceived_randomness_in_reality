## Appendix B. Changes in v3

v3 is a full edition made from H-1 v2's ratified bytes (`8f15109f...0a30`) by counted edits, each asserted to occur exactly once, and by replacing whole parts (`exchange/CLAUDE_WEB_TOOLS/h1v3/make_h1_v3.py`; the diff from v2 travels with it). It changes no rule; section 1.7 records the working approach the owner adopted as guidance. Nothing in v2 was dropped except what is overtaken below. v2's own change list, including where every section of the v1r10r3 delta went, stays in v2's Appendix B.

### B.1 What changed, by section

1. **Header:** v3, 15 November 2026; the baseline (`main` at `a74cfd9`); status CANDIDATE; replaces H-1 v2.
2. **Section 0:** the blurb's name; CONTINUITY_NOW.md and the decision log read first; H-2 v2 r1 installed; register v0.30; the readiness reviews include EX_177 and the run records; item 3 compares CONTINUITY_NOW.md with the owner's account; item 6 keeps CONTINUITY_NOW.md current.
3. **Section 1:** 1.1 the reviewer chat of 6 November ended after EX_177 and the present one took over (EX_178-EX_180) and has advised since; **1.7 (new)**, the working approach P0-P6.
4. **Section 2:** two bullets (show the reasoning; chat length restated). **Section 2A is unchanged, byte for byte** (the builder asserts it).
5. **Section 4:** the register pointer (v0.29 installed at `5a8527b`; v0.30 with this file).
6. **Section 5:** 5.3 the owner's decisions of 14 November 2026; 5.4 the dependency change and its scoped W-23 acceptance; OUTLANDISH_01's commits during the freeze.
7. **Section 6:** the environment digest is now T024's `5bf4eb8a36dd...` (90 distributions); T016's `966a2792...` kept as history.
8. **Section 7:** 7.1 the dependency change and the documentation install; 7.6 the POC rerun and the updater self-test no longer untested.
9. **Section 10:** item 1 rewritten (done since v2); item 2 this edition; item 3 D1-D7 decided, the remaining prerequisites on the day of the first Approval 1, the expected digest `5bf4eb8a36dd`; item 6 OUTLANDISH_01's family probably first among the methods still to do, and the ideas backlog; D1-D7 removed from the OPEN questions, OUTLANDISH_01's identities added.
10. **Section 11:** the POC rerun and self-test have run; the other prerequisites still need their own gos.
11. **Section 12:** 12.1 EX_190 newest, pasted replies and the run records; 12.6 OUTLANDISH_01 and the owner's commits; 12.8 rewritten; 12.9 item 4 points to CONTINUITY_NOW.md.
12. **Appendix A:** H-1 v2 and H-2 v2 r1 with their hashes; register v0.29; readiness sheet r2c; the decision records of 14 November 2026; the dependency change and T024's report; the run records.

### B.2 Integrity

Every fact added here was checked against the repository at `a74cfd9` (15 November 2026; full history) or taken from the records named; every hash was computed with `git show HEAD:<path> | sha256sum`. The builder asserts v2's input hash, that each counted edit's old text occurs exactly once, that section 2A is byte-identical to v2's (and so to v1r8's), and that the output is US-ASCII with LF line endings and one final newline. Nothing in this edition was run against real data, and nothing is installed by it. Absence from these summaries is not proof of nonexistence; verify the current repository, the ratified source documents and the owner before concluding that a decision, file or obligation does not exist (EX_172 C03).

**Review:** sent with register v0.30 as EX_190 for the reviewer's documentary review; **EX_191**: PASS WITH CORRECTIONS (C01 the installer's modes and when a new digest is needed; C02 CONTINUITY_NOW.md's lower sections; O01 which steps share a day), applied as FIX AND PROCEED in EX_192; section 2A unchanged. The reviewer judged that H-2 v2 r1 needs no new edition before the freeze.

*End of H-1.*
