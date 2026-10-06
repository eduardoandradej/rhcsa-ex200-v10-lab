#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

echo "== OBJ06 NetworkManager keyfile permission contract =="

grader="$ROOT/labs/06-networking/05-keyfile-edit/grade.py"

grep -q 'sudo", "-n", "cat"' "$grader" || {
    echo "FAIL: obj06-05 grader must inspect root-only keyfile through sudo -n."
    exit 1
}

if grep -Eq 'Path\("/etc/NetworkManager/system-connections/.*\.nmconnection"\).*read_text' "$grader"; then
    echo "FAIL: grader directly reads a root-only NetworkManager keyfile."
    exit 1
fi

echo "OK: root-only NetworkManager keyfiles are inspected through privileged read"
