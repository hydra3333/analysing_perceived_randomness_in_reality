"""The light tidy-up of the existing method files: the words that are added (headers and comments only).

What this file is for
    It holds, as plain data, every header and every comment that the tidy-up adds to the existing method files,
    so that the reviewer and the owner can read all of the new wording in one place. make_tidy_up.py (beside this
    file) puts these texts into the files and proves that nothing but comments changed. No calculation is here.

Which part of the specification it carries out
    The owner's note of ratification RAT-40, item 3 (decision log entry 147), and doc/CODING_PRACTICES_v0_1.md
    sections 1 to 3 and 6: each existing method file gets its header and dependency list, and comments where
    they are plainly missing; no calculation changes.

Which of the project's own modules it uses
    None.

What uses it
    exchange/CLAUDE_WEB_TOOLS/tidy1/make_tidy_up.py.
"""

# The specification of the layout, named in every header.
LAYOUT_SPEC = 'doc/Predictive_Randomness_System_Specification_v0_6.md section 3.2'

# The design document of each group of families.
WAVE1 = 'doc/Predictive_Randomness_Wave1_E7_E8_E9_E10_Design_v0_1r1.md'
WAVE2 = 'doc/Predictive_Randomness_Wave2_E2_E17_E18_E19_Design_v0_1r2.md'
POLY = 'doc/Predictive_Randomness_E3_E4_Polynomial_Fit_Design_v0_1.md'
E6_DESIGN = 'doc/Predictive_Randomness_E6_Specification_and_Method_Template_Design_v0_1.md'

# What each shared helper gives a family core that uses it (one line for the header's list of modules).
HELPER_USE = {
    'recurrence_gaps_v1': 'each number\'s appearances, gaps and age at the target; exposures by age; age bins',
    'occurrence_counts_v1': 'how often each number was drawn in a window, in periods, or with decaying weights',
    'polynomial_fits_v1': 'exact polynomial fits to a short series (least squares, interpolation, minimax)',
}

