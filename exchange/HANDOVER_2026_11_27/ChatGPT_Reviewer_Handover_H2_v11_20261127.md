# H-2 v11 - ChatGPT independent reviewer handover (short form)

Date: 27 November 2026
Project: hydra3333/analysing_perceived_randomness_in_reality
Status: CANDIDATE for owner ratification; supersedes H-2 v10 (RAT-63) upon owner agreement.
Cutoff: main 168b896cf75874bfad77480991392fc49a9a4d63, decision log entry 365,
plus the subsequent owner chat instruction to proceed with the three rehearsal decisions and wording refinements.
Rulebook v0.8 and refreshed H-1 are being prepared, not ratified at this cutoff.
Prepared by the incumbent reviewer at the owner's request.

## 0. Takeover and reading order

Read current main first. This edition updates the short-form H-2 v10 (RAT-63, entry 355).
The owner's reframing on 26 November 2026 and the agreed simple scheme supersede the former administrative
design. H-2 v9 and earlier records are retained as history and a source of independent-review experience,
not a second active design. Do not reinstate obsolete controls by reading old handovers.

Read, in order:
1. This handover and the current HEAD.
2. exchange/Claude_The_Simple_Scheme_v0_2_20261126.md (owner agreed, entry 344).
3. exchange/DECISIONS/DECISION_LOG.md from entry 330 through the newest entry, not merely this cutoff.
4. exchange/CONTINUITY_NOW.md, current top block; exchange/OWNER_REMINDERS.md for deferred work.
5. Latest ratified H-1 in doc/HANDOVER/; at cutoff Claude_Primary_Handover_H1_v16r1.md
   (RAT-62, entry 352), now outdated in its work order. Apply later decisions. Read new candidate
   and runner rulebook/task files when available, distinguishing candidates from ratified instructions.
6. doc/CODING_PRACTICES_v0_1.md (RAT-40) and doc/FILE_FORM_STANDARD_v0_2.md (RAT-49), binding as
   modified by the simple scheme (section 5 below).
7. exchange/Claude_Step_2_Engine_Simplified_And_Compared_v0_1_20261126.md; subsequent corrections and
   evidence named in the decision log; a_p_r_i_r_DEV/README.md.
8. The scientific references and actual code appropriate to the next requested review (sections 3-4).

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

The reviewer's permitted writes are its own review/discussion papers and requested EX messages in
exchange/, and its own handover/blurb candidates or owner-authorised installed editions. Never edit
Claude's papers, H-1, the decision log, continuity page, register, code, tests or data without separate
explicit owner authority. The new direct-code-commit permission in the living subtree is Claude's,
not a general reviewer code-writing permission. Do not alter the frozen top level.

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
- Runner rulebook CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md v0.7 remains in force for its existing
  scope until its replacement is ratified. Proposed v0.8: scratch-only writes in D:\DELETE_ME,
  task-specific GO for scratch commands; real updater prohibited everywhere, including scratch,
  except isolated invented-page tests with no network. Read-only copying from real DEV into scratch
  permitted by entry 365 subject to updated rulebook/task. Proposed T031-only exception to use
  real DEV's Python as interpreter for scratch computations (no package changes or other writes).
  Use -I -B, scratch cwd and TMP/TEMP; no output leaves scratch. No runner execution or new privilege
  merely from this handover. Read actual ratified rulebook and task before any runner GO.

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

Settings: identical form, role line differs; role sections specify tree_root and backup_root.
Local root comes from launcher, not current directory or configured path; role suffix and actual
real absolute Windows path must agree. Validate both ends of copies; create only absent/empty tree.
No duplicate/nested tree roots; no backup root equal to or inside ANY tree. Never copy settings
between trees. One records/TREE.lock per tree; lock all participating existing trees, including sources and --show.
Who_Uses is the read-only exception. Child job uses its own Python, --no-update and --under-lock key;
parent waits without killing child and keeps lock until child ends. Manual stale-lock removal only
when owner has ensured no relevant job runs. No elaborate process inspection or recovery machinery.

I_AM_INSTALLABLE identifies marked software; stale mark reported, no deployment of unmarked bytes.
INFRA flag holds engine, updater and launcher fingerprints; updater/launcher-only changes do not
trigger scientific rebuilding. Shared helper changes must include all affected destination methods,
including readable declarations of refused methods; otherwise hold back and report.
I_AM_RETIRED has game-specific retirement boundaries and reason. IN_PLACE_SINCE is per game plus
method fingerprint, local establishment bookkeeping. Entry 352: all THREE files tracked in DEV Git.
Exclude flags and caches from fingerprints. Compare producer fingerprints to software: a difference
means replace/rebuild, not refuse. Method change rebuilds that method; infrastructure change rebuilds
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

## 6. Current position at cutoff (entry 365 and report commit 168b896)

