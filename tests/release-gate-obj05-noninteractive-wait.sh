#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

echo "== OBJ05 non-interactive wait contract =="

targets=(
  "$ROOT/labs/05-processes-systemd/04-resource-hogs/setup.yml"
  "$ROOT/labs/05-processes-systemd/10-integrated-challenge/setup.yml"
)

for setup in "${targets[@]}"; do
  [[ -f "$setup" ]] || {
    echo "FAIL: missing ${setup#"$ROOT"/}"
    exit 1
  }

  if grep -q 'ansible\.builtin\.pause' "$setup"; then
    echo "FAIL: ${setup#"$ROOT"/} still uses ansible.builtin.pause."
    exit 1
  fi

  grep -q '/usr/bin/sleep' "$setup" || {
    echo "FAIL: ${setup#"$ROOT"/} has no non-interactive bounded wait."
    exit 1
  }
done

echo "OK: OBJ05 metric waits do not require a controller TTY"
