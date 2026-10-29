"""Coordinator side of the E_2-readiness dispatch gate (E2R-CODE-2; E2R-R57, E2R-T14).

The coordinator has no coordinated contract-method dispatch yet: scientific coordination is switched
off and the coordinated science allowlist is empty. This is the single entry point any future
coordinated contract dispatch must use. It applies exactly the standalone runner's gate, so a request
the gate refuses gets the same rule and the same refusal text from both launchers. A request the gate
admits is then refused here too, because coordinated contract runs are not enabled. It reads no data,
starts nothing and writes nothing. Replacing the final refusal is a separate, reviewed package.
"""
from __future__ import annotations

from collections.abc import Mapping

from _common.contract_dispatch import DispatchRefused, dispatch_gate, refusal_text


def gate_coordinated_contract_request(request: Mapping) -> None:
    """Always raises DispatchRefused in CODE-2: first the shared gate's own refusal, if any; otherwise
    COORDINATED_CONTRACT_DISPATCH_NOT_ENABLED."""
    dispatch_gate(request)
    r = request
    raise DispatchRefused(refusal_text(r['game_id'], r['method_id'], r['variant_id'], r['method_revision'],
                                       'COORDINATED_CONTRACT_DISPATCH_NOT_ENABLED: coordinated contract runs '
                                       'are not implemented or enabled'),
                          'COORDINATED_CONTRACT_DISPATCH_NOT_ENABLED')
