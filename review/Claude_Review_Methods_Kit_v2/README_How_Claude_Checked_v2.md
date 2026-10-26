# How Claude checked things - review methods kit v2

**Date:** 26 October 2026, evening (Adelaide).
**Written by:** Claude, reviewer chat (the one that wrote handover v10), at the project owner's request.
**For:** the project owner, and any later Claude or ChatGPT chat, to see what was checked and how, and to reuse the same checks.

**Principle:** verify, don't assert. Every claim in a handback is checked against the actual bytes, using independent methods rather than the author's own scripts where possible.

## 1. Contents

**v2 adds** `inputs/` (the review inputs not already in the repository, byte for byte) and `INPUTS_INDEX_v2.md` (every input with its SHA-256 and location).

| Item | What it is |
|---|---|
| `reviews/Claude_Review_ChatGPT_Coder_Handover_v1_0_v1.md` | The full review of ChatGPT's coder handover v1.0 (committed in `review/`) |
| `reviews/Claude_Response_ChatGPT_MR_v0_2_Review_v1.md` | Item-by-item response to ChatGPT's review of ranking proposal v0.2 (not previously committed) |
| `reviews/Claude_Review_Package2_v0_11_v1.md` | Review of the Package 2 v0.11 code (1 blocker, 1 correction) |
| `scripts/01_verify_commit_hashes.sh` | Hash files as stored at a commit (`git show <commit>:<path>`) |
| `scripts/02_removed_lines.sh` | Base lines missing from a candidate (catches silent loss) |
| `scripts/03_protected_blocks.py` | Section hashing to prove protected blocks byte-identical |
| `scripts/04_id_inventory.py` | Ratified ID survival (catches dropped IDs) |
| `scripts/05_coordinator_ast.py` | Protected-function AST comparison, plus the diff-rebuild instruction |
| `scripts/06_e1_synthetic_goldens.py` | Recompute the ratified synthetic E_1 goldens |
| `scripts/07_statistical_toys.py` | The exact enumerations that settled the N1 calibration questions |
| `inputs/` | Integration candidates v1 ZIP, ChatGPT's review of it, Package 2 v0.11 ZIP |
| `INPUTS_INDEX_v2.md` | Every reviewed input, its SHA-256, and where it lives |

Run Python scripts with `python -I`. Run them on scratch copies, never on the working checkout.

## 2. Checks by kind of work

### 2.1 A commit or snapshot (any time the owner pushes)

1. Clone or fetch, then `git log --oneline` and `git diff --name-status <old> <new>` to see exactly what changed, including renames.
2. Hash every file that matters with `git show <commit>:<path> | sha256sum` (script 01).
   - Git stores `.md` and `.py` with LF line endings. A CRLF file delivered in chat is compared via `sed 's/\r$//' file | sha256sum`.
3. Confirm that things that must be absent are absent (for example `src/GAIS/`), and that moved files kept their hashes (renames shown as R100).

### 2.2 A handover or handback document

1. Check that the file is complete: its hash and size match the author's report, and it has its closing marker.
2. Diff it against its predecessor. List every **removed** line and make sure each is either replaced by an updated version or genuinely obsolete (status lines). This is how "nothing good is lost" is proven.
3. Look up every 64-hex hash it cites in the repository (`git grep <hash> <commit>`). A hash found nowhere is either an external artefact or an error.
4. List the whole repository tree and compare it with the document's inventory. This is how the unreviewed GAIS script was found.
5. Mark each claim VERIFIED, OWNER-REPORTED or UNVERIFIED, and correct any that are wrongly labelled.

### 2.3 A governing-document edition (consolidation or integration)

1. **Removed base lines:** these must match the evidence note's list exactly, both count and content (script 02). Read every replacement line, especially any ratification or status sentence. For example, R3 0.1 must keep the [R3-PROPOSED] provisions ratified.
2. **Protected blocks:** byte-identical by your own extraction (script 03).
3. **IDs:** every base ID survives (script 04), and every required item of the source being integrated is present.
4. **Rules without IDs:** search for each one by its distinctive wording. ID checks cannot see them. That lesson came from consolidation v0.3.
5. **Old wording:** search for phrases that should be gone or qualified, and read each remaining hit in context.
6. **Cross-references:** check that every reference in moved text points to its new home. Claude missed this on the integration package, and the ChatGPT reviewer caught two relics of the source proposal's own numbering. Add it every time text is moved between documents.
7. **Encoding:** new text should be ASCII; existing UTF-8 text stays as stored, so protected blocks keep their bytes.
8. **Holdout:** search for number lists, then check where each one comes from without printing its surroundings (mask the digits). Every list must be a frozen forecast or an existing illustrative example.

### 2.4 A code package

1. Verify the ZIP hash and every file against its manifest.
2. Build a scratch tree: `git archive <base> | tar -x`, then copy the overlay over it, and check that the retired paths are absent.
3. Run the offline test suite yourself and explain every skip.
4. **Coordinator:** apply the "exact" diff to the committed v0.6 and `cmp` the result with the shipped file. Compare the protected-function ASTs yourself (script 05). Then **read every changed unprotected function by hand**: timing, waits, exit observation, receipt paths, gates. Grep the switches and the allowlist.
5. **Scientific boundaries:** read the reader line by line. Ask of every object that reaches a method: could any field depend on draws at or after N?
   - That question found the v0.11 blocker: a whole-file hash in the method-facing view. At the last development target it would allow brute-force recovery of the target draw.
   - When estimating such a channel, count the **ordered** rows as stored. Claude first understated it by counting unordered sets.
6. **Goldens:** confirm that the tests assert the **ratified** values (R2 5.5), not merely some values. Recompute them with the committed code (script 06).

### 2.5 A statistical or calibration claim

1. Write the smallest toy that could break the claim, and enumerate it exactly with `fractions.Fraction` (script 07).
2. Test both directions: a claimed failure (the counterexample) and a claimed rescue (for example the invariance of hit codes).
3. State the exact conditions under which "exact" or "calibrated" holds: a fixed grid, outcome-independent selection, single-track hit codes.

## 3. Habits

- **Holdout discipline:** never print draw rows. Print only the needed fields (`cut -d, -f1-2` for draw number and date) and mask digits when showing context.
- **Isolation:** unpack every ZIP into its own fresh folder, and run Python on untrusted content with `-I`.
- **Correct yourself in the open.** For example, Claude's mid-review figure of "134 million" was corrected in the file to about 6.6 x 10^11 ordered rows.
- **Present findings** as BLOCKER / CORRECTION / OPTIONAL, with exact locations and replacement text, and end with a paste-ready block.
- **The speculative lens:** a change is acceptable if it makes a number more honest without making any idea, method or measure ineligible. Prefer "mark, never suppress".
