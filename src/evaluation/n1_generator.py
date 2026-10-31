"""N1's fair-draw generator (releases and WF-1 design v0.1r1 section 7.2, decision WF1-8; OWNER-RATIFIED 31 October 2026).

Python's standard library only, so the simulated draws are identical on every platform and library version:
- the stream key for replicate r and target draw N is the concatenation of length-prefixed fields (a uint32
  little-endian byte length, then the UTF-8 bytes): 'PREDICTIVE_RANDOMNESS/N1_FAIR_DRAW_V1', the seed policy ID,
  the root (the beacon's outputValue: 128 upper-case hexadecimal characters, as published), the game ID, r and N
  in decimal;
- the words are the SHAKE-256 output of that key, read as consecutive unsigned 64-bit little-endian integers
  (a longer SHAKE request extends the shorter one, so the stream is well defined at any length);
- U(k): take the next word w; accept it if w < 2**64 - (2**64 mod k) and return w mod k; otherwise take the next;
- Powerball: a partial Fisher-Yates shuffle of 1..35 (i = 0..6), the first 7 are the main set; then 1 + U(20);
- Oz Lotto: the same over 1..47 for i = 0..9; the first 7 are main, the last 3 supplementary.

Draws are keyed by (r, N), so a target's simulated draw never depends on the window, cohort or table. The outputs
are NULL_CALIBRATION artefacts (design 7.5): never written into a real ledger and never read by a method.
"""
from __future__ import annotations

import hashlib
import re
import struct

DOMAIN = 'PREDICTIVE_RANDOMNESS/N1_FAIR_DRAW_V1'
ROOT = re.compile(r'[0-9A-F]{128}\Z', re.ASCII)
GAMES = {'POWERBALL': (35, 7, 0, 20), 'OZLOTTO': (47, 7, 3, None)}   # pool, main, supplementaries, PB range
_CHUNK = 256                                  # 32 words; a draw needs 8 (Powerball) or 10 (Oz Lotto) without rejection
_TWO64 = 1 << 64


def _check(root_hex: str, policy_id: str, game_id: str, replicate: int, target: int) -> None:
    if type(root_hex) is not str or not ROOT.fullmatch(root_hex):
        raise ValueError('N1 root must be 128 upper-case hexadecimal characters, as published')
    if type(policy_id) is not str or not policy_id or not policy_id.isascii():
        raise ValueError('N1 policy ID must be a non-empty ASCII string')
    if game_id not in GAMES:
        raise ValueError(f'unknown game {game_id!r}')
    if type(replicate) is not int or replicate < 1:
        raise ValueError('replicate must be an integer >= 1')
    if type(target) is not int or target < 1:
        raise ValueError('target must be an integer >= 1')


def _lp(text: str) -> bytes:
    raw = text.encode('utf-8')
    return struct.pack('<I', len(raw)) + raw


def stream_key(root_hex: str, policy_id: str, game_id: str, replicate: int, target: int) -> bytes:
    _check(root_hex, policy_id, game_id, replicate, target)
    return b''.join(_lp(f) for f in (DOMAIN, policy_id, root_hex, game_id, str(replicate), str(target)))


class _Stream:
    """SHAKE-256 output of one key, read as unsigned 64-bit little-endian words."""

    __slots__ = ('key', 'buf', 'pos')

    def __init__(self, key: bytes):
        self.key = key
        self.buf = hashlib.shake_256(key).digest(_CHUNK)
        self.pos = 0

    def word(self) -> int:
        if self.pos + 8 > len(self.buf):
            self.buf = hashlib.shake_256(self.key).digest(2 * len(self.buf))   # extends the earlier output
        w = int.from_bytes(self.buf[self.pos:self.pos + 8], 'little')
        self.pos += 8
        return w

    def below(self, k: int) -> int:
        limit = _TWO64 - (_TWO64 % k)
        while True:
            w = self.word()
            if w < limit:
                return w % k


def first_word(root_hex: str, policy_id: str, game_id: str, replicate: int, target: int) -> int:
    return _Stream(stream_key(root_hex, policy_id, game_id, replicate, target)).word()


def fair_draw(root_hex: str, policy_id: str, game_id: str, replicate: int, target: int) -> tuple:
    """POWERBALL: (main: 7 ascending ints in 1..35, powerball: int in 1..20).
    OZLOTTO: (main: 7 ascending ints in 1..47, supplementaries: 3 ascending ints)."""
    s = _Stream(stream_key(root_hex, policy_id, game_id, replicate, target))
    size, main, supps, pb = GAMES[game_id]
    pool = list(range(1, size + 1))
    for i in range(main + supps):
        j = i + s.below(size - i)
        pool[i], pool[j] = pool[j], pool[i]
    if game_id == 'POWERBALL':
        return tuple(sorted(pool[:main])), 1 + s.below(pb)
    return tuple(sorted(pool[:main])), tuple(sorted(pool[main:main + supps]))


def fair_draws_for_targets(root_hex: str, policy_id: str, game_id: str, replicate: int, targets) -> list:
    return [fair_draw(root_hex, policy_id, game_id, replicate, t) for t in targets]
