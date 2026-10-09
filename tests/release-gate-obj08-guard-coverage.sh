#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

echo "== OBJ08 storage-guard coverage =="

for n in $(seq -w 2 12); do
  setup="$(find "$ROOT/labs/08-storage" -path "*/setup.yml" | sort | sed -n "$((10#$n))p")"
  : # ordering is not used below; check via lab id instead
done

for lab in "$ROOT/labs/08-storage"/*; do
  id="$(awk '/^id: /{print $2}' "$lab/lab.yml")"
  [[ "$id" == "obj08-01" ]] && continue

  grep -q 'rhcsa-storage-guard blank' "$lab/setup.yml" || {
    echo "FAIL: $id setup lacks blank-device safety guard"
    exit 1
  }

  grep -q 'rhcsa-storage-reset' "$lab/finish.yml" || {
    echo "FAIL: $id finish lacks guarded storage reset"
    exit 1
  }

  grep -q 'Save fstab baseline' "$lab/setup.yml" || {
    echo "FAIL: $id setup does not preserve /etc/fstab"
    exit 1
  }

  grep -q 'Restore fstab baseline' "$lab/finish.yml" || {
    echo "FAIL: $id finish does not restore /etc/fstab"
    exit 1
  }
done

echo "OK: all destructive OBJ08 labs are guarded and restore fstab"
