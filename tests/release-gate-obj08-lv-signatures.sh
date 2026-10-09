#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

echo "== OBJ08 stale LV signature contract =="

for setup in \
  "$ROOT/labs/08-storage/08-lvm-xfs-persistent/setup.yml" \
  "$ROOT/labs/08-storage/09-lvextend-xfs/setup.yml" \
  "$ROOT/labs/08-storage/10-vgextend/setup.yml"
do
  if grep -q '\blvcreate\b' "$setup"; then
    grep -q -- '--wipesignatures' "$setup" || {
      echo "FAIL: $(basename "$(dirname "$setup")") lvcreate can prompt on stale signatures."
      exit 1
    }
  fi
done

bad="$(
  grep -RPsn '\blvcreate\b' "$ROOT/tests/reference-solutions" --include='obj08-*.sh' |
  grep -v -- '--wipesignatures y' || true
)"
if [[ -n "$bad" ]]; then
  echo "$bad"
  echo "FAIL: an OBJ08 reference lvcreate does not wipe stale signatures deterministically."
  exit 1
fi

reset="$ROOT/ansible/files/rhcsa-storage-reset"
grep -q 'wipe signatures on LV' "$reset" || {
  echo "FAIL: reset does not clear signatures from known training LVs."
  exit 1
}

grep -q 'wipefs -a -f "\$lv"' "$reset" || {
  echo "FAIL: reset lacks deterministic training-LV signature cleanup."
  exit 1
}

echo "OK: training LV reuse cannot trigger an interactive stale-signature prompt"
