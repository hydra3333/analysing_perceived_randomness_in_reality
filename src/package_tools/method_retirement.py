"""CODE-3: retiring a method revision into the revision-labelled archive (E2R-R54 to R56, T15; owner decision D-5).

Package-time tooling, written by the Claude web chat (CODE-3 and E_1 revision 2 design v0.1r2, owner-ratified
31 October 2026). Package builders and tests use it; no runner imports it, and it never imports or runs anything
under archive/. It reads and writes files only under the repository root it is given.

  retire()          copy a revision's unchanged bytes into archive/methods/E_<nnn>/r<k>/, keeping their paths
                    relative to src/methods/, write the README, and remove the paths the successor drops
  readme_text()     the README of E2R-R54: the method and revision, the dates, the previous paths, the shared
                    helpers with their revisions; no Git commit ID and no file hash
  check_archive()   E2R-R55's package-time checks: exact file list, bytes equal to the pre-install baseline,
                    lower-case unique revision folders, no package marker above the revision's own files (a layout
                    rule, not an import barrier), and README helper references that resolve
  archive_execution_findings()   E2R-R56's static check over Python files: no import of archive, no dynamic
                    loading or path change that names it, and no expression that builds a path into it
"""
from __future__ import annotations

import ast
import re
from collections.abc import Iterable, Mapping
from pathlib import Path, PurePosixPath

ARCHIVE_METHODS = PurePosixPath('archive') / 'methods'
README = 'README.md'
HELPER_LINE = re.compile(r'^- `(_common/[A-Za-z0-9_]+\.py)` \(revision (\d+)\)', re.M)
DYNAMIC_CALLS = frozenset({'import_module', '__import__', 'run_path', 'run_module', 'exec', 'compile',
                           'spec_from_file_location', 'SourceFileLoader', 'module_from_spec', 'exec_module'})


def method_folder(method_id: str) -> str:
    """E_1 -> E_001 (E2R-R53's zero-padding rule)."""
    if re.fullmatch(r'E_[1-9][0-9]{0,2}', method_id) is None:
        raise ValueError(f'not a method ID: {method_id!r}')
    return f'E_{int(method_id[2:]):03d}'


def archive_dir(method_id: str, revision: str) -> PurePosixPath:
    if re.fullmatch(r'[1-9][0-9]*', revision) is None:
        raise ValueError(f'not a revision: {revision!r}')
    return ARCHIVE_METHODS / method_folder(method_id) / f'r{revision}'


def _rel(path: str) -> PurePosixPath:
    p = PurePosixPath(path)
    if p.is_absolute() or '..' in p.parts or not p.parts or p.suffix == '' and not p.name:
        raise ValueError(f'not a relative file path: {path!r}')
    return p


def readme_text(*, method_id: str, method_name: str, revision: str, successor_revision: str, variants: Iterable[str],
                games: Iterable[str], prepared: str, previous_paths: Iterable[str], helpers: Mapping[str, str], reason: str,
                replay_note: str) -> str:
    """The archive README (ASCII). `helpers` maps a path under src/methods/ (for example
    `_common/canonical_encoding.py`) to its revision. No commit ID and no hash (E2R-R54)."""
    lines = [f'# {method_id} revision {revision} (archived)', '',
             f'- **Method:** {method_id}, {method_name}, revision {revision}; variants: '
             + ', '.join(f'`{v}`' for v in variants) + '; games: ' + ', '.join(games) + '.',
             f'- **Prepared:** {prepared} (the date this archive was prepared by its package).',
             '- **Retired:** when the owner installs that package. The installation date and commit are recorded in '
             'the ratification register, not here.',
             f'- **Superseded by:** revision {successor_revision}.',
             f'- **Why retired:** {reason}', '',
             '## Previous paths under `src/methods/`', '']
    lines += [f'- `{p}`' for p in previous_paths]
    lines += ['', '## Shared helpers used', '']
    lines += [f'- `{p}` (revision {r})' for p, r in helpers.items()]
    lines += ['', '## Replay', '', replay_note, '']
    text = '\n'.join(lines)
    if not text.isascii():
        raise ValueError('the README must be ASCII')
    return text


def retire(repo: Path, method_id: str, revision: str, files: Iterable[str], readme: str, *,
           drop: Iterable[str] = ()) -> list[str]:
    """Copy each file (a path relative to src/methods/) into the archive unchanged, write the README, then delete
    the `drop` paths from src/methods/ (those the successor does not reuse). Refuses if the archive folder exists.
    Returns the archive's paths relative to the repository root."""
    repo = Path(repo)
    files = [_rel(f) for f in files]
    drop = [_rel(f) for f in drop]
    if not set(drop) <= set(files):
        raise ValueError('a dropped path must be one of the archived files')
    adir = repo / archive_dir(method_id, revision)
    if adir.exists():
        raise ValueError(f'{adir} already exists')
    for f in files:                       # every input is checked before anything is written (EX_093 O01)
        src = repo / 'src' / 'methods' / f
        if src.is_symlink() or not src.is_file():
            raise ValueError(f'not a regular file: {src}')
    if len(set(files)) != len(files):
        raise ValueError('a file is listed twice')
    written = []
    for f in files:
        src = repo / 'src' / 'methods' / f
        dst = adir / f
        dst.parent.mkdir(parents=True, exist_ok=True)
        with dst.open('xb') as fh:
            fh.write(src.read_bytes())
        written.append((archive_dir(method_id, revision) / f).as_posix())
    with (adir / README).open('xb') as fh:
        fh.write(readme.encode('ascii'))
    written.append((archive_dir(method_id, revision) / README).as_posix())
    for f in drop:
        (repo / 'src' / 'methods' / f).unlink()
    return written


