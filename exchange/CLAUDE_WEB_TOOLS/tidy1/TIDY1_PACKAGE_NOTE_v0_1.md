# The light tidy-up of the existing method files - package note v0.1

**Date:** 23 November 2026. **Author:** the Claude web chat. **Status:** built and proved in the cloud; NOT yet
reviewed; NOT installed. It authorises nothing: the owner's install is on his own separate go.
**Authority:** the owner's ratification RAT-40, note 3 (decision log entry 147): "each existing method file is given
its header and dependency list, and comments where they are plainly missing. No calculation changes; the
equivalence check is run again"; `doc/CODING_PRACTICES_v0_1.md` sections 1 to 3 and 6. The owner's go: entry 165.
**Base commit:** `7be6b3aa8115d6a44edd9ab59180c1cdcfcda674` (`src/` and `tests/` as build step 1 left them, `0aea10a`).

## 1. What it does, in plain English

It replaces 37 existing method files with the same files carrying fuller headers and comments. No file is added,
moved or deleted. No line of code changes.

- **Headers.** Each of the 37 files now begins with the header of the coding practices: what the file is for; which
  part of the specification (and which design document and section) it carries out; which of the project's own
  modules it uses and what for; and what uses it. The header each file had before is kept, word for word, under its
  own label, because it holds the mathematics.
- **Function comments.** 64 of the 130 functions in these files had no comment. Each now has one: what it does, each
  parameter, what it returns with an example, and what makes it refuse. Every example value is invented to show a
  shape; none comes from a real draw.
- **Constants.** Each family core gets one note saying what its fixed constants are; six other constants that had no
  comment get one.
- **Out-of-date wording corrected.** The family `__init__.py` files said "`contract` connects the method to the
  shared contract runner" and named helpers at `_common/...py`; since build step 1 those files are `core_v1.py`
  and `_shared/..._v1.py`. The new headers say so.

## 2. The files (37)

| Files | Count |
|---|---:|
| `E_002` ... `E_019` (11 families): `__init__.py`, `core_v1.py`, and `variants.py` (E_6: `beta_bernoulli.py`) | 33 |
| `_shared/occurrence_counts_v1.py`, `polynomial_fits_v1.py`, `recurrence_gaps_v1.py` | 3 |
| `E_001/FULL_HISTORY_RAW_COUNTS_V1/method.py` (E_1's variant file, the former wrapper) | 1 |

1,385 lines added and 259 removed, all of them comment or docstring lines
(`evidence/TIDY1_CHANGE.diff`, `evidence/TIDY1_CHANGED_FILES.txt`).

**Not touched, and why:**

- **The 39 `method.py` files written in build step 1** already have these headers and comments.
- **Six of E_1's own modules** (`E_001/__init__.py`, `e1_common_reader_bridge.py`,
  `e1_historical_appearance_frequency.py`, `e1_standalone_contract.py`, `e1_training_view.py`, `multigame_e1.py`).
  The old system's archive tests rebuild E_1's earlier revisions from these files' exact bytes and compare two of
  them with reference hashes (`tests/test_code3_retirement.py`, `tests/test_e1r3_revision3.py`). One added comment
  would fail those tests, and a reference hash is never refreshed. The package's verifier guards all six.
  **This is a choice for the owner** (section 6).
- **The old system's own machinery** under `_common/` and `src/` outside the method families. It is not a method
  file, and build step 2 replaces what the new system needs of it.

## 3. How it was made

`make_tidy_up.py` applies the wording held in `tidy_texts.py` to a clean clone, and refuses on anything unexpected: a
function left without a comment, a comment written for a function that is not there, a constant that already had
one. Nothing is typed into the method files by hand, so the reviewer can read every new word in one file.

## 4. The proof that no calculation changed

| Proof | Result | Evidence |
|---|---|---|
| **Comments-only check** (`check_comments_only.py`): each file's code, with comments and docstrings removed, compared before and after | 211 Python files under `src` and `tests` compared; 37 with changed text; 0 with a problem; `RESULT: PASS` | `evidence/COMMENTS_ONLY_CHECK.txt` |
| **The suite, before and after**, compared test by test (the tools of build step 1) | 45 modules, 571 tests, all identified in both runs; the same result for all 571; the same three known failing tests | `evidence/suite_before/`, `suite_after/`, `SUITE_COMPARISON.txt` |
| **The equivalence check of build step 1, run again** on the tidied tree (the same tool, byte for byte) | 17,400 of 17,400 scored forecasts equal by content digest (Powerball 11,442; Oz Lotto 5,958); no `DIFFERENT`, no `FAILED`. **`RESULT: PARTIAL`, as it must be in the cloud:** the 5,838 and 2,802 never-scored forecasts exist only in the owner's run folders | `evidence/EQUIVALENCE_CLOUD_TIDIED_TREE_PART_1_OF_2.txt`, `..._PART_2_OF_2.txt` |
| **Install rehearsal** in an LF clone and a `core.autocrlf=true` clone, and five planted faults | both installs pass every phase; all five faults STOP, including a planted change of a calculation constant | `evidence/INSTALL_REHEARSAL.txt` |

The comments-only check is the direct proof: Python runs the same code. The suite matters for a second reason:
several tests read the method files as text and refuse certain words in them, and the new wording passes them.
**The complete equivalence evidence is the owner's run** (sheet part 4), which must end `RESULT: PASS - COMPLETE`.

## 5. The package

`package/TIDY1_Method_Comments_v1.zip`, SHA-256
`a8d2f1136a41a361e665ef2b16e2f3ce073dff64b52e697f4588971fc812ad4c`, 44 files: the overlay (37), the read-only verifier
from the project's reviewed template (30 guarded files), the manifest, the sheet, and four tools (three are the tools
of build step 1 unchanged; the fourth is `check_comments_only.py`). The sheet has the parts the owner ran for build
step 1, less the deletions and the ZIP: baseline suite; check, copy, check and the comments-only check; the suite
again and the comparison; the equivalence check; commit, check, push. About 95 minutes, nearly all of it unattended.

## 6. For the owner to decide

**Question.** E_1's six own modules get no new comments. Is that acceptable?
**Why it matters.** RAT-40 note 3 says "each existing method file". These six are method files of a kind, and they
keep their old headers.
**Recommended: yes, leave them.** Their bytes are pinned by the archive tests that prove the old system's E_1
history; touching them trades a real safeguard for comments on code that the new system calls through one
unchanged function. The new E_1 variant file's header now says what they are and how they are used.
**The other option.** Comment them too, and change the two archive tests to expect the new bytes. That edits tests
of the sealed history for the sake of comments; not recommended.

## 7. Coding practices

**The new tools** (`make_tidy_up.py`, `tidy_texts.py`, `check_comments_only.py`, `build_tidy_pkg.py`): coding
practices met.
**The 37 tidied files:** headers, dependency lists, constants and function comments now meet sections 1 to 3.
Exceptions, all because the tidy-up may change no code: names are unchanged; comments that existed but are brief
were left as they are; the error messages are unchanged; and the six E_1 modules of section 6.
