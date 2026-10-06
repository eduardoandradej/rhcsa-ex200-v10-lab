#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
solver="$ROOT/tests/reference-solutions/obj07-02.sh"

echo "== OBJ07 tmpfiles age semantics =="

if grep -Eq '^[[:space:]]*sudo[[:space:]]+touch[[:space:]].*-d[[:space:]]' "$solver"; then
    echo "FAIL: obj07-02 must not fake tmpfiles age with touch -d."
    exit 1
fi

grep -Eq '^[[:space:]]*sleep[[:space:]]+(3[1-9]|[4-9][0-9])[[:space:]]*$' "$solver" || {
    echo "FAIL: obj07-02 reference solver must let the 30s file actually age."
    exit 1
}

grep -q 'systemd-tmpfiles --clean /etc/tmpfiles.d/rhcsa-momentary.conf' "$solver" || {
    echo "FAIL: obj07-02 must clean using the specific training rule."
    exit 1
}

echo "OK: tmpfiles age is validated with real elapsed time"
