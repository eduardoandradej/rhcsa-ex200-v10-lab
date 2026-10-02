#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
f="$ROOT/tests/reference-solutions/obj05-06.sh"

echo "== OBJ05 TuneD verify contract =="

grep -q 'set +e' "$f" || {
    echo "FAIL: obj05-06 reference solver must tolerate diagnostic verify rc."
    exit 1
}

grep -q 'output/verify.rc' "$f" || {
    echo "FAIL: obj05-06 must preserve tuned-adm verify exit status."
    exit 1
}

grep -q "grep -q 'throughput-performance' output/active.txt" "$f" || {
    echo "FAIL: obj05-06 must validate the actual active profile."
    exit 1
}

echo "OK: TuneD verify is diagnostic; active profile remains the graded state"