# One entry per family that has a core_v1.py and a variants.py (E_6 and E_1 are set out separately below).
#   title        the family's name
#   design       its design document and section
#   helper       the shared helper it uses
#   outputs      the output types it takes from the forecast module
#   settings     what one line of its VARIANTS table holds, in order
#   example      one line of that table, as _config() returns it
#   score        what one score is, in a few words
#   score_example an invented {number: score} example (no real draw is used)
#   chances      True if the scores are also published as chances (they then sum to the number drawn)
#   poly_pick    (E_3 and E_4 only) which coefficient of the example polynomial the family scores by
# Every example value in this file is invented to show a shape; none is taken from a real draw.
FAMILIES = {
    'E_002': dict(method='E_2', title='Expected Recurrence-Interval Alignment', design=WAVE2 + ' section 4.1',
                  helper='recurrence_gaps_v1', outputs='MethodOutput, BarrelOutput, ScoredRanking',
                  settings='the statistic ("mean" or "median"), the last n gaps used (None for all), the minimum history',
                  example="('mean', None, 104)",
                  score='minus the distance between the number\'s age at the target and its usual gap, as a share of that gap',
                  score_example='{1: Fraction(-2, 5), 2: Fraction(-1, 10), ...}', chances=False),
    'E_003': dict(method='E_3', title='Occurrence-Curve Endpoint Forecast', design=POLY + ' sections 2 to 4',
                  helper='polynomial_fits_v1', outputs='MethodOutput, BarrelOutput, ScoredRanking',
                  settings='the kind of fit ("LS", "INTERP" or "MINIMAX"), the window M, the degree D, the smoothing '
                           'half-width H, the interpolation positions',
                  example="('LS', 52, 2, None, None)", poly_pick='Fraction(9, 44)',
                  score='the fitted curve\'s value at the target',
                  score_example='{1: Fraction(9, 44), 2: Fraction(7, 55), ...}', chances=False),
    'E_004': dict(method='E_4', title='Occurrence-Curve Gradient Forecast', design=POLY + ' sections 2 to 4',
                  helper='polynomial_fits_v1', outputs='MethodOutput, BarrelOutput, ScoredRanking',
                  settings='the kind of fit ("LS", "INTERP" or "MINIMAX"), the window M, the degree D, the smoothing '
                           'half-width H, the interpolation positions',
                  example="('LS', 52, 2, None, None)", poly_pick='Fraction(1, 300)',
                  score='the fitted curve\'s slope at the target, per draw',
                  score_example='{1: Fraction(1, 300), 2: Fraction(-1, 450), ...}', chances=False),
    'E_007': dict(method='E_7', title='Bayesian Frequency Shrinkage', design=WAVE1 + ' section 3.1',
                  helper='occurrence_counts_v1', outputs='MethodOutput, BarrelOutput, ScoredRanking, ProbabilityVector',
                  settings='the window M (None for all earlier draws), the prior strength c, the minimum history',
                  example='(52, Fraction(52), 52)',
                  score='the number\'s rate in the window, pulled towards the fair rate',
                  score_example='{1: Fraction(21, 104), 2: Fraction(19, 104), ...}', chances=True),
    'E_008': dict(method='E_8', title='Hierarchical Dirichlet-Multinomial Propensity', design=WAVE1 + ' section 3.4',
                  helper='occurrence_counts_v1', outputs='MethodOutput, BarrelOutput, ScoredRanking, ProbabilityVector',
                  settings='the period length P, the minimum history (2P)',
                  example='(13, 26)',
                  score='a weighted mix of the number\'s rate in the latest period and its rate over all periods',
                  score_example='{1: Fraction(11, 52), 2: Fraction(5, 26), ...}', chances=True),
    'E_009': dict(method='E_9', title='Exponentially Decayed Occurrence Rates', design=WAVE1 + ' section 3.2',
                  helper='occurrence_counts_v1', outputs='MethodOutput, BarrelOutput, ScoredRanking',
                  settings='the decay factor lambda, the minimum history',
                  example='(Fraction(5, 6), 1)',
                  score='the number\'s count, each appearance weighted by lambda to the power of its age',
                  score_example='{1: Fraction(91, 36), 2: Fraction(5, 6), ...}', chances=False),
    'E_010': dict(method='E_10', title='Multi-Horizon Frequency Contrasts', design=WAVE1 + ' section 3.3',
                  helper='occurrence_counts_v1', outputs='MethodOutput, BarrelOutput, ScoredRanking',
                  settings='the short window S, the long window Lw (None for all earlier draws), the minimum history',
                  example='(13, 104, 104)',
                  score='the number\'s rate in the newest S draws minus its rate in the rest of the long window',
                  score_example='{1: Fraction(3, 91), 2: Fraction(-2, 91), ...}', chances=False),
    'E_017': dict(method='E_17', title='Discrete Recurrence Hazard Curves', design=WAVE2 + ' section 4.2',
                  helper='recurrence_gaps_v1', outputs='MethodOutput, BarrelOutput, ScoredRanking',
                  settings='the form ("bins" or "logage"), the prior strength c (None for "logage"), the window in '
                           'draws (None for all), the minimum history',
                  example="('bins', Fraction(100), None, 52)",
                  score='the hazard at the number\'s age ("bins"), or its age times a certified sign ("logage")',
                  score_example='{1: Fraction(41, 200), 2: Fraction(19, 100), ...}', chances=False),
    'E_018': dict(method='E_18', title='Mixtures of Recurrence Modes', design=WAVE2 + ' section 4.4',
                  helper='recurrence_gaps_v1', outputs='MethodOutput, BarrelOutput, ScoredRanking',
                  settings='the window in draws for the completed gaps (None for all), the prior pseudo-gaps c, the '
                           'minimum history',
                  example='(None, Fraction(10), 104)',
                  score='the hazard, at the number\'s age, of its fitted mixture of four gap laws',
                  score_example='{1: Fraction(13, 64), 2: Fraction(3, 16), ...}', chances=False),
    'E_019': dict(method='E_19', title='Periodic Recurrence-Hazard Peaks', design=WAVE2 + ' section 4.3',
                  helper='recurrence_gaps_v1', outputs='MethodOutput, BarrelOutput, ScoredRanking',
                  settings='the cycle T, the trend prior c, the shrinkage d, the minimum history',
                  example='(2, Fraction(100), Fraction(20), 104)',
                  score='the trend hazard at the number\'s age times its own factor for that age\'s place in the cycle',
                  score_example='{1: Fraction(21, 100), 2: Fraction(9, 50), ...}', chances=False),
}

