# FILE_FORM_Conversion_v2: note for the reviewer (focused confirmation asked; EX_313)

**From:** the Claude web chat. **Date:** 24 November 2026, late evening. **Standing:** a package put to the reviewer
for the focused confirmation EX_313 names; not installed; nothing of it run on the owner's PC. **It authorises
nothing.** The day is the owner's own go, part by part.

**What it is.** `FILE_FORM_Conversion_v1` with EX_313 carried out, by small edits to the existing programs and a
shorter sheet. v1 is kept as it was, as evidence. Nothing was redesigned.

| Path under `exchange/CLAUDE_WEB_TOOLS/conversion/` | What it is |
|---|---|
| `package/FILE_FORM_Conversion_v2.zip` | The package. SHA-256 `ca5816cb85813de1df88fbeaf37097c6bd2126fa59f0d3a36f7927783f1c091c` |
| `package/FILE_FORM_Conversion_v2/` and `package/FILE_FORM_Conversion_v2_MEMBERS.txt` | The same content unpacked, and each member's SHA-256 |
| `package/FILE_FORM_Conversion_v1_TO_v2.diff` | Every difference in the four members that changed (line endings set aside) |
| `trial/REHEARSAL_OF_THE_SHEET_v2.txt` | The sheet rehearsed in the cloud from the built ZIP, in the sheet's order, with the restoration |
| `tools/test_convert_to_file_form.py` (46), `tools/test_stage_and_refresh.py` (20) | The two programs' tests, all passing |

**Unchanged from v1, byte for byte:** `repo_overlay/` (the 12 files that go into the living project), `tools/file_form.py`,
`run_suite.py`, `compare_suite_reports.py`, `compare_fill_with_old_records.py`. The conversion list differs in the
one line `made_from_commit`. So the science, the serialization and the suite evidence you passed in EX_312 are
those of this package.

## EX_313 and EX_312 C01 to C05, point by point

| Point | What v2 does |
|---|---|
| **No resumption** (EX_313 item 4; C02, C05) | The conversion program refuses a record that already exists, before a lock is taken or a byte is changed: "one attempt ... never resumed or repeated". The second-run branch and `read_record` are gone. Both typed words are asked for **before** the first change, and the record is written only then, so "not confirmed" always means "nothing changed, no record". Every STOP ends with the same words: run nothing again; the way back is the whole folder from the copy, on the owner's go. No recovery of temporary files, no state machine. |
| **Whole-project copy, verified before the overlay** (C01) | Sheet part 1: `robocopy` of the whole project folder (`.git` and `.venv` included) to a new folder outside it, then the verifier's new phase `copy`, which compares every file of the project folder with the copy, whole. Part 2 does not begin without `COPY PASS`. The conversion program's own check of the copy (every file it changes or removes, by SHA-256) stays. |
| **Package verified before the overlay** (C01) | `certutil` on the ZIP against the SHA-256 above; phase `pre` now also checks every overlay file against the manifest before anything is copied; `pre`, `xcopy` and `post` are one `&&` line, so no copy follows a failed check (C05). |
| **DEV only** (C01) | The settings file must say `[environment] role = DEV` and its `tree_root` must be this folder; a tree without a settings file is refused. Named by fixed words only. |
| **Orphan marker** (C01) | `transitory_data/poc_runs/UNRESOLVED_ORPHAN.json` existing is a finding: nothing is changed. |
| **Original bytes before each removal** (C02) | Each file is hashed again immediately before it is unlinked and removed only while it has the SHA-256 it had at the look, which is the one the copy holds. A file gone or changed stops the run. |
| **Statuses valid and ACTIVE-only** (C03) | A status file is removed only if its own `[check]` digest holds over its bytes, it holds at least one status, every status is `ACTIVE`, and it records no withdrawal or eligibility draw. |
| **The four masters and ledgers** (C03) | All four are named; one missing is a finding. Each is hashed at the look and proved unchanged at the end, as in v1. |
| **GAIS** (C04) | Excluded by name from every candidate of the staging program, for staging and for refreshing. |
| **Previously raw-byte-protected, unlisted paths** (C04) | The paths of the old root attribute file's `-text` lines (`source_data/`, `results/`, the install records, the three named files): one whose bytes on disk are not Git's is a finding and stops the run; it is never put back. |
| **Unrelated staged changes** (C04) | Before anything is staged the index must be exactly the last commit; at the proof, nothing may be staged that is not on the list. No commit, no push: the owner does both, the push last. |
| **Links** | Not expanded (EX_313). v1's refusal stays as it was. |
| **Baseline for the suite comparison** (C05) | The sheet checks that the last commit touching `src` or `tests` is `5f16b35` (build step 2), so the suite run made after build step 2 is known to match; otherwise it stops. |

## Three things for your eye

1. **Not rerun:** the planted-fault scripts and the whole suite (the overlay is byte for byte v1's). The fill is the
   owner's part 6.
2. **Not Windows:** `robocopy`, `xcopy`, `ren` and `&&` were not run in the cloud. Part 9 (the restoration) renames
   the stopped folder aside and copies the whole copy back; it does not delete anything.
3. **The runner's rehearsal.** The standard v0.2 says the staging step "is rehearsed by the runner before the day";
   EX_313 says "the already planned Windows rehearsal as appropriate". **Claude's recommendation to the owner is to
   drop it:** with a verified whole-folder copy, a failed real attempt costs one restoration, which is what a failed
   rehearsal on a copy would also cost, and a rehearsal task is one more thing to write, review and run on a night
   when the owner's plan is ending. No task file has been written. It is the owner's decision; if he or you want the
   rehearsal, Claude writes the task.

## The narrow change proposed for RAT-50 (the owner alone ratifies)

> **RAT-50.** For the one conversion of DEV, `doc/FILE_FORM_STANDARD_v0_2.md` section 7 is changed narrowly; the
> document is not re-issued. (a) Its rule that an interrupted conversion "is therefore simply run again" no longer
> applies: the conversion is one attempt; on any STOP it is not resumed, and the whole project folder is put back
> from the owner's verified whole-folder copy, on his go; a fresh attempt comes only after the cause is understood.
> (b) The package `FILE_FORM_Conversion_v2` (ZIP SHA-256 `ca5816cb...1c091c`) is accepted for that attempt.
> (c) *Only if the owner so decides:* section 5's sentence that the staging step "is rehearsed by the runner before
> the day" is waived for this conversion. The backup, the scientific protections and every other rule stand.
