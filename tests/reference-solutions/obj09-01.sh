#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj09-01
uname -r > output/kernel.txt
cat /proc/cmdline > output/cmdline.txt
sudo grubby --default-kernel > output/default-kernel.txt
sudo grubby --info=ALL > output/grubby.txt
systemctl get-default > output/default-target.txt
EOS
