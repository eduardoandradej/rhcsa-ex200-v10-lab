#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj08-08
DEV=/dev/rhcsa_vgdata/rhcsa_lvdata
sudo timeout --signal=TERM --kill-after=2s 30s mkfs.xfs -f -L LVDATA08 "$DEV" >/dev/null
UUID=$(sudo blkid -s UUID -o value "$DEV")
echo "UUID=$UUID /lvdata xfs defaults 0 0" | sudo tee -a /etc/fstab >/dev/null
sudo systemctl daemon-reload
sudo timeout --signal=TERM --kill-after=2s 30s mount /lvdata
echo OBJ08-LVDATA | sudo tee /lvdata/marker.txt >/dev/null
findmnt --verify >/dev/null
findmnt /lvdata > output/findmnt.txt
lsblk -f > output/lsblk.txt
sudo lvs > output/lvs.txt
EOS
