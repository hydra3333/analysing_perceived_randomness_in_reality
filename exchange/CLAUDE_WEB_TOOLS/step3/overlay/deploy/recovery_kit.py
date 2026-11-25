"""The recovery kit: a small checked ZIP in a tree's backup root that holds the restore tool.

What this file is for
    A restore must be possible when no tree of the project can be used. So, for every software state a tree is
    given, a kit is written into that tree's backup root: the restore tool (one file, standard library only),
    Restore.bat, plain instructions and the kit's own list of its files with their hashes. This file builds one,
    from DEV's install-tool files exactly as DEV's infrastructure marker lists them, checks it by reading it
    back, and only then gives it its name and its ".sha256" file. Building a kit is always an attempt: the
    result is returned as it is, and the command that asked decides with the owner what follows.

Which part of the specification it carries out
    doc/Predictive_Randomness_Deployment_Design_v0_12.md section 11; specification v0.6 section 14.1.

Which of the project's own modules it uses
    None (the infrastructure marker is read as the JSON it is).

What uses it
    The install tools of build step 3 (Init_Tree, Install, Reinstall_Infra and the QA software replacement), at
    every creation and install; and its tests.
"""
from __future__ import annotations

import hashlib
import json
import os
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

# DEV's infrastructure marker, which lists every install-tool file with its hash (deploy/install_readiness.py).
INFRA_MARKER_PATH = 'deploy/INFRA_IS_INSTALLABLE.json'
# The kit's files: where each lies in DEV, and its name in the kit.
KIT_FILES = (('deploy/restore_tool.py', 'restore_tool.py'), ('deploy/kit/Restore.bat', 'Restore.bat'),
             ('deploy/kit/HOW_TO_RESTORE.txt', 'HOW_TO_RESTORE.txt'))
# The kit's own list of its files (the restore tool reads it before it does anything), and its kind.
KIT_MANIFEST_NAME = 'KIT_MANIFEST.json'
KIT_MANIFEST_KIND = 'KIT_MANIFEST_V1'
PARTIAL_SUFFIX = '.partial'


@dataclass(frozen=True)
class KitResult:
    """What an attempt at a kit came to. made: True only for a kit that was read back and has its name.
    path: the ZIP, or None.  reason: when not made, why, in a sentence."""
    made: bool
    path: Path | None = None
    reason: str = ''

    def line(self) -> str:
        """One line for the owner: 'RECOVERY KIT WRITTEN AND CHECKED: <path>' or 'RECOVERY KIT NOT WRITTEN: <why>'."""
        return f'RECOVERY KIT WRITTEN AND CHECKED: {self.path}' if self.made else f'RECOVERY KIT NOT WRITTEN: {self.reason}'


def build_kit(dev_root: Path, backup_root: Path, software_fingerprint: str, now=None) -> KitResult:
    """Try to write one recovery kit into a backup root. It never raises for a kit that cannot be written.

    dev_root: DEV's folder.  backup_root: the backup root of the tree the kit is for.
    software_fingerprint: the fingerprint of the software state that tree will have (the SHA-256 of its list of
    installed files); its first 12 characters go into the kit's name.  now: gives the present time (UTC).
    Returns a KitResult. Not written, with the reason, when: DEV's infrastructure is not marked ready; a file of
    the kit is not the file the marker lists; the backup root cannot be written; the kit read back is not what
    was written. A ".partial" that failed is removed if it can be.
    """
    now = now or (lambda: datetime.now(timezone.utc))
    moment = now()
    name = f'KIT_{moment.astimezone().strftime("%Y%m%d_%H%M%S")}_{software_fingerprint[:12]}.zip'
    final, partial = Path(backup_root) / name, Path(backup_root) / (name + PARTIAL_SUFFIX)
    try:
        try:
            marker = json.loads((Path(dev_root) / INFRA_MARKER_PATH).read_text(encoding='ascii'))
            marked = {entry['path']: entry['sha256'] for entry in marker['install_tool']}
        except (OSError, ValueError, KeyError, TypeError):
            return KitResult(False, reason=f'DEV\'s infrastructure is not marked ready ({Path(dev_root) / INFRA_MARKER_PATH} '
                                           f'is missing or is not a marker). Run Make_Installable.bat INFRA in DEV.')
        contents = {}
        for source, kit_name in KIT_FILES:
            data = (Path(dev_root) / source).read_bytes()
            if marked.get(source) != hashlib.sha256(data).hexdigest():
                return KitResult(False, reason=f'{source} in DEV is not the file DEV\'s infrastructure marker lists. '
                                               f'Run Make_Installable.bat INFRA in DEV.')
            contents[kit_name] = data
        manifest = {'kind': KIT_MANIFEST_KIND, 'software_fingerprint': software_fingerprint,
                    'made_utc': moment.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'files': [{'path': kit_name, 'sha256': hashlib.sha256(data).hexdigest()}
                              for kit_name, data in sorted(contents.items())]}
        contents[KIT_MANIFEST_NAME] = (json.dumps(manifest, indent=1, sort_keys=True).replace('\n', '\r\n')
                                       + '\r\n').encode('ascii')
        Path(backup_root).mkdir(parents=True, exist_ok=True)
        beside = Path(str(final) + '.sha256')
        if final.exists() or partial.exists() or beside.exists():
            return KitResult(False, reason=f'{final}, its ".partial" or its ".sha256" exists already. Nothing was '
                                           f'removed. Run the command again.')
        try:
            with zipfile.ZipFile(partial, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
                for kit_name, data in contents.items():
                    archive.writestr(kit_name, data)
            with zipfile.ZipFile(partial) as archive:
                if {member: archive.read(member) for member in archive.namelist()} != contents:
                    raise OSError('the kit read back is not what was written')
            digest = hashlib.sha256(partial.read_bytes()).hexdigest()
            with open(beside, 'wb') as handle:               # the ".sha256" first: a kit that has its name
                handle.write(f'{digest} *{name}\r\n'.encode('ascii'))     # always has its ".sha256" beside it
            os.replace(partial, final)
        except BaseException:
            for ours in (partial, beside):                   # only what this attempt made itself
                try:
                    ours.unlink()
                except OSError:
                    pass
            raise
    except (OSError, zipfile.BadZipFile) as failure:
        return KitResult(False, reason=f'{failure}')
    return KitResult(True, path=final)
