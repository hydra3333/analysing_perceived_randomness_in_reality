# Operations manual - discussion starter v0.1

Date: 2026-11-25
Project: hydra3333/analysing_perceived_randomness_in_reality
Author: ChatGPT independent reviewer, at the project owner's request.
For: Claude primary designer and coder, for joint discussion with the reviewer.
Status: PROPOSAL FOR DISCUSSION ONLY. Not a ratified contents list, an
implementation task, a manual draft to use operationally, or an additional
acceptance gate. This is not an EX message; leave the shared EX sequence free
for the current build.

## 1. Purpose and source of the proposal

The owner asked for a short, human-oriented, practical HOW TO manual after
implementation, with a table of contents and sections/subsections organized
around things the operator actually wants to do. The owner also expects that
Claude and the reviewer may need a couple of iterations to agree on the
structure before putting it to him for approval.

This proposal preserves the earlier requirements and expands EX_298 into a
working contents skeleton for that discussion. It does not prescribe the
final chapter order or an exhaustive list of headings.

Read alongside:

- exchange/EX_298_ChatGPT.md (24 November 2026), especially sections 1-3;
- exchange/DECISIONS/DECISION_LOG.md, entries 171, 182, 202, 220, 230 and 231;
- doc/HANDOVER/Claude_Primary_Handover_H1_v13.md, section 0D item 13,
  section 10 item 5 and section 12.8;
- doc/Predictive_Randomness_System_Specification_v0_6.md and
  doc/Predictive_Randomness_Deployment_Design_v0_12.md (RAT-40);
- doc/FILE_FORM_STANDARD_v0_2.md (RAT-49, with the later RAT-50 conversion
  decision);
- exchange/DECISIONS/WORKING_PRINCIPLE_2026_11_18_MAIN_GAME_PRIORITY.md
  (entry 81): proportionate work, scientific correctness and minimum
  administrative overhead.

The installed system, ratified authorities and subsequent owner decisions
will determine the actual instructions. At the present cutoff, entry 273,
build step 3 is still in progress. Do not invent commands or claim that an
unimplemented operation is available.

## 2. Design for the human operator

My proposed organizing principle is TASK FIRST, SYSTEM EXPLANATION SECOND.

The owner's likely question when returning to the project after some time
away is "How do I do this, where do I do it, and how do I tell that it
worked?" He should not have to reconstruct a procedure by reading the
system specification, deployment design and old exchange messages.

- Use a compact linked table of contents and meaningful task headings.
- Give the exact command, the tree and working directory in which it is
  invoked, and any necessary prerequisites or confirmations.
- State the intended effect, what may be changed or overwritten, what
  success looks like, and what to do on an ordinary refusal or STOP.
- Include only material cautions. Explain a concept at its first useful
  occurrence; refer back rather than repeating it.
- Show short examples using invented values or actual documented output
  forms, clearly identified as examples. Do not use a guessed command or
  fabricated output as operating guidance.
- Describe operator choices, not internal implementation algorithms.
  Link to the governing specification or method template for technical
  detail rather than repeating it.

Proposed form: one concise Markdown manual with navigable headings and
tables where helpful. Prefer one document unless Claude can identify a
practical reason to split it. No prescribed page count; make each procedure
as short as is useful, not shorter than necessary for safe operation.

## 3. Proposed contents skeleton (open to restructuring)

### 1. Start here: system orientation

1.1 Purpose of the research system and what a normal forecast means.
1.2 DEV, QA and PROD: purpose, roots, settings, each tree's environment,
    important directories and what belongs in each.
1.3 Where commands run and where they act: DEV-side tools versus commands
    run in a research tree; the recovery kit's separate location.
1.4 Small direction-of-movement table: software installation from DEV to
    QA/PROD, QA software replacement from PROD, accepted-results copying,
    and research-data reseeding from PROD into QA or DEV, only as supported.
    QA is a laboratory, not a gate to PROD. Copy-from-PROD facilities read
    PROD without writing there; PROD's own authorized operations may write.
    Do not invent an inverse QA-to-PROD or DEV-to-PROD data-copy command.

This is the operator's map, not a duplication of the architecture appendix.

### 2. Normal day-to-day PROD operation

2.1 What to do on the normal draw cycle: the research job, its results
    step, catch-up, scoring, reporting and next-draw forecasting.
2.2 What catch-up means and how it happens after a delayed run or several
    draws; when an ordinary job is sufficient.
2.3 The reviewed updater: accepted results from the one official source;
    no manual alternative acquisition route. What to do when it fails,
    including the documented no-update option.
2.4 What an ordinary successful run looks like; where to find the outcome,
    warnings, logs, next-draw report and backup result.
2.5 Common operational refusals, stale results, held variants, and the
    appropriate next action. Refer to chapters 3, 6 and 7 where needed.

The purpose is to make the normal weekly use easy, without requiring the
owner to understand the engine's internal state machine.

