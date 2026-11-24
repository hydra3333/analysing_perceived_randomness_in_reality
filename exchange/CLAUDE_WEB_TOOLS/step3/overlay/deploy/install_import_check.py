"""The static import check: which project files a Python file imports, and the constructs that would hide one.

What this file is for
    A variant may be installed only if everything it imports is named: on its own lists, or on the infrastructure
    manifest. And the infrastructure may be installed only if every project file it imports is on the manifest
    too, or the installed tree would lack it. This file reads `import` and `from ... import` statements (it runs
    none of the code), says which project files they name, and finds the constructs that import by a computed
    name, which a variant's files and helpers may not use. It is a check against accidents: a determined
    workaround would escape it (specification section 20).

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 3.4 ("Imports are checked statically") and
    section 12.4 (nothing is infrastructure unless it is on the list);
    doc/Predictive_Randomness_Deployment_Design_v0_12.md sections 3.1 and 15 ("an imported module not listed").

Which of the project's own modules it uses
    None. The standard library only.

What uses it
    deploy/install_readiness.py (the two readiness markers), and its tests.
"""
from __future__ import annotations

import ast
from pathlib import Path

# The two folders of a tree that Python imports the project's code from: the engine, and the variants and helpers.
# A module name is looked for under each, in this order (the launchers put them on Python's path in this order).
IMPORT_ROOTS = ('src', 'src/methods')
# Names whose use in a variant's file or a helper means "import by a computed name" (specification 3.4). Any use
# of one of them fails the check, wherever it stands in the file.
FORBIDDEN_NAMES = ('importlib', '__import__', 'exec', 'eval')
# The module and the attribute whose use means "a change to Python's import path" (specification 3.4). Any mention
# of sys.path fails the check: a method has no reason to read it either.
PATH_MODULE, PATH_ATTRIBUTE = 'sys', 'path'


class ImportCheckRefused(ValueError):
    """A file could not be read as Python. The message names the file and what was found."""


def project_file_of(tree_root: Path, module_name: str) -> str | None:
    """The project file a module name is imported from.

    tree_root: the tree's folder.  module_name: a dotted name, for example 'research.reader' or 'E_019.core_v1'.
    Returns the file as a path from the tree root with forward slashes, for example 'src/research/reader.py' or
    'src/methods/E_019/__init__.py' for the package 'E_019'; None for a module that is not the project's (the
    standard library, numpy) or a package folder without an __init__.py. Never refuses.
    """
    for root in IMPORT_ROOTS:
        stem = f'{root}/{module_name.replace(".", "/")}'
        for candidate in (f'{stem}.py', f'{stem}/__init__.py'):
            if (Path(tree_root) / candidate).is_file():
                return candidate
    return None


def _parse(tree_root: Path, file_path: str) -> ast.Module:
    """Read one project file as Python's own parser reads it, running nothing.

    file_path: a path from the tree root, for example 'src/methods/E_019/core_v1.py'.
    Returns the parsed file. Refuses (ImportCheckRefused) a file that is missing or is not valid Python.
    """
    try:
        return ast.parse((Path(tree_root) / file_path).read_text(encoding='utf-8'))
    except (OSError, SyntaxError, ValueError) as error:
        raise ImportCheckRefused(f'{file_path}: cannot be read as Python ({error}). Correct the file.') from None


def _package_of(file_path: str) -> list:
    """The package a file lies in, as the parts of its dotted name, for resolving a relative import.

    file_path: a path from the tree root. Returns for example ['E_019'] for 'src/methods/E_019/core_v1.py',
    ['research'] for 'src/research/reader.py', and [] for a file directly in an import root.
    """
    for root in sorted(IMPORT_ROOTS, key=len, reverse=True):           # the longest root first: src/methods before src
        if file_path.startswith(root + '/'):
            return file_path[len(root) + 1:].split('/')[:-1]
    return []


def imported_project_files(tree_root: Path, file_path: str) -> list:
    """Every project file one file imports directly, wherever the statement stands (also inside a function).

    tree_root: the tree's folder.  file_path: the importing file, as a path from the tree root.
    Returns sorted (line number, project file) pairs, for example
        [(21, 'src/methods/E_019/__init__.py'), (21, 'src/methods/E_019/core_v1.py')]
    for the line `from E_019 import core_v1`: the package's own file is imported on the way and counts. A name
    that is no project file (the standard library, an attribute of a module) gives nothing.
    Refuses (ImportCheckRefused) a file that cannot be read as Python.
    """
    found = set()
    for node in ast.walk(_parse(tree_root, file_path)):
        names = []
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            base = node.module.split('.') if node.module else []
            if node.level:                                             # a relative import: from . or from .name
                package = _package_of(file_path)
                base = package[:len(package) - (node.level - 1)] + base
            if base:
                names = ['.'.join(base)] + ['.'.join(base + [alias.name]) for alias in node.names]
            else:
                names = [alias.name for alias in node.names]
        for name in names:
            parts = name.split('.')
            for depth in range(1, len(parts) + 1):
                target = project_file_of(tree_root, '.'.join(parts[:depth]))
                if target is not None:
                    found.add((node.lineno, target))
    return sorted(found)


