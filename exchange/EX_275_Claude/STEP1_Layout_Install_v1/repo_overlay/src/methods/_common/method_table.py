"""The runner's table of methods, built from the folder tree.

What this file is for
    Until build step 1 the runner kept a hand-written table of the methods it could dispatch. From build step 1
    the table is read from the folders: every family folder (E_002, E_017, ...) holds one folder per variant, and
    each variant folder holds its own `method.py` and its declaration `VARIANT.json`. This file finds them, checks
    that each folder is what it says it is, and gives the runner one entry per family that sends a task to the
    `method.py` of the task's own variant. It computes nothing itself and changes no forecast.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 3.2 (the layout) and section 17.3, phase 1
    ("the table is built from the folder tree").

Which of the project's own modules it uses
    None. It imports each variant's `method.py` by its folder path, which is the purpose of this file.

What uses it
    src/methods/Method_Contract_Runner.py builds its ADAPTERS table with build_method_table(); the walk-forward
    driver and the tests take the table from the runner, as before.
"""
from __future__ import annotations

import importlib
import json
import re
from collections.abc import Mapping
from pathlib import Path
from types import MappingProxyType

# src/methods, found from this file's own place (src/methods/_common/method_table.py): no path is typed in code.
METHODS_FOLDER = Path(__file__).resolve().parents[1]

# A family folder is "E_" and three digits (E_002). The old records name the same family without the padding
# (E_2), so the table is keyed by that unpadded method ID, as the hand-written table was.
FAMILY_FOLDER_PATTERN = re.compile(r'E_(\d{3})')

# The two files that make a folder a variant folder (specification 3.2).
VARIANT_DECLARATION_NAME = 'VARIANT.json'
VARIANT_METHOD_NAME = 'method.py'

# Folders Python itself creates beside source files; never a variant.
IGNORED_FOLDER_NAMES = ('__pycache__',)


class MethodTableRefused(ValueError):
    """A folder under src/methods is not laid out as the specification requires. The message names the folder,
    says what was found and what to do."""


class FamilyMethods:
    """The variants of one family, offered to the runner as one compute() and one verify().

    The runner and the walk-forward driver call `table[method_id].compute(task, view)` and
    `table[method_id].verify(task, view, forecast, diagnostic)`, exactly as they did with the hand-written
    table. This class passes each call to the `method.py` of the variant the task names.
    """

    def __init__(self, method_id: str, variant_methods: Mapping):
        """method_id: the family's unpadded ID, for example 'E_2'.
        variant_methods: {variant ID: the imported method.py module}, for example
            {'RECUR_MEAN_ALL_V1': <module 'E_002.RECUR_MEAN_ALL_V1.method'>, ...}.
        """
        self.method_id = method_id
        self.variant_methods = MappingProxyType(dict(variant_methods))

    def method_for(self, task):
        """Return the method.py module of the task's own variant.

        task: the frozen MethodTask the runner built (it carries method_id and variant_id).
        Returns the module, for example <module 'E_002.RECUR_MEAN_ALL_V1.method'>.
        Refuses (ValueError) a task of another family, or of a variant that has no folder here.
        """
        if task.method_id != self.method_id:
            raise ValueError(f'this table entry is for {self.method_id}; the task is for {task.method_id}')
        method = self.variant_methods.get(task.variant_id)
        if method is None:
            raise ValueError(f'unknown {self.method_id} variant {task.variant_id!r}: no variant folder of that name '
                             f'holds {VARIANT_METHOD_NAME} and {VARIANT_DECLARATION_NAME}')
        return method

    def compute(self, task, view):
        """Compute the task's forecast with its own variant's method.py and return that method's output
        (a MethodOutput, for example MethodOutput(barrels={'MAIN': BarrelOutput(...)})), unchanged."""
        return self.method_for(task).compute(task, view)

    def verify(self, task, view, forecast, diagnostic) -> None:
        """Run the variant's own check of its record; raises whatever that check raises, returns nothing."""
        self.method_for(task).verify(task, view, forecast, diagnostic)


