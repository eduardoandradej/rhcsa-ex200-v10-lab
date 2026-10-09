#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

echo "== OBJ08 target contract =="

count=0
for f in "$ROOT/labs/08-storage"/*/lab.yml; do
  count=$((count+1))
  grep -q '^target: \[servera\]$' "$f" || {
    echo "FAIL: OBJ08 destructive scope must stay on snapshot-tested servera: $f"
    exit 1
  }
done

[[ "$count" -eq 12 ]] || {
  echo "FAIL: expected 12 OBJ08 labs, got $count"
  exit 1
}

echo "OK: 12 labs, all constrained to servera"
