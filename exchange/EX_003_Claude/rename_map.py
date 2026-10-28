"""NAMES-1 candidate rename map (design evidence). Module renames only; folders unchanged."""
MODULES = {  # old dotted module (relative to its package root) -> new
    '_common.e1_common_reader_bridge_v1': '_common.e1_common_reader_bridge',
    '_common.e1_historical_appearance_frequency_v0_3': '_common.e1_historical_appearance_frequency',
    '_common.e1_standalone_contract_v0_1': '_common.e1_standalone_contract',
    '_common.e1_training_view_v0_1': '_common.e1_training_view',
    '_common.game_draws_reader_v1': '_common.game_draws_reader',
    '_common.game_profiles_v1': '_common.game_profiles',
    '_common.multigame_ancestry_release_v1': '_common.multigame_ancestry_release',
    '_common.multigame_console_protocol_v1': '_common.multigame_console_protocol',
    '_common.multigame_coordinated_manifest_v1': '_common.multigame_coordinated_manifest',
    '_common.multigame_e1_v1': '_common.multigame_e1',
    '_common.multigame_method_registry_v1': '_common.multigame_method_registry',
    '_common.multigame_result_registry_v1': '_common.multigame_result_registry',
    '_common.multigame_standalone_contract_v1': '_common.multigame_standalone_contract',
    '_common.multigame_synthetic_scorer_v1': '_common.multigame_synthetic_scorer',
    '_common.multigame_worker_launch_handshake_v1': '_common.multigame_worker_launch_handshake',
    'coordinator_private.multigame_coordinator_exit_receipt_v2': 'coordinator_private.multigame_coordinator_exit_receipt',
    'coordinator_private.multigame_launch_spec_v1': 'coordinator_private.multigame_launch_spec',
    'coordinator_private.multigame_windows_lifecycle_v1': 'coordinator_private.multigame_windows_lifecycle',
}
TESTS = {  # standard offline suite and other current tests
    'test_multigame_console_and_synthetic_scorer_v0_4': 'test_multigame_console_and_synthetic_scorer',
    'test_multigame_exit_receipt_v0_8': 'test_multigame_exit_receipt',
    'test_multigame_launch_and_manifest_v0_8': 'test_multigame_launch_and_manifest',
    'test_multigame_science_allowlist_v0_8': 'test_multigame_science_allowlist',
    'test_multigame_v011_reader_contracts': 'test_multigame_reader_contracts',
    'test_multigame_v011_static_and_timing': 'test_multigame_static_and_timing',
    'test_multigame_windows_lifecycle_review_v0_9': 'test_multigame_windows_lifecycle_review',
    'test_p2_r1_t05_hardening_v1': 'test_t05_hardening',
    'test_p3_e1_standalone_v0_1': 'test_e1_standalone',
}
def files():
    out = {}
    for old, new in MODULES.items():
        pkg, o = old.split('.'); _, n = new.split('.')
        base = 'src/methods/_common/' if pkg == '_common' else 'src/coordinator_private/'
        out[base + o + '.py'] = base + n + '.py'
    for o, n in TESTS.items():
        out['tests/' + o + '.py'] = 'tests/' + n + '.py'
    return out
# Bare names that appear as identifiers or in strings: old basename -> new basename
def bare():
    m = {}
    for old, new in MODULES.items():
        m[old.split('.')[1]] = new.split('.')[1]
    m.update(TESTS)
    return m
