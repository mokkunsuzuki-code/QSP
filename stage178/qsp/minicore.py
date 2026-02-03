# MIT License © 2025 Motohiro Suzuki
"""
qsp/minicore.py (Stage178-A/B minimal core)

This file is intentionally *test-compatible* with two call styles found in this repo:

(1) Old style:
    core = MiniCore(session_id=123)
    core.accept_frame("HS", claimed_session_id=123, claimed_epoch=0) -> b"OK:HS"
    core.accept_frame("APP_DATA", b"hello", claimed_session_id=123, claimed_epoch=0) -> b"OK:APP_DATA:hello"
    core.advance_epoch()

(2) Dict style:
    c = MiniCore()
    c.accept_frame({"type":"HANDSHAKE_DONE","session_id":777,"epoch":1,"payload":b""}) -> MiniResult(...)
    c.accept_frame({"type":"REKEY",...}) -> MiniResult(...)
    c.accept_frame({"type":"APP_DATA",...}) -> MiniResult(...)

Stage178-B addition (minimal):
- downgrade detection via "mode" pinning:
  handshake pins session.mode; subsequent frames must not change it.
  If changed -> fail-closed "downgrade detected".
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Optional, Any, Dict


class ProtocolViolation(Exception):
    """Raised when protocol rules are violated (fail-closed)."""
    pass


def _h(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


@dataclass
class MiniResult:
    ok: bool
    detail: str
    epoch: int
    session_id: int
    key_fingerprint_hex: str


@dataclass
class MiniSession:
    expected_session_id: Optional[int] = None

    session_id: int = 0
    epoch: int = 0
    handshake_complete: bool = False
    closed: bool = False
    key_material: bytes = b"init"

    # Stage178-B: downgrade detection (pinned at handshake)
    mode: Optional[str] = None  # e.g., "PQC+QKD" or "PQC_ONLY"

    def fingerprint_hex(self) -> str:
        return hashlib.sha256(self.key_material).hexdigest()

    def close(self, reason: str) -> None:
        self.closed = True
        raise ProtocolViolation(reason)


class MiniCore:
    def __init__(self, session_id: Optional[int] = None):
        # If provided, tests treat it as an expected session_id.
        self.s = MiniSession(expected_session_id=session_id)

    # --- helper expected by some tests ---
    def advance_epoch(self) -> None:
        """Advance local epoch by 1 (used by epoch-mismatch unit test)."""
        if not self.s.handshake_complete:
            self.s.close("before handshake")
        self.s.epoch += 1
        # Evolve key material deterministically as epoch changes
        self.s.key_material = _h(self.s.key_material + b"advance" + self.s.epoch.to_bytes(8, "big", signed=True))

    # --- unified accept_frame supporting both call styles ---
    def accept_frame(
        self,
        ft_or_frame: Any,
        payload: Any = None,
        *,
        claimed_session_id: int = None,
        claimed_epoch: int = None,
    ):
        # Branch by call style:
        # - dict style: accept_frame({..})
        # - old style : accept_frame("HS", ..., claimed_session_id=..., claimed_epoch=...)
        if isinstance(ft_or_frame, dict):
            return self._accept_dict_frame(ft_or_frame)
        if isinstance(ft_or_frame, str):
            return self._accept_old_style(ft_or_frame, payload, claimed_session_id=claimed_session_id, claimed_epoch=claimed_epoch)
        self.s.close("Invalid frame input")

    # -------------------------
    # downgrade guard (dict)
    # -------------------------
    def _guard_mode_dict(self, frame: Dict[str, Any]) -> None:
        """
        Stage178-B: detect downgrade by pinning 'mode' at handshake.
        - If frame contains 'mode' and it conflicts with pinned -> fail-closed.
        - If pinned exists and frame omits 'mode', do nothing (backward compatible).
        """
        mode = frame.get("mode")
        if mode is None:
            return
        if not isinstance(mode, str):
            self.s.close("Invalid mode")
        if self.s.mode is None:
            # Only pinned at handshake
            return
        if mode != self.s.mode:
            self.s.close("downgrade detected")

    # -------------------------
    # dict style implementation
    # -------------------------
    def _accept_dict_frame(self, frame: Dict[str, Any]) -> MiniResult:
        ft = frame.get("type") or frame.get("frame_type")
        if not isinstance(ft, str):
            self.s.close("Missing frame type")

        sid = frame.get("session_id")
        epoch = frame.get("epoch")
        payload_b = frame.get("payload", b"")
        if payload_b is None:
            payload_b = b""
        if isinstance(payload_b, bytearray):
            payload_b = bytes(payload_b)

        if not isinstance(sid, int) or not isinstance(epoch, int):
            self.s.close("Invalid session_id or epoch")
        if not isinstance(payload_b, (bytes, bytearray)):
            self.s.close("Invalid payload")

        if ft == "HANDSHAKE_DONE":
            if self.s.handshake_complete:
                self.s.close("Duplicate handshake")
            if epoch < 1:
                self.s.close("Handshake epoch must be >= 1")
            if self.s.expected_session_id is not None and sid != self.s.expected_session_id:
                self.s.close("session mismatch")

            # Stage178-B: pin mode at handshake if provided, else default
            mode = frame.get("mode", "PQC+QKD")
            if not isinstance(mode, str):
                self.s.close("Invalid mode")
            self.s.mode = mode

            self.s.session_id = sid
            self.s.epoch = epoch
            self.s.handshake_complete = True
            self.s.key_material = _h(b"hs" + sid.to_bytes(8, "big") + epoch.to_bytes(8, "big", signed=True) + mode.encode("utf-8"))
            return MiniResult(True, "handshake", self.s.epoch, self.s.session_id, self.s.fingerprint_hex())

        if not self.s.handshake_complete:
            self.s.close("before handshake")

        # Stage178-B: downgrade guard (only after handshake)
        self._guard_mode_dict(frame)

        if sid != self.s.session_id:
            self.s.close("session mismatch")

        if ft == "REKEY":
            if epoch != self.s.epoch + 1:
                self.s.close("bad rekey epoch")
            self.s.epoch = epoch
            self.s.key_material = _h(self.s.key_material + b"rekey" + epoch.to_bytes(8, "big", signed=True) + bytes(payload_b))
            return MiniResult(True, "rekey", self.s.epoch, self.s.session_id, self.s.fingerprint_hex())

        if ft == "APP_DATA":
            if epoch != self.s.epoch:
                self.s.close("epoch mismatch")
            return MiniResult(True, "app", self.s.epoch, self.s.session_id, self.s.fingerprint_hex())

        self.s.close("unknown frame")

    # -------------------------
    # downgrade guard (old style)
    # -------------------------
    def _guard_mode_old(self, payload_b: bytes) -> None:
        """
        Old-style has no structured field, but we allow an optional marker:
        payload starting with b"MODE:" + utf-8 text.
        If pinned mode exists and marker conflicts -> fail-closed.
        This keeps old tests working (they don't use MODE:).
        """
        if not payload_b.startswith(b"MODE:"):
            return
        try:
            mode = payload_b[5:].decode("utf-8", errors="strict")
        except Exception:
            self.s.close("Invalid mode")
        if self.s.mode is None:
            return
        if mode != self.s.mode:
            self.s.close("downgrade detected")

    # -------------------------
    # old style implementation
    # -------------------------
    def _accept_old_style(self, ft: str, payload: Any, *, claimed_session_id: int, claimed_epoch: int) -> bytes:
        if not isinstance(claimed_session_id, int) or not isinstance(claimed_epoch, int):
            self.s.close("Invalid claimed_session_id or claimed_epoch")

        # normalize payload
        if payload is None:
            payload_b = b""
        elif isinstance(payload, (bytes, bytearray)):
            payload_b = bytes(payload)
        else:
            self.s.close("Invalid payload")

        if ft == "HS":
            if self.s.handshake_complete:
                self.s.close("Duplicate handshake")
            if self.s.expected_session_id is not None and claimed_session_id != self.s.expected_session_id:
                self.s.close("session mismatch")

            # tests use epoch=0 at HS time
            if claimed_epoch < 0:
                self.s.close("bad epoch")

            # Stage178-B: pin default mode for old style handshake
            self.s.mode = "PQC+QKD"

            self.s.session_id = claimed_session_id
            self.s.epoch = claimed_epoch
            self.s.handshake_complete = True
            self.s.key_material = _h(
                b"hs"
                + claimed_session_id.to_bytes(8, "big")
                + claimed_epoch.to_bytes(8, "big", signed=True)
                + self.s.mode.encode("utf-8")
            )
            return b"OK:HS"

        if not self.s.handshake_complete:
            self.s.close("before handshake")

        # Stage178-B: optional downgrade guard via MODE: marker
        self._guard_mode_old(payload_b)

        if claimed_session_id != self.s.session_id:
            self.s.close("session mismatch")

        if ft == "REKEY":
            if claimed_epoch != self.s.epoch + 1:
                self.s.close("bad rekey epoch")
            self.s.epoch = claimed_epoch
            self.s.key_material = _h(self.s.key_material + b"rekey" + claimed_epoch.to_bytes(8, "big", signed=True) + payload_b)
            return b"OK:REKEY"

        if ft == "APP_DATA":
            if claimed_epoch != self.s.epoch:
                self.s.close("epoch mismatch")
            return b"OK:APP_DATA:" + bytes(payload_b)

        self.s.close("unknown frame")
