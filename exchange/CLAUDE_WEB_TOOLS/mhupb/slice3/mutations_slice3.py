"""MHUP-B slice 3: mutation checks (design Appendix L: one planted defect per rule, each caught by a named test).

For each mutant: one counted edit to one file of a built dev TREE, the named test is run in its own process and must
FAIL; the file is then restored byte for byte. A mutant that survives is reported and the tool exits 1.
Usage: python3 -I mutations_slice3.py TREE [name-substring ...]

Not listed, because they are equivalent (each is one of two guards on the same fact, tried 18 November 2026):
  * the kind check in league_publish.admit when a batch is named: league_sources.attempt_entry refuses the same
    exploratory attempt with the same words; the attempt_entry one is listed;
  * the "a row already names this publication" test in league_publish._log (EX_225 RC-225-2): a logged manifest is
    never handed to it again, because `manifests` already marks it logged; kept as a second guard;
  * the forecast-ledger extent test of a pinned rebuild in league_sources._weekly: the lines are cut to the pinned
    count on the next line, and the score lines' own linkage refuses a ledger that lost a line;
  * "an archive member holds other bytes" in league_publish._finish when the rebuilt bytes already differ: the first
    comparison marks the same publication; each is listed with the case only it catches;
  * the digest test of a selected forecast in ov1_retrospective.tickets: the fixtures hold one forecast per pair, and
    the X cross-check refuses a ticket that is not the scored one.
"""
import os
import subprocess
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
only = sys.argv[2:]
C = 'src/methods/_common/'
E = 'src/evaluation/'
LG, WR_, SQ = 'tests.test_mhupb_league', 'tests.test_mhupb_weekly_report', 'tests.test_mhupb_sequencers'
FIG = LG + '.Figures.test_every_figure_equals_the_oracle_and_forward_is_kept_apart'
PURE = LG + '.Figures.test_the_formatter_is_pure'
ROWS = LG + '.Figures.test_no_scores_one_draw_and_retired_rows'
ONE = LG + '.Sources.test_one_score_per_key_across_sources'
GONE = LG + '.Sources.test_a_missing_or_altered_source_is_not_available_never_a_partial_total'
MH = LG + '.Sources.test_mode_h_as_sealed_is_shown_and_never_summed'
REV = LG + '.Sources.test_a_lost_source_blanks_only_the_revision_it_supplies'
LATE = LG + '.Sources.test_late_pre_draw_is_counted_once_and_never_forward_and_a_witness_must_be_verified_in_time'
CHAIN = LG + '.Sources.test_a_branching_correction_chain_refuses'
SAME = LG + '.Publication.test_unchanged_inputs_publish_nothing_and_a_change_takes_the_next_version'
FAULT = LG + '.Publication.test_a_fault_after_every_durable_step_then_a_rerun'
MARK = LG + '.Publication.test_an_interrupted_publication_whose_table_cannot_be_rebuilt_is_marked_never_logged'
GROWN = LG + '.Publication.test_a_grown_ledger_does_not_stop_an_interrupted_publication'
CUR = LG + '.Publication.test_the_current_copies_are_restored_from_the_archive'
TORN = LG + '.Publication.test_a_torn_or_doubled_search_log_row_refuses'
ORPH = LG + '.Publication.test_the_orphan_marker_blocks_every_writing_command'
HIST = LG + '.Publication.test_history_recomputes_nothing_and_every_reconstruction_row_is_labelled'
COMPLETE = LG + '.Admission.test_only_a_complete_correctly_labelled_attempt_is_admitted'
REPEAT = LG + '.Admission.test_a_repeat_changes_no_byte_and_a_changed_identity_refuses'
ATOMIC = LG + '.Admission.test_the_replace_is_atomic_and_an_interrupted_job_resumes'
EXPL = LG + '.Admission.test_a_routine_fill_is_admitted_and_an_exploratory_rerun_never'
SEAM = LG + '.Seams.test_ov1_reconcile_reads_the_publication_manifests'
ORACLE = WR_ + '.Retrospective.test_the_series_equals_an_oracle_made_from_the_files_on_disk'
FORMAL = WR_ + '.Retrospective.test_over_the_formal_streams_draws_the_arithmetic_is_the_formal_ledgers'
COHORT = WR_ + '.Retrospective.test_cohorts_missing_pairs_and_contradictions'
REF = WR_ + '.Retrospective.test_reaching_the_reference_line_is_reported_as_an_observation'
VIEWS = WR_ + '.Views.test_both_views_under_their_labels_and_the_formal_records_untouched'
STATES = WR_ + '.Views.test_a_formal_stream_that_is_not_registered_stopped_or_unreadable_is_said_so'
POOL = WR_ + '.Parts.test_nothing_is_pooled_and_every_part_names_its_source'
APART = WR_ + '.Parts.test_forward_and_catch_up_are_kept_apart_and_equal_to_counts_made_here'
INDEX = WR_ + '.Parts.test_the_matched_view_the_retired_index_and_the_written_files'
FAILS = WR_ + '.Parts.test_a_failing_report_changes_nothing_else_and_refusals_write_nothing'
ORDER = SQ + '.Weekly.test_the_order_of_a_session_after_two_missed_draws'
LIVE = SQ + '.Weekly.test_a_stop_of_the_live_path_leaves_the_lock_and_starts_no_reporting'
FMT = SQ + '.Isolation.test_the_formatter_failing_gives_the_distinct_status_and_a_later_publish_writes_the_table'
BLOCK = SQ + '.Isolation.test_ov1_blocked_or_silent_gives_its_own_status_and_both_give_the_third'
STATE = SQ + '.Isolation.test_ov1s_state_line_is_read_not_only_its_exit_code'
FILL = SQ + '.Batches.test_fill_runs_reports_admits_and_publishes_and_a_second_fill_finds_nothing'
RERUN = SQ + '.Batches.test_a_rerun_is_reported_and_never_admitted'
KIDS = SQ + '.Children.test_commands_plain_arguments_and_the_result_line'
STATIC = SQ + '.Statics.test_the_sequencers_import_no_method_or_evaluator_code_and_act_on_no_process'
LAYERS = SQ + '.Statics.test_every_source_file_is_classified_and_the_live_path_imports_no_reporting_module'

