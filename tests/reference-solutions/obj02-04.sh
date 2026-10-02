#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'sudo bash -Eeuo pipefail -s' <<'EOS'
usermod -aG projecta teamuser1
usermod -aG projecta teamuser2
usermod -g projectb teamuser2
runuser -u teamuser1 -- sg projecta -c 'touch /home/teamuser1/projecta-owned.txt'
EOS
