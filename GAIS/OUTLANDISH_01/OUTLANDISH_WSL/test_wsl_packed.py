#!/usr/bin/env python3
"""Synthetic tests: no real lottery histories or existing project artifacts used."""
import csv
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from wsl_format import PREFIXES,FULL_LEMNISCATE,REPORT_NAMES,STEMS,pack_ascii,packed_bytes,unpack_numeric,sample_plan
from wsl_verify_windows import verify_packed
from wsl_scan_packed_powerball import Draw,build_index,scan_file,load_draws

HERE=Path(__file__).resolve().parent

class PackedSuite(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
        self.root=Path(self.t.name)
        self.inroot=self.root/'linux';self.attempt=self.inroot/'attempt'
        self.attempt.mkdir(parents=True)
        self.outroot=self.root/'testroot';(self.outroot/'staging').mkdir(parents=True)

    def payload(self,const='phi',digits=65,*,text=None,report_good=True):
        self.assertGreaterEqual(digits,32)
        source_prefix=FULL_LEMNISCATE if const=='lemniscate' else PREFIXES[const]
        stream=text if text is not None else source_prefix+b'0'*(digits-len(source_prefix))
        inp=self.attempt/'ycruncher.txt'
        inp.write_bytes(stream[:1]+b'.'+stream[1:])
        report=self.attempt/'report.txt'
        report.write_text(f"Constant: {REPORT_NAMES[const]}\nDecimal Digits: {digits-1:,}\nVerify Output: Enabled\nSpot Check: {'Good through 32' if report_good else 'BAD'}\n")
        dest=self.outroot/'staging'/f'digits_{STEMS[const]}_candidate.packed.bin'
        cmd=[sys.executable,str(HERE/'wsl_convert.py'),'--constant',const,'--digits',str(digits),
             '--source-root',str(self.inroot),'--input',str(inp),'--report',str(report),
             '--output-root',str(self.outroot),'--output',str(dest)]
        return cmd,inp,dest

    def exec(self,cmd,rc=0):
        p=subprocess.run(cmd,capture_output=True,text=True)
        self.assertEqual(p.returncode,rc,p.stdout+'\n'+p.stderr)
        return p

    def test_packing_pairs_and_padding(self):
        self.assertEqual(pack_ascii(b'161803'),bytes.fromhex('16 18 03'))
        self.assertEqual(pack_ascii(b'16180'),bytes.fromhex('16 18 00'))
        self.assertEqual(unpack_numeric(bytes.fromhex('16 18 00'),5),bytes([1,6,1,8,0]))
        self.assertEqual(packed_bytes(100_000_000_001),50_000_000_001)
        with self.assertRaises(ValueError):unpack_numeric(bytes.fromhex('16 18 01'),5)
        with self.assertRaises(ValueError):pack_ascii(b'0A')

    def test_preview_no_outputs(self):
        cmd,inp,dest=self.payload()
        p=self.exec(cmd)
        self.assertIn('PREVIEW ONLY',p.stdout)
        self.assertFalse(dest.exists());self.assertTrue(inp.exists())

    def test_all_constants_even_odd_cleanup(self):
        for const in PREFIXES:
            for digits in (64,65):
                with self.subTest(const=const,digits=digits):
                    # Each case uses new isolated sandbox.
                    if (self.attempt/'ycruncher.txt').exists(): (self.attempt/'ycruncher.txt').unlink()
                    for old in (self.outroot/'staging').glob('*.bin*'):old.unlink()
                    cmd,inp,dest=self.payload(const,digits)
                    self.exec(cmd+['--run'])
                    self.assertFalse(inp.exists(),'source removed only after success')
                    self.assertEqual(dest.stat().st_size,packed_bytes(digits))
                    self.assertEqual(verify_packed(dest)['digits'],digits)
                    rec=json.loads(Path(str(dest)+'.wsl-receipt.json').read_text())
                    self.assertEqual(rec['format_version'],1)
                    self.assertEqual(rec['verification_policy'],'STREAM_ALL_SOURCE_VALIDATE;SHA256_WHILE_WRITE;SAMPLED_OUTPUT_READBACK')
                    self.assertEqual(rec['binary_sha256_streamed'],__import__('hashlib').sha256(dest.read_bytes()).hexdigest())
                    self.assertEqual(unpack_numeric(dest.read_bytes(),digits)[:32],bytes(x-48 for x in PREFIXES[const]))

    def test_keep_text_and_legacy_reference(self):
        cmd,inp,dest=self.payload('phi',65)
        self.exec(cmd+['--run','--keep-text'])
        self.assertTrue(inp.exists())
        numeric=unpack_numeric(dest.read_bytes(),65)
        ref=self.root/'old_numeric.bin';ref.write_bytes(numeric+b'0'*32)
        check=verify_packed(dest,reference=ref)
        self.assertEqual(check['legacy_reference_prefix_digits_eligible'],65)
        ref.write_bytes(b'\x09'+numeric[1:])
        with self.assertRaisesRegex(ValueError,'reference mismatch|prefix mismatch'):verify_packed(dest,reference=ref)

    def test_invalid_sources_preserved(self):
        for wrong in ('bad-char','missing-dot','double-dot','wrong-length','bad-report','wrong-prefix'):
            with self.subTest(wrong=wrong):
                for old in (self.outroot/'staging').glob('*.bin*'):old.unlink()
                cmd,inp,dest=self.payload(report_good=wrong!='bad-report')
                data=inp.read_bytes()
                if wrong=='bad-char':data=data.replace(b'0',b'X',1)
                if wrong=='missing-dot':data=data.replace(b'.',b'')
                if wrong=='double-dot':data+=b'.'
                if wrong=='wrong-length':data=data[:-1]
                if wrong=='wrong-prefix':data=b'9'+data[1:]
                inp.write_bytes(data)
                self.exec(cmd+['--run'],rc=2)
                self.assertTrue(inp.exists());self.assertFalse(dest.exists())

    def test_output_collision_and_path_escape(self):
        cmd,inp,dest=self.payload()
        dest.write_bytes(b'untouched')
        self.exec(cmd+['--run'],rc=2)
        self.assertEqual(dest.read_bytes(),b'untouched')
        dest.unlink()
        cmd[cmd.index('--output')+1]=str(self.root/'escape.packed.bin')
        self.exec(cmd+['--run'],rc=2)
        self.assertFalse((self.root/'escape.packed.bin').exists())

    def test_symlink_refusal(self):
        cmd,inp,dest=self.payload()
        lnk=self.attempt/'linked.txt'
        try:lnk.symlink_to(inp)
        except OSError:self.skipTest('symlink unavailable')
        cmd[cmd.index('--input')+1]=str(lnk)
        self.exec(cmd+['--run'],rc=2)
        self.assertFalse(dest.exists())

    def test_sample_mutation_detected(self):
        cmd,inp,dest=self.payload(digits=65537)
        self.exec(cmd+['--run','--keep-text'])
        with dest.open('r+b') as f:
            f.seek(1);v=f.read(1);f.seek(1);f.write(bytes([v[0]^1]))
        with self.assertRaisesRegex(ValueError,'sample mismatch'):verify_packed(dest)

    def test_invalid_receipt_format(self):
        cmd,inp,dest=self.payload()
        self.exec(cmd+['--run'])
        p=Path(str(dest)+'.wsl-receipt.json')
        obj=json.loads(p.read_text());obj['format']='legacy';p.write_text(json.dumps(obj))
        with self.assertRaisesRegex(ValueError,'unexpected packed format'):verify_packed(dest)

    def test_unsampled_corruption_rejected_by_full_scanner_hash(self):
        digits = 240000
        cmd, inp, dest = self.payload('phi', digits)
        self.exec(cmd + ['--run', '--keep-text'])
        rec = json.loads(Path(str(dest) + '.wsl-receipt.json').read_text())
        spans = [(a['offset_bytes'], a['offset_bytes'] + a['size']) for a in rec['samples']]
        off = next(i for i in range(16, dest.stat().st_size)
                   if not any(start <= i < end for start,end in spans))
        with dest.open('r+b') as f:
            f.seek(off); before = f.read(1)[0]
            f.seek(off); f.write(bytes([before ^ 1]))
        # Intentional reduced-verification policy: this does NOT detect the change.
        self.assertTrue(verify_packed(dest)['no_registration'])
        output = self.root / 'results'; output.mkdir()
        draw = Draw(1500, (3,14,25,7,31,8,22), 12)
        # A complete, naturally required scan hashes the entire file in-stream.
        with self.assertRaisesRegex(ValueError, 'FULL SCAN SHA DIFFERS'):
            scan_file(dest, rec, [draw], output, chunk_digits=32768,
                      progress_seconds=9999)

    def test_scan_cross_boundary_even_and_odd_digit_offsets(self):
        d=Draw(1500,(3,14,25,7,31,8,22),12)
        seq1=b'0314250731082212'
        seq2=b'25143108220312'  # P3 only? this is 6 main+PB
        stream=PREFIXES['phi']+b'9'*3+seq1+b'9'*7+seq2+b'9'*24
        digits=len(stream)
        cmd,inp,dest=self.payload('phi',digits,text=stream)
        self.exec(cmd+['--run','--keep-text'])
        resultdir=self.root/'results';resultdir.mkdir()
        s=scan_file(dest,json.loads(Path(str(dest)+'.wsl-receipt.json').read_text()),[d],resultdir,
                    chunk_digits=32,progress_seconds=100)
        self.assertGreaterEqual(s['match_counts']['P1'],1)
        self.assertGreaterEqual(s['match_counts']['P2'],1)
        self.assertGreaterEqual(s['match_counts']['P3'],1)
        self.assertTrue(s['digest_compared_to_conversion_receipt'])
        found=list(resultdir.glob('*/matches.csv'))
        self.assertEqual(len(found),1)
        csv_text=found[0].read_text()
        self.assertIn(',35,51,',csv_text)  # offset 32 + 3

    def test_holdout_refusal_before_lottery_parse(self):
        p=self.root/'draws.csv'
        p.write_text('Draw_Number,Date,'+','.join('Drawn_'+str(i) for i in range(1,8))+',Powerball\n'
                     '1577,UNREAD,SECRET,SECRET,SECRET,SECRET,SECRET,SECRET,SECRET,SECRET\n')
        with self.assertRaisesRegex(ValueError,'cutoff'):load_draws(p)

if __name__=='__main__':unittest.main(verbosity=2)
