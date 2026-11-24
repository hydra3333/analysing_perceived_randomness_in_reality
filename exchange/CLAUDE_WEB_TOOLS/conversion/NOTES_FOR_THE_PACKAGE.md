# The conversion to the file-form standard: Claude's working notes (not a package; nothing here is reviewed or installed)

**State, 24 November 2026, late evening (decision log entry 254).** The package is built
(`package/FILE_FORM_Conversion_v1.zip`, made by `build_package.py` from the working sources here and
`package_sources/`) and is with the reviewer (`package/FILE_FORM_Conversion_v1_REVIEW_NOTE.md`). Nothing has run on
the owner's PC but the look-only run of entry 249.

## What is here

| Path | What it is |
|---|---|
| `overlay/` | The files the package will deliver, in working form (LF; the package delivers them CRLF): the rule `deploy/file_form.py`; the engine's helper `src/research/windows_text.py`; the four engine modules whose writers changed (`reports.py`, `status_file.py`, `derived_check.py`, `job_lock.py`); two lines of the old `src/two_site_results_check_v0_7.py`'s self-test; `deploy/INFRA_MANIFEST.ini` (one line added); the tests `tests/test_file_form.py` (52) and `tests/test_research_file_form.py` (16) |
| `git_settings/` | The two Git settings files the package delivers into the root, under plain names so that Git does not obey them here: `gitattributes` (`* -text`) and `gitignore` (two lines added) |
| `make_conversion_list.py` | Makes the conversion list from Git at HEAD with the package's files laid over it |
| `tools/convert_to_file_form.py` | The conversion program the owner runs in DEV (standard library; never calls Git) |
| `tools/test_convert_to_file_form.py` | Its tests on an invented tree (41) |
| `tools/stage_and_refresh.py`, `tools/test_stage_and_refresh.py` | After the conversion: stages the listed files exactly as on disk and puts every other tracked file's working copy back to Git's own bytes; proves that what is on disk is what is committed; commits nothing (17 tests) |
| `plant_faults_in_writers.py`, `plant_faults_in_conversion.py`, `plant_faults_in_staging.py` | Plant one fault at a time and show that the tests catch it (11 of 11; 22 of 22; 11 of 11) |
| `trial/` | The cloud trial's evidence |
| `look_kit_r1/`, `LOOK_ONLY_SHEET_r1.md`, `look_kit_TO_r1.diff`, `make_look_kit.py` | The three files (in Windows form) and the sheet for the owner's look-only run in his real DEV, before anything is packaged, corrected after the reviewer's EX_308 (decision log entries 246 and 247). `look_kit/` and `LOOK_ONLY_SHEET.md` are the first edition, kept as the reviewer read it |

## Still to do before it is a package

1. **Done in the cloud (decision log entry 250): the one refresh of the owner's working copy and the staging of
   the converted files,** as the program `tools/stage_and_refresh.py`; `trial/SIMULATED_DAY_IN_GIT.txt` says what
   plain Git does and does not do. **Open with the owner:** the root attribute file needs two more lines so
   that `GAIS\` is truly left as it is (a narrow amendment of the standard's section 5); `git_settings/gitattributes`
   still holds the one ratified line.
2. **The sheet** (the owner's copy first; the package's files; a look-only run; the run; the refresh and commit;
   the suite; the fill; the comparison with the old system's records).
3. **The package itself:** the overlay in its form, the list, the tools, the verifying script, the manifest.
4. **A rehearsal by the runner** in a scratch tree, and a look-only run by the owner in his real DEV beforehand
   (it changes nothing and shows what his tree holds that Git does not track).
5. **Slice A's working files** (`../step3/overlay/`) brought to the standard and rebased on this package (its
   manifest and settings files were written before it).
6. One line for the coding practices at their next edition: every write names its line ending.

## Readings of the standard to put to the reviewer with the package

1. **The search for writes that name no line ending covers the project's programs, not the tests' own code.**
   Tests write made-up files in temporary folders about 130 times without naming one; section 2 puts "whatever a
   test writes in a temporary folder" outside the standard.
2. **Section 4's "17 ... to be corrected":** sixteen are in `src/results_master_v0_2.py`, which section 3A leaves
   exactly as it is; they stay. Two, in the old two-site checker's self-test, are corrected.
3. **What is listed beyond `src`, `deploy`, `tests` and the root's files:** `.claude/settings.json`,
   `.vscode/settings.json`, the runner's three tools, and the two results verification records. Not listed, as
   ratified text or history: the runner's rulebook, its inbox and outbox, its other documents. The suite's own
   check walks exactly what section 6 says (`src`, `deploy`, `tests`, the root's files), so the seven others are
   converted but not watched by that test afterwards.
4. **The three documents in the root** (`README.md`, `CLAUDE.md`, the old safety review) are the root's own
   files and are converted.
5. **The program itself removes what is made again** (DEV's research results, status files, control-folder
   leftovers), on a second typed word, after checking each file against the owner's copy. The standard says
   "removed on the owner's own go" and, in one place, "by hand"; a program that removes exactly the files it
   listed and checked is safer than a typed `rmdir`.
6. **Anything in the walked folders that fits no class stops the run before a change,** the `scratch\` folder
   included: the standard's table names no class for it.
7. **A status file's check is now over CRLF bytes,** and a status file in the old form is refused with a plain
   message. DEV's are removed by the conversion; QA and PROD do not exist yet.
8. **One new infrastructure file,** `src/research/windows_text.py` (class `derived`): the one place where the
   engine turns its texts to the standard's form.
10. **A second program, which does call Git,** stages and refreshes after the conversion. The conversion program
    still never calls Git. Staging a commit is what Git is for; no tree's readiness is ever asked of Git.
9. **The list's "before" for a file the package delivers is its "after":** such a file found in any other state
   means the package's files were not copied; a real run refuses, a look reports it. The program takes the
   standard's rule from the copy beside it, checked by SHA-256 against the list, never from the tree.
