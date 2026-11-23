"""Families and variants as folders: finding them, checking each declaration, and the variant's fingerprint.

What this file is for
    A variant is a folder under src/methods/<family>/ holding method.py and its declaration VARIANT.json. This
    file finds every variant folder of a tree, checks the declaration against the folder, computes the variant's
    fingerprint (one SHA-256 over the declaration, the files it lists and the helpers it lists), and imports the
    variant's method.py. A folder that fails a check is not run and is named with the reason.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md sections 3.1, 3.2 and 3.4 (identity, layout, the
    declaration and the fingerprint). The readiness marker and the static import check of 3.4 and 4 belong to
    the install tools (build step 3).

Which of the project's own modules it uses
    _common.game_profiles     get_profile: to check the games a declaration names

What uses it
    research/research_job.py, research/forecast_engine.py, research/withdraw.py, and the engine's tests.
"""
from __future__ import annotations

import hashlib
import importlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

from _common.game_profiles import get_profile

# A family folder is "E_" and three digits (E_002); a variant folder is capitals, digits and underscores.
FAMILY_FOLDER_PATTERN = re.compile(r'E_\d{3}\Z')
VARIANT_FOLDER_PATTERN = re.compile(r'[A-Z0-9_]{3,96}\Z')
# The declaration's file name, and the exact keys it holds (specification 3.4).
DECLARATION_NAME = 'VARIANT.json'
DECLARATION_KEYS = ('family', 'variant', 'title', 'description', 'games', 'minimum_earlier_draws',
                    'observation_view', 'files', 'helpers')
# Files a variant folder may hold besides those its declaration lists (3.4): the status file and the readiness
# marker. Python's own cache folders and files are ignored.
STATUS_FILE_NAME = 'VARIANT_STATUS.ini'
MARKER_FILE_NAME = 'I_AM_INSTALLABLE.json'
# The observation views a declaration may name (R2 section 4).
OBSERVATION_VIEWS = ('UNORDERED_SET', 'OPERATOR_DRAWN_ORDER', 'PAIRED_DIAGNOSTIC')
# The two functions every method.py provides.
METHOD_FUNCTIONS = ('compute', 'verify')


class VariantRefused(ValueError):
    """A variant folder is not as the specification requires. The message names the folder or file, says what
    was found and what to do."""


@dataclass(frozen=True)
class Variant:
    """One variant of a tree.

    family, variant: the folder names, for example 'E_002' and 'RECUR_MEAN_ALL_V1'.
    folder: the variant's folder.  declaration: the parsed VARIANT.json.
    fingerprint: 64 hexadecimal characters (see fingerprint_of).
    fingerprint_lines: the hashed list the fingerprint was computed from, as (path from src/methods, sha256).
    """
    family: str
    variant: str
    folder: Path
    declaration: dict
    fingerprint: str
    fingerprint_lines: tuple

    @property
    def identity(self) -> str:
        """The variant's name as people write it, for example 'E_002/RECUR_MEAN_ALL_V1'."""
        return f'{self.family}/{self.variant}'

    @property
    def method_id(self) -> str:
        """The family's ID as the methods and the tie rule use it: no padding, for example 'E_2' for 'E_002'."""
        return f'E_{int(self.family[2:])}'

    def supports(self, game_id: str) -> bool:
        """True if the declaration lists the game, for example supports('OZLOTTO')."""
        return game_id in self.declaration['games']

    def minimum_earlier_draws(self, game_id: str) -> int:
        """How many earlier draws the variant needs in a game, for example 104."""
        return self.declaration['minimum_earlier_draws'][game_id]


