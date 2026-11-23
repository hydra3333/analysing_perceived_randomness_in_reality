"""Assemble EX_282: the step 2 package ZIP with its member list, the message with its hash tables, and the outer ZIP.

What this file is for
    It turns the committed package ZIP (package/STEP2_Research_Engine_v1.zip, beside this file) and the message
    body (EX_282_body.md) into the files of the exchange protocol (exchange/README.md v0.6, "Message plus a code
    package"): the package ZIP unchanged, its member list in the format of exchange/EX_019_Claude/make_zip.py,
    EX_282_Claude.md (US-ASCII, CRLF) with every hash computed here and never typed, and EX_282_Claude.zip holding
    the three flat. The table of repository files is made from the bytes Git holds for each path (`git show
    :<path>`), so a file that Git ignores or that was not added stops the assembly. Stage the files first.

Which part of the specification it carries out
    exchange/README.md v0.6 (the exchange protocol); it adds nothing to the project's code.

Which of the project's own modules it uses
    None.

What uses it
    Claude, in the cloud workspace. Usage:  python assemble_ex282.py <repository clone> <out folder> <base commit>
"""
import hashlib
import pathlib
import subprocess
import sys
import zipfile

MESSAGE_NAME = 'EX_282_Claude.md'
# The committed package ZIP that the message carries, byte for byte, and the name of its member list.
PACKAGE_ZIP = 'exchange/CLAUDE_WEB_TOOLS/step2/package/STEP2_Research_Engine_v1.zip'
MEMBERS_NAME = 'STEP2_Research_Engine_v1_MEMBERS.txt'
# The passed OV-1 kernel, whose bytes the package's copy must equal.
PASSED_KERNEL = 'exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/slice2_new/src/evaluation/ov1_numeric.py'
PACKAGE_KERNEL = 'exchange/CLAUDE_WEB_TOOLS/step2/overlay/src/research/ov1_numeric.py'
# The fixed time stamp the project's deterministic ZIPs use (exchange/EX_019_Claude/make_zip.py).
ZIP_TIME = (2026, 10, 28, 20, 0, 0)
# The repository files the message names, for its second table.
S = 'exchange/CLAUDE_WEB_TOOLS/step2/'
REPOSITORY_FILES = tuple(S + name for name in (
    'STEP2_PACKAGE_NOTE_v0_1.md', 'STEP2_BUILD_PLAN_v0_2.md', 'apply_edits.py', 'make_reader.py', 'reader_template.py',
    'build_step2_pkg.py', 'comparison_expected.md', 'rehearse_install.sh', 'mutation_check.py',
    'compare_fill_with_old_records.py', 'package/STEP2_Research_Engine_v1.zip', 'package/INSTALL_AND_RUN_SHEET.md',
    'package/INSTALL_MANIFEST_SHA256.txt', 'evidence/SUITE_COMPARISON.txt', 'evidence/suite_before/MODULES.txt',
    'evidence/suite_after/MODULES.txt', 'evidence/SUITE_AFTER_THE_FIRST_FILL.txt', 'evidence/PLANTED_FAULTS.txt',
    'evidence/INSTALL_REHEARSAL.txt', 'evidence/REAL_FILL_CLOUD.txt', 'evidence/REAL_COMPARISON_CLOUD.txt',
    'evidence/REAL_COMPARISON_SAMPLE.txt', 'evidence/CODING_PRACTICES_SCAN.txt'))


def sha256_of(data: bytes) -> str:
    """Return the SHA-256 of some bytes as 64 hexadecimal characters."""
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    """Write the package ZIP, its member list, the message and the outer ZIP into the out folder; return 0."""
    repository, out, base = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve(), sys.argv[3]
    out.mkdir(parents=True, exist_ok=True)
    package_zip = out / pathlib.Path(PACKAGE_ZIP).name
    package_zip.write_bytes((repository / PACKAGE_ZIP).read_bytes())
    lines = []
    with zipfile.ZipFile(package_zip) as z:
        for i in z.infolist():
            if not i.is_dir():
                b = z.read(i)
                lines.append(f'{sha256_of(b)}  {sha256_of(b.replace(b"\r\n", b"\n"))}  {i.filename}')
    (out / MEMBERS_NAME).write_bytes(('# ' + package_zip.name + ' members: SHA-256 as stored, SHA-256 after CRLF->LF, '
                                      'path\r\n' + '\r\n'.join(lines) + '\r\n').encode('ascii'))
    members = [package_zip.name, MEMBERS_NAME]
    rows = ['| Member | SHA-256 as stored | SHA-256 after CRLF->LF |', '|---|---|---|']
    for name in members:
        data = (out / name).read_bytes()
        rows.append(f'| `{name}` | `{sha256_of(data)}` | '
                    + (f'`{sha256_of(data.replace(b"\r\n", b"\n"))}` |' if name.endswith('.txt') else '(a ZIP: not applicable) |'))
    repo_rows = ['| File | SHA-256 |', '|---|---|']
    for path in REPOSITORY_FILES:
        data = subprocess.run(['git', '-C', str(repository), 'show', f':{path}'], check=True, capture_output=True).stdout
        assert data == (repository / path).read_bytes(), f'the staged bytes of {path} differ from the working copy'
        repo_rows.append(f'| `{path}` | `{sha256_of(data)}` |')
    kernel = sha256_of((repository / PASSED_KERNEL).read_bytes())
    assert kernel == sha256_of((repository / PACKAGE_KERNEL).read_bytes()), 'the package\'s kernel is not the passed one'
    body = (pathlib.Path(__file__).resolve().parent / 'EX_282_body.md').read_text(encoding='ascii')
    text = (body.replace('@@CONTENTS@@', ', '.join([MESSAGE_NAME] + members)).replace('@@BASE@@', base)
            .replace('@@KERNEL@@', kernel)
            .replace('@@ZIPTABLE@@', '\n'.join(rows)).replace('@@REPOTABLE@@', '\n'.join(repo_rows)))
    assert '@@' not in text
    (out / MESSAGE_NAME).write_bytes(text.replace('\n', '\r\n').encode('ascii'))
    with zipfile.ZipFile(out / 'EX_282_Claude.zip', 'w') as outer:
        for name in [MESSAGE_NAME] + members:
            info = zipfile.ZipInfo(name, ZIP_TIME)
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            outer.writestr(info, (out / name).read_bytes())
    print(sha256_of((out / 'EX_282_Claude.zip').read_bytes()), 'EX_282_Claude.zip')
    return 0


if __name__ == '__main__':
    sys.exit(main())
