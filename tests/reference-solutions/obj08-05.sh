#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj08-05
sudo timeout --signal=TERM --kill-after=2s 30s mkswap -L RHCSA08SWAP /dev/vde1 >/dev/null
sudo swapon /dev/vde1
UUID=$(sudo blkid -s UUID -o value /dev/vde1)
echo "UUID=$UUID none swap defaults 0 0" | sudo tee -a /etc/fstab >/dev/null
sudo systemctl daemon-reload
swapon --show > output/swapon.txt
free -h > output/free.txt
findmnt --verify >/dev/null
EOS
