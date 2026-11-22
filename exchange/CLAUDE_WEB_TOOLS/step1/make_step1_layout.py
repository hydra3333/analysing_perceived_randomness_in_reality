"""Build step 1 (the folder layout): the builder that turns a copy of the project into the new layout.

What this file is for
    It makes every change of build step 1 mechanically, in a disposable copy of the project, so that the change
    can be repeated exactly and checked: it moves the method files to the family and variant layout, renames the
    three shared helpers, creates each variant's folder with its `method.py` and `VARIANT.json`, replaces the
    runner's hand-written table of methods by the table built from the folders, and makes every import of a moved
    file follow the move. It changes no calculation. It refuses (an assertion) if the tree is not exactly as
    expected, and it never runs against the owner's checkout: Claude runs it in the cloud workspace, and the
    result travels to the owner as a reviewed package.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 17.3, phase 1, and its table "What phase 1
    moves"; the layout is section 3.2 and the declaration is section 3.4.

Which of the project's own modules it uses
    None: it reads and writes files only. It reads the installed method declarations
    (src/methods/_common/contract_data/declarations) as data, for each variant's games, minimum history and view.

What uses it
    Nothing in the project. It is kept beside the package as the record of how the package was made.

Usage:  python make_step1_layout.py <a disposable Git clone of the project at the base commit>
"""
from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------- constants

# This file's own folder: the templates of the newly written files are beside it.
TEMPLATES_FOLDER = Path(__file__).resolve().parent / 'templates'

# The three helpers used by more than one family: old place and name, new place and versioned name (spec 17.3).
SHARED_HELPERS = {'recurrence_gaps': 'recurrence_gaps_v1', 'occurrence_counts': 'occurrence_counts_v1',
                  'polynomial_fits': 'polynomial_fits_v1'}

# E_1 keeps its own modules where the proof-of-concept suite imports them; only its external wrapper moves,
# and becomes the method.py of E_1's one variant (spec 17.3).
E1_FAMILY, E1_VARIANT = 'E_001', 'FULL_HISTORY_RAW_COUNTS_V1'
E1_OLD_WRAPPER = 'contract_adapters/e_001.py'
E1_OLD_WRAPPER_PACKAGE_FILE = 'contract_adapters/__init__.py'   # left with nothing to describe: removed

# The games, and the order they are written in a declaration.
GAMES = ('POWERBALL', 'OZLOTTO')

# In VARIANT.json's helper list, files under this folder are infrastructure, not helpers (spec 3.4, 12.4).
INFRASTRUCTURE_FOLDER = '_common'

# What the runner's hand-written table is replaced by (three lines of imports and comment, one of table).
RUNNER_NEW_TABLE = '''from _common.method_table import build_method_table

# The methods this runner can dispatch, read from the folder tree (specification 3.2 and 17.3): one entry per
# family, and each entry sends a task to the method.py of the task's own variant.
# Being listed here is not permission: the dispatch gate decides.
ADAPTERS = build_method_table()
'''