# ---------------------------------------------------------------- headers built from the table above

CORE_HEADER = '''{method} ({title}): the family's shared calculation, used by every {method} variant.

What this file is for
    It holds the whole calculation of {method}. compute() turns the draws before a target into one score for
    every number of every barrel; verify() works the same scores out again by a second, differently written
    route and refuses the record if they differ. Each variant's own method.py passes its task here, and the
    variant's fixed settings are looked up, by the task's variant ID, in {family}/variants.py.

Which part of the specification it carries out
    The method: {design}.
    Its place in the layout: {layout} (a family's shared core file).

Which of the project's own modules it uses
{modules}

What uses it
    {family}/<VARIANT>/method.py of every {method} variant, and this family's tests.

How it computes (the header this file had before the tidy-up, kept)
{old_body}
'''

VARIANTS_HEADER = '''{method} ({title}): the fixed settings of each {method} variant.

What this file is for
    One table, VARIANTS, with one line for each variant: {settings}.
    Nothing is computed here. The settings never change: a different setting is a new variant with a new name.

Which part of the specification it carries out
    The method: {design_doc} (its section on the variants).
    Its place in the layout: {layout}.

Which of the project's own modules it uses
    None.

What uses it
    {family}/core_v1.py, which picks a variant's line by the task's variant ID; and this family's tests.

The header this file had before the tidy-up, kept
{old_doc}
'''

INIT_HEADER = '''{method} - {title}: the family's folder.

What this file is for
    It makes this folder a Python package, so that the family's files can be imported as {family}.core_v1 and
    {family}.{settings_module}. It holds no code. Each variant has its own folder here (method.py and
    VARIANT.json); the calculation they share is core_v1.py{helper_sentence}

Which part of the specification it carries out
    {layout}. The method itself: {design_doc}.

Which of the project's own modules it uses
    None.

What uses it
    Python, whenever a file of this family is imported.
'''

# ---------------------------------------------------------------- headers written out in full

