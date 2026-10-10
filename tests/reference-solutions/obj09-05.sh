#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj09-05
UUID=$(sudo blkid -s UUID -o value /dev/vdb1)
sudo mkdir -p /srv/recovery09
sudo sed -i '\|[[:space:]]/srv/recovery09[[:space:]]|d' /etc/fstab
echo "UUID=$UUID /srv/recovery09 xfs defaults 0 0" | sudo tee -a /etc/fstab >/dev/null
sudo systemctl daemon-reload
sudo mount -a
sudo findmnt --verify > output/verify.txt
findmnt /srv/recovery09 > output/findmnt.txt
EOS
