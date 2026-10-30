"""Write E_6 revision 1's six declarations and six FORMULA_OPEN registry entries (Claude, 30 Oct 2026).

Usage: python3 -I make_e6_contract_data.py TREE
TREE is a checkout of the repository; the files are created (never overwritten) under
src/methods/_common/contract_data/. Every record is validated by the installed CODE-1 validators and
written as canonical bytes, so InstalledRegistry loads it unchanged.
"""
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(tree / 'src' / 'methods')]
from _common.contract_records import canonical, record_digest, validate_declaration, validate_registry_entry  # noqa: E402
from _common.game_profiles import get_profile  # noqa: E402
from E_006.beta_bernoulli import VARIANTS  # noqa: E402

DATE = '2026-10-30'
SPEC = 'doc/Predictive_Randomness_E6_Specification_and_Method_Template_Design_v0_1.md'
PK = {'MAIN': 'MARGINAL_INCLUSION_PROBABILITY', 'POWERBALL': 'PB_CATEGORICAL'}
SMOOTHING = 'Beta prior centred on the fair-draw inclusion rate and worth one draw.'
NOT_CALIBRATED = ('Not calibrated: the model ignores that the 7 main numbers are drawn together, and no '
                  'calibration has been tested.')
FULL = 'BETA_BERNOULLI_FULL_MEMORY_V1'
# The reviewer's terminology note (EX_051): only lam = 1 is the plain posterior; lam < 1 is a discounted update.
FIT_VERSION = {True: 'BETA_BERNOULLI_POSTERIOR_MEAN_V1', False: 'BETA_BERNOULLI_DISCOUNTED_UPDATE_V1'}
CALIBRATION = {True: 'Posterior means of independent per-number Beta-Bernoulli models. ' + NOT_CALIBRATED,
               False: ('Discounted (power-likelihood) Beta-Bernoulli updates, one per number: older draws are '
                       'down-weighted, so these are not the posterior of the plain model. ' + NOT_CALIBRATED)}
MEMORY = {
    'BETA_BERNOULLI_FULL_MEMORY_V1': (
        'all earlier draws of the current era, counted equally',
        'Every earlier draw counts equally, so it ranks the numbers in the same order as E_1\'s counts; only '
        'the order of numbers with exactly equal counts can differ, because the tie rule includes the '
        'method and variant.'),
    'BETA_BERNOULLI_DECAY_74_75_V1': (
        'earlier draws, each older draw counting 74/75 as much as the next (about a year\'s half-life)',
        'Older draws count for less: each draw back counts 74/75 as much as the one after it, so a draw '
        'about 52 draws (a year of weekly draws) old counts half as much as the newest. This down-weighting '
        'makes it a discounted update, not the plain Bayesian posterior.'),
    'BETA_BERNOULLI_DECAY_149_150_V1': (
        'earlier draws, each older draw counting 149/150 as much as the next (about two years\' half-life)',
        'Older draws count for less: each draw back counts 149/150 as much as the one after it, so a draw '
        'about 104 draws (two years of weekly draws) old counts half as much as the newest. This down-weighting '
        'makes it a discounted update, not the plain Bayesian posterior.'),
}


def channel(barrel_id, full):
    return {'ranking_kind': 'RANKING_WITH_SCORES', 'score_type': 'FLOAT64', 'order_ties': 'NOT_APPLICABLE',
            'top_rule_id': 'TOP_MARGINAL', 'worst_rule_id': 'INVERSE',
            'readout_selection_rule_version': 'TOP_MARGINAL_AND_INVERSE_V1',
            'ranking_tie_readout_version': 'TIE_SHA256_V1', 'probability_kind': PK[barrel_id],
            'probability_sum_tolerance': 1e-12, 'smoothing_note': SMOOTHING, 'calibration_note': CALIBRATION[full]}


def declaration(game, variant):
    p = get_profile(game)
    return validate_declaration({
        'schema': 'METHOD_DECLARATION_V1', 'game_id': game, 'profile_version': p.version, 'era_id': p.era_id,
        'method_id': 'E_6', 'variant_id': variant, 'method_revision': '1', 'observation_views': ['UNORDERED_SET'],
        'uses_dates': False, 'minimum_history_draws': 1, 'stochastic_fit': False, 'fit_seed_policy_id': None,
        'fit_sampling_model_version': FIT_VERSION[variant == FULL],
        'channels': {b.barrel_id: channel(b.barrel_id, variant == FULL) for b in p.barrels}, 'diagnostic_schema_id': None,
        'is_capability': 'IS_NOT_APPLICABLE', 'is_interface_version': None, 'source_method_dependencies': []})


def texts(game, variant):
    p = get_profile(game)
    main = next(b for b in p.barrels if b.barrel_id == 'MAIN')
    fair = f'{main.selected} in {main.high - main.low + 1} for a main number'
    if any(b.barrel_id == 'POWERBALL' for b in p.barrels):
        fair += ', 1 in 20 for the Powerball'
    span, memory = MEMORY[variant]
    one = f'Estimates each number\'s own chance of being drawn from {span}, starting from the fair-draw chance.'
    short = (f'E_6 treats each number on its own. For every earlier draw it notes whether the number was drawn, '
             f'and estimates the number\'s chance with the standard Beta-Bernoulli model: it starts from the '
             f'fair-draw chance ({fair}), worth one draw of evidence, and updates it with the history. {memory} '
             f'The estimated chances are the scores: its top pick is the highest-ranked numbers and its inverse '
             f'pick the lowest-ranked, with exact ties settled by the project tie rule (TIE_SHA256_V1). The '
             f'chances are also published as probabilities, labelled as uncalibrated model outputs, because the '
             f'model ignores that the main numbers are drawn together. It uses only which numbers were drawn, not '
             f'their order or the dates. If the draws are fair, it is not expected to beat chance.')
    return one, short


def entry(decl):
    one, short = texts(decl['game_id'], decl['variant_id'])
    return validate_registry_entry({
        'schema': 'REGISTRY_ENTRY_V1', 'game_id': decl['game_id'], 'method_id': 'E_6',
        'variant_id': decl['variant_id'], 'entry_sequence': 1, 'method_revision': '1',
        'declaration_digest': record_digest(decl), 'registry_status': 'FORMULA_OPEN',
        'registry_status_reason': ('Revision 1 installed for review and not yet released (E2R-R58): '
                                   'IN_DEVELOPMENT.txt is present and no SUPPORTED entry exists.'),
        'method_name': 'Per-Number Fitted Distribution Models', 'one_liner': one, 'short_explanation': short,
        'text_provenance': {'author': 'Claude (primary designer and coder)', 'date': DATE, 'text_version': 'v1',
                            'source_reference': f'{SPEC} section 2; R2 v0.5 section 7.1; E2R-1 v0.3r3 E2R-R21A'},
        'effective_date': DATE, 'previous_entry_digest': None})


root = tree / 'src' / 'methods' / '_common' / 'contract_data'
for game in ('POWERBALL', 'OZLOTTO'):
    for variant in VARIANTS:
        d = declaration(game, variant)
        e = entry(d)
        for path, rec in ((root / 'declarations' / game / 'E_6' / variant / 'r1.json', d),
                          (root / 'registry' / game / 'E_6' / variant / 'entry_0001.json', e)):
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open('xb') as fh:
                fh.write(canonical(rec))
            print(record_digest(rec), path.relative_to(tree).as_posix())
