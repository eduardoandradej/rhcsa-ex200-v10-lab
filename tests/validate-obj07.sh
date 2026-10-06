#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
bash tests/release-gate.sh
bash tests/release-gate-obj07-privileged-files.sh
bash tests/release-gate-obj07-cleanup.sh
bash tests/release-gate-obj07-tmpfiles-permissions.sh
bash tests/release-gate-obj07-tmpfiles-age.sh
echo; echo "OBJ07 VALIDATION: PASS"
