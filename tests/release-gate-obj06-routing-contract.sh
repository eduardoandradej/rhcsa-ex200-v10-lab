#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

echo "== OBJ06 NetworkManager routing contract =="

solver="$ROOT/tests/reference-solutions/obj06-03.sh"
grader="$ROOT/labs/06-networking/03-modify-secondary-ip/grade.py"

grep -q 'ipv4.never-default yes' "$solver" || {
    echo "FAIL: obj06-03 must set ipv4.never-default yes."
    exit 1
}

if grep -Eq 'ipv4\.gateway[[:space:]]+10\.66\.3\.254' "$solver"; then
    echo "FAIL: obj06-03 must not combine never-default=yes with a gateway."
    exit 1
fi

grep -q 'ipv4.gateway ""' "$solver" || {
    echo "FAIL: obj06-03 must explicitly clear any gateway."
    exit 1
}

grep -q 'gateway in ("", "--")' "$grader" || {
    echo "FAIL: grader must expect an empty gateway with never-default=yes."
    exit 1
}

echo "OK: obj06-03 respects NetworkManager never-default/gateway semantics"
