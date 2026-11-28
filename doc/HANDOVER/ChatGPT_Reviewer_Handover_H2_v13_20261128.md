# H-2 v13 - ChatGPT independent reviewer handover (candidate)

Date: 28 November 2026
Project: hydra3333/analysing_perceived_randomness_in_reality
Status: RATIFIED by the owner, RAT-69 (decision log entry 397); not an operational GO.
Corrected by the Claude web chat at the owner's request after the reviewer chat ended (entry 397): the
position brought to entry 396 (QA created; the owner's decision on QA's first fetch; the agreement on main).
Proposed successor to installed H-2 v12 (RAT-67, entry 390). H-2 v12 remains ratified until replaced.
Cutoff: main 5498e5a1b0a5a7ee475385904a3052ca024a65fe, decision log entry 395, plus subsequent
owner/reviewer chat; Claude's corrections bring the position to entry 396 (main 0185e71).
Prepared by the incumbent reviewer. DEV rebuild complete and clean; 41 installable flags committed.
QA then PROD are next.

## 0. Takeover and reading order

Read current main first. This candidate updates H-2 v12 (RAT-67, entry 390).
The owner's reframing on 26 November 2026 and the agreed simple scheme supersede the former administrative
design. H-2 v9 and earlier records are retained as history and a source of independent-review experience,
not a second active design. Do not reinstate obsolete controls by reading old handovers.

Read, in order:
1. This handover and the current HEAD.
2. exchange/Claude_The_Simple_Scheme_v0_2_20261126.md (owner agreed, entry 344).
3. exchange/DECISIONS/DECISION_LOG.md from entry 330 through the newest entry, not merely this cutoff.
4. exchange/CONTINUITY_NOW.md, current top block; exchange/OWNER_REMINDERS.md for deferred work.
5. Latest ratified H-1 in doc/HANDOVER/; at cutoff Claude_Primary_Handover_H1_v18.md
   (RAT-68, entry 392). Later decisions control its work order. Read actual ratified runner
   rulebook and task files as relevant; T029-T031 are completed.
6. doc/CODING_PRACTICES_v0_1.md (RAT-40) and doc/FILE_FORM_STANDARD_v0_2.md (RAT-49), binding as
   modified by the simple scheme (section 5 below).
7. exchange/Claude_Step_2_Engine_Simplified_And_Compared_v0_1_20261126.md; subsequent corrections and
   evidence named in the decision log; a_p_r_i_r_DEV/README.md.
8. The scientific references and actual code appropriate to the next requested review (sections 3-4).
9. For the deferred tidy only: exchange/Claude_Tree_Tidy_Inventory_And_Procedure_v0_1_20261128.md;
   exchange/ChatGPT_Tree_Tidy_Consolidated_Agreement_v0_1_20261128.md (committed by Claude, cbda280), or
   its later agreed successor. See section 7A. Do not interrupt QA/PROD work for the tidy.

For the owner's precise direction, read Part 1 of
exchange/Claude_Comment_On_The_Owners_Reframing_Back_To_The_Research_v0_1_20261126.md, and the consolidated
reviewer paper exchange/ChatGPT_Comment_On_The_Owners_Reframing_Back_To_The_Research_v0_1_20261126.md.
Claude's response and entries 335 onward settle differences. Do not assume an earlier proposal is a decision.

First reply: state actual current position, outstanding items, what is authorised, next recommendation,
and uncertainties. Read only until the owner accepts takeover or specifically authorises work.
Do not impose a takeover questionnaire if the owner has waived it. No automatic tests, edits or commits.

## 1. Mandate and ownership

The research asks whether Australian Powerball and Oz Lotto draws contain patterns missed by ordinary
statistics. It is speculative exploratory work; a carefully measured null is a useful result.
The science must be right; administration small. Formal investigation, if warranted, is a separate
follow-on project using then-future draws, not an infrastructure deliverable of this project.

Owner (GitHub hydra3333) alone decides, ratifies and authorises. Never publish his personal name.
Claude web chat is primary designer/coder. ChatGPT is the independent reviewer, not the default
installer or second administrative designer. Both may contribute scientific ideas; no AI is the final
independent reviewer of its own implementation. Any future role reversal is an owner decision.
Claude Code on the owner's PC is a local runner under its own rulebook and explicit task-specific GO.

