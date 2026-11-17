"""MHUP-B: what the forecasting half may know about scores (code plan v0.3 CF-9; EX_223 CP-Q5).

The forecasting half must know which records are scored, to decide which target is closed (design 6.3), and it must
never see an outcome. This module is its only reader of the weekly score ledger. It returns scientific identities only:
(game, method, revision, variant, target, the scored record's digest, the scoring policy id). It returns no match
count, division, rank, drawn number, score or date, and imports nothing from the evaluator.

A target is closed only by valid routine score lines of the records its own freeze line names (EX_229 F-229-2). Before
any identity is returned, every line of the ledger must be exactly its canonical bytes and a complete, well-formed score
line (weekly_records.validate_score_line), and must belong to one record of its target's freeze line, repeating that
record's facts (weekly_records.check_score_linkage). A line that is an identity-shaped fragment, not canonical, without
its provenance, a repeat of a scientific identity, or the score of a record no freeze line names refuses: it never
closes a target and is never read as "not scored". The validation happens inside this module; what comes out is
identities only.
"""
from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import _common.contract_vocab as V
from _common import owner_records as OR
from _common import weekly_records as WR

IDENTITY_FIELDS = ('game_id', 'method_id', 'method_revision', 'variant_id', 'target_draw_number',
                   'scored_record_digest', 'scoring_policy_id')


def identity_of(line: Mapping) -> tuple:
    """The scientific identity of one score line (design 6.6), checked for shape; nothing else of the line is read."""
    if type(line) is not dict or line.get('schema') != WR.SCORE_LINE_SCHEMA:
        raise OR.RecordRefused('score ledger: a line of an unknown schema')
    ident = tuple(line.get(f) for f in IDENTITY_FIELDS)
    game, method, revision, variant, target, digest, policy = ident
    if (type(game) is not str or type(method) is not str or not V.METHOD_ID.fullmatch(method) or
            type(revision) is not str or not V.REVISION.fullmatch(revision) or
            type(variant) is not str or not V.VARIANT_ID.fullmatch(variant) or type(target) is not int or
            type(digest) is not str or not V.SHA256.fullmatch(digest) or type(policy) is not str or not policy):
        raise OR.RecordRefused('score ledger: a line without a well-formed scientific identity')
    return ident


def scored_identities(root: Path, game_id: str, freeze_lines) -> frozenset:
    """Every scientific identity in the game's weekly score ledger, after the whole ledger has been validated: canonical
    lines of the full shape (weekly_records.score_ledger), each linked to a record of its target's freeze line, one
    line per identity (an amendment carries another policy id and names the earlier line of the same record it stands
    beside). `freeze_lines` are the verified lines of the forecast ledger. Only identities are returned."""
    from _common.contract_records import record_digest
    rows = WR.score_ledger(root, game_id)                    # canonical bytes, the full shape, this game
    by_target = {line['target_draw_number']: line for line in freeze_lines}
    seen, earlier = set(), {}
    for s in rows:
        ident = identity_of(s)
        if ident in seen:
            raise OR.RecordRefused('score ledger: a scientific identity scored twice')
        line = by_target.get(s['target_draw_number'])
        if line is None:
            raise OR.RecordRefused('score ledger: a score for a target that has no freeze line')
        WR.check_score_linkage(s, line)
        if s['amendment_of'] is not None and earlier.get(s['amendment_of']) != ident[:6]:
            raise OR.RecordRefused('score ledger: an amendment that names no earlier score line of the same record')
        earlier[record_digest(s)] = ident[:6]
        seen.add(ident)
    return frozenset(seen)


def routine_identity(game_id: str, target: int, named: Mapping) -> tuple:
    return (game_id, named['method_id'], named['method_revision'], named['variant_id'], target,
            named['scored_record_digest'], WR.ROUTINE_POLICY)


def closed_targets(game_id: str, freeze_lines, identities) -> set[int]:
    """The targets whose every named record has its routine score line. `identities` come from scored_identities, which
    has already validated each line and tied it to its freeze line."""
    out = set()
    for line in freeze_lines:
        t = line['target_draw_number']
        if all(routine_identity(game_id, t, r) in identities for r in line['records']):
            out.add(t)
    return out


def unscored_records(game_id: str, line: Mapping, identities) -> list[dict]:
    """The records of one freeze line that have no routine score line yet, in the line's order."""
    t = line['target_draw_number']
    return [r for r in line['records'] if routine_identity(game_id, t, r) not in identities]