Old design A/B/C accepted (EX_321/327/333) but never installed; set aside entry 330. Simple scheme agreed
344, direct Claude code commits to a_p_r_i_r_DEV approved 342. H-1 v16r1 RAT-62, H-2 v10 RAT-63.
Steps 1-4 complete; no outstanding reviewer findings from those steps. No Windows rehearsal yet.
Owner built living .venv (346); frozen top-level .venv retained. QA/PROD not established.

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

Report wording: 168b896cf75874bfad77480991392fc49a9a4d63. RETIRED/method replace old wording,
second OV-1 explicitly exploratory, reference line 40, no statistical error bound; 20 declared wording
normalisations on frozen reports only. 280 tests; SAME on accepted results with reports regenerated
from stored computations, not full new-engine fill. Reviewer read PREVAILING_CLAIM and comparison.
Recommended two refinements: "score (numerical lower bound)" instead of "proved lower bound";
forecasts use permitted earlier-draw view, choices may depend on observed results, each draw at
most once, safeguards do not establish independence of method choices. Owner says Claude is
implementing the relayed recommendations. Check actual new commit and updated normalisation list.
No repeat full comparison requested just for wording. Do not change operational fingerprint manually
to avoid a rebuild: cloud reports-only experiment was a controlled comparison, not operational advice.

All tests and comparisons above are author-reported cloud Linux evidence (Python 3.15.0b4).
Reviewer inspected named commits, no independent runtime execution; no live website reached.
Windows whole-tree rename, real Windows child-process launch and equivalence remain to be shown.
No owner-PC operation authorised by this handover.

## 7. Next work (each on owner's GO)

Entry 365 replaces original scheme order for steps 5-6. Read actual current decisions before action.

1. Finish report wording refinements, runner rulebook v0.8, rehearsal task files, refresh H-1/H-2.
   Owner says Claude is proceeding on relayed recommendations; at cutoff no new rulebook or task
   ratification recorded. Do not treat an outline as executable authority.
2. T029: Windows suite in scratch DEV with fresh own venv, TMP/TEMP within scratch; T030: operational
   rehearsal of commands on three scratch trees with invented small histories. Include real child
   process and restore rename, planted refusals, role/path/lock checks. Scratch-only configured
   roots and backups, role suffixes. Passing simulated interrupt tests is not observing real
   console Ctrl+C; no need to interrupt real job. Runner never real updater.
3. Owner performs operational DEV first fill himself with --no-update, after operational rehearsal
   accepted. About 47 minutes as previously measured, not a guarantee. Only accepted historical data.
4. T031: runner copies required DEV source_data and results/research into scratch by reading.
   Frozen engine run there; align establishment flags in scratch only, then compare both engines.
   No data leaves scratch, no artificial flags touch real DEV. Preserve actual computation provenance.
   No import utility. Proposed approved interpreter choice: real DEV .venv Python for T031 scratch
   only, including comparison children, -I -B, scratch cwd/TMP/TEMP, no package writes or upgrades.
   This avoids version differences without a new environment gate. Check ratified task permissions.
   Compare both games, all method forecasts/scores, both OV-1 series, reports with only declared
   wording normalisations. Regression equivalence is not independent validation of hypotheses.
5. Owner accepts Windows comparison. If DIFFERENT, investigate and correct before proceeding;
   DEV generated research can be rebuilt. Do not silently normalise numerical differences.
6. Owner alone performs first real fetch: Run_Results_Updater.bat in DEV, standalone (entry 358).
   Until then DEV jobs --no-update. Inspect printed output, ledger, grab and backup when updated;
   only then owner runs a fetching job. Remind again before first QA and PROD jobs. No AI real fetch.
7. Establish QA then PROD, each on GO, correct settings and fresh own venv; use flagged software.
   Frozen top-level venv may go only after reference use and explicit owner decision.

Rulebook v0.8 proposed: update role paths, distinguish real-tree command prohibitions from task-specific
scratch authorisation, never real updater even in scratch. Remove old known-failure exception; tests
currently have none (platform-specific skips should still be described). Two proposed permission guards
in owner's .claude/settings.json (results_updater; T: and G:): support after checking patterns, not
a sandbox or substitute for rulebook. Invented-page tests remain permitted. Owner changes settings.
Do not claim these guards are installed or tested until evidence exists.

Step 7: how-to and final handovers, CRLF conversion of two remaining LF records, trim continuity,
three-way operations manual revisit (343); owner decides frozen top-level disposition.
Step 8: before new methods, independent coding-practice suggestions (299-300), future priorities
(289; doc/Predictive_Randomness_Future_Method_Priorities_v0_1_DRAFT.md), roles/possible self-contained
role-reversal trial (292). Preserve owner reminders, E_45, E_59, speculative leads, all methods and
NL-means R-002; no changed priority order assumed. Profiling/acceleration deferred until full
implementation; measure first, then consider selective Cython/Numba/native optimisation.
OUTLANDISH_01 Powerball investigation closed by owner; Oz Lotto not required. No revival.
No-op runtime optimisation only if owner still wants it.

Recommendation at cutoff: finish and ratify handovers/rulebook/tasks, then owner GO for T029 and T030.
Do not repeat completed reviews. No PC action authorised by this paper.

END.
