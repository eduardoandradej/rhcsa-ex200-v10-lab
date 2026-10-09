#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj08-02
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdb mklabel gpt
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdb mkpart data08 xfs 1MiB 1025MiB
sudo udevadm settle --timeout=15
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdb unit MiB print > output/parted.txt
lsblk -o NAME,SIZE,TYPE,FSTYPE,PARTLABEL /dev/vdb > output/lsblk.txt
EOS
