#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

bash tests/release-gate.sh
bash tests/release-gate-obj11-nfs-autofs.sh

echo
echo "OBJ11 VALIDATION: PASS"
