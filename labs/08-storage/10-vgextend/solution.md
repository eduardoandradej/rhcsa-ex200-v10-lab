```bash
cd /home/student/rhcsa-lab/obj08-10
sudo parted -s /dev/vdd mklabel gpt
sudo parted -s /dev/vdd mkpart pv2 1MiB 2049MiB
sudo parted -s /dev/vdd set 1 lvm on
sudo udevadm settle --timeout=15
sudo pvcreate /dev/vdd1
sudo vgextend rhcsa_vgextend /dev/vdd1
sudo lvcreate -L 2G -n rhcsa_lvextra rhcsa_vgextend
sudo pvs > output/pvs.txt
sudo vgs > output/vgs.txt
sudo lvs > output/lvs.txt
```
