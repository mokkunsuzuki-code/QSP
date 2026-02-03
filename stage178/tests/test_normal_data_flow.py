# MIT License © 2025 Motohiro Suzuki

from qsp.minicore import MiniCore


def test_normal_data_flow():
    core = MiniCore(session_id=123)

    # handshake (with correct session_id/epoch)
    r = core.accept_frame("HS", claimed_session_id=123, claimed_epoch=0)
    assert r == b"OK:HS"

    # app data allowed after handshake
    r2 = core.accept_frame("APP_DATA", b"hello", claimed_session_id=123, claimed_epoch=0)
    assert r2 == b"OK:APP_DATA:hello"