MUTANTS = [
    # ---- L4, the sources (Sup 4)
    ('sources: the one-score rule dropped', E + 'league_sources.py', "        if key in seen:\n", "        if False:\n", ONE),
    ('sources: a listed ledger read without its digest', E + 'league_sources.py',
     "    if sha256_hex(raw) != entry['score_ledger_sha256']:\n", "    if False:\n", GONE),
    ('sources: the scoring plan not tied to the list entry', E + 'league_sources.py',
     "        raise LeagueRefused('its scoring plan is not the attempt, batch, window and plan the source list names')\n",
     "        pass\n", GONE),
    ('sources: a missing source read as no scores', E + 'league_sources.py',
     "            not_available.append({'source': e['attempt_id'], 'reason': str(exc), 'variants': _affected(game_id, e)})\n",
     "            pass\n", GONE),
    ('sources: Mode H as sealed added to the totals', E + 'league_sources.py',
     "    rows, not_available = list(weekly['rows']), []\n",
     "    rows, not_available = list(weekly['rows']) + _mode_h(root, game_id)['rows'], []\n", MH),
    ('sources: the sealed ledger read without its recorded digest', E + 'league_sources.py',
     "        if sha256_hex(raw) != ident['score_ledger_sha256']:\n", "        if False:\n", MH),
    ('sources: a branching correction chain accepted', E + 'league_sources.py',
     "            if s['amendment_of'] in amended:                   # the routine line, and a branching chain refuses\n",
     "            if False:\n", CHAIN),
    ('sources: a correction summed beside its routine score', E + 'league_sources.py',
     "        if s['scoring_policy_id'] != WR.ROUTINE_POLICY:        # a correction stands beside its line; the table uses\n",
     "        if False:\n", CHAIN),
    ('sources: LATE_PRE_DRAW counted as forward', E + 'league_sources.py',
     "'LATE_PRE_DRAW': 'LATE_PRE_DRAW', 'CATCH_UP': 'CATCH_UP',", "'LATE_PRE_DRAW': 'FORWARD', 'CATCH_UP': 'CATCH_UP',", LATE),
    ('sources: an unverified witness counted', E + 'league_sources.py',
     "        if (line is not None and w['kind'] == 'WITNESS_VERIFIED' and w['freeze_line_digest'] == record_digest(line) and\n",
     "        if (line is not None and w['freeze_line_digest'] == record_digest(line) and\n", LATE),
    ('sources: a witness received after the draw counted', E + 'league_sources.py',
     "                WR.parse_utc(w['received_utc'], 'witness received_utc') < WR.parse_utc(line['deadline_utc'])):\n",
     "                True):\n", LATE),
    ('sources: a witness of another freeze line counted', E + 'league_sources.py',
     "        if (line is not None and w['kind'] == 'WITNESS_VERIFIED' and w['freeze_line_digest'] == record_digest(line) and\n",
     "        if (line is not None and w['kind'] == 'WITNESS_VERIFIED' and\n", LATE),
    ('sources: a rebuild reads past the pinned score lines', E + 'league_sources.py',
     "        scores = _prefix(scores, pins['weekly_score_ledger'], 'the weekly score ledger')\n", "        pass\n", GROWN),
    ('sources: two rows for one publication accepted', E + 'league_sources.py', "    if twice:\n", "    if False:\n", TORN),
    ('sources: a row without its manifest accepted', E + 'league_sources.py', "    if missing:\n", "    if False:\n", TORN),
    ('sources: an unfinished search-log row read past', E + 'league_sources.py',
     "    if not raw.endswith(b'\\n'):\n        raise LeagueRefused('the search log does not end at a line end",
     "    if False:\n        raise LeagueRefused('the search log does not end at a line end", TORN),
    ('sources: an incomplete publication offered to OV-1 as evidence', E + 'league_sources.py',
     "            for p in manifests(root, game_id) if not p['incomplete']]\n", "            for p in manifests(root, game_id)]\n", MARK),
    # ---- L4, admission (Sup 4 rule 2A)
    ('admit: an exploratory rerun admitted', E + 'league_sources.py',
     "    if batch_kind not in SI.LEAGUE_SOURCE_KINDS:\n        raise LeagueRefused(f'{attempt_id}: an exploratory",
     "    if False:\n        raise LeagueRefused(f'{attempt_id}: an exploratory", EXPL),
    ('admit: a report without its files admitted', E + 'league_sources.py',
     "    if len(found) != 1:\n        raise LeagueRefused(f'{attempt_id}: its report did not complete",
     "    if not found:\n        found = [reports_dir(root, game_id) / 'none.json']\n    if False:\n        raise LeagueRefused(f'{attempt_id}: its report did not complete", COMPLETE),
    ('admit: changed report files admitted', E + 'league_sources.py',
     "            any(OR.absent(p) or sha256_hex(p.read_bytes()) != man.get(f'{ext}_sha256' if ext == 'csv' else 'text_sha256')\n"
     "                for ext, p in members.items())):\n", "            False):\n", COMPLETE),
    ('admit: a scoring plan that is not the logged one admitted', E + 'league_sources.py',
     "    if (record_digest(body) != row.get('plan_digest') or sp.get('attempt_id') != attempt_id or\n",
     "    if (sp.get('attempt_id') != attempt_id or\n", COMPLETE),
    ('admit: an incomplete score ledger admitted', E + 'league_sources.py',
     "    if got != set(want) or {k[:3] for k in want} != set(selected):\n", "    if False:\n", COMPLETE),
    ('admit: a score that is not its ticket\'s matches admitted', E + 'league_sources.py',
     "        if rec['main_matches'] != len(set(ticket[0]) & set(rec['drawn_main'])) or \\\n", "        if False or \\\n", COMPLETE),
    ('admit: a key scored twice inside one ledger admitted', E + 'league_sources.py',
     "        if ticket is None or key in got or selected[key[:3]][0] != rec['forecast_content_digest']:\n",
     "        if ticket is None or selected[key[:3]][0] != rec['forecast_content_digest']:\n", COMPLETE),
    ('admit: a score under another revision of the method admitted (F3-01)', E + 'league_sources.py',
     "        if (rec['method_revision'], rec['freeze_receipt_digest']) != frozen[key[:3]]:\n",
     "        if rec['freeze_receipt_digest'] != frozen[key[:3]][1]:\n", COMPLETE),
    ('admit: a score with another freeze receipt admitted (F3-01)', E + 'league_sources.py',
     "        if (rec['method_revision'], rec['freeze_receipt_digest']) != frozen[key[:3]]:\n",
     "        if rec['method_revision'] != frozen[key[:3]][0]:\n", COMPLETE),
    ('admit: a prize division its matches do not give admitted (F3-01)', E + 'league_sources.py',
     "        if rec['division'] != DV.division(game_id, rec['main_matches'], rec.get('powerball_match'),\n",
     "        if False and rec['division'] != DV.division(game_id, rec['main_matches'], rec.get('powerball_match'),\n", COMPLETE),
    ('sources: a lost source blanks another revision (F3-02)', E + 'league_table.py',
     "        if n['variants'] is None or [method, revision, variant] in [list(v) for v in n['variants']]:\n",
     "        if n['variants'] is None or [method, variant] in [[v[0], v[2]] for v in n['variants']]:\n", REV),
    ('sources: a lost source whose plan cannot be read blanks nothing (F3-02)', E + 'league_sources.py',
     "    except WF.BatchRefused:\n        return None\n    return sorted({(m['method_id'], m['method_revision'], m['variant_id'])",
     "    except WF.BatchRefused:\n        return []\n    return sorted({(m['method_id'], m['method_revision'], m['variant_id'])", REV),
    ('sources: a changed manifest accepted under its logged name (F3-03)', E + 'league_sources.py',
     "            if name in logged and logged[name][0] != record_digest(m):          # EX_240 F3-03\n", "            if False:\n", SEAM),
    ('admit: a repeat rewrites or refuses', E + 'league_publish.py', "            if s == entry:\n", "            if False:\n", REPEAT),
    ('admit: the same attempt with another identity accepted', E + 'league_publish.py', "            if s == entry:\n", "            if True:\n", REPEAT),
    ('admit: an overlapping key admitted', E + 'league_publish.py', "    if clash:\n", "    if False:\n", ONE),
    ('admit: admitted while a listed source is unreadable', E + 'league_sources.py',
     "    if data['not_available']:\n        n = data['not_available'][0]\n        raise LeagueRefused(f'a listed source is not available",
     "    if False:\n        n = data['not_available'][0]\n        raise LeagueRefused(f'a listed source is not available", GONE),
    # ---- L4, the publication (Sup 5.1; plan sections 7 and 9)
    ('publish: unchanged inputs published again', E + 'league_publish.py',
     "    if logged and logged[-1]['manifest']['inputs'] == pins:\n", "    if False:\n", SAME),
    ('publish: the row before the members', E + 'league_publish.py',
     "    for ext in ('txt', 'csv'):\n        _create(folder / f'{name}.{ext}', built[ext])                       # step 3\n"
     "    _log(root, game_id, name, manifest)                                     # step 4: the row, last\n",
     "    _log(root, game_id, name, manifest)                                     # step 4: the row, last\n"
     "    for ext in ('txt', 'csv'):\n        _create(folder / f'{name}.{ext}', built[ext])                       # step 3\n", FAULT),
    ('publish: a version number reused', E + 'league_publish.py',
     "    version = (pubs[-1]['manifest']['version'] if pubs else 0) + 1          # from the manifests: never reused\n",
     "    version = (logged[-1]['manifest']['version'] if logged else 0) + 1\n", MARK),
    ('publish: an unfinished one finished without comparing its bytes', E + 'league_publish.py',
     "        if any(sha256_hex(built[ext]) != m[f'{ext}_sha256'] for ext in ('txt', 'csv')):\n", "        if False:\n", MARK),
    ('publish: an archive member with other bytes logged', E + 'league_publish.py',
     "                if not OR.absent(path) and path.read_bytes() != built[ext]:\n", "                if False:\n", LG + '.Publication.test_an_unfinished_publication_with_a_damaged_member_is_marked'),
    ('publish: the current copies not refreshed', E + 'league_publish.py',
     "    _refresh_current(root, game_id, manifest)                               # step 5\n", "    pass\n", SAME),
    ('publish: the notice left in place', E + 'league_publish.py', "    _remove(folder / NOTICE)\n", "    pass\n", SAME),
    ('publish: no notice while the copies are replaced', E + 'league_publish.py',
     "    if OR.absent(folder / NOTICE):\n", "    if False:\n", FAULT),
    ('publish: the archive member not verified before it is copied', E + 'league_publish.py',
     "        if OR.absent(path) or sha256_hex(path.read_bytes()) != m[f'{ext}_sha256']:\n", "        if OR.absent(path):\n", CUR),
    ('publish: the orphan marker ignored', E + 'league_publish.py', "    if m.exists() or m.is_symlink():\n", "    if False:\n", ORPH),
    ('views: the history rebuilds a table', E + 'league_publish.py',
     "        txt = _archived(root, game_id, p['manifest'])[f'{p[\"name\"]}.txt']\n",
     "        txt = LT.build(LS.collect(root, game_id)[0], _identity(p['manifest']))['txt']\n", HIST),
    ('views: a reconstruction row without its label', E + 'league_table.py',
     "            w.writerow([label, game, t, *k, r['kind'],", "            w.writerow(['', game, t, *k, r['kind'],", HIST),
    ('views: "released at that date" always yes', E + 'league_table.py',
     "                        'yes' if current[k] != '-' and current[k] <= day else 'no'])\n", "                        'yes'])\n", HIST),
    # ---- L4, the table (Sup 3)
    ('table: ordered by hits, not by hits per draw', E + 'league_table.py',
     "        rate = Fraction(e['all_hits'], e['all_draws']) if ranked else Fraction(0)\n",
     "        rate = Fraction(e['all_hits']) if ranked else Fraction(0)\n", PURE),
    ('table: a variant with one draw ranked', E + 'league_table.py',
     "        if e['not_available'] is None and e['all_draws'] >= 2:\n            rank += 1\n",
     "        if e['not_available'] is None and e['all_draws'] >= 1:\n            rank += 1\n", PURE),
    ('table: LOW_N below 3', E + 'league_table.py', "LOW_N = 30\n", "LOW_N = 3\n", FIG),
    ('table: chance of one number, not of seven', E + 'league_table.py',
     "    return Fraction(49, WR.MAIN_POOL[game_id])\n", "    return Fraction(7, WR.MAIN_POOL[game_id])\n", FIG),
    ('table: every kind in the forward column', E + 'league_table.py',
     "        fwd = [r for r in top if r['kind'] == 'FORWARD']\n", "        fwd = top\n", FIG),
    ('table: the first ten, not the last ten', E + 'league_table.py',
     "             'last10_hits': sum(r['main'] for r in top[-10:]),\n", "             'last10_hits': sum(r['main'] for r in top[:10]),\n", PURE),
    ('table: a partial total shown for a missing source', E + 'league_table.py',
     "             'status': people[key][1], 'not_available': _blocked_by(data, *key),\n",
     "             'status': people[key][1], 'not_available': None,\n", GONE),
    ('table: rounding by cutting', E + 'league_table.py',
     "    scaled = round(Fraction(x) * 10 ** places)\n", "    scaled = int(Fraction(x) * 10 ** places)\n", PURE),
    ('table: exposure flags not counted', E + 'league_table.py',
     "             'exposure_flagged_draws': sum(1 for t in targets if OR.exposure_flag(game, t) is not None)}\n",
     "             'exposure_flagged_draws': 0}\n", FIG),
    ('table: a retired revision unmarked', E + 'league_table.py',
     "        if e['status'] == 'RETIRED':\n            labels.append('RETIRED_AS_PUBLISHED')\n", "        if False:\n            labels.append('RETIRED_AS_PUBLISHED')\n", ROWS),
    ('table: the WORST ticket in the main figures', E + 'league_table.py',
     "        top = sorted((r for r in by[key] if r['readout'] == 'TOP'), key=lambda r: r['target'])\n",
     "        top = sorted((r for r in by[key]), key=lambda r: r['target'])\n", FIG),
    ('table: missing draws not counted', E + 'league_table.py',
     "             'missing_targets': (targets[-1] - targets[0] + 1 - len(set(targets))) if targets else 0,\n",
     "             'missing_targets': 0,\n", PURE),
    # ---- L5 seam (Sup 6.8; EX_237 section 5)
    ('ov1: the publication manifests not read', E + 'ov1.py',
     "        return LS.publication_names(root, game_id)\n", "        return []\n", SEAM),
    ('ov1: an unreadable manifest taken as no evidence', E + 'ov1.py',
     "        raise OV1Blocked(f'the league table\\'s publication records do not verify: {exc}') from None\n",
     "        return []\n", SEAM),
    # ---- L7, the retrospective view (EX_235 section 2 B)
    ('retro: the WORST ticket added, not subtracted', E + 'ov1_retrospective.py',
     "            for labels, sign in zip(have[k], (1, -1)):\n", "            for labels, sign in zip(have[k], (1, 1)):\n", ORACLE),
    ('retro: X not checked against the scored matches', E + 'ov1_retrospective.py', "        if x != x_matches:\n", "        if False:\n", COHORT),
    ('retro: the sums start again at every draw', E + 'ov1_retrospective.py',
     "                sums = [a + row[x] for a, row in zip(sums, table['rows'])]\n",
     "                sums = [row[x] for row in table['rows']]\n", ORACLE),
    ('retro: the window ignored', E + 'ov1_retrospective.py',
     "    inside = lambda t: (first is None or t >= first) and (last is None or t <= last)\n", "    inside = lambda t: True\n", ORACLE),
    ('retro: every scored variant used whatever the cohort', E + 'ov1_retrospective.py',
     "        if k[:3] in set(members) and inside(k[3]):\n", "        if inside(k[3]):\n", COHORT),
    ('retro: a named identity nobody released or scored accepted', E + 'ov1_retrospective.py',
     "        if not members or any(len(m) != 3 or m not in known for m in members):\n", "        if not members:\n", COHORT),
    ('retro: disagreeing drawn numbers accepted', E + 'ov1_retrospective.py',
     "                elif drawn != list(row['drawn_main']):\n", "                elif False:\n", COHORT),
    ('retro: a scored pair without tickets skipped silently', E + 'ov1_retrospective.py',
     "            if k not in have:\n                raise RetroRefused(f'the scored pair {k} has no frozen forecast giving both tickets')\n",
     "            if k not in have:\n                continue\n", COHORT),
    ('retro: a member without a pair not counted as missing', E + 'ov1_retrospective.py',
     "'cohort_without_pair': len(members) - len(here),", "'cohort_without_pair': 0,", COHORT),
    ('retro: the last draw at the reference line reported as the first', E + 'ov1_retrospective.py',
     "        if at and first_at is None:\n", "        if at:\n", REF),
    ('retro: the highest score not kept', E + 'ov1_retrospective.py', "        peak = max(peak, value)\n", "        peak = value\n", ORACLE),
    ('retro: the label loses "descriptive, not formal"', E + 'ov1_retrospective.py',
     "LABEL = 'OV-1 RETROSPECTIVE WALK-FORWARD - DESCRIPTIVE, NOT FORMAL PROSPECTIVE'\n", "LABEL = 'OV-1 RETROSPECTIVE WALK-FORWARD'\n", VIEWS),
    ('retro: the weekly forecasts left out', E + 'ov1_retrospective.py',
     "        if pair[0] is not None and pair[1] is not None:\n            out[key] = (pair[0][0], pair[1][0])\n",
     "        if False:\n            out[key] = (pair[0][0], pair[1][0])\n", FORMAL),
    # ---- L7, the consolidated report (Sup 8; plan L7)
    ('report: forward and catch-up merged', E + 'consolidated_report.py',
     "            if s['effective_class'] != cls:\n                continue\n", "            if False:\n                continue\n", APART),
    ('report: a secondary row without its label', E + 'consolidated_report.py',
     "            add(f'SECONDARY_{name}', SECONDARY_LABEL, x['unit'],", "            add(f'SECONDARY_{name}', '', x['unit'],", POOL),
    ('report: the retrospective rows under the formal label', E + 'consolidated_report.py',
     "            add('OV1_RETROSPECTIVE', RET.LABEL, s['target'], 'score_after_this_draw',", "            add('OV1_RETROSPECTIVE', FORMAL_LABEL, s['target'], 'score_after_this_draw',", VIEWS),
    ('report: the guarantee printed without its assumptions', E + 'consolidated_report.py',
     "          f'{s[\"bar\"]} is at most 1 in {s[\"bar\"]} (2.5%), provided that: ' + '; '.join(f['assumptions']) + '.')\n",
     "          f'{s[\"bar\"]} is at most 1 in {s[\"bar\"]} (2.5%).')\n", VIEWS),
    ('report: a current revision in the retired index', E + 'consolidated_report.py',
     "        if e['status'] != 'RETIRED':\n            continue\n", "        if False:\n            continue\n", INDEX),
    ('report: matched over any draw, not every variant\'s', E + 'consolidated_report.py',
     "    common = sorted(set.intersection(*[set(by[k]) for k in keys])) if keys else []\n",
     "    common = sorted(set.intersection(*[set(by[k]) for k in keys[:1]])) if keys else []\n", INDEX),
    ('report: a part that cannot be computed stops the report', E + 'consolidated_report.py',
     "    except RET.RetroRefused as exc:\n        return {'label': RET.LABEL, 'statement': RET.STATEMENT, 'state': 'NOT_AVAILABLE',",
     "    except ZeroDivisionError as exc:\n        return {'label': RET.LABEL, 'statement': RET.STATEMENT, 'state': 'NOT_AVAILABLE',", FAILS),
    ('report: an unreadable formal ledger shown as running', E + 'consolidated_report.py',
     "    except OV.OV1Blocked as exc:\n        return {'label': FORMAL_LABEL, 'state': 'NOT_AVAILABLE', 'reason': str(exc)}\n",
     "    except OV.OV1Blocked as exc:\n        return {'label': FORMAL_LABEL, 'state': 'NOT_REGISTERED', 'reason': str(exc)}\n", STATES),
    ('report: the orphan marker ignored', E + 'consolidated_report.py', "    if m.exists() or m.is_symlink():\n", "    if False:\n", FAILS),
    ('report: the quoted league table rebuilt, not read', E + 'consolidated_report.py',
     "    raw = LP._archived(root, game_id, m)[f'{m[\"name\"]}.txt']\n",
     "    raw = LT.build(LS.collect(root, game_id)[0], LP._identity(m))['txt'] + b'\\n'\n", POOL),
    # ---- L8, the weekly sequencer (design Appendix F; plan L8 and section 7)
    ('weekly: the table published before the session is closed', 'src/Weekly_Session_Orchestrator.py',
     "    code, _f = forecast('close-session', '--game', g, '--session', session)\n    if code != 0:\n        return live_stop('close-session', code)\n",
     "", ORDER),
    ('weekly: no OV-1 record after a score', 'src/Weekly_Session_Orchestrator.py',
     "            last_scored = target\n            record_ov1(f'after the score of draw {target}')\n", "            last_scored = target\n", ORDER),
    ('weekly: no OV-1 record at the end of the loop', 'src/Weekly_Session_Orchestrator.py',
     "            record_ov1(f'at the end of the loop ({state}' + (f', draw {target})' if target != '-' else ')'))\n", "", ORDER),
    ('weekly: OV-1\'s state line not read', 'src/Weekly_Session_Orchestrator.py',
     "        if code != 0 or state not in OV1_FINE:              # the state line is read, not only the exit code\n",
     "        if code != 0:\n", STATE),
    ('weekly: a stopped stream not announced', 'src/Weekly_Session_Orchestrator.py',
     "        ov1_stopped = ov1_stopped or state == 'STOPPED'\n", "        ov1_stopped = False\n", STATE),
    ('weekly: a table failure reported as complete', 'src/Weekly_Session_Orchestrator.py',
     "    table_ok = code == 0 and f.get('state') in ('PUBLISHED', 'UP_TO_DATE')\n", "    table_ok = True\n", FMT),
    ('weekly: an OV-1 failure reported as complete', 'src/Weekly_Session_Orchestrator.py',
     "    if table_ok and not ov1_trouble:\n", "    if table_ok:\n", BLOCK),
    ('weekly: a failed score does not stop the live path', 'src/Weekly_Session_Orchestrator.py',
     "            if code != 0 or f.get('state') != 'SCORED':\n", "            if False:\n", LIVE),
    ('weekly: an existing lock ignored', 'src/Weekly_Session_Orchestrator.py',
     "        if (SC.ROOT / 'results' / 'real' / 'weekly' / g / 'ACTIVE_SESSION.lock').exists():\n", "        if False:\n", LIVE),
    ('weekly: both reporting failures given one status', 'src/Weekly_Session_Orchestrator.py',
     "    return EXIT_BOTH if ov1_trouble and not table_ok else EXIT_OV1 if ov1_trouble else EXIT_TABLE\n",
     "    return EXIT_OV1 if ov1_trouble else EXIT_TABLE\n", BLOCK),
    # ---- L8, the development sequencer (plan L8, 12A)
    ('batch: an exploratory rerun sent to admission', 'src/Development_Batch_Orchestrator.py',
     "        if kind not in ADMITTED_KINDS:\n", "        if False:\n", RERUN),
    ('batch: a routine fill not admitted', 'src/Development_Batch_Orchestrator.py',
     "ADMITTED_KINDS = ('ROUTINE_FILL', 'WF_BATCH_PLAN_V1')\n", "ADMITTED_KINDS = ('WF_BATCH_PLAN_V1',)\n", FILL),
    ('batch: a reported batch reported again', 'src/Development_Batch_Orchestrator.py',
     "        if f['report'] == '-':\n", "        if True:\n", FILL),
    ('batch: nothing to fill treated as a stop', 'src/Development_Batch_Orchestrator.py',
     "            if code == 0 and f.get('state') == 'NOTHING_TO_FILL':\n", "            if False:\n", FILL),
    ('batch: a fill ends without publishing', 'src/Development_Batch_Orchestrator.py',
     "        code, f = league('publish', '--game', g)\n        if code != 0 or f.get('state') not in ('PUBLISHED', 'UP_TO_DATE'):\n            return stop('publish', code, batch, g)\n",
     "        f = {'state': 'UP_TO_DATE'}\n", FILL),
    ('batch: nothing-to-fill is a refusal again', 'src/methods/Method_Walk_Forward.py',
     "    except WF.NothingToFill as exc:\n", "    except ZeroDivisionError as exc:\n", FILL),
    ('batch: a fill planned over an unadmitted report', C + 'walk_forward.py',
     "        if waiting:\n            b, s, l = waiting[0]\n", "        if False:\n            b, s, l = waiting[0]\n",
     SQ + '.Batches.test_a_fill_waits_for_a_report_that_is_not_yet_admitted'),
    ('ov1 tool: an unregistered game refuses', E + 'Method_OV1.py',
     "            if OV.OR.absent(OV.registration_path(OV._root(), args.game)):\n", "            if False:\n", STATE),
    # ---- L8, the shared child launcher (design 6.1)
    ('children: any argument forwarded', 'src/sequencer_children.py', "        if not SAFE_ARG.fullmatch(a):\n", "        if False:\n", KIDS),
    ('children: a loose result line parsed', 'src/sequencer_children.py',
     "    if not RESULT_LINE.fullmatch(line):\n        return None\n", "    if ' RESULT ' not in line or '=' not in line:\n        return None\n", KIDS),
    ('children: a shell', 'src/sequencer_children.py', "cwd=str(ROOT), shell=False)", "cwd=str(ROOT), shell=True)", STATIC),
    ('layers: the scoring half imports the league', E + 'weekly_score.py',
     "from . import collect as COL\n", "from . import collect as COL\nfrom . import league_sources as _LS\n", LAYERS),
]

