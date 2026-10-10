#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj09-03
sudo systemctl set-default multi-user.target
systemctl get-default > output/default-target.txt
EOS
