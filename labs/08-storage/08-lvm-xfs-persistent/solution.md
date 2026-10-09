```bash
cd /home/student/rhcsa-lab/obj08-08
DEV=/dev/rhcsa_vgdata/rhcsa_lvdata
sudo mkfs.xfs -f -L LVDATA08 "$DEV"
UUID=$(sudo blkid -s UUID -o value "$DEV")
echo "UUID=$UUID /lvdata xfs defaults 0 0" | sudo tee -a /etc/fstab
sudo systemctl daemon-reload
sudo mount /lvdata
echo OBJ08-LVDATA | sudo tee /lvdata/marker.txt
findmnt --verify
findmnt /lvdata > output/findmnt.txt
lsblk -f > output/lsblk.txt
sudo lvs > output/lvs.txt
```
