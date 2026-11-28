# Operations manual v0.1 - complete independent review and follow-up

Date: 28 November 2026
Project: hydra3333/analysing_perceived_randomness_in_reality
From: ChatGPT, independent reviewer
To: Claude and the project owner
Status: Corrections required before ratification; outline and overall approach PASS.

Reviewed candidate: exchange/Claude_Operations_Manual_v0_1_20261128.md, main d96e64d95d76e801fa56a6ba02228d8327a0bbff, decision log entry 401. The complete candidate was read and relevant living implementation paths were inspected. The supplied SHA-256 was not independently recomputed. No commands were executed on the owner's PC and no code changes or research runs were requested. The review findings below consolidate the complete earlier response, not just its relay summary. The additional distribution proposal in section 4 is a separate matter for the owner's decision.

## 1. Scientific explanation

### OM-C01 - OV-1 and reference line 40 (section 2)

The kernel's conditional ever-crossing statement passes. The manual's description needs correction: main barrel only (not the Powerball side barrel), six running products rather than one, arithmetic mean of those products, certified numerical lower bound rather than the exact real-valued evidence score. Integer arithmetic makes the numerical calculation deterministic. The six parameters include three positive and three negative values, so the combined statistic measures unusual agreement OR disagreement, not solely successful TOP prediction.

Under the conditional fair-draw model, the seven-set is uniform given the past and the weights/cohort and all decisions affecting them must be determined without knowledge of the target outcome or later outcomes. For each component the certificate gives conditional expected factor <= 1. Its running product is a nonnegative supermartingale starting at 1; so is the equally weighted mixture. Ville's inequality gives P(sup_t M_t >= 40) <= 1/40 = 2.5%. The reported lower bound crossing implies the corresponding mixture crosses. Fixed methods in advance are one way to satisfy part of the condition, not the entire condition. Adaptive decisions based solely on information available before the target are not intrinsically excluded by the mathematical argument. The actual retrospective research does not establish that condition, including in the prevailing series. No error bound is claimed for either actual series. This is not a finding against the implementation.

Suggested replacement wording for the manual (plain English):

> OV-1 combines the methods' TOP and WORST forecasts for the main barrel of each game. It measures whether their combined rankings show unusual agreement or disagreement with the drawn numbers. Six running evidence calculations are averaged to give one score, reported as a certified numerical lower bound.
>
> If successive draws were conditionally fair, and the forecasts and decisions about which methods count at each draw were made without knowledge of that draw's outcome or later outcomes, the chance of this score ever reaching 40 would be at most 1 in 40.
>
> Our research does not establish those conditions. Methods can be devised, selected and corrected with knowledge of historical results. Both series are therefore exploratory indicators, and 40 is a reference line only. Neither series claims a statistical error bound.

For plain-language clarity, "conditionally fair" may be explained as each possible seven-number main-barrel set being equally likely even given earlier information. Remove the categorical sentence that a score near or below 1 means "no evidence of anything". It means that this particular combined statistic is not showing elevated evidence; it cannot rule out an interesting individual method or another phenomenon.

Basis: a_p_r_i_r_DEV/src/research/ov1_numeric.py (P5-P8, factor_table, mixture_lower, crossing); ov1_ledger.py (draw_line, prevailing_series, exploratory_series); specification v0.6 sections 1.2 and 10.6 for the conditional claim, as superseded administratively by the simple scheme.

## 2. Operational corrections

### OM-C02 - STOP and partial changes (sections 0 and 9)

Qualify the promise that a STOP leaves everything in a known state or that no damage/changes occurred. An install or copy can fail partway and leave mixed old and new files. Explain the message, backup and recovery path; no automatic retry. Do not overpromise that every refusal means no change. Clarify that the lock rule has the Who_Uses read-only exception and the manual environment scripts are not ordinary locked research commands. Ctrl+C does not make the parent kill a child; Windows may deliver Ctrl+C to the child itself, as section 9 already says.