def check_archive(repo: Path, method_id: str, revision: str, files: Iterable[str],
                  baseline: Mapping[str, bytes], *, normalise_eol: bool = False) -> list[str]:
    """E2R-R55's checks. `baseline` maps each archived path (relative to src/methods/) to its pre-install bytes.
    Returns a list of problems (empty if the archive is right)."""
    repo = Path(repo)
    problems = []
    rel_dir = archive_dir(method_id, revision)
    adir = repo / rel_dir
    want = {_rel(f).as_posix() for f in files} | {README}
    if not adir.is_dir():
        return [f'{rel_dir} is missing']
    have = {p.relative_to(adir).as_posix() for p in adir.rglob('*') if p.is_file()}
    if have != want:
        problems.append(f'{rel_dir}: file list differs: extra {sorted(have - want)}, missing {sorted(want - have)}')
    for f in sorted(want - {README}):
        p = adir / f
        if not p.is_file():
            continue
        got, exp = p.read_bytes(), baseline.get(f)
        if normalise_eol and exp is not None:
            got, exp = got.replace(b'\r\n', b'\n'), exp.replace(b'\r\n', b'\n')
        if exp is None or got != exp:
            problems.append(f'{rel_dir}/{f}: bytes differ from the pre-install baseline')
    # Revision folders: lower-case r<k>, unique ignoring case; no package marker above the revision's own files.
    mroot = repo / ARCHIVE_METHODS / method_folder(method_id)
    names = [d.name for d in mroot.iterdir() if d.is_dir()] if mroot.is_dir() else []
    for n in names:
        if re.fullmatch(r'r[1-9][0-9]*', n) is None:
            problems.append(f'{mroot.relative_to(repo).as_posix()}/{n}: not a lower-case revision folder')
    if len({n.lower() for n in names}) != len(names):
        problems.append(f'{mroot.relative_to(repo).as_posix()}: revision folders differ only in case')
    for level in (repo / 'archive', repo / ARCHIVE_METHODS, mroot, adir):
        if (level / '__init__.py').exists():
            problems.append(f'{level.relative_to(repo).as_posix()}/__init__.py: the archive layout has no package '
                            'marker (a layout rule; namespace packages mean it does not by itself prevent an import)')
    readme = adir / README
    if readme.is_file():
        text = readme.read_bytes()
        if not text.isascii():
            problems.append(f'{rel_dir}/{README}: not ASCII')
        text = text.decode('ascii', 'replace').replace('\r\n', '\n')
        for needle in (f'# {method_id} revision {revision} (archived)', '**Prepared:**', '**Retired:**',
                       '## Previous paths under `src/methods/`', '## Shared helpers used', '## Replay'):
            if needle not in text:
                problems.append(f'{rel_dir}/{README}: lacks {needle!r}')
        if re.search(r'\b[0-9a-f]{40}\b|\b[0-9a-f]{64}\b', text):
            problems.append(f'{rel_dir}/{README}: holds a commit ID or a hash (E2R-R54)')
        helpers = HELPER_LINE.findall(text)
        if not helpers:
            problems.append(f'{rel_dir}/{README}: lists no shared helper')
        for path, rev in helpers:
            name = PurePosixPath(path).stem
            current = repo / 'src' / 'methods' / path
            archived = repo / 'archive' / 'common' / name / f'r{rev}'
            if not (current.is_file() or archived.is_dir()):
                problems.append(f'{rel_dir}/{README}: helper {path} revision {rev} resolves to nothing')
        for f in sorted(want - {README}):
            if f'- `{f}`' not in text:
                problems.append(f'{rel_dir}/{README}: does not list the previous path {f}')
    else:
        problems.append(f'{rel_dir}/{README} is missing')
    return problems


PATH_CALLS = frozenset({'Path', 'PurePath', 'PurePosixPath', 'PureWindowsPath', 'PosixPath', 'WindowsPath'})
UNKNOWN = '\x00'          # a path component the static check cannot know (a variable, a call result)


