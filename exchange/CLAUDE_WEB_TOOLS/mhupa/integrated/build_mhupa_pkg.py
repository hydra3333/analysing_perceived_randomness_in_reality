#!/usr/bin/env python3
"""Build the integrated MHUP-A install package (H-1 v1r10r3 delta section 7 item 2; design v0.1r6 Appendix J).

Claude web chat, 10 November 2026. A working tool (exchange/CLAUDE_WEB_TOOLS), not project code.
Usage:
  python3 -I build_mhupa_pkg.py BASE DEV OUT BASE_COMMIT DATE
    BASE         git archive of BASE_COMMIT, with source_data/, results/ and transitory_data/ removed
    DEV          BASE + the reviewed MHUP-A changes, built by build_dev_integrated.sh BASE DEV TOOLS DATE
    OUT          a new, absent folder; the package is written to OUT/MHUPA_Install_v1/
    BASE_COMMIT  the full 40-hex commit BASE was archived from
    DATE         E_1 revision 3's effective_date (C01-EFF); must equal what DEV carries
It asserts, and STOPs on any difference:
  - the changed set (new, modified, deleted) is exactly 37 + 34 + 1 = 72 paths: the reviewed overlay's 37 + 33 + 1, plus
    .gitattributes with the N1 line (owner decision D02), whose presence it also asserts;
  - the step 6 gate files, computed from the static import closure of contract_dispatch.py (every import, including
    those inside functions, followed through src/methods and src; restricted to files the package changes or adds),
    equal GATE_FILES exactly (EX_157 C02: eight changed, two new);
  - E_1 revision 3's date is DATE in both registry entries, the r2 archive README and the test that pins it;
  - the release entries derive from the two new entry_0003.json files (E_1 revision 3, both games; R-020 (a)).
It writes: repo_overlay/, PACKAGE_MANIFEST_MHUP_A.json (the one manifest: install_records.py and process_check.py
read it; the copy tool and the verifier read it), MHUPA_COPY.py, VERIFY_MHUP_A.py, RUN_MHUP_A_SUITE.py,
STAGE_PACKAGE_COMMIT.txt, STAGE_RELEASE_COMMIT.txt, INSTALL_MANIFEST_SHA256.txt, INSTALL_INSTRUCTIONS.md (DRAFT) and
BUILD_REPORT.txt. Item 3 (the verifier's `released` phase, the two-commit and barrier-order proofs) is NOT built
here: the verifier's `released` phase is a refusing stub, and the package says DRAFT throughout.
"""
import ast, hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PKG_NAME = 'MHUPA_Install_v1'
PACKAGE = 'MHUP_A'
EXPECT_COUNTS = {'new': 37, 'modified': 34, 'deleted': 1}   # 34 since N1 (.gitattributes)
GATE_FILES = sorted([
    'src/methods/_common/contract_dispatch.py', 'src/methods/_common/contract_forecast.py',
    'src/methods/_common/contract_receipts.py', 'src/methods/_common/contract_records.py',
    'src/methods/_common/contract_runner.py', 'src/methods/_common/contract_task.py',
    'src/methods/_common/contract_vocab.py', 'src/methods/_common/game_draws_reader.py',
    'src/methods/_common/master_versions.py', 'src/methods/_common/owner_records.py'])
GATE_ROOT_MODULE = 'src/methods/_common/contract_dispatch.py'
TOOLS_IN_OVERLAY = ['src/package_tools/process_check.py', 'src/package_tools/install_records.py',
                    'src/methods/_common/release_records.py']
BARRIERS = {'E': 'src/methods/E_001/IN_DEVELOPMENT.txt',
            'P': 'src/methods/_common/contract_data/INSTALL_IN_PROGRESS.txt',
            'U': 'source_data/.results_master.lock'}
RECORDS = 'src/methods/_common/contract_data/install_records'
N1_LINE = RECORDS + '/** -text'
INSTALL_RECORD = f'{RECORDS}/INSTALL_{PACKAGE}_V1.json'
RELEASE_RECORD = f'{RECORDS}/RELEASE_{PACKAGE}_V1.json'
E1R3_ENTRIES = ['src/methods/_common/contract_data/registry/POWERBALL/E_1/FULL_HISTORY_RAW_COUNTS_V1/entry_0003.json',
                'src/methods/_common/contract_data/registry/OZLOTTO/E_1/FULL_HISTORY_RAW_COUNTS_V1/entry_0003.json']
SOURCE_ROOTS = ['src', 'src/methods']        # the order of PYTHONPATH (src;src/methods;tests); resolve() refuses a
                                             # module name found in both, so the order cannot matter


