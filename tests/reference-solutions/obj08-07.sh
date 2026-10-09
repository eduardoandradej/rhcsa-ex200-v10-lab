#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj08-07
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdc mklabel gpt
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdc mkpart lvm08 1MiB 4097MiB
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdc set 1 lvm on
sudo udevadm settle --timeout=15
sudo timeout --signal=TERM --kill-after=2s 30s pvcreate /dev/vdc1 >/dev/null
sudo timeout --signal=TERM --kill-after=2s 30s vgcreate rhcsa_vgdata /dev/vdc1 >/dev/null
sudo timeout --signal=TERM --kill-after=2s 30s lvcreate --yes --wipesignatures y -L 1536M -n rhcsa_lvdata rhcsa_vgdata >/dev/null
sudo pvs > output/pvs.txt
sudo vgs > output/vgs.txt
sudo lvs > output/lvs.txt
EOS
