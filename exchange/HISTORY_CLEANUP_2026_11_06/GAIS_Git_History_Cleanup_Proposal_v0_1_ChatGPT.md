# Proposal v0.1 - Git history size audit and optional targeted cleanup

**Project:** hydra3333/analysing_perceived_randomness_in_reality  
**Date:** 2026-11-06 (Australia/Adelaide)  
**Status:** PROPOSAL FOR CLAUDE REVIEW AND OWNER DECISION; NOT AUTHORISED FOR EXECUTION  
**Prepared by:** ChatGPT, independent reviewer  
**Subject:** Historical y-cruncher binaries, `.bin` files, intermediate decimal-digit files, and other large Git blobs

## 1. Purpose and executive recommendation

Assess whether the repository's approximately 983 MiB of local packed Git objects can be materially reduced by removing unnecessary historical large files, WITHOUT casually rewriting scientific provenance or disrupting work currently in progress with Claude.

**Recommended disposition:** APPROVE A READ-ONLY, METADATA-ONLY INVENTORY FIRST. Do not yet approve any history rewrite, force-push, garbage collection, deletion of backups, or change to existing project records. When the inventory is available, make a separate go/no-go decision. A targeted cleanup is preferable to a blanket size threshold if, and only if, the benefit justifies the history-integrity cost.

The immediate GAIS relocation is already committed and pushed. It does not need repeating.

## 2. Established facts (owner-supplied Windows command output)

| Observation | Evidence / interpretation |
|---|---|
| Local `git count-objects -vH`: `count: 167`, `size: 1.21 MiB` | Loose objects, approximately 1.21 MiB on disk |
| `in-pack: 5077`, `packs: 5`, `size-pack: 982.99 MiB` | Existing local packed object storage; NOT a proven removable total |
| `prune-packable: 0`, `garbage: 0`, `size-garbage: 0 bytes` | No reported loose garbage; does not classify all objects in packs as reachable or needed |
| `git log --all --oneline -- "src/GAIS/OUTLANDISH_01/y-cruncher v0.8.7.9547b/"` | The displayed path appeared at `54d161f` (add more GAIS outlandish) and in `6b99029` (relocation/removal) |
| Commit `6b99029` | `Relocate GAIS to repository root and exclude y-cruncher artifacts`; owner reported successful `git push origin main` |
| `git status --short --branch` | `## main...origin/main`, clean at the time checked |
| Old tracked y-cruncher distribution | 246 files in `src/GAIS/OUTLANDISH_01/y-cruncher v0.8.7.9547b/`; removed from current tree in `6b99029` |
| Old tracked ycruncher_digits item | One file removed from current tree in `6b99029` |
| Current root-level GAIS tracked files | 39 relocated files; no eligible file >=10 MiB in the owner's previous worktree scan |
| Current-index `.bin` query | No output from `git ls-files -- "*.bin"` at the time; THIS DOES NOT ASSESS HISTORY |
| Existing `.gitignore` | `/GAIS/**/*.bin`, `/GAIS/OUTLANDISH_01/ycruncher_digits/`, and `/GAIS/OUTLANDISH_01/y-cruncher v0.8.7.9547b/` confirmed by `git check-ignore` |

**Unknowns:** Historical `.bin` filenames, path variants, largest historical digit intermediates regardless of extension, compressed contribution of those objects, oldest affected commit, whether packed storage includes unreachable objects, all active branches/tags/pull requests/forks/clones, and the extent of references to affected commit IDs in authoritative science records.

**Caution:** `git log --all` searches commits reachable from local refs, not arbitrary unreachable objects or every ref that GitHub might retain. The local 982.99 MiB figure is not a current GitHub repository-size measurement. No full historical blob inventory has yet been supplied.

## 3. Inventory scope: DO NOT ASSUME `.bin` IS THE WHOLE ISSUE

Include all historical file blobs, including deleted and renamed files, across all intended repository refs. Rank by actual uncompressed blob size and by aggregate path/directory contribution; report a fresh-clone packed-size baseline separately. Examine:

