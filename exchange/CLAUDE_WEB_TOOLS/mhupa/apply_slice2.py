"""MHUP-A slice 2: the counted edits to existing root files of a dev tree, and the updater's file rename.

Usage: python3 -I apply_slice2.py <dev tree>

- src/results_master_v0_1.py is removed (v0.2 is copied in by build_dev_slice2.sh from slice2_new; design 7).
- Run_Results_Updater.bat: line 13 (TOOL) and line 47 (error text) name v0_2 (design 7).
- Run_Experiment.bat: the four byte-code-cache changes (a)-(d) of design 4.1.
- Run_Evaluation.bat: written as the mirror of the edited Run_Experiment.bat for src\\evaluation\\ (design 6.1).
- .gitignore: the MHUP-A lines (design 4.2 and the holdout run, attempts and score folders; Appendix J; 6.1).
Every edit anchors on exact text and is counted; CRLF files stay CRLF and ASCII.
"""
import sys
from pathlib import Path

CRLF = b'\r\n'


def replace_counted(data: bytes, old: bytes, new: bytes, count: int = 1) -> bytes:
    n = data.count(old)
    if n != count:
        raise SystemExit(f'anchor found {n} time(s), expected {count}: {old[:100]!r}')
    return data.replace(old, new)


def bat(path: Path) -> bytes:
    data = path.read_bytes()
    data.decode('ascii')
    assert data.count(b'\n') == data.count(CRLF), f'{path.name}: not CRLF throughout'
    return data


def main(dev: Path) -> None:
    # ------------------------------------------------------------ the updater file
    old_tool = dev / 'src' / 'results_master_v0_1.py'
    if old_tool.exists():
        old_tool.unlink()
    assert (dev / 'src' / 'results_master_v0_2.py').is_file(), 'results_master_v0_2.py must be copied in first'

    # ------------------------------------------------------------ Run_Results_Updater.bat lines 13 and 47
    p = dev / 'Run_Results_Updater.bat'
    d = bat(p)
    d = replace_counted(d, b'set "TOOL=%ROOT%src\\results_master_v0_1.py"' + CRLF,
                        b'set "TOOL=%ROOT%src\\results_master_v0_2.py"' + CRLF)
    d = replace_counted(d, b'echo [RUN-RESULTS-UPDATER] ERROR: src\\results_master_v0_1.py not found. >&2' + CRLF,
                        b'echo [RUN-RESULTS-UPDATER] ERROR: src\\results_master_v0_2.py not found. >&2' + CRLF)
    assert b'v0_1' not in d
    p.write_bytes(d)

    # ------------------------------------------------------------ Run_Experiment.bat (a)-(d)
    p = dev / 'Run_Experiment.bat'
    d = bat(p)
    lines = d.split(CRLF)
    assert lines[-1] == b'' and len(lines) == 78, len(lines)
    assert lines[29] == b':verify_python' and lines[31] == b'if errorlevel 1 goto :prefix_failed'
    assert lines[40] == b'"%PY%" -u %*' and lines[68] == b':prefix_failed' and lines[71] == b'goto :finish'
    # (d) first, so the earlier indices stay valid; then (c), (b), (a)
    lines[72:72] = [b':pycache_present',
                    b'echo [RUN-EXPERIMENT] ERROR: transitory_data\\no_pycache_ever exists; refusing to run. >&2',
                    b'set "RC=10"',
                    b'goto :finish']
    lines[40] = b'"%PY%" -B -u %*'
    lines[32:32] = [b'set "PYTHONPYCACHEPREFIX=%ROOT%transitory_data\\no_pycache_ever"',
                    b'if exist "%PYTHONPYCACHEPREFIX%" goto :pycache_present']
    lines[30:30] = [b'set "PYTHONDONTWRITEBYTECODE=1"']
    d = CRLF.join(lines)
    p.write_bytes(d)

    # ------------------------------------------------------------ Run_Evaluation.bat: the mirror
    e = d
    e = replace_counted(e, b'rem Human-facing AND provisional coordinator-facing experiment runner (Option F).',
                        b'rem Evaluator launcher (MHUP-A design 6.1): the mirror of Run_Experiment.bat for src\\evaluation\\.')
    e = replace_counted(e, b'[RUN-EXPERIMENT]', b'[RUN-EVALUATION]', count=d.count(b'[RUN-EXPERIMENT]'))
    e = replace_counted(e, b'if not exist "%ROOT%src\\methods\\%SCRIPT_NAME%" goto :missing_script',
                        b'if not exist "%ROOT%src\\evaluation\\%SCRIPT_NAME%" goto :missing_script')
    e = replace_counted(e, b'pushd "%ROOT%src\\methods"', b'pushd "%ROOT%src\\evaluation"')
    e = replace_counted(e, b'echo Usage: %~nx0 POC_Architecture_Probe.py --poc --case=echo-argv [options] >&2',
                        b'echo Usage: %~nx0 Method_Mode_H.py statements [options] >&2')
    e = replace_counted(e, b'First argument must be a filename like POC_Architecture_Probe.py',
                        b'First argument must be a filename like Method_Mode_H.py')
    e = replace_counted(e, b'ERROR: Experiment Python file does not exist in src\\methods:',
                        b'ERROR: Evaluation Python file does not exist in src\\evaluation:')
    e = replace_counted(e, b'ERROR: Could not enter src\\methods.', b'ERROR: Could not enter src\\evaluation.')
    e = replace_counted(e, b'rem Pin numerical library threads before the experiment imports NumPy / SciPy.',
                        b'rem Pin numerical library threads before the evaluator imports NumPy / SciPy.')
    assert b'methods' not in e and b'EXPERIMENT' not in e, 'the mirror still names the method side'
    e.decode('ascii')
    (dev / 'Run_Evaluation.bat').write_bytes(e)

    # ------------------------------------------------------------ .gitignore
    p = dev / '.gitignore'
    g = p.read_bytes()
    assert b'\r' not in g and g.endswith(b'\n')
    block = (b'\n'
             b'# MHUP-A (design 4.2, Appendix J, 5.1-5.4, 6.1): the updater\'s local working files (covered by the owner\'s\n'
             b'# backups), the two install barriers, the Mode H holdout contract runs, each batch\'s attempts log and the\n'
             b'# score ledgers (they hold drawn numbers; the plan, the batch-id record, the lifecycle markers, the study\n'
             b'# manifest and the owner records are committed), the lock clearance records and the byte-code sentinel\n'
             b'source_data/backups/\n'
             b'source_data/grabs/\n'
             b'source_data/.results_master.lock\n'
             b'src/methods/E_001/IN_DEVELOPMENT.txt\n'
             b'src/methods/_common/contract_data/INSTALL_IN_PROGRESS.txt\n'
             b'results/real/holdout/contract_runs/\n'
             b'results/real/holdout/wf_batches/**/attempts.jsonl\n'
             b'results/real/holdout/scores/\n'
             b'transitory_data/lock_clearances/\n'
             b'transitory_data/no_pycache_ever\n')
    if block not in g:
        g += block
    p.write_bytes(g)
    print(f'{dev}: slice 2 root-file edits applied')


if __name__ == '__main__':
    main(Path(sys.argv[1]))
