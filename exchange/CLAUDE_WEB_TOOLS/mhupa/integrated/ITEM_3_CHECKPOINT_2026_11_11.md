# MHUP-A integrated package - item 3 checkpoint (11 November 2026)

By the Claude web chat (Fable 5.2 for item 3; Opus 5.5 for the N1 packaging before it), under the owner's decisions D01-D08 of
10 November 2026 (`exchange/HO2_2026_11_10/`). Not an EX message. US-ASCII, CRLF. Everything here is **PRELIMINARY, on a
DRAFT package**: nothing is frozen, reviewed, installed or run on real data. Base: `main` `c48ac3c`. Working date 2026-11-10.

## 1. Result in one paragraph

Item 3 is built and its own tests pass, **but the rehearsal found that Appendix J step 10 cannot pass as written (N5): with
barriers U, E and P in place, the reviewed suite fails in 21 of 45 modules.** This is a STOP for the end-to-end positive
path and needs a decision by the reviewer and the owner (section 3). Everything else in steps 0-18 passes on LF and CRLF
clones with step 10 omitted, and 88 negative checks behave as required.

## 2. What was built (all install-time tooling; no production code changed)

| Piece | What it does now |
|---|---|
| Verifier `released` phase | Two-commit proof: the release commit has exactly one parent; that parent passes every package-commit check; the release commit adds only the release record. The record: canonical, same bytes in Git and on disk, this package, exactly the manifest's entries, the committed install record's SHA-256, times in the order U taken, install record, release record. Record/repository agreement: each released entry is the newest registry entry of its variant, SUPPORTED; the baseline marks the earlier revision superseded; 40 released per game; no barrier or IN_DEVELOPMENT flag committed. |
| Barrier state in every phase | PRE: U, E, P absent. POST and COMMITTED: all three present. RELEASED: E and P absent, U still held. |
| Barrier order, enforced by the copy tool | No E or P without U; no file copied without U, E and P; the rest only after the gate files; E removed only if the verifier's COMMITTED phase passes at that moment; P only after E; P can be re-created for the STOP handling of steps 16 and 17. Files are written whole, then put in place in one step. |
| Verifier `staged` phase (new) | Before each commit: the index holds exactly that commit's paths. Replaces counting 73 lines by eye; the commit line runs only if it passes. |
| Instructions (DRAFT) | Lines chained with `&&` so nothing runs after a failure; a repeatable "names" block for a new window; step 18 releases U only if RELEASED passes at that moment; rerun forms; STOP texts matched to Appendix J's table. |
| Rehearsal tool `rehearse_mhupa.py` (S1, D07) | Stops at the first step that does not give its expected output; nothing runs after a STOP. Replaces `smoke_steps.sh` and `neg_smoke.sh` (removed; in history at `b9ef1bb`). |

Draft package identities (`evidence_2026_11_11/PRELIMINARY_BUILD_REPORT.txt` has all): manifest
`149fbe7af99d258b2c7d392b54a8512fc82a82fc1fa44f3601efac835a8925ad`; `VERIFY_MHUP_A.py` `d339726b...`; `MHUPA_COPY.py`
`57794721...`; 37 new, 34 modified, 1 deleted (71 overlay files; 72 changed paths; 73 staged with the install record).

## 3. Findings

**N5 - BLOCKER for Appendix J step 10 (found by rehearsal; root cause established).**
- Appendix J step 10 runs the suite with E and P present, on the premise "the barrier paths are module constants the harness
  patches, so the suite passes with P present".
- The reviewed code does not meet that premise. Only the new MHUP-A tests use a patched project root. The older accepted tests
  (REL-1, CODE-2, E_1, WF-1A/B and others) exercise the installed tree through the real gate, so P makes every dispatch
  refuse (`INSTALL_IN_PROGRESS`) and E makes E_1 "SUPPORTED but still flagged IN_DEVELOPMENT".
- Evidence: at step 10 of the full rehearsal, 560 of 570 ran and 21 modules failed, on LF/3.13 and CRLF/3.15
  (`N5_step10_suite_STOP_with_barriers_*.txt`). A byte copy of the same tree without the barrier files passes 570/570
  (`N5_suite_PASS_on_barrier_free_byte_copy_lf_py313.txt`). T022 could not see it: it ran with no barriers.
