#!/usr/bin/env python3
"""OUTLANDISH_01 v0.2 synthetic cross-platform regression tests.

Each test runs in an isolated workspace and separate storage root. No real
lottery data, no third-party calculator and no primary-project paths are opened.
"""
from __future__ import annotations
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
FILES = ('outlandish_config.py', 'outlandish_artifacts.py',
         'outlandish_big_constants.py', 'outlandish_powerball_stage_a.py')
EPREFIX = bytes(int(c) for c in '27182818284590452353602874713526')
E40 = bytes(int(c) for c in '2718281828459045235360287471352662497757')


class V02SafeguardTests(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.tmp = Path(t.name)
        self.work = self.tmp / 'Local repo space' / 'GAIS' / 'OUTLANDISH_01'
        self.work.mkdir(parents=True)
        self.external = self.tmp / 'G External Data (simulated)'
        for item in FILES:
            shutil.copy2(HERE / item, self.work / item)
        template = (HERE / 'outlandish.local.toml').read_text(encoding='utf-8')
        template = template.replace(r'G:\OUTLANDISH_01', str(self.external))
        assert 'G:\\OUTLANDISH_01' not in template
        template = template.replace('# Absolute parent of ALL generated, potentially large files.',
                                    '# USER COMMENT preserved\n# Absolute parent of ALL generated, potentially large files.')
        self.config = self.work / 'outlandish.local.toml'
        self.config.write_text(template, encoding='utf-8')
        self.digits = self.external / 'large_artifacts' / 'digits'

    def run_it(self, script, *args, code=0):
        done = subprocess.run([sys.executable, str(self.work / script), *map(str, args)],
                              cwd=self.work, capture_output=True, text=True)
        result = done.stdout + done.stderr
        self.assertEqual(done.returncode, code, f'RC {done.returncode}, expected {code}\n{result}')
        return result

    def _put(self, name: str, payload: bytes):
        self.digits.mkdir(parents=True, exist_ok=True)
        path = self.digits / name
        path.write_bytes(payload)
        return path

    def _register(self, const: str, path: Path, *, source=None, delete=False, code=0):
        if source is None:
            source = path
        return self.run_it('outlandish_artifacts.py', 'register', '--constant', const,
                           '--source', source, '--digits', str(path.stat().st_size),
                           '--expected-sha256', hashlib.sha256(path.read_bytes()).hexdigest(),
                           '--apply', '--confirm-idle', *(['--delete-source'] if delete else []), code=code)

    def test_empty_registry_comment_preservation_and_paths(self):
        self.assertIn('0 active constants', self.run_it('outlandish_artifacts.py', 'validate'))
        self.assertIn(str(self.external), self.run_it('outlandish_artifacts.py', 'paths'))
        self.assertIn('active=NONE', self.run_it('outlandish_artifacts.py', 'status'))
        self.assertFalse(self.external.exists())  # Read-only operations create nothing.
        self.assertIn('AUDIT PASS', self.run_it('outlandish_artifacts.py', 'audit'))
        # Read as text so Python normalises Windows CRLF and POSIX LF.
        # Validate TOML section content, not an OS-specific byte encoding.
        original = self.config.read_text(encoding='utf-8')
        self.assertIn('[state.active]\n', original)
        self.assertIn('# Parent: settings.storage.digits_dir', original)

    def test_registry_updates_preserve_comments_and_create_folders(self):
        existing = self._put('digits_e_33_digits.bin', EPREFIX + b'\x06')
        self._register('e', existing)
        written = self.config.read_text(encoding='utf-8')
        self.assertIn('# USER COMMENT preserved', written)
        self.assertIn("file = 'digits_e_33_digits.bin'", written)
        self.assertIn('# Parent: settings.storage.digits_dir', written)
        self.assertTrue(self.config.with_suffix('.toml.bak').exists())
        self.assertIn('AUDIT PASS', self.run_it('outlandish_artifacts.py', 'audit'))

    def test_legacy_workspace_detection_and_archive_inventory(self):
        legacy = self.work / 'digits_pi_10_to_9.bin'
        legacy.write_bytes(b'\x03')
        self.assertIn('ARTIFACT SAFETY STOP', self.run_it('outlandish_artifacts.py', 'audit', code=2))
        legacy.unlink()
        (self.work / 'ARCHIVE').mkdir()
        (self.work / 'ARCHIVE' / 'old_calculator.py').write_text('print("archive")')
        self.assertIn('ARCHIVED-ENTRY', self.run_it('outlandish_artifacts.py', 'inventory'))
        (self.work / 'unused_launcher.bat').write_text('@echo off')
        self.assertIn('UNREVIEWED-ENTRY', self.run_it('outlandish_artifacts.py', 'inventory', code=2))

    def test_register_preview_no_digest_and_sha_refusal(self):
        source = self.work / 'digits_e_33_digits.bin'
        source.write_bytes(EPREFIX + b'\x06')
        good = hashlib.sha256(source.read_bytes()).hexdigest()
        txt = self.run_it('outlandish_artifacts.py', 'register', '--constant', 'e',
                          '--source', source, '--digits', '33', '--expected-sha256', good)
        self.assertIn('PREVIEW', txt)
        self.assertFalse(self.external.exists())
        txt = self.run_it('outlandish_artifacts.py', 'register', '--constant', 'e',
                          '--source', source, '--digits', '33', '--expected-sha256', '0'*64,
                          '--apply', '--confirm-idle', code=2)
        self.assertIn('independent expected SHA', txt)
        self.assertTrue(source.exists())
        self.assertIn('active=NONE', self.run_it('outlandish_artifacts.py', 'status'))

    def test_external_import_verified_copy_and_delete_source(self):
        source = self.work / 'digits_e_33_digits.bin'
        source.write_bytes(EPREFIX + b'\x06')
        out = self._register('e', source, delete=True)
        self.assertIn('PROMOTED', out)
        self.assertFalse(source.exists())
        self.assertEqual((self.digits/source.name).read_bytes(), EPREFIX + b'\x06')
        self.assertIn('AUDIT PASS', self.run_it('outlandish_artifacts.py', 'audit'))

    def test_import_source_cleanup_after_registry_published(self):
        source = self.work / 'digits_e_33_digits.bin'
        source.write_bytes(EPREFIX + b'\x06')
        # Successfully promoted, but explicit deletion not requested; audit
        # flags the remaining misplaced source and exits nonzero.
        first = self._register('e', source, code=2)
        self.assertIn('SOURCE RETAINED', first)
        self.assertTrue(source.exists())
        retried = self._register('e', source, delete=True)
        self.assertIn('REGISTRY ALREADY PROMOTED', retried)
        self.assertFalse(source.exists())
        self.assertIn('AUDIT PASS', self.run_it('outlandish_artifacts.py', 'audit'))

    def test_interrupted_copy_reuse_with_matching_hash(self):
        source = self.work / 'digits_e_33_digits.bin'
        source.write_bytes(EPREFIX + b'\x06')
        dest = self._put(source.name, source.read_bytes())  # Interrupted after copy, before registry
        report = self._register('e', source, delete=True)
        self.assertIn('REUSE VERIFIED EXISTING DESTINATION', report)
        self.assertFalse(source.exists())
        self.assertEqual(dest.read_bytes(), EPREFIX + b'\x06')

    def test_promote_refuses_same_size_and_mismatched_prior_prefix(self):
        p33 = self._put('digits_e_33_digits.bin', EPREFIX + b'\x06')
        self._register('e', p33)
        rejected = self.run_it('outlandish_artifacts.py', 'register', '--constant', 'e',
                               '--source', p33, '--digits', '33',
                               '--expected-sha256', hashlib.sha256(p33.read_bytes()).hexdigest(),
                               '--apply', '--confirm-idle')
        self.assertIn('REGISTRY ALREADY PROMOTED', rejected)
        p40 = self._put('digits_e_40_digits.bin', EPREFIX + b'\x07' + E40[33:])
        rejected = self._register('e', p40, code=2)
        self.assertIn('differs from existing verified active prefix', rejected)
        self.assertIn('active=digits_e_33_digits.bin', self.run_it('outlandish_artifacts.py', 'status'))

    def test_verified_promotion_explicit_retire_and_recovery(self):
        p33 = self._put('digits_e_33_digits.bin', E40[:33])
        self._register('e', p33)
        p40 = self._put('digits_e_40_digits.bin', E40)
        self._register('e', p40)
        self.assertIn('pending_retire=digits_e_33_digits.bin', self.run_it('outlandish_artifacts.py', 'status'))
        self.assertTrue(p33.exists())
        self.run_it('outlandish_artifacts.py', 'retire', '--constant', 'e')
        self.assertTrue(p33.exists())
        self.run_it('outlandish_artifacts.py', 'retire', '--constant', 'e', '--apply', '--confirm-idle')
        self.assertFalse(p33.exists())
        self.assertTrue(p40.exists())
        self.assertIn('pending_retire=NONE', self.run_it('outlandish_artifacts.py', 'status'))
        # Simulate interrupted delete after unlink, before durable TOML state update.
        p50 = self._put('digits_e_50_digits.bin', E40 + b'\x00'*10)
        self._register('e', p50)
        p40.unlink()
        self.assertIn('RECO', self.run_it('outlandish_artifacts.py', 'recover-retirement', '--constant', 'e'))
        self.run_it('outlandish_artifacts.py', 'recover-retirement', '--constant', 'e', '--apply', '--confirm-idle')
        self.assertIn('pending_retire=NONE', self.run_it('outlandish_artifacts.py', 'status'))
        self.assertTrue(p50.exists())

    def test_promotion_after_partial_recovery_refused(self):
        p33 = self._put('digits_e_33_digits.bin', E40[:33])
        self._register('e', p33)
        p40 = self._put('digits_e_40_digits.bin', E40)
        self._register('e', p40)
        p50 = self._put('digits_e_50_digits.bin', E40 + b'\x00'*10)
        report = self._register('e', p50, code=2)
        self.assertIn('unresolved pending retirement', report)
        self.assertTrue(p50.exists())

    def test_scanner_uses_active_prefix_not_arbitrary_binary(self):
        # Invented one-draw fixture, unrelated to the real pre-holdout dataset.
        csv = self.work / 'POWERBALL_preholdout_only.csv'
        csv.write_text('Draw_Number,Date,Drawn_1,Drawn_2,Drawn_3,Drawn_4,Drawn_5,Drawn_6,Drawn_7,Powerball\n'
                       '1500,2026-01-01,3,14,25,7,31,8,22,12\n')
        pattern = bytes((0,3,1,4,2,5,0,7,3,1,0,8,2,2,1,2))
        p49 = self._put('digits_e_49_digits.bin', EPREFIX + b'\x06' + pattern)
        self._register('e', p49)
        short = self.run_it('outlandish_powerball_stage_a.py', 'scan', '--constants', 'e',
                            '--prefix-digits', '33', '--chunk-bytes', '32')
        self.assertIn('P1=0', short)
        long = self.run_it('outlandish_powerball_stage_a.py', 'scan', '--constants', 'e',
                           '--chunk-bytes', '32')
        self.assertIn('P1=1', long)
        self.assertEqual(len(list((self.external/'large_artifacts'/'results').glob('run_*'))), 2)
        self.assertIn('AUDIT PASS', self.run_it('outlandish_artifacts.py', 'audit'))

    def test_invalid_config_fails_closed(self):
        wrong = self.config.read_text().replace("digits_dir = 'digits'", "digits_dir = '../escape'")
        self.config.write_text(wrong, encoding='utf-8')
        report = self.run_it('outlandish_artifacts.py', 'audit', code=2)
        self.assertIn('single relative directory name', report)

    def test_symlink_rejection_if_supported(self):
        dest = self.work / 'outside'
        dest.mkdir()
        try:
            (self.work / 'shortcut').symlink_to(dest, target_is_directory=True)
        except (NotImplementedError, OSError):
            self.skipTest('symbolic link creation unsupported on this Windows account')
        self.assertIn('link/junction', self.run_it('outlandish_artifacts.py', 'audit', code=2))

    def test_generator_and_scanner_synthetic_self_tests(self):
        self.assertIn('SELF-TEST PASS', self.run_it('outlandish_big_constants.py', 'self-test'))
        self.assertIn('SELF-TEST PASS', self.run_it('outlandish_powerball_stage_a.py', 'self-test'))
        self.assertIn('AUDIT PASS', self.run_it('outlandish_artifacts.py', 'audit'))

    def test_generator_dry_run_does_not_create_data(self):
        # Uses a placeholder executable on POSIX; no calculation launched.
        fake = self.work / 'placeholder.exe'
        fake.write_bytes(b'just a placeholder')
        out = self.run_it('outlandish_big_constants.py', 'pipeline', '--constant', 'e',
                          '--digits', '33', '--exe', fake)
        self.assertIn('DRY RUN', out)
        self.assertFalse(self.external.exists())

    def test_large_ram_preflight_is_preview_only_and_refuses_run(self):
        fake = self.work / 'placeholder.exe'
        fake.write_bytes(b'placeholder')
        preview = self.run_it('outlandish_big_constants.py', 'pipeline',
                              '--constant', 'pi', '--digits', '10000000000',
                              '--exe', fake, '--mode', 'ram')
        self.assertIn('DRY RUN', preview)
        self.assertIn('actual --run would refuse', preview)
        refused = self.run_it('outlandish_big_constants.py', 'pipeline',
                              '--constant', 'pi', '--digits', '10000000000',
                              '--exe', fake, '--mode', 'ram', '--run', code=2)
        self.assertIn('blocked pending measured safe-memory review', refused)
        self.assertFalse(self.external.exists())

    def test_ycruncher_output_verification_flag_default_and_overrides(self):
        # Dry-run previews only; the placeholder must never be executed.
        fake = self.work / 'placeholder.exe'
        fake.write_bytes(b'placeholder -- never executed')
        common = ('generate', '--constant', 'e', '--digits', '33', '--exe', fake)
        default = self.run_it('outlandish_big_constants.py', *common)
        self.assertIn('-verify:0', default)
        self.assertIn('OUTPUT VERIFICATION: OFF', default)
        self.assertIn('DRY RUN', default)
        enabled = self.run_it('outlandish_big_constants.py', *common, '--ycruncher-verify-output')
        self.assertIn('-verify:1', enabled)
        self.assertIn('OUTPUT VERIFICATION: ON', enabled)
        self.assertIn('DRY RUN', enabled)
        # The local TOML setting can change the default, and CLI can override it.
        text = self.config.read_text(encoding='utf-8')
        text = text.replace('ycruncher_verify_output = false', 'ycruncher_verify_output = true')
        self.config.write_text(text, encoding='utf-8')
        enabled_by_toml = self.run_it('outlandish_big_constants.py', *common)
        self.assertIn('-verify:1', enabled_by_toml)
        cli_off = self.run_it('outlandish_big_constants.py', *common,
                              '--no-ycruncher-verify-output')
        self.assertIn('-verify:0', cli_off)
        self.assertIn('DRY RUN', cli_off)
        self.assertFalse(self.external.exists())

    def test_generator_output_verification_setting_validation(self):
        source = self.config.read_text(encoding='utf-8')
        self.config.write_text(source.replace('ycruncher_verify_output = false',
                                              'ycruncher_verify_output = "false"'), encoding='utf-8')
        report = self.run_it('outlandish_artifacts.py', 'validate', code=2)
        self.assertIn('invalid [settings.generator]', report)
        # An older v0.2 config without the new key retains default OFF.
        self.config.write_text(source.replace('ycruncher_verify_output = false\n', ''), encoding='utf-8')
        self.assertIn('CONFIG PASS', self.run_it('outlandish_artifacts.py', 'validate'))
        fake = self.work / 'placeholder.exe'
        fake.write_bytes(b'placeholder')
        preview = self.run_it('outlandish_big_constants.py', 'generate', '--constant', 'pi',
                              '--digits', '33', '--exe', fake)
        self.assertIn('-verify:0', preview)

    def test_all_launchers_use_manifest_not_hardcoded_drive(self):
        for name in ('scan_1e9.cmd', 'scan_1e10.cmd', 'generate_1e10.cmd'):
            s = (HERE/name).read_text(encoding='ascii')
            self.assertIn('pushd "%~dp0"', s)
            self.assertNotIn('G:\\', s)
            self.assertNotIn('large_artifacts\\', s)
            self.assertIn('outlandish_artifacts.py audit', s)
        self.assertIn('--prefix-digits 1000000000', (HERE/'scan_1e9.cmd').read_text())
        self.assertIn('--prefix-digits 10000000000', (HERE/'scan_1e10.cmd').read_text())
        self.assertIn('RUN', (HERE/'generate_1e10.cmd').read_text())


if __name__ == '__main__':
    unittest.main(verbosity=2)
