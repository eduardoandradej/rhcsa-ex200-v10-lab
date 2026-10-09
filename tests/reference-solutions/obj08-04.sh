#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj08-04
UUID=$(sudo blkid -s UUID -o value /dev/vdb1)
echo "UUID=$UUID /data1 xfs defaults 0 0" | sudo tee -a /etc/fstab >/dev/null
sudo systemctl daemon-reload
sudo timeout --signal=TERM --kill-after=2s 30s mount /data1
findmnt --verify > output/verify.txt
findmnt /data1 > output/findmnt.txt
EOS
