# MIT License © 2025 Motohiro Suzuki

from qsp.session import SessionState


def test_epoch_increase():
    s = SessionState()
    assert s.epoch == 0
    assert s.advance_epoch() == 1
    assert s.advance_epoch() == 2
    assert s.epoch == 2
