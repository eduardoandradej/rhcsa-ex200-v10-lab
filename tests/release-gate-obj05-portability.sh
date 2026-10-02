#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

echo "== OBJ05 portable signal syntax =="

bad="$(
  grep -RInE \
    '(^|[[:space:]])kill[[:space:]]+-SIG[A-Z]+' \
    "$ROOT/labs/05-processes-systemd" \
    --include='*.yml' || true
)"

if [[ -n "$bad" ]]; then
    echo "$bad"
    echo "FAIL: Ansible shell tasks must not depend on builtin kill -SIG* syntax."
    exit 1
fi

echo "OK: no non-portable kill -SIG* form in OBJ05 Ansible YAML"
