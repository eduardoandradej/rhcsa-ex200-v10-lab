```bash
cd /home/student/rhcsa-lab/obj08-11
sudo parted -s /dev/vde mklabel gpt
sudo parted -s /dev/vde mkpart pvswap 1MiB 1537MiB
sudo parted -s /dev/vde set 1 lvm on
sudo udevadm settle --timeout=15
sudo pvcreate /dev/vde1
sudo vgcreate rhcsa_vgswap /dev/vde1
sudo lvcreate -L 768M -n rhcsa_lvswap rhcsa_vgswap
sudo mkswap -L LVSWAP08 /dev/rhcsa_vgswap/rhcsa_lvswap
sudo swapon /dev/rhcsa_vgswap/rhcsa_lvswap
UUID=$(sudo blkid -s UUID -o value /dev/rhcsa_vgswap/rhcsa_lvswap)
echo "UUID=$UUID none swap defaults 0 0" | sudo tee -a /etc/fstab
sudo systemctl daemon-reload
sudo pvs > output/pvs.txt
sudo vgs > output/vgs.txt
sudo lvs > output/lvs.txt
swapon --show > output/swapon.txt
```