Reviewer independence remains: access exact relevant source; question assumptions; use proportionate
independent mathematical oracles/offline tests when justified and authorised; raise material findings
even outside a narrow diff; distinguish alternatives from defects; disclose uncertainty and not-tested
scope; decline unsafe work. H-2 v9 chapters 1-3 preserve historical R-1..R-11 formulations; their former
routine hash-table, exhaustive reproduction, HIGH review ceremony and package requirements are NOT
mandatory under the new scheme. Independence is retained, bureaucracy is not. Owner decides any conflict.
For behaviour-preserving changes compare detailed before/after computations. Intentional scientific
corrections and new methods need independent mathematics and suitable tests, not forced equality.

The reviewer's permitted writes are its own review/discussion papers and requested EX messages in
exchange/, and its own handover/blurb candidates or owner-authorised installed editions. Never edit
Claude's papers, H-1, the decision log, continuity page, register, code, tests or data without separate
explicit owner authority. The new direct-code-commit permission in the living subtree is Claude's,
not a general reviewer code-writing permission. Do not alter the frozen top level.
Proposed tidy does not yet authorise any deletion.

## 2. Safety and operational boundaries

- Only the owner's approved updater contacts Lotterywest-GOV (www.lotterywest.wa.gov.au, HTTPS).
  Neither AI chat nor the local runner contacts any lottery website, searches for draw results, or
  executes the updater. Read supplied or repository draw data if needed; never write accepted results
  or research outputs. Chat-derived observations are suggestive, not reviewed scientific results.
- Strict method-facing N-1, separate games, TOP/WORST from the same model for each target.
- No process termination; no PC date/time/time-zone changes. A STOP is a STOP. No work on the
  owner's PC, installation, run, backup, restore, migration or deletion without his explicit GO.
  A design agreement, review PASS or commit is never a GO.
- Frozen first-system files and sealed Mode H records are not altered or maintained. Its three safety
  switches stay False, allowlist empty, orphan marker blocks launches as before. Owner entry 353
  removes the orphan-marker check from the NEW living trees at step 4 only; no bypass in old system.
- No writes to transitory_data/ or GAIS/. No Git-based operational gate. PROD is protected against
  side effects of DEV/QA work. Entry 365 permits Copy_From_PROD exactly one transient source write:
  records/TREE.lock, created and removed by the command. No other PROD writes by that command.
- Runner rulebook CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md v0.8 ratified (RAT-66, 370); settings r2
  installed (375). Scratch-only writes in D:\DELETE_ME for named tasks on owner GO. Real updater
  forbidden to runner everywhere, including scratch; invented-page tests only in authorised suite.
  Read-only copying from DEV only as task names. T031 specifically permitted real DEV Python for
  scratch work, -I -B, scratch cwd/TMP/TEMP, no package changes. T031 complete; no blanket permission
  follows. Seven successful permission probes establish tested forms only, not a filesystem sandbox.
  Rulebook primary; new task needs separate GO. No real-tree commands by runner.

## 3. Scientific rules that remain

Read the scientific portions of doc/Predictive_Randomness_System_Specification_v0_6.md, sections
1.2, 3.4, 6, 8, 9, 10, and the underlying R1/R2/R3 and method/readout contracts it references as
needed. Its obsolete administrative provisions and the old deployment design v0.12 are superseded
by simple scheme v0.2 sections 2 and 11. Later decisions control. Do not resurrect Mode H rules.

For target T, train/compute only from permitted earlier draws, including all method-facing metadata,
seeds, cache keys and tie order. Test suffix isolation when scientifically relevant. Preserve
permitted-view digest: it participates in deterministic tie ordering. Keep deterministic seeds where
applicable; the current methods are deterministic. TOP and WORST are produced by the same model,
with valid outputs; score against the proper game/outcome; no pooling. Preserve ranking measures,
divisions, minimum history, draw-order views and OV-1 numerical arithmetic.

Whether historical outcomes were previously known to designers is NOT an eligibility concern.
Try reasonably not to let such knowledge influence design, but do not disqualify an idea or create
an unseen-results check. Full historical walk-forward and normal scoring/ranking are legitimate.
The latest accepted results and actual local starting draws are used; no new holdout or formal
evidence-preservation regime is required. A potential follow-on investigation is separate.

