# GAIS history clean-up - pre-cutover evidence package (Gate A)

- **Prepared by:** Claude (lead, by the owner's decision of 6 November 2026), from a fresh mirror of GitHub, 6 November 2026,
  about 11:15 Adelaide.
- **Answers:** the reviewer's assessment v0.1 (B01-B03, C01-C05).
- **Status:** nothing has been pushed or changed on GitHub. Claude makes no commits until the cutover is complete (C05). This
  file and `commit-map.txt` are delivered to the owner outside the repository (B01).

## 1. Identities (C03)

| Item | Value |
|---|---|
| Old `main` (GitHub, from `git ls-remote` just before the trial) | `6b9902968b6f97faffa8c3d4d38b6ea5edb9e389` |
| New `main` (rehearsed) | `9d28b9f51bab150ae5c8f9ccf62388b4853c4d0f` |
| Old and new `main^{tree}` | **identical**: `e8be5988e18f79d13cd1e34bbbf461f3659cca2c`; the full `git ls-tree -r` listings are identical |
| Unaffected boundary (the parent of `54d161f`) | `653b80c2fd542758d1604817a55b4cc00409817f`, an ancestor of new main |
| Commits on `main` | 416 before, 416 after: 389 kept with the same IDs (all ancestors of new main), 27 rewritten |
| Integrity | `git fsck --full` on the rewritten mirror: no errors |
| Tools | git 2.43.0; git-filter-repo `a40bce548d2c` |
| Command (in a fresh `--mirror` clone) | `git filter-repo --refs 54d161f^..main --invert-paths --path "src/GAIS/OUTLANDISH_01/y-cruncher v0.8.7.9547b/" --path "src/GAIS/OUTLANDISH_01/ycruncher_digits/" --path "src/GAIS/OUTLANDISH_01/digits_golden_ratio_10_to_6.bin" --path "src/GAIS/OUTLANDISH_01/digits_pi_10_to_6.bin"` |
| ref-map | `refs/heads/main`: `6b9902968b6f97faffa8c3d4d38b6ea5edb9e389` -> `9d28b9f51bab150ae5c8f9ccf62388b4853c4d0f` (the only ref) |
| Removed paths reachable from new main afterwards | 0 |

**Size (C03 item 5).** Both mirrors were measured the same way: a fresh mirror clone of all refs, then `git gc --prune=now
--aggressive`, then `git count-objects -vH`.
- Before: 5,233 objects, **82.84 MiB**.
- After: 4,975 objects, **44.62 MiB**.

What GitHub stores afterwards is not promised: it may keep unreferenced objects for a while (B03).

**Rejected variant (disclosed).** Claude also tried excluding the four EX_149-EX_152 commits from the rewrite, to keep their IDs.
That changed the tree and left 252 of the removed paths in place, so it was rejected. Only the verified command above is
proposed.

## 2. The removal set is complete and narrow (B02)

Inventory of every blob reachable from all refs, by metadata only (blob ID, size, path); no content was read:
- **The removal set:** 249 blobs, 155.1 MB uncompressed:
  - the y-cruncher folder (246 paths);
  - the `ycruncher_digits` placeholder (1 file);
  - `src/GAIS/OUTLANDISH_01/digits_golden_ratio_10_to_6.bin` and `digits_pi_10_to_6.bin` (1.0 MB each).
  These are the only `.bin` files ever committed.
- **Protected folders** (`source_data/`, `results/`, `transitory_data/`): 38 blobs, 7.3 MB, aggregate only. Their largest blob is
  3.0 MB, under `results/`. **Untouched.**
- **Everything else:** 2,478 blobs, 91.9 MB uncompressed. Its largest blobs are a 6.5 MB review bundle, three saved results-page
  `.mhtml` test fixtures (3.5, 1.5 and 1.5 MB) and EX ZIPs and diffs (0.6-0.9 MB). They are project records and test fixtures,
  so they are **kept**.
- **One digit file outside the set:** `GAIS/OUTLANDISH_01/Pi - Dec - Chudnovsky.txt` (0.95 MB) is tracked in the **current**
  tree. Removing it would change the current tree, so it is **not** in this rewrite. The owner may untrack it later by an
  ordinary commit if wanted.
- **No other** digit or constant-like file of 0.5 MB or more exists in history.
- **The owner's local 983 MiB** is not GitHub's history: the owner's own backup bundle of all reachable refs is 87.75 MiB. The
  rest is local-only, unreachable objects (section 5).

## 3. Refs, pull requests, collaborators (B03)

- **GitHub refs** (`git ls-remote`, just before the trial): `HEAD` and `refs/heads/main`, both `6b99029...`. There are no tags,
  no other branches and no `refs/pull/*`.
- **GitHub API:** pull requests 0 (all states); forks 0; branch protection on `main`: none.
- **Writers:**
  - the owner's PC;
  - this Claude chat (it commits nothing until cutover);
  - Claude Code (disposable clones, none open).
  The ChatGPT reviewer has no clone. No automations.
- **Temporary branch:** `history-cleanup`, holding only the rewritten main, deleted right after the cutover. After that, the old
  27 commits are reachable from no ref on GitHub. GitHub may still serve them by full ID for a while; no purge is claimed.

## 4. The 27 rewritten commits: crosswalk and signatures (B01, C01)

A correction to Claude's earlier statement ("9 earlier signed commits"): **227 commits in the history are signed**, all
Claude's (the cloud workspace signs its commits automatically).
- **15 of the 27 rewritten commits are signed, all Claude's.** git-filter-repo drops their signatures, and Claude cannot
  reproduce them. Content and authorship are unchanged.
- **The other 212 signed commits keep their IDs and signatures.**
- **The owner is asked to accept this explicitly (C01).**

| # | Old commit (full) | New commit (full) | Signed before | Date (Adelaide) | Author: subject |
|---|---|---|---|---|---|
| 1 | `534af84746af4cfaa9ccc8712ce354093ac92196` | `a0ebb1f85d6ca8c837af58662ccc729cb2942738` | SIGNED | 2026-11-05 20:42 | Claude (web chat): exchange: EX_149 (Claude to ChatGPT): MHUP-A review slice 2 candidate |
| 2 | `54d161f8da625e18aa337a7c110290e0fefc7e83` | `64d54744f3d3a8c59a8bf34b72042b3a5cb679d5` | unsigned | 2026-11-05 21:08 | hydra3333@gmail.com: add more GAIS outlandish |
| 3 | `442597aeee02b14a499254851e2bfd9e3e141a95` | `129cf3218ef42d5c5a8935ab238918af7dd5c101` | unsigned | 2026-11-05 21:08 | hydra3333@gmail.com: Merge branch 'main' of https://github.com/hydra3333/analysing_perceive |
| 4 | `ece780a27b0386df652ab14e0bba4cc14d114462` | `8e2c214719352c6283dce4d8abb603b08f8681e5` | unsigned | 2026-11-05 21:12 | hydra3333@gmail.com: add more GAIS outlandish 10 to 6 search |
| 5 | `456cefd35197fdc38cfff1a203089ad578a942b7` | `a8dc0109e072b0b3d1e83bc16a447bd94278cc2a` | unsigned | 2026-11-05 21:19 | hydra3333@gmail.com: updated outlandish - needs proper draw input data |
| 6 | `c498103ff671ba3176b1d58472970255db22d376` | `a74fb977d67a0e7515d2d5847ef2b2dbe91e8536` | SIGNED | 2026-11-05 21:37 | Claude (web chat): exchange: EX_150 (ChatGPT, for the record: slice 2 v1r1 B02-B04 and C0 |
| 7 | `8b5acaabb980e48973ac560d27806ec94ca5825f` | `b8db7329386886b6e51581e5caec3b6f2ef4f341` | SIGNED | 2026-11-05 22:15 | Claude (web chat): exchange: EX_151 (Claude to ChatGPT): MHUP-A review slice 2 candidate |
| 8 | `f7d90da5d8aff46d896923c751bff8342439160b` | `9605ba7a251c845c679b9b157feb19aff9ca36bb` | SIGNED | 2026-11-05 23:57 | Claude (web chat): exchange: EX_152 (ChatGPT, for the record): MHUP-A slice 2 candidate v |
| 9 | `43dd069237c723d056e710a0775f1a42f61fadd6` | `e25ed7f9a75b45b72ea48a97a46693d09f483561` | unsigned | 2026-11-06 00:15 | hydra3333@gmail.com: more outlandosh stuff including handover |
| 10 | `c84e2dc24e82cbc73860242f6e557f88642038e7` | `edd44778f92d906a30a9db9aa26ff0608b8aac8b` | SIGNED | 2026-11-06 00:24 | Claude (web chat): exchange: HANDOVER_2026_11_06 (risk management, 1 of several): Claude |
| 11 | `957a452c04ea9e073282689ca987234a01bed749` | `b335dadef4c7cec9100e0d91bf4a91e2e97ea15d` | SIGNED | 2026-11-06 00:25 | Claude (web chat): exchange: HANDOVER_2026_11_06 (2 of several): reminders R-022 (the Cha |
| 12 | `2660e4606d65036f20dbca62060d38bcc8add931` | `bdcc5390a51a704d5aa825bd43e7c1fc65d91c8a` | SIGNED | 2026-11-06 00:27 | Claude (web chat): exchange: HANDOVER_2026_11_06 (3 of several): the ChatGPT reviewer han |
| 13 | `dbde41f05657b5693a91ddda40896db305503308` | `c907e69fade5dcaf17b229f471b153579174d444` | SIGNED | 2026-11-06 00:28 | Claude (web chat): exchange: HANDOVER_2026_11_06 (4 of 4): the introductory blurb for a n |
| 14 | `aa3adbbcd5e22e48a42d8c7dc162752be089fbd4` | `ddaf1724c315a5bc146abe166b636a0b9f6c5493` | SIGNED | 2026-11-06 00:46 | Claude (web chat): exchange: HANDOVER_2026_11_06 (5): register v0.25 CANDIDATE (unreviewe |
| 15 | `8e8c1af937f1d117bc3e95d9fbc97975bcbc6d20` | `e061f12a4a22b5d2ec8b99190d1ef9adeb0acfc3` | SIGNED | 2026-11-06 00:47 | Claude (web chat): exchange: HANDOVER_2026_11_06 README - file sizes and SHA-256 recomput |
| 16 | `929eff549ae9870c2a6404f00e1ab53b8998f80f` | `030a3894970e30ad13b8899874a5ceabb9ac5901` | unsigned | 2026-11-06 00:50 | hydra3333@gmail.com: latest handover docs |
| 17 | `5a0bb9ad75054b38a669d3eae0f5745fcac5d5a7` | `a79def819c84c93b179d27d67c6fe2a06f5c4e3e` | unsigned | 2026-11-06 01:27 | hydra3333@gmail.com: handover stuff |
| 18 | `0432b7fdd7f713503ba098d48e555d42daa38d48` | `8e1d74dc96194595c7c7d482b67a1ab1ad8ae651` | SIGNED | 2026-11-06 01:29 | Claude (web chat): exchange: EX_153 (ChatGPT, for the record: the new reviewer's takeover |
| 19 | `b20f2c034323060240f87decec401213c850029c` | `95bcb77f45ee0c18196e6e201592e04f6472dbeb` | unsigned | 2026-11-06 01:36 | hydra3333@gmail.com: more handover |
| 20 | `b913e51acb357fd61bdb03ecac5ace66da995cdc` | `bffa962aea2840b12b49137a1cd5b521e6797cf2` | SIGNED | 2026-11-06 01:48 | Claude (web chat): exchange: EX_155 (ChatGPT, for the record: TAKEOVER-C01 RECHECK PASS; |
| 21 | `3e0d15d9d6d615b0db4757114c0ad1907fde611c` | `2253703644026082d4b3cf076b1b6968c4017b6a` | unsigned | 2026-11-06 01:52 | hydra3333@gmail.com: candidate 3 |
| 22 | `8841e62403368a37ab91c142d2219c6452031a13` | `7d3e164898f256964868baf62c59f0d4d25672fa` | SIGNED | 2026-11-06 01:55 | Claude (web chat): exchange: DOC12 - the owner's ratification RAT-25 (6 November 2026: ne |
| 23 | `377e27ae81d4e7f6bfd748e01eacca1b40541df3` | `fafa1ba2484348c5ab26ec7526cf614c884bfb98` | unsigned | 2026-11-06 01:57 | hydra3333@gmail.com: DOC-12: H-2 v1r9 and register v0.25 (owner-ratified 6 November 2026, R |
| 24 | `2eb9abb2d84dbc6367f795d8dee6b3c9c5942e8e` | `e963e0e9dd11ca5a132120a9be5169298f33d693` | unsigned | 2026-11-06 02:21 | hydra3333@gmail.com: CLAUDE_CODE_WORKING_FOLDER_TREE: report for task T022 (Claude Code loc |
| 25 | `cbf29bbefb0d53389cae2beb0df4f2571be51214` | `4dac77d73ba7dcbb416ed7fa4891f490b21e2841` | SIGNED | 2026-11-06 10:14 | Claude (web chat): exchange: roadmap - DOC-12 installed at 377e27a and verified from GitH |
| 26 | `6eb1fbd93c28edf9f9f78be421748b694bba3667` | `f99de9fb8f6458dc4509437e57f26db36df4cf8e` | SIGNED | 2026-11-06 10:40 | Claude (web chat): exchange: reminders R-020 (e) and (f) decided by the owner, 6 November |
| 27 | `6b9902968b6f97faffa8c3d4d38b6ea5edb9e389` | `9d28b9f51bab150ae5c8f9ccf62388b4853c4d0f` | unsigned | 2026-11-06 10:42 | hydra3333@gmail.com: Relocate GAIS to repository root and exclude y-cruncher artifacts |

Commits 1, 6, 7 and 8 (EX_149-EX_152) never contained y-cruncher. They change only because the tool rewrites them without their
signatures.

**Commit messages.** git-filter-repo also replaces abbreviated commit IDs *inside the messages* of rewritten commits with the
new IDs. For example, the roadmap commit now reads "DOC-12 installed at fafa1ba" instead of "377e27a". No file contents change.

**Old IDs in project records.** The ratified register v0.25, H-2 v1r9, EX_154-EX_156, DOC12's README, the roadmap, the
reminders and REPORT_T022 cite some of the old IDs (for example `54d161f`, `43dd069`, `c84e2dc`, `2660e46`, `929eff5`,
`377e27a`, `2eb9abb`, `b913e51`).
- They are **not edited**. This crosswalk maps each one.
- After the cutover, Claude commits the crosswalk to `exchange/`, and register v0.26 cites it.
- Every document SHA-256 in every record is unchanged, because no file changes.

`commit-map.txt`, git-filter-repo's own map (27 lines plus a header; SHA-256 `52b27bb30b32e07cbaab14b2553d318d5071d26421bc40a222859b6302974d1c`), travels with this file.

## 5. Backup, rollback, local clean-up (C04)

- **Backup:** the owner's bundle `E:\TEMP\repo_before_cleanup.bundle` (87.75 MiB, all refs) holds the complete old history.
  Verify it with `git bundle verify E:\TEMP\repo_before_cleanup.bundle`.
- **Rollback:** only by a separate owner decision. Push old main `6b99029...` back from the bundle, using the same pinned-lease
  form. It would restore the removed binaries.
- **Local garbage collection** (`git reflog expire`, `git gc --prune=now`) is **not part of this cutover**. It is optional and
  later, and only after a physical copy of the owner's `.git` folder, because a bundle does not keep unreachable objects.

## 6. The cutover commands (C02, C03); each gate only after the previous one passes

Windows CMD, in the repository folder. `^` must be quoted in CMD, as shown.

**Gate B (owner):**
```
git bundle verify E:\TEMP\repo_before_cleanup.bundle
git status --short
git ls-remote origin refs/heads/main
```
Expected:
- the bundle verifies;
- `git status --short` prints nothing;
- `git ls-remote` prints `6b9902968b6f97faffa8c3d4d38b6ea5edb9e389`.

No commits by anyone until Gate E is complete.

**Gate C (Claude, after the reviewer's RECHECK and the owner's go).** Claude pushes
`9d28b9f51bab150ae5c8f9ccf62388b4853c4d0f` to `refs/heads/history-cleanup`, and nothing else. The owner then checks:
```
git fetch origin
git rev-parse origin/history-cleanup
git rev-parse "origin/history-cleanup^{tree}" "main^{tree}"
git diff main origin/history-cleanup --stat
```
Expected:
- `9d28b9f51bab150ae5c8f9ccf62388b4853c4d0f`;
- `e8be5988e18f79d13cd1e34bbbf461f3659cca2c`, twice;
- no output from the diff.

**Gate D (owner, exactly one update of main):**
```
git ls-remote origin refs/heads/main
git push --force-with-lease=refs/heads/main:6b9902968b6f97faffa8c3d4d38b6ea5edb9e389 origin 9d28b9f51bab150ae5c8f9ccf62388b4853c4d0f:refs/heads/main
git push origin --delete history-cleanup
git ls-remote origin
```
- Run the first command just before the push. If it does not print `6b99029...`, **STOP**.
- After the push and the branch deletion, `git ls-remote origin` must show only `HEAD` and `refs/heads/main`, both `9d28b9f...`.

**Gate E (owner, then Claude):**
```
git status --short
git fetch origin
git rev-parse origin/main "origin/main^{tree}" "main^{tree}"
git reset --soft origin/main
git status --short
git rev-parse HEAD
```
- The first `git status --short` must print nothing.
- Expected from the first `rev-parse`: `9d28b9f...`, then `e8be598...` twice.
- The second `git status --short` must print nothing.
- `git rev-parse HEAD` must print `9d28b9f...`.
- Never use `--hard`. Ignored local files (GAIS digits, score ledgers, `transitory_data`) are untouched by `--soft`.

Then Claude:
- verifies GitHub from a fresh clone;
- confirms that no removed path is reachable;
- commits the crosswalk to `exchange/`;
- notifies the reviewer.

Claude Code needs nothing, because each task makes a fresh clone.

**At any STOP:** leave everything as it is, keep the bundle and this file, and tell Claude. No retry without the owner's decision.
