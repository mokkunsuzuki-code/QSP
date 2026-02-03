# MIT License © 2025 Motohiro Suzuki
"""
protocol/core.py  (Stage178-A minimal)

Minimal protocol core to prove Claim A1 (Handshake gating) via tests.

Claim A1:
- Application data MUST NOT be accepted before a successful handshake completes.

This is intentionally tiny:
- "handshake" just flips a boolean
- "APP_DATA" is rejected unless handshake_complete == True
"""

from __future__ import annotations

from dataclasses import dataclass


class ProtocolViolation(Exception):
    """Raised when protocol rules are violated (fail-closed behavior)."""


@dataclass
class ProtocolCore:
    handshake_complete: bool = False

    def server_handshake(self) -> None:
        """
        Minimal handshake:
        - In real QSP this would verify signatures, derive keys, etc.
        - Here we only mark the session as 'handshake complete'.
        """
        self.handshake_complete = True

    def accept_frame(self, frame_type: str, payload: bytes = b"") -> bytes:
        """
        Accept a frame. For Stage178-A minimal:
        - HS: completes handshake
        - APP_DATA: only allowed after handshake_complete
        """
        if frame_type == "HS":
            self.server_handshake()
            return b"OK:HS"

        if frame_type == "APP_DATA":
            if not self.handshake_complete:
                # fail-closed
                raise ProtocolViolation("APP_DATA rejected: handshake not complete (Claim A1)")
            return b"OK:APP_DATA:" + payload

        # Unknown frame types are rejected (fail-closed)
        raise ProtocolViolation(f"Unknown frame_type rejected: {frame_type!r}")
