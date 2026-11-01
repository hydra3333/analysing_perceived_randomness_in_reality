## 12. Working knowledge (for a chat that starts without the previous chat's workspace)

This section writes down how the previous chat actually worked, so that a new chat can work the same way from the repository alone. It describes practice, not rules; where it repeats a rule, the rule's own document prevails. The previous chat's cloud workspace is gone when the chat ends; nothing here assumes it.

### 12.1 The work cycle, step by step

1. **Scope.** The owner names the work. Write a work-item card (section 1.2). For HIGH work, write the design first (section 8.2).
2. **Design round** (R-3): an EX message to the reviewer with the design note (a builder script for any document edition, and any reference or probe script). The reviewer replies PASS or RECHECK with findings. Fix, resend for a focused RECHECK, repeat. The owner ratifies the design (and decides any OWNER question) before code depends on it. The owner may vary the process for a small item: PERF-1 was coded and tested first and reviewed once (owner, 1 November 2026).
3. **Code round** (R-2): build the package (12.3), run the suite on both Pythons, the mutation checks and the LF/CRLF rehearsals, then send an EX message with the package zip, its member list, the complete source and test diff, the rehearsal logs and a not-tested list. Iterate as for the design.
4. **Windows rehearsal:** a Claude Code task file (12.4); the owner runs it and pushes the report; Claude reads the report from GitHub and checks every step's output.
5. **Owner acceptance and install:** lead the owner through the package's `INSTALL_INSTRUCTIONS.md` one block at a time (save the zip to `E:\TEMP`, check its SHA-256 with `certutil -hashfile`, extract with `tar -xf`, then PRE, copy, POST, suite, stage, status, commit, COMMITTED, push). Ask for each block's whole output before the next.
6. **Verify from GitHub:** `git pull`, then check the commit's file list, every blob against the package's `INSTALL_MANIFEST_SHA256.txt` (LF-normalised), and that no data folder changed.
7. **Record:** update `exchange/OWNER_ROADMAP.md` and `exchange/OWNER_REMINDERS.md` (CRLF, US-ASCII); the next register edition records the round.

**The EX protocol in practice** (`exchange/README.md`):
- Numbers are shared and increasing; check the highest committed number first. The snapshot's review request is EX_116 and the reviewer's reply EX_117; after that, check the highest committed number before choosing the next.
- An EX message is US-ASCII with CRLF: first line `# EX_NNN - <Sender> to <Recipient>`; then `Date`, `Project`, `Replies to`, `Contents`, `Subject`; ask the reviewer to number its reply; end with a member table (file, SHA-256 as stored, SHA-256 after CRLF to LF) and `End of EX_NNN.`
- Claude's messages with attachments are a flat zip `EX_NNN_Claude.zip` built with `exchange/EX_019_Claude/make_zip.py SRC OUT MEMBERS flat` (deterministic: fixed timestamps, sorted members). An install package inside it is its own zip (`make_zip.py PKGDIR OUT MEMBERS`, which keeps the top folder).
- Commit each EX zip as `exchange/EX_NNN_Claude.zip` **and** its members extracted to `exchange/EX_NNN_Claude/`; commit each reviewer reply byte for byte as `exchange/EX_NNN_ChatGPT.md` (or its zip, extracted). The owner uploads the reviewer's files to the Claude chat; Claude commits them.
- Send the zip to the owner with the file-sending tool and give a short paste-ready block for the reviewer naming the zip and the reply number.

