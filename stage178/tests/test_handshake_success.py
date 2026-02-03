# MIT License © 2025 Motohiro Suzuki

from qsp.minicore import MiniCore


def test_handshake_success():
    core = MiniCore(session_id=1)
    r = core.accept_frame("HS", claimed_session_id=1, claimed_epoch=0)
    assert r == b"OK:HS"
    assert core.s.handshake_complete is True
