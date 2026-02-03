# MIT License © 2025 Motohiro Suzuki
"""
qsp/session.py  (Stage178-A minimal)

Implements Claim A2 (Epoch monotonicity):
- Epoch MUST monotonically increase
- Epoch MUST NOT roll back

Design:
- advance_epoch() increments by exactly +1
- set_epoch() allows setting only to current+1 (strict monotone step)
"""

from __future__ import annotations


class EpochViolation(Exception):
    """Raised when epoch monotonicity is violated (fail-closed)."""


class SessionState:
    def __init__(self) -> None:
        self.epoch: int = 0

    def advance_epoch(self) -> int:
        """Advance epoch by exactly +1 and return new epoch."""
        self.epoch += 1
        return self.epoch

    def set_epoch(self, new_epoch: int) -> int:
        """
        Strict monotonic rule:
        - allow only new_epoch == current_epoch + 1
        - otherwise fail-closed
        """
        expected = self.epoch + 1
        if new_epoch != expected:
            raise EpochViolation(
                f"Epoch rollback/skip rejected (Claim A2): current={self.epoch}, "
                f"attempted={new_epoch}, expected={expected}"
            )
        self.epoch = new_epoch
        return self.epoch
