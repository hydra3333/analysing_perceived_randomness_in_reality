"""MHUP-B slice 3: counted edits on top of slice 2's tree (code plan v0.3 section 5, L4, L7 and L8).

 release_records  `released_history`: every entry any release record ever named (the league table shows retired
                  revisions "as published", supplement 3.1).
 registry         MEASURE_REGISTRY_V1.json: the CATCH_UP evidence tier, and OV-1 with its two labelled uses (code plan L5/L7
                  as changed by the owner's clarification of 18 November 2026). The file's `source` field still names
                  R3 as installed; R3's amendment travels with the integrated package.
 walk_forward     a routine fill is not planned while a development report of this game is not yet a canonical source
                  (code plan L4: the two existing attempts are admitted first; otherwise one mistaken command would
                  plan and run their whole windows a second time). `NothingToFill` (a BatchRefused): a routine fill with nothing missing is told apart from a refusal, so the
                  development sequencer can go on to publish. Method_Walk_Forward.py prints one machine-readable last
                  line for a plan of the second kind, as the other tools do (design 6.1).
 Method_OV1       `record` for a game that is not registered says NOT_REGISTERED and exits 0: nothing is due, and the
                  weekly sequencer reads that state (EX_237 section 5: the state line, not only the exit code).
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

# ---------------------------------------------------------------- L8: what the sequencers read from their children
edit(C + 'walk_forward.py', [
    ("            raise BatchRefused('nothing to fill: every eligible pair of every released variant is covered')\n",
     "            raise NothingToFill('nothing to fill: every eligible pair of every released variant is covered')\n"),
    ("        pairs = _fill_pairs(game_id, members, last_draw)\n        if not pairs:\n",
     "        waiting = _unadmitted_reports(game_id)\n"
     "        if waiting:\n"
     "            b, s, l = waiting[0]\n"
     "            raise BatchRefused(f'a report of batch {b} over draws {s}-{l} is not yet a canonical source of the league '\n"
     "                               f'table, so a fill would plan its pairs a second time. Admit it first: '\n"
     "                               f'Run_Development_Batch.bat --game {game_id} --report --batch {b} --first {s} --last {l}')\n"
     "        pairs = _fill_pairs(game_id, members, last_draw)\n        if not pairs:\n"),
    ("\n\ndef make_dev_plan(game_id: str, plan_kind: str, adapters: Mapping, *, variants=None, first=None, last=None) -> dict:\n",
     "\n\ndef _unadmitted_reports(game_id: str) -> list:\n"
     "    \"\"\"(batch, first, last) of every development report in the search log whose batch and window no canonical source\n"
     "    of the league table has yet, oldest first (MHUP-B, code plan L4: the existing report attempts are admitted before\n"
     "    any routine fill, or the fill would run their pairs again). Value-free: the search log, the plans and the source\n"
     "    list only. An exploratory rerun's report is never a source and never counts.\"\"\"\n"
     "    from _common import score_identities as SI\n"
     "    path = roots()['search_log']\n"
     "    if not path.is_file() or path.is_symlink():\n"
     "        return []\n"
     "    try:\n"
     "        listed = {(s['batch_id'], s['window_first'], s['window_last']) for s in SI.league_sources(roots()['project'], game_id)}\n"
     "    except OR.RecordRefused as exc:\n"
     "        raise BatchRefused(f'the league\\'s source list does not read: {exc}') from None\n"
     "    out = []\n"
     "    for r in csv.DictReader(io.StringIO(path.read_bytes().decode('ascii'))):\n"
     "        if r.get('row_type') != 'RANKING_REPORT' or r.get('game_id') != game_id:\n"
     "            continue\n"
     "        key = (r.get('batch_id'), int(r['window_first']), int(r['window_last']))\n"
     "        if key in listed or key in out:\n"
     "            continue\n"
     "        try:\n"
     "            plan = load_plan(game_id, key[0])\n"
     "        except BatchRefused:\n"
     "            plan = {}                                    # a report whose batch no longer loads still has to be looked at\n"
     "        if plan.get('plan_kind') != 'EXPLORATORY_RERUN':\n"
     "            out.append(key)\n"
     "    return out\n"
     "\n\ndef make_dev_plan(game_id: str, plan_kind: str, adapters: Mapping, *, variants=None, first=None, last=None) -> dict:\n"),
    ("\n\ndef roots(kind: str = 'WF_BATCH') -> dict:\n",
     "\n\nclass NothingToFill(BatchRefused):\n"
     "    \"\"\"A routine fill found no pair without a canonical score: no plan is made. Not an error (MHUP-B, L8).\"\"\"\n"
     "\n\ndef roots(kind: str = 'WF_BATCH') -> dict:\n"),
])
edit('src/methods/Method_Walk_Forward.py', [
    ("                print(f\"[WALK-FORWARD] next: Run_Experiment.bat Method_Walk_Forward.py run --game {args.game} \"\n"
     "                      f\"--batch {made['batch_id']}\", flush=True)\n"
     "                return 0\n"
     "            if args.variants is not None:\n",
     "                print(f\"[WALK-FORWARD] next: Run_Experiment.bat Method_Walk_Forward.py run --game {args.game} \"\n"
     "                      f\"--batch {made['batch_id']}\", flush=True)\n"
     "                print(f\"[WALK-FORWARD] RESULT state=PLANNED game={args.game} batch={made['batch_id']} \"\n"
     "                      f\"kind={made['plan_kind']} first={made['window_first']} last={made['window_last']}\", flush=True)\n"
     "                return 0\n"
     "            if args.variants is not None:\n"),
    ("    except (WF.BatchRefused, ValueError) as exc:\n",
     "    except WF.NothingToFill as exc:\n"
     "        print(f'[WALK-FORWARD] {exc}. No plan was made and nothing was run.', flush=True)\n"
     "        print(f'[WALK-FORWARD] RESULT state=NOTHING_TO_FILL game={args.game} batch=-', flush=True)\n"
     "        return 0\n"
     "    except (WF.BatchRefused, ValueError) as exc:\n"),
])
edit(E + 'Method_OV1.py', [
    ("        elif args.command == 'record':\n"
     "            out = OV.record(args.game, echo=echo)\n",
     "        elif args.command == 'record':\n"
     "            if OV.OR.absent(OV.registration_path(OV._root(), args.game)):\n"
     "                echo(f'[OV1] {args.game} is not registered: nothing is due (the owner registers OV-1 once, before '\n"
     "                     f'its first eligible draw)')\n"
     "                _result('NOT_REGISTERED', args.game, None)\n"
     "                return 0\n"
     "            out = OV.record(args.game, echo=echo)\n"),
])
