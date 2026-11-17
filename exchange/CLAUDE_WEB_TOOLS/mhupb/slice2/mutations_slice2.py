"""MHUP-B slice 2: mutation checks (design Appendix L; code plan v0.3 section 6.5: one planted defect per rule, each
caught by a named test).

For each mutant: one counted edit to one file of a built dev TREE, the named test is run in its own process and must
FAIL; the file is then restored byte for byte. A mutant that survives is reported and the tool exits 1.
Usage: python3 -I mutations_slice2.py TREE [name-substring ...]

Not listed, because they are equivalent (each is one of two guards on the same fact, tried 18 November 2026):
  * the first cut-off test in ov1._due ("if WR.now_utc() >= cut"): the second reading of the clock, taken last, stops
    the same cases; the second one is listed;
  * 'NEXT_DRAW_SET' in the pre-cut-off test: a catch-up line is always frozen after the draw, so after the cut-off;
  * check_score_linkage in ov1.factor_step: the digest comparison beside it refuses the same planted line;
  * "the freeze line names the variant" in the planner (walk_forward._fill_pairs): a named record always has its session
    ticket, which the next condition finds; at the gate the two are separate and both are listed;
  * the first plan kind's cap in report.run_report: a plan of the first kind cannot reach the holdout (make_plan
    refuses it), so the window check beside it refuses the same request;
  * the "drawn numbers disagree" test in ov1.factor_step: X by matches and by weights then disagree, the same stop;
  * the byte comparison of an eligibility line in ov1.verify: the factor line's rebuild refuses the same altered ledgers.
"""
import os
import subprocess
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
only = sys.argv[2:]
C = 'src/methods/_common/'
E = 'src/evaluation/'
KT, RT = 'tests.test_mhupb_ov1_numeric', 'tests.test_mhupb_ov1'
P, D, FT, X = KT + '.Primitives', KT + '.Distribution', KT + '.FactorTable', KT + '.Crossing'
DB = 'tests.test_mhupb_dev_batch'
GT = DB + '.Gate.test_every_refusal_of_the_dev_batch_branch'
R2A = DB + '.Plans.test_rule_2a_back_history_by_the_release_instant'
SRC = DB + '.Sources.test_canonical_coverage_and_the_source_list'
REL = DB + '.Reports.test_the_release_rules_of_the_outcome_reader'

