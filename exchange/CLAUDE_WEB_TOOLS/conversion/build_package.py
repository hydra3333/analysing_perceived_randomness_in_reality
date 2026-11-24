#!/usr/bin/env python3
"""Builds the conversion package FILE_FORM_Conversion_v1: the folder, its ZIP and the list of the ZIP's members.

What this file is for
    The owner installs and runs the conversion from one package, extracted to E:\\TEMP. This script assembles it
    from the working sources in this folder and from Git at HEAD: the package's own files in the standard's form
    (CRLF); the conversion list; the three programs and the rule they share; the three suite and comparison
    tools already reviewed and used at build step 2, byte for byte; the verifying script; the manifest; and the
    sheet, with every count and hash in it computed here, never typed. The ZIP is made the same way every time
    (sorted members, one fixed time), so that the same sources give the same bytes.

Which part of the project's rules it carries out
    doc/FILE_FORM_STANDARD_v0_2.md section 7 (the conversion, safely); H-1 section 8 (packages).

Which of the project's own modules it uses
    file_form (overlay/deploy/)     to_form: the package's text files are written in their form
    make_conversion_list (beside this file)     the list

What uses it
    Claude, in the cloud workspace. Usage:  python3 -I build_package.py <repository root> <revision, e.g. v1>
    It refuses (FileExistsError) to write over a package folder that exists.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'overlay', 'deploy'))
import file_form                                            # noqa: E402
import make_conversion_list                                 # noqa: E402

# The package's own programs, from this folder, delivered in the standard's form: {name in tools/: source}.
OWN_TOOLS = {'convert_to_file_form.py': 'tools/convert_to_file_form.py',
             'stage_and_refresh.py': 'tools/stage_and_refresh.py',
             'file_form.py': 'overlay/deploy/file_form.py'}
# The suite and comparison tools of the build step 2 package (reviewed in EX_294, used on the owner's PC), taken
# from Git byte for byte and delivered unchanged.
EARLIER_PACKAGE = 'exchange/EX_293_Claude/STEP2_Research_Engine_v1r3/tools/'
EARLIER_TOOLS = ('run_suite.py', 'compare_suite_reports.py', 'compare_fill_with_old_records.py')
# The two documents of the package's top folder, from package_sources/.
VERIFIER, SHEET = 'VERIFY_FILE_FORM_INSTALL.py', 'INSTALL_AND_RUN_SHEET.md'
LIST_NAME, MANIFEST_NAME = 'CONVERSION_LIST.json', 'INSTALL_MANIFEST_SHA256.txt'
# The two new test modules, whose tests are counted for the sheet; and how many tests the suite has today.
NEW_TEST_MODULES = ('tests/test_file_form.py', 'tests/test_research_file_form.py')
TESTS_TODAY = 762
# The time every member of the ZIP is given, so that the ZIP's bytes do not depend on the clock.
FIXED_ZIP_TIME = (2026, 11, 24, 0, 0, 0)


def sha(data: bytes) -> str:
    """SHA-256 of some bytes, as 64 hexadecimal characters."""
    return hashlib.sha256(data).hexdigest()


def git_bytes(root: str, path: str) -> bytes | None:
    """The bytes Git holds for a path at HEAD, or None when HEAD does not have it."""
    done = subprocess.run(['git', '-C', root, 'show', f'HEAD:{path}'], capture_output=True, check=False)
    return done.stdout if done.returncode == 0 else None


def read(path: str) -> bytes:
    """The bytes of a file of this folder."""
    with open(os.path.join(HERE, path), 'rb') as handle:
        return handle.read()


def in_its_form(path: str, data: bytes) -> bytes:
    """Some bytes in the form the standard gives a file of that name."""
    return file_form.to_form(data, file_form.form_of(path))


def main(root: str, revision: str) -> int:
    """Build the package; print each member's SHA-256 and the ZIP's; return 0."""
    name = f'FILE_FORM_Conversion_{revision}'
    out = os.path.join(HERE, 'package', name)
    os.makedirs(os.path.join(HERE, 'package'), exist_ok=True)
    os.makedirs(out)
    members = {}
    # The package's own files, as they are copied into the tree.
    delivered = make_conversion_list.overlay_files(os.path.join(HERE, 'overlay'))
    manifest = [f'# {name} installation manifest (SHA-256 of the package\'s own bytes, which are in the standard\'s form)',
                '# "N" a new file; "M" a replaced file, with the SHA-256 of the content it replaces (every CRLF read as LF);',
                '# the package deletes no tracked file']
    new_count = modified_count = 0
    for path in sorted(delivered):
        data = in_its_form(path, delivered[path])
        members[f'repo_overlay/{path}'] = data
        replaced = git_bytes(root, path)
        if replaced is None:
            manifest.append(f'N {sha(data)}  {path}')
            new_count += 1
        else:
            manifest.append(f'M {sha(data)}  {sha(replaced.replace(bytes([13, 10]), bytes([10])))}  {path}')
            modified_count += 1
    members[MANIFEST_NAME] = in_its_form('manifest.txt', ('\n'.join(manifest) + '\n').encode('ascii'))
    # The conversion list.
    list_path = os.path.join(out, LIST_NAME)
    make_conversion_list.main(root, os.path.join(HERE, 'overlay'), list_path)
    with open(list_path, 'rb') as handle:
        members[LIST_NAME] = handle.read()
    os.remove(list_path)
    entries = json.loads(members[LIST_NAME].decode('ascii'))['files']
    staged = sum(1 for entry in entries
                 if (lambda blob: blob is None or sha(blob) != entry['sha256_after'])(git_bytes(root, entry['path'])))
    # The programs.
    for tool, source in OWN_TOOLS.items():
        members[f'tools/{tool}'] = in_its_form(tool, read(source))
    for tool in EARLIER_TOOLS:
        members[f'tools/{tool}'] = git_bytes(root, EARLIER_PACKAGE + tool)
        assert members[f'tools/{tool}'] is not None, f'{tool} is not in the build step 2 package at HEAD'
    members[VERIFIER] = in_its_form(VERIFIER, read(f'package_sources/{VERIFIER}'))
    # The sheet, with its counts and hashes computed here.
    new_tests = sum(len(re.findall(r'^    def test_', delivered[module].decode('utf-8'), flags=re.MULTILINE))
                    for module in NEW_TEST_MODULES)
    base = subprocess.run(['git', '-C', root, 'rev-parse', 'HEAD'], check=True, capture_output=True,
                          text=True).stdout.strip()
    values = {'BASE': base, 'OVERLAY_COUNT': len(delivered), 'NEW_COUNT': new_count, 'MODIFIED_COUNT': modified_count,
              'LIST_COUNT': len(entries), 'LIST_SHA': sha(members[LIST_NAME]), 'STAGED_COUNT': staged,
              'NEW_TESTS': new_tests, 'TESTS_AFTER': TESTS_TODAY + new_tests,
              'NEW_LINES': new_tests + len(NEW_TEST_MODULES)}
    sheet = read(f'package_sources/{SHEET}').decode('ascii')
    for key, value in values.items():
        assert f'@@{key}@@' in sheet, f'the sheet does not use @@{key}@@'
        sheet = sheet.replace(f'@@{key}@@', str(value))
    assert '@@' not in sheet, 'the sheet holds a placeholder that was not filled'
    members[SHEET] = in_its_form(SHEET, sheet.encode('ascii'))
    # The folder, the ZIP and the list of its members.
    for member, data in members.items():
        full = os.path.join(out, member)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'wb') as handle:
            handle.write(data)
    zip_path = os.path.join(HERE, 'package', f'{name}.zip')
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for member in sorted(members):
            info = zipfile.ZipInfo(f'{name}/{member}', date_time=FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, members[member])
    lines = [f'{sha(members[member])}  {name}/{member}' for member in sorted(members)]
    with open(os.path.join(HERE, 'package', f'{name}_MEMBERS.txt'), 'wb') as handle:
        handle.write(in_its_form('members.txt', ('\n'.join(lines) + '\n').encode('ascii')))
    print('\n'.join(lines))
    with open(zip_path, 'rb') as handle:
        print(sha(handle.read()), f'{name}.zip')
    print({key: values[key] for key in sorted(values)})
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
