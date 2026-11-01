# CLAUDE_WEB_TOOLS - the Claude web chat's working tools

Kept by the Claude web chat; committed to `exchange/CLAUDE_WEB_TOOLS/` so that a new Claude chat (or anyone) can
rebuild packages, evidence and task files the same way. These are working tools, not project code: they are not
reviewed as code, never run by the project owner or Claude Code, and nothing in `src/` or `tests/` imports them.
Copies of the build and mutation tools that shipped inside an install package are also under that package's
`review/<PACKAGE>/tools/` folder (those are the reviewed copies). US-ASCII; the `.py` and `.sh` files keep LF.

## Where the tools expect things (hard-coded paths)

The tools were written in one cloud workspace. Several have absolute paths near the top; edit them for a new
workspace before use:

| Path in the scripts | What it was |
|---|---|
| `/home/claude/analysing_perceived_randomness_in_reality` | the Claude chat's clone of the repository (`REPO` / `R`) |
| `/home/claude/work/wf1code` | folder holding `verifier_template.py` and `suite_template.py` (`WH`); here they are in `wf1/` |
| `/home/claude/work/wf1bcode`, `/home/claude/work/perf1code` | the WF-1B and PERF-1 build folders (`HERE` / `H`): the builder, `test_counts.txt`, `ev/` (evidence copied into the package), `tools/`, `docs/` |
| `/tmp/claude-0/-home-claude/<session>/scratchpad` | the session scratchpad: dev trees, base trees, the frozen mirror, the Python 3.15 venv |

Scripts that take their trees and output folders as arguments have no other hidden paths.

## The recipe every code package follows

1. **Base tree:** `git archive <BASE_COMMIT> | tar -x -C BASE`, then delete `BASE/source_data`, `BASE/results` and
   `BASE/transitory_data` (Claude never reads those folders).
2. **Dev tree:** a copy of the base tree, plus the package's changes. Develop and run tests there with
   `PYTHONPATH=src:src/methods:tests python3 -B -m unittest tests.<module>`.
3. **Mutation checks** (`<pkg>/tools/*_mutations.py DEV_TREE`): each planted defect must make a named test fail.
   Each mutant runs in a temporary copy of the dev tree; the dev tree itself is never changed. Use `unittest -f`
   (fail fast) so slow suites stop at the first failure (the PERF-1 tool does).
4. **Build** (`build_*_pkg.py DEV BASE OUTDIR BASE_COMMIT`): checks that only the expected new and replaced files
   differ, writes `repo_overlay/`, the install manifest (LF Git-content SHA-256), the verifier (from
   `wf1/verifier_template.py`), the suite runner (from `wf1/suite_template.py`, with the expected per-module test
   counts from `test_counts.txt`) and `INSTALL_INSTRUCTIONS.md` (CRLF).
5. **Rehearse** (`e2e_*.sh MIRROR PKGDIR WORKDIR [PYTHON]`): disposable clones of a frozen mirror of `main`, in LF
   and CRLF (`core.autocrlf=true`), each running PRE, the copy, POST, the full suite, stage, commit and COMMITTED;
   then the negatives, each of which must STOP. Run it under Python 3.13 and 3.15.
6. **Assemble the EX message** (`assemble_ex*.py`): zips the package with `exchange/EX_019_Claude/make_zip.py`
   (deterministic zip plus a member list with SHA-256 as stored and after CRLF to LF), fills the EX template's
   `@@...@@` placeholders, adds the member table, makes the EX zip and copies everything to `exchange/EX_NNN_Claude/`.
7. **Task file for Claude Code** (`make_t0NN.py ZIP_PATH ZIP_SHA N_NEW N_MOD SUITE_N BASE OUT`), then
   **always** `cc/check_task_vs_deny.py .claude/settings.json TASK_FILE` before committing it.

## The tools

