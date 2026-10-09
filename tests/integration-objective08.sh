#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

echo "===== Objective 08 safety/prerequisites ====="
(
  cd "$ROOT/ansible"
  ansible-playbook prepare-objective08.yml
)

exec "$ROOT/tests/integration-reference.sh" \
  obj08-01 obj08-02 obj08-03 obj08-04 obj08-05 obj08-06 \
  obj08-07 obj08-08 obj08-09 obj08-10 obj08-11 obj08-12
