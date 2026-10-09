#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj08-12
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdc mklabel gpt
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdc mkpart pv1 1MiB 4097MiB
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdc set 1 lvm on
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdd mklabel gpt
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdd mkpart pv2 1MiB 2561MiB
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdd set 1 lvm on
sudo udevadm settle --timeout=15
sudo timeout --signal=TERM --kill-after=2s 30s pvcreate /dev/vdc1 /dev/vdd1 >/dev/null
sudo timeout --signal=TERM --kill-after=2s 30s vgcreate rhcsa_vgfinal /dev/vdc1 /dev/vdd1 >/dev/null
sudo timeout --signal=TERM --kill-after=2s 30s lvcreate --yes --wipesignatures y -L 2G -n rhcsa_data rhcsa_vgfinal >/dev/null
sudo timeout --signal=TERM --kill-after=2s 30s lvcreate --yes --wipesignatures y -L 512M -n rhcsa_swap rhcsa_vgfinal >/dev/null
sudo timeout --signal=TERM --kill-after=2s 30s mkfs.xfs -f -L FINAL08 /dev/rhcsa_vgfinal/rhcsa_data >/dev/null
DUUID=$(sudo blkid -s UUID -o value /dev/rhcsa_vgfinal/rhcsa_data)
echo "UUID=$DUUID /lvfinal xfs defaults 0 0" | sudo tee -a /etc/fstab >/dev/null
sudo systemctl daemon-reload
sudo timeout --signal=TERM --kill-after=2s 30s mount /lvfinal
echo OBJ08-FINAL | sudo tee /lvfinal/marker.txt >/dev/null
sudo timeout --signal=TERM --kill-after=2s 30s mkswap -L FINALSWAP08 /dev/rhcsa_vgfinal/rhcsa_swap >/dev/null
SUUID=$(sudo blkid -s UUID -o value /dev/rhcsa_vgfinal/rhcsa_swap)
echo "UUID=$SUUID none swap defaults 0 0" | sudo tee -a /etc/fstab >/dev/null
sudo swapon /dev/rhcsa_vgfinal/rhcsa_swap
sudo timeout --signal=TERM --kill-after=2s 30s lvextend -L 3G /dev/rhcsa_vgfinal/rhcsa_data >/dev/null
sudo timeout --signal=TERM --kill-after=2s 30s xfs_growfs /lvfinal >/dev/null
findmnt --verify >/dev/null
sudo pvs > output/pvs.txt
sudo vgs > output/vgs.txt
sudo lvs > output/lvs.txt
findmnt /lvfinal > output/findmnt.txt
swapon --show > output/swapon.txt
df -h /lvfinal > output/df.txt
EOS
