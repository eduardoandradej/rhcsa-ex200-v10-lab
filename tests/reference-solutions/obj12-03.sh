#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
sudo parted -s /dev/vdb mklabel gpt
sudo parted -s /dev/vdb mkpart primary 1MiB 3073MiB
sudo partprobe /dev/vdb || true
sudo udevadm settle --timeout=15 || true
for i in $(seq 1 15); do test -b /dev/vdb1 && break; sleep 1; done
test -b /dev/vdb1
sudo pvcreate -ff -y /dev/vdb1
sudo vgcreate vg12 /dev/vdb1
sudo lvcreate --yes --wipesignatures y -L 1024M -n lvdata vg12
sudo mkfs.xfs -f -L DATA12 /dev/vg12/lvdata
sudo lvextend -L +512M /dev/vg12/lvdata
sudo mkdir -p /srv/data12
DATA_UUID=$(sudo blkid -s UUID -o value /dev/vg12/lvdata)
echo "UUID=$DATA_UUID /srv/data12 xfs defaults 0 0" | sudo tee -a /etc/fstab >/dev/null
sudo lvcreate --yes --wipesignatures y -L 512M -n lvswap vg12
sudo mkswap -L SWAP12 /dev/vg12/lvswap
SWAP_UUID=$(sudo blkid -s UUID -o value /dev/vg12/lvswap)
echo "UUID=$SWAP_UUID none swap defaults 0 0" | sudo tee -a /etc/fstab >/dev/null
sudo systemctl daemon-reload
sudo mount -a
sudo xfs_growfs /srv/data12
sudo swapon -a
cd /home/student/rhcsa-lab/obj12-03
lsblk -f /dev/vdb > output/lsblk.txt
{ sudo pvs; sudo vgs; sudo lvs; } > output/lvm.txt
findmnt /srv/data12 > output/findmnt.txt
cat /proc/swaps > output/swap.txt
sudo findmnt --verify > output/verify.txt 2>&1
EOS