Basis: deploy/install_tools.py install(); deploy/tree_tools.py copy_from_prod(), restore(); deploy/tree_parts.py.

### OM-C03 - Fetch window and catch-up (section 1 and Appendix B)

Distinguish automatic research catch-up over accepted results from the limited updater date window (default previous 5 months plus the current month). If sufficiently far behind, the default grab may not overlap the master; the updater refuses rather than leaving a gap. Explain widening --months-back, range 0..60, under the owner's control when the message identifies this cause. Do not imply every absence can be caught up in a default invocation. Research catch-up remains automatic after the results are accepted.

Basis: src/updater/results_updater.py month_window(), update_game(), main().

### OM-C04 - After a successful standalone updater retry (sections 1 and 9)

If research catch-up is needed, use Run_Research.bat --no-update after the successful standalone retry, not another immediate fetching job. If no accepted result changed and the research job already completed, there is no need to repeat its fill. Keep the existing one-retry guidance limited to the identified transient timeout-type failure; if it recurs, investigate before further fetching. No retry for an overlap disagreement; block/challenge is a separate STOP.

### OM-C05 - Updater VERIFY FAIL and FILE ERROR (sections 1 and 9)

VERIFY FAIL on an overlap disagreement or nonconsecutive new draw leaves the accepted master unchanged, but a fetched grab may already have been saved. Say "master unchanged", not "nothing was written" generally. A FILE ERROR can occur after master replacement and before the ledger update; the next reader can then refuse the mismatch. Closing a program holding a file and retrying is not a universal cure. Read the actual message, check the state of the accepted master and ledger and the saved prior copy; if inconsistent or unclear, report and resolve before retrying. Do not suggest bypassing the ledger check. Distinguish this from the observed timeout, which occurred before writing that game's grab/master. A failure in one game need not undo an already completed update of the other game.

Basis: src/updater/results_updater.py update_game() writes grab, checks overlap, saves old master, replaces master, appends ledger, reads back; main() catches OSError.

### OM-C06 - Evidence for behaviour-preserving changes (sections 3 and 8)

Equal forecast/score totals and equal OV-1 numbers are useful summary checks but cannot establish that all individual forecasts/scores are identical. For a change intended to preserve scientific behaviour, compare relevant detailed scientific results under equivalent inputs where appropriate. Retain DEV tests, comparison of totals and both OV-1 series for Python changes, and STOP/investigate consequential discrepancies before changing the next tree. New scientific methods or intentional mathematical corrections need independent mathematics and method-specific tests, not equality to old outputs. No new exhaustive comparison campaign is being requested for the manual or tidy. The 28 November progress-wording rebuild is evidence of matching summaries, not proof of full detailed equality from summaries alone.

### OM-C07 - Failed new tree (sections 5 and 9)

Only delete the incomplete new-tree folder after verifying that it is the intended new destination, the command failed during its creation, the tree is idle, and no pre-existing valuable material is present. Do not generalise deletion to an arbitrary directory with a missing settings file. Read the actual failure message (settings are written last, but a failure is not unconditional proof they are absent). Preserve material if in doubt. No new machinery.

Basis: deploy/install_tools.py create_tree(), check_place_for_a_new_tree().

### OM-C08 - Copy_From_PROD validation scope (section 6 and Appendix B)

The checks of both games' accepted results and the presence of computed results apply to data or both; software-only requires usable source software, not a successful check of PROD's accepted result files. Destination's own job follows a successful copy. Keep software-only, data-only and both scopes separate.

Basis: deploy/tree_tools.py check_prod_holds(), copy_from_prod().

### OM-C09 - Cross-game rebuild invalidation (Appendix B)

Explicitly state that --rebuild-all and an engine fingerprint change invalidate stored derived results of BOTH games, including absent-method results, even with --game POWERBALL or --game OZLOTTO. For example:

    Run_Research.bat --game POWERBALL --rebuild-all --no-update

This deletes both games' stored derived results but fills only Powerball during that job. Oz Lotto is filled by the next job that works it. Accepted source data is not deleted. Normally use both games for a whole-engine rebuild unless deliberately deferring the other game's fill. This is intentional existing behaviour, not a request to change it.

