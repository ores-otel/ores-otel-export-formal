#!/usr/bin/env python3
"""Fail-closed schema-v1 shape check that does not require fmctl on PATH."""

from __future__ import annotations

import pathlib
import sys

try:
    import tomllib
except ImportError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "formal" / "fm.toml"
REQUIRED_TOP = (
    "schema_version",
    "project",
    "model",
    "language",
    "spec",
    "main",
    "init",
    "step",
    "invariants",
)
REQUIRED_LANGS = ("rust", "typescript", "dart", "gleam", "go")


def main() -> int:
    if not MANIFEST.is_file():
        print(f"missing {MANIFEST}", file=sys.stderr)
        return 2
    data = tomllib.loads(MANIFEST.read_text())
    missing = [key for key in REQUIRED_TOP if key not in data]
    if missing:
        print(f"manifest missing {missing}", file=sys.stderr)
        return 2
    if data["schema_version"] != 1:
        print("schema_version must be 1", file=sys.stderr)
        return 2
    if data["language"] != "quint":
        print("language must be quint", file=sys.stderr)
        return 2
    java = data.get("toolchain", {}).get("java")
    if not java:
        print("toolchain.java is required", file=sys.stderr)
        return 2
    spec = ROOT / data["spec"]
    if not spec.is_file():
        print(f"spec missing: {spec}", file=sys.stderr)
        return 2
    adapters = data.get("adapters")
    if not isinstance(adapters, dict):
        print("adapters table is required", file=sys.stderr)
        return 2
    for language in REQUIRED_LANGS:
        if language not in adapters:
            print(f"missing adapters.{language}", file=sys.stderr)
            return 2
    print(f"ok {data['project']} {data['model']} {spec.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
