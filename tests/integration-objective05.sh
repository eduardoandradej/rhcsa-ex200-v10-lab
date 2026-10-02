#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

echo "===== Objective 05 prerequisites ====="
(
    cd "$ROOT/ansible"
    ansible-playbook prepare-objective05.yml
)

exec "$ROOT/tests/integration-reference.sh" \
  obj05-01 obj05-02 obj05-03 obj05-04 obj05-05 \
  obj05-06 obj05-07 obj05-08 obj05-09 obj05-10
