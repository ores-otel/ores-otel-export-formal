#!/usr/bin/env python3
"""Fail-closed fmctl.adapter.v1 protocol fixture.

This fixture deliberately cannot certify product conformance because it does not
execute an ores-otel runtime or compare observable state. It remains useful for
checking the response envelope without creating a false proof claim.
"""

from __future__ import annotations

import json
import sys


def main() -> None:
    request = json.load(sys.stdin)
    adapter = request.get("adapter")
    traces = request.get("traces") or []
    if not adapter:
        raise SystemExit("adapter name missing from fmctl.adapter.v1 request")
    if not traces:
        raise SystemExit("replay request must contain at least one trace")

    mismatches = [
        {
            "trace": trace,
            "step": None,
            "action": None,
            "message": "protocol fixture cannot compare product observable state",
            "expected": {"conformance": "product runtime comparison"},
            "actual": {"conformance": "not implemented"},
        }
        for trace in traces
    ]

    json.dump(
        {
            "protocol": "fmctl.adapter.v1",
            "success": False,
            "traces_total": len(traces),
            "traces_passed": 0,
            "mismatches": mismatches,
            "implementation": {
                "language": adapter,
                "name": "formal-methods-fail-closed-fixture",
                "version": "1",
            },
        },
        sys.stdout,
        separators=(",", ":"),
    )
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
