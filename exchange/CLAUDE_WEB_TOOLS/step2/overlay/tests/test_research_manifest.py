"""Tests of the infrastructure manifest's classes, by following the imports (specification v0.6 section 12.4).

A class is a careful label, not a proof, so these tests check each label against what the code imports: every
project file the forecasting entry point imports, and every infrastructure file a variant's files or helpers
import, must be classed `forecast`; every file the scoring, list, report and OV-1 code imports must be `forecast`
or `derived`. A planted dependency from the forecasting path into a weaker file must fail the check.
"""
import ast
import tempfile
import unittest
from pathlib import Path

from research import code_identity, variant_folders

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
# The two folders Python imports the project's code from.
IMPORT_ROOTS = ('src', 'src/methods')
# The entry point of the forecasting code, and the entry points of the code that makes derived results.
FORECAST_ENTRY = 'src/research/forecast_engine.py'
DERIVED_ENTRIES = ('src/research/scoring.py', 'src/research/variant_lists.py', 'src/research/status_file.py',
                   'src/research/code_identity.py')


def project_file_of(tree: Path, module: str) -> str | None:
    """The project file a module name is imported from, as a path from the tree root, or None for a module that
    is not the project's (the standard library, numpy). For example 'research.reader' -> 'src/research/reader.py'."""
    for root in IMPORT_ROOTS:
        for candidate in (f'{root}/{module.replace(".", "/")}.py', f'{root}/{module.replace(".", "/")}/__init__.py'):
            if (tree / candidate).is_file():
                return candidate
    return None


def imported_project_files(tree: Path, entries) -> set:
    """Every project file the entry files import, directly or through other project files, the entries included.

    It reads `import` and `from ... import` statements wherever they stand (also inside a function), and counts
    the __init__.py of every package on the way.
    """
    found, waiting = set(), list(entries)
    while waiting:
        path = waiting.pop()
        if path in found:
            continue
        found.add(path)
        for node in ast.walk(ast.parse((tree / path).read_text(encoding='utf-8'))):
            names = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                names = [node.module] + [f'{node.module}.{alias.name}' for alias in node.names]
            for name in names:
                parts = name.split('.')
                for depth in range(1, len(parts) + 1):
                    target = project_file_of(tree, '.'.join(parts[:depth]))
                    if target is not None:
                        waiting.append(target)
    return found


def class_faults(tree: Path, manifest: dict, entries, allowed, excused=()) -> list:
    """The files reached from the entries whose class is not allowed, as 'path: found class' lines.

    excused: files that need no class of their own (a variant's files and helpers: its fingerprint covers them).
    """
    faults = []
    for path in sorted(imported_project_files(tree, entries)):
        if path in excused:
            continue
        if manifest.get(path) not in allowed:
            faults.append(f'{path}: {manifest.get(path, "not on the manifest")}')
    return faults


class ManifestClasses(unittest.TestCase):
    """The real manifest of this tree."""

    @classmethod
    def setUpClass(cls):
        """Read the manifest and every variant's own files and helpers once."""
        cls.manifest = code_identity.read_manifest(REPOSITORY_ROOT)
        variants, refused = variant_folders.find_variants(REPOSITORY_ROOT / 'src' / 'methods')
        assert not refused, refused
        cls.variant_files = {f'src/methods/{path}' for variant in variants for path, _ in variant.fingerprint_lines
                             if path.endswith('.py')}

    def test_everything_the_forecasting_entry_point_imports_is_forecast_class(self):
        self.assertEqual(class_faults(REPOSITORY_ROOT, self.manifest, [FORECAST_ENTRY], ('forecast',)), [])

    def test_every_infrastructure_file_a_variant_or_helper_imports_is_forecast_class(self):
        self.assertEqual(class_faults(REPOSITORY_ROOT, self.manifest, sorted(self.variant_files), ('forecast',),
                                      excused=self.variant_files), [])

    def test_everything_the_derived_results_code_imports_is_forecast_or_derived_class(self):
        self.assertEqual(class_faults(REPOSITORY_ROOT, self.manifest, DERIVED_ENTRIES, ('forecast', 'derived')), [])

    def test_every_file_of_the_engine_is_on_the_manifest(self):
        engine = {path.relative_to(REPOSITORY_ROOT).as_posix() for path in (REPOSITORY_ROOT / 'src' / 'research').glob('*.py')}
        self.assertEqual(sorted(engine - set(self.manifest)), [])

    def test_no_variant_file_or_helper_is_also_listed_as_infrastructure(self):
        self.assertEqual(sorted(self.variant_files & set(self.manifest)), [])


class TheCheckCatchesAPlantedFault(unittest.TestCase):
    """The class check itself: a label that is too weak must be found (EX_267 N01)."""

    def setUp(self):
        """A small invented tree: an entry that imports a helper module, which imports a third (inside a function)."""
        self.folder = tempfile.TemporaryDirectory()
        self.tree = Path(self.folder.name)
        (self.tree / 'src' / 'pkg').mkdir(parents=True)
        (self.tree / 'src' / 'pkg' / '__init__.py').write_text('')
        (self.tree / 'src' / 'pkg' / 'entry.py').write_text('import json\nfrom pkg import middle\n')
        (self.tree / 'src' / 'pkg' / 'middle.py').write_text('def f():\n    from pkg.deep import g\n    return g()\n')
        (self.tree / 'src' / 'pkg' / 'deep.py').write_text('def g():\n    return 1\n')
        self.all_forecast = {f'src/pkg/{name}.py': 'forecast' for name in ('__init__', 'entry', 'middle', 'deep')}

    def tearDown(self):
        """Remove the temporary folder."""
        self.folder.cleanup()

    def test_imports_are_followed_through_packages_and_inside_functions(self):
        self.assertEqual(imported_project_files(self.tree, ['src/pkg/entry.py']), set(self.all_forecast))
        self.assertEqual(class_faults(self.tree, self.all_forecast, ['src/pkg/entry.py'], ('forecast',)), [])

    def test_a_derived_label_on_a_file_the_forecasting_entry_imports_is_found(self):
        manifest = dict(self.all_forecast, **{'src/pkg/deep.py': 'derived'})
        self.assertEqual(class_faults(self.tree, manifest, ['src/pkg/entry.py'], ('forecast',)), ['src/pkg/deep.py: derived'])

    def test_a_planted_dependency_from_the_forecasting_path_into_an_other_file_is_found(self):
        (self.tree / 'src' / 'pkg' / 'launcher.py').write_text('X = 1\n')
        (self.tree / 'src' / 'pkg' / 'deep.py').write_text('import pkg.launcher\n')
        manifest = dict(self.all_forecast, **{'src/pkg/launcher.py': 'other'})
        self.assertEqual(class_faults(self.tree, manifest, ['src/pkg/entry.py'], ('forecast',)), ['src/pkg/launcher.py: other'])

    def test_a_file_missing_from_the_manifest_is_found(self):
        manifest = {path: label for path, label in self.all_forecast.items() if not path.endswith('middle.py')}
        self.assertEqual(class_faults(self.tree, manifest, ['src/pkg/entry.py'], ('forecast',)),
                         ['src/pkg/middle.py: not on the manifest'])


if __name__ == '__main__':
    unittest.main()
