# Windows POC — first P0 source package v0.1

**Status:** Source candidate for review and first operator-controlled Windows P0 execution. **NOT Windows-tested, and not accepted Option F.** No genuine E-method or lottery computation is implemented. Based on the attached repository ZIP `analysing_perceived_randomness_in_reality-main(3).zip`; the ZIP does not identify a Git commit.

## Contents and what is deliberately deferred

This ZIP is a **repository-relative overlay**, not a complete replacement repository. Install at the root of `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality` after inspecting the files.

| File/path | Action |
|---|---|
| `install_upgrade_dependencies_into_venv.bat` | Add self-contained direct PyPI list; `VERIFY` / `INSTALL` / `UPGRADE` modes. |
| `Run_Experiment.bat` | Add protected standalone experiment launch; provisional common launch path. |
| `src/methods/POC_Architecture_Probe.py` | Add non-scientific P0 probe for argv, synthetic canonical output, exit status and bounded verbose output. |
| `src/methods/_common/*.py` | Add small path, runtime identity, status/metrics and JSON helpers. |
| `tests/fixtures/poc_canonical_fixture.json` | Add synthetic-only fixture. |
| `tests/p0_static_checks.py` | Add non-Windows static check; does not pretend to test CMD. |
| `.gitattributes` | Add `*.bat text eol=crlf`. |
| `.gitignore` | Retain existing rules; append only `transitory_data/poc_runs/` and `transitory_data/dependency_snapshots/`. |
| `activate_venv.bat`, `deactivate_venv.bat` | Preserve their existing contents, converting **line endings only** from LF to CRLF. |

**Deliberately not yet included:** `Run_Coordinator.bat`, `src/Powerball_Experiment_Coordinator.py`, six-worker concurrency, timeout/supervisor implementation, synthetic process-kill tests and the full W-01–W-25 execution suite. Those follow in P1/P2 once standalone Windows behaviour is observed. Do **not** mark P0/P1/P2 or ERR-R2-02 accepted on this package alone.

**Existing files unchanged:** `requirements.txt` (historical, **not authoritative**), existing scraper, CSV data, ratified documents, README, VS Code configuration and result placeholders. No Python module imports source data.

## Windows operator commands — first safe sequence

From an ordinary Windows CMD at the project root (or an activated VS Code terminal):

```cmd
python tests\p0_static_checks.py
install_upgrade_dependencies_into_venv.bat INSTALL
install_upgrade_dependencies_into_venv.bat VERIFY
Run_Experiment.bat POC_Architecture_Probe.py --poc --case=echo-argv --note="hello,world;demo" --history=100
Run_Experiment.bat POC_Architecture_Probe.py --poc --case=canonical-fixture
Run_Experiment.bat POC_Architecture_Probe.py --poc --case=exit-code --exit=3
echo Expected failure exit 3; observed %ERRORLEVEL%
```

`INSTALL` invokes pip **deliberately** and may install missing packages; `UPGRADE` is explicitly requested and may update package versions. With **no argument**, the dependency script uses `VERIFY` and does not install or upgrade. No wrapper automatically downloads dependencies. If you are using a different project's virtual environment, wrappers should refuse rather than silently switch.

Each successful probe writes `transitory_data\poc_runs\<generated-run-id>\status.json` and `canonical_result.json`. Each run has a different status/provenance identity. The canonical fixture data is independent of time, PID and worker count. A `--run-id` can be supplied for a deliberately named disposable test; existing run IDs should be rejected. POC output must **never** be treated as a Powerball prediction.

The dependency script's source contains the single editable direct PyPI package list: `requests`, `beautifulsoup4`, `psutil`, `numpy`, `scipy`, `threadpoolctl`. It generates a Python/version/package/script-hash snapshot beneath ignored `transitory_data\dependency_snapshots`. The existing pinned `requirements.txt` has deliberately been preserved for a later explicit historical-file decision; **do not maintain it as a parallel authority**.

## Validation claims and limitations

- Static checks and Python compilation completed under the authoring environment.
- **Not yet tested on Windows:** `.bat` activation, `cmd.exe` quoting (`=`, comma, semicolon, spaces), stdout piping, subprocess PIDs, Ctrl+C, process tree, and Windows-specific `os.rename` refusal to overwrite existing destination files.
- Do not feed metacharacters such as `%`, `^`, `&`, `|`, `<`, `>` or `!` through the batch interface; they remain outside the accepted P0 argument contract until tested and/or properly rejected.
- The first filename must be a basename containing ASCII letters, digits and underscores, ending `.py`. No paths or arbitrary command executables.
- The result no-overwrite protection uses preflight checking plus `os.rename` on Windows. **W-23 must verify the no-clobber semantics**; concurrent same-run-id races are not claimed resolved by P0.
- Optional process metrics use `psutil` if installed and explicitly record `UNAVAILABLE` where not available; without `INSTALL`, full process-memory testing is not available.
- Existing LF batch files are supplied with CRLF bytes; verify final Windows checkout and `git` line-ending behavior independently.
- `--case=exit-code --exit-style=hard` deliberately invokes `os._exit(7)`, leaving STARTED-only evidence; use only within explicit negative testing, not during casual runs.

## Evidence requested before next phase

Record the commands and outputs, `git rev-parse HEAD`, `git status --short`, `python --version`, the wrapper's printed virtual-environment identity, the returned `ERRORLEVEL` for deliberate failures, and any unusual CMD quoting or terminal behaviour. Return these logs for review before we extend the coordinator.

Keep Option F **provisionally approved, conditional on full Windows W-suite testing and review**. The package contains no six-worker or process-tree supervisor and cannot close that acceptance gate.
