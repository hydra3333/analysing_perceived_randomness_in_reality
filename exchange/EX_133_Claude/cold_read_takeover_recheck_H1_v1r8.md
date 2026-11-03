# Takeover recheck - DOC-11 rehearsal copy 2 (c4ee4da)

Same limits as before: read-only, no data folders, no web, no outcomes, no suite. Checks run on the new copy:
- DOC-11 manifest: 20 of 20 match.
- H-1 hashes: 84 distinct, the same 75 file hashes all match. The coordinator anchor is now labelled as the
  fixture's hash.
- `src/` and `tests/` are unchanged since PERF-1.
- H-1 is ASCII.

## The 20 gaps

| # | Verdict | New text (quoted) / note |
|---|---|---|
| 1 | FIXED | H-1 0.3: "if this file's or register v0.24's status line still reads CANDIDATE, stop and ask the owner which handover is in force"; blurb step 1: "If H-1's or the register's status line still reads CANDIDATE, stop and ask the owner." |
| 2 | FIXED (not exercised by me) | `build_doc11.py`: H-1 is built first, then `h1sha = sha(...)`, `blsha = ...` are passed to `make_register_v24.py`. The version line is now "(the Claude handover package reviewed in ... EX_133 and EX_134)", so `@@EX@@` is gone. The usage line says "[DATE text for @@DATE@@, RATIFIED only]". `e2e_doc11.sh` tests an already-built package only, so the RATIFIED build is still untested end to end. |
| 3 | FIXED | H-1 10 item 2: "**The code is paused** ... until the staged takeover is verified and the owner explicitly authorises normal work (section 0, item 4); DOC-11's install alone does not lift the pause." 12.8 matches. |
| 4 | FIXED | Roadmap header "Last updated: 3 November 2026 (evening): the MHUP-1 design ratified (MHUP-R); DOC-11 ... (HO-2); the code paused." 10c: "then, ONLY after that check and your explicit go-ahead, MHUP-A code". The stale paths are corrected. |
| 5 | FIXED | R-015 ("The owner's choices still to come for MHUP-1") and R-016 (HO-2) are added. R-007, R-008 and R-010 now say "folded into MHUP-A". R-013 says "OPEN until DOC-11 is installed, then DONE". The standing reminders point to v0_8 and v0_2r1 and say "Recorded as MC-1". |
| 6 | FIXED | H-1 0.1: "except the two master hashes in section 7.5 (never open `source_data/`) and the computed E_1 digests in section 7.3". 7.2: "`2e23d550...` is the SHA-256 of the v0.6 fixture file, not of the current coordinator". Appendix A is labelled the same way. The blurb carries the same exclusions. |
| 7 | PARTLY | H-1 0.4: "no test suite run (section 12.9's suite and workspace steps wait for the owner's authorisation)". That settles the takeover. But 7.4 still says E2R-T12 "needs the owner's approval for each run context", and nothing says whether "authorises normal work" covers T12 in Claude's cloud workspace. See also new problem N1. |
| 8 | FIXED | H-1 0.4: "the owner relays the reviewer's questions on their own (a paste, or an EX file holding only the questions); the reviewer's assessment and suggested answers stay with the owner until you have sent your answers ... Once the owner authorises normal work, you record every takeover exchange in `exchange/` under the next free EX numbers". The blurb step 4 matches. |
| 9 | FIXED | H-1 12.1: "(EX_132 offered EX_133 for an optional reply; if that number was used, the request took the next free one)". |
| 10 | FIXED | H-1 0.4: "no commit or push, even in `exchange/` ... The outgoing Claude chat stops committing once you start." Blurb: "(Claude pushes only its own `exchange/` and `CLAUDE_CODE_WORKING_FOLDER_TREE/` commits, and none during the takeover)". |
| 11 | FIXED | H-1 8.2: "A speculative candidate ... is fine (but never during a takeover: section 0, item 4)". H-1 0.4 and blurb step 3: "no draft or speculative code, task file or package in your workspace". |
| 12 | FIXED | H-1 10 item 2: "The planning dates of ST-5 have not been moved by the owner; HO-2 adds a review round and a takeover check, and FB-1 applies". The roadmap matches. |
| 13 | FIXED | Register out-of-date statements: "The direction document v0.2r1 ... where it differs from the design (the design prevails)", naming sections 4, 5 step 4, 7 and 11. The H-1 section 4 row: "prevail where it is looser or differs (register v0.24 lists four places ...)". |
| 14 | FIXED | Register: "its section 8 names only `Run_Evaluation.bat` and `Method_Mode_H.py` ... this register's ratification and its future action 1 (four tools) prevail". |
| 15 | FIXED | Blurb "Still open" adds Q7 "to be decided before the first results update, Approval 2" and "the owner's confirmation of a backup". The reading list adds "the rest of H-1 section 0's list (H-3 and the review-disposition procedure)". |
| 16 | PARTLY | `doc11/` now holds `build_doc11.py` and `e2e_doc11.sh`, byte-identical to the `review/` copies. The README has a `doc11/` section, which notes "REPO is hard-coded at the top". The README's 3.15 venv list ("numpy scipy psutil") still differs from H-1 12.3's seven packages. |
| 17 | FIXED | H-1 section 4 design row: "byte-identical to EX_132's member, so its own header, section 1 and section 8 table still read as before ratification; register v0.24 records the ratification". The register adds the same. |
| 18 | FIXED | Appendix A: "its "DRAFT" title and footer are historical, the register's status prevails". |
| 19 | PARTLY | Fixed: "Appendix J's steps 0 to 19 (two commits)"; DOC-11's verifier is now named in 1.6; `H1_blurb_v1r7_to_v1r8.diff` is added. Not fixed: `METHOD_TEMPLATE/README.md`'s "DRAFT 3" Status line (pre-existing; NIT). |
| 20 | FIXED | The routes in items 3, 4, 11 and 12 are all closed. |

