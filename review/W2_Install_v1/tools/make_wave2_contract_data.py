"""Write E_2's, E_17's, E_18's and E_19's revision 1 declarations and FORMULA_OPEN registry entries (Claude, 30 Oct 2026).

Made from the wave 1 generator (itself from the new-method template's make_contract_data.py.txt).
Usage: python3 -I make_wave2_contract_data.py TREE
TREE is a disposable checkout with the method folders already copied in. The files are created, never
overwritten, under src/methods/_common/contract_data/. Every record is validated by the installed contract
validators and written as canonical bytes. All four methods are score-only (owner decision W2-4).
"""
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(tree / 'src' / 'methods')]
from _common.contract_records import canonical, record_digest, validate_declaration, validate_registry_entry  # noqa: E402
from _common.game_profiles import get_profile  # noqa: E402
from E_002.variants import VARIANTS as V2  # noqa: E402
from E_017.variants import VARIANTS as V17  # noqa: E402
from E_018.variants import VARIANTS as V18  # noqa: E402
from E_019.variants import VARIANTS as V19  # noqa: E402

DATE = '2026-10-30'
SPEC = 'doc/Predictive_Randomness_Wave2_E2_E17_E18_E19_Design_v0_1r2.md'


def words(method, variant, cfg):
    """(one-line description of the variant, sentences for the short explanation)."""
    if method == 'E_2':
        stat, last_n, _m = cfg
        gaps = 'all its gaps' if last_n is None else f'its last {last_n} gaps'
        kind = 'average' if stat == 'mean' else 'middle'
        return (f'how close its next draw would come to completing its usual gap (the {kind} of {gaps})',
                f'For each number it takes the {kind} length of {gaps} between appearances (or the fair-draw '
                f'average gap if it has none) and asks how close the gap the next draw would complete comes to '
                f'that length: its usual return is due now, rather than it being the longest overdue.')
    if method == 'E_17':
        form, c, window, _m = cfg
        if form == 'logage':
            return ('how long it has been absent, in the direction learned from the data (Method A)',
                    'It measures, over all the numbers together, whether a number is more or less likely to come '
                    'up the longer it has been absent, using the logarithm of the absence (the owner\'s Method A). '
                    'If longer absence goes with more appearances, it ranks the longest absent first; if with '
                    'fewer, the most recently drawn first; if neither, all numbers tie.')
        span = 'all earlier draws' if window is None else f'the last {window} draws'
        return (f'the chance, learned from {span}, that a number absent for as long as it has been comes up next',
                f'It groups absences into seven lengths and estimates, over all the numbers together and over '
                f'{span}, how often a number absent for each length came up at the next draw, pulled towards the '
                f'fair rate by {c} fair draws. Each number scores the estimate for its present absence.')
    if method == 'E_19':
        T, c, d, _m = cfg
        return (f'a repeating {T}-draw cycle in its returns, on top of the general effect of absence',
                f'It looks for a repeating {T}-draw cycle in how long each number stays away, for example from '
                f'draw machines or ball sets used in turn. It starts from E_17\'s estimate for the present '
                f'absence and multiplies it by the number\'s own cycle factor, shrunk towards all numbers\' factor '
                f'and with the number\'s overall rate divided out.')
    window, c, _m = cfg
    span = 'all its gaps' if window is None else f'its gaps within the last {window} draws'
    return (f'its chance of returning now under its own mix of four return patterns, fitted to {span}',
            f'It describes each number\'s gaps between appearances ({span}) as a mix of four fixed patterns: quick '
            f'returns, fair returns, long absences and evenly spaced returns, fitted exactly and pulled towards '
            f'the fair pattern by {c} fair gaps. Each number scores its chance of returning now under its mix.')


