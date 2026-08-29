#!/usr/bin/env python3
"""Regression tests for the fail-closed formal adapter boundary."""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import unittest

try:
    import tomllib
except ImportError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "formal" / "fm.toml"
FIXTURE = ROOT / "formal" / "echo.py"


class FormalBoundaryTests(unittest.TestCase):
    def test_non_conforming_fixture_is_not_an_active_adapter(self) -> None:
        manifest = tomllib.loads(MANIFEST.read_text())
        rust_adapter = manifest["adapters"]["rust"]

        self.assertEqual(rust_adapter["status"], "planned")
        self.assertNotIn("command", rust_adapter)

    def test_protocol_fixture_reports_a_mismatch(self) -> None:
        trace = "formal/trace-0.itf.json"
        completed = subprocess.run(
            [sys.executable, str(FIXTURE)],
            input=json.dumps({"adapter": "rust", "traces": [trace]}),
            capture_output=True,
            check=False,
            text=True,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        response = json.loads(completed.stdout)
        self.assertFalse(response["success"])
        self.assertEqual(response["traces_total"], 1)
        self.assertEqual(response["traces_passed"], 0)
        self.assertEqual(len(response["mismatches"]), 1)
        self.assertEqual(response["mismatches"][0]["trace"], trace)


if __name__ == "__main__":
    unittest.main()

