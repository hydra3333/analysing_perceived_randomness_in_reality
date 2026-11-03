# Recheck of design v0.1r3 DRAFT after the cold read (P1-P24)

Reader: the same helper as `cold_read_v0_1r3.md`. Input: the revised `..._v0_1r3_DRAFT.md` (752 lines, read in full; 0 non-ASCII bytes; no personal names). The previous draft is `..._DRAFT_before_cold_read.md`. The newly cited code lines were checked at `3a9f6ac` (code files only):
- `results_master_v0_1.py` line 54 `TOOL_VERSION = "0.1"`, 278 `def append_ledger`, 288 `os.fsync(fh.fileno())`, 540 `class BrowserFetcher:`, 567 `self.driver.get(url)`;
- `Run_Experiment.bat` line 41 `"%PY%" -u %*`;
- `Run_Results_Updater.bat` line 13 `set "TOOL=%ROOT%src\results_master_v0_1.py"`;
- `tests/test_wf1b_static.py` lines 40, 52-53 and 59.

All are correct. Draft line numbers below are physical lines of the revised file.

## 1. P1-P24

| P | Status | New text (quoted) | Still wrong |
|---|---|---|---|
| P1 BLOCKER partial sets | PARTIAL | Terms Ticket: "never a second one for a pair that has a DONE ticket in **any** attempts ledger of the game"; 3.4(b): "no DONE ticket in **any** attempts ledger of the game (fixed root, every session's ledger read)"; 6.3: "naming for each variant its one ticketed DONE record with that record's own session binding (a line may name records of several sessions; it lists their session ids)"; 6.3 next-draw cases: "**M has a `SET_STARTED` ticket (any session) and no freeze line** ... the set is completed, whatever the clock says now" | The core fix is right. Four places still assume a single session per line (N1, N2), and three still describe a `NONE` exit that can no longer happen (N3). |
| P2 BLOCKER preflight tool absent | APPLIED | 6.1: "for the MHUP-A install itself it is run from the package staging folder after PRE has verified its SHA-256 against the package manifest"; J step 2 the same; L-I1 "runs from the package staging folder in the MHUP-A rehearsal" | none |
| P3 BLOCKER byte-code | APPLIED | 4.1: "this needs `Run_Experiment.bat` (today line 41: `"%PY%" -u %*`, no `-B`) to gain both, so `Run_Experiment.bat` is an MHUP-A member"; "a `*.pyc` or `*.pyo` file **outside** a `__pycache__/` folder ... is an ordinary closure file and, under `src/`, a refusal"; the planted `json.pyc` test | `Run_Experiment.bat` is also the coordinator's wrapper (coordinator line 35) and the subject of `tests/windows_architecture_poc_suite.py` (line 20) and `tests/p0_static_checks.py` (line 10). Changing it touches the ratified POC/coordinator path, and the design does not say whether those Windows tests are rerun (N12). Section 8's MHUP-A list does not name `Run_Experiment.bat` (it appears only in 4.1, J step 6 and K). "A fresh, empty scratch folder": its location and clean-up are unstated. |
| P4 updater redirect and identity | APPLIED | 7 A6: "after the page loads and before any parse, lock or write, it refuses unless the browser's final URL (`driver.current_url`) has scheme `https` and host exactly `www.lotterywest.wa.gov.au`"; 7: "The permitted difference ... `TOOL_VERSION` (line 54 ...), the module docstring and the file name ... a comparison of the two files' syntax trees"; "line 13 (`set "TOOL=..."`)" | Appendix K, R2-C03 row: "the trusted origin is exactly `https://www.lotterywest.wa.gov.au`, no redirect, no fallback". "No redirect" contradicts 7, where the browser follows a redirect and only the final host is checked. Fix: "final host checked, no fallback". |
| P5 stale open tickets | PARTIAL | 3.4: "it would have to copy the run id of a live open ticket, and a resume marks every open ticket of a run that never completed `FAILED_TO_START`"; 5.2 "the run id is never reused"; 6.3 "first it marks `FAILED_TO_START` every open ticket for N in any session's ledger whose run folder does not prove a completed run" | (a) Neither the weekly half nor 3.4 says what happens to an open ticket whose run folder *does* prove a completed run, i.e. a crash after publication but before the DONE ticket. 6.3 neither marks it DONE nor FAILED, so the variant has no DONE ticket and is run again: a second published record for the pair, the first unnamed. The Mode H driver relies on "as today" resume. Fix: "...and writes the DONE ticket for every open ticket whose run folder proves a completed run". (b) "a live open ticket" understates: a crashed run's ticket stays open until the next resume. Fix: "an open ticket (of a live run, or of a crashed run until the next resume marks it)". |
| P6 gate freeze-line check | APPLIED | 3.4(b): "the game's forecast ledger must hold **no freeze line for the target**"; Appendix E row 18 and Appendix I updated | none |
| P7 diagnostic before seal | APPLIED | 3.4(b): "for any target at or above `holdout_first` only with the opening record and the game's `MODE_H_SEALED` marker" | none |
| P8 recovery paths | PARTIAL | 4.1: "the one reviewed path forward is the **study version advance** ... `STUDY_VERSION_ADVANCE_<GAME>_V1.json` ... every Mode H check ... and the updater's refusal (1) read that record ... Abandoning the batch and re-planning is **not** provided" | Appendix H line 641 still says "the owner then chooses a study version advance or a re-plan (4.1)". Appendix K's new-names list omits the `advance` command of `Method_Mode_H.py` and writes the record without `_V1`. |
| P9 baseline date | APPLIED | 4.3: "**The baseline is the one exception** ... validated against register v0.23 lines 1183, 1189 and 1215"; "read from the PC clock when the record is written (clock-dependent ...)" | none |
| P10 cross-references | APPLIED | 4.3 "(Appendix J step 13)"; B.2 C05 "steps 9, 11, 13, 14"; 3.2 `results_master_v0_2.py`; 6.1 "lines 34-38 and 40-53", "line 59", "the listed standard modules, numpy and `evaluation` itself; the text ban on `subprocess` and `os.kill` at lines 52-53" | Appendix D was not extended for the new citations (see N9). |
| P11 invariant | APPLIED | 6.4: "exactly one for every variant of the open line's line roster ... and none for a session-roster variant absent from that line" | none |
| P12 WAIT/NONE | APPLIED | 6.3: "**Otherwise** (no set started and fewer than sixty minutes remain, or the deadline has passed and M's result is not yet accepted): `NONE`"; `WAIT` gone from 6.1, 6.3, F, K (checked by search) | Terms: "Exit words ... each a persisted state, not a recomputation". `NONE` and `STALE` are computed from the clock and the ledger at that moment, not persisted. Fix: drop "each a persisted state". |
| P13 lock cross-checks | APPLIED | 6.1: "(new or `--resume`) while the updater's lock ... exists"; "`--resume` and every `next` also refuse if the closure or environment digest differs"; lock path `results/real/weekly/<GAME>/ACTIVE_SESSION.lock`; J step 2 "no `ACTIVE_SESSION.lock` for either game and no updater lock" | A small time-of-check gap remains (N10). The session record lists "the environment digest" twice (6.1: "the environment digest, the developed record's digest, the closure and environment digests"). |
| P14 resume token | APPLIED | 6.1: "`open-session --resume` requires the newest token for the lock's session, unused, with a check time within five minutes (PC clock, stated as clock-dependent)"; "With `--game G` and that game's lock present, `CLEAN` also writes ... a resume token"; "it never acts on a process and writes only its own value-free records" | Appendix K still says "`process_check.py` is named as a read-only process tool"; 7 A7 still says "the same read-only psutil check". This is minor wording. |
| P15 process identity | APPLIED, but over-corrected | 6.1: "lists ... every process other than itself and its own parent chain ... that meets any of: its executable is the venv's `Scripts\python.exe` redirector or the base interpreter named in `pyvenv.cfg`; its current directory is under the project root; its command line, or any ancestor's, names the project root ... a process whose details cannot be read (access denied) is a refusal, not `CLEAN`" | A new BLOCKER: as written the check will in practice never print `CLEAN` on Windows (N13). 7 A7's `clear-updater-lock` still uses the old rule ("a Python process whose command line names the updater"). |
| P16 barrier overstatement and STOP paths | APPLIED | J: "every dispatch-gated run refuses (P)"; "the updater, the WF-1B report tool and the coordinator's POC path are not dispatch-gated and are forbidden by the checklist until step 12"; step 5 restore "deletion of the package's added paths"; steps 10, 11, 13, 14 STOP cells give the forward path | Step 11's cell "a further small package commit or a restore" leaves "restore" undefined after a commit (a revert commit? a reset is forbidden to the runner). Minor. |
| P17 orchestrator pipe, third child | PARTIAL | 6.1: "`subprocess.Popen(..., stdout=PIPE, stderr=STDOUT, ...)`, reads the child's output line by line to end of file, echoing it ... then calls `wait()`"; "the process tool directly with the venv's Python and `-I` (its third and only other child)"; F step 2 uses `.venv\Scripts\python.exe` | Appendix K still says "the orchestrator is named as a sequencer of the two launchers"; it should name the third child. |
| P18 witness evidence, name | PARTIAL | 6.5: "`--verified-by <role>`, where `<role>` is `project-owner` or `reviewer` (never a name ...)"; "The tool checks ... that the evidence text is non-empty and contains the `WITNESS_RECORDED` line's reference ...; that the referenced commit or message carries the freeze line's digest is the **verifier's human check** ... (`digest_binding: human-checked`)"; public-repository and delay limits stated | Appendix G's diagram still says "a named person checks the reference" (line 614). Fix: "the verifier (a role)". |
| P19 `.pyc` consistency | APPLIED | 4.1 and H: "pip leaves `RECORD` itself and compiled `.pyc` entries unhashed"; "`__pycache__/` folders under `site-packages/` and the base `Lib/` are excluded from the digests and from the orphan check" | none |
| P20 report-then-seal | APPLIED | 5.2: "if the attempt's report does not exist it writes the report from the accepted lines, and if it already exists it verifies the report's digest against the accepted lines and writes nothing new; then it writes the seal. The report carries the attempt id and no wall-clock field"; L-H3 both cases | none |
| P21 torn JSONL line | PARTIAL | 6.5: "a reader that finds a final line without its newline ... ignores it and reports it, and the next writer completes the ledger by appending the same event again" | Appending after a final line that has no newline joins the new event onto the fragment, producing one corrupt middle line. Readers ignore only a *final* unterminated line, so the chain and grammar checks then refuse for ever (N8). |
| P22 retirement | APPLIED | 4.3: "**Retired:** a variant is retired when its registry chain entry is superseded ... or marked retired by an installed package; the session roster is computed at `open-session` ... a retirement takes effect at the next `open-session`"; Terms Roster | none |
| P23 LATE_PRE_DRAW wording | APPLIED | 6.4 and I: "whether it was frozen before the draw itself is not established, only before the result was accepted" | none |
| P24 overclaims | APPLIED | Section 1 "(addressed in ...)"; I "Every record falls in exactly one of the tier rows above (the first seven rows ...)"; I unreachable row noted; Terms lifecycle "after the one permitted first update"; section 2 "deleted last of the install's files"; Appendix C rewritten | See P12 for the new "persisted state" overclaim in Terms. |

