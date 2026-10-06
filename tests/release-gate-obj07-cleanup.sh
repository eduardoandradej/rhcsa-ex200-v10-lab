#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
echo "== OBJ07 cleanup contract =="
for a in rhcsa-momentary.conf rhcsa-report rhcsa-debug.conf rhcsa-journal.service 99-rhcsa-persistent.conf rhcsa-audit.service rhcsa-audit.timer rhcsa-audit.conf; do grep -Rqs "$a" "$ROOT/labs/07-scheduling-logs"/*/finish.yml || { echo "FAIL: cleanup missing for $a"; exit 1; }; done
echo "OK: cleanup coverage present"
