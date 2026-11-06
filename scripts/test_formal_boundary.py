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


    def test_all_trace_inputs_fail_closed_with_one_mismatch_per_trace(self) -> None:
        traces = [f"synthetic/trace-{index:03}.itf.json" for index in range(64)]
        completed = subprocess.run(
            [sys.executable, str(FIXTURE)],
            input=json.dumps({"adapter": "rust", "traces": traces}),
            capture_output=True,
            check=False,
            text=True,
            timeout=5,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        response = json.loads(completed.stdout)
        self.assertEqual(response["protocol"], "fmctl.adapter.v1")
        self.assertIs(response["success"], False)
        self.assertEqual(response["traces_total"], len(traces))
        self.assertEqual(response["traces_passed"], 0)
        self.assertEqual([m["trace"] for m in response["mismatches"]], traces)
        self.assertTrue(
            all(m["actual"] == {"conformance": "not implemented"}
                for m in response["mismatches"])
        )

    def test_missing_identity_and_empty_trace_sets_cannot_certify_runtime(self) -> None:
        cases = [
            {"traces": ["synthetic/one.itf.json"]},
            {"adapter": "", "traces": ["synthetic/one.itf.json"]},
            {"adapter": "rust", "traces": []},
            {"adapter": "rust", "traces": None},
            {"adapter": "rust"},
        ]
        for request in cases:
            with self.subTest(request=request):
                completed = subprocess.run(
                    [sys.executable, str(FIXTURE)],
                    input=json.dumps(request),
                    capture_output=True,
                    check=False,
                    text=True,
                    timeout=5,
                )
                self.assertNotEqual(completed.returncode, 0)
                self.assertFalse(completed.stdout.strip())

    def test_adapter_label_cannot_turn_protocol_fixture_into_pass_evidence(self) -> None:
        for adapter in ["rust", "typescript", "java", "attolang", "wasm"]:
            with self.subTest(adapter=adapter):
                completed = subprocess.run(
                    [sys.executable, str(FIXTURE)],
                    input=json.dumps({
                        "adapter": adapter,
                        "traces": ["synthetic/check.itf.json"],
                    }),
                    capture_output=True,
                    check=False,
                    text=True,
                    timeout=5,
                )
                self.assertEqual(completed.returncode, 0, completed.stderr)
                result = json.loads(completed.stdout)
                self.assertIs(result["success"], False)
                self.assertEqual(result["traces_passed"], 0)
                self.assertEqual(len(result["mismatches"]), 1)
                self.assertEqual(result["implementation"]["language"], adapter)
                self.assertEqual(result["implementation"]["name"],
                                 "formal-methods-fail-closed-fixture")


if __name__ == "__main__":
    unittest.main()
