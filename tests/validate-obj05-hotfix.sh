#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

bash tests/release-gate.sh
bash tests/release-gate-obj05-portability.sh
bash tests/release-gate-obj05-ssh-background.sh
bash tests/release-gate-obj05-process-ownership.sh
bash tests/release-gate-obj05-tuned-verify.sh

echo
echo "OBJ05 HOTFIX VALIDATION: PASS"
