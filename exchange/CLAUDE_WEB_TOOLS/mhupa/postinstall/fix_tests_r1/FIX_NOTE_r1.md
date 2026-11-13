# MHUP-A post-install test fix (r1) - DRAFT for the reviewer's focused check

By the Claude web chat (Opus 5.5), 13 November 2026, after the owner's yes (19:11) to drafting the fix for the finding in
`../POSTINSTALL_VERIFICATION_2026_11_13.md`. Nothing is installed; `tests/` on `main` is unchanged. US-ASCII, CRLF.

## 1. The change (tests only; no production file, no closure file, no record, no registry entry)

Two files, `overlay/tests/` (full files) and `FIX_against_effc179.diff` (every changed line; 23 added, 7 removed):
- `tests/test_mhupa_install_records.py`: the temporary repository gets the **baseline record only** instead of a copy of
  the repository's whole `install_records/` folder, and the baseline test's pre-install assertions (the baseline alone;
  78 released entries) are made on that copy. One assertion added on the real repository that holds whatever has been
  installed: its records validate and include the baseline.
- `tests/mhupa_slice2_fixtures.py`: `copy_closure` copies `src/` without the repository's install records other than the
  baseline (a copytree ignore), so every Mode H test project starts at the pre-install state; the tests that need
  MHUP-A's records already write them with `write_e1r3_release`. Docstring updated to say so.
No test is added, removed or renamed (571 tests, 45 modules; the runner's counts unchanged).

SHA-256: `mhupa_slice2_fixtures.py` a0923a5ba576a0c48c72b05ca982b156ffd4510616dba92780c8993811e9c44e;
`test_mhupa_install_records.py` c82231a1e33e1ecc1d2bbda790baf3f80e1c7bfcdf3ec573befa992e2d432b47.

## 2. Evidence (Linux, Python 3.15; `evidence/`)

| State | Run | Result |
|---|---|---|
| installed `main` (MHUP-A records present), fix applied | the whole suite (`--repo` mode) | SUITE PASS, 571/571 (`suite_fixed_post.txt`) |
| the step-10 state (package files, no MHUP-A records), fix applied | `test_mhupa_install_records`; the whole `test_mhupa_mode_h` | 9/9 OK; 20/20 OK (`two_pre.txt`, `modeh_pre.txt`) |
| both states | the formerly failing Mode H test alone | OK (`one_r.txt`, `one_pre.txt`) |

Without the fix, installed `main`: 563/571 (`../SUITE_ON_INSTALLED_MAIN_effc179_py315.txt`). The full-suite and pre-state
runs used the r1 files before the `copy_closure` docstring line was corrected; after it, the install-records module and
the Mode H `ManifestAndOpening` class were rerun on the final bytes: 15/15 OK.

## 3. How to deliver it (a question for the reviewer and the owner)

The change touches only `tests/`, which is outside the frozen closure (design 4.1) and releases nothing, so the full
Appendix J route (barriers, install and release records, two commits) has nothing to protect here. Proposed, the lightest
route that keeps the evidence:
1. a read-only Windows suite run by Claude Code in a task clone with the two files overlaid (as T020-T022; a new task
   number, T023), the reviewer having checked this draft;
2. then one owner commit of the two files (the owner copies them from this folder, checks the two SHA-256 values above
   with certutil, `git add` the two paths by name, commits, pushes); Claude verifies from GitHub.
Alternative: the full Appendix J route as a package MHUP-A1 (heavier; nothing it adds applies to a tests-only change).

## 4. Process change (proposed; no new production mechanism)

Every future package rehearsal also runs the whole suite on the tree after step 18 (the installed state with its
records), not only at step 10. That is the step that would have caught this before the install.
