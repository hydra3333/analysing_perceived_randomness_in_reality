#!/usr/bin/env python3
"""Synthetic-only, isolated artifact safeguard regression tests (no live data)."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SOURCES = Path(__file__).resolve().parent
CORE = ('outlandish_artifacts.py', 'outlandish_big_constants.py',
        'outlandish_powerball_stage_a.py')


class Safeguards(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name) / 'OUTLANDISH_01 Folder With Spaces'
        self.base.mkdir()
        for name in CORE:
            shutil.copy2(SOURCES / name, self.base / name)

    def run_cmd(self, *args, expect=0):
        result = subprocess.run([sys.executable, *map(str,args)], cwd=self.base,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, expect, result.stdout + result.stderr)
        return result.stdout + result.stderr

    def test_clean_workspace(self):
        self.assertIn('PASS', self.run_cmd('outlandish_artifacts.py', 'audit'))
        (self.base / 'Pi - Dec - Chudnovsky.txt').write_bytes(b'0'*123)
        self.run_cmd('outlandish_artifacts.py', 'audit')

    def test_classify_and_create_only_migration(self):
        src = self.base / 'digits_pi_10_to_6.bin'
        src.write_bytes(b'12345')
        digest = hashlib.sha256(src.read_bytes()).hexdigest()
        self.run_cmd('outlandish_artifacts.py', 'audit', expect=2)
        self.run_cmd('outlandish_artifacts.py', 'migrate', expect=2)
        self.assertTrue(src.exists())  # Preview is read-only.
        self.run_cmd('outlandish_artifacts.py', 'migrate', '--apply', expect=2)
        self.assertTrue(src.exists())  # Cannot move without idle confirmation.
        self.run_cmd('outlandish_artifacts.py', 'migrate', '--apply', '--confirm-idle')
        dest = self.base / 'large_artifacts' / 'digits' / src.name
        self.assertFalse(src.exists())
        self.assertEqual(hashlib.sha256(dest.read_bytes()).hexdigest(), digest)
        self.run_cmd('outlandish_artifacts.py', 'audit')

    def test_large_non_binary_and_legacy_text(self):
        huge = self.base / 'mystery_archive.txt'
        with huge.open('wb') as file:
            file.truncate(10 * 1024 * 1024)
        old = self.base / 'ycruncher_digits' / 'pi_33_digits'
        old.mkdir(parents=True)
        (old / 'Pi - Dec - Chudnovsky.txt').write_bytes(b'x'*34)
        result = self.run_cmd('outlandish_artifacts.py', 'audit', expect=2)
        self.assertIn('mystery_archive.txt', result)
        self.assertIn('pi_33_digits', result)
        # Unknown large file is deliberately NOT moved without separate review.
        result = self.run_cmd('outlandish_artifacts.py', 'migrate', '--apply', '--confirm-idle', expect=2)
        self.assertIn('MANUAL REVIEW', result)
        self.assertTrue(huge.exists())
        # Simulate owner-reviewed manual relocation of the unknown file.
        reviewed = self.base / 'large_artifacts' / 'intermediate' / 'reviewed'
        reviewed.mkdir(parents=True)
        huge.rename(reviewed / huge.name)
        self.run_cmd('outlandish_artifacts.py', 'audit')

    def test_create_only_refusal(self):
        src = self.base / 'digits_pi_10_to_6.bin'
        src.write_bytes(b'abc')
        dest = self.base / 'large_artifacts' / 'digits' / src.name
        dest.parent.mkdir(parents=True)
        dest.write_bytes(b'xyz')
        msg = self.run_cmd('outlandish_artifacts.py', 'migrate', '--apply', '--confirm-idle', expect=2)
        self.assertIn('non-overwrite refusal', msg)
        self.assertEqual(src.read_bytes(), b'abc')
        self.assertEqual(dest.read_bytes(), b'xyz')

    def test_preflight_and_post_run_refusal(self):
        misplaced = self.base / 'not_in_artifacts.bin'
        misplaced.write_bytes(b'1234')
        msg = self.run_cmd('outlandish_big_constants.py', 'self-test', expect=2)
        self.assertIn('ARTIFACT SAFETY STOP (preflight)', msg)
        misplaced.unlink()
        code = ("from pathlib import Path; from outlandish_artifacts import guarded_call; "
                "guarded_call(lambda: Path('stray.bin').write_bytes(b'abc'))")
        msg = self.run_cmd('-c', code, expect=1)
        self.assertIn('ARTIFACT SAFETY STOP (post-run)', msg)
        self.assertIn('post-run artifact audit failed', msg)

    def test_inventory_flags_unreviewed_entry(self):
        self.run_cmd('outlandish_artifacts.py', 'inventory')
        (self.base / 'old_helper.bat').write_text('@echo off\necho old\n')
        msg = self.run_cmd('outlandish_artifacts.py', 'inventory', expect=2)
        self.assertIn('UNREVIEWED-ENTRY old_helper.bat', msg)

    def test_symlink_detection(self):
        target = Path(self.temp.name) / 'external'
        target.mkdir()
        try:
            (self.base / 'shortcut').symlink_to(target, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest('OS cannot create symbolic links')
        self.assertIn('link/junction', self.run_cmd('outlandish_artifacts.py', 'audit', expect=2))

    def test_path_traversal_refusal(self):
        source = "from outlandish_artifacts import require_artifact_path, ARTIFACTS; require_artifact_path(ARTIFACTS / 'digits' / '..' / '..' / 'escape.bin')"
        proc = subprocess.run([sys.executable, '-c', source], cwd=self.base, capture_output=True, text=True)
        self.assertNotEqual(proc.returncode, 0, proc.stdout)
        self.assertIn('ArtifactPolicyError', proc.stderr)

    def test_generator_and_scanner_self_tests(self):
        self.run_cmd('outlandish_big_constants.py', 'self-test')
        self.run_cmd('outlandish_powerball_stage_a.py', 'self-test')
        self.run_cmd('outlandish_artifacts.py', 'audit')

    def test_synthetic_mock_calculator_and_small_scanner(self):
        if os.name == 'nt':
            self.skipTest('POSIX executable stand-in; Windows generator requires an independently reviewed native mock')
        # Purpose-built calculator stand-in: no y-cruncher or real lottery data.
        mock = self.base / 'fake_calculator.py'
        mock.write_text('#!/usr/bin/env python3\n'
                        'from pathlib import Path\n'
                        "Path('generated.txt').write_text('2.71828182845904523536028747135264')\n",
                        encoding='utf-8')
        mock.chmod(0o755)
        # 1+decimal+32 = 33 bytes total; therefore 32 numeric digits.
        self.run_cmd('outlandish_big_constants.py', 'pipeline', '--constant', 'e',
                     '--digits', '32', '--exe', str(mock), expect=2)
        # Explicit minimum remains 33. New mock output has 33 digits + point.
        mock.write_text('#!/usr/bin/env python3\n'
                        'from pathlib import Path\n'
                        "Path('generated.txt').write_text('2.71828182845904523536028747135267')\n",
                        encoding='utf-8')
        self.run_cmd('outlandish_big_constants.py', 'pipeline', '--constant', 'e',
                     '--digits', '33', '--exe', str(mock), '--run')
        binary = self.base / 'large_artifacts' / 'digits' / 'digits_e_33_digits.bin'
        self.assertEqual(binary.stat().st_size, 33)
        self.assertTrue((self.base / 'large_artifacts' / 'intermediate' / 'e_33_digits' / 'OUTLANDISH_01_verified.json').exists())
        self.assertFalse((self.base / 'large_artifacts' / 'intermediate' / 'e_33_digits' / 'generated.txt').exists())
        # One invented historic draw with exact canonical schema, no restricted rows.
        from datetime import date
        csv = self.base / 'POWERBALL_preholdout_only.csv'
        csv.write_text('Draw_Number,Date,Drawn_1,Drawn_2,Drawn_3,Drawn_4,Drawn_5,Drawn_6,Drawn_7,Powerball\n'
                       '1500,2026-01-01,3,14,25,7,31,8,22,12\n', encoding='utf-8')
        # For scanner search, e's prefix must be present, then planted P1 pattern.
        dig = binary.read_bytes() + bytes([0, 3, 1, 4, 2, 5, 0, 7, 3, 1, 0, 8, 2, 2, 1, 2])
        binary.write_bytes(dig)
        report = self.run_cmd('outlandish_powerball_stage_a.py', 'scan', '--digits', binary.name,
                              '--chunk-bytes', '32')
        self.assertIn('P1=1', report)
        runs = list((self.base/'large_artifacts'/'large_results').glob('run_*'))
        self.assertEqual(len(runs), 1)
        self.assertTrue((runs[0]/'digits_e_33_digits_matches.csv').exists())
        self.run_cmd('outlandish_artifacts.py', 'audit')


if __name__ == '__main__':
    unittest.main(verbosity=2)
