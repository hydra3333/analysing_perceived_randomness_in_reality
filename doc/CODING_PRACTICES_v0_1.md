# Predictive Randomness - coding practices - v0.1

**Status:** OWNER-RATIFIED 22 November 2026 with RAT-40 (decision log entry 147), as a note of ratification to the system
specification v0.6 and the deployment design v0.12. It is a one-page checklist, checked by eye. It adds no tool and no
approval step: every code package says "coding practices met" or lists its exceptions with reasons, and the reviewer
checks code against it in its ordinary review.
**Applies to:** all new code from build step 2 on, and the light tidy-up of the existing method files (section 6).
**Source:** the project owner's words in the Claude chat of 22 November 2026 (13:26 and 13:33), set out as a list by
Claude. Items marked (Claude) were added by Claude at his invitation; the owner may strike them.

## 1. Every `.py` file opens with a plain-English header

- What the file is for, in two or three sentences.
- Which part of the specification it carries out.
- Which of the project's own modules it uses, and what each is used for.
- What uses it.

## 2. Constants and settings

- Constants are declared at or near the top of the file, each with a comment saying what it is and why it has that
  value. No unexplained number or text sits in the body of the code.
- No path, drive letter or role is written in code; they come from the settings file.
- **A setting that is needed and is missing, empty or malformed in an `.ini` file is checked for and refused at the
  start,** with a message naming the file, the section and the key.

## 3. Every function or self-contained block

- A comment in plain English: what it does; each parameter and what it means; **what it returns, with a good example
  of the returned data;** what makes it refuse.
- Comments that say why, wherever the reason is not obvious from the code.
- One job each; long functions are split.

## 4. Names

- A name says what the thing is and matches its purpose: `first_eligible_draw`, not `x`, `tmp`, `data` or `val`.
- A name shows whether it holds a draw number, a count or a position in a list.
- No abbreviations except the project's own terms.

## 5. Behaviour and messages

- **An error message says what occurred, where, and why, and advises what to do about it.** A fault stops loudly;
  nothing is swallowed or skipped silently.
- **Wherever variants are held or results are not current, the job says so plainly at its start and again at its end,**
  names the cause, and gives the exact command to run (the owner's condition of ratification).
- Messages to the owner use the project's words: restore from backup, catch-up, walk-forward, historical walk-forward
  rerun.
- Results never depend on the clock, the PC's locale or accidental ordering; seeds are explicit.
- (Claude) Every command says at its start which tree it is running in (role and root) and what it is about to do,
  and ends with one plain line saying how it finished.
- (Claude) One piece of shared code for each shared task (reading the settings, hashing a file, writing a list line):
  it is not copied into several files.

## 6. Housekeeping

- No commented-out code and no leftovers.
- Each test is named for the rule it proves, and each rule has a test with a planted fault.
- **The light tidy-up of the existing method files (owner, 22 November 2026):** after build step 1 is proved and before
  anything is installed into QA or PROD, each existing method file is given its header and dependency list, and
  comments where they are plainly missing. No calculation changes; the equivalence check of step 1 is run again to
  prove that no forecast changed. It is done then because a variant's files can never change once installed.

End of the coding practices, v0.1.
