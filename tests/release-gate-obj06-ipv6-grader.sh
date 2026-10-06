#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

echo "== OBJ06 IPv6 grader contract =="

for f in \
  "$ROOT/labs/06-networking/04-dual-stack/grade.py" \
  "$ROOT/labs/06-networking/08-integrated-challenge/grade.py"
do
    grep -q '"--escape", "no", "-g"' "$f" || {
        echo "FAIL: IPv6 grader still uses escaped nmcli terse output: $f"
        exit 1
    }
done

echo "OK: IPv6 graders read nmcli values with escaping disabled"