## New problems introduced by the fixes

- **N1 (MINOR): the first-hour checklist now contradicts itself in its order.**
  - H-1 0 item 7 is unchanged: "Work through section 12.9's first-hour checklist before your first reply (it reads
    and checks; it builds and runs nothing on the owner's machine)".
  - But 12.9 step 2 now says "**After the owner has authorised normal work (section 0, item 4), not before:** ...
    set up a workspace".
  - Step 3 (the whole suite) depends on step 2's workspace but is not labelled the same way.
  - Step 5 ("Confirm the takeover") still comes after the suite.
  - A literal reader cannot do 12.9 "before your first reply".
  - Fix:
    - item 7: "Work through 12.9 steps 1, 4 and 5 before your first reply; steps 2 and 3 only after the owner
      authorises normal work";
    - prefix step 3 with "After step 2:".

- **N2 (NIT): the reason given for DOC-11's verifier is wrong.**
  - H-1 1.6 now reads "**DOC-10 (the snapshot) and DOC-11 have one each** (...), because it also replaces files
    outside `doc/` and `review/` (`README.md`, `.gitattributes`, the Claude Code rulebook)".
  - That reason is DOC-10's only. DOC-11 adds only files under `doc/` and `review/`.
  - Fix: "...have one each (DOC-10 because it also replaces files outside `doc/` and `review/`; DOC-11 because the
    owner wanted a checked install of the handover package)", or whatever DOC-11's actual reason is.

No other new conflicts found. Specifically, the CANDIDATE stop rule, the blind relay and the no-commit rule agree
between H-1 0.3 and 0.4, the blurb, the roadmap and R-016.

## Verdict

No: a new chat could no longer reasonably read its authority as starting MHUP-A. Every text it is told to read now
says MHUP-A waits for the verified takeover and the owner's explicit go-ahead. Only N1's order clash (when to set up
and run the suite) is left, and it touches no data, holdout or install gate.
