#!/usr/bin/env python3
"""One Powerball mode for the existing Q4h stack; NO filesystem discovery.

Only two constructors: isolated synthetic or fixed-root production Powerball.
Constructing production mode is read-only and *does not* authorise a scan.
Actual production scan starts require the Q5 switch inside the Q4h runner.
"""
from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

import OUTLANDISH_01_Q4_Published_Source_Guards_v0_1 as G


@dataclass(frozen=True)
class PowerballMode:
    roots: G.FixedRoots
    profile: G.HistoryProfile
    run_type: str
    digits: int

    def checked(self) -> 'PowerballMode':
        roots, profile = self.roots, self.profile
        if not isinstance(roots, G.FixedRoots) or not isinstance(profile, G.HistoryProfile):
            raise ValueError('fixed roots and validated profile required')
        if profile.game != 'powerball' or profile.header != G.PB_HEADER:
            raise ValueError('Powerball mode rejects other game/roles')
        if roots.synthetic:
            G.FixedRoots.test_sandbox(roots.base)
            if (self.run_type != 'TEST_REAL' or type(self.digits) is not int
                    or not 32 <= self.digits < G.DIGITS_PRODUCTION
                    or not profile.synthetic or Path(profile.source).absolute() !=
                    (roots.base / 'histories' / 'powerball_synthetic.csv').absolute()):
                raise ValueError('invalid TEST_REAL Powerball mode identity')
            if os.name == 'nt' and roots.base.is_relative_to(
                    Path(r'G:\OUTLANDISH_01\large_artifacts').absolute()):
                raise ValueError('synthetic sandbox under real production root')
            if any(not (roots.base / label).is_dir() for label in ('digits', 'histories', 'results')):
                raise ValueError('incomplete marked synthetic sandbox')
        else:
            expected_roots = G.FixedRoots.production()
            expected_profile = G.installed_history_profile('powerball')
            if (self.run_type != 'REAL' or self.digits != G.DIGITS_PRODUCTION
                    or roots.base != expected_roots.base or profile != expected_profile
                    or profile.synthetic):
                raise ValueError('invalid installed Powerball production mode')
        return self

    @classmethod
    def synthetic(cls, roots: G.FixedRoots, profile: G.HistoryProfile, digits: int):
        return cls(roots, profile, 'TEST_REAL', digits).checked()

    @classmethod
    def production_powerball(cls):
        # No G: file opened here. G.FixedRoots enforces Windows and fixed G: root.
        return cls(G.FixedRoots.production(), G.installed_history_profile('powerball'),
                   'REAL', G.DIGITS_PRODUCTION).checked()
