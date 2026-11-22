"""Assemble EX_275: the install package as a deterministic ZIP, the message with its two hash tables, and the outer ZIP.

What this file is for
    It turns the built package folder and the message body (EX_275_body.md, beside this file) into the files of
    the exchange protocol (exchange/README.md v0.6, "Message plus a code package"): the package ZIP with its member
    list, EX_275_Claude.md (US-ASCII, CRLF) with every hash computed here and never typed, and EX_275_Claude.zip
    holding the three flat. It is a workspace tool; nothing in the project imports it.

Usage:  python assemble_ex275.py <repository clone> <built package folder> <out folder> <base commit>
"""
import hashlib
import pathlib
import subprocess
import sys
import zipfile

MESSAGE_NAME = 'EX_275_Claude.md'
# The fixed time stamp the project's deterministic ZIPs use (exchange/EX_019_Claude/make_zip.py).
ZIP_TIME = (2026, 10, 28, 20, 0, 0)
# The repository files the message names, for its second table.
REPOSITORY_FILES = (
    'exchange/CLAUDE_WEB_TOOLS/step1/STEP1_PACKAGE_NOTE_v0_2.md',
    'exchange/CLAUDE_WEB_TOOLS/step1/make_step1_layout.py', 'exchange/CLAUDE_WEB_TOOLS/step1/build_step1_pkg.py',
    'exchange/CLAUDE_WEB_TOOLS/step1/templates/method_table.py',
    'exchange/CLAUDE_WEB_TOOLS/step1/templates/variant_method.py.template',
    'exchange/CLAUDE_WEB_TOOLS/step1/check_layout_equivalence.py', 'exchange/CLAUDE_WEB_TOOLS/step1/run_suite.py',
    'exchange/CLAUDE_WEB_TOOLS/step1/compare_suite_reports.py', 'exchange/CLAUDE_WEB_TOOLS/step1/rehearse_install.sh',
    'exchange/CLAUDE_WEB_TOOLS/step1/evidence/STEP1_LAYOUT_CHANGE.diff',
    'exchange/CLAUDE_WEB_TOOLS/step1/evidence/STEP1_CHANGED_FILES.txt',
    'exchange/CLAUDE_WEB_TOOLS/step1/evidence/SUITE_COMPARISON.txt',
    'exchange/CLAUDE_WEB_TOOLS/step1/evidence/EQUIVALENCE_CLOUD_MOVED_TREE.log',
    'exchange/CLAUDE_WEB_TOOLS/step1/evidence/EQUIVALENCE_PLANTED_FAULTS.log',
    'exchange/CLAUDE_WEB_TOOLS/step1/evidence/INSTALL_REHEARSAL.txt',
    'exchange/CLAUDE_WEB_TOOLS/wf1/verifier_template.py',
)


def sha256_of(data: bytes) -> str:
    """Return the SHA-256 of some bytes as 64 hexadecimal characters."""
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    """Write the package ZIP, its member list, the message and the outer ZIP into the out folder; return 0."""
    repository, package, out, base = (pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve(),
                                      pathlib.Path(sys.argv[3]).resolve(), sys.argv[4])
    out.mkdir(parents=True, exist_ok=True)
    package_zip = out / f'{package.name}.zip'
    members_list = out / f'{package.name}_MEMBERS.txt'
    subprocess.run([sys.executable, '-B', str(repository / 'exchange' / 'EX_019_Claude' / 'make_zip.py'),
                    str(package), str(package_zip), str(members_list)], check=True, capture_output=True)
    members = [package_zip.name, members_list.name]
    rows = ['| Member | SHA-256 as stored | SHA-256 after CRLF->LF |', '|---|---|---|']
    for name in members:
        data = (out / name).read_bytes()
        rows.append(f'| `{name}` | `{sha256_of(data)}` | '
                    + (f'`{sha256_of(data.replace(b"\r\n", b"\n"))}` |' if name.endswith('.txt') else '(a ZIP: not applicable) |'))
    repo_rows = ['| File | SHA-256 |', '|---|---|']
    for path in REPOSITORY_FILES:
        data = (repository / path).read_bytes()
        assert b'\r' not in data, path
        repo_rows.append(f'| `{path}` | `{sha256_of(data)}` |')
    body = (pathlib.Path(__file__).resolve().parent / 'EX_275_body.md').read_text(encoding='ascii')
    text = (body.replace('@@CONTENTS@@', ', '.join([MESSAGE_NAME] + members)).replace('@@BASE@@', base)
            .replace('@@ZIPTABLE@@', '\n'.join(rows)).replace('@@REPOTABLE@@', '\n'.join(repo_rows)))
    assert '@@' not in text
    (out / MESSAGE_NAME).write_bytes(text.replace('\n', '\r\n').encode('ascii'))
    with zipfile.ZipFile(out / 'EX_275_Claude.zip', 'w') as outer:
        for name in [MESSAGE_NAME] + members:
            info = zipfile.ZipInfo(name, ZIP_TIME)
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            outer.writestr(info, (out / name).read_bytes())
    print(sha256_of((out / 'EX_275_Claude.zip').read_bytes()), 'EX_275_Claude.zip')
    return 0


if __name__ == '__main__':
    sys.exit(main())
