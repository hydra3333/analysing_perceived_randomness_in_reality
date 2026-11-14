#!/usr/bin/env python3
r"""OUTLANDISH_01 Q2 supplemental tests: fail-closed inputs and mutation canaries.

Run on Ryzen/Windows from the repository root with project .venv:
  .venv\Scripts\python.exe GAIS\OUTLANDISH_01\OUTLANDISH_01_Q2_Remaining_Qualification_v0_1.py --self-test
  .venv\Scripts\python.exe GAIS\OUTLANDISH_01\OUTLANDISH_01_Q2_Remaining_Qualification_v0_1.py --run

Requires the previously executed Q2 v0.1 oracle and old-scanner comparison harness.
Reads source files from GAIS/OUTLANDISH_01, never modifies them. All fixture
files, mutated COPIES of old scanner, and report directories are under TEMP.
NEVER uses real lotteries, published 5-GB files or REAL output as inputs.
The old scanner remains an UNQUALIFIED historical reference. The known
requested-prefix EOF defect is separately preserved as a future regression.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import OUTLANDISH_01_Q2_LegacyScanner_Comparison_v0_1 as base


# Exact replacements. A shadow copy is modified ONLY in disposable TEMP.
# The originals (including known prefix bug) remain byte-for-byte unchanged.
MUTATIONS = {
    'odd_digit_starts_omitted': (
        'indices=np.flatnonzero(p2_ok|p3_ok)',
        'indices=np.flatnonzero(p2_ok|p3_ok);indices=indices[(indices%2)==0]',
        'chunk_crossings_duplicate_keys_odd_N'),
    'chunk_lookahead_removed': (
        'look=min(total-start,span+15)',
        'look=min(total-start,span)',
        'chunk_crossings_duplicate_keys_odd_N'),
    'pb_main_equality_wrongly_forbidden': (
        'if bool(p3_ok[i]):',
        'if bool(p3_ok[i]) and seventh not in six:',
        'chunk_crossings_duplicate_keys_odd_N'),
    'seventh_p2_main_wrongly_limited_to_20': (
        'p2_ok=six_ok&(balls[6]>=1)&(balls[6]<=35)',
        'p2_ok=six_ok&(balls[6]>=1)&(balls[6]<=20)',
        'planted_baseline_340'),
    'off_by_one_start_offset': (
        'pos=start+i',
        'pos=start+i+1',
        'planted_baseline_340'),
    'duplicate_chunk_start_ownership': (
        'valid=min(span,max(0,len(digits)-13))',
        'valid=min(span+1,max(0,len(digits)-13))',
        'planted_baseline_340'),
    'K6S_wrong_family_lookup': (
        'for d in p3.get((tuple(sorted(six)),seventh),()):',
        'for d in p2.get((tuple(sorted(six)),seventh),()):',
        'planted_baseline_340'),
    'K6S_corrupt_end_offset': (
        "writer.writerow((inp.name,d,'P3',pos,pos+14,text(14)))",
        "writer.writerow((inp.name,d,'P3',pos,pos+13,text(14)))",
        'planted_baseline_340'),
}

REFUSALS = (
    'wrong_draw_header', 'nonconsecutive_draw_id', 'repeated_draw_id',
    'duplicate_main', 'bad_powerball_range', 'invalid_receipt_format',
    'wrong_receipt_bytes', 'incorrect_sample_sha', 'nonzero_odd_padding',
    'truncated_binary', 'missing_receipt', 'altered_known_prefix',
)


def _check_in_temp(root: Path) -> None:
    if not root.is_dir() or root.is_symlink():
        raise ValueError('TEMP test root not an ordinary directory')
    real_dirs = (base.REAL_RESULTS_ROOT,
                 Path(r'G:\OUTLANDISH_01\large_artifacts\digits'),
                 base.HERE)
    dest = str(root.resolve()).casefold().rstrip('\\/') + os.sep
    for real in real_dirs:
        source = str(real.resolve()).casefold().rstrip('\\/') + os.sep
        if dest.startswith(source) or source.startswith(dest):
            raise ValueError(f'TEMP isolation failed: {root}, {real}')


def _run_old(scanner: Path, binary: Path, draws: Path, output_root: Path):
    args = [sys.executable, str(scanner), '--input', str(binary),
            '--draws', str(draws), '--output-root', str(output_root),
            '--chunk-digits', '32', '--progress-seconds', '999', '--run']
    return subprocess.run(args, cwd=output_root.parent, text=True,
                          encoding='utf-8', errors='replace', stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, timeout=45, check=False)


def _materials(folder: Path, case: base.Scenario) -> tuple[Path, Path, Path]:
    folder.mkdir(exist_ok=False)
    packed = folder / 'SYNTHETIC_PB_NOT_A_CONSTANT.packed.bin'
    draws = folder / 'SYNTHETIC_NOT_REAL.csv'
    out = folder / 'results_test_only'
    out.mkdir()
    base.write_synthetic(packed, case.digits)
    base.write_draws(draws)
    return packed, draws, out


def _actual(run: Path) -> set[tuple[int,str,int,str]]:
    dirs = list(run.glob('packed_run_*'))
    if len(dirs) != 1:
        raise ValueError(f'expected one isolated output, got {len(dirs)}')
    return base.read_actual_rows(dirs[0] / 'matches.csv', 10_000_000)


def _case(name: str) -> base.Scenario:
    match = [s for s in base.scenario_set() if s.name == name]
    if len(match) != 1 or match[0].prefix_digits is not None:
        raise ValueError(f'expected one full-scan scenario {name}')
    return match[0]


def _mutant_test(root: Path, name: str) -> tuple[bool,str]:
    target, replacement, case_name = MUTATIONS[name]
    folder = root / ('mutation_' + name)
    case = _case(case_name)
    data, draws, out = _materials(folder, case)
    shadow = folder / 'SHADOW_SCANNER_COPY_ONLY'
    shadow.mkdir()
    original = base.OLD_SCANNER.read_text(encoding='utf-8')
    if original.count(target) != 1:
        return False, f'CANARY CONFIG ERROR: target occurrence count={original.count(target)}'
    for lib in ('wsl_format.py','wsl_verify_windows.py'):
        p = base.OLD_SCANNER.parent / lib
        if not p.is_file() or p.is_symlink():
            return False, f'required historical library not regular: {p}'
        shutil.copyfile(p, shadow / lib)
    mutated = original.replace(target, replacement, 1)
    # Pure local syntax gate. Mutations must parse; a SyntaxError is not a useful detection.
    compile(mutated, f'SHADOW_{name}', 'exec')
    scanner = shadow / 'wsl_scan_packed_powerball.py'
    scanner.write_text(mutated, encoding='utf-8', newline='\n')
    result = _run_old(scanner, data, draws, out)
    if result.returncode:
        detail = (result.stderr + '\n' + result.stdout).strip()[-250:]
        return False, f'mutant failed to execute normally (not crediting as detected): {detail}'
    try:
        got = _actual(out)
    except ValueError as exc:
        if 'duplicate old scanner event identity' in str(exc) or 'malformed old scanner row' in str(exc):
            return True, 'detected invalid/duplicated output: ' + str(exc)[:110]
        return False, f'unexpected comparison error: {exc}'
    expected = base.expected_rows(case)
    if got == expected:
        return False, 'MUTATION ESCAPED: incorrect scanner generated exact same event set'
    return True, f'detected by exact oracle tuple comparison (missing={len(expected-got)}, extra={len(got-expected)})'


def _modify_csv(path: Path, name: str) -> None:
    with path.open(encoding='utf-8', newline='') as f:
        lines = list(csv.reader(f))
    if name == 'wrong_draw_header':
        lines[0][0] = 'Unexpected_ID'
    elif name == 'nonconsecutive_draw_id':
        lines[2][0] = '999'
    elif name == 'repeated_draw_id':
        lines[2][0] = lines[1][0]
    elif name == 'duplicate_main':
        lines[1][3] = lines[1][2]
    elif name == 'bad_powerball_range':
        lines[1][-1] = '21'
    else:
        raise AssertionError(name)
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(lines)


def _tamper_binary_and_reseal(path: Path, receipt: Path, name: str) -> None:
    blob = bytearray(path.read_bytes())
    if name == 'nonzero_odd_padding':
        blob[-1] = (blob[-1] & 0xf0) | 0x01
    elif name == 'altered_known_prefix':
        blob[0] = 0x99
    else:
        raise AssertionError(name)
    path.write_bytes(blob)
    meta = json.loads(receipt.read_text(encoding='utf-8'))
    digest = hashlib.sha256(blob).hexdigest()
    meta['binary_sha256_streamed'] = digest
    meta['samples'][0]['sha256'] = digest # short file, whole file sampled
    receipt.write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')


def _refusal_test(root: Path, name: str) -> tuple[bool,str]:
    folder = root / ('refusal_' + name)
    case = _case('chunk_crossings_duplicate_keys_odd_N') if name == 'nonzero_odd_padding' else _case('planted_baseline_340')
    data, draws, out = _materials(folder, case)
    receipt = data.with_name(data.name + '.wsl-receipt.json')
    if name in ('wrong_draw_header','nonconsecutive_draw_id','repeated_draw_id',
                'duplicate_main','bad_powerball_range'):
        _modify_csv(draws, name)
    elif name == 'invalid_receipt_format':
        meta = json.loads(receipt.read_text(encoding='utf-8'))
        meta['format'] = 'INVALID_BYTE_FORMAT'
        receipt.write_text(json.dumps(meta),encoding='utf-8')
    elif name == 'wrong_receipt_bytes':
        meta = json.loads(receipt.read_text(encoding='utf-8'))
        meta['packed_bytes'] += 1
        receipt.write_text(json.dumps(meta),encoding='utf-8')
    elif name == 'incorrect_sample_sha':
        meta = json.loads(receipt.read_text(encoding='utf-8'))
        meta['samples'][0]['sha256'] = '0' * 64
        receipt.write_text(json.dumps(meta),encoding='utf-8')
    elif name in ('nonzero_odd_padding','altered_known_prefix'):
        _tamper_binary_and_reseal(data, receipt, name)
    elif name == 'truncated_binary':
        data.write_bytes(data.read_bytes()[:-1])
    elif name == 'missing_receipt':
        receipt.unlink()
    else:
        raise AssertionError(name)
    res = _run_old(base.OLD_SCANNER,data,draws,out)
    detail = (res.stderr + '\n' + res.stdout).strip()
    if res.returncode == 0 or 'SCAN PASS' in res.stdout:
        return False, 'unexpectedly accepted invalid fixture'
    if 'Traceback' in detail:
        return False, 'unhandled exception (not crediting as controlled refusal): ' + detail[-250:]
    if 'PACKED SCAN STOP:' not in detail:
        return False, 'did not produce scanner refusal message: ' + detail[-250:]
    return True, 'controlled refusal: ' + detail.split('PACKED SCAN STOP:',1)[-1].split('\n',1)[0].strip()[:170]


def _self_test() -> None:
    base.self_test()
    source = base.OLD_SCANNER.read_text(encoding='utf-8')
    for name, (old,new,case) in MUTATIONS.items():
        if source.count(old) != 1:
            raise ValueError(f'{name}: mutation target absent/ambiguous')
        compile(source.replace(old,new,1),f'SHADOW_{name}','exec')
        if not base.expected_rows(_case(case)):
            raise ValueError(f'{name}: test scenario has zero expected tuples')
    if len(MUTATIONS) != len(set(MUTATIONS)) or len(REFUSALS) != len(set(REFUSALS)):
        raise ValueError('duplicate test identifiers')
    print(f'Q2 EXTENSION SELF-TEST PASS: {len(MUTATIONS)} syntactically valid mutation templates, '
          f'{len(REFUSALS)} refusal cases; pinned historic scanner/oracle; no files created')


def _run() -> int:
    if os.name != 'nt':
        raise ValueError('Run the actual scanner qualification on Windows/Ryzen')
    _self_test()
    before = base.result_root_fingerprint()
    failures=[]
    with tempfile.TemporaryDirectory(prefix='OUTLANDISH_Q2_EXTENSION_TEST_ONLY_') as temp:
        root=Path(temp)
        _check_in_temp(root)
        for scenario_name in ('planted_baseline_340','chunk_crossings_duplicate_keys_odd_N'):
            scenario = _case(scenario_name)
            ok,detail=base.check_one(scenario,root)
            print(f'{"PASS" if ok else "FAIL"}: control_{scenario_name}: {detail}',flush=True)
            if not ok: failures.append('control_'+scenario_name)
        for name in MUTATIONS:
            ok,detail=_mutant_test(root,name)
            print(f'{"PASS" if ok else "FAIL"}: mutation_{name}: {detail}',flush=True)
            if not ok: failures.append('mutation_'+name)
        for name in REFUSALS:
            ok,detail=_refusal_test(root,name)
            print(f'{"PASS" if ok else "FAIL"}: refusal_{name}: {detail}',flush=True)
            if not ok: failures.append('refusal_'+name)
    after = base.result_root_fingerprint()
    if after != before:
        failures.append('REAL_RESULTS_FINGERPRINT_CHANGED')
        print('FAIL: REAL results directory listing/metadata changed')
    else:
        print('PASS: REAL results directory listing/metadata unchanged')
    if failures:
        print(f'Q2 EXTENSION INCOMPLETE ({len(failures)}): {", ".join(failures)}')
        return 1
    print(f'Q2 EXTENSION PASS: controls=2/2 mutations={len(MUTATIONS)}/{len(MUTATIONS)} '
          f'refusals={len(REFUSALS)}/{len(REFUSALS)}; historical scanner unchanged; '
          'KNOWN Q2 FINDING PREFIX_END_EOF_ELIGIBILITY retained for Q3')
    print('This is not Q3 or Q5 approval, and old scanner remains unqualified.')
    return 0


def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    choices=p.add_mutually_exclusive_group(required=True)
    choices.add_argument('--self-test',action='store_true')
    choices.add_argument('--run',action='store_true')
    opt=p.parse_args()
    try:
        if opt.self_test:
            _self_test()
            return 0
        return _run()
    except (OSError,ValueError,AssertionError,subprocess.TimeoutExpired,json.JSONDecodeError,csv.Error) as ex:
        print(f'Q2 EXTENSION STOP: {ex}',file=sys.stderr)
        return 2

if __name__=='__main__':
    raise SystemExit(main())
