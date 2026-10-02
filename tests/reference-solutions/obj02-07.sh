#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'sudo bash -Eeuo pipefail -s' <<'EOS'
usermod -L -e 1 departed1
usermod -s /sbin/nologin serviceacct
usermod -e "$(date -d '+30 days' +%F)" tempcontract
usermod -U -e '' recoveruser
EOS