# Lines of tests that name a moved file by its path, list a family folder's content, or pin the runner's table:
# (file, old text, new text, how many times the old text must occur). They follow the move; nothing else in a
# test changes. replace_counted refuses any other count.
_E1_METHOD = 'E_001/FULL_HISTORY_RAW_COUNTS_V1/method.py'
_OLD_LISTING = "sorted(p.name for p in folder.iterdir() if p.name != '__pycache__')"
_NEW_LISTING = "sorted(p.name for p in folder.iterdir() if p.is_file())"     # variant folders are beside the files now
_OLD_TABLE_CHECK = "self.assertIs(M.ADAPTERS[name], mod)"
_NEW_TABLE_CHECK = "self.assertTrue(all(m.core_v1 is mod for m in M.ADAPTERS[name].variant_methods.values()))"
TEST_TEXT_CHANGES = (
    # The three shared helpers, read as text by their own tests.
    ('tests/test_recurrence_gaps.py', "'_common' / 'recurrence_gaps.py'", "'_shared' / 'recurrence_gaps_v1.py'", 1),
    ('tests/test_occurrence_counts.py', "'_common' / 'occurrence_counts.py'", "'_shared' / 'occurrence_counts_v1.py'", 1),
    ('tests/test_polynomial_fits.py', "'_common' / 'polynomial_fits.py'", "'_shared' / 'polynomial_fits_v1.py'", 1),
    # The list of modules that must import without side effects.
    ('tests/test_code3_retirement.py', "'_common.occurrence_counts', '_common.polynomial_fits',",
     "'_shared.occurrence_counts_v1', '_shared.polynomial_fits_v1',", 1),
    ('tests/test_code3_retirement.py', "'_common.recurrence_gaps',", "'_shared.recurrence_gaps_v1',", 1),
    ('tests/test_code3_retirement.py', "'contract_adapters.e_001',", "'E_001.FULL_HISTORY_RAW_COUNTS_V1.method',", 1),
    # E_1's wrapper, read as text or hashed. The reference file's key stays the old path: it names the archived
    # revision-2 bytes, and a reference is never refreshed.
    ('tests/test_e1r3_revision3.py', "'src' / 'methods' / 'contract_adapters' / 'e_001.py'",
     "'src' / 'methods' / 'E_001' / 'FULL_HISTORY_RAW_COUNTS_V1' / 'method.py'", 1),
    ('tests/test_e1r3_revision3.py',
     "        for rel in ('src/methods/E_001/multigame_e1.py', 'src/methods/contract_adapters/e_001.py'):\n"
     "            self.assertNotEqual(hashlib.sha256((ROOT / rel).read_bytes()",
     "        for rel, now in (('src/methods/E_001/multigame_e1.py', 'src/methods/E_001/multigame_e1.py'),\n"
     "                         ('src/methods/contract_adapters/e_001.py', 'src/methods/" + _E1_METHOD + "')):\n"
     "            self.assertNotEqual(hashlib.sha256((ROOT / now).read_bytes()", 1),
    # The wrappers that must read no data: once one folder of wrappers, now each variant's method.py.
    ('tests/test_e2r_dispatch.py', "(ROOT / 'src' / 'methods' / 'contract_adapters').glob('*.py')",
     "(ROOT / 'src' / 'methods').glob('E_*/*/method.py')", 1),
    # A released family's calculation file.
    ('tests/test_rel1_release.py', "method_folder(m) / 'contract.py'", "method_folder(m) / 'core_v1.py'", 1),
    # A family folder's own files (its variant folders are now beside them).
    ('tests/test_wave1_frequency.py', _OLD_LISTING, _NEW_LISTING, 1),
    ('tests/test_wave1_frequency.py', "['__init__.py', 'contract.py', 'variants.py']", "['__init__.py', 'core_v1.py', 'variants.py']", 1),
    ('tests/test_wave2_recurrence.py', _OLD_LISTING, _NEW_LISTING, 1),
    ('tests/test_wave2_recurrence.py', "['__init__.py', 'contract.py', 'variants.py']", "['__init__.py', 'core_v1.py', 'variants.py']", 1),
    ('tests/test_e3_e4_polynomial.py', _OLD_LISTING, _NEW_LISTING, 1),
    ('tests/test_e3_e4_polynomial.py', "['__init__.py', 'contract.py', 'variants.py']", "['__init__.py', 'core_v1.py', 'variants.py']", 1),
    ('tests/test_e6_beta_bernoulli.py', _OLD_LISTING, _NEW_LISTING, 1),
    ('tests/test_e6_beta_bernoulli.py', "['__init__.py', 'beta_bernoulli.py', 'contract.py']", "['__init__.py', 'beta_bernoulli.py', 'core_v1.py']", 1),
    # The runner's table: once "the family's module itself", now "every variant's method.py uses that module".
    ('tests/test_wave1_frequency.py', _OLD_TABLE_CHECK, _NEW_TABLE_CHECK, 1),
    ('tests/test_wave2_recurrence.py', _OLD_TABLE_CHECK, _NEW_TABLE_CHECK, 1),
    ('tests/test_e3_e4_polynomial.py', _OLD_TABLE_CHECK, _NEW_TABLE_CHECK, 1),
    ('tests/test_e6_beta_bernoulli.py', "self.assertIs(M.ADAPTERS['E_6'], E6)",
     "self.assertTrue(all(m.core_v1 is E6 for m in M.ADAPTERS['E_6'].variant_methods.values()))", 1),
)