def die(msg):
    print('BUILD STOP:', msg)
    sys.exit(1)


def need(cond, msg):
    if not cond:
        die(msg)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def norm(b):
    return b.replace(b'\r\n', b'\n')


def files(root):
    return {p.relative_to(root).as_posix() for p in root.rglob('*')
            if p.is_file() and '__pycache__' not in p.parts}


def changed_sets(base, dev):
    fb, fd = files(base), files(dev)
    new = sorted(fd - fb)
    deleted = sorted(fb - fd)
    modified = sorted(p for p in fd & fb if (base / p).read_bytes() != (dev / p).read_bytes())
    return new, modified, deleted


# ------------------------------------------------------------------ the gate closure (EX_157 C02)

def resolve(dev, name):
    """A dotted module name -> its repository path under src/methods or src, or None (stdlib, third party)."""
    hits = []
    for root in SOURCE_ROOTS:
        stem = dev / root / Path(*name.split('.'))
        for cand in (stem.with_suffix('.py'), stem / '__init__.py'):
            if cand.is_file():
                hits.append(cand.relative_to(dev).as_posix())
    hits = sorted(set(hits))
    need(len(hits) <= 1, f'module {name} resolves to more than one file: {hits}')
    return hits[0] if hits else None


def module_name(rel):
    for root in sorted(SOURCE_ROOTS, key=len, reverse=True):      # src/methods/x is module x, not methods.x
        if rel.startswith(root + '/'):
            parts = rel[len(root) + 1:-3].split('/')
            return '.'.join(parts[:-1] if parts[-1] == '__init__' else parts)
    raise ValueError(rel)


def imports_of(dev, rel):
    tree = ast.parse((dev / rel).read_text(encoding='utf-8'), filename=rel)
    name = module_name(rel)
    if rel.endswith('__init__.py'):
        pkg = name                                          # a package's own relative imports start from itself
    else:
        pkg = name.rsplit('.', 1)[0] if '.' in name else ''
    out = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                parts = a.name.split('.')
                for i in range(1, len(parts) + 1):          # importing a.b imports a and a.b
                    out.add('.'.join(parts[:i]))
        elif isinstance(n, ast.ImportFrom):
            if n.level:
                base = pkg.split('.') if pkg else []
                base = base[:len(base) - (n.level - 1)] if n.level > 1 else base
                mod = '.'.join(base + ([n.module] if n.module else []))
            else:
                mod = n.module
            if mod:
                parts = mod.split('.')
                for i in range(1, len(parts) + 1):
                    out.add('.'.join(parts[:i]))
            for a in n.names:
                out.add(f'{mod}.{a.name}' if mod else a.name)  # `from pkg import module` imports a module
    return out


def gate_closure(dev, changed):
    seen, todo = set(), [GATE_ROOT_MODULE]
    while todo:
        rel = todo.pop()
        if rel in seen:
            continue
        seen.add(rel)
        for name in imports_of(dev, rel):
            r = resolve(dev, name)
            if r:
                todo.append(r)
    return sorted(seen), sorted(r for r in seen if r in changed)


# ------------------------------------------------------------------ the test counts (from the tools, never by hand)

def test_counts(dev, python):
    mods = sorted(p[:-3].replace('/', '.') for p in files(dev) if re.fullmatch(r'tests/test_[^/]+\.py', p))
    code = ('import sys, unittest\n'
            'for m in sys.argv[1:]:\n'
            '    print(m, unittest.defaultTestLoader.loadTestsFromName(m).countTestCases())\n')
    env = {k: v for k, v in os.environ.items() if k != 'PYTHONPATH'}
    env['PYTHONPATH'] = os.pathsep.join(str(dev / p) for p in ('src', 'src/methods', 'tests'))
    r = subprocess.run([python, '-B', '-c', code, *mods], cwd=dev, env=env, capture_output=True, text=True)
    need(r.returncode == 0, 'counting tests failed (loading only, nothing run):\n' + r.stderr[-2000:])
    counts = [(ln.split()[0], int(ln.split()[1])) for ln in r.stdout.split('\n') if ln.strip()]
    need([m for m, _ in counts] == mods, 'test counting returned a different module list')
    need(all(n > 0 for _, n in counts), 'a test module with no tests: ' + repr([m for m, n in counts if n == 0]))
    return counts


# ------------------------------------------------------------------ the build

