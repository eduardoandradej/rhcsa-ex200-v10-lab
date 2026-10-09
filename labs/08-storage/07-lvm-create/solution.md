```bash
cd /home/student/rhcsa-lab/obj08-07
sudo parted -s /dev/vdc mklabel gpt
sudo parted -s /dev/vdc mkpart lvm08 1MiB 4097MiB
sudo parted -s /dev/vdc set 1 lvm on
sudo udevadm settle --timeout=15
sudo pvcreate /dev/vdc1
sudo vgcreate rhcsa_vgdata /dev/vdc1
sudo lvcreate -L 1536M -n rhcsa_lvdata rhcsa_vgdata
sudo pvs > output/pvs.txt
sudo vgs > output/vgs.txt
sudo lvs > output/lvs.txt
```
