# HO-2 - third cross-check by the predecessor Claude chat

Date: 10 November 2026 (Adelaide)
Project: hydra3333/analysing_perceived_randomness_in_reality
Checkpoint: main c48ac3c393d2eab30014e6200d427b76d90f47ac (verified as HEAD of my read-only clone)
Exchange number: none. Nothing was built, run, committed or pushed. No data folder was opened.
For: the ChatGPT reviewer, via the project owner. Not for the replacement Claude until the owner decides.

## 0. What I received, and the limits of this check

**v0.2 (same evening):** v0.1 was written before I had the replacement's answers. The owner has now sent the blind answers
file, and section 1a is my pass over its exact wording. F5, F6 and section 3 are adjusted to match. No other finding changed.

**Received from the owner:**
- the forwarding blurb (v0.1);
- ChatGPT's independent assessment (v0.1);
- ChatGPT's post-hoc suggested-answer comparison (v0.1);
- `HO2_NewClaude_Blind_Answers_v0_1-2026.11.10.md`. I verified it independently:
  - 24,792 bytes, US-ASCII, CRLF;
  - SHA-256 as stored `14b495be38d3d1ddd349dc53cc25fe60d48a1409c0c8926e5fa4ce91c81ccebf`;
  - SHA-256 after CRLF -> LF `e5e30914...`.
  Both hashes match ChatGPT's.

**Not received:** the replacement's POST, the nine questions and the original pre-answer key. I read each question from its
answer.

**Checked myself, read-only, at c48ac3c:**
- `.claude/settings.json`;
- `exchange/CLAUDE_WEB_TOOLS/check_task_commands.py`;
- the rulebook v0.4;
- design v0.1r6: sections 4.1, 4.4, 6.1 and 8, and Appendices J and L;
- `exchange/MHUP1_design_amendment_A1_RATIFIED.md`;
- register v0.26: future actions 1-3, and the line about the deny lines;
- R-020 in `exchange/OWNER_REMINDERS.md`;
- `integrated/PLAN.md`;
- H-1 v1r10r3 delta, sections 4.9, 6 and 7;
- `outbox/REPORT_T022.md`;
- the candidate's `slice2_new/src/methods/_common/closure.py`.

The only look at the data folders was a count of tracked path names (`git ls-files`), with no file contents read.

## 1. Disposition

**No BLOCKER to the takeover.** On the evidence ChatGPT describes, I agree with PASS on Q1-Q9.

I checked A1's order and recovery states against A1 itself:
- section 2: one read after `SCORING_STARTED`; the whole ledger published create-only; that published ledger validated
  before `SCORE_COMPLETE`, which holds its digest; then the report, resumed file by file; then `MODE_H_SEALED`;
- section 4: re-reading is allowed only before publication; after publication there is no read; after `SCORE_COMPLETE`,
  report and seal only;
- section 6: corrections go through MHUP-B's route.

The handover and the answers as described match all of this.

I also confirmed:
- C01-EFF and its four affected files;
- the ten gate files;
- DEP-1 and GAIS-1;
- that `create_venv.bat` is inside the closure.

## 1a. Verbatim pass over the replacement's answers (v0.2)

The answers are accurate. I found no factual error that bears on the takeover.

I spot-checked these against the repository:

| Claim | Where | My check |
|---|---|---|
| Since `009c985`, the only change outside `exchange/`, `GAIS/`, `doc/` and the Claude Code folder is the root `README.md` | Q5 | `git diff --name-only 009c985 c48ac3c` agrees |
| T022 had 4 allowed symlink skips | Q1 | 4 skip lines in `REPORT_T022.md` |
| The closure is enumerated from the disk | Q5's "reading to confirm" | Confirmed by the candidate's `closure.py` (`os.walk` of `src/`; root `glob('*.bat')`) |
| No settings deny line names either tool; the only related entry is `*results_master*` | Q6 | Agrees |
| The release sequence: COMMITTED at step 13, then step 14, E then P at step 15, the release record at 16 (refusing while P exists), the release commit at 17, U at 18, push at 19 | Q7 | Exactly Appendix J |
| The `released` phase checks "E and P are absent and U still holds this package's content" | Q7 | Correct |

The Q7 order also means F5 is not a fault in the replacement's answers.

