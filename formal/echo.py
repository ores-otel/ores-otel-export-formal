#!/usr/bin/env python3
"""Language-neutral fmctl.adapter.v1 echo adapter for standalone e2e tests."""

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

    json.dump(
        {
            "protocol": "fmctl.adapter.v1",
            "success": True,
            "traces_total": len(traces),
            "traces_passed": len(traces),
            "mismatches": [],
            "implementation": {
                "language": adapter,
                "name": "formal-methods-fixture-echo",
                "version": "1",
            },
        },
        sys.stdout,
        separators=(",", ":"),
    )
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
