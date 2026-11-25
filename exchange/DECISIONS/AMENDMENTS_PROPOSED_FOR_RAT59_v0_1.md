# Two narrow amendments proposed for the owner's ratification as RAT-59 (v0.1)

**Date:** 25 November 2026. **Author:** the Claude web chat, at the owner's word (decision log entry 318).
**Status:** PROPOSED. Not ratified until the owner says so. The reviewer has given its view of both (EX_329, section 2:
CONCUR, with the one wording change taken in below). As with RAT-56, the two ratified files are not edited: the words
below are how the named clauses are read from the day of ratification. This document authorises no install or run.

## Amendment 1: `Verify_Tree.bat` does not run the test suite (the owner's decision, entry 305)

**Why.** The tests live only in DEV. A QA or PROD tree's own settings do not say where DEV is, and the project's rule
is that the installed software starts no program. The same software then does the same thing in QA and in PROD, and a
tree can be verified with no DEV on the PC (after a restore onto a new one).

**Deployment design v0.12, section 7, first paragraph, is read as:**

> Process check; a backup attempted; the structure; every installed variant's smoke case; the fixed forecast sample,
> whose differences after an environment change are **reported** for the W-23 review and do not by themselves refuse;
> the derived results in full, reported likewise; `ENVIRONMENT_VERIFIED.json`; a backup attempted. **The test suite is
> not run by `Verify_Tree`:** the tests live in DEV and the installed software starts no program; the command says so
> every time. A failed smoke case writes no marker and removes an older one. The owner's install script removes the
> marker before it changes anything. The environment's digest is taken over the fixed inventory of specification
> 13, which does not contain the marker.

**Specification v0.6, section 13, the item "Verified before use", is read as:**

> **Verified before use.** `Verify_Tree.bat`, run in the tree, makes the checks of 12.3 that travel with the installed
> software (items 1, 4 and 5, and every installed variant's smoke case) with that tree's Python and, on success,
> writes `.venv\ENVIRONMENT_VERIFIED.json` with the environment's digest. Launchers refuse without it; each job
> compares the digest at its start; the owner's install script removes the marker before changing anything.

**Specification v0.6, section 12.3, item 3, gains this sentence** (the reviewer's wording, EX_329):

> The suite is run by the install tools in DEV when the target infrastructure is file for file DEV's (at creation,
> every infrastructure reinstall, and an ordinary variant installation when that condition holds), never by
> `Verify_Tree`.

**What it does not do** (the reviewer's cautions, accepted). W-23 is unchanged in full. The smoke cases, the forecast
sample and the derived results in full are not represented as equal to the whole suite. The marker certifies the
environment, not every historical result; the research job's own safeguards remain binding.

## Amendment 2: the job lock at an infrastructure reinstall is let go for the backup and taken again (reading C-R9)

**Why.** Deployment design section 6 has `Reinstall_Infra` take the target's job lock at step 2 and hold it "to the
end", and attempt the `PRE_INFRA` backup at step 4. A backup is never made while a job lock lies in the tree (slice B,
reviewed: the lock file would be inside the ZIP and a restored tree would refuse every job). Both cannot hold.

**Deployment design v0.12, section 6, steps 2, 4, 6 and 11 are read as:**

> | 2 | The process check; the target's job lock is taken and held through step 3; no updater lock, orphan marker or other unfinished operation |
>
> | 4 | The job lock is released. The recovery kit for the new software state is written; the `PRE_INFRA` backup is attempted. Each result is noted exactly as it is. **No earlier backup is looked for, counted or verified** |
>
> | 6 | **The target is reserved again before anything in it is overwritten:** its job lock is taken by an exclusive create, which fails if a job holds it, with a fresh process check and the guard's checks under that lock. **If the accepted plan, or anything step 3's statement rested on, has changed since step 3, the command refuses here, having overwritten nothing, and the owner runs it afresh for a current statement.** Then the barrier, holding the plan and step 3's statement; the updater's own lock; `SNAPSHOT_DUE`. The job lock is held through step 10 |
>
> | 11 | The job lock is released. The `POST_INFRA` backup is attempted and its result reported. If a change from draw X was accepted, the tool ends by naming the command the owner now owes that game: `Rerun_Walk_Forward.bat --game <game> --from <X> --derived-only` |

**What it does not do.** No new kind of lock; no backup inside a job lock; no change to what a backup leaves out or to
the restore's exact set. Step 9's comparison in place is still made. No process is ever ended.

## What ratifying means

One word from the owner ratifies both as RAT-59 (or either alone, if he prefers). Claude then records it in the
decision log with this file's SHA-256, as was done for RAT-56. Slice C's code already follows amendment 1; it follows
amendment 2 once the corrections EX_329 asked for are made (its finding C-B01 is the check named in step 6).