1. **y-cruncher distribution** under the historical `src/GAIS/OUTLANDISH_01/y-cruncher v0.8.7.9547b/` path and any additional historical placement; `.exe`, `.dll`, `.txt`, `.cfg`, and other files.
2. **Historical `.bin` files** anywhere, particularly `src/GAIS/` and `GAIS/`, irrespective of whether they are present in the current tree.
3. **Intermediate decimal-digit files of ANY extension**: `.txt`, `.dat`, `.tmp`, `.dec`, unnamed/no extension, chunk/partial files, and large representations of pi/other mathematical constants. Do not assume their names or paths; derive candidates from the metadata report.
4. **Generated run outputs and archives** such as CSV, JSON, ZIP and intermediary folders, distinguishing reproducible scratch artifacts from unique experiments or provenance.
5. **Other large historical blobs across the repository**, regardless of extension, for owner visibility; do not automatically propose deleting unrelated scientific data or archives.

Report unique blob IDs as well as paths: a blob may occur at several paths or in multiple commits. Summing path sizes or uncompressed sizes does NOT establish reclaimable packed bytes. Trial rewrite plus fresh repacking is necessary to measure savings.

**Data firewall:** Metadata-only examination (blob ID, size, path, commit relationship) is in scope for a proposed audit. Do NOT open, display, decompress, search inside, parse, execute, or inspect contents of lottery outcomes or files under `source_data/`, `results/`, `transitory_data/`. Do not invoke project results fetchers, experiment runners, updater, Model H, or any unknown script. Do not display protected Powerball/Oz Lotto holdout results. If a metadata report names a protected path, report only its category and aggregate size unless owner explicitly authorises more. Executable binaries must never be run in the audit.

## 4. Work division and coordination with current Claude activity

### Claude - immediate review requested

A. Acknowledge this as an **unratified maintenance proposal**. Continue authorised ongoing project work; do not interpret this proposal as authority to begin maintenance or alter current repository history.

B. Identify any pending commits/branches, GitHub actions, reviews, install/release documents, handovers, exchange artifacts, ratifications, or pending external snapshots that assume stable Git IDs. Identify other clones/worktrees (including Claude Code/disposable clones) and any concurrent writers.

C. Assess whether a history rewrite is compatible with current project governance. Produce a dependency/impact inventory for commit-ID-based provenance, immutable review citations, signed commits/tags, GitHub Actions/release references, ZIP source snapshots and owner/Claude handover references. Recommend whether to **defer all rewriting until a quiet, owner-approved maintenance window**, which is the default preference.

D. Review/adjust the exact owner-run audit steps below, Windows CMD quoting, paths and tool versions. No repo mutation or code/test execution is authorised by this request.

E. Return a brief **Claude review and proposed audit specification**: blockers, any correction to assumptions, which output reports to collect, and which active tasks impose timing constraints. If useful, supply one non-destructive analysis script with output outside the Git repo, but do not silently execute it.

### ChatGPT independent reviewer

Independently review Claude's audit design and resulting report: distinguish verified observed facts from conjecture, enforce protected-data and process-safety boundaries, check the candidate deletion manifest against scientific/provenance requirements, and review a trial-rewrite result before any owner cutover decision. Reviewer does not authorise installation, Git history rewrite, or real-data access.

### Owner

Runs any approved Windows commands; decides whether to schedule maintenance, what exact files may be removed, whether changed commit IDs are acceptable, and whether/when to freeze writers and update GitHub. Owner alone may explicitly authorise a history rewrite and force-push after independent review.

## 5. Proposed phased procedure and approval gates

### Phase A - READ-ONLY discovery and baseline (proposed next action)

Gate A0: Claude reviews the plan and owner authorises the metadata-only inventory. This can be performed without freezing ongoing work if baselines identify the exact observed remote commit; later re-run after any further commits.