def run_git(tree: Path, *arguments: str) -> str:
    """Run one Git command in the tree and return what it printed. Refuses (an exception) if Git fails."""
    return subprocess.run(['git', '-C', str(tree), *arguments], check=True, capture_output=True, text=True).stdout


def replace_counted(path: Path, old: str, new: str, count: int) -> None:
    """Replace `old` by `new` in one file, requiring that `old` occurs exactly `count` times.

    path: the file to change.  old, new: exact text.  count: how many occurrences are expected.
    Returns nothing. Refuses (an assertion naming the file and both counts) if the count differs, so a change
    is never made to a file that is not as expected.
    """
    text = path.read_text(encoding='utf-8')
    found = text.count(old)
    assert found == count, f'{path}: expected {count} occurrence(s) of {old!r}, found {found}'
    path.write_bytes(text.replace(old, new).encode('utf-8'))


def replace_import_lines(path: Path, pattern: str, replacement: str) -> int:
    """Rewrite the import lines of one file that match a pattern; touch no other line.

    path: a Python source file.  pattern: a regular expression for a whole import statement (after its
    indentation).  replacement: its new text (may use the pattern's groups).
    Returns how many lines were changed, for example 2. Line endings and every other byte are kept.
    """
    lines = path.read_bytes().decode('utf-8').split('\n')
    changed = 0
    for position, line in enumerate(lines):
        match = re.fullmatch(r'(\s*)' + pattern + r'(\s*(?:#.*)?)', line)
        if match:
            groups = match.groups()
            lines[position] = groups[0] + match.expand(shift_groups(replacement)) + groups[-1]
            changed += 1
    if changed:
        path.write_bytes('\n'.join(lines).encode('utf-8'))
    return changed


def shift_groups(replacement: str) -> str:
    r"""Shift \1, \2 ... in a replacement by one, because replace_import_lines adds a leading group.

    replacement: for example r'from _shared import \1_v1 as \2'.
    Returns for example r'from _shared import \2_v1 as \3'.
    """
    return re.sub(r'\\(\d)', lambda m: '\\' + str(int(m.group(1)) + 1), replacement)


def project_imports(source_path: Path, methods_folder: Path) -> list:
    """List the project files one Python file imports directly (not the standard library, not third parties).

    source_path: the file to read.  methods_folder: <tree>/src/methods, where project modules are found.
    Returns paths from src/methods with forward slashes, for example
        ['E_002/__init__.py', 'E_002/core_v1.py', '_common/game_profiles.py'].
    A package's __init__.py is listed with any module imported from it, because Python runs it first.
    """
    found = []
    package_parts = source_path.relative_to(methods_folder).parts[:-1]
    for node in ast.walk(ast.parse(source_path.read_text(encoding='utf-8'))):
        names = []
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            base = list(package_parts[:len(package_parts) - node.level + 1]) if node.level else []
            module = '.'.join(base + ([node.module] if node.module else []))
            names = [module] + [f'{module}.{alias.name}' for alias in node.names]
        for name in names:
            parts = name.split('.')
            for depth in range(1, len(parts) + 1):
                package_init = methods_folder.joinpath(*parts[:depth], '__init__.py')
                module_file = methods_folder.joinpath(*parts[:depth]).with_suffix('.py')
                for candidate in (package_init, module_file):
                    if candidate.is_file():
                        found.append(candidate.relative_to(methods_folder).as_posix())
    return sorted(set(found))


def helpers_of(method_path: Path, methods_folder: Path) -> list:
    """List every helper file a variant's method.py depends on, directly or through another helper.

    method_path: the variant's method.py.  methods_folder: <tree>/src/methods.
    Returns paths from src/methods, sorted, for example
        ['E_002/__init__.py', 'E_002/core_v1.py', 'E_002/variants.py', '_shared/recurrence_gaps_v1.py'].
    Infrastructure files (under _common/) are not helpers and are left out, with everything they import.
    """
    helpers, to_read = set(), [method_path]
    while to_read:
        for relative in project_imports(to_read.pop(), methods_folder):
            if relative.split('/')[0] == INFRASTRUCTURE_FOLDER or relative in helpers:
                continue
            helpers.add(relative)
            to_read.append(methods_folder / relative)
    return sorted(helpers)


