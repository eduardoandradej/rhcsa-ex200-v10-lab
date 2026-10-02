#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

exec "$ROOT/tests/integration-reference.sh" \
  obj04-01 obj04-02 obj04-03 obj04-04 \
  obj04-05 obj04-06 obj04-07 obj04-08
