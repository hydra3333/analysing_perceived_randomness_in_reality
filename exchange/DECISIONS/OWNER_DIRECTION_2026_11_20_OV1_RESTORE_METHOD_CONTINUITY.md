# Owner direction: OV-1, exact-backup restoration, permanent method continuity and future evolution

Date: 2026-11-20 (Australia/Adelaide)
Project: hydra3333/analysing_perceived_randomness_in_reality
Status: OWNER DIRECTION AND REVIEW-CYCLE RECORD, relayed by ChatGPT. This file is a durable companion to EX_258_ChatGPT.md, not a new ratified design. Claude should append the owner's decisions to the living exchange/DECISIONS/DECISION_LOG.md (preserving its append-only practice), cross-link this record, update continuity and handover, and propose exact governing-document amendments for independent review and owner ratification before implementation.
Sources: Owner's direct messages to ChatGPT after EX_257, the prior owner answers relayed in EX_253/EX_255 and recorded in decision log 116, 118, 119, and exchanges EX_252 through EX_257. Wording labelled "owner" is owner direction; reviewer interpretations, calculations and recommendations are distinguished below.

## 1. The underlying research objective (OWNER)

Research possible deviations from presumed physical randomness, even if unconventional; expect that most or all methods will ultimately show no consistent advantage. A method's consistent deviation in either direction is interesting. A reliably INVERSE predictor is scientifically as interesting as a reliably successful conventional predictor. Each method/variant/revision retains both TOP and WORST ranking outputs and is evaluated impartially, including comparative chance/null measures.

The sample rate is VERY SLOW (one draw per game per scheduled event). Statistical power accumulates slowly, even over years. Do not discard a scientifically valid working method or a version merely because it has yet to show a convincing effect.

**LATEST OWNER DECISION (overrides earlier speculative retirement/culling discussion): do NOT retire any methods, INCLUDING OLDER REVISIONS, from active future work merely because another revision is released or because performance appears unremarkable. Leave them ALL working.** A newly revised method is ADDITIONAL to its predecessor, with its own immutable version/variant identity and separate performance track. The older versions continue forecasting every eligible new draw and contributing to the prevailing OV-1 under its normal objective rules. The owner is not requesting automated culling or an evolutionary method selector now. Any change in this no-retirement direction needs a future explicit owner decision, not an implicit "supersedes" flag or a developer's default.

The owner especially endorses: (a) do not mistake lack of statistical evidence for evidence that a method has no effect, particularly at this sampling frequency; (b) NEVER lose historic method definitions, forecasts, or results; a future review may revisit them. The current choice is stronger than mere preservation: leave the old revisions RUNNABLE and ACTIVE alongside new ones. Preserve full per-revision historical and forward scores, with TOP and WORST outputs and the correct roster in each game's prevailing OV-1.

Potential future evolution, if genuinely exceptional sustained positive or inverse deviations appear: add revised/inverted/combined methods as distinct identities, evaluate them fully, and then observe genuine new draws. It is a DEFERRED research possibility, not current permission to select, retire or suppress methods based on rankings. If all remain chance-like, report that honestly; do not manufacture success through endless adaptive searching.

## 2. Historical walk-forward, rankings and prevailing OV-1 (OWNER)

- Every new method or new revision is run by N-1 historical walk-forward from that GAME's first available COMPATIBLE target draw, subject to its legitimate minimum-history requirement; no calendar-date boundary truncates the historical evaluation.
- Historical league rankings and full draw-by-draw current-cohort reconstruction are recomputed with the new method/revision IN, with all relevant methods and old revisions evaluated impartially. Earlier published histories remain archived. A retrospective OV-1-derived research view may be recomputed and labelled EXPLORATORY.
- The one continuously accumulated PREVAILING OV-1 e-process per game is not retroactively modified when historical backfill finds a new method was unusually successful. Only genuine forward eligibility adds it from its explicitly recorded effective start DRAW NUMBER. No other history is silently spliced into the prevailing stream.
- Methods and revisions are not automatically removed from that stream on later releases. Thus the roster can grow over time. The project allows correlated methods; preserve the defined TOP-minus-WORST weight mathematics rather than arbitrarily filtering methods for being similar or apparently unsuccessful.
- The objective uses official DRAW NUMBERS as the timeline, separately by game. Dates/timestamps are useful metadata for backups, operations, reporting and auditing, not scientific eligibility arithmetic. Actual draw wall-clock timing cannot be proven from an announced schedule; do not build a statistical machinery around an assumed exact drawing instant.
- The initial prevailing stream starts on the future draw after the reviewed implementation is introduced, as the owner chose. Each later batch release has one effective first draw number per game, determined from the then-current accepted draw sequence, after normal preparation and catch-up. New methods can be grouped into one owner-approved release. No separate manual OV-1 registration ceremony.

