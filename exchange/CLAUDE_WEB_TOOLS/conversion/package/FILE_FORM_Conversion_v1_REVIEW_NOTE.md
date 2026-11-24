# FILE_FORM_Conversion_v1: note for the reviewer (the conversion of DEV to the file-form standard v0.2)

**From:** the Claude web chat. **Date:** 24 November 2026. **Standing:** a package put to the reviewer; not installed,
nothing of it run on the owner's PC except the look-only run of entry 249 (an earlier edition of one program).
**It authorises nothing.** The rehearsal by the runner and the day itself are each the owner's own go.

## What is put to you

| Path under `exchange/CLAUDE_WEB_TOOLS/conversion/` | What it is |
|---|---|
| `package/FILE_FORM_Conversion_v1.zip` and the same content unpacked in `package/FILE_FORM_Conversion_v1/` | The package; `package/FILE_FORM_Conversion_v1_MEMBERS.txt` gives each member's SHA-256 |
| `package/FILE_FORM_Conversion_v1/INSTALL_AND_RUN_SHEET.md` | The owner's sheet for the day |
| `build_package.py`, `make_conversion_list.py`, `package_sources/` | How the package is made; every count and hash in the sheet is computed by the builder |
| `overlay/`, `git_settings/`, `tools/` | The working sources (LF) of what the package delivers in CRLF |
| `tools/test_convert_to_file_form.py` (41), `tools/test_stage_and_refresh.py` (17) | The two programs' tests |
| `plant_faults_in_writers.py`, `plant_faults_in_conversion.py`, `plant_faults_in_staging.py` | Planted faults: 11 of 11, 22 of 22, 11 of 11 caught |
| `trial/` | Claude's evidence from the cloud |
| `look_result/OWNERS_LOOK_20261124.txt` | The owner's look-only run in his real DEV: no finding |
| `NOTES_FOR_THE_PACKAGE.md` | The readings of the standard (its second list, items 1 to 10) |

## What the package changes in the living project

1. **Four engine modules write CRLF** through one new helper, `src/research/windows_text.py`: `reports.py`,
   `status_file.py` (its check is now over the CRLF bytes; a file in the old form is refused), `derived_check.py`,
   `job_lock.py`. No `.jsonl` writer is touched. `deploy/INFRA_MANIFEST.ini` gains the helper (class `derived`).
2. **Two lines** of the self-test of the old `src/two_site_results_check_v0_7.py` name their line ending. Nothing
   else of the old system's code is changed.
3. **New:** `deploy/file_form.py` (the standard's one rule and the search for writes that name no line ending) and
   the tests `tests/test_file_form.py` and `tests/test_research_file_form.py`.
4. **`.gitattributes`** becomes the three lines of the standard v0.2; **`.gitignore`** gains the two readiness markers.
5. **The conversion program** changes line endings only in the other listed files and in DEV's `ENVIRONMENT.ini`,
   and removes DEV's research results and status files on a second typed word.
6. **The stage-and-refresh program** stages the listed files exactly as on disk and puts every other tracked
   file's working copy back to Git's own bytes.

## What Claude asks you to check

1. The two programs: that each prints first and waits for its word; that the conversion program changes line
   endings only, refuses a third SHA-256, keeps the results masters and ledgers untouched, and on a second run
   checks the owner's copy against the first run's recorded hashes (your watchpoint of EX_305); that the
   stage-and-refresh program refuses any file that differs from Git's bytes in more than line endings, never
   touches `GAIS\`, and commits and pushes nothing.
2. The engine's changed writers and their tests, and that no forecast, score or list line can change.
3. The sheet: its order (the owner's copy first; the push last, after the suite, the fill and the comparison
   with the old system's records), its expected lines, and its STOP rules.
4. **The readings** of `NOTES_FOR_THE_PACKAGE.md`, and with reading 1 the assumption your FFS2-C01 named: that
   the tests' own writes go to disposable fixtures. What Claude has on that is in `trial/REHEARSAL_OF_THE_SHEET.txt`.
5. Coding practices v0.1: Claude's own statement is "coding practices met", with these exceptions: the three
   tools of the build step 2 package are delivered unchanged (LF, as reviewed in EX_294), and the two
   `plant_faults_*` scripts and the builders are workspace tools.

## What it does not claim

Windows; the owner's Git for Windows; his real tree beyond the look-only run; a whole fill on his PC. Those are
the runner's rehearsal and the day.
