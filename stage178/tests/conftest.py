# MIT License © 2025 Motohiro Suzuki
"""
tests/conftest.py  (Stage178-A)

Make project root importable in pytest.

Why:
- Some environments run tests with sys.path[0] pointing to tests/ directory,
  causing 'import qsp.core' to fail.
- Stage178-A requires deterministic CI behavior, so we force-add the repo root.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # stage178/
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