| Tool | What it does |
|---|---|
| `wf1/verifier_template.py` | The read-only install verifier (phases pre, post, committed); the builders fill in BASE, the new/modified/deleted maps and the guarded files. |
| `wf1/suite_template.py` | The suite runner: each test module in its own `python -B -m unittest -v` process, compared with the expected counts; only symlink skips on the listed modules are allowed; a failing module prints its failure output ("inspect before sharing"). |
| `wf1/build_wf1_pkgs.py`, `wf1/e2e_wf1.sh` | REL-1 and WF-1A package builder and rehearsal (31 October 2026). |
| `wf1b/build_wf1b_pkg.py`, `wf1b/e2e_wf1b.sh` | WF-1B package builder (v3) and rehearsal. |
| `wf1b/assemble_ex112.py` | Assembled EX_112 (pattern for any EX message carrying a package). |
| `wf1b/make_t012.py` .. `make_t014.py` | Generators of TASK_T012 to T014. T013/T014 name the `.bat` wrapper only by the pattern `Run_Method_Rankings.*`, because `.claude\settings.json` refuses any command containing `.bat`. |
| `wf1b/tools/make_wf1b_registries.py` | Builds `src/evaluation/registry/MEASURE_REGISTRY_V1.json` and `FAMILY_REGISTRY_V1.json`. |
| `wf1b/tools/wf1b_mutations.py` | WF-1B's 23 mutants. |
| `perf1/build_perf1_pkg.py`, `perf1/e2e_perf1.sh`, `perf1/assemble_ex114.py`, `perf1/make_t015.py` | The same four for PERF-1 (replaced files instead of new ones; seven negatives). |
| `perf1/tools/perf1_mutations.py` | PERF-1's 9 mutants (fail-fast). |
| `perf1/tools/profile_stats.py` | Profiles the report's statistics stage (N1 runner and measures) at full size on INVENTED data: `PYTHONPATH=src:src/methods python3 profile_stats.py GAME [R]` from a dev tree. |
| `cc/check_task_vs_deny.py` | `check_task_vs_deny.py SETTINGS TASK`: matches every command line in a task file's code blocks against the settings' `Bash(...)` deny patterns (fnmatch on the whole line); exit 1 on any match. |
| `seed/check_pulse.py` | Checks a saved NIST Beacon pulse file against EX_103's acceptance row (version, chain, timestamp, status, 128 upper-case hex). The timestamp is that policy's; edit it for a new policy. |
| `register/make_register_v22.py` | Made register v0.22 from v0.21 by counted in-place edits (every old string must occur exactly once). The pattern for later editions. |
| `register/build_doc9.py` | DOC-9, the document-only install package for a register edition. |
| `handover/make_h1_v1r6.py`, `handover/make_h2_v1r7.py` | Made the handover editions by counted edits; H-2's reviewer-rights sections must stay byte-for-byte. |

## The frozen mirror and the Python 3.15 interpreter

- **Mirror:** `git clone --mirror <repo> scratchpad/repo_snapshot.git`; refresh with
  `git -C repo_snapshot.git fetch <local clone> main:main`. The rehearsals clone `main` from it.
- **Python 3.15:** the rehearsals used Python 3.15.0b4 in a uv virtual environment (`pyvenv.cfg`: uv 0.11.32,
  uv-managed CPython 3.15), with numpy 2.5.4, scipy 1.18.1 and psutil installed. To recreate it (if pip and uv
  can reach the package index): `uv python install 3.15` then `uv venv --python 3.15 scratchpad/v315` and
  `uv pip install --python scratchpad/v315/bin/python numpy scipy psutil`. The owner's Windows venv is Python
  3.15.2; the Linux rehearsals are evidence, the Windows rehearsal (Claude Code) is the acceptance.

## Gotchas learned the hard way

- **Never `pkill -f unittest`** (or any pattern that matches your own shell's command line): it killed the shell
  twice (exit 144). Find PIDs with `ps -eo pid,cmd` and kill those.
- **Run the e2e rehearsals one after another.** Two clones made in parallel from a freshly fetched mirror failed
  with "tmp_pack missing".
- **Long jobs:** the Bash tool times out at 2 minutes by default (10 at most). Start long jobs with `nohup ... &`,
  write output to files, and poll with short `sleep`s.
- **Do not import or run package scripts in place** for probes: a `__pycache__` folder appeared in the package and
  ended up in a zip. Copy first, or check `find pkg -name __pycache__` before zipping (assemble_ex114 asserts it).
- **Task files:** `.claude\settings.json` refuses any Bash command containing `.bat` (and many other patterns);
  always run the deny check. Claude Code also cannot write a report through a shell heredoc whose text contains a
  refused word; it uses its file-writing tool.
- **Windows tests:** creating a symbolic link needs a privilege Windows does not give by default. Guard every
  `symlink_to`/`os.symlink` with `except (OSError, NotImplementedError): self.skipTest('platform disallows
  symlinks')`, and list the module in the runner's allowed-skip set. Hard links (`os.link`) work on NTFS.
- **Line endings:** `.md` files exchanged with the reviewer are CRLF; package source files are LF; the owner's Git
  has `core.autocrlf=true`, so Git can rewrite committed record files with CRLF on his PC (see reminder R-011).
- **Helpers (Agent tool) are blocking** and are stopped if the owner sends a message while they run.

## snapshot/ (added 1 November 2026)

The DOC-10 snapshot tools: build_doc10.py (package builder), e2e_doc10.sh (rehearsal), assemble_ex116.py (EX assembly; --to-exchange off by default), and the document generators make_register_v23.py, make_arch_v09.py, make_h1_v1r7.py (uses section12.md, kept in the package review folder), make_blurbs_v1r7_v1r8.py and make_h2_v1r8.py. Copies are also in review/DOC10_Snapshot_v1/ once the snapshot is installed. Hard-coded paths are under /home/claude/work/snap/.
