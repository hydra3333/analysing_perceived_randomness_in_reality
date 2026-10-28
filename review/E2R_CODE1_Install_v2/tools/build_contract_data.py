"""Generate CODE-1's installed contract data (Claude, 28 Oct 2026). Run once; the output is reviewed and frozen.

Usage: python3 -I build_contract_data.py TREE R2_NAMES_JSON EFFECTIVE_DATE
Writes TREE/src/methods/_common/contract_data/{declarations,registry}/... as canonical JSON, one file per
record, using the contract's own validators. E_1 has a declaration and a SUPPORTED entry in both games;
E_2..E_62 have a FORMULA_OPEN entry (variant NOT_YET_SPECIFIED) in both games. Texts for E_1 and E_2
are plain English (owner decision D-3); E_3..E_62 carry the exact R2 name and a "not yet specified" text.
"""
import json, sys
from pathlib import Path

tree, names_path, eff = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
sys.path.insert(0, str(tree / 'src' / 'methods'))
from _common.contract_records import canonical, record_digest, validate_declaration, validate_registry_entry
from _common.game_profiles import POWERBALL, OZLOTTO

names = json.load(open(names_path, encoding='utf-8'))
out = tree / 'src' / 'methods' / '_common' / 'contract_data'
assert not out.exists(), 'contract_data already exists'
PROV = {'author': 'Claude (primary designer and coder)', 'date': '2026-10-28', 'text_version': 'v1',
        'source_reference': 'R2 v0.5 section 7.1; E2R-1 v0.3r3 E2R-R21A (owner decision D-3)'}
E1_VARIANT = 'FULL_HISTORY_RAW_COUNTS_V1'
E1_CHANNEL = {'ranking_kind': 'RANKING_WITH_SCORES', 'score_type': 'INTEGER', 'order_ties': 'NOT_APPLICABLE',
              'top_rule_id': 'TOP_MARGINAL', 'worst_rule_id': 'INVERSE',
              'readout_selection_rule_version': 'TOP_MARGINAL_AND_INVERSE_V1',
              'ranking_tie_readout_version': 'TIE_SHA256_V1', 'probability_kind': 'NONE',
              'probability_sum_tolerance': None, 'smoothing_note': None, 'calibration_note': None}
TEXT = {
    'E_1': ('Ranks every number by how many times it was drawn in all earlier draws of the current era.',
            'E_1 counts how often each number appeared in every draw before the target draw, within the '
            'current era of the game, and ranks the numbers from most to least often drawn. Numbers with '
            'equal counts are put in a fixed order by the project tie rule (TIE_SHA256_V1). Its top pick is '
            'the highest-ranked numbers and its inverse pick the lowest-ranked. It uses only which numbers '
            'were drawn, not the order they came out in or the dates. It is a baseline: if the draws are '
            'fair, it is not expected to beat chance.'),
    'E_2': ('Will rank every number by how well its usual gap between appearances lines up with the target draw.',
            'E_2 will look, for each number, at the gaps between its past appearances, estimate its typical '
            'gap, and project whether its next appearance falls at the target draw: the projected interval '
            'at the target, not simply how long the number has been missing. Different ways of estimating '
            'the gap (mean, median, mode, hazard or a mixture) will be separate named variants, and numbers '
            'never yet seen need a stated rule. Its specification is not yet written, so it cannot run.'),
}
UNSPEC = ('Not yet specified.',
          'This method is registered under its R1/R2 name. Its specification has not been written yet, '
          'so it has no declaration and cannot run.')


def write(path, rec):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical(rec))


for p in (POWERBALL, OZLOTTO):
    g = p.game_id
    decl = {'schema': 'METHOD_DECLARATION_V1', 'game_id': g, 'profile_version': p.version, 'era_id': p.era_id,
            'method_id': 'E_1', 'variant_id': E1_VARIANT, 'method_revision': '1',
            'observation_views': ['UNORDERED_SET'], 'uses_dates': False, 'minimum_history_draws': 1,
            'stochastic_fit': False, 'fit_seed_policy_id': None,
            'fit_sampling_model_version': 'RAW_APPEARANCE_COUNTS_V1',
            'channels': {b.barrel_id: dict(E1_CHANNEL) for b in p.barrels}, 'diagnostic_schema_id': None,
            'is_capability': 'IS_NOT_APPLICABLE', 'is_interface_version': None, 'source_method_dependencies': []}
    validate_declaration(decl)
    write(out / 'declarations' / g / 'E_1' / E1_VARIANT / 'r1.json', decl)
    for i in range(1, 63):
        mid = f'E_{i}'
        one, short = TEXT.get(mid, UNSPEC)
        if mid == 'E_1':
            variant, rev, dig, status = E1_VARIANT, '1', record_digest(decl), 'SUPPORTED'
            reason = ('Accepted implementation (Package 2 v0.11-r1, NAMES-1, E1-ALIGN); stage-1 contract '
                      'declaration installed with E2R-CODE-1.')
        else:
            variant, rev, dig, status = 'NOT_YET_SPECIFIED', None, None, 'FORMULA_OPEN'
            reason = 'Method specification not yet written and ratified (R2 section 7.1).'
        entry = {'schema': 'REGISTRY_ENTRY_V1', 'game_id': g, 'method_id': mid, 'variant_id': variant,
                 'entry_sequence': 1, 'method_revision': rev, 'declaration_digest': dig,
                 'registry_status': status, 'registry_status_reason': reason, 'method_name': names[mid],
                 'one_liner': one, 'short_explanation': short, 'text_provenance': dict(PROV),
                 'effective_date': eff, 'previous_entry_digest': None}
        validate_registry_entry(entry)
        write(out / 'registry' / g / mid / variant / 'entry_0001.json', entry)
print(sum(1 for _ in out.rglob('*.json')), 'files written under', out)