## 2. New contradictions and defects introduced by the fixes

**N1 - CORRECTION - two definitions of the line roster.**
- 6.3 "Closed" (line 251): "The line's roster is the roster of the session that froze it, fixed for ever".
- Terms Roster and 6.3 "The loop": "the writing session's roster plus every variant with an earlier session's ticketed DONE record for that target".

Fix: in 6.3 "Closed", replace that sentence with the Terms definition.

**N2 - CORRECTION - multi-session lines are verified and recorded as if single-session.** These texts still assume one session per line:
- 6.3 "Across weeks": "S1's session record exists and has the digest the line names; every record the line names has a DONE ticket in S1's attempts ledger".
- Appendix F score step: "the line's session record + digest".
- Appendix E row 22: "if S1's session record and digest verify".
- 6.5 freeze-line content: "the session id and the session record's digest".

A line written under the new rule names records from several sessions, so a scorer implemented from this text would refuse every line that completes another session's set.

Fix: the line holds, per named record, its session id and that session record's digest, plus the writing session's id. The scorer verifies each named record against its own session record and attempts ledger. Update 6.3, 6.5, E and F accordingly.

**N3 - CORRECTION - a `NONE` exit can no longer leave a partial set, but three places still say it can.** Under the new 6.3 branch, a set with a `SET_STARTED` ticket is always completed ("whatever the clock says now"), and `NONE` arises only when no set started. So `NONE` never leaves a partial set. Yet:
- 6.3 "The loop": "an earlier session that ended `STALE` or `NONE` or whose lock was cleared";
- Appendix F property (v): "left without a line by `STALE`, `NONE` or a cleared lock";
- Appendix L L-W3b: "interrupted and left without a line by `NONE` (resumed with less than an hour left)".

