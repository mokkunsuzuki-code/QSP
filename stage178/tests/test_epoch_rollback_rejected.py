# MIT License © 2025 Motohiro Suzuki

import pytest

from qsp.session import SessionState, EpochViolation


def test_epoch_rollback_rejected():
    s = SessionState()
    s.advance_epoch()  # epoch = 1
    s.advance_epoch()  # epoch = 2

    # rollback attempt (2 -> 1) must fail
    with pytest.raises(EpochViolation):
        s.set_epoch(1)


def test_epoch_skip_rejected():
    s = SessionState()
    s.advance_epoch()  # epoch = 1

    # skip attempt (1 -> 3) must fail
    with pytest.raises(EpochViolation):
        s.set_epoch(3)
