# One repository tree tidy - consolidated agreement and outstanding actions v0.1

Date: 28 November 2026
Project: hydra3333/analysing_perceived_randomness_in_reality
From: ChatGPT, independent reviewer, for Claude and the project owner.
Status: AGREEMENT IN PRINCIPLE, WITH OUTSTANDING ACTIONS. Not ratified; not authority to delete or run anything.

## 1. Purpose and relationship to earlier papers

This is the evolving record of the agreement between the two AIs, including the owner's latest direction about
preserving valuable material in exchange/. It is intended to be committed by Claude under exchange/ and retained
in the living tree, not to become another disposable numbered exchange.

Basis:
- Decision log entries 394 and 395; repository main checked at 6d0ba88cea89e6abec58de6af815e64fffcb91c3.
- Claude_Tree_Tidy_Inventory_And_Procedure_v0_1_20261128.md (at that commit), independently read; supplied copy
  SHA-256 verified as ef4b1d1db1342df2e12ea2b4aaba06369dc66ffb7e8476929c840bdede3a078a.
- ChatGPT's subsequent review in the owner chat (four corrections C01-C04), and the owner's subsequent instruction
  that useful material in exchange/, notably the decision log, must not be lost.

Claude's inventory and procedure v0.1 remain the detailed starting proposal. This record supplements them and
captures the agreed changes for the next candidate. Where there is a difference, incorporate the clarification
here into the revised candidate before ratification. The earlier ChatGPT history-reset discussion proposal is
withdrawn, not an alternative implementation plan.

## 2. Agreed objectives and scope

1. Retain Git history in its entirety and retain the existing GitHub repository, identity, URL, permissions,
   secrets and configuration. No history rewrite, force-push, replacement repository or old-history deletion.
   Ordinary git gc is optional, for the owner, after backup. Claude measured 68 MB packed versus 63 MB as one
   commit, only about 5 MB saved by a reset; the owner's .git was 95 MB. The cost in historical references is
   not justified. The 1.5 GB working tree is predominantly untracked material, not Git history.
2. One consolidated tidy, after QA and PROD are established and their first fills are accepted. QA is next;
   do not interrupt or delay that work for the tidy. All future software development is in a_p_r_i_r_DEV;
   documentation and governance records remain in their appropriate locations.
3. Preserve all scientific work, decisions, method ideas, useful references, unresolved matters and evidence.
   Reduce obsolete operational and administrative clutter. Ease of continued research is more important than
   maximising the number of files removed or disk space saved.
4. Retain the original results/ tree, including sealed Mode H records, without changing any byte. Retain all
   current living source files byte for byte. No tidy-related engine, method, updater or launcher changes and
   no unnecessary research rebuild. QA and PROD software/data are not targets of the tidy.