Both OV-1 series are exploratory: all available scored history; and one combined series per game
with each method contributing after its recorded establishment draw, no earlier than its first target,
and strictly before retirement. Establishment numbers are local bookkeeping, not proof of what
designers knew or eligibility to run. Retain OV-1 arithmetic (six lambda components, threshold 40,
the conditional fair-draw/nonanticipation mathematics); 40 is an investigative reference, not a
certified false-positive guarantee for this exploratory selection. No automatic formal claim or
trigger. No new hashing of results or backups for proof. Existing updater ledger comparison retained
by owner entry 335. Corrected historical draws require corrected scores at T and affected later forecasts.

## 4. Simple scheme in force

Three independent trees, one shape, one local job and one updater, no implicit PROD copy:
DEV = E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\a_p_r_i_r_DEV
QA = T:\a_p_r_i_r_QA; PROD = G:\a_p_r_i_r_PROD; backups T:\a_p_r_i_r_backups\{DEV,QA,PROD}.
DEV has deploy/ and tests/; each tree has its own .venv, settings, software, accepted results and research.
Top-level src/, tests/, documents and historical artifacts remain frozen as the regression reference,
except authorised current documentation/records. QA can equal or be ahead of PROD. QA is not a gate.
The proposed later retirement of the frozen software is not ratified; see section 7A.

Settings: identical form, role line differs; role sections specify tree_root and backup_root.
Local root comes from launcher, not current directory or configured path; role suffix and actual
real absolute Windows path must agree. Validate both ends of copies; create only absent/empty tree.
No duplicate/nested tree roots; no backup root equal to or inside ANY tree. Never copy settings
between trees. One records/TREE.lock per tree; lock all participating existing trees, including sources and --show.
Who_Uses is the read-only exception. Child job uses its own Python, --no-update and --under-lock key;
parent waits without killing child and keeps lock until child ends. Windows Ctrl+C may reach the child itself.
Manual stale-lock removal only
when owner has ensured no relevant job runs. No elaborate process inspection or recovery machinery.

I_AM_INSTALLABLE identifies marked software; stale mark reported, no deployment of unmarked bytes.
INFRA flag holds engine, updater and launcher fingerprints; updater/launcher-only changes do not
trigger scientific rebuilding. Shared helper changes must include all affected destination methods,
including readable declarations of refused methods; otherwise hold back and report.
I_AM_RETIRED has game-specific retirement boundaries and reason. IN_PLACE_SINCE is per game plus
method fingerprint, local establishment bookkeeping. Entry 352: all THREE files tracked in DEV Git.
Exclude flags and caches from fingerprints. Compare producer fingerprints to software: a difference
means replace/rebuild, not refuse (research/producer fingerprints, not invalid settings/results).
Method change rebuilds that method; infrastructure change rebuilds
all in both games. Recompute incomplete/outdated records. Retirement keeps earlier results, rebuilds
up to but excluding retirement draw; forecasts AND scores from retirement draw onward removed
(entry 353 amends RAT-61 choice 3). Restore/rebuild not a formal evidence operation.

Run_Research: local updater unless --no-update, rebuild stale data, fill/catch up, forecast next draw,
score, league/reports and both OV-1 series, job log, backup. --rebuild <method>, --rebuild-all.
Commands: Run_Results_Updater, Backup in every tree; DEV Make_Installable, Who_Uses, Create_Tree,
Install (including --show), Retire, Copy_From_PROD, Restore. Create_Tree copies flagged infrastructure,
flagged non-retired methods and accepted results, checks copy and writes settings last. Install preserves
local flags; existing retired methods may be replaced but never added. Retire computes each tree's next
local draw, backs up all affected trees first, writes flags; no job until next ordinary run. No typed
confirmation. Copy_From_PROD software/data/both QA or data DEV; both saves an intermediate rebuild.
Software copy includes retirement and establishment flags (not installable); no flags copied by
Install/Create_Tree. Data copy checks both PROD games with existing reader and nonempty source before
replacement. Only temporary source lock in PROD. Install/Copy invoke destination's own no-update job.
Backup before replacement or retirement, after jobs and on demand: ZIP level 9, omit .venv, lock and
caches, never overwrite. Directory-listing errors fail backup. Failure stops replacement; after job it
warns twice, notes failure in log, returns 1; results stand. Log line precedes backup. Restore checks ZIP
and settings, unpacks fresh before renaming old tree aside, then renames fresh into place; rebuild venv.
Never deletes old tree; unreadable settings require manual rename-aside. No mixing. Do not demand
additional backup hashes, readback proofs or recovery kits.

