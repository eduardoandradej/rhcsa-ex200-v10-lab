#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
reset="$ROOT/ansible/files/rhcsa-storage-reset"

echo "== OBJ08 reset swap identity contract =="

grep -q 'training_swap_labels=(' "$reset" || {
  echo "FAIL: reset has no allowlist of OBJ08 swap labels."
  exit 1
}

for label in RHCSA08SWAP BASWAP08 LVSWAP08 FINALSWAP08; do
  grep -q "$label" "$reset" || {
    echo "FAIL: reset swap-label allowlist is missing $label."
    exit 1
  }
done

grep -q 'swapon --show=NAME --noheadings --raw' "$reset" || {
  echo "FAIL: reset does not enumerate the actual active swap device names."
  exit 1
}

grep -q 'blkid -s LABEL -o value "\$swapdev"' "$reset" || {
  echo "FAIL: reset does not resolve active swap identity by label."
  exit 1
}

grep -q 'swapoff training swap' "$reset" || {
  echo "FAIL: reset does not deactivate the resolved training swap device."
  exit 1
}

if grep -q 'grep -Fxq "\$swapdev"' "$reset"; then
  echo "FAIL: reset still compares swapon output to a friendly LVM path."
  exit 1
fi

echo "OK: reset deactivates OBJ08 swaps by active-device identity and label"
