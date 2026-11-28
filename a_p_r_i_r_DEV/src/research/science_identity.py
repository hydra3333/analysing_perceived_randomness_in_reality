"""The science identity: one small file a game saying what its stored science was made from.

What this file is for
    At the end of each game's work the research job has read the accepted results, worked every stored score out
    again from them (supplementary numbers included), dropped what no longer followed, filled what was missing
    and made both OV-1 series again. Only then does it write this file, beside the game's results: the SHA-256 of
    the accepted results file, the engine's fingerprint, each method's fingerprint and status, how far its lines
    run, the size and SHA-256 of each of its list files and of both series files, and why the second OV-1 series
    stopped early (or an explicit null when it did not). The reporting part, which only reads, works the same
    identity out from the files as they are now and makes no report unless the two agree. So a report is never
    made from science that no longer follows from the accepted results, and the reporting part never scores.

    It is one plain file, written whole and made again by every job; it is removed when a game's work begins, so
    that a job that stops part way leaves no identity behind. Nothing in a forecast, score or series line
    changes, and nothing is chained.

Which part of the design it carries out
    doc/Predictive_Randomness_Reporting_Design_And_Specification_Amendment_A1_v0_5.md (RAT-74) A2 (what the
    reporting part refuses) and A11 (the reason the second series stopped); the reviewer's C03 on the code plan
    (decision log entries 426 and 428).

Which of the project's own modules it uses
    research.variant_lists   where a game's results and a method's lists are kept
    research.ov1_ledger      where the two series are kept
    research.windows_text    every line of the file ends CRLF

What uses it
    research/research_job.py (writes it), reporting/report_inputs.py (compares it), and the tests.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from research import ov1_ledger
from research import variant_lists as lists
from research.windows_text import windows_lines

# The file's name, in the game's research folder (beside its variants and ov1 folders).
IDENTITY_NAME = 'SCIENCE_IDENTITY.json'
# The form of the file, named in it, so that a later form is told apart.
IDENTITY_FORMAT = 'SCIENCE_IDENTITY_V1'
# The key that says why the second OV-1 series stopped early: a text, or null when it did not. A file without it
# is not an identity (the reviewer's C03: an explicit "no block" is told apart from a missing field).
BLOCKED_KEY = 'prevailing_blocked'


def identity_path(tree_root: Path, game_id: str) -> Path:
    """Where a game's identity is kept, for example <tree>/results/research/POWERBALL/SCIENCE_IDENTITY.json."""
    return Path(tree_root) / lists.RESEARCH_FOLDER / game_id / IDENTITY_NAME


def file_identity(path: Path):
    """[size in bytes, SHA-256] of a file, or None if there is no file; for example [20341, 'ab12...']."""
    if not path.is_file():
        return None
    data = path.read_bytes()
    return [len(data), hashlib.sha256(data).hexdigest()]


