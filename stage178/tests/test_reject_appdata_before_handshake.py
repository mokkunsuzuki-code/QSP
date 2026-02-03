# MIT License © 2025 Motohiro Suzuki

import pytest

from qsp.minicore import MiniCore, ProtocolViolation


def test_reject_appdata_before_handshake():
    core = MiniCore(session_id=1)
    with pytest.raises(ProtocolViolation):
        core.accept_frame("APP_DATA", b"hello", claimed_session_id=1, claimed_epoch=0)
