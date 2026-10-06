#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
echo "===== Objective 07 prerequisites ====="
( cd "$ROOT/ansible" && ansible-playbook prepare-objective07.yml )
exec "$ROOT/tests/integration-reference.sh" obj07-01 obj07-02 obj07-03 obj07-04 obj07-05 obj07-06 obj07-07 obj07-08
