#!/usr/bin/env python3
"""Shared immutable game mode for existing Q4h stack; NO filesystem discovery.

Isolated synthetic or fixed-root per-game production. A mode does NOT authorise
production scans; the runner independently checks the corresponding game switch.
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
    game: str = 'powerball'  # historical Powerball constructors remain unchanged

    def checked(self) -> 'PowerballMode':
        roots, profile = self.roots, self.profile
        if not isinstance(roots, G.FixedRoots) or not isinstance(profile, G.HistoryProfile):
            raise ValueError('fixed roots and validated profile required')
        if (self.game not in ('powerball', 'oz') or profile.game != self.game
                or profile.header != (G.PB_HEADER if self.game == 'powerball' else G.OZ_HEADER)):
            raise ValueError('game/role mismatch in immutable mode')
        if roots.synthetic:
            G.FixedRoots.test_sandbox(roots.base)
            if (self.run_type != 'TEST_REAL' or type(self.digits) is not int
                    or not 32 <= self.digits < G.DIGITS_PRODUCTION
                    or not profile.synthetic or Path(profile.source).absolute() !=
                    (roots.base / 'histories' / f'{self.game}_synthetic.csv').absolute()):
                raise ValueError('invalid TEST_REAL Powerball mode identity')
            if os.name == 'nt' and roots.base.is_relative_to(
                    Path(r'G:\OUTLANDISH_01\large_artifacts').absolute()):
                raise ValueError('synthetic sandbox under real production root')
            if any(not (roots.base / label).is_dir() for label in ('digits', 'histories', 'results')):
                raise ValueError('incomplete marked synthetic sandbox')
        else:
            expected_roots = G.FixedRoots.production()
            expected_profile = G.installed_history_profile(self.game)
            if (self.run_type != 'REAL' or self.digits != G.DIGITS_PRODUCTION
                    or roots.base != expected_roots.base or profile != expected_profile
                    or profile.synthetic):
                raise ValueError('invalid installed game production mode')
        return self

    @classmethod
    def synthetic(cls, roots: G.FixedRoots, profile: G.HistoryProfile, digits: int,
                  *, game: str = 'powerball'):
        return cls(roots, profile, 'TEST_REAL', digits, game).checked()

    @classmethod
    def production(cls, game: str):
        if game not in ('powerball', 'oz'):
            raise ValueError('unknown production game')
        # Constructing mode does not open G: history or packed sources.
        return cls(G.FixedRoots.production(), G.installed_history_profile(game),
                   'REAL', G.DIGITS_PRODUCTION, game).checked()

    @classmethod
    def production_powerball(cls):
        return cls.production('powerball')

    @classmethod
    def production_oz(cls):
        return cls.production('oz')