## 5. Review and coding standards

Review where science is: actual method mathematics, N-1, numerical behaviour, scoring, OV-1, correct
rebuild and meaningful equivalence. Admin scripts: one proportionate reading for whether they can
destroy something not reproducible, or silently invalidate results. Raise concrete consequences with
simplest remedy. No speculative edge-case programmes, routine mutation campaigns for admin code,
hash tables, package overlays or repeated correction/recheck rounds. A named Git commit identifies
the bytes. Verify relevant claims, distinguish inspected vs author-tested vs independently executed.
No testing of real PC or real scientific data by the reviewer without proper authority. Do not claim
a run from a static reading. No demand to repeat unaffected tests solely for completeness.

Binding coding practices doc/CODING_PRACTICES_v0_1.md: each Python file header explains purpose,
design reference, imports and callers; constants documented near top; meaningful names; function
comments explain inputs, return example, refusals; clear errors say what/where/why/remedy; deterministic
behaviour, shared tasks implemented once; no swallowed failures; purposeful named tests and planted
faults in proportion to risk. Each code commit and accompanying paper says "coding practices met"
or explains exceptions. Reviewer checks these by eye in ordinary review, not a new approval gate.
Under the new scheme: cite scheme for administration, "held/not current" becomes rebuild reporting,
installed software may change. Review standards together before new methods; no preemptive rewrite.

File form doc/FILE_FORM_STANDARD_v0_2.md as amended by scheme: all living text CRLF and ASCII,
including JSONL (old LF hash-chain exception gone); explicit write endings, Git converts nothing.
Intentional LF bytes in synthetic fixtures are test inputs, not a change to the living-file standard.
a_p_r_i_r_DEV/deploy/file_form.py is checker. Frozen history and GAIS untouched; decision log and
continuity page still LF until step 7. Cloud shell helpers outside living Windows system.
Python 3.15 only. Do not apply old file-form migration procedure to new work.

Owner working preference: plain English, question/why/recommendation/options, disclose uncertainty,
short milestone process note. Every response says what owner should do next. Discuss before EX;
issue numbered EX only when asked. Paste-ready short relay block when useful. Fresh fetch before
review or write, do not race owner pull-to-push interval; only named paths, no overwrite of history.
No routine hash table; normal exact readback for own publication is enough. Shared EX numbering
highest existing + 1, currently EX_334 next (EX_333 last), subject to fresh fetch. Owner record of
decision is authoritative; do not silently change choices. Claude's Fable (High) model rule is
Claude's; do not claim to select Claude's model or change user's model setting.

## 6. Current position at cutoff (entry 395 and subsequent chat, 28 November 2026)

Old design A/B/C accepted (EX_321/327/333) but never installed; set aside entry 330. Simple scheme agreed
344, direct Claude code commits to a_p_r_i_r_DEV approved 342. H-1 v17r1 RAT-64, H-2 v11 RAT-65.
Steps 1-4 complete. Work order 365 items 1-6 and the DEV wording-fix rebuild complete.
Item 7: QA then PROD, not yet established. Frozen top level retained for now.
No outstanding findings on the installed engine. Proposed tidy has bounded corrections and awaits agreement.

Step 1: 4985468177213245ddd8c86c9e01579143417bba, living subtree copied.
Step 2: aedda2e; accepted/invented results SAME; 161 tests. RAT-61 choices with later amendments.
Corrections 57ca865 (354), owner approvals 356: global engine rebuild deletes absent-method results too,
obsolete reports removed, malformed IN_PLACE_SINCE repaired before reading status, retirement forecast
and score at boundary removed. Full exploratory OV-1 comparison added. Ordinary absent-method results
remain outside global rebuild and excluded from reports. All three flags tracked in DEV (352).
Updater excluded from engine fingerprint (356). No formal recheck requested.

