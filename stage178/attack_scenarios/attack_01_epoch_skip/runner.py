# MIT License © 2025 Motohiro Suzuki
"""
attack_scenarios/attack_01_epoch_skip/runner.py

Stage178-B Attack A-01: epoch skip / jump

This runner simulates an attacker trying to REKEY with epoch jump.
Expected secure behavior: fail-closed (ProtocolViolation).
Exit code:
- 0 if attack is correctly rejected
- 1 if attack is (incorrectly) accepted
"""

from qsp.minicore import MiniCore, ProtocolViolation


def main() -> int:
    c = MiniCore()

    # handshake completes at epoch=1
    c.accept_frame({"type": "HANDSHAKE_DONE", "session_id": 777, "epoch": 1, "payload": b""})

    try:
        # attacker tries jump to epoch=3
        c.accept_frame({"type": "REKEY", "session_id": 777, "epoch": 3, "payload": b"evil"})
    except ProtocolViolation as e:
        msg = str(e)
        if "bad rekey epoch" in msg:
            print("[OK] attack rejected:", msg)
            return 0
        print("[FAIL] rejected, but unexpected reason:", msg)
        return 1

    print("[FAIL] attack was accepted (should have been rejected)")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
