#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj08-11
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vde mklabel gpt
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vde mkpart pvswap 1MiB 1537MiB
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vde set 1 lvm on
sudo udevadm settle --timeout=15
sudo timeout --signal=TERM --kill-after=2s 30s pvcreate /dev/vde1 >/dev/null
sudo timeout --signal=TERM --kill-after=2s 30s vgcreate rhcsa_vgswap /dev/vde1 >/dev/null
sudo timeout --signal=TERM --kill-after=2s 30s lvcreate --yes --wipesignatures y -L 768M -n rhcsa_lvswap rhcsa_vgswap >/dev/null
sudo timeout --signal=TERM --kill-after=2s 30s mkswap -L LVSWAP08 /dev/rhcsa_vgswap/rhcsa_lvswap >/dev/null
sudo swapon /dev/rhcsa_vgswap/rhcsa_lvswap
UUID=$(sudo blkid -s UUID -o value /dev/rhcsa_vgswap/rhcsa_lvswap)
echo "UUID=$UUID none swap defaults 0 0" | sudo tee -a /etc/fstab >/dev/null
sudo systemctl daemon-reload
sudo pvs > output/pvs.txt
sudo vgs > output/vgs.txt
sudo lvs > output/lvs.txt
swapon --show > output/swapon.txt
EOS
