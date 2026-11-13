# MHUP-A live install: verification from GitHub (13 November 2026)

By the Claude web chat (Opus 5.5), after the project owner's live install (gate F, 13 November 2026, about 17:55-18:50
Adelaide) and push `5211a42..effc179`. Read-only checks on a fresh clone of `main`. US-ASCII, CRLF.

## 1. The install itself: VERIFIED

- Commits: `2860e86` (package commit; parent `5211a42`) and `effc179` (release commit; parent `2860e86`).
- The owner's window showed every Appendix J step 0-19 with its expected line: PRE PASS; `CLEAN` at steps 2, 5, 7, 11
  and 14; U, then E and P; COPY PASS gate 10 and rest 61 + 1 deletion; POST PASS; step 10 SUITE PASS (571/571, 4 symlink
  skips, the live tree barred throughout, the temporary copy removed); INSTALL RECORD PASS; STAGED PASS (73 paths);
  COMMITTED PASS; E and P removed; RELEASE RECORD PASS; STAGED PASS (1 path); RELEASED PASS twice; U released; pushed.
- Every one of the 71 overlay files equals its blob at `effc179` (the three `.bat` files after Git's `eol=crlf`
  normalisation; their checked-out bytes equal the overlay's); `src/results_master_v0_1.py` is absent; no barrier
  (U, E, P) is in the tree.
- The records: `INSTALL_MHUP_A_V1.json` names the manifest `8ad51e76...24b5`, local date 2026-11-13;
  `RELEASE_MHUP_A_V1.json`, local date 2026-11-13 (E_1 revision 3's release date for MH-1). `install_records.py
  validate`: `RECORDS PASS: 1 install record(s), 2 release record(s), 80 released unretired entries`.
- `i/lf w/lf attr/-text` on the six byte-checked files; the clone is clean.

## 2. Found after the install: 8 tests assume the PRE-install records (not a fault of the install)

The whole suite run on the installed `main` (no barriers; `SUITE_ON_INSTALLED_MAIN_effc179_py315.txt`): 571 ran;
563 passed; 8 failed, in two modules:
- `tests.test_mhupa_install_records`: 7. The test copies the repository's real `install_records/` folder into its
  temporary root and asserts what was true before the install: only the baseline record, 78 released entries, no record
  naming E_1 revision 3. After the install the folder also holds `INSTALL_MHUP_A_V1.json` and `RELEASE_MHUP_A_V1.json`
  (80 entries), so those assertions no longer hold.
- `tests.test_mhupa_mode_h`, `test_the_cohort_must_be_exactly_the_released_set`: 1. It expects Mode H to refuse because
  E_1 revision 3's release record is absent; after the install it is present (as it should be), so no refusal.

The same 571 tests passed at step 10 because step 10 runs before the records exist. Production behaviour is unaffected
(the records validate; the released set is 40 per game). But the suite on `main` now fails, so the next package's step
10 would STOP on these 8 until they are fixed.

My miss: the rehearsals ran the suite only at step 10, never on the tree after step 18. The fix is test-only: build the
tests' records fixture from the baseline record alone (and, in the Mode H test, without the MHUP_A records), so they no
longer depend on the repository's install state. It needs the reviewed package route; nothing is changed now.
