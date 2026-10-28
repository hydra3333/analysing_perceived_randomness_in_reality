"""E_2-readiness contract (E2R-1 v0.3r3): closed vocabularies, identity formats and legal tables.

Stage-1 contract library (E2R-CODE-1). Shared code: it imports no method code, reads no file,
starts no process and is wired into no launcher. Every set here is closed; a value outside it is
a validation failure (E2R-R06). Section references are to E2R-1 v0.3r3.
"""
from __future__ import annotations

import re
from types import MappingProxyType

# Schema IDs (E2R-R13). Written schemas are V1; nothing else is writable in stage 1.
DECLARATION = 'METHOD_DECLARATION_V1'
REGISTRY_ENTRY = 'REGISTRY_ENTRY_V1'
RUN_REQUEST = 'RUN_REQUEST_V1'
FORECAST = 'METHOD_FORECAST_V1'
DIAGNOSTIC = 'METHOD_DIAGNOSTIC_V1'
FREEZE_RECEIPT = 'FORECAST_FREEZE_RECEIPT_V1'
DIAGNOSTIC_RECEIPT = 'DIAGNOSTIC_FREEZE_RECEIPT_V1'
TERMINAL = 'RUN_TERMINAL_RECORD_V1'
SCORE = 'POST_OUTCOME_SCORE_RECORD_V1'
WRITABLE_SCHEMAS = frozenset((DECLARATION, REGISTRY_ENTRY, RUN_REQUEST, FORECAST, DIAGNOSTIC,
                              FREEZE_RECEIPT, DIAGNOSTIC_RECEIPT, TERMINAL, SCORE))
# Frozen legacy schemas (E2R-R50, E2R-R49): readable for history, never writable again.
LEGACY_READ_ONLY_SCHEMAS = frozenset((
    'E1_SYNTHETIC_FORECAST_V0_1_NOT_FINAL', 'E1_HISTORICAL_DEVELOPMENT_FORECAST_V0_1_REVIEW',
    'E1_STANDALONE_MANIFEST_V0_1_REVIEW', 'MULTIGAME_E1_FORECAST_V1_REVIEW',
))

# Identity formats (E2R-R14).
METHOD_ID = re.compile(r'E_[1-9][0-9]*\Z', re.ASCII)
VARIANT_ID = re.compile(r'[A-Z0-9_]{3,96}\Z', re.ASCII)
REVISION = re.compile(r'[1-9][0-9]*\Z', re.ASCII)
SHA256 = re.compile(r'[0-9a-f]{64}\Z', re.ASCII)
RUN_ID = re.compile(r'mg-[a-z0-9][a-z0-9_-]{7,95}\Z', re.ASCII)  # Package 2 format (E2R-R52)
VERSION_TAG = re.compile(r'[A-Z0-9_]{3,64}\Z', re.ASCII)
NOT_YET_SPECIFIED = 'NOT_YET_SPECIFIED'  # variant of a FORMULA_OPEN entry with no specification

OBSERVATION_VIEWS = frozenset(('UNORDERED_SET', 'OPERATOR_DRAWN_ORDER', 'PAIRED_DIAGNOSTIC'))
RANKING_KINDS = frozenset(('RANKING_WITH_SCORES', 'RANKING_ORDER_ONLY', 'NONE'))
SCORE_TYPES = frozenset(('INTEGER', 'FLOAT64', 'NONE'))
ORDER_TIES = frozenset(('STRICT', 'GROUPED', 'NOT_APPLICABLE'))
TOP_RULES = frozenset(('TOP_MARGINAL', 'MAP_SET', 'TOP_UNAVAILABLE'))
WORST_RULES = frozenset(('INVERSE', 'INVERSE_FROM_MARGINALS', 'INVERSE_UNAVAILABLE'))
TIE_VERSIONS = frozenset(('TIE_SHA256_V1', 'NOT_APPLICABLE'))
TIE_DOMAIN = 'PREDICTIVE_RANDOMNESS/TIE_SHA256_V1'
IS_CAPABILITIES = frozenset(('IS_STATIC', 'IS_STATEFUL', 'IS_NOT_APPLICABLE'))
REGISTRY_STATUSES = frozenset(('SUPPORTED', 'FORMULA_OPEN', 'UNSUPPORTED_FOR_GAME'))

# Probability kinds per barrel (section 5.3). ABSENT is the Oz Lotto Powerball channel only.
PROBABILITY_KINDS = MappingProxyType({
    'MAIN': frozenset(('NONE', 'NORMALIZED_LABEL_PROBABILITY', 'MARGINAL_INCLUSION_PROBABILITY')),
    'POWERBALL': frozenset(('NONE', 'PB_CATEGORICAL')),
})
PROBABILITY_SUM = MappingProxyType({'NORMALIZED_LABEL_PROBABILITY': 1.0,
                                    'MARGINAL_INCLUSION_PROBABILITY': 7.0, 'PB_CATEGORICAL': 1.0})
