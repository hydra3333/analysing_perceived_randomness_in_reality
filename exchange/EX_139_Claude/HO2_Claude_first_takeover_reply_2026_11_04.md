# HO-2 Step 2 - the replacement Claude chat's first substantive takeover reply (4 November 2026, about 11:30 Adelaide)

Recorded for the exchange from the chat text the project owner relayed to the ChatGPT reviewer chat,
re-set as plain ASCII text with the lists run together; the substance and every figure are unchanged, and
the chat text is the original. Basis: main at 20a3f40 (EX_138); DOC-11 installed at 3d4fa3c. Nothing was run, built or
committed to write it.

## 0. What I checked

- Repository state: cloned main at 20a3f40 (EX_138, the last commit); source_data/, results/ and
  transitory_data/ left out of the checkout entirely.
- Hashes: H-1 v1r8 quotes 92 file hashes. Leaving out the 7 its own rule excludes (the five computed
  digests in 7.3 and the two master hashes in 7.5), all other 85 match a committed Git blob, checked by tool.
- DOC-11: installed at 3d4fa3c; 19 of 19 manifest rows match. The three files that cannot hash themselves
  also match: H-1 v1r8 09e579ba...a801; register v0.24 9d9fde67...81ae; the blurb f1833da3...2d19.
- Status lines: H-1 and register v0.24 both read OWNER-RATIFIED, not CANDIDATE.
- Starting text: the text the owner started the chat with is byte-for-byte the committed blurb's body.
- No code changes: no commit has touched src/, tests/ or any .bat since PERF-1 (3fce327), so no MHUP-A
  work has started.
- Latest numbers: the latest exchange message is EX_138 (next free EX_139); the latest runner task is T015,
  report in.

## 1. Implemented, designed, ratified, unresolved

Implemented and installed: the method contract (release checks, create-only frozen records, the strict
"only draws before the target" view); 40 variants released in both games (E_1 revision 2 and 39 variants of
E_2, E_3, E_4, E_6 to E_10 and E_17 to E_19); the walk-forward driver (WF-1A); the scorer and ranking report
(WF-1B) with PERF-1; the first batches done (Powerball 17,280 runs, Oz Lotto 8,760, all SUCCESS); the first
reports showing nothing departing from fair draws in either game (development evidence only); 471 offline
tests (owner-reported on Windows; not re-run by me).

Designed and ratified (3 November 2026), not coded: MHUP-1, authorising no run, install or update. Five
parts: a master that can grow (version-2 reader); E_1 revision 3; opening the holdout once on the record
(study manifest covering cohort, code and installed environment, then the opening record); Mode H (a
precommitted holdout evaluation, not pre-draw forecasting: one batch of 40 variants x 10 targets per game,
each from the draws before its target, nothing scored until every planned run is done, then scored once and
sealed; Powerball 1585 and 1586 flagged but counted fully); the weekly session (forecast N, reveal N, score N,
then N+1; then the next draw's forecast frozen before its deadline).

Unresolved: Q7 (display restriction after Mode H; before Approval 2); the Windows POC suite choice at
MHUP-A's approval; the owner's backup confirmation; longer-term: walk-forward preregistration, each
remaining method's formula, E_63 and later, the scientific allowlist, WF-1C's open choices.

## 2. Position and immediate priority

Inside the staged handover (HO-2), at step 3. The code is paused until the takeover is verified and the
owner explicitly authorises normal work; DOC-11's install does not lift the pause. Then the priority is
MHUP-A. Planning target unchanged (Mode H and the weekly session installed by about 13 to 15 November; first
pre-draw forecasts Oz Lotto 1709 and Powerball 1592); tight now that the takeover adds a round; FB-1: slip
rather than cut.

## 3. Next tasks, dependencies and approvals

1. After authorisation: record the takeover exchanges (EX_139 onward); set up the workspace; run the suite
   on Linux (E2R-T12 needs the owner's separate approval of its run context, or is skipped and said so).
2. MHUP-A (HIGH; work-item card first; "Suggest switching to Fable (High) for this" before the core code):
   E_1 revision 3, master_versions.py, one data kind, the binding and ticket gates, the install barrier, the
   study manifest with installed-file freeze, Method_Mode_H.py, the install- and release-record tool with
   the baseline record, the Mode H batch kind and lifecycle markers, the freeze-before-outcome rule, the
   Mode H families and report texts, Run_Evaluation.bat, Run_Experiment.bat's byte-code lines,
   process_check.py, updater v0.2 (four additions), rulebook rule 7 and LW-1 wording, R-007/R-008/R-010
   folded in. Route: code review with EX_131 section 4's demonstrations, T016, two-commit install.
3. MHUP-B: same route, T017; installed before Approval 1 or only after the seal.
4. Approvals per game, each separate: Q7 and the updater self-test before Approval 2; Approval 1 (manifest,
   opening record); Approval 2 (first update, writes only if all ten holdout draws arrive); Approval 3
   (batch); Approval 4 (score, report, seal); then GOAL-1 and the first weekly session.
5. Register v0.25. 6. Then WF-1C, wave 3, NL-means, waves 4 to 11, ensembles last.

## 4. Restrictions held

Data and holdout: results only from Lotterywest-GOV (https://www.lotterywest.wa.gov.au); never
oz.lotterywest.com, never The Lott automated, no API, no browser impersonation, no scraper; no
lottery-results searches; never display, paste or compute with an outcome for Powerball >= 1577 or Oz Lotto
>= 1694; never open source_data/, results/ or transitory_data/; skip the R1 lines naming quarantined draws.
Process safety: the orphan marker blocks all launches and only the owner's manual procedure clears it; three
switches False and the allowlist empty; nothing kills a project process; a STOP is a STOP. Science: no idea
excluded by conventional statistics; mark, never suppress; statistics never a gate; strict N-1 and T-05; the
whole-file hash never reaches a method; goldens never refreshed. Process: independent other-model review of
every HIGH item, reviewer rights R-1 to R-11 supported; REVIEWER-DECIDED items reported by exception; no
updater run before MHUP-A is installed and the first update approved; the owner's name never committed.

## 5. May and may not

Now: read, check hashes, write replies, answer the reviewer's questions blind. Not without further
authorisation: any code, task file or package; workspace or suite; any commit or push, even in exchange/.
Never without a separate reviewed approval: any batch or report run; any holdout, Mode H or weekly step; any
updater run; any switch change, dependency upgrade, destructive or lifecycle test.

## 6. Discrepancies, gaps and questions

Nothing material. (a) Direction document section 3 says CATCH-UP depends on the method's "install" date;
the design's dated event is the release record (a fifth place where it is looser than the design, beyond the
four register v0.24 lists; no effect on the current cohort). (b) The template README's title says draft 4
but its status line reads "DRAFT 3"; cosmetic. (c) H-1 12.9 step 2 puts the tools README after
authorisation while section 0 lists it for reading now; read only. Not verifiable yet: the 471 count, the
owner's Windows results, the orphan marker's state, the backup. Write access: the session had a read-only
clone; push access would be needed for exchange/ commits. Question: has anything happened since EX_138
(local commits, files saved into the repository, any run)?

## 7. What happens next

The owner relays this reply to the reviewer; the reviewer suggests targeted questions; the owner relays only
the questions; Claude answers blind; the owner decides whether the takeover counts as successful.

End of the first takeover reply (recorded copy).