L-W3b describes a path the rules make impossible, so the test cannot be built as written. Fix: drop `NONE` from those three places. For L-W3b, test instead that a resume with less than an hour left completes the set under `SET_STARTED` and exits `FROZE_NEXT M`.

**N4 - WORDING - stale "re-plan" in Appendix H** (line 641): see P8. Fix: "the owner may apply a study version advance (4.1); re-planning is not provided".

**N5 - WORDING - Appendix K residues.**
- "no redirect" (P4).
- "sequencer of the two launchers" (P17).
- "read-only process tool" (P14).
- New names: add `Method_Mode_H.py advance` and the `_V1` suffix (P8).

**N6 - WORDING - Appendix G** still has "a named person checks the reference" (P18).

**N7 - WORDING - Appendix E residues.**
- The definition of "Ticketed" still says "the pair has no DONE ticket" in the named ledger only; make it "in any attempts ledger of the game".
- Row 25 (`open-session` while a lock exists) omits the updater-lock and digest refusals.

**N8 - CORRECTION - torn-line completion corrupts the ledger** (P21). Fix: "the next writer first truncates the file to the end of its last complete line (the fragment is copied, value-free, into a side file as evidence) and then appends the event". Alternatively, "first appends a newline and readers skip one unparseable line immediately preceded by a crash report". Pick one and test it.

