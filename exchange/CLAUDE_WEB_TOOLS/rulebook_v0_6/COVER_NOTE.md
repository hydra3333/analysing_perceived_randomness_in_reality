# Local runner rulebook v0.6 CANDIDATE - cover note (Claude, 22 November 2026)

**Status:** a candidate for the reviewer's review and the project owner's ratification. **Not installed and not in
force.** The runner still obeys the installed rulebook v0.5 (`CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md`, SHA-256
`fa7a5fe229be832880cda4704ed9e7d27af2f4b9462464f7af262e540acd5200`, RAT-30), which this work did not touch.
Written at the owner's request of 22 November 2026 (decision log entry 154), before the Claude chat changes.

**Files here:** `CLAUDE_v0_6_CANDIDATE.md` (SHA-256 `9d2cae3c780344797e6054b1eeeee875db5efc84aa8384ea7b4fa53ca4e8830f`); `make_rulebook_v0_6.py REPO` (the builder: the installed v0.5,
asserted by hash, with section 2A removed whole and nine counted edits); `CLAUDE_v0_5_TO_v0_6_CANDIDATE.diff` (exact:
applied to v0.5 with `patch` and compared with `cmp`; 13 lines added, 34 removed).

## 1. What it is for

The installed rulebook was written for the old system. It is still safe (it forbids more than it need), but it does
not know that a new system exists. This candidate is a **safe baseline for the build:** it loosens nothing, removes one
allowance that has already ended, and names the new system's commands and places so that the runner refuses them
until a later reviewed edition says otherwise.

## 2. What changes, and why

| Where | Change | Why |
|---|---|---|
| Version line | v0.6 CANDIDATE, with a summary; v0.5's history kept | the usual form |
| Section 1 | the reason for the rules no longer says "holdout data must never be seen"; a new paragraph: two systems, three folder trees, "you work in DEV only" | the holdout was opened, scored and sealed; the runner must know QA and PROD exist and are not its business |
| Section 2, heading | the words about section 2A removed | section 2A is removed |
| Rule 4 | covers the outcome of every draw, not only draws from the former holdout on | all draws are treated the same since 16 November 2026; one rule with no boundary is simpler, and it is stricter, not looser |
| Rule 5 | the T016 pointer removed; the rule itself unchanged | section 2A is removed |
| Rule 7 | the T016 sentence removed; **the new system's seventeen owner commands named, never to be run in any tree** | named before they exist, as v0.4 did for MHUP-A's programs |
| Rule 9 | the T016 sentence removed; research job, rerun, withdrawal, install into a tree, copy between trees, backup and restore added | the new system's operations |
| Rule 10 | the T016 sentence removed | section 2A is removed |
| **New rule 11** | the QA and PROD trees and their backup folders are never read, listed, written, created, renamed or deleted; no `ENVIRONMENT.ini` is read or edited; a task step that names them is a STOP | "nothing run for QA or DEV ever writes a byte of PROD"; the runner has no business in either tree |
| **New rule 12** | never change the PC's date, time or time zone | the owner's rule of 17 November 2026 (decision log entry 78) |
| Section 2A | **removed whole** (26 lines) | its own A1 says it ended when T016's report was committed |
| Section 3 | one line: nothing outside the repository is the runner's to write; rule 11 | the same |

## 3. What is deliberately not changed

- **Rule 5 (the runner never reads the data folders itself).** The AI chats may read them since RAT-34; the runner still
  may not. EX_206 Q4 left a rewording of rules 4 and 5 to a later reviewed edition. The runner has no need to read
  them: its tests read through the project's reader. **Recommendation: keep rule 5 as it is.**
- **The expected-refusal rule and the evidence rule of the removed section 2A (A5, A6).** They were allowed for T016
  alone. A rehearsal of the new system's install tools will need them again (a tool that must refuse is tested by
  making it refuse). They should come back in the edition that first allows such a rehearsal, with that rehearsal's
  exact scope, and not as a general permission now.
- **No allowance for build step 1.** Its equivalence check must read the old forecast records, which exist only on the
  owner's PC under `results`. Whether the runner or the owner runs it, and under which rule, belongs to that step's
  package and its review.

## 4. For the reviewer and the owner

1. Is rule 4's wider wording right, or should the old boundary be kept until a later edition?
2. Is rule 11 worded tightly enough (it names examples and "wherever the owner's settings place them")?
3. Should this baseline be ratified and installed now, before build step 1, or wait and be merged with the first
   edition that allows a rehearsal? **Claude's recommendation: install it before build step 2,** when the new commands
   first appear in the clone; it is not needed for build step 1, which adds no new command.

## 5. Proposed lines for `.claude/settings.json` (the owner edits that file; nothing here changes it)

`Bash(*.bat*)` is already denied, so no new `.bat` can be run by text. To back rule 11 with the tool's own refusal, add
to `permissions.deny`:

    "Bash(*TEST_BED*)",
    "Bash(*a_p_r_i_r*)",
    "Bash(*ENVIRONMENT.ini*)"

If the owner's settings place QA or PROD elsewhere, the patterns follow those names. When the new system's Python
programs exist, each gets a deny pattern by name, as MHUP-A's did (the owner's F1 lines), and
`exchange/CLAUDE_WEB_TOOLS/check_task_commands.py` is run on every task file. Deny patterns for reading files outside
the repository are not proposed here: their exact form should be checked against Claude Code's own documentation by
the chat that writes the first rehearsal task.

End of the cover note.
