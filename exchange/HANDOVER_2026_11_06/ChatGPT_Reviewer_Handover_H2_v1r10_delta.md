# ChatGPT reviewer handover H-2 v1r10 (DELTA on H-2 v1r9) - the state at 8 November 2026, evening

Written by Claude (primary designer and coder) on the project owner's instruction, 8 November 2026, as insurance in case the
reviewer chat that took over on 6 November 2026 has to be replaced. **Not reviewer-written. Checked by the reviewer
(EX_161) and OWNER-RATIFIED on 8 November 2026 (RAT-27) as a working supplement to the ratified H-2 v1r9** (`doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r9.md`).
Read H-2 v1r9 in full first; its reviewer-rights region (sections 2 and 3) is unchanged and is not touched by this delta. Where
this delta and a ratified record disagree, the record wins: register v0.25 (and v0.26 once ratified), the design v0.1r5 as
amended by A1, and the owner's decisions in `exchange/`.

US-ASCII; LF in the repository's `doc/` copy, CRLF in `exchange/` and when relayed. The owner is named only as "the project owner" or "hydra3333". Every fact below should be verified against the
repository before it is relied on (R-9).

## 0. Two things to know first

1. **Commit IDs.** On 6 November 2026 the history was rewritten to remove accidentally committed third-party binaries; 27
   commits of 5-6 November got new IDs (file contents unchanged; 389 earlier commits unchanged). Any record that cites one of
   those 27 uses its old ID, including H-2 v1r9 itself (for example its `43dd069`, `2660e46`), register v0.25 and EX_153-EX_156.
   Translate with `exchange/HISTORY_CLEANUP_2026_11_06/commit-map.txt` (all 27; old in column 1). The H-1 v1r10r1 delta's
   section 0 has a 24-pair selection.
2. **Exchange numbers.** When this delta was written the newest messages were EX_157 to EX_161 (the handover and DOC-13
   checks). Always check `exchange/` for the highest number in use and take the next one.

## 1. What your predecessor did after H-2 v1r9 was written (6-8 November 2026)

| Message | What | Outcome |
|---|---|---|
| EX_153 | Takeover assessment of H-2 v1r9 candidate 1 and register v0.25 candidate 1 | Role accepted on H-2 v1r8; rights region verified (7,676 LF bytes, SHA-256 `70e50dc3...`); TAKEOVER-C01 to C05, O01 |
| EX_155 | Recheck of candidate 2; blind answers to Claude's verification questions Q1-Q19 | C01 PASS; C06, O02; answers all agreed with Claude's sealed key (EX_156) |
| (owner) | RAT-25: H-2 v1r9 and register v0.25 ratified; DOC-12 installed | |
| History clean-up proposal v0.1, assessment v0.1, Gate A RECHECK v0.1 | Your predecessor proposed an audit-first plan, then assessed and rechecked Claude's 27-commit rewrite evidence (B01-B03, C01-C05) | Gate A PASS; the owner then ran gates B-E (`exchange/HISTORY_CLEANUP_2026_11_06/`) |
| EX_157 | Focused documentary check of Claude's H-1 v1r10 handover | P01-P04 PASS; H1R10-C01 (test status overstated), C02 (gate count), C03 (order of work: final evidence only on the date-frozen candidate; R-020 (g) before the rulebook change), O01-O04 |
| EX_159 | Recheck of EX_158 | PASS; O05 editorial pointers |
| (owner) | RAT-26: H-1 v1r10r1 delta and blurb ratified as working supplements to H-1 v1r8 | installed in `doc/HANDOVER/` |

**Your predecessor's evidence boundary:** it reviewed documents and Claude's evidence; it did not execute the project's tests,
the rewrite, or any builder. It said (EX_155 Q15) that for the integrated review it intends R-2 reproduction where authorised and
R-4 oracles (N-1 perturbation including method-visible digests and ties; roster, plan and receipt binding; A1 crash points;
install barrier, process table, two-commit publication and release-record admission), and asked for: the full integrated ZIP,
manifests and hashes, complete test and mutant inventories with negative evidence, clean base and target identities, Windows
T022/T016 outputs, the owner's dependency and GAIS decisions, and explicit authority for any test not already permitted.

## 2. Facts that have changed since H-2 v1r9

- **Windows evidence:** T022 PASSED (slice 2 v1r2, 570 tests, 4 allowed symlink skips; report commit old `2eb9abb` = new
  `e963e0e`). T021 was withdrawn unrun. One recorded runner deviation (step 8 started detached to time it; command unchanged).
