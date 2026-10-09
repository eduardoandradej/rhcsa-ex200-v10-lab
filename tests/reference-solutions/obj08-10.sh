#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj08-10
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdd mklabel gpt
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdd mkpart pv2 1MiB 2049MiB
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdd set 1 lvm on
sudo udevadm settle --timeout=15
sudo timeout --signal=TERM --kill-after=2s 30s pvcreate /dev/vdd1 >/dev/null
sudo timeout --signal=TERM --kill-after=2s 30s vgextend rhcsa_vgextend /dev/vdd1 >/dev/null
sudo timeout --signal=TERM --kill-after=2s 30s lvcreate --yes --wipesignatures y -L 2G -n rhcsa_lvextra rhcsa_vgextend >/dev/null
sudo pvs > output/pvs.txt
sudo vgs > output/vgs.txt
sudo lvs > output/lvs.txt
EOS