**Repository access.** The previous chat ran as a Claude Code cloud session with the repository attached through the GitHub app (the session's `add_repo` tool and its git proxy); `git push` to `main` worked for `exchange/` and `CLAUDE_CODE_WORKING_FOLDER_TREE/` commits. A new session gets the same by attaching `hydra3333/analysing_perceived_randomness_in_reality` with push access. If a session has no write access, do not work around it: give the owner the files (or one zip) with the exact `git add <paths>`, commit message and push commands, and verify from GitHub after his push.

### 12.2 The tools (`exchange/CLAUDE_WEB_TOOLS/`)

The snapshot commits the previous chat's working tools to `exchange/CLAUDE_WEB_TOOLS/`, with a README that is authoritative on their exact names and use. By kind:
- **Package builders** (for example `build_wf1b_pkg.py`, `build_perf1_pkg.py`): from a dev tree and a base tree, they check that only expected files differ, write `repo_overlay/`, the manifest (Git-content SHA-256, LF), the verifier from `verifier_template.py`, the suite runner from `suite_template.py` (expected counts per module, the allowed symlink skips, failure details) and `INSTALL_INSTRUCTIONS.md`. Guarded paths are files that must stay byte-identical in Git (their base blob hashes are written into the verifier).
- **The verifier template** gives `pre` (clean tree, base ancestry, guarded files, new paths absent, replaced files at base bytes), `post` (exactly the new and modified paths, with the expected bytes after CRLF to LF) and `committed` (the last commit changed exactly those paths; Git blobs match). **The suite template** runs each module in its own `python -B -m unittest -v` process with `PYTHONPATH=src;src/methods;tests`.
- **Mutation tools** (`wf1b_mutations.py`, `perf1_mutations.py`): each mutant is (name, file, exact old text, new text, test modules); the tool copies the dev tree, applies one mutant, runs the modules with `-f` (fail fast) and reports CAUGHT or SURVIVED. Ship the tool and its output in the package's `review/<PACKAGE>/`.
- **Rehearsal scripts** (`e2e_wf1b.sh`, `e2e_perf1.sh`): in disposable clones of a frozen mirror, LF and CRLF, they run PRE, copy, POST, the suite, stage, commit and COMMITTED, then the negatives (an untracked file, wrong bytes in a new and a replaced file, a missing file, an unexpected change, a stray committed file, a damaged package), each of which must STOP.
- **Task-file generators** (`make_t012.py` to `make_t015.py`): each writes `CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_Tnnn.md` from the zip path, its SHA-256, the counts and the base; make each new one from the last by counted edits. **`check_task_vs_deny.py SETTINGS TASK`** tests every command line in a task file against `.claude/settings.json`'s Bash deny patterns; run it on every task file.
- **Assemble scripts** (`assemble_ex112.py`, `assemble_ex114.py`): stage an EX message's members, fill its placeholders from the evidence files (asserting the expected PASS/STOP counts), write the member table, zip it, and copy it into `exchange/`.
- **Others:** `profile_stats.py` (profiles the report's statistics stage at full size on invented data); `check_pulse.py` (checks a saved NIST Beacon pulse file against a policy's acceptance row); `make_wf1b_registries.py` (builds WF-1B's measure and family registries); the register and handover builders (`make_register_v2N.py`, `make_h1_v1r7.py`, `make_h2_v1r8.py`).

The workspace paths inside these scripts are the previous chat's (for example `/home/claude/work/...`; the snapshot tools in `snapshot/` hard-code `/home/claude/work/snap/`); change them at the top of each script before use.

### 12.3 Building and rehearsing a package

- **Base tree:** `git archive <base commit> | tar -x -C BASE`, then delete `source_data/`, `results/` and `transitory_data/` from it. **Dev tree:** a copy of the base tree plus your changes. Never work in the owner's checkout.
- **Suite on Linux:** `PYTHONPATH=src:src/methods:tests python3 -B -m unittest <module>` per module, on the system Python 3.13 and on a Python 3.15 venv with the project's dependencies. The 3.15 venv will not exist in a new workspace: `uv python install 3.15`, `uv venv --python 3.15 <dir>`, then install the project's direct packages, as listed in `DIRECT_PACKAGES` in `install_upgrade_dependencies_into_venv.bat` (`requests beautifulsoup4 psutil numpy scipy threadpoolctl selenium`; `requirements.txt` is historical), with `uv pip install --python <dir>/bin/python ...` (a bare 3.15 fails every module on `numpy` and `psutil`). The owner's exact versions appear only in each report's environment line (Windows, Python 3.15.2, numpy 2.5.4); a full freeze list of his venv is not recorded (an open item for R3-T50's no-upgrade rule in Mode H).
- **Where the suite runs:** the base and dev trees (without the data folders) are for building packages only. The suite and the rehearsals run in **full disposable clones of the frozen mirror**, where the project's accepted tests read what they are written to read, some of them the development masters through the project's reader (rulebook rule 2.5). Claude never opens those folders itself. That is how the 471-test count is reproduced on Linux.
- **Frozen mirror for rehearsals:** `git clone --mirror <repo> repo_snapshot.git` once, then `git -C repo_snapshot.git fetch <repo> main:main` to bring it to the package's base. Run the rehearsals **one after another**, never two at once from a freshly made mirror (parallel clones failed with a missing `tmp_pack`).
- **Before sending:** both Pythons pass, the mutations are all caught, both rehearsals pass with every negative STOPping, the task file passes the deny check, and every count in the instructions came from the tools.

### 12.4 Claude Code task files

- One task per rehearsal (`TASK_Tnnn.md` in `inbox/`), committed by Claude; the owner pulls, starts a **new** Claude Code conversation, and types `Do inbox\TASK_Tnnn.md`. The report comes back as `outbox/REPORT_Tnnn.md`, committed by the runner and pushed by the owner.
- Commands are written out in full with absolute Windows paths; each step states its expected PASS line; a STOP sends the runner to clean-up and the report.
- **Never put `.bat` in a task command** (the deny list), nor any other denied text (`lottery`, `results_master`, `Run_Experiment` and the rest); run `check_task_vs_deny.py`. Name a `.bat` file by pattern when you must (`"Run_Method_Rankings.*"`).
- Read the whole report: every step's command, exit code and output. The runner records deviations (for example writing its report with its file tool); they are facts, not failures.

### 12.5 Traps in the cloud workspace

- **Stopping your own test jobs in the cloud workspace, and nothing else (EX_117 C02).** This applies only to expendable, non-scientific test processes that Claude itself started in its own cloud workspace for this chat (a test suite, a rehearsal, a mutation run, a profile). Never stop them by a name pattern: `pkill -f unittest` matched the chat's own shell twice and killed it. Find the job you started (`ps -eo pid,ppid,etime,cmd`), confirm from its parent and its full command line that it is that job, and stop only that one; if you are not certain, let it finish. **A PID is neither proof of ownership nor permission to stop anything else.** Claude never terminates a project process: no experiment, worker, coordinator, batch, report or uncertain process, on any machine. The protected no-status/no-kill interlock (Architecture section 5C; section 5.4 above) and the owner's separate process-control gates govern those, and nothing on the owner's computer is ever stopped by Claude.
- **The shell tool's default timeout is about two minutes.** Give a longer timeout, or run long jobs in the background (`nohup ... &`) writing to a file, and poll the file with short sleeps.
- **Do not import a package's own scripts in place** for a probe (a `__pycache__` folder crept into a package and had to be removed and the package rebuilt); copy the script elsewhere or load it with Python's `-B`.
- **The shell resets its working directory** after some commands; use absolute paths.
- **Outbound network** goes through a proxy allowlist (package registries and GitHub); lottery sites are never contacted, and must not be tried.
- **Downloaded or received files** go into a fresh directory each; run Python that reads them with `-I`.

### 12.6 The owner's machine and checkout

- Windows 11, the project venv at `.venv` (Python 3.15.2), the repository at `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality`, Git with `core.autocrlf=true`. Downloads go to `E:\TEMP`. The owner's PC has 12 cores and 24 logical processors.
- Git's "LF will be replaced by CRLF" warnings when staging are harmless. But a Git operation that rewrites files (a rebase after a rejected push, a checkout) writes CRLF into text files under `results/`, and a create-only record checked byte for byte then refuses (the first Powerball report; R-011).
- If a Windows console window is clicked, it can enter "Select" mode and freeze the program the moment it prints; Esc releases it. Turning off QuickEdit Mode prevents it.
- To see whether a long run is alive without disturbing it, from a second window: `powershell -command "Get-Process python | Select-Object Id,CPU,StartTime"` twice, a minute apart (CPU seconds rising means busy); file names, times and sizes from `dir` show the stage. Never open record contents.
- `Run_Experiment.bat Method_Walk_Forward.py status --game G --batch ID` shows a batch's counts (read-only). The report tool has its own progress lines from PERF-1.

### 12.7 How the owner likes to work (a checklist)

- Plain, step-by-step English; lead each step and say who does what. Commands in one block per step, with the expected output and what to do on a STOP.
- Decisions as question / why / recommendation / options (the question tool is fine).
- A paste-ready block for the reviewer whenever something goes there, naming the zip to upload and the reply number.
- Save downloads to `E:\TEMP`; never into the repository.
- `git add` with specific paths, never `-A`.
- Do not push while the owner may have local commits waiting (section 2); explain the hold if the stop hook complains.
- Never write the owner's name in anything committed.
- The owner sometimes has only a phone; then only phone-possible steps.
- Show the roadmap at milestones; keep the reminders list current.
- The owner prefers getting the project running over machinery; keep the safety-critical parts and keep everything else lean.

### 12.8 Open items at the snapshot

- **The owner's goal:** next-draw forecasts for the draws of the week of 9 November 2026, through Mode H, the results update and the prospective mode (section 10).
- **The reminders** (`exchange/OWNER_REMINDERS.md`): R-001 the owner's Methods A and B (A installed as E_17's log-age variant; B is E_45 in wave 3); R-002 the NL-means discussion after wave 3; R-003 optional tidy-up of old EX copies in `review/`; R-004 the NIST seed (DONE, approved 31 October 2026); R-005 E_1 revision 2 (DONE); R-006 the deferred performance study (FINAL, inactive; WORKERS-1 moved to WF-1C; PERF-1 brought forward); R-007 EX_111 O01 (cross-check the seed record's reader names; optional); R-008 the verifier's wording when a new file is missing ("unexpected new paths"); R-009 template draft 4 (in DOC-10, pending install); R-010 EX_113 O02 (the runner's failure-detail label; fixed in the template); R-011 a `results/** -text` rule (in DOC-10, pending install); R-012 the cold-read probe findings (all 23 in `exchange/EX_116_Claude/cold_read_probe_findings.md`).
- **The cold-read probes (1 November 2026).** Two fresh helpers, given only the repository, described the results updater and the performance plan; Claude compared them with the record. Findings carried to the **Mode H, update and prospective design**:
  - A1 (critical for the goal): both readers accept only the single version-1 INIT ledger line, so any update stops every run and report until a version-2 reader exists;
  - A2: `HOLDOUT_OPENED_<GAME>.json` (`HOLDOUT_OPENED_V1`) is defined only in code (schema, writer, study-manifest hash, commit), and is permanent, so it also unlocks all later updates;
  - A3: the updater can add the holdout only together with every later draw; the Mode H store is OPEN;
  - A6: production is single-source (Lotterywest only; "there is no manual Lott check in production (owner-decided)", as recorded in `doc/HANDOVER/Claude_Reviewer_Handover_Predictive_Randomness_v10.md` line 250 and carried in H-1 since) while R2-C03 and proposal v0.6 speak of independent evidence and a candidate-then-promotion step: to be reconciled;
  - A7: no written owner procedure for accepting a new master version, a stale lock, a crash between the master replace and the ledger append, or grabs from refused runs;
  - A8: the default window (current month plus five back) stops overlapping the master around January 2027;
  - A9: the data tools have never run under Python 3.15;
  - A11: R3 7.6's "independent outcome ledger" is undefined beside the master ledger.

  Settled or recorded in the snapshot (as register v0.23 lists them): A4 (the bare updater launch, recorded as a warning; the launcher is unchanged); A5 (the two-site checker's Lott automation: decision TSC-1, the checker is never used again; rulebook v0.3 rule 7); A9 (recorded); the rulebook's rule 1 heading (A10, in part); B1, B2 and B5 (corrected in register v0.23); B9 (Architecture v0.9 points 10.1 to WF-1C's design); B12 (PERF-1 recorded). Carried: A1-A3, A6-A8 and A11 to the Mode H design (above); B4, B7, B8, B10 and B11 to WF-1C or the performance study. Left as small wording slips for a later edition: the rest of A10 (proposal v0.6's link to `oz.lotterywest.com`, the checker's "pending ratification" comments). B3 (R-006's unprofiled "4%") and B6 (WF-1C's place in the roadmap) were fixed directly in Claude's working lists with candidate 2.
- **The cold-read test of this file (1 November 2026).** A third fresh helper, given only the repository and this file, explained the project back and listed 20 gaps; candidate 2 fixed them (`exchange/EX_116_Claude/cold_read_h1_gaps.md`). Two needed the owner: HX-2 (section 5.1) and FB-1 (section 10).
- **The owner's binding inputs for the Mode H, results update and prospective design (1 November 2026; register v0.23):**
  - **MH-1, the weekly session per game:** the results update; then catch up every draw that has no forecast, in draw order (predict N from draws up to N-1 only, reveal N, score it); then score any open prospective forecast; then freeze and publish the next draw's forecast, so exactly one forecast is always open. Labels PROSPECTIVE (frozen before its draw) and CATCH-UP (made after it, in order; valid only if the method revision was installed before that draw's date, otherwise ordinary walk-forward evidence), kept apart in records and league tables. One wrapper command per game; the owner's updater and the scoring and forecasting code stay separate programs. The league table is cumulative; no method is retuned because of its ranking. Open: the production report cadence (weekly, monthly or on request).
  - **OFF-1, offline:** everything installed runs without GitHub. Prospective timing evidence is a local, create-only, digest-chained forecast record with timestamps; a GitHub push or an emailed digest is an optional witness only. Catch-up validity is checked against local registry install records, not Git history. Only the results update needs the internet.
  - **EFF-1, efficiency:** the weekly path is incremental (append-only ledgers; only new runs and the new draw; league table from ledgers; N1 over prospective and catch-up draws only). Full rebatches use WF-1C. The report's collect stage (22 minutes for Powerball: it rereads every frozen run record) is a candidate for a cached index in the performance study, with identical results required.
  - **TSC-1:** the two-site checker stays as it is and is never used again.
- **HX-1 and HX-2** (section 5.1): Mode H scores all ten, with Powerball 1585 and 1586 flagged; the holdout is never extended; Powerball 1587 and 1588 are flagged when the catch-up scores them. Flagged draws remain fully valid and counted (no gap); the flag is information only.
- **FB-1** (section 10): if the week-of-9-November forecasts cannot be ready, slip a week rather than rush.
- **Terms to keep straight in that design:** the prospective mode is MH-1's weekly loop; "developed" (GOAL-1) means the pipeline is declared ready for the released cohort; how R3's FINAL mode relates to the loop is OPEN; Mode H is every released variant forecasting each holdout draw walk-forward, frozen before opening, scored once.
- **R3's OPEN items for Mode H and the prospective mode:** R3 section 6.2 (the study manifest, the opening record, combined versus sequential release), section 10 and V1 (the controlled historical holdout), R3-D20 (the timing proof for prospective forecasts; R3 says GitHub push evidence, which OFF-1 makes an optional witness: to be reworded in that design), R3-T50 (no dependency upgrade within Mode H).
- **WF-1C's obligations:** EX_101's four (memory headroom, which bytes must match across worker counts, failure semantics, the default on odd or unknown processor counts) and EX_105's B01 (atomic admission, no prefetch, fail closed on parent loss, no kill) and C02-C05 in full (EX_107).

### 12.9 The first hour in a new chat

1. Clone, read section 0's list, and check the hashes in sections 4 and 7 and Appendix A.
2. Read `exchange/CLAUDE_WEB_TOOLS/README.md`; set up a workspace: a base tree from the current `main` without the data folders, the Python 3.15 venv, and a frozen mirror (12.3).
3. Run the whole suite on Linux in a full disposable clone of the mirror at `main` (12.3), on both Pythons, and check the count against section 7.4 (and the latest register). This proves the tools and the workspace before any change.
4. Read the newest EX messages and the roadmap; list anything in flight (an unanswered EX message, a task report not yet read, an install not yet verified).
5. **Confirm the takeover to the owner** in plain English: where the project stands; the next step as you understand it; the hard rules; anything in this file that did not match the repository; and your questions. Do no work until the owner says so. The owner may ask the reviewer chat to check your takeover reply, as it did for the reviewer's own.