**N9 - CORRECTION - Appendix D is no longer complete.** New citations have no anchor rows:
- `results_master_v0_1.py` 54, 278-288, 540, 567;
- `Run_Experiment.bat` 41;
- `Run_Results_Updater.bat` 13;
- `tests/test_wf1b_static.py` 40-53, 52-53, 59.

The header still says "seven anchors added", and B.1 C07 claims every citation is anchored. All of these lines are correct at `3a9f6ac` (verified above). Fix: add the rows and update the count.

**N10 - WORDING - a small time-of-check gap between the updater and `open-session`.** Appendix I, master-grows row: "possible only if the updater was running when the session opened, which the updater-lock check refuses". But the updater makes its refusal checks "before any fetch, any lock or any ledger write" (4.1), so the order "updater checks for a session lock -> session checks for the updater lock and takes its own -> updater takes its lock and appends" is still possible. Fix: the updater re-checks the session lock after taking its own lock, or Appendix I says "or in the instant between the updater's check and its lock".

**N11 - WORDING - a later session that completes a set uses its own roster.** By the Terms definition (writing session's roster plus earlier DONE variants), a variant released between S1's `SET_STARTED` and S2's completion joins M's line, possibly as `PROSPECTIVE` if frozen before the deadline, although the hour rule was judged for S1's cohort. This is consistent with "first target frozen after its release", but it should be said: either "a completing session adds its newcomers to the set" or "a completing session runs only variants of the original `SET_STARTED` session's roster". The second is simpler and keeps the hour judgement meaningful.

**N12 - CORRECTION - changing `Run_Experiment.bat` reaches beyond MHUP-1.** It is the coordinator's `WRAPPER` (coordinator line 35) and is exercised by `tests/windows_architecture_poc_suite.py` (line 20, the Windows lifecycle POC) and `tests/p0_static_checks.py` (line 10, CRLF). Fix:
- state that the change is limited to adding `-B` and the `PYTHONPYCACHEPREFIX` line;
- state that `p0_static_checks.py` still passes;
- state that the Windows POC suite must be rerun under the owner's separate approval (the rulebook forbids Windows lifecycle tests without it), or that it is accepted unrun with a stated reason;
- name `Run_Experiment.bat` in section 8's MHUP-A list and in Appendix L's "existing tests" paragraph if any expectation changes.

**N13 - BLOCKER - the process rule of 6.1 will not print `CLEAN` in practice.** As written, the selection runs over *every* process, not Python processes only, and three criteria make it fail:
- **Current directory.** Any console, editor, git process or the Claude Code runner whose current directory is under the project root matches. The rulebook describes Claude Code working with this repository open as its workspace, so its node process would be listed.
- **Unreadable details.** To test the current-directory and ancestor criteria, every process's details must be read. Without elevation, psutil on Windows raises access-denied for the current directory of many system and service processes, and "a process whose details cannot be read (access denied) is a refusal".
- **Base interpreter.** Any unrelated Python started from the same base installation also matches.

Together these make the install preflight (J steps 2 and 4), the session resume and `clear-session-lock` fail closed every time, so B05's recovery path is unusable.

Fix: first select only processes whose executable name is `python.exe` or `pythonw.exe` (the name is readable without elevation). Apply the venv-redirector, base-interpreter, current-directory and ancestor tests to those only, and treat access-denied as a refusal only for those candidates. Treat a non-Python process with the root as its current directory as harmless and not listed. State that an unrelated Python from the same base installation is a known false positive, which the owner closes. Add a T016 check that the preflight prints `CLEAN` on the owner's ordinary desktop with Claude Code and a console open at the root. Also align 7 A7's `clear-updater-lock` with the same rule.

## 3. The ten scenarios under the revised rules

1. **Rerun after `FROZE_NEXT M`, before M's result.** A new session opens with the same pin; there is no unclosed accepted N; M has a line, so `OPEN M` and nothing is made (6.3, F). One answer.
2. **S1 freezes N at v; the updater admits v+1; S2 scores N.** 6.3 "Across weeks" and F: the score binds to S1's line, training pin v, outcome pin v+1, provenance S2. One answer for a single-session line. For a line naming several sessions, the verification text is singular and fails (N2).
3. **Crash after the freeze line, before scoring; rerun.** The lock remains. The orchestrator runs `check-no-runs --game G`; on `CLEAN` it writes a token; `--resume` (token newest, unused, no older than five minutes; no updater lock; same digest); `next` returns `FROZE N`; `score` runs. One answer, but N13 means `CLEAN` will not be reached on a normal desktop.
4. **Crash during the runs for N; rerun.** The session resumes. Open tickets whose run never completed are marked `FAILED_TO_START`; the missing line-roster variants run; then the line. For M with a `SET_STARTED` ticket, the set is completed whatever the clock says (6.3, 6.4, I). That is one answer, with two exceptions:
   - The case of an open ticket whose run *did* complete is unspecified, which allows a second record for the pair (P5(a)).
   - 6.3, F(v) and L-W3b still describe a `NONE` partial set (N3).
5. **A new variant released after three post-holdout targets were scored.** Those lines stay closed; it joins at the next session (6.3, E, F(vii), L-R1). One answer, but 6.3 "Closed" disagrees with Terms on what a line roster is (N1), and N11 applies if it is released while a `SET_STARTED` set is incomplete.
6. **A variant retired while it has an open forecast.** It stays in that line and is scored; the retirement takes effect at the next `open-session`, so it gets no later forecast (4.3, 6.3, I). One answer.
7. **The master grows during a session.** Ordinarily prevented by the two lock checks, except for the small gap of N10 or a hand edit. If it happens: `STALE`; every further publication refuses; the next session completes N from the game-wide DONE tickets, naming both sessions' records (6.3, I). One answer, subject to N2.
8. **`clear-session-lock` on an incomplete set for N, then a new session.** Appendix F: completed from the game-wide DONE tickets, running only the missing variants, with the old records named under their own binding. 6.3 and B.2 B01(c) agree. One answer, subject to N1 and N2.
9. **The Mode H scorer crashes after `SCORE_COMPLETE`, before the seal.** No outcome is read. If the report exists, its digest is verified and only the seal is written; otherwise the report, then the seal (5.2, L-H3). One answer.
10. **A hand-typed run with a valid Mode H binding while the batch is in progress.** Refused for lack of a ticket (3.4, E, L-G1). It is admitted only if it copies the run id of a live open ticket, or of a crashed run's ticket before the next resume (P5(b)), which the text should state.

## 4. EX_127 coverage

- **B01: PARTIAL (narrow).** All four parts (a)-(d) now have concrete rules: `OPEN M`, cross-session scoring, same-session resume with fresh tokens, game-wide DONE tickets, the persisted `SET_STARTED`, and the lock checks. Still needed: multi-session line verification (N2), removal of the stale `NONE` path (N3), and a usable `CLEAN` for the resume (N13).
- **B02: RESOLVED** in substance (the line roster versus the session roster, the closed-under-line-roster rule, the defined retirement, the corrected invariant), subject to the one-sentence fix in N1.
- **B03: RESOLVED.** Gate with ticket, no-DONE check and lifecycle markers; marker order; same-attempt resume; idempotent seal. A narrow remainder: the completed-run open ticket (P5(a)) and the "live" wording (P5(b)).
- **B04: RESOLVED.** The updater v0.2 refusals; the defined study version advance; the `RECORD` and interpreter freeze; `-B` and `PYTHONPYCACHEPREFIX` in `Run_Experiment.bat`; sourceless `.pyc` refused. Stale wording in H (N4); the effect on the coordinator and POC suite should be stated (N12).
- **B05: PARTIAL.** The order, the gate files first, barriers kept until COMMITTED, forward STOP paths, lock checks in the preflight and the package-folder preflight are all applied. But the process rule as written cannot print `CLEAN` in practice (N13), so the preflight and the lock recovery would always refuse.
- **C01: RESOLVED.** Tickets, `FAILED_TO_START`, the diagnostic route and the stated trust boundary; wording P5(b).
- **C02: RESOLVED.**
- **C03: RESOLVED.** The final-host check on the browser's URL with no fallback, and its limits stated; Appendix K's "no redirect" wording (N5).
- **C04: RESOLVED.** Evidence must contain the reference; the digest binding is recorded as human-checked; a role, not a name; the limits stated; Appendix G's diagram wording (N6).
- **C05: RESOLVED.** Install record versus release record; the baseline exception stated; forward STOP paths; the release date taken at the step that writes the record.
- **O01: RESOLVED.**
- **O02: RESOLVED.**
