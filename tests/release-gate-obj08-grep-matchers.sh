#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

echo "== OBJ08 grep matcher contract =="

bad="$(
  grep -Rns --include='release-gate-obj08-*.sh' \
    -E 'grep[[:space:]]+-[A-Za-z]*P[A-Za-z]*E|grep[[:space:]]+-[A-Za-z]*E[A-Za-z]*P' \
    "$ROOT/tests" || true
)"

if [[ -n "$bad" ]]; then
  echo "$bad"
  echo "FAIL: a release gate combines incompatible grep -P and -E matchers."
  exit 1
fi

echo "OK: OBJ08 release gates use one grep matcher mode at a time"
