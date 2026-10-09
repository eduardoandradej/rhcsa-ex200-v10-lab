#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

echo "== OBJ08 swap identity contract =="

for folder in 05-swap-partition 06-basic-integrated 11-lvm-swap 12-integrated-lvm; do
  grader="$ROOT/labs/08-storage/$folder/grade.py"
  setup="$ROOT/labs/08-storage/$folder/setup.yml"

  grep -q 'active_swap_uuids' "$grader" || {
    echo "FAIL: $folder grader does not identify active swap by UUID"
    exit 1
  }

  grep -q 'baseline_swap_uuids' "$grader" || {
    echo "FAIL: $folder grader does not verify baseline swap preservation"
    exit 1
  }

  grep -q 'Save active swap UUID baseline' "$setup" || {
    echo "FAIL: $folder setup does not record baseline swap UUIDs"
    exit 1
  }
done

if grep -Rqs --include='grade.py' 'swapon.*--show=NAME,UUID' "$ROOT/labs/08-storage"; then
  echo "FAIL: unsupported swapon UUID output-column dependency found"
  exit 1
fi

echo "OK: swap state uses blkid UUID identity and preserves baseline swaps"
