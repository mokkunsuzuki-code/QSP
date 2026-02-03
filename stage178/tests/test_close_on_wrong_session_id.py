# MIT License © 2025 Motohiro Suzuki

import pytest

from qsp.minicore import MiniCore, ProtocolViolation


def test_close_on_wrong_session_id():
    core = MiniCore(session_id=123)

    # wrong session_id should fail-closed immediately
    with pytest.raises(ProtocolViolation):
        core.accept_frame("HS", claimed_session_id=999, claimed_epoch=0)