FULL_HEADERS = {
    'E_006/core_v1.py': '''E_6 (Per-Number Fitted Distribution Models): the family's shared calculation, used by every E_6 variant.

What this file is for
    It connects the mathematics of E_6 (beta_bernoulli.py, beside this file) to the research code. compute()
    turns the draws before a target into one estimate for every number of every barrel; verify() works the
    same estimates out again by a different exact algorithm and refuses the record if they differ. Each
    variant's own method.py passes its task here, and the variant's forgetting factor is looked up, by the
    task's variant ID, in the VARIANTS table of beta_bernoulli.py.

Which part of the specification it carries out
    The method: {e6} section 2.
    Its place in the layout: {layout} (a family's shared core file).

Which of the project's own modules it uses
    E_006.beta_bernoulli         VARIANTS, and the two exact algorithms posterior_means and posterior_means_by_recursion
    _common.contract_forecast    the types a method returns (MethodOutput, BarrelOutput, ScoredRanking, ProbabilityVector)
    _common.game_profiles        get_profile: each game's barrels (lowest and highest number, how many are drawn)

What uses it
    E_006/<VARIANT>/method.py of every E_6 variant, and this family's tests.

How it computes (the header this file had before the tidy-up, kept)
{old_body}
''',
    'E_006/beta_bernoulli.py': '''E_6 (Per-Number Fitted Distribution Models): the mathematics, and the fixed settings of each variant.

What this file is for
    It holds the two exact algorithms that estimate, for one barrel, how likely each number is to be drawn
    next (posterior_means and, written differently for checking, posterior_means_by_recursion), and the table
    VARIANTS that gives each variant its forgetting factor. Exact fractions only; the caller rounds once.

Which part of the specification it carries out
    The method: {e6} section 2 (the variants: section 2.5).
    Its place in the layout: {layout} (a family's own module beside its core file).

Which of the project's own modules it uses
    None.

What uses it
    E_006/core_v1.py, and this family's tests.

The mathematics (the header this file had before the tidy-up, kept)
{old_body}
''',
    'E_006/__init__.py': '''E_6 - Per-Number Fitted Distribution Models: the family's folder.

What this file is for
    It makes this folder a Python package, so that the family's files can be imported as E_006.core_v1 and
    E_006.beta_bernoulli. It holds no code. Each variant has its own folder here (method.py and VARIANT.json);
    the calculation they share is core_v1.py, and the mathematics and the variants' settings are in
    beta_bernoulli.py. Nothing in this folder reads a file, starts a process or touches orchestration.

Which part of the specification it carries out
    {layout}. The method itself: {e6} section 2.

Which of the project's own modules it uses
    None.

What uses it
    Python, whenever a file of this family is imported.
''',
    'E_001/FULL_HISTORY_RAW_COUNTS_V1/method.py': '''E_1 variant FULL_HISTORY_RAW_COUNTS_V1: the variant's own entry file.

What this file is for
    It is the one file the research code calls for E_1's only variant. It calls E_1's own counting function
    (E_001/multigame_e1.py, forecast) unchanged and turns its counts into the output every method returns.
    verify() then works E_1's own result out again and requires the assembled record to equal it number for
    number (scores, ranking, TOP and WORST), so a published record can never differ from what E_1 itself
    computes. Until build step 1 this file was the wrapper src/methods/contract_adapters/e_001.py.

Which part of the specification it carries out
    The wrapper: doc/Predictive_Randomness_E2R_CODE2_Design_v0_1r1.md section 5.
    Its place in the layout: {layout}, and section 17.3's table of what moves where.

Which of the project's own modules it uses
    E_001.multigame_e1           forecast: E_1's own count of how often each number was drawn, with its ranking
    _common.contract_forecast    the types a method returns (MethodOutput, BarrelOutput, ScoredRanking)
    _common.contract_task        permitted_view_digest and view_data_kind: the identity of the earlier-draws view
    _common.game_profiles        get_profile: each game's barrels

What uses it
    src/methods/_common/method_table.py imports it when it builds the runner's table of methods; and E_1's tests.

The header this file had while it was that wrapper, outside E_1's folder; kept
{old_doc}
''',
    '_shared/occurrence_counts_v1.py': '''Shared helper, version 1: exact occurrence counts.

What this file is for
    It counts, for one barrel, how often each number was drawn: in the newest draws, in consecutive periods,
    or with weights that shrink with age. Every count has a second, differently written form that the methods
    use to check themselves. Exact whole numbers and fractions only, so every result is the same on every PC.

Which part of the specification it carries out
    The wave 1 design, {wave1}: section 3 (the rules
    these counts serve) and section 11 (the package, which lists what this helper holds).
    Its place in the layout: {layout} (a helper used by more than one family, versioned by its name).

Which of the project's own modules it uses
    None. It also reads nothing and starts nothing.

What uses it
    E_007/core_v1.py, E_008/core_v1.py, E_009/core_v1.py and E_010/core_v1.py; and tests/test_occurrence_counts.py.

The functions (the header this file had before the tidy-up, kept)
{old_body}
''',
    '_shared/polynomial_fits_v1.py': '''Shared helper, version 1: exact polynomial fits to a short series.

What this file is for
    It fits a polynomial to a short series of values in three ways (least squares, interpolation, minimax),
    each with a second, differently written form that the methods use to check themselves. Exact fractions
    only: no library solver, so every result is the same on every PC.

Which part of the specification it carries out
    The E_3 and E_4 design: {poly}, section 3.
    Its place in the layout: {layout} (a helper used by more than one family, versioned by its name).

Which of the project's own modules it uses
    None. It also reads nothing and starts nothing.

What uses it
    E_003/core_v1.py and E_004/core_v1.py; and tests/test_polynomial_fits.py.

The fits (the header this file had before the tidy-up, kept)
{old_body}
''',
    '_shared/recurrence_gaps_v1.py': '''Shared helper, version 1: gaps between a number's appearances, exposures by age, age bins and a certified sign.

What this file is for
    For one barrel it finds where each number appeared, the gaps between its appearances, its age at the
    target, how long numbers were "at risk" at each age and how often they then came up, the age bins, and the
    proved sign of a sum of logarithms. Each has a second, differently written route that the methods use to
    check themselves. Exact arithmetic only.

Which part of the specification it carries out
    The wave 2 design: {wave2}, sections 3, 4.2 and 10.
    Its place in the layout: {layout} (a helper used by more than one family, versioned by its name).

Which of the project's own modules it uses
    None. It also reads nothing and starts nothing.

What uses it
    E_002/core_v1.py, E_017/core_v1.py, E_018/core_v1.py and E_019/core_v1.py; and tests/test_recurrence_gaps.py.

What it holds (the header this file had before the tidy-up, kept)
{old_body}
''',
}