Step 3: d4f01e0 (357), simplified local updater, original validation/ledger comparison retained,
Mode H removed. Reviewer accepted overall. Corrections 2ebbb11 (359): website Stop suppresses further
fetches in that job, both games continue on accepted local results if reader accepts; other failures
do not suppress other game's fetch; failure warning does not assert no results added; final URL
rechecked immediately before parse. Updater comparison SAME; 192 tests. Common entry and single lock
carried to 4a and addressed. Exact intended HTTPS host/accepted final URL checks are not a network
firewall against browser subrequests. No AI/local-runner real site contact.

Step 4a: 3effdbe (361), 213 tests, updater and engine comparisons SAME; accepted choices 362.
Reviewer reading: backup os.walk must raise listing errors, Make_Installable reads under lock,
Who_Uses read-only exception. All corrected e452f32 (363), 215 tests. No recheck requested.

Step 4b: 42bb082 (364), 270 tests, 15 planted faults caught, Linux child-process install test passed.
End-of-step-4 accepted-results comparison SAME: PB 15,118 forecasts and 15,078 scores, Oz 6,598 and
6,558, 40 methods each game; both OV-1 series line by line; 901 and 475 report files byte for byte.
Reviewer concurred with design and choices, four findings confirmed and corrected 068c93f (365):
F01 launcher installation-only fingerprint; F02 shared helper checks readable refused declarations;
F03 source preflight for both games and nonempty enumeration before removal; F04 Popen wait in steps
without kill on Ctrl+C, keep lock until child ends. Windows console Ctrl+C can reach child itself;
no command ends another process. README clarifies damaged-tree manual rename-aside and PROD lock.
277 tests, all four re-planted faults caught, no repeat full comparison requested. Owner approved
choices, source lock and reversed seeding work order at 17:33 (365).

Report wording: 168b896 and refinements 56cc3ec (366), accepted. RETIRED/method replace old wording.
Both OV-1 series exploratory, reference line 40, no error bound claimed. "Score (numerical lower
bound)", forecasts use permitted earlier-draw view, choices may depend on observed results, each
draw at most once; safeguards do not establish independence of method choices. 280 reported cloud
tests; reports-only comparison SAME (controlled experiment; never manually set operational fingerprint).
Above implementation evidence was author-reported cloud Linux; reviewer inspected named commits.

Handovers RAT-64/65 and rulebook v0.8 RAT-66 installed (367,370). T029-T031 tasks reviewed; corrections
4180ac2 (369). Scratch TMP/TEMP/PIP_CACHE_DIR and T031 interpreter exception agreed (366).
T029 STOPs: backslash deny patterns and escaped variants did not refuse; settings r2 installed (375)
adds four backslash-independent project-path patterns (*T:*a_p_r_i_r*, lower case and G: analogues).
Avoid bare *T:* (trailing :* syntax). All seven harmless probes refused; no broader protection claim.
Next STOP: inherited VIRTUAL_ENV; command-local subshell unset only, 7bfc772 (376-377); inherited
PATH may remain; scripts verify destination. Next STOP: test fixture CRLF/LF mismatch, 165d19f;
two fixture changes only, actual diff read. Reproduced by author with CRLF simulation; corrected
suite passed normally and simulated. Failed run: 276 passed, 1 failed, 3 skipped (379).

T029 PASS a0662da (380): 280 run, 277 passed, 3 expected skips (frozen reference absent), zero errors
or failures, exit 0; scratch own Python 3.15.2, 39 requirements; seven probes refused, temp empty,
no deviations. T030 PASS 607834e (382): all 31 steps, ten minutes, three scratch trees with invented
results and own venvs. Create_Tree QA/PROD, Install --show and actual child job under lock (no lock
left), stale flag, Backup, Retire all three and PROD job, Copy_From_PROD both (QA job zero forecasts
and scores), Restore (Windows rename aside, 563 files restored), three planted refusals, Who_Uses.
Reviewer accepts both, no repeats. Simulated Ctrl+C tests do not prove real console interruption
cannot reach the child.

DEV first fill (383): owner --no-update, 49 minutes, backup DEV_20261127_215052_after_job.zip.
PB through 1591: 15,118 forecasts, 15,078 scores; Oz through 1708: 6,598 / 6,558; 40 methods each.
40 IN_PLACE_SINCE files committed 62872f8, matching method fingerprints and both establishment draws
(1591/1708), zero form faults across 229 tracked DEV files.