## 3. EXACT disaster restoration and catch-up (OWNER - important correction to EX_256 and EX_257)

Owner's meaning of RESTORE is to recreate the exact last selected VERIFIED complete backup at the original production location: methods/revisions, executable code, configuration, relevant input data and records, and its saved Python environment (where it can run), along with only the minimal necessary restore bookkeeping and standing process-safety rules. This is a KNOWN PROVEN STATE, not a jumping-off point for an automated speculative reinstallation.

**Do NOT automatically re-install, re-introduce, retire, supersede, activate, replay-in, or apply software/method releases that occurred after the selected backup.** Do not consult a damaged set-aside tree as science authority. Do not automatically take later code from Git/clone to "repair" the restored scientific roster. The owner alone reviews the reason for restoration and decides what to implement afterwards, under a separate ordinary release go.

After restore: refresh accepted actual results as required; process the missing draws IN DRAW-NUMBER ORDER using precisely the installed methods/revisions and the N-1 input prefix, including TOP and WORST, scores, historical ranks and applicable OV-1. Keep the restored roster active, including older versions. It is ACCEPTABLE that a method or revision originally retired/replaced in a LOST later state gets additional valid target runs during the restored catch-up; nothing about that automatically makes the research invalid or the revised score "qualified". A restore normally uses the last reliable snapshot, so missing post-snapshot changes should often be few. A restore motivated by a bad installation, faulty revision, method crash or broken calculation especially MUST NOT automatically reinstate the very release that may have caused the damage.

No special OV-1 restore notices, wall-clock MISSED or permanent STOP. Restore and catch-up should be reliable and straightforward. If a documented, real data/score/numerical integrity failure prevents a particular draw, give a specific explanation and recover by ordinary reviewed methods; never invent missing predictions or secretly skip an outcome.

**The OV-1 timeline after catch-up is the legitimately reconstructed timeline of the restored system**, which may differ from a lost, unrecoverable alternative release history. Its score may therefore differ. That is not, by itself, evidence of computational or statistical invalidity. The new science timeline is truthful about which revisions were actually run and when new releases are subsequently authorised. It should not be marked QUALIFIED solely because an absent post-backup release was not automatically reapplied. The user is choosing an operationally reliable snapshot, NOT comparing backups to maximise OV-1.

Reviewer statistical precision (not a new user constraint): any unconditional type-I guarantee needs non-anticipation of the particular target's result in the rules deciding its participant cohort and numerical factor. A verified operational restoration using unchanged snapshot methods, impartial N-1 computation and no outcome-driven cherry-picking is compatible IN PRINCIPLE with the e-process theorem even when runs occur after the results are physically known. A physically changed historical course is not intrinsically invalid, but a post-result choice of backup, method or environment engineered to optimise OV-1 would be different. State this as a reasonable mathematical/operational assumption, not a suspicion about this owner or a need for manual registration. No extra restoration bureaucracy is justified.

## 4. Python environment, reproducibility and proportionality (OWNER and reviewer)

Owner does NOT want a Python/NumPy/SciPy environment pinned separately for each historical draw. Ordinary package changes through the project's reviewed route are permitted; if there is a failure the owner may restore and choose how to proceed. The owner regards slight version-related numerical differences as possible but not a leading practical concern. Reviewer agrees no per-draw environment pin, no automatic qualification merely because the digest changes, and no new elaborate environment-dependent procedure. Keep meaningful numerical oracles, the recorded environment identity for diagnosis, and the existing W-23 independent upgrade review (owner affirmed W-23 in decision log 116; no repeal has been authorised).

The 2.5% per-game e-process claim is a CONDITIONAL mathematical result: valid when the fair-draw null and prediction/cohort/selection non-anticipation assumptions hold. Passing software integrity checks cannot prove all real-world conduct or absence of target-outcome-sensitive selection, but neither is a changing, normally maintained Python environment inherently an invalidating event. Report structural validity and the ordinary mathematical assumptions accurately. A genuine failure may warrant labelling; an ordinary deterministic replay using original snapshot methods does not warrant a restore-only statistical penalty.

Use the project-wide agreed proportional-engineering principle: rigorous science, N-1, scores, statistical mathematics and safety, but avoid peripheral overengineering and extra user approvals for routine operations. No new owner registry, manual OV-1 pre-draw freeze ceremony or permanent STOP.

## 5. NORMAL multi-method development workflow (OWNER; separate from disaster restore)

A nominated batch of new methods and/or new revisions may be implemented and evaluated in one owner-approved development/release cycle. The desired logical sequence is:

