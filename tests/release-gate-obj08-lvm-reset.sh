#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
reset="$ROOT/ansible/files/rhcsa-storage-reset"

echo "== OBJ08 interrupted-LVM reset contract =="

grep -q 'training_lvs=(' "$reset" || {
  echo "FAIL: reset does not explicitly enumerate training LVs."
  exit 1
}

grep -q '/dev/rhcsa_vgdata/rhcsa_lvdata' "$reset" || {
  echo "FAIL: reset does not cover obj08-09 LV."
  exit 1
}

grep -q 'lvchange -an' "$reset" || {
  echo "FAIL: reset does not deactivate LVs before removal."
  exit 1
}

grep -q 'lvremove -fy' "$reset" || {
  echo "FAIL: reset does not remove interrupted training LVs."
  exit 1
}

grep -q "grep '^rhcsa_'" "$reset" || {
  echo "FAIL: stale dm fallback is not constrained to rhcsa_*."
  exit 1
}

if grep -q 'if timeout 5s vgs "\$vg"' "$reset"; then
  echo "FAIL: reset still depends on VG discovery before cleanup."
  exit 1
fi

if grep -Ev '^[[:space:]]*#' "$reset" | grep -q 'rhel_servera'; then
  echo "FAIL: executable reset logic must never target the system VG."
  exit 1
fi

echo "OK: interrupted training LVM is explicitly deactivated and removed"