def method_id_of_family_folder(family_folder_name: str) -> str:
    """Turn a family folder's name into the method ID the records use.

    family_folder_name: for example 'E_002'.
    Returns the unpadded ID, for example 'E_2'. Refuses a name that is not "E_" and three digits.
    """
    match = FAMILY_FOLDER_PATTERN.fullmatch(family_folder_name)
    if match is None:
        raise MethodTableRefused(f'{family_folder_name!r} is not a family folder name (E_ and three digits)')
    return f'E_{int(match.group(1))}'


def load_variant_method(family_folder: Path, variant_folder: Path):
    """Check one variant folder and import its method.py.

    family_folder: for example <src/methods>/E_002.  variant_folder: for example .../E_002/RECUR_MEAN_ALL_V1.
    Returns the imported module, for example <module 'E_002.RECUR_MEAN_ALL_V1.method'>.
    Refuses if either of the two files is missing, if VARIANT.json is not valid JSON or names another family
    or variant than its folders, or if method.py has no compute() or verify().
    """
    declaration_path = variant_folder / VARIANT_DECLARATION_NAME
    method_path = variant_folder / VARIANT_METHOD_NAME
    if not (declaration_path.is_file() and method_path.is_file()):
        raise MethodTableRefused(f'{variant_folder} holds only one of {VARIANT_METHOD_NAME} and '
                                 f'{VARIANT_DECLARATION_NAME}. A variant folder needs both: add the missing file, '
                                 'or remove the folder if it is not a variant.')
    try:
        declaration = json.loads(declaration_path.read_text(encoding='utf-8'))
    except ValueError as problem:
        raise MethodTableRefused(f'{declaration_path} is not valid JSON ({problem}). Correct the file.') from None
    named = (declaration.get('family'), declaration.get('variant'))
    if named != (family_folder.name, variant_folder.name):
        raise MethodTableRefused(f'{declaration_path} declares family and variant {named}, but it is in the folder '
                                 f'{family_folder.name}/{variant_folder.name}. The declaration and the folder '
                                 'names must be equal: correct whichever is wrong.')
    method = importlib.import_module(f'{family_folder.name}.{variant_folder.name}.method')
    for needed in ('compute', 'verify'):
        if not callable(getattr(method, needed, None)):
            raise MethodTableRefused(f'{method_path} has no {needed}() function. Every method.py provides '
                                     'compute(task, view) and verify(task, view, forecast, diagnostic).')
    return method


def build_method_table() -> Mapping:
    """Read the folder tree under src/methods and build the table of methods.

    Returns a read-only mapping {method ID: FamilyMethods}, in family-folder order, for example
        {'E_1': <FamilyMethods E_1: 1 variant>, 'E_2': <FamilyMethods E_2: 3 variants>, ...}.
    A family folder with no variant folder is left out. Refuses (MethodTableRefused) on any folder that is
    not laid out as the specification requires; nothing is skipped silently.
    """
    table = {}
    for family_folder in sorted(p for p in METHODS_FOLDER.iterdir() if p.is_dir()):
        if FAMILY_FOLDER_PATTERN.fullmatch(family_folder.name) is None:
            continue
        variant_methods = {}
        for variant_folder in sorted(p for p in family_folder.iterdir() if p.is_dir()):
            if variant_folder.name in IGNORED_FOLDER_NAMES:
                continue
            has_either = ((variant_folder / VARIANT_DECLARATION_NAME).exists()
                          or (variant_folder / VARIANT_METHOD_NAME).exists())
            if not has_either:
                raise MethodTableRefused(f'{variant_folder} is a folder inside a family folder but holds neither '
                                         f'{VARIANT_METHOD_NAME} nor {VARIANT_DECLARATION_NAME}. Only variant '
                                         'folders belong there: remove it or complete it.')
            variant_methods[variant_folder.name] = load_variant_method(family_folder, variant_folder)
        if variant_methods:
            table[method_id_of_family_folder(family_folder.name)] = FamilyMethods(
                method_id_of_family_folder(family_folder.name), variant_methods)
    return MappingProxyType(table)