Collect the following baseline, preferably in a fresh **separately located mirror clone of the current GitHub remote** (not by rewriting the owner's active repository):

- Exact `HEAD`/remote branch tip, repo URL, timestamp, all branch/tag refs, object format, Git/tool versions, GitHub remote-tracking state, and worktree cleanliness.
- `git count-objects -vH` in BOTH original local clone (already sampled) and a fresh mirror clone. Difference may expose local-only object retention.
- `git filter-repo --analyze` reports from the isolated mirror (read-only analysis mode, no filtering). Rank top historical blobs, by path and directory, including deleted paths and total/unique sizes. Use the documented analysis reports; do not assume exact report filenames without checking installed version.
- Explicit lists for historical `.bin` files and candidate digit intermediates (not limited by filename extension); y-cruncher distribution path(s); first/last relevant commits; branch/tag/reachability; current `HEAD` inclusion flag.
- Quantify how much of the top-size list is uncontroversial disposable output versus protected or consequential records; classify unknowns as HOLD, not DELETE.

**Suggested owner-run CMD audit outline, FOR CLAUDE TO REVIEW FIRST; NOT AN EXECUTION AUTHORISATION:**

```bat
REM In a separate scratch parent folder outside the working repository:
git clone --mirror https://github.com/hydra3333/analysing_perceived_randomness_in_reality.git repo_history_audit_mirror.git
cd repo_history_audit_mirror.git
git rev-parse HEAD
git show-ref
git count-objects -vH
git filter-repo --analyze
```

Notes: Install/verify `git-filter-repo` separately if not present; do not install dependencies or change the owner's Python environment just to do this without approval. `git filter-repo --analyze` is a metadata analysis command; no `--invert-paths`, filtering, `--force`, garbage collection, or push in Phase A. Keep reports OUTSIDE the tracked project files until reviewed; metadata reports may include historical or confidential pathnames. Do not run the historical code.

**Deliverable A1:** A concise inventory table including: blob SHA; byte size; filename/path(s); extension; first/last reachable commit; whether in current HEAD; refs affected; category (`YCRUNCHER_DISTRIBUTION`, `GENERATED_BIN`, `DIGIT_INTERMEDIATE`, `OTHER_GENERATED`, `SCIENCE_RECORD`, `UNKNOWN`); candidate disposition (`REMOVE`, `KEEP`, `HOLD`); rationale; potential governance impact. Add summary counts and actual mirror clone packed bytes.

### Phase B - Scope/benefit decision (separate owner approval)

Gate B0: Independent review of A1 and selection of an **explicit path-based deletion manifest**. No blanket `--strip-blobs-bigger-than` and no `*.bin` wildcard removal without reviewing every matching historical path. Historical renames/case variants must be handled explicitly. The deletion set must not include files still required in current HEAD, immutable artifacts, or scientific provenance merely because they are large.

Produce alternatives:

- **Option 0 (default if provenance impact is excessive):** NO HISTORY REWRITE. Keep current `.gitignore` and the already successful current-tree cleanup; document historical size. Git GC alone will not remove still-reachable historical objects.
- **Option 1:** Narrow historical path cleanup of y-cruncher, plus individually approved generated `.bin`/decimal intermediates, if the first affected commit is sufficiently recent and the changed-SHA burden is acceptable.
- **Option 2:** Wider targeted historical cleanup only if audited savings are substantial and owner accepts the greater provenance/coordination cost.
- **Option 3:** Defer any rewrite until the ongoing implementation/release/ratification sequence has finished and a coordinated maintenance window is available.

For each option: estimate actual reclaimable bytes only from an isolated trial; list earliest affected commit, number of rewritten commits and refs, critical records affected, re-clone/transition cost, and residual GitHub/server storage uncertainties.

### Phase C - Isolated trial rewrite (NOT APPROVED BY THIS PROPOSAL)

Gate C0: Owner explicitly authorises only the disposable test, after independent review of manifest and commands. Protect the original repo and all authoritative records with a separately verified full mirror backup and/or Git bundle covering required refs, plus recorded original SHAs. Maintain any separate offline copies of locally ignored huge files (a Git backup cannot capture ignored/untracked files). Do not overwrite or modify the owner's current working directory.

Use fresh isolated clone(s) with only approved explicit path filters, such as `git-filter-repo --invert-paths --path <exact-historical-path>`; include renamed historical paths separately. Filtering alters commit IDs and normally removes signatures, so a trial must collect and preserve a complete old-to-new ID map. A GitHub URL alone is not proof of a recoverable backup; verify the backup in isolation.

Compare before/after:

- Original vs rewritten `HEAD` tracked-tree identity (`HEAD^{tree}`), provided all excluded paths are already absent from current HEAD. Expected equal tree hash for the same Git object format; verify, do not assume.
- Exact branch/tag/ref roster; commits/parents, signed objects and notes; impact to chronological evidence and immutable statements.
- Unwanted historical blob IDs absent from rewritten reachable history; no unintended removals; aggregate storage after repack in disposable clone; tool's commit map and first-changed commits.
- Local ignored/untracked materials still present in the untouched owner workspace.
- Proof that the historical rewrites do not violate the project's holdout, process safety, manifest/canonical hash, governance, firewall and installation constraints.

Do not modify authoritatively ratified documents to retroactively claim their old SHAs were new ones. Any necessary crosswalk or new provenance statement must be clearly identified and separately ratified; the old history must be retained safely as an evidence artifact if required by project governance.

### Phase D - Optional GitHub cutover (SEPARATE EXPLICIT OWNER GO/NO-GO)

Only after trial PASS and independent review: agree a brief freeze of all writers/actions, archive old history and authoritative SHA records, settle all in-flight Claude changes, ensure refs have not moved, review permissions/branch protection/tags/releases, and document exact ref-update/rollback/re-clone steps. A history rewrite is a controlled replacement of published refs, not an ordinary `git push`.

Do **not** run `git push --force`, `git push --mirror`, `git gc --prune=now`, or delete original packs/repos based on this proposal. On cutover, an authorised owner-run force update may be required; keep reintroduction-prone clones isolated and re-clone/transition collaborators carefully. Do not merge a branch still rooted in the old history into rewritten `main`.

GitHub may retain old commit objects through pull-request refs, forks, cached views, or internal retention. GitHub's published policy does not generally offer server-side purging for **non-sensitive** size-only cleanup. No precise claim of immediate GitHub storage reclamation should be made without measurement and verification.

### Phase E - Record and close

After any approved cutover: verify remote branches/tags and latest tree, clone the new remote afresh, verify no forbidden blobs reachable, capture true packed size, reconcile workflow/install documentation and SHA-dependent evidence, report any inaccessible old SHAs, cleanly resynchronise Claude and other workspaces, and explicitly close the maintenance task. Continue monitoring `.gitignore` and generated-output paths for reintroduction.

## 6. Acceptance criteria and hard stops

- **Audit PASS:** exact inventory of historically large blobs (including non-`.bin` intermediate digits), IDs, sizes, paths, affected refs and oldest affected commit, with no content reads of protected science data.
- **Proposal decision:** owner chooses NO REWRITE or approves a specific manifest plus an isolated trial. Mere desire for a smaller `.git` directory is insufficient authority.
- **Trial PASS:** correct current tracked tree, expected ref coverage, no critical artifact removed, audited blob absence, quantified actual storage savings, complete provenance mapping, no damage to original workspace.
- **Cutover PASS:** explicit final owner authorisation, coordinated writer freeze, reviewed backup/recovery plan, safely updated refs, new clean clone and provenance reconciliation.
- **STOP:** unclear protected data classification; hidden large blobs; active writers; missing/failed backup; unexpected ref deletion; unreviewed changes to authoritative experiments or immutable records; failure to explain changed historical identities; unapproved remote ref updates.

No safety switches, coordinator termination, orphan markers, draw outcomes, development holdouts, Mode H, FINAL, or production tools are implicated or authorised by this maintenance proposal. This document does not modify RAT-25 / DOC-12 or the owner-ratified scientific controls.

## 7. Precise questions for Claude's next response

1. Does ongoing implementation/review work make even an **audit** inconvenient, or only a later history rewrite? Recommend a suitable maintenance window without imposing one.
2. Which current and forthcoming ratification/provenance records actually embed Git commit identities that a rewrite would affect? Is this a governance BLOCKER or a manageable crosswalk?
3. What read-only Windows CMD audit outputs would Claude like the owner to collect, and can a single offline metadata-only report cover historical `.bin`, digit intermediates of any extension, and all large blobs?
4. Which backup, tag/branch/ref and re-clone procedures must be tested before any trial? Are there GitHub forks, pull requests, protected refs or signed commits/tags?
5. Should the default choice be Option 0/3 (preserve history/defer), unless the inventory proves large net savings and limited provenance impact?

**Requested next exchange:** Claude responds with a focused review and owner-run Phase A audit procedure only. Do NOT provide or run a production force-push/rewrite script until the owner explicitly authorises a later phase.

## 8. External technical references (background, not project authority)

- `git-filter-repo` manual, including `--analyze`, the fresh-clone safety check, and the need to specify historical renamed paths: https://github.com/newren/git-filter-repo/blob/main/Documentation/git-filter-repo.txt
- GitHub documentation on the consequences of rewriting history, changed Git IDs, collaborator coordination and limits of server-side purging: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository

---

**End of proposal v0.1.**
