#!/bin/sh
set -eu
root="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
candidates="
${FORMAL_METHODS_RS:-}
${root}/../formal-methods.rs
${root}/../../oresoftware/formal-methods.rs
${HOME}/codes/oresoftware/formal-methods.rs
"
fmctl=""
for candidate in $candidates; do
  [ -n "$candidate" ] || continue
  manifest="${candidate}/tools/fmctl/Cargo.toml"
  if [ -f "$manifest" ]; then
    exec cargo run --locked --quiet --manifest-path "$manifest" --bin fmctl -- --workspace "$root" "$@"
  fi
  if [ -x "${candidate}/tools/fmctl/target/release/fmctl" ]; then
    exec "${candidate}/tools/fmctl/target/release/fmctl" --workspace "$root" "$@"
  fi
done
echo "fmctl not found; clone ORESoftware/formal-methods.rs or set FORMAL_METHODS_RS" >&2
exit 4
