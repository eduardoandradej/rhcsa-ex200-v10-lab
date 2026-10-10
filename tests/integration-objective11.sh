#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

echo "===== Objective 11 prerequisites ====="
(
  cd "$ROOT/ansible"
  ansible-playbook prepare-objective11.yml
)

"$ROOT/tests/integration-reference.sh" \
  obj11-01 obj11-02 obj11-03 obj11-04 obj11-05 obj11-06

echo
echo "OBJ11 AUTOMATED INTEGRATION: PASS"
