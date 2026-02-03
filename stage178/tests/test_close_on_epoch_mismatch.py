# MIT License © 2025 Motohiro Suzuki

import pytest

from qsp.minicore import MiniCore, ProtocolViolation


def test_close_on_epoch_mismatch():
    core = MiniCore(session_id=123)

    # correct handshake first
    core.accept_frame("HS", claimed_session_id=123, claimed_epoch=0)

    # advance local epoch to 1
    core.advance_epoch()
    assert core.s.epoch == 1

    # send frame with stale epoch (0) -> mismatch => fail-closed
    with pytest.raises(ProtocolViolation):
        core.accept_frame("APP_DATA", b"x", claimed_session_id=123, claimed_epoch=0)
