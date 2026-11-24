#!/usr/bin/env python3
"""Makes the conversion list of the file-form standard: every tracked file of the living project that is brought
to its form, with its SHA-256 before and after.

What this file is for
    The standard's section 7 item 1: "A conversion list, made in the cloud from the repository: every tracked
    file to be converted, with its SHA-256 before and after." This script reads the tracked files from Git at
    HEAD, lays the conversion package's own files over them (the files the package delivers already in their
    form), keeps those the standard calls the living project, and writes one JSON document. For each file it
    proves, before writing anything, that the bytes after differ from the bytes before in line endings only.
    The conversion program on the owner's PC then needs nothing but this list and the disk: it never asks Git.

Which part of the project's rules it carries out
    doc/FILE_FORM_STANDARD_v0_1.md (RAT-47) sections 2, 3, 3A and 7.

Which of the project's own modules it uses
    file_form (overlay/deploy/)     the standard's rule: form_of, to_form, differ_in_line_endings_only,
                                    is_left_out_by_name

What uses it
    Claude, in the cloud workspace. Usage:
        python3 -I make_conversion_list.py <repository root> <overlay folder> <output .json>
It refuses (an assertion or FileFormRefused) a file of a kind the standard does not name, a file that cannot be
brought to its form, and any difference other than line endings.
"""
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# The rule lies in the package's overlay; isolated mode (-I) leaves this script's folder off Python's path.
sys.path.insert(0, os.path.join(HERE, 'overlay', 'deploy'))
import file_form                                            # noqa: E402

# What this document says it is, so that a file of another kind is never taken for a conversion list.
LIST_KIND = 'FILE_FORM_CONVERSION_LIST_V1'
# The living project's tracked files (standard section 2): everything under these folders ...
LIVING_FOLDERS = ('src/', 'deploy/', 'tests/', '.claude/', '.vscode/', 'CLAUDE_CODE_WORKING_FOLDER_TREE/tools/')
# The two Git settings files the package delivers into the root, kept beside this script under plain names: a
# file called .gitattributes or .gitignore inside this folder would itself be obeyed by Git for the folder.
GIT_SETTINGS = {'.gitattributes': 'git_settings/gitattributes', '.gitignore': 'git_settings/gitignore'}
# ... the files that lie directly in the root, and these two records of the results (the owner, decision log
# entry 231 item 4). The results masters and their ledgers are CRLF already and are not listed: the conversion
# program proves them untouched instead.
LIVING_FILES = ('source_data/OZLOTTO_results_master_init_verification.json',
                'source_data/POWERBALL_results_master_init_verification.json')


def sha(data: bytes) -> str:
    """SHA-256 of some bytes, as 64 hexadecimal characters."""
    return hashlib.sha256(data).hexdigest()


def is_living(path: str) -> bool:
    """Whether a tracked path is one of the living project's own files, by the scope written above."""
    return '/' not in path or path.startswith(LIVING_FOLDERS) or path in LIVING_FILES


def tracked_at_head(root: str) -> dict:
    """Every tracked file at HEAD with its bytes: {'src/a.py': b'...'} (only the living ones are read)."""
    names = subprocess.run(['git', '-C', root, 'ls-files', '-z'], check=True, capture_output=True).stdout
    paths = [name for name in names.decode('utf-8').split('\0') if name and is_living(name)]
    return {path: subprocess.run(['git', '-C', root, 'show', f'HEAD:{path}'], check=True,
                                 capture_output=True).stdout for path in paths}


def overlay_files(overlay: str) -> dict:
    """Every file the package delivers with its bytes, by its path from the tree root: the overlay's files and the
    two Git settings files kept beside this script."""
    found = {}
    for path in file_form.files_under(overlay, ('.',), with_root_files=False):
        path = path[2:] if path.startswith('./') else path
        with open(os.path.join(overlay, path), 'rb') as handle:
            found[path] = handle.read()
    for path, kept_as in GIT_SETTINGS.items():
        with open(os.path.join(HERE, kept_as), 'rb') as handle:
            found[path] = handle.read()
    return found


def main(root: str, overlay: str, output: str) -> int:
    """Build the list and write it; print its counts and its SHA-256; return 0."""
    head = tracked_at_head(root)
    delivered = overlay_files(overlay)
    assert all(is_living(path) for path in delivered), 'the overlay holds a file outside the living project'
    entries, left_out, binary = [], [], []
    for path in sorted(set(head) | set(delivered)):
        if file_form.is_left_out_by_name(path):
            assert path not in delivered, f'the package must not deliver {path}: the standard leaves it as it is'
            left_out.append(path)
            continue
        form = file_form.form_of(path)
        assert form is not None, f'{path} is of a kind the standard does not name'
        if form == file_form.BINARY:
            binary.append(path)
            continue
        source = delivered.get(path, head.get(path))
        after = file_form.to_form(source, form)
        assert file_form.differ_in_line_endings_only(source, after), f'{path}: more than line endings would change'
        assert not file_form.faults_in_bytes(after, form), f'{path}: the converted bytes do not conform'
        entry = {'path': path, 'form': form, 'sha256_after': sha(after), 'bytes_after': len(after)}
        if path in delivered:
            # The package delivers this file already in its form: on disk it is the "after" or the tree is not
            # the one the package was copied into.
            entry['delivered_by_package'] = True
            entry['sha256_before'] = sha(after)
        else:
            entry['sha256_before'] = sha(source)
        entries.append(entry)
    assert len(left_out) == len(file_form.LEFT_OUT_BY_NAME), f'the six files left out by name: found {left_out}'
    commit = subprocess.run(['git', '-C', root, 'rev-parse', 'HEAD'], check=True, capture_output=True,
                            text=True).stdout.strip()
    document = {'kind': LIST_KIND, 'standard': 'doc/FILE_FORM_STANDARD_v0_1.md (RAT-47)',
                'made_from_commit': commit,
                'left_out_by_name': left_out, 'binary_by_kind': binary, 'files': entries}
    text = json.dumps(document, indent=1, ensure_ascii=True, sort_keys=True) + '\n'
    data = file_form.to_form(text.encode('ascii'), file_form.CRLF)
    with open(output, 'wb') as handle:
        handle.write(data)
    changing = sum(entry['sha256_before'] != entry['sha256_after'] for entry in entries)
    print(f'{len(entries)} files listed: {changing} change bytes, {len(entries) - changing} are in their form '
          f'already ({sum(1 for entry in entries if entry.get("delivered_by_package"))} delivered by the package); '
          f'{len(left_out)} left out by name; {len(binary)} binary by kind; made from {commit[:7]}')
    print(sha(data), os.path.basename(output))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))