5. Push a clearly named annotated tag before the tidy (Claude's before_tidy_<date> convention is fine).
   Check the peeled tag resolves to the intended pre-tidy commit. All removed tracked files remain retrievable
   from Git history; retain a short ARCHIVE_INDEX.md with retrieval examples, tag, commit and inventory link.
6. An exact, reviewed removal inventory and owner ratification (anticipated RAT-69, subject to numbering at
   the time) are required. Separate owner operational GO is required when the prerequisites are met. A failed
   check means STOP and report, not proceed or automatically undo anything. No generic git clean -fdx.

## 3. Retention policy: exchange/ and other useful material

The owner has specifically emphasised the value of material in exchange/, especially the decision log. The
previous agreement to remove old exchange material is therefore conditional on retaining useful contents. A
file's EX number, date, location in a work-package folder, or historical status is not in itself a sufficient
reason to remove it. The tag is a historical archive, not a substitute for keeping material useful to future work
readily accessible in the current tree.

### 3.1 Explicitly retain

- All of exchange/DECISIONS/ (complete decision log and owner's decision records, not an abridgement).
- exchange/CONTINUITY_NOW.md, exchange/OWNER_REMINDERS.md, exchange/OWNER_ROADMAP.md, exchange/README.md.
  The agreed later continuity-page simplification is permitted; it must not discard live obligations or ideas.
- The agreed simple scheme and its supporting discussion papers (the eight 26 November papers in Claude's
  keep list), the operations-manual discussion, this agreement, the tidy proposal and successors, and the
  exact ratified removal inventory. The archive index is to point to the inventory.
- Any other older EX message, attachment, work-package document or research note containing worthwhile
  scientific ideas, mathematical reasoning, unresolved questions, deferred proposals, owner requirements,
  or useful evidence not adequately and accurately preserved elsewhere in the retained material.
- The living a_p_r_i_r_DEV (subject only to the explicitly agreed comparison-tool/test retirement and
  documentation changes), original results/, runner's whole folder including old tasks and reports,
  root CLAUDE.md, .claude/settings.json, .gitattributes, .gitignore, LICENSE, and .vscode (see C02).
- Current handovers and their blurbs; coding practices and file-form standards; scientific specifications
  and method designs, R1/R2/R3, errata, ranking measures, game rules and source references; future-method
  priorities, the deferred performance proposal, GASI_thought_experiments, and newest ratification register.
  Claude's section 3.1 doc keep list was accepted in principle after checking the actual doc directory and
  selected old E1/E2R designs. No specific extra doc file was requested in that review; the protection for
  useful material applies equally to doc/ and exchange/. NL-means R-002 is substantively retained in
  OWNER_REMINDERS. Keep current scientific text, not superseded operational instructions as authority.

### 3.2 Candidates to remove from the current tree, subject to P1

- GAIS/ at the consolidated tidy (the separate investigation is finished), review/ duplicates and old review
  copies, superseded documents and obsolete implementation designs, completed EX correspondence and package
  copies that have no remaining unique useful contents. Preserve exceptions identified under section 3.1.
- The frozen first-system root src/, tests/, deploy/, archive/, launchers, environment scripts, obsolete root
  requirements/settings examples and tracked source_data/ and transitory_data/ stubs, after dependency checks.
  The two frozen comparisons have served their purpose; no current operational engine depends on the old one.
- Only owner-approved and backup-verified untracked leftovers, dealt with separately by the owner, not Git rm.

Do not silently discard worthwhile material to meet the earlier numerical target of 4,599 removed / 425 retained
files. That count was provisional at 59f7a31 and will change as the inventory is refined. A conservative pass over
exchange/ and other removal candidates should identify additional keep exceptions. Keep a document when in doubt;
there is no need to expend disproportionate effort proving that every old document is redundant. Do not duplicate
or rewrite useful historical material merely for the sake of tidiness. If its substantive contents already exist in
a retained document, the original can be archived by tag. Otherwise retain the original, with necessary context or
attachments. Ask the owner about any material whose value is genuinely uncertain rather than deleting it by rule.

## 4. Living software, tests and scientific verification

Agree to retire a_p_r_i_r_DEV/deploy/compare_with_frozen.py and compare_updater_with_frozen.py, the six tests in
test_research_compare.py and the two tests of TheSameAsTheFrozenUpdater in test_research_updater.py. The other
25 updater tests use invented pages and trees from the latter tool: preserve the necessary helpers (make_tree,
InventedPages, page_text, invented_draw, load, HELD, TODAY) unchanged in a tests/ fixtures file, with imports
adjusted. Expect 280 -> 272 tests at the reviewed baseline; recheck counts against the actual pre-tidy tree.
Run the remaining suite, retaining all independent tests including the no-real-browser safeguard. Do not run a
real updater for this check. Confirm no living dependencies on retired files remain.

No src/ file is to change, including the updater comment naming the retired comparison tool. That comment can be
corrected at its next substantive change. The Git tree object of a_p_r_i_r_DEV/src and the original results/
must match the pre-tidy tag after each principal commit. This protects tracked bytes; the owner's subsequent
local no-update run checks that local fingerprints have not changed either.

For future behaviour-preserving changes, compare relevant detailed before/after results; a rebuild-equals-before
check is not a universal scientific proof. Intentional scientific corrections and new methods require independent
mathematical verification and method-specific tests. Preserve strict N-1 isolation, correct scoring, separate games
and same-model TOP/WORST. No fresh frozen-engine comparison campaign is needed for the tidy.

## 5. Four review corrections to Claude's proposed procedure

C01 - P0, first fills: compare forecasts and scores for identical methods, inputs and targets, and comparable
all-draw OV-1 series. The prevailing OV-1 series may legitimately differ because of the local establishment
boundaries; compare it against the appropriate local cohort. Do not artificially align the real trees, change
establishment dates or impose a new scientific acceptance mechanism merely to obtain equality.

C02 - P4, VS Code: the actual retained .vscode/settings.json points both python.defaultInterpreterPath and the
custom CMD activation profile at the retiring top-level .venv. Change those two paths only to the living DEV
.venv: ${workspaceFolder}/a_p_r_i_r_DEV/.venv/Scripts/python.exe and, in JSON with escaped backslashes,
${workspaceFolder}\\a_p_r_i_r_DEV\\.venv\\Scripts\\activate.bat. Preserve the owner's existing terminal profile
and other configuration. Add .vscode/settings.json explicitly to the permitted P4 modifications.

C03 - P5/P6 and rollback: the pre-tidy tag is only a tracked-file archive. Verify the new full-tree backup
contains the specific untracked material to be deleted. List full paths for manual deletion by the owner, with
no broad cleanup of a drive or parent folder. Especially protect DEV's environment, settings, accepted source
and results, and the real QA/PROD trees and backups. Any scratch cleanup is limited to expressly identified,
inactive disposable folders and is not implicit authority to delete D:\DELETE_ME\ as a whole. Rollback must
include the associated rulebook, documentation and VS Code changes if applied, not just P3/P4. Revert the relevant
commits in reverse order with the owner's authority; restore deleted untracked files from backup if needed. No
history rewrite. If other work has intervened, review conflicts rather than reverting unrelated changes.

C04 - P5, owner's local check: after a clean pull, Run_Research.bat --no-update in DEV should show no REBUILD,
zero newly written forecasts and scores, unchanged prevailing OV-1 values and establishment records, and a
successful backup, assuming identical accepted data and software. A no-update check must not fetch new results.
If a check fails, STOP and investigate before deleting untracked files.

## 6. Runner rulebook v0.9

Agree in principle to using the real DEV Python as the runner's interpreter instead of keeping an obsolete
second top-level environment. Use the full path to a_p_r_i_r_DEV\.venv\Scripts\python.exe with -I -B; no
activation, pip, install, upgrade or modification of DEV. Authorised scratch computations keep their working
folder, TMP, TEMP and outputs in their permitted scratch location. Operational scratch trees retain their own
venvs for operational commands; the existing permitted scratch-environment creation scripts remain permitted
only in their defined scratch context. Preserve all prohibitions on real operations, real results fetching,
unauthorised reads/writes, and process termination. The earlier T031 interpreter exception is precedent for
read-only interpreter use, not general authority to run real-tree programs. Retired task instructions are
historical evidence, not executable authorisation. Retain the runner's entire folder and reports.

Issue the short revised rulebook as a separately ratified candidate before the old environment is deleted.
Check current runner instructions, task examples and launch paths for stale top-level interpreter references.
Retain the owner's existing safety permissions; any necessary permission change must be identified and reviewed.

## 7. Backup evidence and operational boundary

The owner reported successful full-repository ZIP backup on 28 November 2026, 09:23:03 to 09:46:08, with
archive integrity read and SHA-256-verified copies on F:, I: and Y: from U:. Filename:
analysing_perceived_randomness_in_reality_2026_11_28_09_23_03.zip
SHA-256: 0DA6DF03A81A1C4F3446CA6F4AE142CEE4221E776E9FED9EABF605167D49B373
This is reported owner evidence, not an independently executed restoration test. Keep these copies. Make and
verify another full-tree backup immediately before the tidy, and check relevant untracked entries are present
before deletion. Where practical demonstrate retrieval of a representative file to a separate safe location;
never extract a trial restore over the live tree. Do not regard an archive hash as proof of source completeness.
The Git tag plus the verified backup provide recovery paths; no operation has an unconditional guarantee.

## 8. Actions requested of Claude

1. Commit this agreement under exchange/ as a retained discussion record, unchanged, and record its status in
   the decision log. It is not ratification or permission to carry out the tidy. No numbered EX is needed.
2. QA and PROD remain the immediate priority. Continue the existing agreed deployment sequence with the owner.
3. Update the tidy candidate to incorporate sections 2-7, including all four corrections C01-C04. In particular,
   reconsider the exchange/ removal rules in light of the owner's latest instruction. Identify unique useful
   material, unresolved/deferred work and scientific reasoning that would otherwise cease to be readily accessible.
   Retain questionable files rather than over-engineering an exhaustive archival exercise. Provide any additional
   keep exceptions by name and a short reason; propose alternatives if there is a better way to preserve them.
   Check the doc keep list, active handovers/roadmap/reminders, runner and README references for live dependencies.
4. Prepare P1 against the actual tree to be tidied, with exact tracked paths, counts and sizes; include the
   test/fixture changes and documentation amendments as explicit changes, not hidden in directory-wide rules.
   Review removal candidates against the retained-material policy. Provide the short exact permitted change
   list for P3/P4 and any subsequent rulebook/continuity work, and refresh if the baseline changes. Keep P1.
5. Send the revised proposal and P1 list to ChatGPT for independent review. If there are further questions,
   discuss and resolve them with ChatGPT; record agreed changes in the next version of this record or a clearly
   identified consolidated successor. Do not treat the present agreement in principle as final approval.
6. After both AIs agree, seek the owner's explicit ratification of the final proposal and exact inventory.
   Wait for the prerequisites and separate operational GO. Confirm no runner or research work is active, backup
   is verified, and the owner's working tree is clean before cutover. Push and verify the annotated pre-tidy tag.
7. Only then execute the agreed P3/P4 tracked changes and reviewed checks. Update/ratify rulebook, owner pulls
   and checks DEV, owner approves and performs the exact untracked cleanup, and refresh both handovers and
   continuity. Follow P0-P7 as revised. Record results and any STOP, without expanding scope.

ChatGPT's next action is to review Claude's response, revised candidate and exact P1 list. The owner's immediate
next action is QA establishment, not deletion. No repository modification, code execution, test run or deletion
has been performed by ChatGPT in preparing this paper. This is a static design agreement only.

END.
