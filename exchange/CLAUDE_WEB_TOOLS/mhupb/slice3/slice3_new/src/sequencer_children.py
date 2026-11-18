"""MHUP-B layer L8: how the two sequencers start a child (design v0.1r7 section 6.1; code plan v0.3 L8). The rules are
written once, here, and both sequencers use nothing else:

 - a child is started through its launcher (Run_Experiment.bat, Run_Evaluation.bat, Run_Method_Rankings.bat), or, for
   the one process-check tool, directly with the venv's Python and the no-byte-code options;
 - its output is read line by line to the end and echoed, so the pipe never fills; then the sequencer waits for it,
   with no time limit;
 - nothing here ends, stops, inspects or looks up a process. A child that hangs is visible to the owner, who closes
   the console;
 - the child's exit code and its one machine-readable last line (`[TOOL] RESULT key=value ...`) are used for
   sequencing only. The evidence is the records the children write.

This module imports neither the method code nor the evaluator, and holds no state.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT_LINE = re.compile(r'\[[A-Z0-9-]+\] RESULT( [a-z_]+=[^ ]+)+\Z')
SAFE_ARG = re.compile(r'[A-Za-z0-9_.:,=-]+\Z')
LAUNCHERS = {'experiment': 'Run_Experiment.bat', 'evaluation': 'Run_Evaluation.bat', 'rankings': 'Run_Method_Rankings.bat'}
GAMES = ('POWERBALL', 'OZLOTTO')


class SequencerRefused(Exception):
    """Refused before any child was started."""


def expected_venv() -> Path:
    return (ROOT / '.venv').resolve()


def check_environment() -> None:
    """Architecture 5C.1, as the coordinator does: only inside the project's own .venv, started by the launcher."""
    expected = str(expected_venv()).casefold()
    if str(Path(sys.prefix).resolve()).casefold() != expected:
        raise SequencerRefused(f'wrong Python environment: sys.prefix is {sys.prefix}; expected {expected_venv()}')
    active = os.environ.get('VIRTUAL_ENV')
    if not active or str(Path(active).resolve()).casefold() != expected:
        raise SequencerRefused('VIRTUAL_ENV is not this project\'s .venv; start through the .bat launcher')


def command(kind: str, *args: str) -> list[str]:
    """The argument list of one child. Every argument must be plain (letters, digits and _ . : , = -), which is what
    the launchers forward unchanged."""
    args = [str(a) for a in args]
    for a in args:
        if not SAFE_ARG.fullmatch(a):
            raise SequencerRefused(f'an argument is not plain text the launchers forward unchanged: {a!r}')
    if kind in LAUNCHERS:
        return [str(ROOT / LAUNCHERS[kind]), *args]
    if kind == 'process':
        return [str(ROOT / '.venv' / 'Scripts' / 'python.exe'), '-I', '-B', '-X',
                f'pycache_prefix={ROOT / "transitory_data" / "no_pycache_ever"}',
                str(ROOT / 'src' / 'package_tools' / 'process_check.py'), *args, '--root', str(ROOT)]
    raise SequencerRefused(f'unknown child kind {kind!r}')


def parse_result(line: str) -> dict | None:
    """The fields of a machine-readable last line, or None."""
    line = line.strip()
    if not RESULT_LINE.fullmatch(line):
        return None
    return dict(part.split('=', 1) for part in line.split(' RESULT ', 1)[1].split(' '))


def run_child(argv: list[str], echo=print) -> tuple[int, dict]:
    """Start one child, echo its output to the end, wait for it. Returns (exit code, the fields of its last RESULT
    line or {})."""
    child = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                             text=True, encoding='utf-8', errors='replace', bufsize=1, cwd=str(ROOT), shell=False)
    fields: dict = {}
    for line in child.stdout:
        echo(line.rstrip('\r\n'))
        found = parse_result(line)
        if found is not None:
            fields = found
    return child.wait(), fields