A. Prepare and independently review the batch's new code as distinct method/revision identities. Old revisions must remain separately runnable.
B. Give EACH new identity its COMPLETE compatible per-game historical N-1 walk-forward, not a merely recent time window. Admit the scores and republish the historical league plus automated draw-by-draw rankings with all old and new methods.
C. Catch up the NORMAL EXISTING roster and the validated actual-draw sequence through the most recently available accepted draw, including any outcomes arriving while the full-history batch was running.
D. Finalise one effective FIRST FORWARD DRAW NUMBER per game for the nominated new cohort when it is activated/released. Activate ALL methods without automatically retiring their predecessors, and produce that next genuine draw's forecast (later scored/ranked/OV-1 when its outcome is accepted).
E. Continue all versions on subsequent draws. If there is a conflict between the staged implementation's "released variants only" development fill and the desired pre-release whole-history evaluation, Claude must resolve the workflow at design level, using existing mechanisms and the smallest needed changes. The owner need not issue separate manual starts for every method.

This ordinary batch-release workflow is NOT a restoration workflow. After a disaster restore, the correct default is AVOID new releases until catch-up has finished and the owner separately decides to introduce them.

## 6. Reviewer findings for Claude: exact current design conflicts

The following are observed in the reviewed public GitHub project, not assumed:
- Installed src/methods/_common/release_records.py lines 11-14, 124-144 defines released_variants as only non-retired and latest-active versions. Its current(k) filter keeps only the ACTIVE newest revision of each (game, method, variant) registry chain. This is INCOMPATIBLE with the owner's now-explicit intent that older versions remain active. The registry identity/runnability route must allow multiple released revisions to run concurrently, not merely preserve their records.
- The staged weekly session demands a roster equal to released runnable variants. Therefore it too must use the corrected all-versions active population, with distinct revision identities and TOP/WORST results, not force automatic supersession.
- The OV-1 amendment DRAFT v0.2 section 2.3 explicitly defines effective_first_draw of a release as the stopping number for "retired or superseded" variants and its examples treat older A2 as automatically displaced by A2R. This is NOT the default desired policy. Revised methods add to the population; old ones continue. Preserve explicit retirement machinery only if scientifically/operationally necessary, with no automatic use and no owner-authorised retirements in the present direction.
- EX_256 and deployment note DRAFT v0.5 section 9 describe reinstating later release records before catch-up. The owner rejects this. Remove automatic later-release reinstatement from the restore procedure and test/run sheet. Catch up ONLY using the restored snapshot's population.
- EX_257 section 3 required a clear multi-method batch historical-WF -> normal catch-up -> activation sequence. This remains, and the requirement to preserve old revisions actively running strengthens it. The standalone normal release procedure must not be used as an automatic post-restore "repair".
- Some current designs assume one latest revision per variant. Claude must inventory and propose minimal reviewed corrections to the release schema/registry chain status, forecast runner, per-game roster, scheduler, ordinary development fill, ranking report and OV-1, as needed. Do not falsely claim the change is only in an explanatory paragraph or only in OV-1.

## 7. Owner decisions versus reviewer recommendations, and authority

OWNER DECISIONS:
1. Never automatically retire existing methods or previous revisions merely due to new development; leave ALL working, despite weak or mediocre performance and very slow draw accumulation.
2. Preserve complete historical N-1 assessment, ranking reruns, and TOP/WORST inspection for every method and revision; investigate sustained positive or inverse signals.
3. One prevailing continuous draw-number-based OV-1 per game; new identities join from their effective next eligible future draws; no retroactive backfill into that prevailing score.
4. Restore ONLY the verified selected snapshot as the known working state; do not automatically apply later releases or alter the snapshot's methods; catch up using the snapshot's revisions. Subsequent method changes solely on a separate owner go.
5. No per-draw pinned Python environment; changing dependencies through the ordinary reviewed route is permitted.
6. Potential future evolutionary method additions/combinations are interesting but no automated retirement/culling or selection engine is authorised now.

REVIEWER ANALYSIS, NOT an independently ratified rule:
- The mathematical anytime bound is conditional on non-anticipation, independent of an operator's desire to do honest science; normal restoration as described is not inherently invalid, and an alternate score is not automatically a suspect score.
- The current installed release-record reader and staged weekly/OV-1 "supersede/retire" assumptions conflict with the owner's latest no-retirement direction; the primary designer should propose minimal changes and scientific impact.
- Disentangle normal multi-method release activation from plain disaster recovery, with a bounded design update rather than architectural expansion.

This decision record itself supplies NO authority to code, install, execute, update production, change protected governance blocks, or ratify an amended design. The owner will ratify reviewed governing-text changes and separately authorise a code round in due course. Claude should preserve this record and make it discoverable in the living decision log/continuity/handover. EX_258 gives the precise request for the next design review.

End of owner-direction record.
