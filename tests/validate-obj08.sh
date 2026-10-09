#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

bash tests/release-gate.sh
bash tests/release-gate-obj08-protected-disk.sh
bash tests/release-gate-obj08-guard-coverage.sh
bash tests/release-gate-obj08-targets.sh
bash tests/release-gate-obj08-bootstrap.sh
bash tests/release-gate-obj08-swap-identity.sh
bash tests/release-gate-obj08-reset-swap-identity.sh
bash tests/release-gate-obj08-bounded-setup.sh
bash tests/release-gate-obj08-bounded-reset.sh
bash tests/release-gate-obj08-lvm-reset.sh
bash tests/release-gate-obj08-timeout-containment.sh
bash tests/release-gate-obj08-lv-signatures.sh
bash tests/release-gate-obj08-grep-matchers.sh

echo
echo "OBJ08 VALIDATION: PASS"
