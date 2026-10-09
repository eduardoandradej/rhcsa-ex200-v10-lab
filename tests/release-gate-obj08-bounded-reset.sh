#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
reset="$ROOT/ansible/files/rhcsa-storage-reset"

echo "== OBJ08 bounded reset contract =="

grep -q 'TIMEOUT_SECONDS=15' "$reset" || {
  echo "FAIL: storage reset has no global bounded-command timeout."
  exit 1
}

grep -q 'udevadm settle --timeout=10' "$reset" || {
  echo "FAIL: storage reset still lacks a bounded udev settle."
  exit 1
}

grep -q 'partx -d' "$reset" || {
  echo "FAIL: storage reset lacks an explicit kernel partition removal step."
  exit 1
}

grep -q 'blockdev --rereadpt' "$reset" || {
  echo "FAIL: storage reset lacks an explicit partition-table reread."
  exit 1
}

grep -q 'for _ in $(seq 1 15)' "$reset" || {
  echo "FAIL: storage reset lacks a bounded verification loop."
  exit 1
}

grep -q 'STORAGE RESET: kernel still reports partitions' "$reset" || {
  echo "FAIL: storage reset does not expose useful failure diagnostics."
  exit 1
}

if grep -RPsn 'udevadm settle([[:space:]]*$|[[:space:]]*[;&|])' \
    "$ROOT/labs/08-storage" "$ROOT/tests/reference-solutions" \
    --include='*.yml' --include='*.sh' --include='*.md' 2>/dev/null; then
  echo "FAIL: unbounded udevadm settle remains in OBJ08 automation/docs."
  exit 1
fi

echo "OK: reset and OBJ08 udev synchronization are bounded"
