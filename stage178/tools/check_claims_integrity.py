# MIT License © 2025 Motohiro Suzuki
"""
tools/check_claims_integrity.py  (Stage178-A)

Purpose:
- Validate that claims/claims.yml is parseable.
- Validate that each Claim row references real artifacts:
  - formal_model.file exists
  - implementation.file exists
  - all tests.positive / tests.negative files exist
- (Optional) Validate that formal_model.lemma name appears in the model file text
  - This is a lightweight check (string search), not a proof run.

Exit code:
- 0 if all checks pass
- 2 if any integrity check fails

Usage:
  python tools/check_claims_integrity.py
  python tools/check_claims_integrity.py --strict-lemma
  python tools/check_claims_integrity.py --root /path/to/stage178
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    import yaml  # type: ignore
except Exception as e:
    print("[FATAL] PyYAML is not installed. Install it via: python -m pip install pyyaml")
    raise


def _read_yaml(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            raise ValueError("claims.yml root must be a YAML mapping (dict).")
        return data
    except Exception as e:
        raise RuntimeError(f"Failed to parse YAML: {path} ({e})") from e


def _as_list(v: Any) -> List[str]:
    if v is None:
        return []
    if isinstance(v, list):
        out: List[str] = []
        for x in v:
            if isinstance(x, str):
                out.append(x)
            else:
                out.append(str(x))
        return out
    if isinstance(v, str):
        return [v]
    return [str(v)]


def _check_file_exists(root: Path, rel_path: str) -> Tuple[bool, str]:
    # allow absolute paths, but prefer relative
    p = Path(rel_path)
    full = p if p.is_absolute() else (root / p)
    if full.exists() and full.is_file():
        return True, str(full)
    return False, str(full)


def _find_lemma_in_model(model_file: Path, lemma_name: str) -> bool:
    # lightweight string presence check
    try:
        text = model_file.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return False
    return lemma_name in text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="project root (default: current dir)")
    ap.add_argument("--claims", default="claims/claims.yml", help="claims.yml path from root")
    ap.add_argument(
        "--strict-lemma",
        action="store_true",
        help="also require that formal_model.lemma name appears in model file text",
    )
    args = ap.parse_args()

    root = Path(args.root).resolve()
    claims_path = (root / args.claims).resolve()

    if not claims_path.exists():
        print(f"[FAIL] claims file not found: {claims_path}")
        return 2

    data = _read_yaml(claims_path)

    claims = data.get("claims")
    if not isinstance(claims, list):
        print("[FAIL] claims.yml must contain top-level key 'claims:' as a list")
        return 2

    failures: List[str] = []
    warnings: List[str] = []

    def fail(msg: str) -> None:
        failures.append(msg)

    def warn(msg: str) -> None:
        warnings.append(msg)

    seen_ids: set[str] = set()

    for i, c in enumerate(claims):
        if not isinstance(c, dict):
            fail(f"Claim index {i}: must be a mapping")
            continue

        cid = str(c.get("id", "")).strip()
        if not cid:
            fail(f"Claim index {i}: missing 'id'")
            continue
        if cid in seen_ids:
            fail(f"Claim {cid}: duplicate id")
        seen_ids.add(cid)

        # formal model file + lemma
        fm = c.get("formal_model", {})
        if not isinstance(fm, dict):
            fail(f"Claim {cid}: formal_model must be a mapping")
            fm = {}

        fm_file = str(fm.get("file", "")).strip()
        fm_lemma = str(fm.get("lemma", "")).strip()

        if not fm_file:
            fail(f"Claim {cid}: formal_model.file is missing")
        else:
            ok, resolved = _check_file_exists(root, fm_file)
            if not ok:
                fail(f"Claim {cid}: formal_model.file not found: {fm_file} -> {resolved}")
            else:
                if args.strict_lemma:
                    if not fm_lemma:
                        fail(f"Claim {cid}: formal_model.lemma is missing (strict-lemma enabled)")
                    else:
                        if not _find_lemma_in_model(Path(resolved), fm_lemma):
                            fail(
                                f"Claim {cid}: lemma name not found in model file text: "
                                f"{fm_lemma} (file: {fm_file})"
                            )
                else:
                    if not fm_lemma:
                        warn(f"Claim {cid}: formal_model.lemma is empty (non-strict mode)")

        # implementation anchor file
        impl = c.get("implementation", {})
        if not isinstance(impl, dict):
            fail(f"Claim {cid}: implementation must be a mapping")
            impl = {}

        impl_file = str(impl.get("file", "")).strip()
        if not impl_file:
            fail(f"Claim {cid}: implementation.file is missing")
        else:
            ok, resolved = _check_file_exists(root, impl_file)
            if not ok:
                fail(f"Claim {cid}: implementation.file not found: {impl_file} -> {resolved}")

        # tests
        tests = c.get("tests", {})
        if not isinstance(tests, dict):
            fail(f"Claim {cid}: tests must be a mapping")
            tests = {}

        pos = _as_list(tests.get("positive"))
        neg = _as_list(tests.get("negative"))

        if not pos:
            warn(f"Claim {cid}: tests.positive is empty")
        if not neg:
            fail(f"Claim {cid}: tests.negative MUST NOT be empty (Stage178-A requirement)")

        for p in pos:
            ok, resolved = _check_file_exists(root, p)
            if not ok:
                fail(f"Claim {cid}: tests.positive missing: {p} -> {resolved}")

        for p in neg:
            ok, resolved = _check_file_exists(root, p)
            if not ok:
                fail(f"Claim {cid}: tests.negative missing: {p} -> {resolved}")

    if warnings:
        print("[WARN] non-fatal issues:")
        for w in warnings:
            print(f"  - {w}")

    if failures:
        print("[FAIL] integrity check failed:")
        for f in failures:
            print(f"  - {f}")
        return 2

    print(f"[OK] claims integrity passed: {len(claims)} claims checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
