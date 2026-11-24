# FILE_FORM_Lock_Fix_v1: note for the reviewer

**From:** the Claude web chat. **Date:** 25 November 2026. **Standing:** a small follow-up package, as you asked when you
agreed to option 1 on the night of the conversion; not installed. **It authorises nothing.**

**What it corrects.** After the conversion one new test fails on Windows only:
`test_research_file_form.TheSmallFiles.test_a_lock_file_is_one_line_ending_crlf`
("holds 1 carriage return(s) that no line feed follows"). `src/research/job_lock.py` opens the lock file with
`os.open` without `O_BINARY`; on Windows the C runtime then writes a carriage return of its own before each line
feed, so with the conversion's CRLF line the file ends CR CR LF. Linux does no such thing, so the cloud passed.

**The change, whole** (`package/FILE_FORM_Lock_Fix_v1_DIFFERENCE.txt`): one line gains
`| getattr(os, 'O_BINARY', 0)`, as `src/research/reader.py` already does, with a two-line comment. Nothing else.

| Path under `exchange/CLAUDE_WEB_TOOLS/lock_fix/package/` | SHA-256 |
|---|---|
| `FILE_FORM_Lock_Fix_v1.zip` | `744efbd3ca1ea70162d6c1dcae060836e9326625299f9116b5ac2dbb19e20318` |
| `FILE_FORM_Lock_Fix_v1/repo_overlay/src/research/job_lock.py` (CRLF) | `efe8419e5927d87207fc39de0b97519c86b0b4a01f533b5751b6a6f54bc7853f` |
| `FILE_FORM_Lock_Fix_v1/INSTALL_SHEET.md` | `def09593cc80155b21c596589dcc1633631dc067e82ea00fa9ee5b94678ef712` |
| the file it replaces, as committed at `691f58e` | `fadb1785ff2703249b132bf555e4bf2a7311565a1914492dbfdb7585870ba6a7` |

**Checked in the cloud** (a converted tree with the corrected file): `test_research_file_form`, `test_research_job`,
`test_file_form` and `test_research_manifest`, all OK. This cannot show the Windows behaviour; the owner's run of
the three modules in the sheet's part 3 does (116 tests).

**No rebuild.** `job_lock.py` is class `derived` in the manifest. The engine writes the digest of that code into new
score and OV-1 lines (`research_job.py`) and compares it nowhere; a line already written keeps the digest it was
written with. The sheet runs no research job.

**The same slip in the one-off conversion program** (its own lock, `HeldLock`): its two lock files were made and
removed within the run of 24 November and held no result. That program is not used again, so it is not changed.

**Asked of you:** a focused look at the one-line difference and the sheet.
