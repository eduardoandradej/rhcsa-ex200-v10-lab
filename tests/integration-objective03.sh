#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

echo "===== Objective 03 infrastructure ====="
(
  cd "$ROOT/ansible"
  ansible-playbook prepare-objective03.yml
)

exec "$ROOT/tests/integration-reference.sh" \
  obj03-01 obj03-02 obj03-03 obj03-04 \
  obj03-05 obj03-06 obj03-07 obj03-08
