#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj08-06
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdb mklabel gpt
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdb mkpart basicdata xfs 1MiB 2049MiB
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdb mkpart basicswap linux-swap 2049MiB 3073MiB
sudo udevadm settle --timeout=15
sudo timeout --signal=TERM --kill-after=2s 30s mkfs.xfs -f -L BASIC08 /dev/vdb1 >/dev/null
sudo timeout --signal=TERM --kill-after=2s 30s mkswap -L BASWAP08 /dev/vdb2 >/dev/null
U1=$(sudo blkid -s UUID -o value /dev/vdb1)
U2=$(sudo blkid -s UUID -o value /dev/vdb2)
echo "UUID=$U1 /basicdata xfs defaults 0 0" | sudo tee -a /etc/fstab >/dev/null
echo "UUID=$U2 none swap defaults 0 0" | sudo tee -a /etc/fstab >/dev/null
sudo systemctl daemon-reload
sudo timeout --signal=TERM --kill-after=2s 30s mount /basicdata
sudo swapon /dev/vdb2
echo OBJ08-BASIC | sudo tee /basicdata/marker.txt >/dev/null
findmnt --verify >/dev/null
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdb unit MiB print > output/parted.txt
lsblk -f /dev/vdb > output/lsblk.txt
findmnt /basicdata > output/findmnt.txt
swapon --show > output/swapon.txt
EOS
