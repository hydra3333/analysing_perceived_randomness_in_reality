"""MHUP-B: what the forecasting half may know about scores (code plan v0.3 CF-9; EX_223 CP-Q5).

The forecasting half must know which records are scored, to decide which target is closed (design 6.3), and it must
never see an outcome. This module is its only reader of the weekly score ledger. It returns scientific identities only:
(game, method, revision, variant, target, the scored record's digest, the scoring policy id). It returns no match
count, division, rank, drawn number, score or date, and imports nothing from the evaluator.

A target is closed only by routine score lines that carry the digests of the records its own freeze line names. A score
line that is malformed, repeats a scientific identity, or names a record no freeze line names refuses: it never closes
a target and is never read as "not scored".
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


def scored_identities(root: Path, game_id: str) -> frozenset:
    """Every scientific identity in the game's weekly score ledger. A repeated identity refuses (one routine score per
    identity; an amendment carries another policy id)."""
    rows, _torn = OR.read_jsonl(WR.score_ledger_path(root, game_id))
    seen = set()
    for line in rows:
        ident = identity_of(line)
        if ident[0] != game_id:
            raise OR.RecordRefused('score ledger: a line of another game')
        if ident in seen:
            raise OR.RecordRefused('score ledger: a scientific identity scored twice')
        seen.add(ident)
    return frozenset(seen)


def routine_identity(game_id: str, target: int, named: Mapping) -> tuple:
    return (game_id, named['method_id'], named['method_revision'], named['variant_id'], target,
            named['scored_record_digest'], WR.ROUTINE_POLICY)


def closed_targets(game_id: str, freeze_lines, identities) -> set[int]:
    """The targets whose every named record has its routine score line. Every routine identity must belong to a record
    some freeze line names, with that record's digest; a foreign identity refuses."""
    owed = {}
    for line in freeze_lines:
        for r in line['records']:
            owed[routine_identity(game_id, line['target_draw_number'], r)] = line['target_draw_number']
    for ident in identities:
        if ident[6] == WR.ROUTINE_POLICY and ident not in owed:
            raise OR.RecordRefused('score ledger: a routine score for a record no freeze line names')
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
