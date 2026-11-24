#!/usr/bin/env python3
"""Makes the look kit: the three files the owner needs for a look-only run of the conversion program in his
real DEV tree, before anything is packaged or installed.

What this file is for
    A look-only run changes nothing and shows what a tree holds that Git does not track. This script puts the
    program, the rule it uses and today's conversion list into look_kit/, each in the standard's form (CRLF), so
    that the bytes on the owner's disk after a pull are the bytes committed and the hashes quoted are the hashes
    he sees. It makes the list afresh from Git at HEAD with the package's files laid over.

Which part of the project's rules it carries out
    doc/FILE_FORM_STANDARD_v0_1.md section 7 (the walk and its print-out before anything is changed) and section
    11 (what the owner's DEV holds that Git does not track).

Which of the project's own modules it uses
    file_form (overlay/deploy/)     to_form: the three files are written in their form
    make_conversion_list (beside this file)     the list

What uses it
    Claude, in the cloud workspace. Usage:  python3 -I make_look_kit.py <repository root> <kit folder name>
    (a new folder name for each edition: a kit that has been reviewed is never written over)
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'overlay', 'deploy'))
import file_form                                            # noqa: E402
import make_conversion_list                                 # noqa: E402

# What goes into the kit beside the list: {name in the kit: where it comes from, from this folder}.
COPIED = {'convert_to_file_form.py': 'tools/convert_to_file_form.py', 'file_form.py': 'overlay/deploy/file_form.py'}
LIST_NAME = 'CONVERSION_LIST.json'


def main(root: str, kit_name: str) -> int:
    """Write the kit's three files into a new folder beside this script and print the SHA-256 of each; return 0.
    Refuses (FileExistsError) a folder that exists already."""
    KIT = os.path.join(HERE, kit_name)
    os.makedirs(KIT)
    make_conversion_list.main(root, os.path.join(HERE, 'overlay'), os.path.join(KIT, LIST_NAME))
    for name, source in COPIED.items():
        with open(os.path.join(HERE, source), 'rb') as handle:
            data = file_form.to_form(handle.read(), file_form.CRLF)
        with open(os.path.join(KIT, name), 'wb') as handle:
            handle.write(data)
    for name in sorted(os.listdir(KIT)):
        with open(os.path.join(KIT, name), 'rb') as handle:
            print(hashlib.sha256(handle.read()).hexdigest(), name)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