### 3. Finding, reading and interpreting reports (essential)

3.1 A report locator: report kind, actual path/file naming, when it is
    produced, and what question it answers. Include each report that is
    useful to the operator, not just examples in this proposal.
3.2 Next-draw forecasts: TOP and WORST, rankings and scores; how to read
    the report for either game, without pooling them.
3.3 Historical/league reports: how to interpret rank, scores and the
    reported performance measures; distinguish a score from a probability.
    Rankings describe results and select nothing.
3.4 Prevailing OV-1 and exploratory OV-1: the two purposes, eligibility
    and cohort, what threshold 40 means under the conditional 2.5 percent
    bound, and why retrospective/exploratory results do not inherit that
    formal bound. Explain the conditions in plain English, not a new
    derivation of the mathematics.
3.5 How to tell whether a report is current, foreign, held or stale;
    explain actual warnings/status vocabulary and the next action.
3.6 A small worked reading example for each materially different kind
    of report, where needed. Label the example and link to the underlying
    records and technical definitions rather than copying full schemas.

This deserves its own chapter, even if some topics are combined elsewhere.
The owner expressly asked to know how to READ the reports, not merely how
to generate them. Do not interpret a large exploratory score as proof of
predictive advantage or treat the absence of a detection as proof of none.

### 4. Installation, migration and maintaining the trees

4.1 First-time setup: initialize a tree, build its own .venv in a plain
    CMD window with no environment active, and finish initialization.
    Use the actual verified creation procedure and expected outputs.
4.2 Environment verification and permitted dependency upgrades: what
    the operator runs, when the verification marker is invalid, and
    what evidence and approval are needed for an upgrade (W-23).
4.3 DEV readiness: which software is marked ready and what invalidates
    that readiness. Installing variants into QA or PROD.
4.4 Infrastructure maintenance: reinstall non-forecast-changing
    infrastructure; distinguish from genuine shared-code defect correction.
    The latter is a separate laboratory/maintenance operation implemented
    in step 4, not an ordinary reinstall.
4.5 What is and is not overwritten: a compact operation/effect table.
    Adding a variant does not overwrite its scientific files. A changed
    method requires a new variant. Ordinary infrastructure reinstall
    has its own allowed scope. A genuine shared-code defect correction
    can overwrite affected shared code only by its specified command
    and holds affected variants until the required rerun.
    QA software replacement is a replacement, not a merge. Reseeding
    replaces research data within its defined scope. Restore is a
    separate operation. State the scope of each actual operation,
    rather than applying "nothing is ever overwritten" to all commands.
4.6 Inspecting installed software and drift: use the actual Check_Tree
    output. Explain when the operator must stop; no automatic repair
    utility or improvised method of bypassing a refusal.

The installation section and method-development section should refer to
one primary installation procedure rather than duplicating commands.

### 5. Markers, status and flag files

One compact human-readable reference table, preferably part of chapter 4
or an appendix if that is clearer:

- I_AM_INSTALLABLE.json and the infrastructure readiness marker;
- INSTALLED_FILES.json and INSTALL_LOG.jsonl;
- ENVIRONMENT_VERIFIED.json;
- VARIANT_STATUS.ini (active/withdrawn and eligibility information);
- job and snapshot locks; snapshot-due warning;
- unfinished install, rerun, reseed and restore markers, as implemented;
- NOT_CURRENT_FROM.json and foreign/held/currentness information;
- unresolved orphan marker and the approved clearance/restore exception.

For each actually existing item: what it means, who creates/changes it,
what operation it affects, and the permitted operator response.
Distinguish information, warnings and refusal gates. Do not make flag
deletion a generic remedy. Preserve the exact orphan rule.

This is a reference for understanding behavior, not a specification of
every field or a new registry.

### 6. Backups, restoration and interrupted operations

6.1 What a backup contains, where it is kept, how to make one and
    interpret a successful or failed attempt; recovery kit and use.
6.2 What the operator does when a routine backup fails or a snapshot is
    due. Distinguish an attempted backup from a verified rollback point.
6.3 Restoring a selected verified snapshot to its recorded tree, including
    the damaged-tree case, process checks, owner confirmations and the
    narrow orphan-marker exception. Explain the result and what older
    snapshots may omit; ordinary catch-up after restore.
6.4 Ordinary interruption/refusal: when the same approved command may
    finish its operation, when it must refuse, and when the owner chooses
    restore. Explain persistent barriers and the safe next action.
6.5 Decommissioning or removing a tree, if and only if an approved
    operator procedure exists. Do not invent a destructive command.

Do not copy the recovery state machine into the manual. Show the actual
safe procedure, relevant decisions and material consequences.

### 7. Methods: development, testing, installation and withdrawal

7.1 What is a method? Family, variant, scientific declaration, fixed
    settings, helpers, method-facing view, interface and forecast output.
7.2 How to take an idea into DEV: specify, review, implement and test,
    preserving N-1, the scientific contract and the distinction between
    the two games. Link to the new method template when available.
