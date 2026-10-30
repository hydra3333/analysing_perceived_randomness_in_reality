"""Write E_7's, E_8's, E_9's and E_10's revision 1 declarations and FORMULA_OPEN registry entries (Claude, 30 Oct 2026).

Made from the new-method template's generator (doc/METHOD_TEMPLATE/make_contract_data.py.txt) and the E_3/E_4
generator. Usage: python3 -I make_wave1_contract_data.py TREE
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
from E_007.variants import VARIANTS as V7  # noqa: E402
from E_008.variants import VARIANTS as V8  # noqa: E402
from E_009.variants import VARIANTS as V9  # noqa: E402
from E_010.variants import VARIANTS as V10  # noqa: E402

DATE = '2026-10-30'
SPEC = 'doc/Predictive_Randomness_Wave1_E7_E8_E9_E10_Design_v0_1r1.md'


def years(n):
    return {13: 'a quarter', 26: 'half a year', 52: 'a year', 91: 'the 91 draws before it', 104: 'two years',
            182: 'the 182 draws before it', 208: 'four years'}.get(n, f'{n} draws')


def words(method, variant, cfg):
    """(one-line description of the variant, sentences for the short explanation)."""
    if method == 'E_7':
        M, c, _m = cfg
        span = 'all earlier draws' if M is None else f'the last {M} draws (about {years(M)})'
        extra = (' Over the full history it picks exactly the same numbers as E_1, apart from the order of exact '
                 'ties; its point is its chances, which are pulled further towards fair than E_6\'s.'
                 if M is None else '')
        return (f'the count over {span}, pulled towards the fair rate by a prior worth {c} fair draws',
                f'It counts how often each number was drawn in {span}, then pulls that rate towards the fair-draw '
                f'rate as if {c} perfectly fair draws had been added, so a short lucky run counts for less.{extra}')
    if method == 'E_8':
        P, _m = cfg
        return (f'a blend of each number\'s latest-period rate and its long-run rate, with periods of {P} draws '
                f'(about {years(P)}), weighted by how much the periods differ beyond chance',
                f'It splits the recent history into periods of {P} draws and measures how much more the numbers\' '
                f'rates vary between periods than chance alone would make them. If they vary no more than chance '
                f'allows, it uses each number\'s long-run rate; if more, it leans towards the latest period, by '
                f'exactly that much.')
    if method == 'E_9':
        lam, _m = cfg
        hl = {(5, 6): 'about 4 draws (a month)', (18, 19): 'about 13 draws (a quarter)',
              (37, 38): 'about 26 draws (half a year)'}[(lam.numerator, lam.denominator)]
        return (f'its appearances, each older one counting for less, halving after {hl}',
                f'It adds up every past appearance of each number, with each draw counting {lam} as much as the one '
                f'after it, so an appearance loses half its weight after {hl}.')
    S, Lw, _m = cfg
    before = 'all earlier draws' if Lw is None else years(Lw - S)
    return (f'its rate in the last {S} draws minus its rate in {before}',
            f'It compares each number\'s rate in the last {S} draws (about {years(S)}) with its rate in '
            f'{before}, so its highest-ranked numbers are those rising fastest and its lowest-ranked those falling '
            f'fastest.')


METHODS = {
    'E_7': ('Bayesian Frequency Shrinkage', V7, 'BETA_SHRINKAGE_WINDOW_V1', True,
            'Beta prior centred on the fair-draw rate, worth 52 fair draws.',
            'Posterior means of independent per-number Beta-binomial models over the window. Not calibrated: the '
            'model ignores that the main numbers are drawn together, and no calibration has been tested.'),
    'E_8': ('Hierarchical Dirichlet-Multinomial Propensity', V8, 'HIER_BETA_BINOMIAL_PERIODS_MOM_V1', True,
            'Shrinkage of the latest period towards the long-run rate, by a weight estimated by the method of '
            'moments from the between-period excess variance pooled over all numbers.',
            'Marginal estimates only, not a joint law over sets of numbers drawn without replacement; moment '
            'estimates, not a full Bayesian fit. Not calibrated: no calibration has been tested.'),
    'E_9': ('Exponentially Decayed Occurrence Rates', V9, 'EXP_DECAYED_COUNT_V1', False, None, None),
    'E_10': ('Multi-Horizon Frequency Contrasts', V10, 'TWO_WINDOW_RATE_CONTRAST_V1', False, None, None),
}


def channel(barrel_id, probs, smoothing, calibration):
    kind = 'NONE' if not probs else ('MARGINAL_INCLUSION_PROBABILITY' if barrel_id == 'MAIN' else 'PB_CATEGORICAL')
    return {'ranking_kind': 'RANKING_WITH_SCORES', 'score_type': 'FLOAT64', 'order_ties': 'NOT_APPLICABLE',
            'top_rule_id': 'TOP_MARGINAL', 'worst_rule_id': 'INVERSE',
            'readout_selection_rule_version': 'TOP_MARGINAL_AND_INVERSE_V1',
            'ranking_tie_readout_version': 'TIE_SHA256_V1', 'probability_kind': kind,
            'probability_sum_tolerance': 1e-12 if probs else None,
            'smoothing_note': smoothing if probs else None, 'calibration_note': calibration if probs else None}


def declaration(game, method, variant, cfg):
    name, _v, fit, probs, smoothing, calibration = METHODS[method]
    p = get_profile(game)
    return validate_declaration({
        'schema': 'METHOD_DECLARATION_V1', 'game_id': game, 'profile_version': p.version, 'era_id': p.era_id,
        'method_id': method, 'variant_id': variant, 'method_revision': '1', 'observation_views': ['UNORDERED_SET'],
        'uses_dates': False, 'minimum_history_draws': cfg[-1], 'stochastic_fit': False, 'fit_seed_policy_id': None,
        'fit_sampling_model_version': fit,
        'channels': {b.barrel_id: channel(b.barrel_id, probs, smoothing, calibration) for b in p.barrels},
        'diagnostic_schema_id': None, 'is_capability': 'IS_NOT_APPLICABLE', 'is_interface_version': None,
        'source_method_dependencies': []})


def entry(decl, cfg):
    method = decl['method_id']
    name, _v, _fit, probs, _s, _c = METHODS[method]
    one, long = words(method, decl['variant_id'], cfg)
    meaning = ('Its values are model-based chances of each number being drawn, not tested for calibration.'
               if probs else 'Its scores are not chances, so no probabilities are published.')
    opening = ('looks at every number\'s history, with one weight shared by all the numbers' if method == 'E_8'
               else 'looks at each number on its own')
    short = (f'{method} {opening}. {long} It ranks the numbers by that value: its top pick '
             f'is the highest-ranked numbers and its inverse pick the lowest-ranked, with exact ties settled by '
             f'the project tie rule (TIE_SHA256_V1). {meaning} It uses only which numbers were drawn, not their '
             f'order or the dates, and needs {cfg[-1]} earlier draw{"s" if cfg[-1] != 1 else ""}. If the draws '
             f'are fair, it is not expected to beat chance.')
    return validate_registry_entry({
        'schema': 'REGISTRY_ENTRY_V1', 'game_id': decl['game_id'], 'method_id': method,
        'variant_id': decl['variant_id'], 'entry_sequence': 1, 'method_revision': '1',
        'declaration_digest': record_digest(decl), 'registry_status': 'FORMULA_OPEN',
        'registry_status_reason': ('Revision 1 installed for review and not yet released (E2R-R58): '
                                   'IN_DEVELOPMENT.txt is present and no SUPPORTED entry exists.'),
        'method_name': name, 'one_liner': f'Ranks every number by {one}.', 'short_explanation': short,
        'text_provenance': {'author': 'Claude (primary designer and coder)', 'date': DATE, 'text_version': 'v1',
                            'source_reference': f'{SPEC} sections 3-7; R2 v0.5 sections 7.1 and 7.7; E2R-1 v0.3r3 E2R-R21A'},
        'effective_date': DATE, 'previous_entry_digest': None})


root = tree / 'src' / 'methods' / '_common' / 'contract_data'
for method, (_n, variants, *_rest) in METHODS.items():
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
