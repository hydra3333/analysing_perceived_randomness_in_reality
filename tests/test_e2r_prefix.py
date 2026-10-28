"""E2R-T03 (prefix-only view and digest independence, T-05) and E2R-T10 (B1 hygiene) for the contract. OFFLINE.

The TH-1 harness extended to records (E2R-1 section 13). Synthetic masters only: every row is
invented by test_t05_hardening.write_master in a temporary folder; no file under source_data/ is
opened. For the synthetic contract method, at four targets per game, three views and two date modes,
the rows at and after N are rewritten twice at equal byte length and once longer. The C1 and C2
records' canonical bytes and digests, and every MethodTask field, must be identical across all four
masters, while the freeze receipt's master SHA differs. No master, ledger or INIT hash, path or
code identity may appear in a MethodTask or a C1 or C2 record.
"""
from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

import e2r_fixtures as F
from _common.contract_forecast import assemble_diagnostic, assemble_forecast
from _common.contract_receipts import validate_freeze_receipt
from _common.contract_records import canonical, record_digest
from _common.contract_task import TASK_FIELDS
from _common.game_profiles import POWERBALL, OZLOTTO


def strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from strings(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            yield from strings(v)


class T03AndT10PrefixOnlyRecords(unittest.TestCase):

    def test_records_are_suffix_invariant_and_carry_no_orchestration_identity(self):
        for profile in (POWERBALL, OZLOTTO):
            for target in F.targets(profile):
                decl = F.declaration(profile.game_id, dates=True)   # one method variant, both date modes
                for dates in (False, True):
                    for view_kind in F.VIEWS:
                        with self.subTest(game=profile.game_id, target=target, dates=dates, view=view_kind), \
                                tempfile.TemporaryDirectory() as td:
                            root = Path(td)
                            seen, shas, sizes, forbidden = [], [], [], set()
                            for variant in (0, 1, 2, 3):
                                sha, size, hashes = F.write_master(root, profile, target, variant)
                                shas.append(sha)
                                sizes.append(size)
                                forbidden |= hashes
                                req, view, task = F.load_view(root, decl, target, view_kind, sha, include_dates=dates)
                                out = F.probe_method(view, task)
                                c1 = assemble_forecast(decl, task, view, out)
                                c2 = assemble_diagnostic(decl, task, view, out)
                                receipt = F.receipt_for(c1, sha=sha)
                                validate_freeze_receipt(receipt, c1)
                                seen.append((tuple((f, getattr(task, f)) for f in TASK_FIELDS),
                                             canonical(c1), record_digest(c1), c1['canonical_content_digest'],
                                             canonical(c2), record_digest(c2), receipt['master_sha256']))
                                # E2R-T10: no master, ledger or INIT hash, path or code identity
                                texts = list(strings([task.as_dict(), c1, c2]))
                                for h in forbidden:
                                    self.assertFalse(any(h in t for t in texts), 'an orchestration hash leaked')
                                for fragment in (str(root), 'source_data', 'results_master', 'ledger', '.csv',
                                                 '.py', F.RUN_ID):
                                    self.assertFalse(any(fragment in t for t in texts), f'{fragment!r} leaked')
                            self.assertEqual(len(set(shas)), 4)
                            self.assertEqual(sizes[0], sizes[1])
                            self.assertEqual(sizes[0], sizes[2])
                            self.assertNotEqual(sizes[0], sizes[3])
                            for other in seen[1:]:
                                self.assertEqual(other[:6], seen[0][:6])   # task, C1 and C2 identical
                            self.assertEqual(len({s[6] for s in seen}), 4)  # receipts' master SHA differs


if __name__ == '__main__':
    unittest.main()
