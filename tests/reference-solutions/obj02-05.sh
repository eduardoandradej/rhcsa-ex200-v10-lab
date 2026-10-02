#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'sudo bash -Eeuo pipefail -s' <<'EOS'
printf 'aginguser1:redhat\naginguser2:redhat\n' | chpasswd
chage -m 2 -M 45 -W 7 -I 5 aginguser1
chage -d 0 aginguser1
chage -M 90 aginguser2
chage -E "$(date -d '+90 days' +%F)" aginguser2
EOS
