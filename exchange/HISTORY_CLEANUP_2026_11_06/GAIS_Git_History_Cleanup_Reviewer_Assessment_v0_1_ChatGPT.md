# GAIS Git History Cleanup - Independent Reviewer Assessment v0.1

Date: 2026-11-06
Project: hydra3333/analysing_perceived_randomness_in_reality
To: Claude (primary designer / proposed cleanup lead), via project owner
From: ChatGPT (independent reviewer)
Subject: Focused review of the proposed 27-commit limited-history rewrite and cutover

## 1. Disposition

**APPROVE THE LIMITED-REWRITE METHOD IN PRINCIPLE; RECHECK BEFORE ANY LIVE CUTOVER.**

This is an assessment of the owner's summary of Claude's rehearsal, not independent access to Claude's mirror, command transcript, commit-map, source inventory, or output archive. The owner has approved Claude to LEAD the cleanup. This review does not itself approve a force push, tag/branch changes, local garbage collection, or destruction of locally retained Git objects. No project source edits, scientific runs, or holdout access are authorised by this review.

The limited approach is strongly preferable to a whole-history rewrite IF the reported invariants hold: GitHub-derived history about 85 MB packed; rewritten comparison about 45 MB packed; 27 changed recent commit identities starting at 54d161f; around 390 preceding commit identities retained; latest source tree byte-identical; nine earlier signed commits retained; fifteen rewritten signed commits necessarily become unsigned. The 982.99 MiB local packed object figure cannot by itself be assigned to GitHub-reachable history or deleted safely.

## 2. Reported evidence: accepted provisionally, not independently verified

- Original current HEAD: 6b99029 (full object ID to be recorded).
- Scope: git-filter-repo --refs 54d161f^..main, removing only the historical y-cruncher tree, ycruncher_digits placeholder, and two approximately 1 MB .bin files.
- Claimed: old/new HEAD^{tree} are exactly equal; only final 27 commits changed; all earlier ~390 commits preserved; 15 signatures lost and 9 preceding signatures preserved.
- Claimed: remotely mirrored packed size 85 MB -> 45 MB, rather than the owner's 982.99 MiB local pack storage.
- Proposed: owner makes bundle backup; Claude publishes rewritten history to temporary branch; owner validates empty diff and uses force-with-lease to replace main; owner aligns local main with soft reset; Claude verifies and commits crosswalk.

These are plausible and technically coherent, but the absence of precise IDs, references, and outputs makes final cutover approval premature.

## 3. Required corrections and evidence before cutover

**B01 - Complete and preserve the crosswalk BEFORE the force push [BLOCKER / RECHECK].**

Produce complete full-length old/new commit IDs for all 27 rewritten commits, plus the unaffected boundary parent, old full main SHA, proposed new full main SHA, root tree object SHA, git-filter-repo command/version, and the exact paths filtered. Export the git-filter-repo commit-map and ref-map (including null mappings, if any), plus a human-readable interpretation. Provide the crosswalk to the owner as a separately retained, hash-verified file OUTSIDE the repository before changing main. An in-repository crosswalk may be committed under the authorised path later, but must not be the sole or first copy. Consider the possibility that archived project evidence contains old SHAs, including ratification/exchange records, experiment provenance, and commit-identified design installations. Do not silently replace historical citations with new IDs.

**B02 - Verify the removal set is complete and narrowly scoped [BLOCKER / RECHECK].**

The owner's request includes historically committed .bin files AND large intermediate decimal-digit data, regardless of file extension. Inventory historically reachable blobs by actual size and historical path across ALL relevant refs and report the largest candidates, including .txt, .dat, .csv, .zip and other formats. Identify the TWO .bin paths and exact sizes, the y-cruncher folder, and the placeholder. Demonstrate there are no overlooked large intermediate digit files at other locations or in earlier commits. Do not remove a large archival ZIP, scientific evidence, or other object solely because of its size; any further target requires an explicit path-specific owner decision. If the current four deletion groups are complete, say so with evidence. If not, revise/rehearse and RECHECK.

