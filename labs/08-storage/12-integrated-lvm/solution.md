```bash
cd /home/student/rhcsa-lab/obj08-12

sudo parted -s /dev/vdc mklabel gpt
sudo parted -s /dev/vdc mkpart pv1 1MiB 4097MiB
sudo parted -s /dev/vdc set 1 lvm on

sudo parted -s /dev/vdd mklabel gpt
sudo parted -s /dev/vdd mkpart pv2 1MiB 2561MiB
sudo parted -s /dev/vdd set 1 lvm on
sudo udevadm settle --timeout=15

sudo pvcreate /dev/vdc1 /dev/vdd1
sudo vgcreate rhcsa_vgfinal /dev/vdc1 /dev/vdd1
sudo lvcreate -L 2G -n rhcsa_data rhcsa_vgfinal
sudo lvcreate -L 512M -n rhcsa_swap rhcsa_vgfinal

sudo mkfs.xfs -f -L FINAL08 /dev/rhcsa_vgfinal/rhcsa_data
DUUID=$(sudo blkid -s UUID -o value /dev/rhcsa_vgfinal/rhcsa_data)
echo "UUID=$DUUID /lvfinal xfs defaults 0 0" | sudo tee -a /etc/fstab
sudo systemctl daemon-reload
sudo mount /lvfinal
echo OBJ08-FINAL | sudo tee /lvfinal/marker.txt

sudo mkswap -L FINALSWAP08 /dev/rhcsa_vgfinal/rhcsa_swap
SUUID=$(sudo blkid -s UUID -o value /dev/rhcsa_vgfinal/rhcsa_swap)
echo "UUID=$SUUID none swap defaults 0 0" | sudo tee -a /etc/fstab
sudo swapon /dev/rhcsa_vgfinal/rhcsa_swap

sudo lvextend -L 3G /dev/rhcsa_vgfinal/rhcsa_data
sudo xfs_growfs /lvfinal
findmnt --verify

sudo pvs > output/pvs.txt
sudo vgs > output/vgs.txt
sudo lvs > output/lvs.txt
findmnt /lvfinal > output/findmnt.txt
swapon --show > output/swapon.txt
df -h /lvfinal > output/df.txt
```
