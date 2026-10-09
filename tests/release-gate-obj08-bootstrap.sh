#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

echo "== OBJ08 safety bootstrap contract =="

for helper in rhcsa-storage-guard rhcsa-storage-reset; do
  test -f "$ROOT/ansible/files/$helper" || {
    echo "FAIL: missing reusable helper ansible/files/$helper"
    exit 1
  }
done

for lab in "$ROOT/labs/08-storage"/*; do
  id="$(awk '/^id: /{print $2}' "$lab/lab.yml")"

  grep -q 'Install OBJ08 storage guard' "$lab/setup.yml" || {
    echo "FAIL: $id cannot bootstrap rhcsa-storage-guard by itself"
    exit 1
  }

  grep -q 'Install OBJ08 storage reset utility' "$lab/setup.yml" || {
    echo "FAIL: $id cannot bootstrap rhcsa-storage-reset by itself"
    exit 1
  }
done

grep -Fq 'rhcsa-storage-guard protect {{ item }}' \
  "$ROOT/ansible/prepare-objective08.yml" || {
    echo "FAIL: prepare-objective08 scratch loop has invalid Jinja syntax"
    exit 1
}

grep -q "grep -q '^obj08-'" "$ROOT/tests/integration-reference.sh" || {
  echo "FAIL: targeted OBJ08 reference runs do not execute the objective preflight"
  exit 1
}

echo "OK: every OBJ08 lab self-bootstraps safety helpers"
