```bash
cd /home/student/rhcsa-lab/obj08-06
sudo parted -s /dev/vdb mklabel gpt
sudo parted -s /dev/vdb mkpart basicdata xfs 1MiB 2049MiB
sudo parted -s /dev/vdb mkpart basicswap linux-swap 2049MiB 3073MiB
sudo udevadm settle --timeout=15

sudo mkfs.xfs -f -L BASIC08 /dev/vdb1
sudo mkswap -L BASWAP08 /dev/vdb2

U1=$(sudo blkid -s UUID -o value /dev/vdb1)
U2=$(sudo blkid -s UUID -o value /dev/vdb2)
echo "UUID=$U1 /basicdata xfs defaults 0 0" | sudo tee -a /etc/fstab
echo "UUID=$U2 none swap defaults 0 0" | sudo tee -a /etc/fstab

sudo systemctl daemon-reload
sudo mount /basicdata
sudo swapon /dev/vdb2
echo OBJ08-BASIC | sudo tee /basicdata/marker.txt
findmnt --verify

sudo parted -s /dev/vdb unit MiB print > output/parted.txt
lsblk -f /dev/vdb > output/lsblk.txt
findmnt /basicdata > output/findmnt.txt
swapon --show > output/swapon.txt
```
