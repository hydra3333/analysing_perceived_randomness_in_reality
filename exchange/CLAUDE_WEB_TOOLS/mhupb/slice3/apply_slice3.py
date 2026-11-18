"""MHUP-B slice 3: counted edits on top of slice 2's tree (code plan v0.3 section 5, L4, L7 and L8).

 release_records  `released_history`: every entry any release record ever named (the league table shows retired
                  revisions "as published", supplement 3.1).
 registry         MEASURE_REGISTRY_V1.json: the CATCH_UP evidence tier, and OV-1 with its two labelled uses (code plan L5/L7
                  as changed by the owner's clarification of 18 November 2026). The file's `source` field still names
                  R3 as installed; R3's amendment travels with the integrated package.
 ov1              `publication_names` is connected to the league's publication manifests (supplement 6.8; EX_225
                  RC-225-1; EX_237 section 5): the reconcile step checks the forecast-ledger extent each one pinned.
Every old string must occur exactly once; the script stops otherwise. Usage: python3 -I apply_slice3.py TREE
"""
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()


def edit(rel, pairs):
    p = tree / rel
    raw = p.read_bytes()
    crlf = b'\r\n' in raw
    s = raw.decode('ascii').replace('\r\n', '\n')
    for a, b in pairs:
        assert s.count(a) == 1, (rel, s.count(a), a[:80])
        s = s.replace(a, b)
    s.encode('ascii')
    p.write_bytes(s.replace('\n', '\r\n').encode('ascii') if crlf else s.encode('ascii'))
    print('edited', rel, len(pairs))


C = 'src/methods/_common/'
E = 'src/evaluation/'

# ---------------------------------------------------------------- L4: the roster of every revision ever released
edit(C + 'release_records.py', [
    ("def released_variants(root: Path) -> dict:\n",
     "def released_history(root: Path) -> dict:\n"
     "    \"\"\"(game, method, revision, variant) -> local release date, for EVERY entry any release record names, retired or\n"
     "    superseded ones included (MHUP-B, supplement v0.8 section 3.1: the league table shows them \"as published\").\"\"\"\n"
     "    out: dict = {}\n"
     "    for r in validate_records(root)['releases']:\n"
     "        for e in r['entries']:\n"
     "            out.setdefault(_entry(e, r['_file']), r['local_date'])\n"
     "    return out\n"
     "\n"
     "\n"
     "def released_variants(root: Path) -> dict:\n"),
])

# ---------------------------------------------------------------- L5 seam: OV-1's reconcile reads the league manifests
edit(E + 'ov1.py', [
    ("    The league table is layer L4 (slice 3): until its manifests exist there is nothing to name, and its reader is\n"
     "    connected here in that slice.\"\"\"\n"
     "    return []\n",
     "    The reader is the league's own (layer L4); a manifest that does not validate blocks, for an absence of evidence\n"
     "    is never taken as evidence of absence.\"\"\"\n"
     "    from . import league_sources as LS\n"
     "    try:\n"
     "        return LS.publication_names(root, game_id)\n"
     "    except LS.LeagueRefused as exc:\n"
     "        raise OV1Blocked(f'the league table\\'s publication records do not verify: {exc}') from None\n"),
])

# ---------------------------------------------------------------- L7: the measure registry (the labels' one home)
edit(E + 'registry/MEASURE_REGISTRY_V1.json', [
    ('  {\n   "tier": "PROSPECTIVE",\n   "meaning": "forecasts frozen and published before their draws"\n  },\n',
     '  {\n   "tier": "PROSPECTIVE",\n   "meaning": "forecasts frozen and published before their draws"\n  },\n'
     '  {\n   "tier": "CATCH_UP",\n   "meaning": "forecasts made by the weekly session for a draw whose result was already '
     'accepted: computed from earlier draws only, but not frozen before the draw"\n  },\n'),
    ('   "distinguished_by": "Only HOLDOUT_MODE_H and PROSPECTIVE tiers can show it."\n  }\n ]\n}\n',
     '   "distinguished_by": "Only HOLDOUT_MODE_H and PROSPECTIVE tiers can show it."\n  }\n ],\n'
     ' "overall_measures": [\n  {\n   "id": "OV-1",\n   "heading": "OV-1 - The one overall measure (one per game; games never combined)",\n'
     '   "one_liner": "an evidence score that grows only if the variants\' most favoured numbers keep being drawn more often '
     'than their least favoured ones.",\n   "uses": [\n    {\n     "label": "OV-1 FORMAL PROSPECTIVE (REGISTERED)",\n'
     '     "meaning": "the registered test: one stream per game, every forecast frozen before its draw, bar 40 (if the draws '
     'are fair, at most a 2.5% chance per game of ever reaching it, under the registered operating assumptions)"\n    },\n'
     '    {\n     "label": "OV-1 RETROSPECTIVE WALK-FORWARD - DESCRIPTIVE, NOT FORMAL PROSPECTIVE",\n'
     '     "meaning": "the same arithmetic over forecasts already scored: descriptive, no P value, 40 a reference line only, '
     'never written to the formal ledger"\n    }\n   ]\n  }\n ]\n}\n'),
])
