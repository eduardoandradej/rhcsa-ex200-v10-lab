#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

echo "== OBJ05 process ownership contract =="

for f in \
  "$ROOT/labs/05-processes-systemd/03-signals/setup.yml" \
  "$ROOT/labs/05-processes-systemd/04-resource-hogs/setup.yml" \
  "$ROOT/labs/05-processes-systemd/10-integrated-challenge/setup.yml"
do
    grep -q 'become_user: student' "$f" || {
        echo "FAIL: process controlled by student is not student-owned: $f"
        exit 1
    }
done

echo "OK: student-controlled training processes are student-owned"
