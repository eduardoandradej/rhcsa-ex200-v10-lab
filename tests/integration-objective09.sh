#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

echo "===== Objective 09 prerequisites ====="
(
  cd "$ROOT/ansible"
  ansible-playbook prepare-objective09.yml
)

"$ROOT/tests/integration-reference.sh" \
  obj09-01 obj09-02 obj09-03 obj09-05 obj09-07

echo
echo "OBJ09 AUTOMATED INTEGRATION: PASS"
echo "NOTE: obj09-04 and obj09-06 are manual-console drills and are intentionally excluded."
