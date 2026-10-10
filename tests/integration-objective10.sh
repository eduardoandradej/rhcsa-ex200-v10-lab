#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

echo "===== Objective 10 prerequisites ====="
(
  cd "$ROOT/ansible"
  ansible-playbook prepare-objective10.yml
)

"$ROOT/tests/integration-reference.sh" \
  obj10-01 obj10-02 obj10-03 obj10-04 obj10-05 \
  obj10-06 obj10-07 obj10-08 obj10-09

echo
echo "OBJ10 AUTOMATED INTEGRATION: PASS"
