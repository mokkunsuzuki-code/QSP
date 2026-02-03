# MIT License © 2025 Motohiro Suzuki
"""
tests/test_attack_downgrade_detected.py

Stage178-B Attack A-06: downgrade detected
"""

import pytest

from qsp.minicore import MiniCore, ProtocolViolation


def test_detect_downgrade_on_rekey_mode_change():
    c = MiniCore()
    c.accept_frame({"type": "HANDSHAKE_DONE", "session_id": 6060, "epoch": 1, "mode": "PQC+QKD", "payload": b""})

    with pytest.raises(ProtocolViolation) as e:
        c.accept_frame({"type": "REKEY", "session_id": 6060, "epoch": 2, "mode": "PQC_ONLY", "payload": b"x"})

    assert "downgrade detected" in str(e.value)


def test_allow_same_mode_after_handshake():
    c = MiniCore()
    c.accept_frame({"type": "HANDSHAKE_DONE", "session_id": 6061, "epoch": 1, "mode": "PQC+QKD", "payload": b""})

    r2 = c.accept_frame({"type": "REKEY", "session_id": 6061, "epoch": 2, "mode": "PQC+QKD", "payload": b"ok"})
    assert r2.ok is True
    assert r2.epoch == 2
