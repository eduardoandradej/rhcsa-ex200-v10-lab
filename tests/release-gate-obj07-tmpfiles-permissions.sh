#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
grader="$ROOT/labs/07-scheduling-logs/02-tmpfiles/grade.py"

echo "== OBJ07 tmpfiles permission contract =="

grep -q 'sudo", "-n", "test", "!", "-e"' "$grader" || {
    echo "FAIL: obj07-02 must inspect stale.txt existence with privilege."
    exit 1
}

if grep -Eq 'Path\("/run/rhcsa-momentary/stale\.txt"\)\.exists\(\)' "$grader"; then
    echo "FAIL: obj07-02 directly stats a child below root-only 0700 directory."
    exit 1
fi

echo "OK: root-only tmpfiles child existence is checked with sudo -n test"
