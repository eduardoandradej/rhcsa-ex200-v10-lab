#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
bash tests/release-gate.sh
bash tests/release-gate-obj06-network-safety.sh
bash tests/release-gate-obj06-routing-contract.sh
bash tests/release-gate-obj06-ipv6-grader.sh
bash tests/release-gate-obj06-keyfile-permissions.sh
echo
echo "OBJ06 VALIDATION: PASS"