def identity_of(records, engine_fingerprint: str) -> dict:
    """What a game's stored science is made from, worked out from the records and the files on disk now.

    records: the game's GameRecords (its results on file, its methods' states, the methods with results but no
    software here).  engine_fingerprint: the infrastructure's fingerprint of the tree now.
    Returns the identity without the blocked reason, for example {'format': 'SCIENCE_IDENTITY_V1', 'game':
    'POWERBALL', 'engine_fingerprint': 'ab12...', 'results': {'last_draw': 1593, 'version': 7, 'sha256': '...'},
    'methods': [{'identity': 'E_002/RECUR_MEAN_ALL_V1', 'fingerprint': '...', 'first_target': 1147,
    'counted_from': 1592, 'retired_from': None, 'retired_reason': None, 'last_target': 1594, 'last_scored':
    1593, 'forecasts': [size, sha256], 'scores': [size, sha256]}, ...], 'not_installed': [...], 'series':
    {'prevailing': [size, sha256], 'exploratory': [size, sha256]}}.
    """
    tree_root, game_id = records.tree_root, records.game_id
    methods = []
    for state in sorted(records.states, key=lambda s: s.variant.identity):
        variant, status = state.variant, state.status
        forecasts, scores = lists.variant_list_paths(tree_root, game_id, variant.family, variant.variant)
        methods.append({'identity': variant.identity, 'fingerprint': variant.fingerprint,
                        'first_target': state.first_target, 'counted_from': status.eligible_from,
                        'retired_from': status.withdrawn_from, 'retired_reason': status.withdrawn_reason,
                        'last_target': max(state.targets) if state.targets else None,
                        'last_scored': max(state.score_contents) if state.score_contents else None,
                        'forecasts': file_identity(forecasts), 'scores': file_identity(scores)})
    results = records.results
    return {'format': IDENTITY_FORMAT, 'game': game_id, 'engine_fingerprint': engine_fingerprint,
            'results': {'last_draw': results.last_draw, 'version': results.version, 'sha256': results.sha256},
            'methods': methods, 'not_installed': sorted(records.foreign),
            'series': {'prevailing': file_identity(ov1_ledger.ledger_path(tree_root, game_id)),
                       'exploratory': file_identity(ov1_ledger.ledger_path(tree_root, game_id,
                                                                           ov1_ledger.EXPLORATORY_LEDGER))}}


def remove_identity(tree_root: Path, game_id: str) -> None:
    """Remove a game's identity, as the job does when it begins the game's work (nothing if there is none)."""
    path = identity_path(tree_root, game_id)
    if path.exists():
        path.unlink()


def write_identity(records, engine_fingerprint: str, blocked: str | None) -> Path:
    """Write a game's identity, when its scientific work has finished: identity_of() with the blocked reason.

    blocked: why the second OV-1 series stopped early, or None if it did not (written as null).
    The file is written beside itself under another name and then put in place. Returns its path.
    """
    document = identity_of(records, engine_fingerprint)
    document[BLOCKED_KEY] = blocked
    path = identity_path(records.tree_root, records.game_id)
    staged = path.with_name(path.name + '.writing')
    staged.write_bytes(windows_lines(json.dumps(document, indent=1, sort_keys=True) + '\n').encode('ascii'))
    os.replace(staged, path)
    return path


def read_identity(tree_root: Path, game_id: str) -> dict | None:
    """A game's identity as stored, or None if there is none or it cannot be read as one (no format, another
    game, or no blocked key)."""
    path = identity_path(tree_root, game_id)
    try:
        document = json.loads(path.read_bytes().decode('ascii'))
    except (OSError, ValueError):
        return None
    if (not isinstance(document, dict) or document.get('format') != IDENTITY_FORMAT
            or document.get('game') != game_id or BLOCKED_KEY not in document):
        return None
    return document


def differences(stored: dict, now: dict) -> list:
    """What differs between a stored identity and the one worked out now, in plain words, for example
    ['the accepted results file', 'E_002/RECUR_MEAN_ALL_V1: its scores list']; [] if they agree. The blocked
    reason is not compared (it is known only to the job)."""
    found = []
    for key, words in (('engine_fingerprint', 'the engine'), ('results', 'the accepted results file'),
                       ('not_installed', 'the methods with results but no software here')):
        if stored.get(key) != now.get(key):
            found.append(words)
    for which in ('prevailing', 'exploratory'):
        if (stored.get('series') or {}).get(which) != now['series'][which]:
            found.append(f'the {which} OV-1 series')
    theirs = {method.get('identity'): method for method in stored.get('methods') or []}
    ours = {method['identity']: method for method in now['methods']}
    for identity in sorted(set(theirs) ^ set(ours)):
        found.append(f'{identity}: ' + ('a method now installed' if identity in ours else 'no longer installed'))
    for identity in sorted(set(theirs) & set(ours)):
        unlike = [key for key in ours[identity] if theirs[identity].get(key) != ours[identity][key]]
        if unlike:
            found.append(f'{identity}: ' + ', '.join(unlike))
    return found
