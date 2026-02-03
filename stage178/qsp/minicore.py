# MIT License © 2025 Motohiro Suzuki
"""
qsp/minicore.py  (Stage178-A minimal core)

Implements minimal, testable behaviors for:
- Claim A1: Handshake gating (no APP_DATA before handshake complete)
- Claim A3: Fail-closed on mismatch (wrong session_id or epoch mismatch => close)

Notes:
- This file is intentionally independent from the larger QSP implementation.
- Stage178-A wants deterministic CI "guarantee scaffolding" first.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


class ProtocolViolation(Exception):
    """Raised when protocol rules are violated (fail-closed)."""


@dataclass
class MiniSession:
    # Minimal session state for Stage178-A
    session_id: int
    epoch: int = 0
    handshake_complete: bool = False
    closed: bool = False

    def close(self, reason: str) -> None:
        self.closed = True
        raise ProtocolViolation(reason)


class MiniCore:
    """
    Minimal message handler.

    Frame schema (minimal):
      - HS: completes handshake, sets handshake_complete True
      - APP_DATA: requires handshake_complete True
      - Any frame can optionally include claimed session_id/epoch to be validated

    Fail-closed rules (Claim A3):
      - If provided session_id != local session.session_id -> close
      - If provided epoch != local session.epoch -> close
    """

    def __init__(self, session_id: int = 1) -> None:
        self.s = MiniSession(session_id=session_id, epoch=0, handshake_complete=False, closed=False)

    def server_handshake(self) -> bytes:
        if self.s.closed:
            self.s.close("Handshake rejected: session already closed")
        self.s.handshake_complete = True
        return b"OK:HS"

    def advance_epoch(self) -> int:
        if self.s.closed:
            self.s.close("Epoch advance rejected: session already closed")
        self.s.epoch += 1
        return self.s.epoch

    def _validate_mismatch(self, claimed_session_id: Optional[int], claimed_epoch: Optional[int]) -> None:
        if claimed_session_id is not None and claimed_session_id != self.s.session_id:
            self.s.close(f"Mismatch: wrong session_id (Claim A3) local={self.s.session_id} got={claimed_session_id}")
        if claimed_epoch is not None and claimed_epoch != self.s.epoch:
            self.s.close(f"Mismatch: wrong epoch (Claim A3) local={self.s.epoch} got={claimed_epoch}")

    def accept_frame(
        self,
        frame_type: str,
        payload: bytes = b"",
        *,
        claimed_session_id: Optional[int] = None,
        claimed_epoch: Optional[int] = None,
    ) -> bytes:
        if self.s.closed:
            self.s.close("Frame rejected: session already closed")

        # Claim A3: validate mismatch on every frame
        self._validate_mismatch(claimed_session_id, claimed_epoch)

        if frame_type == "HS":
            return self.server_handshake()

        if frame_type == "APP_DATA":
            # Claim A1: handshake gating
            if not self.s.handshake_complete:
                self.s.close("APP_DATA rejected: handshake not complete (Claim A1)")
            return b"OK:APP_DATA:" + payload

        # Unknown types: fail-closed
        self.s.close(f"Unknown frame_type rejected: {frame_type!r}")

        # unreachable
        return b""
