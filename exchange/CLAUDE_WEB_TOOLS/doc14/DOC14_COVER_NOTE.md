# DOC-14: register v0.27 and design v0.1r7 - for the owner's approval (13 November 2026)

By the Claude web chat (Opus 5.5), under the owner's decision 1 of 13 November 2026
(`exchange/DECISIONS/OWNER_DECISIONS_2026_11_13_MHUPA_CLOSED.md`): documentation of decisions already ratified, not a new
ratification. Nothing is installed. US-ASCII, CRLF.

## 1. The two documents (this folder)

| File | What it is | SHA-256 (LF) |
|---|---|---|
| `Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r7.md` | design v0.1r6 with only RAT-28's amendments, by 10 counted edits (`make_design_v0_1r7.py`, which checks the installed v0.1r6 bytes first) | `c115b289432756b50ff76549be6f44282ca30cd9a94524e6c3271965a085b8de` |
| `RATIFICATION_REGISTER_v0_27.md` | register v0.26 with 3 counted insertions only (`make_register_v27.py`): the version line, the new section (`register_v27_section.md`), and a current-status bullet; nothing of v0.26 changed | `364829394bf7138bdce1452ccc5eb556bf138d83e6d49e9c67c35f026cb48d06` |

Every changed line: `DESIGN_v0_1r6_TO_v0_1r7.diff` and `REGISTER_v0_26_TO_v0_27.diff`.

## 2. What the design edition changes (and nothing else)

- J-1, J-2, J-3, J-4 and the two section 4.3 corrections, in the ratified wording of
  `exchange/CLAUDE_WEB_TOOLS/mhupa/t016/final/APPENDIX_J_AMENDMENTS_RATIFIED.md`, each marked with its label in the table.
- The edition's own lines: the title, the version line (says it records the 11 November ratification and makes no new
  decision), the history line (v0.1r6's version line kept there), and the footer, which read "End of design v0.1r5" since
  v0.1r6 and now reads v0.1r7.
- One editorial point to approve: in 4.3, "40 entries per game (80 in all)" needed "for each game" before "the 39 variants",
  or the sentence would read as 39 in all. No meaning changes.
- Not folded in, on purpose: the stricter checks the package's instructions add (part B of the ratified amendments, recorded
  "for information"); they stay in the instructions and the register.

## 3. What the register edition records

One new section: the integrated package's development and the owner's decisions in it; **RAT-28** (rulebook v0.5 and the
Appendix J amendments, 11 November 2026); the freeze (EX_163, EX_164) and gates B to F with their commits; T016; the live
install and its verification; the post-install test fix (EX_165, EX_166, T023, `87c4219`); the owner's decisions of
13 November 2026; DOC-14 itself; future actions; out-of-date statements; a table of document hashes. The register's
version line says "FOR THE OWNER'S APPROVAL"; on your approval I change only those words to "OWNER-APPROVED <date>" and give you
the new SHA-256.

## 4. Installing, after your approval (your own commit; `doc/` is yours)

```
cd /d E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality
git pull --ff-only
git status --short
copy /Y exchange\CLAUDE_WEB_TOOLS\doc14\Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r7.md doc\
copy /Y exchange\CLAUDE_WEB_TOOLS\doc14\RATIFICATION_REGISTER_v0_27.md doc\
git status --short
git add doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r7.md doc/RATIFICATION_REGISTER_v0_27.md
git commit -m "doc: DOC-14 - register v0.27 and design v0.1r7 (records RAT-28 and MHUP-A's install), owner-approved"
git push
```
Expect two `??` lines before `git add`, and a clean tree at the end. Claude then verifies both files' Git content from GitHub.
v0.1r6 and v0.26 stay in `doc/` (records cite them by name), as with every earlier edition.

## 5. A review?

DOC-13 had the reviewer's documentary check. This round only records ratified decisions, and the design changes are the
reviewed wording itself. A short documentary check by the reviewer is cheap if you want one; otherwise your approval suffices.