- Options:
  - **A (recommended): run step 10's suite on a barrier-free byte copy** of the just-installed files in a temporary folder;
    the live tree stays barred throughout. Cost: one mode in the package's suite runner (install-time only) and one sentence
    of Appendix J step 10 amended. No production code and no reviewed test changes.
  - B: make the whole suite pass under the barriers, as Appendix J words it. It means changing about 21 reviewed test modules
    or a global patching hook; large, fragile, and it weakens what those tests check.
  - C: remove E and P before the suite (as the E_1 revision 2 install did). It opens the gate before the code is tested and
    committed, against EX_125 C01 and EX_127 B05.
- Not decided and not implemented. Until it is, the instructions mark step 10 OPEN.

**N4 - CORRECTION (from the earlier checkpoint; not applied).** In a fresh `core.autocrlf=true` clone of the installed tree two
tests fail on line endings only (568/570). Proposed: `-text` for `src/package_tools/process_check.py` and
`tests/fixtures/results_master_v0_1_reference.py.txt`, as N1.

**Cold read by a fresh helper (Opus) of the instructions and tools against Appendix J.** 17 findings; the instruction and
tool ones are fixed in section 2. Left for the reviewer because they are in reviewed code or the design text:
- `process_check.py release-install-lock` has no preconditions; mitigated: step 18 is chained to RELEASED PASS.
- `install_records.py release-record` does not itself check that U is held; the verifier's RELEASED phase does.
- The install record's `post_pass_utc` is the time of step 12, not of POST PASS (design 4.3 wording).
- Three places print a traceback instead of a STOP line (a lock race, an unlink failure, a failed `git status`).
- A fix commit after step 13 or 17 (which Appendix J allows) needs a matching verifier from Claude at that time; the strict
  verifier accepts only the two-commit shape.
- Design 4.3 says the baseline has "40 entries"; the file has 40 per game (80).

**O1 - observation.** `check-no-runs` counts a Python process that exits while it is being read as a refusal. Fail-closed and
harmless (rerun the step), but it can surprise: it happened once here while another test run was finishing.

## 4. Evidence run (all PRELIMINARY; `evidence_2026_11_11/`)

| What | Result |
|---|---|
| Negatives, synthetic root, Python 3.13 (`PRELIMINARY_negatives_88_py313.txt`) | 88 checks, 0 failed: 58 STOPs, 17 required passes, 13 end-state checks |
| of which RELEASED refused, 13 ways | each STOPs. For 11 (extra file, wrong parent, merge, five forged records, non-canonical record, CRLF, untracked file) the step 17 handling is then applied: P re-created; end state P present, E absent, U held; step 18 not run; RELEASED cannot pass while P is back. The other two: U released early, U naming another package |
| of which barrier order, 13 ways (plus 2 required passes for the restore form) | each out-of-order action refuses |
| of which F1 (D03) | PRE passes on a descendant with only rulebook and settings commits; STOPs on a later change to a package path or under `src/` |
| Positive path steps 0-18, full clone, LF/3.13 and CRLF/3.15, **step 10 omitted** | REHEARSAL PASS on both; RELEASED PASS before U is released |
| N1 oracle with the final tools (`N1_records_eol_oracle_py315.txt`) | N1 ORACLE PASS (5 positive states, 1 negative) |
| Suites on the same bytes without barriers (10 November) | 570/570 on 3.13 and 3.15 |

Not run: any full positive path including step 10 (N5); anything on Windows; mutation chains; the final-candidate evidence.

## 5. F2: the T016 oracle matrix (for the focused RECHECK; nothing here is authorised)

Roots: **REAL** = the owner's repository and its `.venv`. **CLONE** = a non-pushing task clone, as cloned. **SYN** = such a
clone after a local commit removes `source_data/`, `results/` and `transitory_data/` from the index and the working tree,
with empty `source_data/` and `results/` folders (its Git history still holds the data objects; nothing reads them).
**STAGE** = the unzipped package in the task's scratch folder. CC = Claude Code.