def declared_variants(methods_folder: Path) -> dict:
    """Read the installed method declarations and return each variant's games, minimum history and view.

    methods_folder: <tree>/src/methods.
    Returns {(method ID, variant ID): {'minimum_earlier_draws': {game: n}, 'observation_view': view}}, for example
        {('E_2', 'RECUR_MEAN_ALL_V1'): {'minimum_earlier_draws': {'POWERBALL': 104, 'OZLOTTO': 104},
                                         'observation_view': 'UNORDERED_SET'}, ...}.
    Each game's newest declaration of the variant is used. Refuses a variant with more than one view.
    """
    variants = {}
    declarations = methods_folder / '_common' / 'contract_data' / 'declarations'
    for game in GAMES:
        newest = {}
        for path in sorted((declarations / game).glob('*/*/r*.json')):
            record = json.loads(path.read_text(encoding='utf-8'))
            key = (record['method_id'], record['variant_id'])
            if key not in newest or int(record['method_revision']) > int(newest[key]['method_revision']):
                newest[key] = record
        for key, record in newest.items():
            assert len(record['observation_views']) == 1, f'{key}: more than one observation view'
            entry = variants.setdefault(key, {'minimum_earlier_draws': {},
                                              'observation_view': record['observation_views'][0]})
            assert entry['observation_view'] == record['observation_views'][0], f'{key}: views differ by game'
            entry['minimum_earlier_draws'][game] = record['minimum_history_draws']
    return variants


def family_title(family_folder: Path) -> str:
    """The family's name, from the first line of its __init__.py, without the bracketed revision note.

    Returns for example 'E_2 - Expected Recurrence-Interval Alignment'.
    """
    first_line = (family_folder / '__init__.py').read_text(encoding='utf-8').splitlines()[0]
    return first_line.strip('"').split(' (')[0].rstrip('.').strip()


def write_variant_declaration(variant_folder: Path, family: str, variant: str, title: str, description: str,
                              declared: dict, methods_folder: Path) -> None:
    """Write one variant's VARIANT.json (specification 3.4).

    variant_folder: where it goes.  family, variant: the two folder names.  title, description: one line each.
    declared: the variant's entry from declared_variants().  methods_folder: <tree>/src/methods.
    Returns nothing. The helper list is worked out from the import statements, never typed by hand.
    """
    content = {'family': family, 'variant': variant, 'title': title, 'description': description,
               'games': [game for game in GAMES if game in declared['minimum_earlier_draws']],
               'minimum_earlier_draws': {game: declared['minimum_earlier_draws'][game] for game in GAMES
                                         if game in declared['minimum_earlier_draws']},
               'observation_view': declared['observation_view'],
               'files': ['method.py'],
               'helpers': helpers_of(variant_folder / 'method.py', methods_folder)}
    (variant_folder / 'VARIANT.json').write_bytes((json.dumps(content, indent=2) + '\n').encode('ascii'))


