#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
grader="$ROOT/labs/08-storage/02-gpt-partition/grade.py"

echo "== OBJ08-02 partition grader contract =="

[[ -f "$grader" ]] || {
  echo "FAIL: obj08-02 grader is missing."
  exit 1
}

grep -q '"sudo", "-n", "parted", "-sm"' "$grader" || {
  echo "FAIL: grader must inspect GPT metadata with privileged machine-readable parted."
  exit 1
}

grep -q 'part_name = partition\[5\]' "$grader" || {
  echo "FAIL: GPT partition name must come from parted metadata."
  exit 1
}

if grep -q '"PARTLABEL"' "$grader"; then
  echo "FAIL: grader must not depend on lsblk PARTLABEL visibility."
  exit 1
fi

grep -q '"sudo", "-n", "lsblk"' "$grader" || {
  echo "FAIL: filesystem/topology inspection must use privileged lsblk."
  exit 1
}

echo "OK: OBJ08-02 grades GPT name/size from parted and uses privileged lsblk for filesystem state"