T031 PASS 22ea440 (384): real DEV first fill copied by reading, fingerprint matched, frozen engine
filled in scratch, establishment aligned only in scratch, both rerun with real DEV Python 3.15.2,
numpy 2.5.5, --no-update. No REBUILD in new scratch tree. Twelve SAME lines and RESULT: SAME.
PB: 40 methods, 15,118 forecasts, 15,078 scores, second OV-1 41 lines (1551-1591), all-draws 447,
901 reports (2,710 declared wording replacements). Oz: 40, 6,598, 6,558, second OV-1 41 lines
(1668-1708), all-draws 234, 475 reports (1,432 replacements). Total 21,716 forecasts, 21,636 scores,
763 OV-1 lines, 1,376 reports matched with agreed normalisations. Reversed seeding saved a repeat
DEV computation; artificial alignment never written back. Owner accepted 385; reviewer accepted
reported evidence, not independently repeated. Equivalence of tested computations, not validation
of speculative hypotheses. Accepted runner deviations: unchanged background commands finish before
advancing; file tool for authorised report when guards refuse command text.

First real fetch by owner alone (386), 28 Nov 08:05: each game 24 overlapping matched, 2 added,
0 warnings, grabs kept, old masters backed up. PB now 1593, Oz 1710. Owner inspected files.
Normal DEV job 08:13-08:17 (387): both 26 matched, 0 added, 0 warnings, 80 forecasts and 80 scores
each, 2 series and 12 report files each, no REBUILD. Backup DEV_20261128_081745_after_job.zip.
Prevailing OV-1 PB 1592-1593, 0.983267352796; Oz 1709-1710, 0.997794221022; below reference 40.
These are real DEV establishment cohorts, not T031's 41-line aligned cohorts.

