#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
playbook="$ROOT/ansible/prepare-objective03.yml"

echo "== OBJ03 local repository access contract =="

grep -q 'Ensure shared lab root is traversable for local repositories' "$playbook" || {
  echo "FAIL: prepare-objective03 does not manage shared-root traversal."
  exit 1
}
grep -q 'path: /var/lib/rhcsa-lab' "$playbook" || {
  echo "FAIL: shared lab root path is not explicit."
  exit 1
}
grep -q 'mode: "0711"' "$playbook" || {
  echo "FAIL: shared lab root is not configured as traverse-only 0711."
  exit 1
}
grep -q 'Verify base repository metadata is readable by student' "$playbook" || {
  echo "FAIL: base metadata readability is not verified as student."
  exit 1
}
grep -q 'Verify errata repository metadata is readable by student' "$playbook" || {
  echo "FAIL: errata metadata readability is not verified as student."
  exit 1
}
count="$(grep -c 'become_user: student' "$playbook")"
[[ "$count" -ge 2 ]] || {
  echo "FAIL: both repository readability probes must run as student."
  exit 1
}

echo "OK: OBJ03 repository path is traversable and metadata readability is verified as student"
