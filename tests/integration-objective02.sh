#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
exec "$ROOT/tests/integration-reference.sh"   obj02-01 obj02-02 obj02-03 obj02-04   obj02-05 obj02-06 obj02-07 obj02-08