- **The owner's decisions:** DEP-1: `pyahocorasick` is installed in the project venv and approved ("we keep it"); the environment
  freeze records it at Approval 1. GAIS-1: GAIS moved from `src/GAIS/` to the top-level `GAIS/`, outside MHUP-A's code closure;
  y-cruncher untracked. The owner waived the bundle-restore test in the clean-up and accepted the loss of 15 commit signatures
  (all Claude's).
- **The owner's own commits** continue outside the reviewed line: OUTLANDISH work under `GAIS/`, `.gitignore` lines, and a new
  root `create_venv.bat` (creates the venv only if absent; installs nothing). An OUTLANDISH chat works with the owner on that; it
  is not part of this project's review.
- **The integrated MHUP-A package** (the owner's "go", 8 November): the reviewed code was rebuilt on the current `main`
  (`009c985`); a preliminary run of all 570 tests on Linux Python 3.13.18 and 3.15.0b4 had one expected failure each (the test
  pinning E_1 revision 3's `effective_date`, which the build now sets to the package date: C01-EFF); the full suite on the final,
  date-frozen package is still to run. The package itself (manifest; copy tool; verifier with `pre`, `post`, `committed` and a
  new `released` phase; the owner's Appendix J instructions; LF/CRLF rehearsals; T016) is not yet built. **Nothing is installed.**
- **The step 6 gate files are ten** (eight changed, two new; all `src/methods/_common/`); the builder must recompute the import
  closure and assert it equals the manifest's list (EX_157 C02).
- **The order of work** (EX_157 C03, controlling): tools and verifier; the owner's R-020 (g) decision; freeze the date and build
  the final candidate; all final evidence on that candidate (full suites, both mutation chains, LF/CRLF rehearsals, T016 under the
  owner's go); the review request; then install only after PASS and separate approval. If T016 must follow the review, the review
  is provisional as to Windows until an evidence recheck.
- **R-020 (g) is OPEN** (the owner's decision): Appendix J's steps run `process_check.py` and `install_records.py`, which Claude
  Code's rulebook v0.4 rule 7 forbids. Option (i): rulebook v0.5 allows only those two tools, only inside T016's synthetic,
  non-pushing clone, from the staging folder, under the task file. Option (ii): the owner runs T016's steps. Your predecessor
  preferred (i) under conditions (EX_157 section 3).
- **Planning:** ST-5's 13-15 November target is now unlikely; FB-1 applies (nothing is cut).

## 3. Watchpoints for the integrated review (consolidated; H-2 v1r9 section 0.7 plus the above)

1. Assembled behaviour, not slice PASSes (EX_152 s.5): integration, records, installer and verifier, release gating, LF/CRLF,
   Windows and safety rehearsals including T016, the outstanding Windows evidence.
2. EX_148 (ix): COMMITTED PASS proves both commits, the barrier order (U, then E and P, then the gate) and records/repository
   agreement; the `released` phase checks the release commit and record.
3. A1's order exactly: read once; compute; publish whole, create-only; **validate the published ledger**; `SCORE_COMPLETE`;
   report; seal; three recovery states; a refused published ledger is a STOP.
4. C01-EFF: the date set at freeze; every digest and the pinned test follow it; evidence produced after the freeze.
5. R-019 (a), (d), (e) in the assembled behaviour; (b) and (c) are MHUP-B's.
6. R-020 (a) release entries (40 per game after release), (b) orphan files refused, (c) the owner's POC-suite rerun choice,
   (d) the rebase (the owner's `.gitignore` lines kept), (e) DEP-1, (f) GAIS-1, (g) the T016 rule.
7. MHUP-B's timing (design 4.4): before Approval 1 or after a game's seal, never between; the install plan states the route.
8. The rulebook v0.5 change (if (i)): exactly the narrow allowance; the settings denials not bypassed; `check_task_commands.py`
   passes; no change to the main repository; T016 needs its own owner go.

## 4. Change control

Written by Claude from the records; your predecessor's own words are in its messages (EX_153, EX_155, EX_157, EX_159 and the
clean-up documents). No reviewer right, safeguard or procedure is changed. Status: checked by the reviewer (EX_161: C01 applied to
the blurb), OWNER-RATIFIED 8 November 2026 (RAT-27) as a working supplement to H-2 v1r9; the next full H-2 edition folds it in
after MHUP-A.

End of H-2 v1r10 delta.