def forbidden_constructs(tree_root: Path, file_path: str) -> list:
    """The places where a file imports by a computed name or touches Python's import path (specification 3.4).

    tree_root, file_path: as for imported_project_files.
    Returns sorted (line number, what was found) pairs, for example [(12, 'importlib'), (30, 'sys.path')]; an
    empty list when the file is clean. Refuses (ImportCheckRefused) a file that cannot be read as Python.
    """
    found = set()
    for node in ast.walk(_parse(tree_root, file_path)):
        if isinstance(node, ast.Name) and node.id in FORBIDDEN_NAMES:
            found.add((node.lineno, node.id))
        elif isinstance(node, ast.Attribute) and node.attr in FORBIDDEN_NAMES:
            found.add((node.lineno, node.attr))
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split('.')[0] in FORBIDDEN_NAMES:
                    found.add((node.lineno, alias.name.split('.')[0]))
        elif isinstance(node, ast.ImportFrom) and node.module:
            if node.module.split('.')[0] in FORBIDDEN_NAMES:
                found.add((node.lineno, node.module.split('.')[0]))
            if node.module == PATH_MODULE and any(alias.name == PATH_ATTRIBUTE for alias in node.names):
                found.add((node.lineno, f'{PATH_MODULE}.{PATH_ATTRIBUTE}'))
        if (isinstance(node, ast.Attribute) and node.attr == PATH_ATTRIBUTE
                and isinstance(node.value, ast.Name) and node.value.id == PATH_MODULE):
            found.add((node.lineno, f'{PATH_MODULE}.{PATH_ATTRIBUTE}'))
    return sorted(found)


def variant_import_faults(tree_root: Path, own_files, helper_files, manifest: dict) -> list:
    """What the static import check finds wrong in one variant (specification 3.4).

    tree_root: the tree's folder.  own_files: the variant's own listed files, as paths from the tree root, for
    example ['src/methods/E_019/PERIODIC_T4_V1/method.py'] (the declaration is not Python and is left out by the
    caller).  helper_files: its listed helpers, the same way.  manifest: {path: class} of the infrastructure.
    Returns sorted lines, each a full sentence naming the file and the line; empty when the check passes. A fault
    is: a forbidden construct; an import of a project file that is neither one of this variant's listed files or
    helpers nor infrastructure; an import of an infrastructure file whose class is not `forecast` (a file a method
    imports can change a forecast, so it must be classed so).
    Refuses (ImportCheckRefused) a listed file that cannot be read as Python.
    """
    listed = set(own_files) | set(helper_files)
    faults = []
    for file_path in sorted(path for path in listed if path.endswith('.py')):
        for line_number, construct in forbidden_constructs(tree_root, file_path):
            faults.append(f'{file_path} line {line_number}: it uses {construct}. A variant\'s files and helpers '
                          f'import by plain import statements only (specification 3.4).')
        for line_number, target in imported_project_files(tree_root, file_path):
            if target in listed:
                continue
            if target not in manifest:
                faults.append(f'{file_path} line {line_number}: it imports {target}, which is neither on this '
                              f'variant\'s lists (VARIANT.json: files, helpers) nor on the infrastructure '
                              f'manifest. List it as a helper.')
            elif manifest[target] != 'forecast':
                faults.append(f'{file_path} line {line_number}: it imports {target}, an infrastructure file of '
                              f'class {manifest[target]}. A file a method imports can change a forecast: its '
                              f'class in the manifest must be forecast.')
    return sorted(faults)


def infrastructure_import_faults(tree_root: Path, manifest: dict) -> list:
    """The project files the infrastructure imports that are not themselves on the manifest (deployment design
    section 15, "an imported module not listed"): an installed tree would lack them.

    tree_root: the tree's folder.  manifest: {path: class} of the infrastructure.
    Returns sorted lines, each a full sentence naming the importing file, the line and the missing file; empty
    when every import of project code by a manifest file names a manifest file. Variants are loaded by the
    engine by name at run time, never by an import statement, so no variant file is expected here.
    Refuses (ImportCheckRefused) a listed Python file that cannot be read as Python.
    """
    faults = []
    for file_path in sorted(path for path in manifest if path.endswith('.py')):
        for line_number, target in imported_project_files(tree_root, file_path):
            if target not in manifest:
                faults.append(f'{file_path} line {line_number}: it imports {target}, which is not on the '
                              f'infrastructure manifest. Add the file to deploy/INFRA_MANIFEST.ini with its '
                              f'class, or remove the import.')
    return sorted(faults)
