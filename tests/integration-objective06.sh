#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
echo "===== Objective 06 prerequisites ====="
(cd "$ROOT/ansible" && ansible-playbook prepare-objective06.yml)
exec "$ROOT/tests/integration-reference.sh" obj06-01 obj06-02 obj06-03 obj06-04 obj06-05 obj06-06 obj06-07 obj06-08
