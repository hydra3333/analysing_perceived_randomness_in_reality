"""MHUP-B slice 3: counted edits on top of slice 2's tree (code plan v0.3 section 5, L4, L7 and L8).

 release_records  `released_history`: every entry any release record ever named (the league table shows retired
                  revisions "as published", supplement 3.1).
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
