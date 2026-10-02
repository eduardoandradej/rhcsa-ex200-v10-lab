#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
kill -s STOP "$(cat /run/rhcsa-signal-alpha.pid)"
kill -s TERM "$(cat /run/rhcsa-signal-beta.pid)"
kill -s CONT "$(cat /run/rhcsa-signal-gamma.pid)"
sleep 0.2
EOS