**B03 - Account for all Git refs, PRs, collaborator copies and old-history retention [BLOCKER / RECHECK].**

Provide old/new refs inventory: main, remote branches, tags (especially signed/annotated tags), GitHub pull-request refs, and temporary/backup branches. Verify none of the original 27 rewritten commits are accidentally left reachable by an old branch or tag on GitHub after the intended cleanup. Partial --refs rewriting intentionally mixes old and new history, retains old refs/reflogs in some situations, and does not itself perform final GC. Determine the status of open PRs, collaborators, automations and disposable clones; freeze writes during the cutover and prevent old-history merges/pushes that would reintroduce removed blobs. Do not promise GitHub will immediately reclaim or make old blobs permanently inaccessible: caches/PR refs/forks can retain old objects; GitHub generally does not purge non-sensitive data just for size reduction.

**C01 - Record explicit acceptance of signed-commit consequences [CORRECTION; owner decision].**

List each of the 15 affected originally signed commits, with old and new SHA, old signature status, and the reason a new signed replacement has not been produced. Present the owner with the explicit trade-off: 15 signatures will be lost; 9 earlier signed commits remain untouched. Owner authorisation to have Claude LEAD the task should not automatically be interpreted as a waiver of the cryptographic signing consequences. Confirm acceptance before cutover. Also check signed tags and any signature-validation gates.

**C02 - Use an explicit, pinned expected-value force-with-lease for main [CORRECTION].**

Freeze at a known full old main SHA. Re-check actual remote main immediately before replacement; abort rather than proceed if it changed. Perform only ONE owner-executed update of refs/heads/main, with an explicit lease of the form '--force-with-lease=refs/heads/main:<FULL_OLD_MAIN_SHA>' and an exact '<FULL_NEW_SHA>:refs/heads/main' refspec. Do NOT use --force, --mirror or an unqualified --force-with-lease; do not overwrite unrelated refs or tags. Detect branch protection/ruleset constraints in advance and restore any temporary rule change afterward. The temporary branch is not cutover approval.

**C03 - Make tree equality, reachability and index safety mechanical [CORRECTION].**

For the rehearsal, record:
(1) old HEAD^{tree} and new HEAD^{tree} IDENTICAL;
(2) old pre-rewrite parent (= 54d161f^) preserved as EXACT SHA and ancestor of new main;
(3) 27 and only 27 commit IDs changed, with the full crosswalk;
(4) current main retains all intended tracked files; filtered historical paths absent from proposed rewritten ancestry;
(5) same-history-size measurement methodology (same refs, pack/gc policy, units) before/after;
(6) optional code/build/test validation only if authorised separately.

After owner cutover and a fresh fetch, the owner's working copy must be CLEAN (tracked index and working tree) before using 'git reset --soft origin/main'. First compare the full old/new Git TREE IDs in the owner's clone and verify origin/main is precisely the preapproved rewritten SHA. The '--soft' mode leaves BOTH index and working tree untouched; if trees match, index should remain clean. Do not use --hard. Ignored large local files should remain untouched; this is to be independently checked by path/metadata, not by loading large files into chat or traversing protected scientific data.

**C04 - Separate backup, rollback and local garbage collection [CORRECTION].**

Before rewriting main, make and VERIFY a complete reachable-history bundle with refs, store it outside the active repository, and preserve an offline copy of the crosswalk and approvals. A Git bundle alone does NOT preserve unreachable objects and all reflog-only objects in the owner's older .git database; therefore preserve a separate physical backup of .git or explicitly inventory and accept loss of such local-only material before running 'git reflog expire' or 'git gc --prune=now'. Do not perform aggressive GC until the cutover, local reset, crosswalk storage and downstream sync have all passed independent checks. Keep a documented conditional rollback; rolling back main would reintroduce old blobs and must be a new owner decision.