METHODS = {
    'E_2': ('Expected Recurrence-Interval Alignment', V2, 'RECURRENCE_INTERVAL_ALIGNMENT_V1'),
    'E_17': ('Discrete Recurrence Hazard Curves', V17, 'DISCRETE_RECURRENCE_HAZARD_V1'),
    'E_19': ('Periodic Recurrence-Hazard Peaks', V19, 'PERIODIC_RESIDUE_HAZARD_V1'),
    'E_18': ('Mixtures of Recurrence Modes', V18, 'FIXED_LIBRARY_GAP_MIXTURE_MINCHISQ_V1'),
}


def channel():
    return {'ranking_kind': 'RANKING_WITH_SCORES', 'score_type': 'FLOAT64', 'order_ties': 'NOT_APPLICABLE',
            'top_rule_id': 'TOP_MARGINAL', 'worst_rule_id': 'INVERSE',
            'readout_selection_rule_version': 'TOP_MARGINAL_AND_INVERSE_V1',
            'ranking_tie_readout_version': 'TIE_SHA256_V1', 'probability_kind': 'NONE',
            'probability_sum_tolerance': None, 'smoothing_note': None, 'calibration_note': None}


def declaration(game, method, variant, cfg):
    _name, _v, fit = METHODS[method]
    p = get_profile(game)
    return validate_declaration({
        'schema': 'METHOD_DECLARATION_V1', 'game_id': game, 'profile_version': p.version, 'era_id': p.era_id,
        'method_id': method, 'variant_id': variant, 'method_revision': '1', 'observation_views': ['UNORDERED_SET'],
        'uses_dates': False, 'minimum_history_draws': cfg[-1], 'stochastic_fit': False, 'fit_seed_policy_id': None,
        'fit_sampling_model_version': fit,
        'channels': {b.barrel_id: channel() for b in p.barrels},
        'diagnostic_schema_id': None, 'is_capability': 'IS_NOT_APPLICABLE', 'is_interface_version': None,
        'source_method_dependencies': []})


def entry(decl, cfg):
    method = decl['method_id']
    name, _v, _fit = METHODS[method]
    one, long = words(method, decl['variant_id'], cfg)
    short = (f'{method} looks at how long each number has been away since it was last drawn. {long} It ranks the '
             f'numbers by that value: its top pick is the highest-ranked numbers and its inverse pick the '
             f'lowest-ranked, with exact ties settled by the project tie rule (TIE_SHA256_V1). Its scores are not '
             f'chances, so no probabilities are published. It uses only which numbers were drawn, not their order '
             f'or the dates, and needs {cfg[-1]} earlier draws. If the draws are fair, it is not expected to beat '
             f'chance.')
    return validate_registry_entry({
        'schema': 'REGISTRY_ENTRY_V1', 'game_id': decl['game_id'], 'method_id': method,
        'variant_id': decl['variant_id'], 'entry_sequence': 1, 'method_revision': '1',
        'declaration_digest': record_digest(decl), 'registry_status': 'FORMULA_OPEN',
        'registry_status_reason': ('Revision 1 installed for review and not yet released (E2R-R58): '
                                   'IN_DEVELOPMENT.txt is present and no SUPPORTED entry exists.'),
        'method_name': name, 'one_liner': f'Ranks every number by {one}.', 'short_explanation': short,
        'text_provenance': {'author': 'Claude (primary designer and coder)', 'date': DATE, 'text_version': 'v1',
                            'source_reference': f'{SPEC} sections 3-7; R2 v0.5 sections 7.1 and 7.17; R1 v0.4; E2R-1 v0.3r3 E2R-R21A'},
        'effective_date': DATE, 'previous_entry_digest': None})


root = tree / 'src' / 'methods' / '_common' / 'contract_data'
for method, (_n, variants, _fit) in METHODS.items():
    for game in ('POWERBALL', 'OZLOTTO'):
        for variant, cfg in variants.items():
            d = declaration(game, method, variant, cfg)
            e = entry(d, cfg)
            for path, rec in ((root / 'declarations' / game / method / variant / 'r1.json', d),
                              (root / 'registry' / game / method / variant / 'entry_0001.json', e)):
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open('xb') as fh:
                    fh.write(canonical(rec))
                print(record_digest(rec), path.relative_to(tree).as_posix())
