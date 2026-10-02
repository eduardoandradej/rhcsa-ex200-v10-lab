#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'sudo bash -Eeuo pipefail -s' <<'EOS'
useradd -u 2301 -c 'Operations Alpha' -s /bin/bash opsalpha
useradd -c 'Operations Beta' opsbeta
usermod -d /srv/opsbeta -m opsbeta
useradd opstemp
userdel -r opstemp
EOS
