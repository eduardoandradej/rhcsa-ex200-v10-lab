#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

echo "== OBJ08 protected system disk contract =="

targets=(
  "$ROOT/labs/08-storage"
  "$ROOT/tests/reference-solutions"
)

pattern='(mkfs(\.[[:alnum:]]+)?|mkswap|pvcreate|pvremove|wipefs|parted[[:space:]].*(mklabel|mkpart|rm)|dd[[:space:]].*of=)[^#\n]*/dev/vda([0-9]+)?'

if grep -RPsn "$pattern" "${targets[@]}" \
  --include='*.sh' --include='*.yml' --include='*.md' 2>/dev/null; then
  echo "FAIL: destructive command targets protected /dev/vda."
  exit 1
fi

guard="$ROOT/ansible/files/rhcsa-storage-guard"
prepare="$ROOT/ansible/prepare-objective08.yml"

test -f "$guard" || {
  echo "FAIL: missing OBJ08 storage guard helper: $guard"
  exit 1
}

grep -Fq '/dev/vda|/dev/vda*) die "/dev/vda and its children are permanently protected"' "$guard" || {
  echo "FAIL: storage guard does not carry the explicit /dev/vda deny rule."
  exit 1
}

grep -Fq '/usr/local/sbin/rhcsa-storage-guard protect /dev/vda' "$prepare" || {
  echo "FAIL: prepare-objective08 does not prove that /dev/vda is rejected."
  exit 1
}

grep -Fq 'failed_when: protected_disk_test.rc == 0' "$prepare" || {
  echo "FAIL: /dev/vda protection probe is not enforced as a negative test."
  exit 1
}

echo "OK: /dev/vda is hard-denied and the preflight proves the denial"
