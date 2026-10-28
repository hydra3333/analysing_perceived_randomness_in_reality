"""Package-2 candidate: frozen Powerball and Oz Lotto current-era identities.

Profiles are CODE, not user-supplied configuration. No filesystem/network access,
process launches, holdout outcome inspection, or scientific execution on import.
A pending Oz holdout is an intentional block on real development, not a ceiling
on later authorised prospective FINAL predictions.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from types import MappingProxyType
import re

_GAME_ID = re.compile(r"[A-Z][A-Z0-9]*\Z", re.ASCII)


@dataclass(frozen=True)
class Barrel:
    barrel_id: str
    low: int
    high: int
    selected: int

    def __post_init__(self) -> None:
        if not self.barrel_id or not self.barrel_id.isascii() or not self.barrel_id.isupper():
            raise ValueError("invalid barrel ID")
        if not (type(self.low) is type(self.high) is type(self.selected) is int and
                1 <= self.low <= self.high and 1 <= self.selected <= self.high - self.low + 1):
            raise ValueError("invalid barrel")


@dataclass(frozen=True)
class GameProfile:
    game_id: str
    version: str
    era_id: str
    first_draw: int
    first_date: date
    barrels: tuple[Barrel, ...]
    raw_supplementary_count: int
    holdout_first: int | None  # Historical DEV boundary, not an ongoing FINAL ceiling.
    holdout_last: int | None
    nominal_draw_time: str | None  # OPEN until official evidence reviewed.
    timezone: str | None
    closing_time_utc: str | None  # OPEN; never fabricate a deadline.

    def __post_init__(self) -> None:
        if not _GAME_ID.fullmatch(self.game_id) or not self.version or not self.era_id:
            raise ValueError("invalid profile identity")
        if type(self.first_draw) is not int or self.first_draw < 1:
            raise ValueError("invalid era draw")
        if not self.barrels or len({b.barrel_id for b in self.barrels}) != len(self.barrels):
            raise ValueError("duplicate or empty barrels")
        if type(self.raw_supplementary_count) is not int or self.raw_supplementary_count < 0:
            raise ValueError("invalid supplementary count")
        if (self.holdout_first is None) != (self.holdout_last is None):
            raise ValueError("incomplete holdout")
        if self.holdout_first is not None and not (self.first_draw <= self.holdout_first <= self.holdout_last):
            raise ValueError("invalid holdout bounds")

    def draw_key(self, draw_number: int) -> str:
        if type(draw_number) is not int or draw_number < self.first_draw:
            raise ValueError("draw outside current era")
        return f"{self.game_id}_{draw_number}"

    def derived_date(self, draw_number: int) -> date:
        if type(draw_number) is not int or draw_number < self.first_draw:
            raise ValueError("draw outside current era")
        return self.first_date + timedelta(days=7 * (draw_number - self.first_draw))

    def historical_development_target_allowed(self, draw_number: int) -> bool:
        """ONLY retrospective development, never an ongoing FINAL ceiling."""
        if type(draw_number) is not int or draw_number <= self.first_draw:
            return False
        return self.holdout_first is not None and draw_number < self.holdout_first



POWERBALL = GameProfile(
    'POWERBALL', 'POWERBALL_PROFILE_V1', 'POWERBALL_CURRENT_2018',
    1144, date(2018, 4, 19), (Barrel('MAIN', 1, 35, 7), Barrel('POWERBALL', 1, 20, 1)),
    0, 1577, 1586, None, None, None,
)
OZLOTTO = GameProfile(
    'OZLOTTO', 'OZLOTTO_PROFILE_V2_FIXED_HOLDOUT', 'OZLOTTO_CURRENT_2022',
    1474, date(2022, 5, 17), (Barrel('MAIN', 1, 47, 7),),
    3, 1694, 1703, None, None, None,
)
PROFILES = MappingProxyType({'POWERBALL': POWERBALL, 'OZLOTTO': OZLOTTO})


def get_profile(game_id: str) -> GameProfile:
    # No case folding: typos do not silently select an unintended game.
    if type(game_id) is not str or game_id not in PROFILES:
        raise ValueError("unsupported game_id; select POWERBALL or OZLOTTO")
    return PROFILES[game_id]


def legacy_powerball_game_id(schema: str, game_id: str | None) -> str:
    """Compatibility for known historical schema only. Not generic inference."""
    if schema in {'E1_HISTORICAL_DEVELOPMENT_FORECAST_V0_1_REVIEW',
                  'E1_STANDALONE_MANIFEST_V0_1_REVIEW'} and game_id is None:
        return 'POWERBALL'
    if game_id not in PROFILES:
        raise ValueError('new schema requires approved game_id')
    return game_id