MUTANTS = [
    # ---- L5, the kernel (plan 6.5): a rounding direction flipped in each primitive; a remainder dropped; the margin
    #      dropped; the certificate skipped; the crossing compared on an upper bound; a float used
    ('exp: a lower term rounded up', E + 'ov1_numeric.py',
     "        tl = _fdiv(tl * a, S * k)\n", "        tl = _cdiv(tl * a, S * k)\n", P + '.test_exp_encloses_the_fraction_oracle_and_decimal'),
    ('exp: an upper term rounded down', E + 'ov1_numeric.py',
     "        tu = _cdiv(tu * a, S * k)\n", "        tu = _fdiv(tu * a, S * k)\n", P + '.test_exp_encloses_the_fraction_oracle_and_decimal'),
    ('exp: the remainder dropped', E + 'ov1_numeric.py',
     "    return lo, hi + 2 * tu + 1\n", "    return lo, hi\n", P + '.test_enclosures_hold_with_few_terms_so_the_remainders_matter'),
    ('exp: the lower square rounded up', E + 'ov1_numeric.py',
     "    return _fdiv(lo * lo, S), _cdiv(hi * hi, S)\n", "    return _cdiv(lo * lo, S), _cdiv(hi * hi, S)\n",
     P + '.test_squaring_rounds_each_end_the_right_way_exactly'),
    ('exp: the upper square rounded down', E + 'ov1_numeric.py',
     "    return _fdiv(lo * lo, S), _cdiv(hi * hi, S)\n", "    return _fdiv(lo * lo, S), _fdiv(hi * hi, S)\n",
     P + '.test_squaring_rounds_each_end_the_right_way_exactly'),
    ('exp: the ends swapped for a negative argument', E + 'ov1_numeric.py',
     "        return _fdiv(S * S, hi), _cdiv(S * S, lo)\n", "        return _fdiv(S * S, lo), _cdiv(S * S, hi)\n",
     P + '.test_exp_encloses_the_fraction_oracle_and_decimal'),
    ('exp: reduced by the floor (the probe\'s hole)', E + 'ov1_numeric.py',
     "    while -((-a) >> j) > S:", "    while (a >> j) > S:", P + '.test_exp_encloses_the_fraction_oracle_and_decimal'),
    ('log: the lower end rounded up', E + 'ov1_numeric.py',
     "        y = _cdiv((m - S) * S, m + S) if up else _fdiv((m - S) * S, m + S)\n",
     "        y = _cdiv((m - S) * S, m + S)\n", P + '.test_log_is_checked_through_the_exponential_oracle_and_decimal'),
    ('log: the upper terms rounded down', E + 'ov1_numeric.py',
     "            total += _cdiv(term, 2 * k + 1) if up else _fdiv(term, 2 * k + 1)\n",
     "            total += _fdiv(term, 2 * k + 1)\n", P + '.test_log_is_checked_through_the_exponential_oracle_and_decimal'),
    ('log: the remainder dropped', E + 'ov1_numeric.py',
     "            total += _cdiv(term * S, S - y2) + 1\n", "            total += 0\n",
     P + '.test_enclosures_hold_with_few_terms_so_the_remainders_matter'),
    ('sqrt: the upper end not above', E + 'ov1_numeric.py',
     "isqrt(_cdiv(p * S * S, q)) + 1\n", "isqrt(_cdiv(p * S * S, q))\n", P + '.test_sqrt_bounds_are_exact'),
    ('the margin dropped', E + 'ov1_numeric.py',
     "            row[x] = lo - MARGIN\n", "            row[x] = lo\n",
     FT + '.test_stored_is_never_above_the_true_factor_and_the_loss_is_below_twice_the_margin'),
    ('the stored factor taken from the upper end', E + 'ov1_numeric.py',
     "            row[x] = lo - MARGIN\n", "            row[x] = hi\n",
     FT + '.test_stored_is_never_above_the_true_factor_and_the_loss_is_below_twice_the_margin'),
    ('the certificate skipped', E + 'ov1_numeric.py',
     "        if sum(c * exp_enc(row[x])[1] for x, c in dist.items()) > total * S:\n", "        if False:\n",
     FT + '.test_the_certificate_catches_an_error_in_the_derivation'),
    ('the certificate on the lower end of exp', E + 'ov1_numeric.py',
     "        if sum(c * exp_enc(row[x])[1] for x, c in dist.items()) > total * S:\n",
     "        if sum(c * exp_enc(row[x])[0] for x, c in dist.items()) > (total + 1) * S:\n",
     FT + '.test_the_certificate_catches_an_error_in_the_derivation'),
    ('the width check skipped', E + 'ov1_numeric.py',
     "            if hi - lo >= MARGIN:\n", "            if False:\n", FT + '.test_a_failed_certificate_or_a_wide_enclosure_refuses'),
    ('the crossing compared on an upper bound', E + 'ov1_numeric.py',
     "    return sum(exp_enc(L)[0] for L in logs) >= len(LAMBDAS) * BAR * S\n",
     "    return sum(exp_enc(L)[1] for L in logs) >= len(LAMBDAS) * BAR * S\n", X + '.test_the_bar_at_the_edge'),
    ('a float used', E + 'ov1_numeric.py',
     "    return a // b                             # exact floor (b > 0)\n", "    return int(a / b)\n",
     KT + '.Static'),
    ('a number counted twice in the distribution', E + 'ov1_numeric.py',
     "        for k in range(K - 1, -1, -1):\n", "        for k in range(K):\n", D + '.test_counts_equal_brute_force_on_small_barrels'),
    ('the grouped route miscounts', E + 'ov1_numeric.py',
     "                new[key] = new.get(key, 0) + c * comb(m, j)\n", "                new[key] = new.get(key, 0) + c * m\n",
     D + '.test_counts_equal_brute_force_on_small_barrels'),
    ('the variance with the wrong denominator', E + 'ov1_numeric.py',
     "(n - 1) * n\n", "n * n\n", D + '.test_full_size_routes_agree_and_the_variance_is_the_formula'),
    ('zero variance not skipped', E + 'ov1_numeric.py',
     "    if v_num == 0:\n        return None\n", "", FT + '.test_zero_variance_is_the_registered_skip'),
    ('the frozen bytes changed', E + 'ov1_numeric.py',
     "            out.append(f'{num}/{den} {x} {table[\"counts\"][x]} {row[x]}')\n",
     "            out.append(f'{num}/{den} {x} {row[x]}')\n", FT + '.test_frozen_fixture_digests'),
    # ---- L5, the recorder
    ('the cut-off twelve hours later', E + 'ov1.py',
     "    return datetime(d.year, d.month, d.day, 1, 30, tzinfo=timezone.utc)\n",
     "    return datetime(d.year, d.month, d.day, 13, 30, tzinfo=timezone.utc)\n", RT + '.CutOff.test_the_cutoff_is_never_after_noon_in_adelaide'),
    ('an eligibility line durable after the cut-off', E + 'ov1.py',
     "        if written >= cut:\n", "        if False:\n", RT + '.CutOff.test_the_cutoff_passing_while_the_line_is_prepared_is_a_stop'),
    ('an eligibility line with the result in the master', E + 'ov1.py',
     "        if last.last_draw >= t:\n", "        if False:\n",
     RT + '.CutOff.test_the_result_already_in_the_master_before_the_cutoff_writes_no_eligibility'),
    ('a late freeze line counted', E + 'ov1.py',
     "line['set_kind'] == 'NEXT_DRAW_SET' and WR.parse_utc(line['frozen_utc']) < cut)\n",
     "line['set_kind'] == 'NEXT_DRAW_SET')\n", RT + '.CutOff.test_the_same_late_line_seen_first_is_still_missed'),
    ('a missed line before the cut-off', E + 'ov1.py',
     "    if now < cut:\n        return None", "    if False:\n        return None",
     RT + '.Missed.test_missed_weeks_then_a_counted_draw_in_order'),
    ('a missed line without the reconciliation', E + 'ov1.py',
     "    reconcile(root, game_id, st, lines, torn, now)\n", "", RT + '.Missed.test_every_reconciliation_failure_blocks_and_the_stream_resumes'),
    ('a torn forecast ledger accepted', E + 'ov1.py',
     "    if torn:\n        raise OV1Blocked('the forecast ledger ends in an unfinished line')\n", "",
     RT + '.Missed.test_every_reconciliation_failure_blocks_and_the_stream_resumes'),
    ('a freeze time after the clock accepted', E + 'ov1.py',
     "    if lines and WR.parse_utc(lines[-1]['frozen_utc']) > now:\n", "    if False:\n",
     RT + '.Missed.test_a_freeze_time_later_than_the_clock_blocks'),
    ('a named extent not checked', E + 'ov1.py',
     "        if type(ext) is not dict or not JL.extent_still_there(lines, ext):\n", "        if False:\n",
     RT + '.Missed.test_a_publication_manifest_that_names_a_lost_extent_blocks'),
    ('a named freeze line not checked', E + 'ov1.py',
     "        if line is None or record_digest(line) != digest:\n", "        if False:\n",
     RT + '.Missed.test_every_reconciliation_failure_blocks_and_the_stream_resumes'),
    ('the witness ledger not reconciled', E + 'ov1.py',
     "            freeze(w['target_draw_number'], w['freeze_line_digest'], 'a witness line')\n", "            pass\n",
     RT + '.Missed.test_every_reconciliation_failure_blocks_and_the_stream_resumes'),
    ('the score ledger not reconciled', E + 'ov1.py',
     "        SI.scored_identities(root, game_id, lines)             # every score line names its target's freeze line\n", "",
     RT + '.Missed.test_every_reconciliation_failure_blocks_and_the_stream_resumes'),
    ('a late record counted', E + 'ov1.py',
     " or r['effective_class'] != 'PROSPECTIVE':\n", ":\n", RT + '.Counted.test_only_complete_prospective_pairs_count'),
    ('a failure record counted', E + 'ov1.py',
     "        if r['record_kind'] != 'FORECAST' or r['run_mode']", "        if r['run_mode']",
     RT + '.Counted.test_only_complete_prospective_pairs_count'),
    ('half a pair counted', E + 'ov1.py',
     "        if pair[0] is None or pair[1] is None:\n", "        if pair[0] is None and pair[1] is None:\n",
     RT + '.Counted.test_only_complete_prospective_pairs_count'),
    ('a malformed ticket counted', E + 'ov1.py',
     "            if len(labels) != NUM.K or len(set(labels)) != NUM.K or \\\n", "            if \\\n",
     RT + '.Counted.test_only_complete_prospective_pairs_count'),
    ('WORST added instead of subtracted', E + 'ov1.py',
     "            weights[j - 1] -= 1\n", "            weights[j - 1] += 1\n", RT + '.Counted.test_three_weeks_against_the_oracles'),
    ('X not checked two ways', E + 'ov1.py',
     "    if x_matches != x_weights or x_weights not in table['counts']:\n", "    if x_weights not in table['counts']:\n",
     RT + '.Stops.test_x_by_matches_and_by_weights_must_agree'),
    ('X not checked against the sealed support', E + 'ov1.py',
     "    if x_matches != x_weights or x_weights not in table['counts']:\n", "    if x_matches != x_weights:\n",
     RT + '.Stops.test_x_outside_the_sealed_table_is_a_stop'),
    ('the sealed table not compared at scoring', E + 'ov1.py',
     "    if table is None or NUM.table_digest(table) != elig['factor_table_digest']:\n", "    if table is None:\n",
     RT + '.Stops.test_a_table_that_is_not_the_sealed_one_is_a_stop'),
    ('a draw with another date accepted', E + 'ov1.py',
     "        if not s['draw_date_is_derived']:\n", "        if False:\n",
     RT + '.Stops.test_a_draw_whose_date_is_not_its_derived_date_is_a_stop'),
    ('two routine scores accepted', E + 'ov1.py',
     "            if len(found) != 1:\n", "            if False:\n", RT + '.Stops.test_two_routine_score_lines_for_one_variant_is_a_stop'),
    ('a corrective score enters OV-1', E + 'ov1.py',
     "        if s['target_draw_number'] == t and s['scoring_policy_id'] == policy and s['amendment_of'] is None:\n",
     "        if s['target_draw_number'] == t:\n", RT + '.Stops.test_what_is_not_a_stop_waits_or_blocks_and_never_skips'),
    ('a replaced freeze line under a sealed draw accepted', E + 'ov1.py',
     "    if line is None or record_digest(line) != elig['freeze_line_digest'] or line['line_number'] != elig['freeze_line_number']:\n",
     "    if line is None:\n", RT + '.Stops.test_a_replaced_forecast_ledger_blocks_a_sealed_draw_and_is_not_a_stop'),
    ('a line appended after a stop', E + 'ov1.py',
     "        if st['stopped'] is not None:\n            break\n", "        if False:\n            break\n",
     RT + '.Stops.test_the_owners_stop_at_an_open_target_and_at_a_sealed_one'),
    ('the reader accepts a line after a stop', E + 'ov1.py',
     "        if st['stopped'] is not None:\n            raise OR.RecordRefused(f'{what}: a line after a stop')\n", "",
     RT + '.Stops.test_the_owners_stop_at_an_open_target_and_at_a_sealed_one'),
    ('registered after its first target is frozen', E + 'ov1.py',
     "    if WR.freeze_line_for(lines, t0) is not None:\n", "    if False:\n", RT + '.Registration.test_refusals'),
    ('registered after the deadline', E + 'ov1.py',
     "    if now >= WR.deadline(game_id, t0)[0]:\n", "    if False:\n",
     RT + '.Registration.test_after_the_deadline_of_the_next_draw_it_refuses'),
    ('registered without the developed record', E + 'ov1.py',
     "        developed = WR.developed(root, game_id)\n", "        developed = {'x': 1}\n", RT + '.Registration.test_refusals'),
    ('a registration under other rules accepted', E + 'ov1.py',
     "    if rec['rules'] != RULES or rec['tool'] != TOOL or rec['tool_version'] != OV1_VERSION:\n", "    if False:\n",
     RT + '.Registration.test_a_registration_under_other_rules_is_not_this_programs'),
    ('the crossing read from the display figure', E + 'ov1.py',
     "            'crossed': NUM.crossing(sums)}\n", "            'crossed': NUM.mixture_lower(sums) >= (NUM.BAR - 1) * NUM.S}\n",
     RT + '.Restart.test_the_bar'),
    ('the reader does not recheck the running sums', E + 'ov1.py',
     "            if any(row[k] != v for k, v in want.items()):\n", "            if False:\n",
     RT + '.Restart.test_verify_and_the_reader_catch_every_altered_line'),
    ('an eligibility line after its cut-off read as valid', E + 'ov1.py',
     "            if st['pending'] is not None or row['cutoff_utc'] != WR.utc_text(cut) or not when < cut or \\\n",
     "            if st['pending'] is not None or row['cutoff_utc'] != WR.utc_text(cut) or \\\n",
     RT + '.Restart.test_verify_and_the_reader_catch_every_altered_line'),
    ('verify does not rebuild the factor lines', E + 'ov1.py',
     "            if step[0] != 'FACTOR' or canonical({**row, **step[1]}) != canonical(row):\n", "            if False:\n",
     RT + '.Restart.test_verify_and_the_reader_catch_every_altered_line'),
    ('OV-1 opens the outcome reader', E + 'ov1.py',
     "from . import collect as COL\n", "from . import collect as COL\nfrom . import outcome_reader\n", RT + '.Isolation.test_statics'),
    # ---- L6, the DEV_BATCH branch of the dispatch gate
    ('a plan without its search-log row admitted', C + 'contract_dispatch.py',
     "            if not OR.search_log_names(root, 'DEV_BATCH', b['batch_id'], b['plan_digest']):\n", "            if False:\n", GT),
    ('a pin that is not the plan\'s admitted', C + 'contract_dispatch.py',
     "            if pin != OR.pin_of(plan, 'development plan'):\n", "            if False:\n", GT),
    ('a pair the plan does not list admitted', C + 'contract_dispatch.py',
     "            if not OR.dev_plan_lists_pair(plan, method, revision, variant, target):\n", "            if False:\n", GT),
    ('a second record for a pair of the batch', C + 'contract_dispatch.py',
     "            if OR.pair_has_done_ticket(rows, pair):\n                refuse('PAIR_ALREADY_DONE', 'the pair has a DONE ticket in this batch; no second record')\n",
     "            if False:\n                refuse('PAIR_ALREADY_DONE', 'the pair has a DONE ticket in this batch; no second record')\n", GT),
    ('a development run without its ticket', C + 'contract_dispatch.py',
     "in this batch; no second record')\n            if not OR.open_ticket_for(",
     "in this batch; no second record')\n            if False and not OR.open_ticket_for(", GT),
    ('a holdout development target before the seal', C + 'contract_dispatch.py',
     "                if not OR.mode_h_sealed(root, game):\n                    refuse('MODE_H_NOT_SEALED', 'a holdout or later development target",
     "                if False:\n                    refuse('MODE_H_NOT_SEALED', 'a holdout or later development target",
     DB + '.Plans.test_before_the_seal_the_old_cap_stands'),
    ('a target still open in the weekly session given to a batch', C + 'contract_dispatch.py',
     "                if len(lines) != 1:\n", "                if False:\n", GT),
    ('rule 2A: the release instant not compared', C + 'contract_dispatch.py',
     "                    if not _instant(frozen) < _instant(released):\n", "                    if False:\n", R2A),
    ('rule 2A: a variant the freeze line names', C + 'contract_dispatch.py',
     "                    if any(type(r) is dict and (r.get('method_id'),", "                    if False and any(type(r) is dict and (r.get('method_id'),", R2A),
    ('rule 2A: a weekly ticket ignored', C + 'contract_dispatch.py',
     "                    if OR.session_ticket_for_pair(root, game, pair):\n", "                    if False:\n", R2A),
    ('a batch of the second kind publishing under the weekly root', C + 'contract_runner.py',
     "        return OR.development_runs_root(PROJECT_ROOT)     # development run root only", "        return OR.weekly_runs_root(PROJECT_ROOT)     #",
     DB + '.Plans.test_a_routine_fill_plans_exactly_the_uncovered_pairs_and_runs_them'),
    ('a development forecast for the next draw', C + 'contract_runner.py',
     "kind not in ('WEEKLY_SESSION', 'OWNER_DIAGNOSTIC', 'DEV_BATCH'):", "kind not in ('WEEKLY_SESSION', 'OWNER_DIAGNOSTIC'):", GT),
    ('the DEV_BATCH binding under another mode', C + 'contract_records.py',
     "        if kind != 'WEEKLY_SESSION':\n            raise ValueError(f'{where}: a {mode} request must be bound to a weekly session')\n",
     "        if kind not in ('WEEKLY_SESSION', 'DEV_BATCH'):\n            raise ValueError(f'{where}: a {mode} request must be bound to a weekly session')\n", GT),
    # ---- L6, the planner and the driver
    ('a routine fill ignores what is covered', C + 'walk_forward.py',
     "            if (*key, t) not in covered:\n                pairs.append([*key, t])\n", "            if True:\n                pairs.append([*key, t])\n",
     DB + '.Plans.test_a_routine_fill_plans_exactly_the_uncovered_pairs_and_runs_them'),
    ('the cap lifted before the seal', C + 'walk_forward.py',
     "    return p.holdout_last if sealed else p.holdout_first - 1\n", "    return p.holdout_last\n", DB + '.Plans.test_before_the_seal_the_old_cap_stands'),
    ('rule 2A in the planner: frozen after the release', C + 'walk_forward.py',
     "                weekly = (WR.parse_utc(line['frozen_utc']) >= WR.parse_utc(released) or\n", "                weekly = (False or\n", R2A),
    ('a rerun over an accepted draw the session has not frozen', C + 'walk_forward.py',
     "            if t > p.holdout_last and (cap != p.holdout_last or t not in lines):\n", "            if False:\n",
     DB + '.Plans.test_an_exploratory_rerun_and_its_refused_windows'),
    ('a rerun of a variant that is not released', C + 'walk_forward.py',
     "            if unknown or not wanted or len(set(wanted)) != len(wanted):\n", "            if not wanted or len(set(wanted)) != len(wanted):\n",
     DB + '.Plans.test_an_exploratory_rerun_and_its_refused_windows'),
    ('runs of the second kind not ticketed', C + 'walk_forward.py',
     "TICKETED = ('MODE_H_BATCH', 'DEV_BATCH')", "TICKETED = ('MODE_H_BATCH',)",
     DB + '.Plans.test_a_routine_fill_plans_exactly_the_uncovered_pairs_and_runs_them'),
    ('an open ticket never closed on resume', C + 'walk_forward.py',
     "    if kind_of(plan) not in TICKETED:\n        return {}\n", "    if kind_of(plan) != 'MODE_H_BATCH':\n        return {}\n",
     DB + '.Gate.test_an_interrupted_batch_resumes_and_no_pair_is_run_twice'),
    # ---- L6, the source list and the coverage reader
    ('an exploratory rerun accepted as a canonical source', C + 'score_identities.py',
     "LEAGUE_SOURCE_KINDS = ('WF_BATCH_PLAN_V1', 'ROUTINE_FILL')", "LEAGUE_SOURCE_KINDS = ('WF_BATCH_PLAN_V1', 'ROUTINE_FILL', 'EXPLORATORY_RERUN')", SRC),
    ('coverage beyond the attempt\'s window', C + 'score_identities.py',
     "            if s['window_first'] <= t <= s['window_last']:\n", "            if True:\n", SRC),
    ('a listed plan\'s digest not checked', C + 'score_identities.py',
     " or kind != s['batch_kind'] or record_digest(plan) != s['plan_digest']:", " or kind != s['batch_kind']:", SRC),
    ('a listed plan\'s kind not checked', C + 'score_identities.py',
     " or kind != s['batch_kind'] or record_digest(plan) != s['plan_digest']:", " or record_digest(plan) != s['plan_digest']:", SRC),
    ('a source list of another shape accepted', C + 'score_identities.py',
     "        if (type(s) is not dict or set(s) != set(LEAGUE_SOURCE_FIELDS) or", "        if (type(s) is not dict or", SRC),
    # ---- L6, the report tool and the outcome reader
    ('a V2 report not checked for release before its row', E + 'report.py',
     "            if not OR.development_release_allowed(roots()['project'], game_id, t):\n", "            if False:\n",
     DB + '.Plans.test_before_the_seal_the_old_cap_stands'),
    ('a holdout outcome to a development report before the seal', E + 'outcome_reader.py',
     "        if OR.opening_record(repo_root, game_id) is None or not OR.mode_h_sealed(repo_root, game_id):\n            return False\n    except OR.RecordRefused:\n        return False\n    return target <=",
     "        pass\n    except OR.RecordRefused:\n        return False\n    return target <=",
     DB + '.Plans.test_before_the_seal_the_old_cap_stands'),
    ('a later outcome to a development report without its freeze line', E + 'outcome_reader.py',
     "    return target <= p.holdout_last or _weekly_release_allowed(repo_root, game_id, target)\n", "    return True\n", REL),
    ('the Mode H scorer\'s rule widened to the development rule', E + 'outcome_reader.py',
     "    released = development_release_allowed if development else outcome_release_allowed\n", "    released = development_release_allowed\n", REL),
    ('the development rule not used by the report', E + 'report.py',
     "                                development=True) if targets else {}\n", "                                development=False) if targets else {}\n",
     DB + '.Reports.test_a_v2_batch_is_reported_on_its_own_pairs'),
    ('the Mode H families loaded by a development report', E + 'report.py',
     "\n            if (f.get('evidence_tier') or 'DEVELOPMENT_WF_EXPLORATORY') == 'DEVELOPMENT_WF_EXPLORATORY']\n", "]\n",
     DB + '.Reports.test_families_are_loaded_by_window_and_tier'),
    ('a V2 batch reported over its whole window', E + 'collect.py',
     "    if WF.kind_of(plan) == 'DEV_BATCH':", "    if False:", DB + '.Reports.test_a_v2_batch_is_reported_on_its_own_pairs'),
    ('a registered family applied to a V2 report', E + 'report.py',
     "        families = []\n    else:\n", "        families = load_families(game_id, 1286, 1576)\n    else:\n",
     DB + '.Reports.test_a_v2_batch_is_reported_on_its_own_pairs'),
    ('the comparison ignores the scores', E + 'reforecast_compare.py',
     "        if x['scores'] != y['scores']:\n", "        if False:\n", DB + '.Reports.test_named_content_comparison'),
    ('the comparison ignores the TOP and WORST sets', E + 'reforecast_compare.py',
     "            if x[side] != y[side]:\n", "            if False:\n", DB + '.Reports.test_named_content_comparison'),
    ('a precondition not judged', E + 'reforecast_compare.py',
     "    ('the same environment', lambda fc, rc: rc.get('environment_identity')),\n", "", DB + '.Reports.test_named_content_comparison'),
]

env = dict(os.environ)
env['PYTHONPATH'] = os.pathsep.join(str(tree / d) for d in ('src', 'src/methods', 'tests'))
env['PYTHONDONTWRITEBYTECODE'] = '1'
survived = caught = 0
for name, rel, old, new, test in MUTANTS:
    if test is None or (only and not any(o in name for o in only)):
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