env = dict(os.environ)
env['PYTHONPATH'] = os.pathsep.join(str(tree / d) for d in ('src', 'src/methods', 'tests'))
env['PYTHONDONTWRITEBYTECODE'] = '1'
survived = caught = 0
for name, rel, old, new, test in MUTANTS:
    if only and not any(o in name for o in only):
        continue
    path = tree / rel
    raw = path.read_bytes()
    text = raw.decode('ascii')
    if text.count(old) != 1:
        print(f'NOT APPLIED  {name}: the old text occurs {text.count(old)} times in {rel}', flush=True)
        survived += 1
        continue
    try:
        path.write_bytes(text.replace(old, new).encode('ascii'))
        r = subprocess.run([sys.executable, '-B', '-m', 'unittest', test], cwd=tree, env=env, capture_output=True, text=True)
    finally:
        path.write_bytes(raw)
    if r.returncode != 0 and ('FAILED' in r.stderr):
        caught += 1
        print(f'CAUGHT       {name}  [{test}]', flush=True)
    else:
        survived += 1
        print(f'SURVIVED     {name}  [{test}]  exit {r.returncode}: {r.stderr.strip().splitlines()[-1] if r.stderr.strip() else ""}', flush=True)
print(f'mutants caught {caught}; survived or not applied {survived}')
sys.exit(1 if survived else 0)