# ---------------------------------------------------------------- comments on the constants of a core file

CONSTANT_NOTES = {
    'METHOD_ID': 'the method\'s ID as the records name it',
    'OBSERVATION_VIEW': 'the view of the earlier draws this family accepts: numbers as a set, no dates',
    'PUBLISHES_PROBABILITIES': 'whether the scores are also published as chances (only where they sum to the number drawn)',
    'PROVENANCE': 'the text stored with the published values, saying how they were computed',
}

# Comments put above other constants that had none: {file: {constant: the comment's lines}}.
POLY_VARIANTS_NOTE = ['# variant_id: (fit; window M; degree D; smoothing half-width H, or None; interpolation positions, or None)']
CONSTANT_COMMENTS = {
    'E_003/variants.py': {'VARIANTS': POLY_VARIANTS_NOTE},
    'E_004/variants.py': {'VARIANTS': POLY_VARIANTS_NOTE},
    '_shared/polynomial_fits_v1.py': {
        'MINIMAX_EXCHANGE_CAP': ['# The most exchange steps a minimax fit may take. A fit that has not finished by then is refused',
                                 '# (RuntimeError) rather than left to run on.'],
    },
    '_shared/recurrence_gaps_v1.py': {
        'BIN_FACTORS': ['# The six fixed factors f of the age bins: a bin\'s upper edge is ceil(f * L / K) for a barrel of L numbers',
                        '# with K drawn (design section 3.4).'],
        'FIRST_TERMS': ['# How many series terms the first try at a certified sign uses; the number doubles at each further try.'],
        'MAX_TERMS': ['# The most series terms tried. With no certified sign by then, the function refuses (ValueError).'],
    },
}

# ---------------------------------------------------------------- comments for functions that had none

DOC_CONFIG = '''Check that the task is for this family and return the variant's fixed settings.

task: the frozen MethodTask the research code built (method, variant, observation view).
Returns the variant's line of VARIANTS, for example {example}, which holds, in order:
    {settings}.
Refuses (ValueError) a task for another method, an unknown variant, or any view but the unordered one without dates.
'''

DOC_SCORES = '''The exact score of every number of one barrel.

A number's score is {score}.
draws: the numbers drawn in this barrel at each earlier draw, oldest first.
b: the barrel (its lowest and highest number, and how many are drawn).
cfg: the variant's settings, as _config() returns them.
second: False for the first route; True for the second, differently written route that verify() uses.
Returns {{number: exact score}}, for example {score_example}.
'''

DOC_COMPUTE = '''Compute the scores for one target draw, from the draws before it only.

task: the frozen MethodTask.  view: the permitted view (the draws before the target, and nothing else).
Returns a MethodOutput holding, for each barrel, every number's exact score rounded once to a float64{chances}, for example
    MethodOutput(barrels={{'MAIN': BarrelOutput(ranking=ScoredRanking({{1: 0.2019, 2: 0.1827, ...}}))}}).
With fewer earlier draws than the variant's minimum it returns MethodOutput(barrels={{}}), which is recorded as
INSUFFICIENT_HISTORY.
'''