Owner noticed "worked through draw 1594 of 1593" (387). Reviewer independently read run_game and
complete_draw: next target included, scoring restricted to <= latest actual, wording defect only.
Owner chose immediate fix (388), before QA/PROD. Commit 8fce853: complete diff read (PASS,389);
one file, two lines, "processed target draw {draw} (results on file through {last_draw})".
No control-flow or scientific changes; 280 author-reported cloud tests pass. Engine fingerprint
changes, updater and method fingerprints unchanged. Normal rebuild mechanism, no exemptions,
no comparison campaign. DEV rebuild --no-update agreed (389), but owner ran ordinary job (393):
28 Nov 08:28-09:17, 49 min, updater 26 matched/0 added/0 warnings in each game, unchanged data.
One REBUILD, all 80 stored method results deleted and rebuilt; PB 15,198 forecasts / 15,158 scores
through 1593, Oz 6,678 / 6,638 through 1710; next targets 1594/1711. Corrected progress displayed.
Prevailing OV-1 unchanged to last digit (PB 1592-1593, 0.983267352796; Oz 1709-1710, 0.997794221022).
904/478 report files; DEV_20261128_091700_after_job.zip. All past forecasts now recomputed after
outcomes were on file, bookkeeping only. Owner git status clean (394); all 40 establishment flags
unchanged. Reviewer accepts reported outcome. No repeat rebuild or comparison needed.
H-2 v12 installed 436f05e9 (blurb e3b14c7a), RAT-67 entry 390; H-1 v18 RAT-68 entry 392.
At 5498e5a, 41 I_AM_INSTALLABLE flags (INFRA and 40 variants) committed. QA CREATED (entry 396):
Make_Installable ALL INFRA flagged 40 methods and the infrastructure (engine 75c7e6195c53...);
Create_Tree QA copied 157 software and 12 results files to T:\a_p_r_i_r_QA, settings last; QA's own
.venv built (Python 3.15.2, numpy 2.5.5, 39 packages, no broken requirements). OWNER DECISION (396):
QA's first fill is an ordinary fetching Run_Research.bat, no --no-update fill and no separate
standalone fetch first; the updater has fetched three times in DEV with every overlap matching, and
Create_Tree checks QA's updater fingerprint. That fill started about 10:31; its output is awaited.
Expected: 26 matched/0 added each game, then DEV's totals (PB 15,198/15,158; Oz 6,678/6,638) while no
new draw has arrived (Oz Lotto's next is Tuesday 1 December). Fetch newest main before advising owner.
Evidence distinction: independent static review and acceptance of author/runner/owner reports,
not independent runtime execution. No outstanding installed-engine findings.

## 7. Next work (each on owner's GO)

Work order 365 items 1-6 COMPLETE, including owner acceptance of T031 and both real DEV updater
runs. Do not repeat completed rehearsal/fetch milestones.

DEV rebuild and clean Git status confirmed (393-394). No repeat. Immediate item 7: establish QA
then PROD, each on owner's separate GO. Make_Installable ALL INFRA flags committed at 5498e5a.
QA is created and its first (fetching) fill was running at the cutoff (entry 396); check its output
before advising PROD. Create_Tree copies flagged infrastructure and nonretired flagged
methods, accepted results only, not historical computed outputs. Local establishment draws
settled at first use. Do not artificially align or copy old establishment flags. Compare
forecasts/scores for identical data/methods/targets; all-draw OV-1 comparable on matching inputs,
prevailing OV-1 may differ by local establishment. The separate standalone first fetch of entry 358
is dropped for QA by the owner (396); Claude recommends the same for PROD (the owner's decision); read
the job's two [MASTER] lines. Only owner operates real trees; no AI or
runner real fetch. Fetch newest status, do not assume QA/PROD exist. Complete QA then PROD before
any tidy. Frozen top-level venv remains until ratified tidy.

Separate whole-project ZIP backup: native Windows tar Deflate 9, entire repository incl .git/.venv,
timestamp, primary U: and USB F:/I:/Y:, full archive read and SHA-256 verified copies, no overwrite.
Owner reported successful run 28 Nov 09:23:03-09:46:08; four copies, SHA-256:
0DA6DF03A81A1C4F3446CA6F4AE142CEE4221E776E9FED9EABF605167D49B373
Filename analysing_perceived_randomness_in_reality_2026_11_28_09_23_03.zip.
Distinct from the living Backup command. No restoration test reported; hash proves copy equality,
not source completeness. Retain copies. New full backup immediately before any tidy.
No script committed here; no PC operation authorised for AI. Source idle during full backup.

Step 7: how-to and final handovers, CRLF conversion of remaining LF decision log and continuity,
trim continuity without losing live material, three-way operations manual revisit (343).
One consolidated tidy proposed for after QA/PROD, not yet ratified (section 7A).

Step 8: before new methods, independent coding-practice suggestions (299-300), future priorities
(289; doc/Predictive_Randomness_Future_Method_Priorities_v0_1_DRAFT.md), roles/possible self-contained
role-reversal trial (292). Preserve owner reminders, E_45, E_59, speculative leads, all methods and
NL-means R-002; no changed priority order assumed. Profiling/acceleration deferred until full
implementation; measure first, then consider selective Cython/Numba/native optimisation.
OUTLANDISH_01 Powerball investigation closed by owner; Oz Lotto not required. No revival.
No-op runtime optimisation only if owner still wants it.

Recommendation at cutoff: proceed with QA, then PROD. Do not repeat completed reviews or rebuild.
No PC action authorised by this paper.

## 7A. Deferred repository tidy: agreement in principle, NOT RATIFIED

Entries 394-395: owner explored safe history reset; Claude measured 68 MB packed history versus 63 MB
for one commit. Local .git 95 MB of 1.5 GB tree; 178 MB tracked. Reviewer withdraws history-reset
proposal: gain about 5 MB not worth loss of cited commits. Retain all history and existing repository,
secrets and permissions. Optional ordinary git gc owner only, after backup. No force-push or rewrite.

Read Claude's tidy proposal v0.1 at 6d0ba88 and the reviewer's consolidated agreement v0.1 dated
28 Nov, committed unchanged by Claude (cbda280, entry 396):
exchange/ChatGPT_Tree_Tidy_Consolidated_Agreement_v0_1_20261128.md.
SHA-256 a6032a02628a0ef17b4a1122f6f62a78dd211424c56a5622234d5e9729480c7b.
Owner expressly wants useful exchange material preserved. Current proposal's blanket EX/package
removal is conditional on retaining unique valuable science, mathematical reasoning, deferred
proposals, unresolved questions, owner requirements and evidence. Keep when in doubt; no target
removal quota. Entire exchange/DECISIONS/ kept, plus continuity/reminders/roadmap/README, scheme and
supporting papers, operations-manual discussion, consolidated agreement, tidy proposal and P1 list.
Keep current scientific specs, method designs, errata, standards, handovers, GASI owner ideas,
future priorities, deferred performance, R-002 in reminders. Actual doc listing and selected E1/E2R
designs reviewed; no additional specific doc requested, subject to retention check. Preserve original
results/ unchanged and runner folder incl old reports/tasks (historical tasks not executable authority).
CLAUDE'S PROPOSED exchange/ RULE (entry 396; awaits the reviewer's view): in the work-package folders
(EX_nnn_* and CLAUDE_WEB_TOOLS) keep every .md/.txt/.json (1,308 files, 25 MB) and remove only code
and data copies .py/.diff/.zip/.bat/.ini/.cmd (1,291 files, 38.5 MB), whose real versions are in
history and a_p_r_i_r_DEV; keep all 334 EX messages and the rest of exchange/; any file may be named
as an exception. Claude proposes writing the revised candidate and P1 once, after PROD.

Proposed removal after QA/PROD: GAIS (owner says can go), obsolete review/work packages and EX
correspondence subject to retention policy, superseded documents, frozen root software, tests,
launchers, data stubs, old venv and transitory_data. No living dependencies except two comparison
programs. Retire compare_with_frozen.py and compare_updater_with_frozen.py under DEV deploy/ and
8 tests (6 test_research_compare.py, 2 TheSameAsTheFrozenUpdater); preserve other 25 updater tests'
fixtures make_tree, InventedPages, page_text, invented_draw, load, HELD, TODAY unchanged in tests/.
280 -> 272 expected baseline. No src changes, even obsolete updater comment; all remaining tests
pass including no-real-browser guard. Git tree equality of results/ and DEV src after both commits.

Four reviewer corrections C01-C04, included in consolidated agreement:
C01 first fills: forecast/score equality for identical inputs; local prevailing OV-1 may differ.
C02 actual .vscode/settings.json uses retiring root .venv twice; change only interpreter and CMD
activation paths to a_p_r_i_r_DEV/.venv, preserving profile. Explicit allowed P4 modification.
C03 tag covers tracked files only; fresh verified full backup and confirm specific untracked entries.
Full-path owner deletion only, never broad git clean -fdx, no whole D: scratch folder cleanup.
Rollback includes subsequent rulebook/docs/config changes, reverse relevant commits, restore
untracked files from backup. No automatic undo on failed check; STOP and consult owner.
C04 after clean owner pull, DEV --no-update: no REBUILD, zero new forecasts/scores, unchanged
prevailing OV-1/establishment records, successful backup, assuming unchanged inputs. QA/PROD untouched.

Runner v0.9 proposed: real DEV interpreter full path -I -B only, no activation/pip/env change;
scratch cwd/TMP/TEMP/outputs, scratch operational trees own venvs, no real updater or real-tree
commands. Keep safety permissions, review any change. v0.8 remains binding until separately ratified.
Check stale interpreter references. GAIS at consolidated tidy preferred. Entire runner folder retained.

Next actions for Claude: commit consolidated agreement unchanged, record status; refine keep list
conservatively, check live dependencies, update proposal incorporating corrections; prepare exact
P1 tracked removal list/counts/sizes at actual baseline and permitted change list; retain P1.
Send revised proposal and P1 to reviewer, iterate to mutual agreement; owner ratifies exact scope
(the RAT number at the time; RAT-69 went to this handover), QA/PROD established, separate GO. Refresh
full backup,
no active runner/job, clean Git, annotated before_tidy_<date> tag pushed and peeled commit verified.
P3/P4 two principal commits with source/results tree equality and exact diff checks, archive index
links to tag/inventory and retrieval examples. P4a rulebook candidate/ratification; P5 owner pull
and no-update check; P6 owner explicit untracked paths only; P7 handovers and records refreshed.
No tests, deletion, tag or code changes performed by reviewer for this design review.

No new scientific comparison campaign. Independent review and owner authority remain. QA first.

END.