**C05 - Commit timing and governance [CORRECTION].**

Freeze new main commits and GitHub-changing actions for the cutover window, including routine exchange commits from Claude, unless the owner explicitly approves a controlled exception. Claude's temporary test branch must have an explicitly authorised name/scope and must not be pushed to main. The post-cutover crosswalk commit can create a new descendant HEAD; distinguish this later documentation commit from the pre-cutover tree-identity test and crosswalk. Verify the independent reviewer and owner have had access to the complete pre-cutover evidence. Preserve standing process-safety protections. No lottery outcome files or experimental data need to be accessed to do this Git metadata work.

## 4. Proposed safer exact order (approval gates)

Gate A: Claude supplies the pre-cutover package (commands, version, path inventory, original/new full SHAs and trees, changed commits/signature impact, size methodology, commit/ref maps, remote refs/PRs inventory, future commands, abort/rollback). Reviewer independently checks; owner explicitly accepts signature loss and precise deletion scope. No live rewrite yet.

Gate B: Owner verifies offline bundle and safe backup of local .git, captures original main SHA, and establishes a quiet/frozen window. Stop if old main has changed or collaborator refs could reintroduce unwanted history.

Gate C: Claude publishes the already-reviewed rewritten candidate to one authorised temporary branch. Owner fetches and verifies proposed SHA and identical tree, remapped 27 commits, unaffected boundary, and filtered-history criteria. No main update if anything differs.

Gate D: Owner performs exactly one pinned force-with-lease update of main after fresh remote check; records actual response and new remote SHA. No --mirror and no blind force.

Gate E: Owner fetches updated main, independently verifies its SHA/tree and clean local state, then performs a documented soft reset to it (no alteration to local working files) and checks status and ignored artifact presence. Claude independently verifies the new main, then adds the reviewed crosswalk through its authorised exchange path, if permitted by owner. Other clones are instructed to re-clone or update safely, never merge the obsolete 27 commits back into main.

Gate F: After independent PASS, owner may conduct a separate, safe audit of unreachable local Git objects, then explicitly approve any reflog expiration/garbage collection. Remote post-GC size and leftover refs are measured but not guaranteed. Closeout records exact old/new SHA, measured results, exceptions, new crosswalk file/commit, and affected old citations.

At ANY STOP: leave owner working files/ignored GAIS data unchanged, retain backups and crosswalk, do not attempt automatic destructive recovery or unreviewed retry. The owner decides next action.

## 5. Additional OUTLANDISH follow-on, not a precondition to cutover

The owner separately requests a final handover to the other ChatGPT OUTLANDISH development chat AFTER cleanup. It will cover the GAIS relocation from src/GAIS/ to root-level GAIS/ (alongside src/), current ignore rules, history-cleanup results, and a recommendation for a dedicated large/generated-data directory under GAIS/OUTLANDISH_01/ with a .gitignore exclusion. All related processes should write/read/move large/intermediate generated files there and perform a shared, mandatory exit-time audit for large files elsewhere; define threshold/exceptions and handle crashes separately. This is a post-cleanup implementation proposal, not permission to modify the OUTLANDISH programs now.

## 6. References independently checked for Git semantics

- git-filter-repo manual (partial --refs and commit-map): https://github.com/newren/git-filter-repo/blob/main/Documentation/git-filter-repo.txt
- GitHub on history rewrite side effects, signatures, PR refs and data persistence: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
- git-push explicit --force-with-lease=<refname>:<expect>: https://git-scm.com/docs/git-push
- git-reset --soft index/working tree semantics: https://git-scm.com/docs/git-reset

Reviewer conclusion: method PASS IN PRINCIPLE; LIVE CUTOVER HOLD until B01-B03 and C01-C05 are resolved and presented for focused independent RECHECK. The project owner remains the final authority for force-push approval and any destructive local Git maintenance.
