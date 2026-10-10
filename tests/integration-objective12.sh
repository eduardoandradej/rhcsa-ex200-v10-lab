#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

echo "===== Objective 12 prerequisites ====="
(
  cd "$ROOT/ansible"
  ansible-playbook prepare-objective08.yml
  ansible-playbook prepare-objective10.yml
  ansible-playbook prepare-objective11.yml
  ansible-playbook prepare-objective12.yml
)

"$ROOT/tests/integration-reference.sh" \
  obj12-01 obj12-02 obj12-03 obj12-04 obj12-05 obj12-06

echo
echo "OBJ12 AUTOMATED INTEGRATION: PASS"