| # | Oracle | Who | Root | Command (outline) | Data safety | PASS / STOP | Authority needed |
|---|---|---|---|---|---|---|---|
| 1 | Package identity | CC | STAGE | `cc_clone.py unzip` with the SHA-256 | none read | SHA matches / STOP | T016 go |
| 2 | The suite on the installed bytes | CC | CLONE | overlay by plan file, then the package suite runner | the accepted tests read the development masters through the project's reader (rule 2.5's allowance); CC opens nothing | SUITE PASS, at most 4 symlink skips / STOP | T016 go; E2R-T12 for this context |
| 3 | Appendix J steps 1-9 and 11-18 (step 0 as an identity check; 19 omitted) | CC | SYN, tools from STAGE | the instructions' lines; Git through `cc_clone.py git` with the pathspec files | no data present; the tools create and read only the lock and the barriers | each step's PASS line / STOP | T016 go; rulebook v0.5's allowance |
| 4 | STOP behaviour | CC | SYN | wrong byte at POST; release record with P present; RELEASED refused, then P re-created | as 3 | each STOPs; end state P present, U held | as 3 |
| 5 | N1 on real Windows Git | CC | SYN after both commits | `git check-attr`, `git ls-files --eol`, `install_records.py validate` | as 3 | `-text`, `w/lf`, RECORDS PASS / STOP | as 3 |
| 6 | **F2-C01:** the real Windows interpreter, DLLs, `Lib/` and venv RECORD inventory | CC | CLONE's installed `src`; reads REAL `.venv` and the base Python only | a small harness in STAGE calling `closure.environment_inventory(Environment.current())`; prints counts and the digest only | no data folder; nothing written; the venv is not changed | counts and digest / STOP naming the orphan or mismatch (a reviewed fix, never a hand deletion) | T016 go; the harness reviewed |
| 7 | **F2-C01:** orphan refusal on the real Windows file system | CC | scratch | the same harness with a scratch `site-packages` (one real distribution copied there plus one planted file) and the real interpreter trees | the real venv is not touched | must STOP naming the planted file | as 6 |
| 8 | **F2-C02 (a):** the preflight prints CLEAN on the ordinary desktop, Claude Code and a console open at the root | **owner** | REAL | `process_check.py check-no-runs --root REAL --install MANIFEST` from STAGE | reads the process table and `.venv\pyvenv.cfg`; tests whether lock files exist; opens no data file; writes nothing | `CLEAN` / REFUSED (send the output) | the owner's own separate approval |
| 9 | **F2-C02 (b):** a live `Run_Experiment.bat` child is listed | **owner** | REAL | console A: `Run_Experiment.bat POC_Coordinator_Probe.py --poc --case=sleep-timeout --sleep-seconds 120` (the existing synthetic engineering probe: it sleeps and ends by itself); console B: the line of 8 | no lottery data; the probe writes only its own folder under `transitory_data\poc_runs`; no coordinator; nothing terminated | REFUSED listing the child; after it ends, CLEAN / otherwise STOP | the owner's own separate approval (a synthetic launch, not a lifecycle or destructive test) |
| 10 | The byte-code folder is never created | CC | SYN | `transitory_data\no_pycache_ever` does not exist after 3 | existence test only | absent / STOP | as 3 |

8 and 9 are owner-run because option (i) confines the two tools to T016's clone and rules 2.5, 7 and 9 keep Claude Code
away from the real root and from launchers. If the owner does not approve 9, the oracle is reported unmet; a bare sleeping
Python is not offered as a substitute. If N5 option A is chosen, row 2 is how step 10 is rehearsed.

## 6. For the deferred KISS review (flagged only; nothing changed)

- The Mode H environment freeze re-hashes the interpreter tree and every installed package at each later step.
- Three overlapping release controls: registry status, the IN_DEVELOPMENT flag, and install/release records.
- Byte-canonical record checks on files Git manages (the source of N1 and N4).
- Three barriers with five install checks in one install.

## 7. Next (each needs its own decision)

1. **N5:** choose how step 10 runs (A recommended). Reviewer first.
2. **N4:** add the two `-text` lines (recommended).
3. **F2:** the reviewer's RECHECK of the matrix; the owner's view on rows 8 and 9.
4. Then, on Opus: rulebook v0.5 and the T016 task for their focused review (Route A).
Not authorised and not started: rulebook v0.5, T016, any settings edit, the freeze, any install.