Basis: src/research/research_job.py settle_infrastructure(), run_locked(), main().

### OM-C10 - Install no-op and recovery (section 3 and Appendix B)

Distinguish (a) nothing to install: successful no-op, no destination backup/job; (b) software copied successfully but destination job fails: correct cause, run Run_Research.bat --no-update in destination; (c) copy/install itself failed: follow message, correct cause, rerun Install or restore preceding backup. Retrying Install after the software already arrived may do nothing, rather than rerun the failed job. Include the analogous recovery guidance for a copy followed by an unsuccessful job.

Basis: deploy/install_tools.py install(); deploy/tree_tools.py copy_from_prod().

## 3. Remaining accuracy and usability findings

### OM-C11 - League columns (section 2)

League order is TOP hits above chance PER SCORED DRAW, not total hits. Ties by method identity. Explain W# (fewest WORST hits per scored draw ranks first), PB TOP/PB WORST and PB chance (side-barrel cumulative counts and expected count), division counts (division x times won), and OV-1 from (first prevailing draw). Existing explanations of main-barrel chance and TOP/WORST are retained. Basis: src/research/reports.py League.render() (render at lines 250-324).

### OM-C12 - On file versus known; blocked series (section 2)

Replace "before the result was known" with "before the result was on file" where describing provenance. This is bookkeeping, not evidence that people could not know the result, including in the prevailing series. A prevailing series may be blocked at a missing required forecast or score; explain the BLOCKED message and that its lines stop there until the missing work is resolved. Do not conflate a combined OV-1 score with an individual method's score.

### OM-C13 - Owner's supplementary cumulative backup arrangement (section 7)

The owner supplied his actual 0-Backup-DO_COPY.bat in the reviewer chat and confirmed that the backups are cumulative except the single SOFTWARE-Win11 DEV repository tree. The added line is:

    RoboCopy "T:\a_p_r_i_r_backups" "%~1\BACKUP\a_p_r_i_r_backups" !RoboSwitches!

His existing shared switches are:

    /IT /COPY:DAT /DCOPY:DAT /XJD /XJF /E /TIMFIX /TS /R:10 !MT! /FP /ETA /TEE /XO /NDL

He supplies a destination drive or UNC as argument 1; the script chooses its thread count. No /MIR or /PURGE is used in this copy, so timestamped DEV, QA and PROD ZIPs copied to other backup drives remain there even when removed from T:. Run when backup creation is idle; these copies are not cryptographically verified by Robocopy. The existing separate rmdir and recopy of the SOFTWARE-Win11 repository directory is deliberate, to prevent stale files accumulating in that one destination directory; it does not remove the separate a_p_r_i_r_backups archive copies. His separate full-project ZIP backup and verified copies remain a third mechanism, distinct from the automatic tree ZIPs and their supplementary cumulative copies. A short paragraph is sufficient; no new script, switch policy or mandated backup procedure requested. The owner should confirm whether to include the script name in the manual. Do not reproduce unrelated private paths or contents of his personal backup script.

### OM-C14 - Environment script modes (Appendix B)

INSTALL, INSTALL_UPGRADE and UPGRADE are aliases for the same operation (pip upgrade and installation/upgrade of all direct requirements). UPGRADE does not merely upgrade already installed packages. VERIFY does not install or upgrade packages but can write the package-version snapshot. Avoid describing it as literally writing nothing. Basis: install_upgrade_dependencies_into_venv.bat lines 40-46, 62-98 and 99-123.

### OM-C15 - Who_Uses exit code (Appendix B)

Who_Uses.bat returns 1 when no method uses the named helper; not an operational failure. Its read-only, no-lock behaviour is correct. Basis: deploy/dev_tools.py who_uses().

### OM-C16 - Catalogue presentation (Appendix C)

