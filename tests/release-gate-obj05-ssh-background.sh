#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

echo "== OBJ05 SSH background process safety =="

for f in \
  "$ROOT/tests/reference-solutions/obj05-02.sh" \
  "$ROOT/tests/reference-solutions/obj05-05.sh" \
  "$ROOT/tests/reference-solutions/obj05-10.sh"
do
    grep -q '>/dev/null 2>&1 &' "$f" || {
        echo "FAIL: background process still owns SSH output descriptors: $f"
        exit 1
    }
done

f="$ROOT/tests/reference-solutions/obj05-02.sh"
grep -q 'rhcsa-job-alpha\\*' "$f" || {
    echo "FAIL: obj05-02 lacks exec() race protection."
    exit 1
}
grep -q 'Second SSH session' "$f" || {
    echo "FAIL: obj05-02 must restore STOP after the job-control shell exits."
    exit 1
}

echo "OK: background jobs are SSH-safe and obj05-02 handles orphaned stopped process groups"