DEFAULT_PROBABILITY_TOLERANCE = 1e-12   # E2R-R17
REVIEWER_TOLERANCE_LIMIT = 1e-9         # above this needs reviewer agreement (E2R-R17)

# Legal channel combinations (E2R-R15A): (ranking present?, top rule, worst rule).
LEGAL_CHANNELS = frozenset((
    (True, 'TOP_MARGINAL', 'INVERSE'),
    (True, 'MAP_SET', 'INVERSE_FROM_MARGINALS'),
    (False, 'MAP_SET', 'INVERSE_UNAVAILABLE'),
    (False, 'TOP_UNAVAILABLE', 'INVERSE_UNAVAILABLE'),
))

# Run modes, products, paths and tiers (section 9.1).
RUN_MODES = frozenset(('REAL_DEVELOPMENT', 'REAL_HOLDOUT', 'FINAL_NEXT_DRAW', 'IN_SAMPLE_DIAGNOSTIC',
                       'SYNTHETIC_CONTRACT_TEST', 'SYNTHETIC_NULL', 'SYNTHETIC_PLANTED',
                       'SYNTHETIC_IDENTIFIABILITY', 'BENCHMARK_REAL', 'BENCHMARK_SYNTHETIC'))
SYNTHETIC_MODES = frozenset(m for m in RUN_MODES if m.startswith('SYNTHETIC_'))
RESERVED_MODES = frozenset(('REAL_HOLDOUT', 'FINAL_NEXT_DRAW', 'IN_SAMPLE_DIAGNOSTIC'))  # E2R-R44, R44A
BENCHMARK_MODES = frozenset(('BENCHMARK_REAL', 'BENCHMARK_SYNTHETIC'))                  # E2R-R41A
PRODUCT_KINDS = frozenset(('WF_FORECAST', 'DIAGNOSTIC_OUTPUT', 'SYNTHETIC_TEST_OUTPUT',
                           'IS_DIAGNOSTIC_ENTRY', 'BENCHMARK_TIMING'))
EXECUTION_PATHS = frozenset(('STANDALONE', 'COORDINATED'))
EVIDENCE_TIERS = frozenset(('DEVELOPMENT_WF_EXPLORATORY', 'HOLDOUT_MODE_H', 'PROSPECTIVE',
                            'IS_DESCRIPTIVE', 'NOT_EVIDENCE'))
DERIVED_SCORING_STATES = frozenset(('NOT_YET_SCORED', 'SCORED', 'NEVER_SCORED'))  # report time only


def producible(run_mode: str, schema: str) -> tuple[str, str]:
    """The stage-1 producible table (E2R-R41): (run_mode, schema) -> (product_kind, evidence_tier).

    Every other combination, including every reserved row and every benchmark, is refused.
    """
    if run_mode in RESERVED_MODES:
        raise ValueError(f'run_mode {run_mode} is reserved and refused in stage 1')
    if run_mode in BENCHMARK_MODES:
        raise ValueError('benchmarks produce no method output record (E2R-R41A)')
    if schema == FORECAST:
        if run_mode == 'REAL_DEVELOPMENT':
            return 'WF_FORECAST', 'DEVELOPMENT_WF_EXPLORATORY'
        if run_mode in SYNTHETIC_MODES:
            return 'SYNTHETIC_TEST_OUTPUT', 'NOT_EVIDENCE'
    elif schema == DIAGNOSTIC:
        if run_mode == 'REAL_DEVELOPMENT' or run_mode in SYNTHETIC_MODES:
            return 'DIAGNOSTIC_OUTPUT', 'NOT_EVIDENCE'
    raise ValueError(f'illegal run_mode/schema combination: {run_mode}/{schema}')


RECORD_STATUSES = frozenset(('PREDICTION_AVAILABLE', 'INSUFFICIENT_HISTORY'))     # 7.4
RANKING_STATUSES = frozenset(('AVAILABLE', 'UNAVAILABLE', 'NOT_DECLARED'))
SCORE_DIRECTIONS = frozenset(('HIGHER_IS_BETTER',))
SELECTION_STATUS_AVAILABLE = 'PREDICTION_AVAILABLE'
TOP_UNAVAILABLE_STATUS = MappingProxyType({'MAIN': 'TOP_MAIN_UNAVAILABLE', 'POWERBALL': 'TOP_PB_UNAVAILABLE'})
WORST_UNAVAILABLE_STATUS = MappingProxyType({'MAIN': 'INVERSE_MAIN_UNAVAILABLE',
                                             'POWERBALL': 'INVERSE_PB_UNAVAILABLE'})
TERMINAL_OUTCOMES = frozenset(('SUCCESS', 'RUNTIME_FAILURE', 'NUMERIC_INVALID', 'VALIDATION_FAILURE',
                               'TIMEOUT', 'INSUFFICIENT_HISTORY', 'ORPHAN_SUSPECTED'))
TRACK_READOUTS = frozenset(('TOP', 'WORST'))
TRACK_MODES = frozenset(('WF', 'IS'))
INT64_MIN, INT64_MAX = -(2 ** 63), 2 ** 63 - 1