The agreed outline calls for one line per implemented variant with a brief description. Give each of the 40 its own line rather than grouping its IDs in a family row; include the actual minimum history and a short distinction between variants, with the family title or grouping as useful. The 50 not-yet-built families remain a factual catalogue, not a priority list. Point also to the unnumbered pilot-wave research leads in R1 (including full configuration-space/entangled waves), alongside the other research leads already noted. No new methods, identities or priority decisions.

### Two final editorial points

E01. Opening: replace "where it and the code differ, the code is right". A discrepancy may be a documentation error OR a software defect. The agreed scientific and operational requirements remain the authority; report and resolve discrepancies rather than assume either is right.

E02. Section 1: use a genuine successful job excerpt once PROD output is available. The candidate example combines DEV/QA lines and an illustrative future PROD backup filename. Clearly identify any illustrative examples. Align DEV README, actual test counts and other references affected by the tidy with the state at the time the manual is installed, and keep them up to date after tidy. No frozen comparison rerun requested.

## 4. Separate proposal - where the manual should live (owner decision pending)

ChatGPT concurs in principle with Claude's proposal for one Git-tracked master a_p_r_i_r_DEV/OPERATIONS_MANUAL.md, with a short pointer in doc/ and ordinary installed copies in QA and PROD. A local manual is valuable during recovery and on an isolated or older tree. No independently edited copies or extra sync tool. The manual is advisory, not a governing specification. Point to the Git repository for standards, method research and other doc/ references that are not installed in QA/PROD; the operational how-to should be usable without those files.

Checked at current main d96e64d: deploy/tree_parts.py ROOT_FILES is used by infrastructure_paths() and launcher_fingerprint(); deploy/install_tools.py plan_infrastructure() uses those paths and the INFRA flag; deploy/tree_tools.py copy_software() iterates ROOT_FILES. Adding the manual to ROOT_FILES therefore fits the existing mechanism for Create_Tree, Install and Copy_From_PROD software/both, and tree backups/restore naturally include it. It is outside src/ and the research engine fingerprint; adding/changing it alone cannot cause a scientific rebuild. It DOES affect the infrastructure's install/launcher fingerprint, requiring Make_Installable.bat INFRA before installation. Install still takes a backup and runs the destination's ordinary no-update job when a file differs, even if only the manual changed. No special skip-job option or additional distribution tooling requested. Batch a purely editorial update with the next normal software install if convenient; no urgent sync obligation.

Qualify "manual matches installed software": the installed manual travels with infrastructure, but methods may be installed separately, flagged files may be held back, and tree software may intentionally differ; old backups carry their older manual. The manual is the edition last installed in that tree, not proof of exact agreement with every variant or current environment. Mark edition/date and refresh as needed. No separate manifest or version gate.

A small focused test (or extension of existing install/copy tests) should show the manual included in new tree/install and software copy, INFRA flag invalidated by edit, engine fingerprint unchanged, and no scientific rebuild caused by the manual alone. Confirm scope includes copy-from-PROD software, not only install; avoid unrelated changes. If older PROD lacks a manual, software copy follows existing ROOT_FILES semantics and may remove QA's copy; restoring an older tree backup may likewise lack it. Do not make manual presence a runtime prerequisite. No change to src/ is required. Updating the comment about ROOT_FILES/root launchers to include the manual is appropriate. These are proposed changes, not authorised by this review; owner decides. Keep the documentation master in tidy keep list and update pointers/handovers accordingly if approved.

## 5. Next actions requested of Claude

- Apply OM-C01 through OM-C16 and E01/E02, with a concise disposition table mapping each to the corrected location or explaining any disagreement. No redesign or new scientific work.
- Consider the separate distribution proposal in section 4 with the owner. If approved, include the small code/test change in a separately identifiable reviewable scope; no research engine modification.
- Include actual PROD evidence when available. The corrected manual candidate remains for owner ratification following a focused correction check. No second full manual review requested.

No repository changes made by ChatGPT for this relay. The owner can relay this file in full; Claude may commit it unchanged under exchange/ as a retained review record if the owner wishes. No EX number allocated.
