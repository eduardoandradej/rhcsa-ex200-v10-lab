#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj07-07
sudo timedatectl set-timezone America/Jamaica
sudo timedatectl set-ntp true
sudo systemctl enable --now chronyd
timedatectl > output/timedatectl.txt
chronyc sources -v > output/sources.txt
chronyc tracking > output/tracking.txt
EOS