def sha256_of_file(path: Path) -> str:
    """The SHA-256 of a file's bytes on disk, as 64 hexadecimal characters."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fingerprint_of(lines) -> str:
    """The fingerprint of a hashed file list (specification 3.4).

    lines: (path from src/methods with forward slashes, sha256) pairs, for example
        [('E_002/RECUR_MEAN_ALL_V1/VARIANT.json', 'ab12...'), ('_shared/recurrence_gaps_v1.py', 'cd34...')].
    Returns the SHA-256 of the lines '<path><TAB><sha256><LF>', sorted by path.
    """
    text = ''.join(f'{path}\t{digest}\n' for path, digest in sorted(lines))
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def _check_declaration(declaration: object, family: str, variant: str, where: Path) -> dict:
    """Check the parsed VARIANT.json against the specification and the folder names; return it.

    Refuses (VariantRefused) wrong keys, identifiers that differ from the folder names, an unknown game or view,
    a minimum that is not a whole number of 1 or more for each game, or a file list without method.py.
    """
    if type(declaration) is not dict or set(declaration) != set(DECLARATION_KEYS):
        raise VariantRefused(f'{where}: the declaration must hold exactly the keys {", ".join(DECLARATION_KEYS)}. '
                             f'Correct the file.')
    if declaration['family'] != family or declaration['variant'] != variant:
        raise VariantRefused(f'{where}: it names {declaration["family"]}/{declaration["variant"]} but lies in '
                             f'{family}/{variant}. The identifiers must equal the folder names.')
    for key in ('title', 'description'):
        if type(declaration[key]) is not str or not declaration[key].strip():
            raise VariantRefused(f'{where}: "{key}" must be a line of text.')
    games, minimum = declaration['games'], declaration['minimum_earlier_draws']
    if type(games) is not list or not games or len(set(games)) != len(games) or type(minimum) is not dict \
            or set(minimum) != set(games):
        raise VariantRefused(f'{where}: "games" must list each supported game once, and "minimum_earlier_draws" '
                             f'must give a number for exactly those games.')
    for game_id in games:
        try:
            get_profile(game_id)
        except ValueError:
            raise VariantRefused(f'{where}: "{game_id}" is not a game this project knows.') from None
        if type(minimum[game_id]) is not int or minimum[game_id] < 1:
            raise VariantRefused(f'{where}: minimum_earlier_draws for {game_id} must be a whole number of 1 or more.')
    if declaration['observation_view'] not in OBSERVATION_VIEWS:
        raise VariantRefused(f'{where}: observation_view must be one of {", ".join(OBSERVATION_VIEWS)}.')
    for key in ('files', 'helpers'):
        names = declaration[key]
        if type(names) is not list or any(type(n) is not str or not n or '\\' in n or n.startswith('/')
                                          or '..' in n.split('/') for n in names) or len(set(names)) != len(names):
            raise VariantRefused(f'{where}: "{key}" must be a list of different file paths with forward slashes.')
    if 'method.py' not in declaration['files'] or any('/' in n for n in declaration['files']):
        raise VariantRefused(f'{where}: "files" must list the folder\'s own files by name, method.py among them.')
    return declaration


def read_variant(methods_root: Path, family: str, variant: str) -> Variant:
    """Read and check one variant folder and compute its fingerprint.

    methods_root: <tree>/src/methods.  family, variant: the folder names.
    Returns the Variant.
    Refuses (VariantRefused): no declaration or one that is not JSON; a declaration that fails its checks; a
    listed file or helper that is missing; and any other file in the folder ("not on the declaration's list:
    remove it or list it"), the status file, the marker and Python's cache apart.
    """
    folder = methods_root / family / variant
    declaration_path = folder / DECLARATION_NAME
    if not declaration_path.is_file():
        raise VariantRefused(f'{folder}: no {DECLARATION_NAME}. Every variant folder holds its declaration.')
    try:
        declaration = json.loads(declaration_path.read_text(encoding='utf-8'))
    except (ValueError, UnicodeDecodeError) as error:
        raise VariantRefused(f'{declaration_path}: not readable JSON ({error}). Correct the file.') from None
    _check_declaration(declaration, family, variant, declaration_path)
    listed = {DECLARATION_NAME, *declaration['files']}
    for item in sorted(folder.iterdir()):
        if item.name == '__pycache__' or item.suffix in ('.pyc', '.pyo'):
            continue
        if item.name in (STATUS_FILE_NAME, MARKER_FILE_NAME):
            continue
        if item.name not in listed or not item.is_file():
            raise VariantRefused(f'{item}: not on the declaration\'s list: remove it or list it in '
                                 f'{DECLARATION_NAME}.')
    lines = []
    for name in sorted(listed):
        path = folder / name
        if not path.is_file():
            raise VariantRefused(f'{path}: listed in {DECLARATION_NAME} but missing.')
        lines.append((f'{family}/{variant}/{name}', sha256_of_file(path)))
    for helper in declaration['helpers']:
        path = methods_root / helper
        if not path.is_file():
            raise VariantRefused(f'{path}: a helper listed in {declaration_path} is missing.')
        lines.append((helper, sha256_of_file(path)))
    lines = tuple(sorted(lines))
    return Variant(family=family, variant=variant, folder=folder, declaration=declaration,
                   fingerprint=fingerprint_of(lines), fingerprint_lines=lines)


def find_variants(methods_root: Path) -> tuple:
    """Find every variant folder of a tree.

    methods_root: <tree>/src/methods.
    Returns (variants, refused): the valid Variants in (family, variant) order, and a list of
    (identity, reason) for each folder that holds a declaration or a method.py but fails a check, for example
        ((Variant('E_002', 'RECUR_MEAN_ALL_V1', ...), ...), [('E_901/BROKEN_V1', '...not on the declaration...')]).
    A folder under a family folder with neither file (for example __pycache__) is not a variant and is skipped.
    """
    variants, refused = [], []
    for family_folder in sorted(p for p in methods_root.iterdir() if p.is_dir() and FAMILY_FOLDER_PATTERN.match(p.name)):
        for folder in sorted(p for p in family_folder.iterdir() if p.is_dir()):
            if not ((folder / DECLARATION_NAME).exists() or (folder / 'method.py').exists()):
                continue
            identity = f'{family_folder.name}/{folder.name}'
            if not VARIANT_FOLDER_PATTERN.match(folder.name):
                refused.append((identity, f'{folder}: a variant folder\'s name is capitals, digits and underscores.'))
                continue
            try:
                variants.append(read_variant(methods_root, family_folder.name, folder.name))
            except VariantRefused as refusal:
                refused.append((identity, str(refusal)))
    return tuple(variants), refused


def load_method(variant: Variant):
    """Import a variant's method.py and check that it is this tree's own file.

    variant: the Variant.
    Returns the imported module, for example <module 'E_002.RECUR_MEAN_ALL_V1.method'>.
    Refuses (VariantRefused) if Python imports the module from another place than the variant's folder (another
    tree's code is on the import path), or if compute() or verify() is missing. An error inside the module's own
    imports is not caught here: it is an environmental fault and stops the job.
    """
    module = importlib.import_module(f'{variant.family}.{variant.variant}.method')
    expected = (variant.folder / 'method.py').resolve()
    if Path(module.__file__).resolve() != expected:
        raise VariantRefused(f'{variant.identity}: Python imported method.py from {module.__file__}, not from '
                             f'{expected}. Another tree\'s code is on the import path: start the job with this '
                             f'tree\'s own launcher.')
    for name in METHOD_FUNCTIONS:
        if not callable(getattr(module, name, None)):
            raise VariantRefused(f'{expected}: no {name}() function. Every method.py provides '
                                 f'{" and ".join(METHOD_FUNCTIONS)}.')
    return module
