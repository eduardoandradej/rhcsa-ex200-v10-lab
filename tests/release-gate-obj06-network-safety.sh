#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
echo "== OBJ06 isolated-network safety =="
bad="$(grep -RInE 'nmcli[[:space:]].*(disconnect|delete|down).*(ens[0-9]|enp[0-9]|eth[0-9])|ip[[:space:]]+link[[:space:]]+del[[:space:]]+(ens|enp|eth)' "$ROOT/labs/06-networking" "$ROOT/tests/reference-solutions"/obj06-*.sh 2>/dev/null || true)"
if [[ -n "$bad" ]]; then echo "$bad"; echo 'FAIL: destructive action references likely management interface'; exit 1; fi
grep -Rqs 'ex200a' "$ROOT/labs/06-networking" || { echo 'FAIL: ex200a missing'; exit 1; }
grep -Rqs 'ex200b' "$ROOT/labs/06-networking" || { echo 'FAIL: ex200b missing'; exit 1; }
echo "OK: destructive network actions are confined to ex200a/ex200b"