def main() -> int:
    """Make every step 1 change in the tree named on the command line; print what was done; return 0."""
    tree = Path(sys.argv[1]).resolve()
    methods = tree / 'src' / 'methods'
    assert run_git(tree, 'status', '--porcelain') == '', 'the tree must be a clean Git clone'
    declared = declared_variants(methods)

    # 1. The three shared helpers: _common/<name>.py -> _shared/<name>_v1.py, bytes unchanged.
    (methods / '_shared').mkdir()
    for old_name, new_name in SHARED_HELPERS.items():
        run_git(tree, 'mv', f'src/methods/_common/{old_name}.py', f'src/methods/_shared/{new_name}.py')

    # 2. Every family but E_1: contract.py -> core_v1.py; one folder per variant with method.py and VARIANT.json.
    method_template = (TEMPLATES_FOLDER / 'variant_method.py.template').read_text(encoding='ascii')
    families = sorted(p.name for p in methods.iterdir() if p.is_dir() and re.fullmatch(r'E_\d{3}', p.name))
    variant_count = 0
    for family in families:
        if family == E1_FAMILY:
            continue
        method_id = f'E_{int(family[2:])}'
        run_git(tree, 'mv', f'src/methods/{family}/contract.py', f'src/methods/{family}/core_v1.py')
        settings_file = 'variants.py' if (methods / family / 'variants.py').is_file() else 'beta_bernoulli.py'
        settings_text = (methods / family / settings_file).read_text(encoding='utf-8')
        for (declared_method, variant), entry in sorted(declared.items()):
            if declared_method != method_id:
                continue
            assert f"'{variant}'" in settings_text, f'{family}/{settings_file} does not name {variant}'
            folder = methods / family / variant
            folder.mkdir()
            (folder / 'method.py').write_bytes(method_template.replace('@@FAMILY@@', family)
                                               .replace('@@METHOD_ID@@', method_id)
                                               .replace('@@VARIANT_ID@@', variant).encode('ascii'))
            variant_count += 1

    # 3. E_1: its external wrapper becomes its one variant's method.py, bytes unchanged.
    (methods / E1_FAMILY / E1_VARIANT).mkdir()
    run_git(tree, 'mv', f'src/methods/{E1_OLD_WRAPPER}', f'src/methods/{E1_FAMILY}/{E1_VARIANT}/method.py')
    run_git(tree, 'rm', '-q', f'src/methods/{E1_OLD_WRAPPER_PACKAGE_FILE}')
    variant_count += 1

    # 4. Every import of a moved file follows the move, in src/ and in the tests; no other line changes.
    import_changes = 0
    helper_names = '|'.join(SHARED_HELPERS)
    for path in sorted(list((tree / 'src').rglob('*.py')) + list((tree / 'tests').rglob('*.py'))):
        import_changes += replace_import_lines(path, rf'from _common import ({helper_names}) as (\w+)',
                                               r'from _shared import \1_v1 as \2')
        import_changes += replace_import_lines(path, r'from (E_\d{3}) import contract as (\w+)',
                                               r'from \1 import core_v1 as \2')
        import_changes += replace_import_lines(path, r'from contract_adapters import e_001',
                                               f'from {E1_FAMILY}.{E1_VARIANT} import method as e_001')

    # 5. The runner's hand-written table of methods is replaced by the table built from the folder tree.
    (methods / '_common' / 'method_table.py').write_bytes((TEMPLATES_FOLDER / 'method_table.py').read_bytes())
    runner = methods / 'Method_Contract_Runner.py'
    runner_text = runner.read_text(encoding='utf-8')
    start = runner_text.index(f'from {E1_FAMILY}.{E1_VARIANT} import method as e_001')
    end_marker = "'E_9': e_009, 'E_10': e_010, 'E_17': e_017, 'E_18': e_018, 'E_19': e_019}\n"
    end = runner_text.index(end_marker) + len(end_marker)
    assert runner_text.count(end_marker) == 1
    runner.write_bytes((runner_text[:start] + RUNNER_NEW_TABLE + runner_text[end:]).encode('utf-8'))

    # 6. Each variant's declaration, written last so that its helper list is read from the finished imports.
    for family in families:
        method_id = f'E_{int(family[2:])}'
        title = family_title(methods / family) if family != E1_FAMILY else 'E_1 - Historical Appearance Frequency'
        for (declared_method, variant), entry in sorted(declared.items()):
            if declared_method != method_id:
                continue
            if family == E1_FAMILY:
                description = ("The wrapper that calls E_1's own counting function (E_001/multigame_e1.py) unchanged "
                               'and checks the record against it')
            else:
                settings_file = 'variants.py' if (methods / family / 'variants.py').is_file() else 'beta_bernoulli.py'
                description = (f'Variant {variant}: its fixed settings are the {variant} line of '
                               f'{family}/{settings_file}; the calculation is {family}/core_v1.py')
            write_variant_declaration(methods / family / variant, family, variant, title, description, entry, methods)

    # 7. Lines of tests that name a moved file by path, or list a family folder's content, follow the move.
    for relative, old, new, count in TEST_TEXT_CHANGES:
        replace_counted(tree / relative, old, new, count)

    run_git(tree, 'add', '-A', 'src', 'tests')
    print(f'families: {len(families)}; variant folders: {variant_count}; import lines changed: {import_changes}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
