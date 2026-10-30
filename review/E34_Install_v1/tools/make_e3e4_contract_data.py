"""Write E_3's and E_4's revision 1 declarations and FORMULA_OPEN registry entries (Claude, 30 Oct 2026).

Made from the new-method template's generator (doc/METHOD_TEMPLATE/make_contract_data.py.txt).
Usage: python3 -I make_e3e4_contract_data.py TREE
TREE is a disposable checkout with the method folders already copied in. The files are created, never
overwritten, under src/methods/_common/contract_data/. Every record is validated by the installed contract
validators and written as canonical bytes.
"""
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(tree / 'src' / 'methods')]
from _common.contract_records import canonical, record_digest, validate_declaration, validate_registry_entry  # noqa: E402
from _common.game_profiles import get_profile  # noqa: E402
from E_003.variants import VARIANTS as V3  # noqa: E402
from E_004.variants import VARIANTS as V4  # noqa: E402

assert dict(V3) == dict(V4)
DATE = '2026-10-30'
SPEC = 'doc/Predictive_Randomness_E3_E4_Polynomial_Fit_Design_v0_1.md'
FIT_VERSION = {'LS': 'POLY_LS_RAW_V1', 'INTERP': 'POLY_INTERP_CHEB_NODES_SMOOTHED_V1',
               'MINIMAX': 'POLY_MINIMAX_SMOOTHED_V1'}
METHODS = {
    'E_3': ('Occurrence-Curve Endpoint Forecast', 'the fitted curve\'s value at the next draw', 'value'),
    'E_4': ('Occurrence-Curve Gradient Forecast', 'the fitted curve\'s slope at the next draw', 'slope'),
}


def fit_words(cfg):
    fit, window, degree, half, _nodes = cfg
    span = f'the last {window} draws'
    if fit == 'LS':
        return (f'a least-squares polynomial of degree {degree} over {span}',
                f'It fits the polynomial of degree {degree} that makes the total squared error smallest, over the 0/1 '
                f'record of {span}.')
    smooth = f'a running average over up to {2 * half + 1} draws'
    if fit == 'INTERP':
        return (f'a polynomial of degree {degree} through {degree + 1} smoothed points of {span}',
                f'It first smooths the 0/1 record of {span} with {smooth}, then passes a polynomial of degree {degree} '
                f'exactly through {degree + 1} of those smoothed values, placed at Chebyshev nodes so the curve does '
                f'not swing wildly.')
    return (f'a Chebyshev minimax polynomial of degree {degree} over {span}, smoothed',
            f'It first smooths the 0/1 record of {span} with {smooth}, then fits the polynomial of degree {degree} '
            f'whose worst single error is as small as possible (Chebyshev minimax, found exactly by the exchange '
            f'method).')


def channel():
    return {'ranking_kind': 'RANKING_WITH_SCORES', 'score_type': 'FLOAT64', 'order_ties': 'NOT_APPLICABLE',
            'top_rule_id': 'TOP_MARGINAL', 'worst_rule_id': 'INVERSE',
            'readout_selection_rule_version': 'TOP_MARGINAL_AND_INVERSE_V1',
            'ranking_tie_readout_version': 'TIE_SHA256_V1', 'probability_kind': 'NONE',
            'probability_sum_tolerance': None, 'smoothing_note': None, 'calibration_note': None}


def declaration(game, method, variant, cfg):
    p = get_profile(game)
    return validate_declaration({
        'schema': 'METHOD_DECLARATION_V1', 'game_id': game, 'profile_version': p.version, 'era_id': p.era_id,
        'method_id': method, 'variant_id': variant, 'method_revision': '1', 'observation_views': ['UNORDERED_SET'],
        'uses_dates': False, 'minimum_history_draws': cfg[1], 'stochastic_fit': False, 'fit_seed_policy_id': None,
        'fit_sampling_model_version': FIT_VERSION[cfg[0]],
        'channels': {b.barrel_id: channel() for b in p.barrels}, 'diagnostic_schema_id': None,
        'is_capability': 'IS_NOT_APPLICABLE', 'is_interface_version': None, 'source_method_dependencies': []})


def entry(decl, cfg):
    name, scored, word = METHODS[decl['method_id']]
    fit_one, fit_long = fit_words(cfg)
    one = f'Ranks every number by {scored}, using {fit_one} fitted to its record of being drawn or not.'
    short = (f'{decl["method_id"]} looks at each number on its own, as a record of 1 (drawn) or 0 (not drawn) over '
             f'recent draws. {fit_long} It then ranks the numbers by {scored}: its top pick is the highest-ranked '
             f'numbers and its inverse pick the lowest-ranked, with exact ties settled by the project tie rule '
             f'(TIE_SHA256_V1). The scores are curve {word}s, not chances, so no probabilities are published. A curve '
             f'fitted to a short, noisy record is least reliable exactly at its end, which is where this method '
             f'looks; that is what the experiment measures. It uses only which numbers were drawn, not their order '
             f'or the dates, and needs {cfg[1]} earlier draws. If the draws are fair, it is not expected to beat '
             f'chance.')
    return validate_registry_entry({
        'schema': 'REGISTRY_ENTRY_V1', 'game_id': decl['game_id'], 'method_id': decl['method_id'],
        'variant_id': decl['variant_id'], 'entry_sequence': 1, 'method_revision': '1',
        'declaration_digest': record_digest(decl), 'registry_status': 'FORMULA_OPEN',
        'registry_status_reason': ('Revision 1 installed for review and not yet released (E2R-R58): '
                                   'IN_DEVELOPMENT.txt is present and no SUPPORTED entry exists.'),
        'method_name': name, 'one_liner': one, 'short_explanation': short,
        'text_provenance': {'author': 'Claude (primary designer and coder)', 'date': DATE, 'text_version': 'v1',
                            'source_reference': f'{SPEC} sections 3-5; R2 v0.5 section 7.1; E2R-1 v0.3r3 E2R-R21A'},
        'effective_date': DATE, 'previous_entry_digest': None})


root = tree / 'src' / 'methods' / '_common' / 'contract_data'
for method in ('E_3', 'E_4'):
    for game in ('POWERBALL', 'OZLOTTO'):
        for variant, cfg in V3.items():
            d = declaration(game, method, variant, cfg)
            e = entry(d, cfg)
            for path, rec in ((root / 'declarations' / game / method / variant / 'r1.json', d),
                              (root / 'registry' / game / method / variant / 'entry_0001.json', e)):
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open('xb') as fh:
                    fh.write(canonical(rec))
                print(record_digest(rec), path.relative_to(tree).as_posix())