def _parts(node: ast.AST) -> list[str]:
    """The path or module-name components an expression spells, as far as constants show them; UNKNOWN for a part
    that is not a constant. Folds strings (split at '/', '\\' and '.'), `a / b`, `a + b`, Path(...)-style calls,
    `x.joinpath(...)`, `os.path.join(...)`, `sep.join([...])`, lists, tuples and starred arguments."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return [x for x in re.split(r'[\\/.]', node.value)]
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        return _parts(node.left) + _parts(node.right)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return _parts(node.left) + _parts(node.right)
    if isinstance(node, (ast.List, ast.Tuple)):
        return [x for e in node.elts for x in _parts(e)]
    if isinstance(node, ast.Starred):
        return _parts(node.value)
    if isinstance(node, ast.Call):
        fn = node.func
        name = fn.attr if isinstance(fn, ast.Attribute) else getattr(fn, 'id', '')
        args = [x for a in node.args for x in _parts(a)]
        if name in PATH_CALLS or ast.unparse(fn).endswith('path.join') or name == 'join':
            return args
        if name == 'joinpath' and isinstance(fn, ast.Attribute):
            return _parts(fn.value) + args
    return [UNKNOWN]


def _spells_archive(parts: list[str], *, strict: bool) -> bool:
    """`archive` followed (after any empty parts) by `methods` or `common`; when `strict`, any part `archive`."""
    words = [p for p in parts if p != '']
    for k, w in enumerate(words):
        if w == 'archive':
            if strict or (k + 1 < len(words) and words[k + 1] in ('methods', 'common')):
                return True
    return False


def _is_path_construction(node: ast.AST) -> bool:
    """A Path-like call, `x.joinpath(...)`, `os.path.join(...)` or a `/` join: an expression that builds a path."""
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        return True
    if isinstance(node, ast.Call):
        fn = node.func
        name = fn.attr if isinstance(fn, ast.Attribute) else getattr(fn, 'id', '')
        return name in PATH_CALLS or name == 'joinpath' or ast.unparse(fn).endswith('path.join')
    return False


def _names_archive(node: ast.AST, *, strict: bool) -> bool:
    """True if any expression inside `node` spells the project's archive: `archive/methods` or `archive/common`
    however it is built (a string with either slash or dots, `Path('archive') / 'methods'`,
    `Path('archive', 'methods')`, `Path('archive').joinpath('methods')`, `os.path.join('archive', 'methods')`,
    `'archive' + '/methods'`, a list of parts); and, when `strict` (the arguments of a loader, exec or path change),
    any expression with an `archive` component at all. The bare word "archive" in ordinary text is not a path to
    the archive, and is not flagged outside those arguments; but any path construction (`Path(...)`, `joinpath`,
    `os.path.join`, `/`) with an `archive` component is (EX_095 O02).

    Scope: this folds constants within one expression. It is not data-flow analysis: a path assembled from
    variables that hold only non-archive-looking parts, or a computed string, is not traced across statements. The
    check is E2R-R56's normal-workflow control, not a security boundary."""
    for n in ast.walk(node):
        if isinstance(n, (ast.Constant, ast.BinOp, ast.Call, ast.List, ast.Tuple)) and \
                _spells_archive(_parts(n), strict=strict):
            return True
        # EX_095 O02: a path construction with an `archive` component at all, so that a root such as
        # `root = Path("archive")` is found on its own line, whatever later joins it to.
        if _is_path_construction(n) and _spells_archive(_parts(n), strict=True):
            return True
    return False


def archive_execution_findings(paths: Iterable[Path], *, allowed: Iterable[Path] = ()) -> list[str]:
    """E2R-R56's static check. For each Python file: no `import archive...`; no dynamic import, `runpy`, `exec`,
    `compile`, loader or `sys.path` change whose arguments name `archive`; and, outside the `allowed` files (those
    that compare archived bytes), no expression that spells the archive's `methods` or `common` folders at all, so
    that no code can build a path into the archive to load from (EX_093 B01).

    This, with the runtime check in the tests, is the boundary. Leaving out `__init__.py` files is a layout rule
    only: under Python 3's namespace packages (PEP 420) a folder without one can still be imported when its parent
    is on the import path, as the repository root is when tests run from it."""
    allowed = {Path(p).resolve() for p in allowed}
    out = []
    for f in paths:
        f = Path(f)
        tree = ast.parse(f.read_text(encoding='utf-8'), filename=str(f))
        for n in ast.walk(tree):
            mods = [n.module or ''] if isinstance(n, ast.ImportFrom) else (
                [a.name for a in n.names] if isinstance(n, ast.Import) else [])
            for m in mods:
                if m == 'archive' or m.startswith('archive.'):
                    out.append(f'{f.name}:{n.lineno}: imports {m}')
            if isinstance(n, ast.Call):
                fn = n.func
                name = fn.attr if isinstance(fn, ast.Attribute) else getattr(fn, 'id', '')
                target = ast.unparse(fn)
                is_path_change = target.startswith('sys.path.') or target in ('site.addsitedir',)
                if (name in DYNAMIC_CALLS or is_path_change) and any(_names_archive(a, strict=True)
                                                          for a in [*n.args, *[k.value for k in n.keywords]]):
                    out.append(f'{f.name}:{n.lineno}: {target}() names an archive path')
        if f.resolve() not in allowed and _names_archive(tree, strict=False):
            out.append(f'{f.name}: names an archive path but is not an allowed byte-comparison file')
    return out
