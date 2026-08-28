# ores-otel-export-formal

Product-owned formal methods for `ores-otel`. The reusable runner, batch
protocol (`fmctl.adapter.v1`), and streaming protocol (`fm.adapter.stream.v1`)
live in [ORESoftware/formal-methods.rs](https://github.com/ORESoftware/formal-methods.rs).
This repository keeps the Quint model and adapter slots beside `ores-otel` code.

Model: `export_bound` (`formal/export_bound.qnt`), invariant `queue_within_capacity`.

## Commands

From a machine that has the shared runner cloned at
`~/codes/oresoftware/formal-methods.rs`:

```bash
python3 scripts/validate_manifest.py
scripts/run-fmctl.sh validate
scripts/run-fmctl.sh --dry-run plan check
```

Replay through the language-neutral echo adapter (fixture ITF, not a product trace):

```bash
scripts/run-fmctl.sh replay --adapter rust --trace formal/trace-0.itf.json
```

The echo adapter does not interpret ITF; it only proves `fmctl.adapter.v1`
wiring. Product adapters must compare canonical observable state.

## Linear

Parent platform issue: [DEN-565](https://linear.app/denman/issue/DEN-565).
Shared runner: [DEN-580](https://linear.app/denman/issue/DEN-580).
