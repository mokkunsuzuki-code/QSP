# MIT License © 2025 Motohiro Suzuki
"""
tests/test_attack_epoch_skip.py

Stage178-B Attack A-01: epoch skip / jump

Goal:
- After handshake, REKEY is only allowed for epoch == current_epoch + 1.
- Any attempt to jump (e.g., N -> N+2) must fail-closed (ProtocolViolation).
"""

import pytest

from qsp.minicore import MiniCore, ProtocolViolation


def test_reject_epoch_jump():
    """
    Attack: try to rekey with epoch jump (N -> N+2).
    Expected: ProtocolViolation("bad rekey epoch")
    """
    c = MiniCore()

    # handshake completes at epoch=1 (dict style requires epoch >= 1)
    r = c.accept_frame({"type": "HANDSHAKE_DONE", "session_id": 777, "epoch": 1, "payload": b""})
    assert r.ok is True
    assert r.epoch == 1

    # attacker tries to jump epoch to 3 (should be only 2)
    with pytest.raises(ProtocolViolation) as e:
        c.accept_frame({"type": "REKEY", "session_id": 777, "epoch": 3, "payload": b"evil"})

    assert "bad rekey epoch" in str(e.value)


def test_reject_epoch_rollback_on_app_data():
    """
    Attack: send APP_DATA with old epoch (rollback).
    Expected: ProtocolViolation("epoch mismatch")
    """
    c = MiniCore()
    c.accept_frame({"type": "HANDSHAKE_DONE", "session_id": 888, "epoch": 1, "payload": b""})

    # legal rekey to epoch=2
    r2 = c.accept_frame({"type": "REKEY", "session_id": 888, "epoch": 2, "payload": b"ok"})
    assert r2.ok is True
    assert r2.epoch == 2

    # attacker sends APP_DATA with epoch=1 (rollback)
    with pytest.raises(ProtocolViolation) as e:
        c.accept_frame({"type": "APP_DATA", "session_id": 888, "epoch": 1, "payload": b"msg"})

    assert "epoch mismatch" in str(e.value)