# The two polynomial-fit families (E_3 and E_4) score by one coefficient of the fitted curve.
DOC_SCORE_POLY = '''The one coefficient of a fitted polynomial that this family scores by.

coeffs: the polynomial's coefficients [a_0, a_1, ...], for example [Fraction(9, 44), Fraction(1, 300)].
Returns coeffs[SCORE_COEFFICIENT], for example {poly_pick} for those coefficients; 0 if the polynomial is
too short to have that coefficient.
'''

DOC_COMPUTE_POLY = '''Compute the scores for one target draw, from the draws before it only.

task: the frozen MethodTask.  view: the permitted view (the draws before the target, and nothing else).
Returns a MethodOutput holding, for each barrel, every number's exact score rounded once to a float64, for example
    MethodOutput(barrels={{'MAIN': BarrelOutput(ranking=ScoredRanking({{1: 0.2045, 2: 0.1273, ...}}))}}).
With fewer earlier draws than the variant's window it returns MethodOutput(barrels={{}}), which is recorded as
INSUFFICIENT_HISTORY.
'''

# Written out in full: {file: {function name (Class.method for a method; outer.inner for a nested one): text}}.
FUNCTION_DOCS = {
    'E_002/core_v1.py': {
        '_median_by_sorting': '''The median of a list of gap lengths, by sorting them.

g: the gaps, for example [3, 9, 4].
Returns the middle value as a Fraction, for example Fraction(4); for an even count, the mean of the two middle
values, for example Fraction(7, 2) for [3, 4].
''',
    },
    'E_006/core_v1.py': {
        '_lam': '''Check that the task is for this family and return the variant's forgetting factor.

task: the frozen MethodTask the research code built (method, variant, observation view).
Returns the variant's entry of VARIANTS, for example Fraction(74, 75) (1 means every earlier draw counts equally).
Refuses (ValueError) a task for another method, an unknown variant, or any view but the unordered one without dates.
''',
        '_exact': '''The exact estimate of every number of every barrel, by one of the two algorithms.

task: the frozen MethodTask.  view: the permitted view (the draws before the target).
method: posterior_means (the first route) or posterior_means_by_recursion (the second, for verify()).
Returns {barrel: {number: exact estimate}}, for example {'MAIN': {1: Fraction(41, 200), 2: Fraction(39, 200), ...}}.
''',
        'compute': '''Compute the estimates for one target draw, from the draws before it only.

task: the frozen MethodTask.  view: the permitted view (the draws before the target, and nothing else).
Returns a MethodOutput holding, for each barrel, every number's exact estimate rounded once to a float64, both as
its score and as its published chance (the estimates of a barrel sum to the number drawn), for example
    MethodOutput(barrels={'MAIN': BarrelOutput(ranking=ScoredRanking({1: 0.205, 2: 0.195, ...}),
                                               probability=ProbabilityVector([0.205, 0.195, ...], PROVENANCE))}).
Unlike the other families it never returns an empty output: every number of every barrel always gets an estimate.
''',
    },
    'E_006/beta_bernoulli.py': {
        '_check': '''Refuse arguments that do not describe a barrel and its draws.

draws: the numbers drawn at each earlier draw, oldest first.  low, high: the barrel's lowest and highest number.
selected: how many numbers are drawn each time.  lam: the forgetting factor.
Returns nothing. Refuses (ValueError) a forgetting factor that is not an exact fraction above 0 and at most 1, a
barrel that is not whole numbers with fewer drawn than it holds, or a draw that is not `selected` different
numbers of the barrel (the message names the draw).
''',
    },
    'E_018/core_v1.py': {
        '_surv_geom': '''The chance that a gap is G draws or longer, when every draw ends the gap with chance p.

p: the chance per draw, an exact fraction, for example Fraction(1, 5).  G: the gap length, 1 or more.
Returns (1 - p) to the power G - 1, for example Fraction(16, 25) for p = 1/5 and G = 3.
''',
        '_surv_nb2': '''The chance that a gap is G draws or longer, when the gap ends at the second "success" of chance p.

p: the chance per draw, an exact fraction.  G: the gap length, 1 or more.
Returns the chance of fewer than two successes in G - 1 draws, for example Fraction(112, 125) for p = 1/5 and
G = 4; 1 for G = 1.
''',
        '_solve': '''Solve the square system of equations A x = rhs exactly (Gauss-Jordan elimination on fractions).

A: the matrix, a list of rows of Fractions.  rhs: the right-hand side, one Fraction for each row.
Returns the solution, for example [Fraction(1, 2), Fraction(3, 4)]; None if the system has no single solution.
''',
        '_objective': '''How far a mixture of the gap laws is from the observed gap shares (a chi-square distance).

q: the observed share of gaps in each bin.  P: for each gap law, its share in each bin.  Pf: the fair law's
shares, used as the weights of the distance.  w: the mixture's weight on each gap law.
Returns the sum over the bins of (q - the mixture's share) squared, divided by Pf, for example Fraction(3, 400).
''',
    },
    'E_001/FULL_HISTORY_RAW_COUNTS_V1/method.py': {
        '_e1_result': '''Run E_1's own counting function on the earlier draws.

task: the frozen MethodTask.  view: the permitted view (the draws before the target, and nothing else).
Returns E_1's own result, a dict with one entry for each barrel under 'barrels', each with 'scores' (how often
each number was drawn), 'ranking', 'top' and 'worst'; for example
    {'barrels': {'MAIN': {'scores': {'1': 61, '2': 58, ...}, 'ranking': [...], 'top': [...], 'worst': [...]}}}.
Refuses (ValueError) a task that is not for E_1.
''',
        'compute': '''Compute E_1's counts for one target draw, from the draws before it only.

task: the frozen MethodTask.  view: the permitted view (the draws before the target, and nothing else).
Returns a MethodOutput holding, for each barrel, how often each number was drawn, for example
    MethodOutput({'MAIN': BarrelOutput(ScoredRanking({1: 61, 2: 58, ...}))}).
''',
    },
    '_shared/occurrence_counts_v1.py': {
        '_check': '''Refuse arguments that do not describe a barrel and its draws.

draws: the numbers drawn at each earlier draw, oldest first.  low, high: the barrel's lowest and highest number.
Returns nothing. Refuses (ValueError) a range that is not positive whole numbers, or a draw holding a repeated
number or one outside the range.
''',
        '_span': '''Refuse a window that is not a whole number from 1 to the number of draws.

S: the window, in draws.  n: how many draws there are.  Returns nothing; refuses (ValueError) otherwise.
''',
        'window_counts': '''How often each number was drawn in the newest S draws.

draws: the numbers drawn at each earlier draw, oldest first.  low, high: the barrel's range.  S: the window.
Returns {number: count}, every number of the barrel included, for example {1: 9, 2: 12, ..., 35: 10}.
''',
        'window_counts_by_prefix': '''The same counts as window_counts, from running totals (the second route, for checking).

draws, low, high, S: as for window_counts.
Returns {number: count}, for example {1: 9, 2: 12, ..., 35: 10}.
''',
        '_lam': '''Refuse a decay factor that is not an exact fraction strictly between 0 and 1.

lam: the decay factor, for example Fraction(5, 6).  Returns nothing; refuses (ValueError) otherwise.
''',
        'decayed_counts': '''Each number's count with every appearance weighted by lam to the power of its age.

draws: the numbers drawn at each earlier draw, oldest first (the newest has age 0 and weight 1).
low, high: the barrel's range.  lam: the decay factor.
Returns {number: exact weighted count}, for example {1: Fraction(91, 36), 2: Fraction(5, 6), ...}.
''',
        'decayed_counts_by_recursion': '''The same weighted counts as decayed_counts, by stepping through the draws (the second route).

draws, low, high, lam: as for decayed_counts. At each draw every count is multiplied by lam, and 1 is added
for a number that was drawn.
Returns {number: exact weighted count}, for example {1: Fraction(91, 36), 2: Fraction(5, 6), ...}.
''',
        '_period': '''Check the period length and return how many whole periods the history holds.

P: the period, in draws.  n_draws: how many draws there are.
Returns the number of whole periods, for example 4 for P = 13 and 60 draws.
Refuses (ValueError) a period that is not a positive whole number, or one longer than the history.
''',
        'period_counts': '''How often each number was drawn in each period of P draws, counted back from the newest draw.

draws: the numbers drawn at each earlier draw, oldest first.  low, high: the barrel's range.  P: the period.
Returns {number: [count in each period, oldest period first]}, for example {1: [2, 4, 3, 1], 2: [3, 3, 2, 2], ...}.
Draws older than the oldest whole period are not used.
''',
        'period_counts_by_index': '''The same counts as period_counts, by giving each draw its period number (the second route).

draws, low, high, P: as for period_counts.
Returns {number: [count in each period, oldest period first]}, for example {1: [2, 4, 3, 1], ...}.
''',
    },
    '_shared/polynomial_fits_v1.py': {
        '_check': '''Refuse arguments that do not describe points to fit a polynomial to.

ts: the positions.  ys: the values, one for each position.  degree: the polynomial's degree.
need: the fewest points the fit needs.
Returns nothing. Refuses (ValueError) a degree that is not a whole number of 0 or more, too few points, a
different number of values and positions, positions that are not different exact fractions, or values that
are not exact.
''',
        'evaluate': '''The value of a polynomial at one position (Horner's rule).

coeffs: the coefficients [a_0, a_1, ...].  t: the position.
Returns the exact value, for example Fraction(7, 4) for coeffs [1, 3] at t = Fraction(1, 4).
''',
        'least_squares': '''The least-squares polynomial of a given degree through the points.

ts: the positions.  ys: the values.  degree: the polynomial's degree.
Returns its coefficients [a_0, ..., a_degree] as exact fractions, for example [Fraction(9, 44), Fraction(1, 300)].
''',
        'LeastSquares.__init__': '''Prepare the fit for these positions and this degree (done once, then reused for every series).

ts: the positions.  degree: the polynomial's degree.
Refuses (ValueError) what _check refuses.
''',
        'LeastSquares.fit': '''The least-squares coefficients for one series of values at the prepared positions.

ys: the values, one for each position.
Returns [a_0, ..., a_degree] as exact fractions, for example [Fraction(9, 44), Fraction(1, 300)].
''',
        'least_squares_by_recurrence.at': 'The value of the polynomial `poly` at position t.',
        'least_squares_by_recurrence.mul_t_minus': 'The coefficients of (t - a) times the polynomial `poly`.',
        'least_squares_by_recurrence.axpy': 'The coefficients of x + a * y, the shorter polynomial padded with zeros.',
        'minimax.sigma': 'Returns +1 or -1; the signs alternate from one reference position to the next.',
    },
    '_shared/recurrence_gaps_v1.py': {
        '_checked': '''Refuse arguments that do not describe a barrel and its draws; otherwise hand the draws back.

draws: the numbers drawn at each earlier draw, oldest first.  low, high: the barrel's lowest and highest number.
Returns `draws` unchanged. Refuses (ValueError) a range that is not positive whole numbers, or a draw holding
a repeated number or one outside the range.
''',
        'completed_gaps': '''The gaps between each number's successive appearances.

app: {number: the positions at which it appeared}, as appearances() returns it, for example {4: [2, 7, 12]}.
Returns {number: [gap, ...]}, for example {4: [5, 5]}; a number seen once or never has an empty list.
''',
        'bin_edges': '''The upper edges of the age bins for a barrel of L numbers with K drawn (design section 3.4).

L: how many numbers the barrel holds.  K: how many are drawn.
Returns the different values of ceil(f * L / K) for the six fixed factors f, in rising order, for example
[1, 2, 3, 5, 8, 13] for L = 35 and K = 7. Ages above the last edge fall in one further bin.
''',
        'bin_of': '''The number of the age bin that an age falls in.

k: the age, in draws.  edges: the bins' upper edges, as bin_edges() returns them.
Returns how many edges lie below k, for example 3 for k = 4 and edges [1, 2, 3, 5, 8, 13] (bins count from 0).
''',
    },
}
