#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

bash tests/release-gate.sh
bash tests/release-gate-obj10-security.sh

echo
echo "OBJ10 VALIDATION: PASS"
