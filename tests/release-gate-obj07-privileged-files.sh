#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
echo "== OBJ07 privileged-file grader contract =="
for f in "$ROOT/labs/07-scheduling-logs/01-systemd-timers/grade.py" "$ROOT/labs/07-scheduling-logs/03-system-cron/grade.py" "$ROOT/labs/07-scheduling-logs/04-rsyslog-routing/grade.py" "$ROOT/labs/07-scheduling-logs/06-persistent-journal/grade.py" "$ROOT/labs/07-scheduling-logs/08-integrated-challenge/grade.py"; do grep -q 'sudo' "$f" || { echo "FAIL: privileged inspection missing in $f"; exit 1; }; done
echo "OK: privileged state inspection present"
