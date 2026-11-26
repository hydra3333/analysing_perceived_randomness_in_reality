# H-2 v10 - ChatGPT independent reviewer handover (short form)

Date: 27 November 2026
Project: hydra3333/analysing_perceived_randomness_in_reality
Status: CANDIDATE for owner ratification; supersedes H-2 v9 upon owner agreement.
Cutoff: main aa60884324e15deaf182b488152079d336b946a6, decision log entry 353.
Prepared by the incumbent reviewer at the owner's request.

## 0. Takeover and reading order

Read current main first. This short handover replaces the old operational account of H-2 v9 (RAT-57).
The owner's reframing on 26 November 2026 and the agreed simple scheme supersede the former administrative
design. H-2 v9 and earlier records are retained as history and a source of independent-review experience,
not a second active design. Do not reinstate obsolete controls by reading old handovers.

Read, in order:
1. This handover and the current HEAD.
2. exchange/Claude_The_Simple_Scheme_v0_2_20261126.md (owner agreed, entry 344).
3. exchange/DECISIONS/DECISION_LOG.md from entry 330 through the newest entry, not merely this cutoff.
4. exchange/CONTINUITY_NOW.md, current top block; exchange/OWNER_REMINDERS.md for deferred work.
5. doc/HANDOVER/Claude_Primary_Handover_H1_v16r1.md (RAT-62, entry 352), with later decisions applied.
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
  side effects of DEV/QA work; explicit copy-from-PROD is read-only at its source.
- Runner rulebook CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md v0.7 remains in force for its existing
  scope. Short new edition before step 5 scratch rehearsal; no real-tree access or lottery sites.
  D:\DELETE_ME is the agreed scratch area. No runner execution or new privilege merely from this handover.

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
between trees. One lock per tree; no double-acquisition when invoking a job, manual stale-lock removal
only after ensuring no relevant job runs. No elaborate process inspection or recovery machinery.

I_AM_INSTALLABLE identifies marked software; stale mark reported, no deployment of unmarked bytes.
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
Install (including --show), Retire, Copy_From_PROD, Restore. Copy software into QA or data into QA/DEV
as separate explicit operations; no source writes. Backup before destructive replacement or retirement,
after jobs, on demand; plain ZIP maximum compression, omit .venv and lock. Backup failure stops
replacement but only warns after job. Restore checks archive's settings identify intended tree, renames
old tree aside, unpacks fresh, rebuilds venv; no mixing. Do not demand readback/hash proofs or recovery kits.

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

## 6. Current position at cutoff (entry 353)

Old design A/B/C accepted (EX_321/327/333) but never installed; set aside by owner entry 330.
No work on old slice D or old step 4. Simple scheme agreed entry 344; direct Claude code commits
to a_p_r_i_r_DEV on main approved entry 342. H-1 v16r1 installed RAT-62 entry 352; its statements
about reviewer still reading, flags and orphan question are superseded by entries 352-353.

Simple scheme step 1 complete: living tree copied, 258 files plus README and .gitignore, commit
4985468177213245ddd8c86c9e01579143417bba. Author cloud 207 tests, 2 skips. Owner built living .venv
(entry 346); top-level .venv retained until after reference use. No QA/PROD yet.

Step 2 code aedda2e, author cloud Python 3.15.0b4: accepted results and invented results compared
on committed engine (entries 348-349). Matching 21,716 forecasts, 21,636 scores, 82 second OV-1
lines, 1,376 report files (tree paths normalised); 161 tests pass. Frozen reference and new methods/
helpers unchanged; no independent execution by reviewer, no Windows equivalence yet. Nine choices
RAT-61 entry 350; later retirement correction entry 353. Owner pulled, no step-2 operational run.

Single reviewer reading completed and recorded entry 352: scientific equivalence supported.
Three findings accepted by Claude; targeted corrections in progress at cutoff, not claimed installed:
1. Global rebuild must remove generated results of absent methods too; otherwise their unchanged
   software can return and reuse results from an earlier engine under the new global fingerprint.
2. Regeneration removes obsolete generated reports (e.g. shortened results); no not-current machinery.
3. Repair malformed IN_PLACE_SINCE before reading status; bookkeeping must not stop a valid method.
Owner also agreed to drop retirement-draw forecast as well as scores (entry 353). Ordinary absent
method results left alone outside global rebuild and excluded from reports; other RAT-61 choices
stand. Full exploratory OV-1 direct comparison useful only if straightforward. No repeated full
comparison campaign or formal recheck requested. Follow actual subsequent commit and report; do not
treat a planned fix as completed. All three flags tracked (352). Orphan check dropped at step 4 (353).

## 7. Next work (each on owner's GO)

- Now: Claude completes targeted step-2 corrections and tests; record outcome. Step 3 on owner's
  GO: one updater in all trees, current reviewed src/results_master_v0_2.py as reference, remove
  Mode H remnants only; source/HTTPS/parse/game/draw/chronology/range/overlap and existing ledger
  comparison remain. Compare using invented pages, not a live website. Job invokes local updater
  unless --no-update. Review science/input correctness and destructive effects once.
- Step 4: simple settings, lock, deploy/retire/copy/backup/restore commands, job backup; remove
  living orphan check. Review one reading for irreversible damage. No old package workflow.
- Before step 5: report wording update (retired/method, exploratory second series, no old
  proof claim/not-current references). Comparison permits explicitly named wording normalisations,
  not scientific value differences. Short new runner rulebook before scratch rehearsal.
- Step 5: owner-authorised Windows scratch rehearsal and section 9 comparison. Compare equivalent
  game, method, input, draw and cohort, including forecasts/scores/OV-1 and reports. Frozen engine
  is regression reference, not independent proof that all hypotheses are valid. No real update
  by runner. Step 6: owner DEV first fill, then QA, then PROD creation and real operation on GO.
- Step 7: short how-to and handovers, CRLF conversion of two remaining LF records, three-way revisit
  operations manual (entry 343). Owner decides eventual frozen top-level disposition; do not remove
  it or its .venv prematurely. Step 8: research, new methods.
- Before new methods: independent suggestions on coding practices (entries 299-300), future-method
  priorities (entry 289; doc/Predictive_Randomness_Future_Method_Priorities_v0_1_DRAFT.md), roles
  and possible self-contained role-reversal trial (entry 292). Preserve owner reminders, E_45,
  E_59 and other speculative leads, all methods and NL-means R-002; do not assume a new priority
  order was adopted. Deferred profiling/acceleration after full implementation; measure first,
  then consider selective Cython/Numba/native numerical optimisation. OUTLANDISH_01 Powerball
  investigation closed by owner; Oz Lotto not required; no revival of historical work.

Recommendation at cutoff: owner ratifies this short handover and blurb, lets Claude finish the
targeted corrections, then authorises step 3 when ready. No further review of the handover's
historical machinery, and no owner-PC action authorised by this paper.

END.