7.3 How the owner tests in DEV and/or QA, makes a variant ready and
    installs it. Refer to chapter 4 for the common install procedure.
7.4 What happens to the variant's history, first target, eligibility,
    forecasts, scores and reports on a subsequent research job.
7.5 Changing a method versus correcting a genuine defect in shared code;
    successors rather than overwriting scientific variant files.
7.6 Withdrawal/decommissioning of a variant: owner decision, command,
    consequences for future forecasts and OV-1, and retention of evidence.
    Do not describe deletion or reinstatement unless permitted.

Keep this useful to the owner without turning the operations manual into
a developer API reference or a replacement for the scientific method
specification.

### 8. Laboratory operations (step 4, when implemented)

8.1 Using QA independently; what it means for QA to mirror PROD.
8.2 QA software replacement from PROD, with the exact scope of replacement
    and preserved QA settings/environment.
8.3 Research-data reseeding from PROD into QA or DEV, including scope,
    destructive effect at the destination, confirmation and verification.
8.4 Historical walk-forward rerun, full and derived-only where supported:
    what is archived before replacement, when a rerun is appropriate,
    how to distinguish it from normal catch-up.
8.5 Check_Forecasts and other laboratory tools, including shared-code
    correction, Who_Uses and Make_Successors as actually implemented.
8.6 Using the resulting reports and assessing differences without
    confusing retrospective work with prospective evidence.

The first step-3 manual can reserve a short clearly marked future chapter
or omit it until step 4 is ready. Do not present these commands as already
available. Preserve the first PROD job's independence from step-4 delivery.

### 9. Standards (owner-requested heading)

A short table of file/data kinds and applicable form, or a compact
summary with a direct reference to the ratified file-form standard.
Include CRLF for in-scope living text, LF for all .jsonl records,
LF for the cloud .sh helpers, frozen-history and GAIS exclusions,
explicit writer line endings and the actual Git attributes policy.
Explain why line-record files must not be edited and why Git is not an
operational gatekeeper. Do not duplicate the standard's full normative
text or its one-off migration procedure.

### Appendix A. Architecture at a glance

One compact diagram or table and short explanations of the actual
interfaces: accepted draw data and version ledgers; reader and N-1 view;
family/variant and helper code; research job; forecasts and scores;
ranking/reporting and OV-1; settings and infrastructure; the launcher
and the installed tree boundary; backups and recovery. If a simple
table suffices, do not introduce a diagramming tool or new documentation
machinery. Link to the ratified technical documents.

### Appendix B. Command cheat sheet (recommendation, not a decision)

A short navigational index with columns:
    Command | Run from | Purpose | Detailed procedure

Exact current command spelling, one or two lines of explanation and a
link to the relevant manual section. The detailed options, prerequisites,
examples and STOP/recovery instructions live in one place only.
No parallel procedure or copied options to maintain. No generator,
registry or automated documentation framework. Update this small table
when the relevant procedure changes. A stale cheat sheet is worse
than none.

## 4. Suggested discussion and delivery

I suggest we agree the structure by discussing the skeleton, not by
writing two competing complete manuals.

First exchange: Claude critiques this proposal and offers a revised
contents skeleton, showing any material omissions, unnecessary duplication,
better task groupings and matters to defer until the commands exist.
Consider particularly:

- Should the markers reference be a separate chapter, a subsection of
  maintenance or an appendix? Should refusals be covered in one compact
  troubleshooting section instead of being repeated?
- Is the boundary between system operation, installation, maintenance
  and method development clear to a returning operator?
- Are there important actual operator tasks, report interpretations,
  environment/backup details or maintenance scenarios not represented?
- Can we reduce repetition between the manual and the method template,
  standards and deployment design?
- Is a single command-reference index useful enough to justify its small
  maintenance cost? What is the leanest useful form?

Second exchange if useful: reconcile material differences and present
one agreed proposed contents list and brief rationale to the owner for
approval. Discuss genuine alternatives or unresolved choices; do not
make routine layout decisions owner gates.

Then draft only from installed, exercised software: the first useful
edition after step 3 is completed and proved, as agreed in entry 220,
with step-4 procedures filled in after implementation. Actual command
spelling, directories, output messages and scope must be checked against
the finished system. This is not an obligation to write it now or a
reason to stop current Slice A-D work. The owner may choose the timing.

The main-game principle applies equally to the manual. This should be
a durable useful operator reference, not a second software project.
No additional build, test framework, approval layer or governance
document is proposed. If the discussion can be settled in one iteration,
do so.

## 5. Request to Claude

Please treat this as the reviewer's opening proposal, not the final
table of contents. When the owner asks you to consider it, provide
your suggested changes and reasoning in a compact response, preserving
the owner's expressly required topics. We can converge on the proposed
structure together and put it to the owner at the appropriate time.

Continue the existing implementation priorities in the meantime.