Three small points:
- **Q8**, on MHUP-B timing, says "never while a holdout is opened and unsealed".
  - Design 4.4's window starts at **Approval 1** (the study manifest freezes the closure), which comes before the holdout is
    opened at Approval 2.
  - It also applies across games (F6).
  - Effect: a wording correction for the install plan, not a takeover issue.
- **Q6** says "steps 3 and 18 act on the clone's own lock path". That lock path is `<clone>/source_data/.results_master.lock`,
  which is exactly the rule 2.5 collision in F2.
  - Q6's controls list covers copying files with denied names, but not staging them at step 12 (F4).
  - Q6 states the rule change is "reviewed with the integrated package", which runs into F3.
  - The replacement inherited these gaps from my H-1 delta. They do not show a misunderstanding.
- **Q6** correctly treats the deny-line order as unsettled. It did not cite the register's line saying the deny lines are
  "made with MHUP-A's install", which already settles the order (F1).

Not checked: the development-report P-values in Q1 (taken from repository records) and the "B05" field details in Q2-Q3. Both
are consistent with what I know; I did not recompute them.

The findings below concern **later package work** (items 2, 5 and 6 of the H-1 delta's section 7). Several of them are
omissions shared by my own handover, the replacement and ChatGPT. None needs another blind round.

## 2. Findings

### F1 - CORRECTION (later: items 5-6). The settings-deny/T016 conflict is real. The documented timing already avoids it, but must be made explicit, together with where the edit is committed.

**Verified:**
- At c48ac3c, `.claude/settings.json` has no Bash denial for any of:
  - `process_check`;
  - `install_records`;
  - `Method_Mode_H` / `mode_h`;
  - `Method_Walk_Forward`.
  Rulebook v0.4 rule 7 is the only barrier for these today. `Method_Walk_Forward.py` already exists on main.
- Register v0.26 future action 1 (in the section "Inside it") plans settings deny patterns for `process_check.py`.
- The register's later line on this says these deny lines are "the owner's edit, made with MHUP-A's install". The install
  comes after T016, so the documented timing already avoids the conflict.
- `check_task_commands.py` checks only the settings `Bash(...)` denials, matched with fnmatch over each command line. It
  never reads the rulebook. A PASS from it therefore says nothing about rulebook compliance.
- In the settings file, deny wins over allow. No exception for T016 can be expressed there.

**Safest compatible sequence (no bypass):**
1. Add the deny lines for the two T016 tools only after T016's final accepted run on the final candidate.
2. Make that edit a **separate owner commit, before Appendix J step 0**, not during steps 0-19. Step 0 needs a clean tree,
   and step 12 needs `git status --short` to show exactly the manifest's paths, which do not include the settings file.
3. Deny lines for MHUP-A programs that T016 never names can be added at any time, and earlier is safer. These are
   `Method_Mode_H`, `mode_h` and `Method_Walk_Forward`.
4. Some are already covered:
   - `Run_Evaluation.bat` and `create_venv.bat`, by `Bash(*.bat*)`;
   - the updater v0.2, by `Bash(*results_master*)`.
5. Rulebook v0.5 should say that the T016 allowance lapses once those two deny lines exist. Any T016 rerun after that needs
   the owner to remove the lines openly, which is a new owner decision and never a workaround.
6. Test every proposed pattern with `check_task_commands.py`:
   - against the real T016 task file, expecting PASS;
   - against negative command lines, expecting STOP.

**Caution:** the staging folder mirrors the repository's layout (`repo_overlay/src/package_tools/process_check.py`). A
path-shaped pattern such as `*src\package_tools\process_check.py*` would therefore also match the staging copy. Timing, not
pattern cleverness, is what keeps the two apart.

**Disagreement with ChatGPT's section 4:** it presents the timing as open. The register already sets the timing; what is
missing is stating it, and placing the commit.

**Effect:** none on HO-2.

### F2 - CORRECTION (later: items 5-6). Under option (i), T016 also collides with rulebook rules 2.5 and 9 and with T016 evidence the design requires. Nobody has listed this, including my H-1 delta.

**Rule 2.5:** "Never read anything under any `source_data`, `results` or `transitory_data` folder, in the main repository or
in any clone." Yet Appendix J:
- steps 3 and 18 take and release U at `source_data/.results_master.lock`;
- the install check reads, under `results/real/weekly/`:
  - the `ACTIVE_SESSION.lock` files;
  - the weekly attempts ledgers;
  - the forecast ledgers.

A `cc_clone.py make` clone is a full GitHub clone. It carries the tracked files under:
- `source_data/` (6);
- `results/` (20);
- `transitory_data/` (7).

PLAN.md item 5 says "a synthetic `source_data` lock path in the clone", and R-020 (g) says "T016's synthetic clone". No
document defines either. Rulebook v0.5 and the T016 task must define them, and the reviewer must check the definition. One
possibility: the tools point at a synthetic root that holds no real data.

**Rule 9 ("No Windows lifecycle tests") and design section 6.1:** the design says "T016 must also show the preflight prints
`CLEAN` on the owner's ordinary desktop with Claude Code and a console open at the root; T016 must show on Windows that a
live `Run_Experiment.bat` child is listed" (also L-I4 in Appendix L). Neither fits option (i):
- Launching `Run_Experiment.bat` is forbidden by rule 7, denied by `*.bat*` and `*Run_Experiment*`, and outside option
  (i)'s two tools.
- The "console at the root" check means the real project root, while option (i) confines `--root` to the clone.

**Remedy:** the T016 design (item 6) maps each piece of T016 evidence the design requires to who runs it:
- Claude Code, under v0.5;
- the owner, by hand (option (ii) for that piece);
- or a reviewed substitute.

**Effect:** none on HO-2.

### F3 - CORRECTION (later: sequencing). "Reviewed with the package" and T016 cannot both happen before EX_163.

The runner reads its rulebook from the main repository's `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md`. T016 cannot run until
v0.5 is ratified and committed on main. If v0.5 is reviewed only inside EX_163, then EX_163 cannot carry T016's evidence.
There are two clean routes; the owner chooses, and R-020 (g) is unchanged either way:
- **(A)** A short separate review of rulebook v0.5 plus the T016 task file. Then the owner's go and T016. Then EX_163, with
  the T016 evidence.
- **(B)** EX_163 is provisional as to Windows (H-1 section 7 item 7 already allows this). Then v0.5, then T016, then an
  evidence RECHECK before install.

The condition "no change to the main repository" applies to T016 itself, not to committing the rulebook.

### F4 - CORRECTION (later: item 2, the builder, and item 6). The Git steps that the deny list blocks.

**Step 12 staging.** `Bash(*results_master*)` denies any command line that names:
- `src/results_master_v0_1.py` (deleted by the package);
- `src/results_master_v0_2.py` (added by the package).

H-1 section 7 item 6 covers copying ("copied by the copy tool ... never named on a command line"). It does not cover staging
the deletion and the addition at step 12. The builder needs a staging route that names neither path on a command line, for
example a pathspec file read by Git, run through `cc_clone.py git` in T016. The owner's own instructions should use the same
route, so that T016 rehearses the owner's real lines.

**Step 0.** `git pull --ff-only` cannot run in a task clone: the clone has no remote, and `git pull*` is denied. T016 and the
LF/CRLF rehearsals must state what replaces step 0's pull. Step 19 is already omitted.

### F5 - CORRECTION (wording: ChatGPT's comparison Q7, and my H-1 delta). The order of barriers and commits.

Appendix J gives this order:

| Step | What happens |
|---|---|
| 13 | COMMITTED (the package commit) |
| 14 | The install check |
| 15 | Delete **E, then P** |
| 16 | The release record. It refuses while P exists and before COMMITTED PASS |
| 17 | The release commit, checked by the `released` phase |
| 18 | Release U |
| 19 | Push |

On a failure at step 16 or 17, P is re-created.

**ChatGPT's comparison, Q7,** says: "separate release record, parent-only release commit, E/P removed and U held through
release, then U released, then push". Read in sequence, that puts E/P's removal after the release commit. In fact E and P go
first.

**My H-1 delta, section 6 item 5,** says "(ix) COMMITTED PASS proves both commits". That is imprecise. EX_148 (ix) asks the
integrated verifier to prove both commits. COMMITTED (step 13) comes before the release commit exists; only the `released`
phase (step 17) checks the release commit. The delta's section 7 item 3 states this correctly.

**Remedy:**
- the builder follows Appendix J;
- fix the delta's wording at the next full H-1 edition;
- (v0.2) The replacement's own Q7 answer gives the order correctly (section 1a).

**Effect:** none on HO-2.

### F6 - OPTIONAL (owner operations; Approvals 1-4). "Never between" is per game, and covers every change to the frozen closure or environment, not only MHUP-B.

**Verified in the candidate's `closure.py`.** The closure is:
- an `os.walk` of `src/`, excluding `__pycache__/`;
- every root `*.bat`;
- `requirements.txt`;
- the dependency installer.

The walk reads the disk, not Git, so untracked files under `src/` count. This settles the replacement's "reading to
verify". The root `*.bat` rule is why `create_venv.bat` is in the closure.

The environment freeze covers:
- the Python version;
- `pyvenv.cfg`;
- the base installation's `python.exe`, DLLs and its `DLLs/` and `Lib/` trees;
- the venv's `Scripts/`;
- every file in site-packages.

**So, while any game is between its Approval 1 and its seal, none of these may happen:**
- any package install;
- a new or edited root `.bat` (OUTLANDISH `.bat` files belong in `GAIS/`);
- a stray file under `src/`;
- any pip, `create_venv` or dependency change;
- a base-Python patch upgrade (T022 recorded Windows Python 3.15.2).

Mode H fails closed (it refuses), but an interpreter upgrade may be hard to undo, and a game that has been blocked has no
provided way to abandon its study (design 4.1).

**Per-game nuance (ChatGPT asked about this).** Design 4.4 is written "for each game". Its text allows MHUP-B to install
after Powerball's seal and before Oz Lotto's Approval 1. The two studies would then freeze different closures, which their
reports must disclose. It is not allowed once Oz Lotto is past its Approval 1. The integrated install plan should state this
per-game reading, with the window starting at Approval 1 (section 1a, on Q8's wording).

### F7 - OPTIONAL (owner operations; from the freeze to the install). Overlay paths are frozen.

The package's `.gitignore` is a whole-file copy (R-020 (d)), and PRE checks the base bytes. After the date and base are
frozen, an owner edit to `.gitignore`, or to any other overlay path, either makes PRE STOP or forces a new candidate with all
evidence redone. OUTLANDISH commits that stay within `GAIS/` and `doc/` are harmless. Tell the owner this at the freeze.

### F8 - OPTIONAL (approval scope). Agree with ChatGPT on E2R-T12.

H-1 v1r8 section 7.4 says E2R-T12 needs "the owner's approval for each run context". A yes given on 10 November covers the
new chat's cloud-workspace suite runs only. It does not cover:
- T016, which is Windows and needs its own task file and go;
- the reviewer's reproduction, which EX_163 must list explicitly (EX_155 Q15).

The owner should confirm the scope in one line in the new chat.

### F9 - OPTIONAL. R-020 (g) is a T016-only allowance.

Register v0.26 future action 3: MHUP-B's Windows rehearsal T017 ("the first production contract run launched from a Python
parent") will meet the same question. By then the `process_check.py` deny line will exist (F1). Do not read (g) as a
standing allowance. T017 needs its own owner decision.

## 3. Points of disagreement with ChatGPT's key and assessment

1. **Q7:** the order wording (F5). The wording at fault is in ChatGPT's comparison, not in the replacement's answer.
2. **Section 4 / Q6:** the timing of the deny lines is already set by the register. The fix is to state the timing and place
   the commit, not to design pattern exceptions (F1).
3. **Missed by all three of us** (my H-1 delta included): F2, F3 and F4. Also F6's widening of "never between" beyond MHUP-B.

Everything else in the key, I agree with:
- A1;
- C01-EFF;
- the ten gate files;
- DEP-1 and GAIS-1;
- Q8's separation of approvals.

One small precision on Q2's "single outcome read": A1 section 4 allows a re-read after a crash **before** publication. "Once"
means once per accepted ledger, as ChatGPT's own Q3 entry says.

## 4. Recommendation

1. The owner may **close HO-2**.
2. Separately, the owner may authorise **only items 1-2**: the current-main rebuild, an optional preliminary suite, and the
   package builder. With that, confirm the scope of E2R-T12 (F8).
3. Hand F1-F5 to the new chat as inputs to its own items 2, 5 and 6:
   - the builder's staging route;
   - the draft of rulebook v0.5;
   - the T016 evidence mapping;
   - route (A) or (B).
   The reviewer then checks them at the v0.5 review or at EX_163.
4. F6 and F7 go into the owner reminders at their next edit.

This recommendation does not widen any authority: rulebook v0.5, T016, install, holdout access, master updates and real runs
each still need their own approvals.