def main():
    if len(sys.argv) != 6:
        die(__doc__)
    base, dev, out = (Path(a).resolve() for a in sys.argv[1:4])
    base_commit, date = sys.argv[4], sys.argv[5]
    need(re.fullmatch(r'[0-9a-f]{40}', base_commit), 'BASE_COMMIT must be a full 40-hex commit id')
    need(re.fullmatch(r'\d{4}-\d{2}-\d{2}', date), 'DATE must be YYYY-MM-DD')
    for d in ('source_data', 'results', 'transitory_data'):
        need(not (base / d).exists() and not (dev / d).exists(), f'{d}/ must not exist in BASE or DEV')
    need(not out.exists(), f'OUT must not exist: {out}')
    pkg = out / PKG_NAME

    new, modified, deleted = changed_sets(base, dev)
    got = {'new': len(new), 'modified': len(modified), 'deleted': len(deleted)}
    need(got == EXPECT_COUNTS, f'changed set {got} differs from the reviewed shape {EXPECT_COUNTS}')
    need(deleted == ['src/results_master_v0_1.py'], f'unexpected deletion set {deleted}')
    need('.gitattributes' in modified and N1_LINE in (dev / '.gitattributes').read_text(encoding='ascii').splitlines(),
         '.gitattributes does not carry the N1 line')
    for p in [INSTALL_RECORD, RELEASE_RECORD, *BARRIERS.values()]:
        need(p not in new and p not in modified and not (dev / p).exists(), f'{p} must not be a package file')
    for p in new + modified:
        need(not (dev / p).is_symlink(), f'symlink in DEV: {p}')
        b = (dev / p).read_bytes()
        try:
            b.decode('utf-8')
        except UnicodeDecodeError:
            die(f'not UTF-8 text: {p}')
    changed = set(new) | set(modified)
    for t in TOOLS_IN_OVERLAY:
        need(t in changed, f'{t} is not a package file')

    closure, gate = gate_closure(dev, changed)
    need(gate == GATE_FILES, 'the computed step 6 gate files differ from GATE_FILES:\n  computed ' + repr(gate) +
         '\n  expected ' + repr(GATE_FILES))
    rest = sorted(changed - set(gate))

    entries = []
    for rel in E1R3_ENTRIES:
        need(rel in new, f'{rel} is not a new package file')
        e = json.loads((dev / rel).read_text(encoding='ascii'))
        need(e.get('effective_date') == date, f'{rel}: effective_date {e.get("effective_date")} is not DATE {date}')
        need((e['method_id'], e['method_revision']) == ('E_1', '3'), f'{rel}: not E_1 revision 3')
        entries.append({'game_id': e['game_id'], 'method_id': e['method_id'], 'method_revision': e['method_revision'],
                        'variant_id': e['variant_id']})
    need(sorted(x['game_id'] for x in entries) == ['OZLOTTO', 'POWERBALL'], 'E_1 r3 entries are not one per game')
    added = sorted(p for p in new if re.fullmatch(r'src/methods/_common/contract_data/registry/.+/entry_\d+\.json', p))
    need(added == sorted(E1R3_ENTRIES), f'registry entries added are not exactly E_1 r3 two entries: {added}')
    need(f'- **Prepared:** {date} ' in (dev / 'archive/methods/E_001/r2/README.md').read_text(encoding='utf-8'),
         'archive/methods/E_001/r2/README.md does not carry DATE')
    need(f"self.assertEqual(chain[2]['effective_date'], '{date}')" in
         (dev / 'tests/test_e1r3_revision3.py').read_text(encoding='utf-8'), 'the pinned test does not carry DATE')

    counts = test_counts(dev, sys.executable)

    # ---- write
    ov = pkg / 'repo_overlay'
    for p in sorted(changed):
        (ov / p).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(dev / p, ov / p)
    lfsha = lambda root, p: sha(norm((root / p).read_bytes()))
    manifest = {
        'schema': 'MHUP_PACKAGE_MANIFEST_V1',
        'package': PACKAGE,
        'package_folder': PKG_NAME,
        'status': 'DRAFT (item 2 scaffold; not for installation)',
        'base_commit': base_commit,
        'e1_r3_effective_date': date,
        'new': {p: lfsha(dev, p) for p in new},
        'modified': {p: [lfsha(base, p), lfsha(dev, p)] for p in modified},
        'deleted': {p: lfsha(base, p) for p in deleted},
        'gate_files': gate,
        'rest_files': rest,
        'release_entries': entries,
        'retires': [],
        'registry_entries_added': added,
        'tool_sha256': {t: lfsha(dev, t) for t in TOOLS_IN_OVERLAY},
        'barriers': BARRIERS,
        'install_record': INSTALL_RECORD,
        'release_record': RELEASE_RECORD,
        'note': ('Hashes are SHA-256 of LF-normalised bytes, equal to the Git blobs. release_entries, retires and '
                 'registry_entries_added are read by src/package_tools/install_records.py and process_check.py.'),
    }
    pkg.mkdir(parents=True, exist_ok=True)
    mbytes = (json.dumps(manifest, indent=1, sort_keys=True, ensure_ascii=True) + '\n').encode('ascii')
    (pkg / 'PACKAGE_MANIFEST_MHUP_A.json').write_bytes(mbytes)
    msha = sha(mbytes)

    copy_src = (HERE / 'mhupa_copy_tool.py').read_bytes()
    (pkg / 'MHUPA_COPY.py').write_bytes(copy_src)
    ver = (HERE / 'mhupa_verifier_template.py').read_text(encoding='ascii')
    ver = ver.replace('@@MANIFEST_SHA256@@', msha).replace('@@COPY_SHA256@@', sha(copy_src))
    need('@@' not in ver, 'unfilled placeholder in the verifier')
    (pkg / 'VERIFY_MHUP_A.py').write_bytes(ver.encode('ascii'))
    suite = (HERE / 'mhupa_suite_template.py').read_text(encoding='ascii')
    suite = suite.replace('@@EXPECTED@@', '\n'.join(f'    ({m!r}, {n}),' for m, n in counts))
    need('@@' not in suite, 'unfilled placeholder in the suite runner')
    (pkg / 'RUN_MHUP_A_SUITE.py').write_bytes(suite.encode('ascii'))
    stage1 = sorted([*new, *modified, *deleted, INSTALL_RECORD])
    (pkg / 'STAGE_PACKAGE_COMMIT.txt').write_bytes(('\n'.join(stage1) + '\n').encode('ascii'))
    (pkg / 'STAGE_RELEASE_COMMIT.txt').write_bytes((RELEASE_RECORD + '\n').encode('ascii'))
    lines = [f'A {manifest["new"][p]}  {p}' for p in new] + [f'M {manifest["modified"][p][1]}  {p}' for p in modified] + \
            [f'D {manifest["deleted"][p]}  {p}' for p in deleted]
    (pkg / 'INSTALL_MANIFEST_SHA256.txt').write_bytes(('\n'.join(sorted(lines, key=lambda s: s[67:])) + '\n').encode('ascii'))

    total = sum(n for _, n in counts)
    ins = (HERE / 'mhupa_install_instructions_template.md').read_text(encoding='ascii')
    fill = {'BASE': base_commit, 'BASE7': base_commit[:7], 'DATE': date, 'N_NEW': str(len(new)),
            'N_MOD': str(len(modified)), 'N_DEL': str(len(deleted)), 'N_GATE': str(len(gate)), 'N_REST': str(len(rest)),
            'N_STAGE1': str(len(stage1)), 'N_TESTS': str(total), 'N_MODULES': str(len(counts)), 'PKG': PKG_NAME,
            'MANIFEST_SHA256': msha, 'PROCESS_CHECK_SHA256': manifest['tool_sha256'][TOOLS_IN_OVERLAY[0]]}
    for k, v in fill.items():
        ins = ins.replace(f'@@{k}@@', v)
    need('@@' not in ins, 'unfilled placeholder in the instructions: ' + repr(re.findall(r'@@\w+@@', ins)))
    (pkg / 'INSTALL_INSTRUCTIONS.md').write_bytes(ins.replace('\r\n', '\n').replace('\n', '\r\n').encode('ascii'))

    report = [f'MHUP-A integrated package build (DRAFT, item 2), base {base_commit}, E_1 r3 effective_date {date}',
              f'changed: {len(new)} new, {len(modified)} modified, {len(deleted)} deleted ({deleted[0]})',
              f'import closure of {GATE_ROOT_MODULE}: {len(closure)} project files; of them changed by the package '
              f'(the step 6 gate files): {len(gate)}', *[f'  gate  {g}' for g in gate],
              f'rest (step 8): {len(rest)} files plus the deletion',
              f'release_entries: {json.dumps(entries)}', f'registry_entries_added: {added}',
              f'tests: {total} in {len(counts)} modules (counted by the unittest loader, nothing run)',
              f'PACKAGE_MANIFEST_MHUP_A.json SHA-256 {msha}',
              *[f'{f.relative_to(pkg).as_posix()}  {sha(f.read_bytes())}' for f in sorted(pkg.iterdir()) if f.is_file()]]
    (pkg / 'BUILD_REPORT.txt').write_bytes(('\n'.join(report) + '\n').encode('ascii'))
    print('\n'.join(report))
    print(f'BUILD PASS (DRAFT, item 2): {pkg}')


if __name__ == '__main__':
    main()
